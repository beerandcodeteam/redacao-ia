---
name: criar-post-blog
description: Cria, agenda e publica posts completos no blog Beer & Code (blog.beerandcode.com.br). Acionar sempre que o usuário pedir para criar, escrever, agendar, montar ou rascunhar um post, artigo, matéria ou conteúdo para o blog Beer & Code, ou der um tema técnico (IA aplicada, LLMs, Claude, OpenAI, Gemini, Laravel, PHP, RAG, agentes, embeddings, engenharia de prompt, ferramentas de dev) que deva virar artigo. Cobre o fluxo completo: pesquisa em fontes oficiais, montagem da estrutura, redação no tom da marca, geração da capa com Gemini nano-banana e publicação via MCP do blog.
---

# Criar post para o blog Beer & Code

Pipeline ponta a ponta para transformar um tema em post agendado no blog Beer & Code. Use sempre que o usuário pedir um post novo.

## Inputs obrigatórios

Antes de começar, garanta que tem:

- **Tema** — o assunto do post. Se vier vago ("um post sobre IA"), peça para refinar.
- **Data e hora de publicação** — vai para `published_at` em ISO8601 (ex: `2026-05-02T09:00:00-03:00`). Se faltar, pergunte. Não invente.

Não comece a pesquisa sem os dois. Se o usuário disser "amanhã", confirme a hora antes de ir.

## Inputs opcionais

- **Destino do CTA** — URL + nome + 1 linha de contexto do evento/recurso para onde o post vai apontar (ex: evento, Clã, repositório, newsletter). **Quando o destino for o Clã Beer and Code, a URL é `https://beerandcode.com.br` — constante do projeto, não pergunte.** Para qualquer outro destino (evento, repositório, newsletter) em fluxo single-post, pergunte ao usuário antes da escrita. Se for batch, vem dos flags `--cta-url`, `--cta-label`, `--cta-pitch` do `scripts/criar-posts-batch.py`. **Sem destino, o post sai sem CTA — não invente um.**

## Pipeline

Cinco passos em ordem. Não pule nenhum sem `ok` explícito do usuário.

### 1. Pesquisa

Use `WebSearch` e `WebFetch`. Priorize as fontes oficiais em `references/sources.md` (labs, libs, vendors). Buscar fora da lista é permitido quando faz sentido — a lista é o ponto de partida, não uma cerca.

Saída desta etapa: 5–10 anotações no formato `fato | fonte | url`. Inclua benchmarks, datas, citações diretas, números, detalhes de API, mudanças de versão. Sem fonte verificável, o fato não entra no post.

Se o tema for um lançamento ou notícia recente, comece pelo anúncio oficial (changelog, post do lab, paper) antes de qualquer secundária.

### 2. Estrutura

Monte um outline seguindo `references/post-template.md`. Mostre o outline ao usuário (títulos H2 + bullets do que vai em cada seção + onde vão os blocos de código/imagens). Espere `ok` antes de escrever o corpo.

Esse passo existe porque é mais barato corrigir ângulo e foco no outline do que no texto pronto.

### 3. Escrita

Escreva o body completo em Markdown. Esse texto vai direto para o campo `body` do `CreatePost`.

Antes de escrever, **leia `references/brand-voice.md`**. O tom é o diferencial do blog — não é negociável. Resumo do que importa:

