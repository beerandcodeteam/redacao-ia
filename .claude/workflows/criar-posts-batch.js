export const meta = {
  name: 'criar-posts-batch',
  description: 'Cria posts do blog Beer & Code em batch a partir de um markdown (h2 = post), seguindo a skill criar-post-blog em modo autônomo',
  whenToUse:
    'Quando o usuário quiser gerar vários posts de uma vez a partir de um arquivo .md com blocos `## Título`. Equivale ao scripts/criar-posts-batch.py, mas com paralelismo, resume granular e o passo de áudio (Haiku) como estágio próprio.',
  phases: [
    { title: 'Parse', detail: 'lê o .md e quebra em posts (1 por h2)' },
    { title: 'Pesquisa+Escrita', detail: 'pesquisa, outline e body por post (skill passos 1-3)' },
    { title: 'Roteiro', detail: 'reescrita narrável via subagent roteiro-narracao (Haiku)', model: 'haiku' },
    { title: 'Capa+Audio+Publicar', detail: 'generate-cover.sh, generate-audio.sh e CreatePost (scheduled) via MCP' },
  ],
}

// ───────────────────────── args ─────────────────────────
// Passe via Workflow({ name: 'criar-posts-batch', args: {...} }):
//   file:    caminho do markdown (obrigatório)
//   cta:     { url, label, pitch }     (opcional — aplica a todos os posts)
//   from:    índice 1-based pra retomar (opcional)        // equivale a --from
//   only:    índice 1-based pra rodar só 1 post (opcional)// equivale a --only
//   dryRun:  true → para depois do Parse e devolve os prompts // equivale a --dry-run
//   withAudio: false → pula roteiro+TTS (rascunho)        // default true (batch)
// o runtime entrega `args` como string JSON — parseia se necessário
let A = typeof args === 'string' ? JSON.parse(args) : args || {}
if (!A.file) throw new Error('args.file é obrigatório (caminho do markdown com os posts)')
const WITH_AUDIO = A.withAudio !== false

// OmniVoice (TTS) é pesado e roda local — não dá pra ter N rodando juntos.
// Por isso o batch processa em chunks. Suba se a máquina aguentar; o teto
// global do runtime ainda é min(16, cores-2).
const CONCURRENCY = 3

// ───────────────────────── schemas ─────────────────────────
const POSTS_SCHEMA = {
  type: 'object',
  required: ['posts'],
  properties: {
    posts: {
      type: 'array',
      items: {
        type: 'object',
        required: ['titulo', 'publicar_em'],
        properties: {
          titulo: { type: 'string' },
          publicar_em: { type: 'string', description: 'ISO8601 com offset -03:00' },
          resumo: { type: 'string' },
          categoria: { type: 'string' },
          autor: { type: 'string' },
          tags: { type: 'string' },
          hook: { type: 'string', description: 'gancho/lead no tom da marca' },
          bullets: { type: 'array', items: { type: 'string' }, description: 'H2 previstos do post' },
          keyword_principal: { type: 'string' },
          keywords_secundarias: { type: 'string' },
          volume: { type: 'string', description: 'notas de SEO: volume, KD, canibalização, links internos' },
        },
      },
    },
  },
}

const DRAFT_SCHEMA = {
  type: 'object',
  required: ['slug', 'title', 'body', 'category_slug', 'author_slug', 'published_at', 'cover_prompt'],
  properties: {
    slug: { type: 'string' },
    title: { type: 'string' },
    body: { type: 'string', description: 'Markdown completo do post' },
    excerpt: { type: 'string' },
    category_slug: { type: 'string' },
    author_slug: { type: 'string' },
    tags: { type: 'array', items: { type: 'string' } },
    published_at: { type: 'string' },
    cover_prompt: { type: 'string', description: 'prompt detalhado pra generate-cover.sh' },
  },
}

const SCRIPT_SCHEMA = {
  type: 'object',
  required: ['audio_script_path', 'word_count'],
  properties: {
    audio_script_path: { type: 'string' },
    word_count: { type: 'number' },
  },
}

const RESULT_SCHEMA = {
  type: 'object',
  required: ['slug', 'status'],
  properties: {
    slug: { type: 'string' },
    title: { type: 'string' },
    published_at: { type: 'string' },
    status: { type: 'string', enum: ['scheduled', 'draft', 'error'] },
    cover_url: { type: 'string' },
    audio_url: { type: 'string' },
    note: { type: 'string' },
  },
}

