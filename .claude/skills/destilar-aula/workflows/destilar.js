export const meta = {
  name: 'destilar-aula',
  description: 'Destila uma aula longa (transcrição em chunks) em capítulos didáticos ordenados logicamente, voltados a consumo em áudio',
  phases: [
    { title: 'Extrair', detail: 'um agente por chunk extrai conceitos/exemplos/passos (Sonnet)' },
    { title: 'Estruturar', detail: 'um agente funde as notas em capítulos numa sequência lógica' },
    { title: 'Escrever', detail: 'um agente por capítulo escreve o texto destilado lendo o trecho-fonte literal' },
  ],
}

// args (pode chegar como string JSON — ver memória workflow_args_string):
//   { curso, curso_dir, segments_file, slice_script, density, chunks: [{id,file,start,end,words}] }
const A = typeof args === 'string' ? JSON.parse(args) : (args || {})
const { curso, curso_dir, segments_file, slice_script, chunks } = A
const density = A.density || 'essência (~10-15%)'
if (!chunks || !chunks.length) throw new Error('args.chunks vazio — rode chunk-transcript.py antes')

// Budget de palavras por capítulo conforme densidade (curso é pra ÁUDIO: ~140 ppm)
const isEssencia = /ess[êe]ncia/i.test(density)
const isCompleto = /completo/i.test(density)
const wordHint = isEssencia
  ? 'Mire 600–1000 palavras NESTE capítulo (≈5–7 min de áudio). Corte agressivamente: só o essencial — conceitos, definições e o exemplo MAIS ilustrativo. Nada de tangente, repetição ou exemplo redundante.'
  : isCompleto
  ? 'Pode ir a 1500–2500 palavras se o conteúdo pedir; preserve quase tudo que é ensinado.'
  : 'Mire 900–1400 palavras (≈6–9 min de áudio). Mantenha conceitos, definições, exemplos-chave e passos; corte repetição e divagação.'
// Quantos capítulos a fase de estrutura deve mirar conforme densidade
const chapterTarget = isEssencia ? '6 a 10' : isCompleto ? '12 a 20' : '8 a 14'

const BEATS_SCHEMA = {
  type: 'object',
  required: ['beats'],
  properties: {
    beats: {
      type: 'array',
      description: 'Unidades atômicas de ensino encontradas neste trecho, na ordem em que aparecem',
      items: {
        type: 'object',
        required: ['topic', 'summary', 'start', 'end', 'new_chapter_signal'],
        properties: {
          topic: { type: 'string', description: 'Título curto do assunto desta unidade' },
          summary: { type: 'string', description: '2-4 frases do que é ensinado aqui, com fidelidade' },
          concepts: { type: 'array', items: { type: 'string' }, description: 'Conceitos-chave nomeados' },
          definitions: {
            type: 'array',
            items: {
              type: 'object',
              required: ['term', 'definition'],
              properties: { term: { type: 'string' }, definition: { type: 'string' } },
            },
          },
          examples: { type: 'array', items: { type: 'string' }, description: 'Exemplos, analogias ou casos citados' },
          practical_steps: { type: 'array', items: { type: 'string' }, description: 'Passos práticos / how-to ensinados' },
          key_quotes: { type: 'array', items: { type: 'string' }, description: 'Frases marcantes do instrutor (verbatim curto)' },
          start: { type: 'string', description: 'Timestamp HH:MM:SS aproximado de início' },
          end: { type: 'string', description: 'Timestamp HH:MM:SS aproximado de fim' },
          new_chapter_signal: { type: 'boolean', description: 'true se aqui claramente começa um novo grande tópico/módulo' },
        },
      },
    },
  },
}