- Frases curtas, ritmo de fala. Pausas. Como se estivesse explicando para outro dev.
- Direto, provocador, didático, técnico, levemente irreverente. Sem ser arrogante.
- Antihype: nada de "fórmula mágica", "desbloqueie", "domine sem esforço", "profissão do futuro".
- Conceito técnico → aplicação prática → impacto em produto. Sempre os três.
- Cite fontes inline: `[texto](url)`.
- ` ```lang ... ``` ` para snippets de código e prompts.
- CTA é embutido, não seção. Quando houver destino nos inputs, integra em 1–2 frases dentro do corpo, **no primeiro terço do post (~30% da leitura)** — tipicamente fechando o bloco de contexto, no trecho que mais conversa com o destino; conclusão só como fallback quando não houver encaixe natural antes. Link inline `[nome](url)`. Sem heading dedicado (`## CTA`, `## Entra no Clã`, `## Inscreva-se`), sem caixa, sem `---` ao redor. Sem destino, o post sai sem CTA — não invente um genérico. Detalhes em `references/brand-voice.md` → "Tom comercial (CTA)". **Se o destino for o Clã Beer and Code ou um evento da marca, use a skill `montar-cta-pitch`** para escolher o ângulo e o nível do pitch (o arsenal de argumentos validado ao vivo vive lá).

Schema dos campos que serão usados em `CreatePost`:

| campo | obrigatório | nota |
|---|---|---|
| `title` | sim | título do post (impacto ou prático) |
| `body` | sim | Markdown completo |
| `category_slug` | sim | escolhido via `ListCategories` + pergunta ao usuário |
| `author_slug` | sim | escolhido via `ListAuthors` + pergunta ao usuário |
| `published_at` | sim | ISO8601 do input |
| `tags` | recomendado | slugs; reuse via `ListTags`, crie só o que faltar |
| `slug` | opcional | auto-gerado do título |
| `excerpt` | recomendado | até 500 chars |
| `cover_image_path` | sim | retorno do `UploadImage` (passo 4) |
| `audio_url` | recomendado | URL pública do mp3 no OCI (passo 5) |
| `meta_title`, `meta_description` | opcional | ou deixe `EnrichPost` gerar |

### 4. Capa

Gere uma imagem minimalista que se encaixe no feed do https://blog.beerandcode.com.br. Estilo de referência: minimalista técnico, paleta sóbria (preto/branco/grafite com 1 cor de destaque ligada ao tema), tipografia ou ícones simples, sem stock-photo de gente sorrindo.

Use o script:

```bash
.claude/skills/criar-post-blog/scripts/generate-cover.sh "<prompt detalhado da imagem>" /tmp/cover-<slug>.png
```

O script gera a imagem com `gemini-3.1-flash-image-preview`, sobe para o OCI Object Storage (bucket `site-assets`, prefixo `posts/`) e imprime a URL pública na **última linha do stdout**. Capture com `url=$(... )` ou pegue a linha `Capa publicada em: <url>` no stderr.

Lê do `.env` (cwd): `GEMINI_API_KEY` e as credenciais OCI (`OCI_ACCESS_KEY_ID`, `OCI_SECRET_ACCESS_KEY`, `OCI_BUCKET`, `OCI_ENDPOINT`, `OCI_URL`).

Mostre a imagem ao usuário e confirme antes de prosseguir. Se ele pedir variação, rode de novo com prompt ajustado (vai subir uma nova) — não use imagem que o usuário não aprovou.

Dica de prompt: descreva composição, paleta, estilo (minimalista, flat, geométrico), elemento central ligado ao tema (ex: "node graph", "terminal cursor", "glyph de chave de API") e proporção (16:9 para capa de blog).

### 5. Áudio narrado

Reescreva o `body` em texto narrável e gere o mp3 com voz clonada (OmniVoice).