// ───────────────────────── helpers ─────────────────────────
function ctaBlock(cta) {
  if (!cta || !cta.url) return ''
  return [
    '',
    'CTA embutido — convite ao destino abaixo, integrado de forma orgânica ao corpo:',
    `- URL: ${cta.url}`,
    cta.label ? `- Nome do destino: ${cta.label}` : '',
    cta.pitch ? `- Contexto/pitch: ${cta.pitch}` : '',
    '',
    'Regras (obrigatórias): nada de heading dedicado (`## CTA`, `## Inscreva-se`), sem caixa/blockquote/`---` ao redor; 1–2 frases em prosa normal, link inline `[nome](url)`, tom de convite curto, sem hard sell.',
    'Posicionamento: no PRIMEIRO TERÇO do post (~30% da leitura), tipicamente fechando o bloco de contexto, no trecho que mais conversa com o destino. A conclusão é fallback só quando não houver encaixe natural antes.',
    'Se o destino for o Clã Beer and Code ou um evento da marca, LEIA `.claude/skills/montar-cta-pitch/SKILL.md` e siga o ângulo/nível de pitch de lá.',
  ]
    .filter(Boolean)
    .join('\n')
}

function writePrompt(post, idx, cta) {
  return [
    `Crie um post completo do blog Beer & Code seguindo o pipeline da skill em \`.claude/skills/criar-post-blog/SKILL.md\` (LEIA o arquivo primeiro).`,
    '',
    `Tema: ${post.titulo}`,
    `Data de publicação: ${post.publicar_em}`,
    post.resumo ? `Ângulo/resumo: ${post.resumo}` : '',
    post.categoria ? `Categoria sugerida: ${post.categoria}` : '',
    post.autor ? `Autor: ${post.autor}` : '',
    post.tags ? `Tags sugeridas: ${post.tags}` : '',
    post.hook ? `Hook (use como lead, no tom da marca): ${post.hook}` : '',
    post.bullets && post.bullets.length
      ? `H2 previstos (use como espinha dorsal do outline; ajuste a redação, mantenha a cobertura):\n${post.bullets.map((b) => `  - ${b}`).join('\n')}`
      : '',
    post.keyword_principal ? `Keyword principal (deve aparecer no title, no 1º parágrafo, num H2 e no slug): ${post.keyword_principal}` : '',
    post.keywords_secundarias ? `Keywords secundárias (distribua naturalmente): ${post.keywords_secundarias}` : '',
    post.volume ? `Notas de SEO da pauta (respeite — inclui canibalização e links internos obrigatórios): ${post.volume}` : '',
    ctaBlock(cta),
    '',
    'MODO BATCH AUTÔNOMO — execute os passos 1 a 3 da skill (pesquisa → outline → escrita) SEM aguardar confirmação humana. Aplique defaults sensatos. Para categoria/autor use ListCategories/ListAuthors do MCP beer-and-code-blog e escolha o mais adequado (não pergunte).',
    'NÃO gere capa, NÃO gere áudio e NÃO publique neste estágio. Apenas devolva o draft estruturado (incluindo o body em Markdown e um cover_prompt detalhado para a capa 16:9).',
  ]
    .filter(Boolean)
    .join('\n')
}

// ───────────────────────── 1. Parse ─────────────────────────
phase('Parse')
const parsed = await agent(
  `Leia o arquivo markdown em "${A.file}". Quebre em posts: cada heading h2 (\`## Título\`) inicia um post. ` +
    `O texto do h2 é \`titulo\`. Bullets do bloco no formato \`- chave: valor\` viram campos (publicar_em/data/publish_at → publicar_em; resumo; categoria; autor; tags). ` +
    `Linhas livres sem bullet viram \`resumo\` se ele não foi declarado. ` +
    `Cada post PRECISA de publicar_em (ISO8601 com offset -03:00) — se faltar, registre mesmo assim e eu trato. Devolva todos os posts na ordem do arquivo.`,
  { schema: POSTS_SCHEMA, phase: 'Parse' },
)