const PLAN_SCHEMA = {
  type: 'object',
  required: ['chapters'],
  properties: {
    chapters: {
      type: 'array',
      items: {
        type: 'object',
        required: ['n', 'slug', 'titulo', 'objetivo', 'intervalos'],
        properties: {
          n: { type: 'integer', description: 'Ordem do capítulo (1-based) na SEQUÊNCIA LÓGICA de aprendizado' },
          slug: { type: 'string', description: 'kebab-case curto, sem acento' },
          titulo: { type: 'string', description: 'Título didático do capítulo' },
          objetivo: { type: 'string', description: '1 frase: o que o aluno sai sabendo/fazendo' },
          intervalos: {
            type: 'array',
            items: { type: 'string' },
            description: 'Intervalos de tempo da aula que alimentam este capítulo, ex "00:12:30 → 00:34:00". Pode juntar trechos não-contíguos.',
          },
          pontos: { type: 'array', items: { type: 'string' }, description: 'Bullets do que cobrir, em ordem' },
        },
      },
    },
  },
}

// ---------- Fase 1: Extrair (map) — um agente por chunk ----------
phase('Extrair')
const mapResults = await parallel(
  chunks.map((c) => () =>
    agent(
      `Você analisa UM trecho de uma transcrição de aula longa. Seja DETALHISTA e fiel — este trecho é pequeno de propósito pra você não perder nada.\n\n` +
      `Leia o arquivo do chunk: ${c.file}\n` +
      `Intervalo: ${c.start} → ${c.end}.\n\n` +
      `Extraia TODAS as unidades de ensino (beats) que aparecem: cada conceito explicado, definição, exemplo/analogia, passo prático e frase marcante do instrutor. ` +
      `Não resuma a aula inteira numa frase — granule. Preserve números, nomes, comandos e termos técnicos exatamente como ditos. ` +
      `Ignore conversa morta, repetição, piada solta, "deixa eu tomar água", problemas de áudio. ` +
      `Marque new_chapter_signal=true quando o instrutor claramente vira pra um novo grande tópico/módulo. ` +
      `Estime start/end de cada beat dentro do intervalo do chunk.`,
      { label: `extrair:chunk-${c.id}`, phase: 'Extrair', schema: BEATS_SCHEMA, model: 'sonnet' }
    ).then((r) => ({ chunk: c.id, start: c.start, end: c.end, beats: (r && r.beats) || [] }))
  )
)

const allBeats = mapResults.filter(Boolean)
const totalBeats = allBeats.reduce((s, r) => s + r.beats.length, 0)
log(`Extração: ${totalBeats} beats de ${allBeats.length} chunks`)

// Compacta as notas pro agente de estrutura (sem o texto-fonte bruto)
const notasCompactas = allBeats
  .map(
    (r) =>
      `### Chunk ${r.chunk} (${r.start}→${r.end})\n` +
      r.beats
        .map(
          (b, i) =>
            `- [${b.start || '?'}–${b.end || '?'}]${b.new_chapter_signal ? ' «NOVO TÓPICO»' : ''} ${b.topic}: ${b.summary}` +
            (b.concepts && b.concepts.length ? `\n    conceitos: ${b.concepts.join('; ')}` : '') +
            (b.practical_steps && b.practical_steps.length ? `\n    passos: ${b.practical_steps.join(' | ')}` : '')
        )
        .join('\n')
  )
  .join('\n\n')