1. **Reescrita do roteiro — SEMPRE via subagent `roteiro-narracao` (Haiku).** Esta etapa é puramente transformação de texto, não envolve pesquisa nem decisão de produto, e por isso roda num modelo barato. **Não execute a reescrita você mesmo (Opus/Sonnet)** — delegue para o subagent via Agent tool com `subagent_type: "roteiro-narracao"`. Isso vale tanto no fluxo single-post quanto no batch (`scripts/criar-posts-batch.py`).

   Como invocar:

   ```
   Agent({
     subagent_type: "roteiro-narracao",
     description: "Roteiro de áudio do post <slug>",
     prompt: "Reescreva o body abaixo em texto narrável e salve em /tmp/audio-script-<slug>.txt.\n\nslug: <slug>\ntitle: <title>\nexcerpt: <excerpt>\n\nbody:\n<markdown completo do post>"
   })
   ```

   O subagent devolve apenas o caminho do `.txt` gerado e a contagem de palavras. As regras detalhadas de transformação vivem em `references/audio-script.md` e na definição do subagent em `.claude/agents/roteiro-narracao.md` — não precisa repetir no prompt, só passe o conteúdo do post.

   Se o subagent `roteiro-narracao` não estiver disponível na sessão, avise o usuário e pare. Não caia no fallback de reescrever no modelo principal sem aprovação explícita — desperdiça tokens caros pra uma tarefa que é de Haiku.

2. **TTS + upload.** Rode:

   ```bash
   .claude/skills/criar-post-blog/scripts/generate-audio.sh \
     /tmp/audio-script-<slug>.txt <slug>
   ```

   O script chama `omnivoice-infer` do `.venv` da raiz do projeto, com `--ref_audio voice/lucas.wav` + `--ref_text voice/lucas.txt` (clone da voz do Lucas), converte WAV → MP3 com ffmpeg e sobe pra `s3://<OCI_BUCKET>/posts/audio/<slug>.mp3`. Imprime a URL pública na **última linha do stdout**. Capture com `audio_url=$(...)`.

   Pré-requisitos: `.venv` com `omnivoice-infer` instalado (já está em `.venv/bin/`), `ffmpeg` no PATH, e as mesmas vars OCI do passo 4. Primeira execução baixa o checkpoint do HuggingFace (`k2-fsa/OmniVoice`) — pode demorar.

   ⚠️ **Rode o `generate-audio.sh` como comando BLOQUEANTE em primeiro plano e espere o stdout no mesmo turno.** NÃO rode em background (`&`, `run_in_background`, `nohup`) e NÃO use `ScheduleWakeup`/timer para "voltar depois que o mp3 ficar pronto". Em modo batch o post é gerado por uma sessão headless (`claude -p`), que **não tem loop interativo para acordar**: se você agendar um wakeup e encerrar o turno, a sessão termina com exit 0 e o post nunca é criado — exatamente a falha silenciosa que faz o batch reportar "concluído" sem publicar. O script é síncrono de propósito (leva ~1–3 min): chame, espere, capture `audio_url` da última linha e só então siga para o passo 5.5/6.

3. **Sem áudio é OK em rascunho.** Se o usuário pediu pra apenas rascunhar e revisar, pule este passo e rode depois via `update-post` passando `audio_url`. Em modo batch, rode sempre.

### 5.5. Revisão de SEO (gate antes de publicar)

Antes de tocar no MCP, rode a skill **`revisar-seo-post`** sobre os campos já montados (`title`, `body`, `meta_title`, `meta_description`, `excerpt`, `slug`, `tags`, `category_slug`) + a keyword-alvo do post (vem da pauta / do prompt do batch; se não vier, a skill infere do título e avisa) + `perguntas_paa`, quando a pauta trouxer o campo — é o que alimenta o check de cobertura de PAA nos H2; sem ele o check fica `(não verificado)`.

Ela faz duas coisas e **é obrigatória**:

1. **Trava de segurança do MCP** — corrige o que faz o `CreatePost` falhar com `-32603` (em-dash no `meta_description`, `meta_description` > ~155 chars, símbolos Unicode tipo `≠` no `title`/`slug`) *antes* de você chamar o MCP. Pula essa e o publish quebra com erro genérico.
2. **Revisão de SEO on-page** — keyword no title/1º parágrafo/H2/slug/meta, tamanho de `meta_title`/`meta_description`, hierarquia de headings, link interno, profundidade e intenção.