let posts = (parsed.posts || []).map((p, i) => ({ ...p, _idx: i + 1 }))
// filtros equivalentes a --from / --only
if (A.from) posts = posts.filter((p) => p._idx >= A.from)
if (A.only) posts = posts.filter((p) => p._idx === A.only)

log(`${posts.length} post(s) selecionado(s) de ${(parsed.posts || []).length} no arquivo`)

const semData = posts.filter((p) => !p.publicar_em)
if (semData.length) log(`⚠ ${semData.length} sem publicar_em — serão pulados: ${semData.map((p) => p.titulo).join('; ')}`)
posts = posts.filter((p) => p.publicar_em)

if (A.dryRun) {
  log('dry-run: devolvendo prompts sem criar nada')
  return posts.map((p) => ({ titulo: p.titulo, publicar_em: p.publicar_em, prompt: writePrompt(p, p._idx, A.cta) }))
}

// ───────────── 2-4. pipeline por post, em chunks (TTS é pesado) ─────────────
const results = []
for (let start = 0; start < posts.length; start += CONCURRENCY) {
  const chunk = posts.slice(start, start + CONCURRENCY)
  log(`processando posts ${chunk[0]._idx}..${chunk[chunk.length - 1]._idx}`)

  const chunkResults = await pipeline(
    chunk,
    // ── estágio 1: pesquisa + escrita (skill passos 1-3) ──
    (post) => agent(writePrompt(post, post._idx, A.cta), {
      label: `escrita:${post.titulo.slice(0, 40)}`,
      phase: 'Pesquisa+Escrita',
      schema: DRAFT_SCHEMA,
    }),

    // ── estágio 2: roteiro narrável em Haiku (skill passo 5.1) ──
    (draft) =>
      !WITH_AUDIO
        ? { ...draft, audio_script_path: null }
        : agent(
            `Reescreva o body abaixo em texto narrável e salve em /tmp/audio-script-${draft.slug}.txt.\n\n` +
              `slug: ${draft.slug}\ntitle: ${draft.title}\nexcerpt: ${draft.excerpt || ''}\n\nbody:\n${draft.body}`,
            { agentType: 'roteiro-narracao', label: `roteiro:${draft.slug}`, phase: 'Roteiro', schema: SCRIPT_SCHEMA },
          ).then((s) => ({ ...draft, audio_script_path: s.audio_script_path })),

    // ── estágio 3: capa + áudio + CreatePost (scheduled) via MCP ──
    (d) =>
      agent(
        [
          `Finalize a publicação do post "${d.title}" (slug ${d.slug}) seguindo os passos 4-6 da skill \`.claude/skills/criar-post-blog/SKILL.md\`. MODO BATCH AUTÔNOMO, sem confirmação humana.`,
          '',
          `1. Capa: rode \`.claude/skills/criar-post-blog/scripts/generate-cover.sh "${d.cover_prompt}" /tmp/cover-${d.slug}.png\` e capture a URL pública (última linha do stdout).`,
          WITH_AUDIO && d.audio_script_path
            ? `2. Áudio: rode \`.claude/skills/criar-post-blog/scripts/generate-audio.sh ${d.audio_script_path} ${d.slug}\` e capture a audio_url (última linha do stdout).`
            : '2. Áudio: PULAR (rascunho sem áudio).',
          `3. Publicação MCP beer-and-code-blog: UploadImage(url=<url da capa>) → guarde o path. Depois CreatePost com title, body, category_slug=${d.category_slug}, author_slug=${d.author_slug}, published_at=${d.published_at}, tags, excerpt, cover_image_path=<path>${WITH_AUDIO && d.audio_script_path ? ', audio_url=<url do mp3>' : ''}. Status default scheduled. NÃO chame PublishPost.`,
          '',
          `body do post (use exatamente este):\n${d.body}`,
          '',
          'Devolva o resultado estruturado (slug, status, cover_url, audio_url, published_at).',
        ]
          .filter(Boolean)
          .join('\n'),
        { label: `publicar:${d.slug}`, phase: 'Capa+Audio+Publicar', schema: RESULT_SCHEMA },
      ),
  )

  results.push(...chunkResults.filter(Boolean))
}

const ok = results.filter((r) => r.status === 'scheduled')
log(`✓ batch concluído — ${ok.length}/${posts.length} agendados`)
return results