// ---------- Fase 2: Estruturar (reduce) — um agente vê todas as notas ----------
phase('Estruturar')
const plan = await agent(
  `Você é o arquiteto pedagógico. Abaixo estão as notas extraídas de uma aula longa, chunk por chunk, em ordem cronológica.\n\n` +
  `Sua tarefa: agrupar essas unidades em CAPÍTULOS coerentes e ordená-los numa SEQUÊNCIA LÓGICA de aprendizado (não necessariamente a ordem em que foram ditos — se o instrutor adiantou um conceito ou voltou nele depois, junte; se um pré-requisito veio depois, mova pra frente).\n\n` +
  `Densidade do curso: ${density}.\n\n` +
  `Regras:\n` +
  `- Funda beats duplicados que aparecem em chunks vizinhos (há overlap proposital entre chunks).\n` +
  `- AGRUPE DE FORMA AGRESSIVA: cada capítulo é um MÓDULO temático inteiro, não um sub-tópico. Mire POUCOS capítulos no total — tipicamente ${chapterTarget}, MESMO numa aula de 4-8h. É melhor um capítulo denso que cobre um tema inteiro do que três rasos. Cada capítulo deve render 5–10 min de áudio destilado.\n` +
  `- Em "intervalos", liste os trechos de tempo da aula que alimentam o capítulo (pode juntar trechos não-contíguos, e cada capítulo costuma juntar VÁRIOS trechos). Isso será usado pra reler o texto-fonte literal.\n` +
  `- Nenhum CONCEITO importante pode ficar de fora, mas conteúdo comercial/institucional (ofertas, venda de curso, plugs) deve ser descartado ou condensado em no máximo um pequeno "extras" final. Não crie capítulos separados pra cada divagação.\n\n` +
  `NOTAS:\n\n${notasCompactas}`,
  { label: 'estruturar:plano', phase: 'Estruturar', schema: PLAN_SCHEMA }
)

const chapters = (plan && plan.chapters ? plan.chapters : []).slice().sort((a, b) => a.n - b.n)
log(`Estrutura: ${chapters.length} capítulos`)

// ---------- Fase 3: Escrever — um agente por capítulo ----------
phase('Escrever')
const written = await parallel(
  chapters.map((ch) => () => {
    const padded = String(ch.n).padStart(2, '0')
    const outPath = `${curso_dir}/capitulos/${padded}-${ch.slug}.md`
    const sliceCmds = (ch.intervalos || [])
      .map((iv) => {
        const m = iv.split('→').map((s) => s.trim())
        return m.length === 2
          ? `python3 ${slice_script} ${segments_file} "${m[0]}" "${m[1]}"`
          : null
      })
      .filter(Boolean)
    return agent(
      `Escreva o capítulo ${ch.n} — "${ch.titulo}" — de um curso destilado para consumo em ÁUDIO.\n\n` +
      `Objetivo do capítulo: ${ch.objetivo}\n` +
      `Pontos a cobrir (em ordem):\n${(ch.pontos || []).map((p) => `- ${p}`).join('\n') || '- (use o trecho-fonte)'}\n\n` +
      `ANTES de escrever, leia o trecho-fonte LITERAL da aula rodando estes comandos no Bash e baseie-se no que foi realmente dito (não invente):\n` +
      sliceCmds.map((c) => `    ${c}`).join('\n') +
      `\n\nDensidade alvo: ${density}. ${wordHint} Corte repetição, divagação e enrolação, mas NÃO omita nem invente conceito ensinado — fidelidade ao que foi dito > brevidade, dentro do orçamento de palavras.\n\n` +
      `Estilo (será narrado em áudio depois): didático, conversacional, frases curtas com ritmo de fala, como um instrutor explicando pra alguém ouvindo no carro. Português brasileiro. ` +
      `NÃO escreva blocos de código longos — descreva o que o código faz em prosa (será TTS). Sem "olá/bem-vindo", sem despedida.\n\n` +
      `Estrutura do arquivo Markdown (escreva via Write em ${outPath}):\n` +
      `---\n` +
      `# ${ch.titulo}\n\n` +
      `Comece com 1 frase de objetivo. Depois o conteúdo destilado em seções H2 curtas. ` +
      `Termine com "## Em resumo" listando 3–6 takeaways.\n` +
      `---\n\n` +
      `Crie a pasta se precisar (mkdir -p). Devolva apenas: path e contagem de palavras.`,
      { label: `escrever:${padded}-${ch.slug}`, phase: 'Escrever', model: 'sonnet' }
    ).then(() => ({ n: ch.n, slug: ch.slug, titulo: ch.titulo, objetivo: ch.objetivo, intervalo: (ch.intervalos || []).join(', '), path: outPath }))
  })
)

return {
  curso,
  curso_dir,
  total_chunks: chunks.length,
  total_beats: totalBeats,
  chapters: written.filter(Boolean),
}