Comportamento por modo:
- **Single-post (humano):** a skill mostra o relatório, aplica correções seguras e segura para `ok` antes do passo 6.
- **Batch (`criar-posts-batch.py` / skill `criar-posts-batch`):** a skill aplica as travas do MCP + correções seguras e segue direto; problemas que exigiriam reescrever o post viram aviso no relatório, não travam o batch.

Use os **campos corrigidos que a `revisar-seo-post` devolveu** no `CreatePost` do passo 6 — não os campos pré-revisão.

### 6. Publicação via MCP

Use o MCP server **Beer & Code Blog** (laravel-boost). Ordem rígida:

1. `ListCategories` e `ListAuthors` → mostre as opções e **pergunte ao usuário** qual usar. Não escolha sozinho.
2. `ListTags` → reaproveite tags existentes. Só use `CreateTag` para o que realmente faltar.
3. `UploadImage` passando o campo `url` com a URL pública devolvida pelo `generate-cover.sh` (bucket OCI). Não envie base64 — a imagem já está no nosso storage. Guarde o `path` retornado.
4. `CreatePost` com todos os campos da tabela acima, **incluindo `audio_url`** (URL completa do mp3 do passo 5). O servidor extrai o path interno via `OciPath::fromUrl()` e popula `audio_path` + `audio_generated_at` automaticamente — você nunca passa `audio_path` direto.

   ⚠️ **Formato da `audio_url`:** passe **`https://blog.beerandcode.com.br/media/posts/audio/<slug>.mp3`**, NÃO a URL nativa do OCI que o `generate-audio.sh` imprime (`...oci.customer-oci.com/n/<ns>/b/site-assets/o/posts/audio/<slug>.mp3`). Com a URL nativa o `OciPath::fromUrl()` não remove o prefixo `n/<ns>/b/<bucket>/o/` e o player renderiza `/media/n/.../<slug>.mp3`, que dá 404 (verificado em 03/09/2026 nos posts de 22/07 a 01/09). O mp3 continua sendo o mesmo objeto no bucket; só a URL passada ao MCP muda. Depois do publish, confira: `curl -sI https://blog.beerandcode.com.br/media/posts/audio/<slug>.mp3` deve dar 200. Status default = `scheduled`; o scheduler do Laravel publica quando `published_at` chegar.
5. `EnrichPost` → gera `meta_title`/`meta_description` se você não enviou. Pule se já mandou ambos no `CreatePost`.

**Nunca** chame `PublishPost` sem `ok` explícito do usuário. Para post agendado, `CreatePost` com `published_at` futura já resolve — `PublishPost` só é necessário se quiser publicar antes da data.

Ao final, mostre o slug e o `published_at` confirmado.

## Pré-requisitos do ambiente

Antes dos passos 4, 5 ou 6, verifique:

- `.env` na raiz do cwd com `GEMINI_API_KEY=...` e credenciais OCI (`OCI_ACCESS_KEY_ID`, `OCI_SECRET_ACCESS_KEY`, `OCI_BUCKET`, `OCI_ENDPOINT`, `OCI_URL`) — passos 4 e 5.
- `aws` CLI v2 e `ffmpeg` instalados no PATH.
- `.venv` da raiz do projeto com OmniVoice (`.venv/bin/omnivoice-infer`) — passo 5.
- `voice/lucas.wav` + `voice/lucas.txt` (transcrição literal) na pasta da skill — referência pro clone de voz do passo 5.
- MCP server `Beer & Code Blog` carregado na sessão. Se não estiver, peça ao usuário para configurar o `.mcp.json` (modelo em `.mcp.json.example`, passo a passo em `docs/setup.md`) e reabrir a sessão. Não tente contornar.

## Quando o usuário corrigir algo

Aplique a correção sem rediscutir. Se ele disser "muda o ângulo para X" no outline, refaça o outline. Se disser "essa frase soa marketeira" no texto, reescreva. Cada ida e volta é caro — confirme uma vez por etapa, não três.
