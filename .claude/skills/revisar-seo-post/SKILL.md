---
name: revisar-seo-post
description: Revisão de SEO on-page + trava de segurança do MCP que roda como GATE logo antes de publicar um post no blog Beer & Code — entre a montagem do draft e o CreatePost/PublishPost do MCP beer-and-code-blog. Acionar sempre que um post estiver pronto para subir ao MCP (no pipeline da skill criar-post-blog, e em cada post do scripts/criar-posts-batch.py), ou quando o usuário pedir para revisar/auditar o SEO de um post ou rascunho antes de publicar. Audita keyword-alvo, title/meta, headings, slug, links e legibilidade; corrige o que é seguro e bloqueia o que quebraria o publish.
---

# Revisão de SEO do post (gate antes de publicar)

Última checagem antes de um post subir ao MCP do blog. Roda sobre os campos já montados (`title`, `body`, `meta_title`, `meta_description`, `excerpt`, `slug`, `tags`, `category_slug`) e a **keyword-alvo** do post. Faz duas coisas:

1. **Trava de segurança do MCP** — pega o que faz o `CreatePost`/`UpdatePost` falhar com `-32603` *antes* de chamar o MCP. Bloqueante e não-negociável.
2. **Revisão de SEO on-page** — confere se o post está otimizado para a keyword-alvo, com a profundidade e a estrutura que rankeiam.

Esta skill **não escreve o post do zero** e **não publica**. Ela revisa, corrige o que é seguro, e devolve um veredito. Quem publica é o passo 6 da `criar-post-blog`.

## Inputs

- **Draft do post** (obrigatório) — os campos que irão ao `CreatePost`: `title`, `body` (Markdown), `meta_title`, `meta_description`, `excerpt`, `slug`, `tags`, `category_slug`.
- **Keyword-alvo** (`keyword_principal`) + **secundárias** (`keywords_secundarias`) — vêm da pauta / do prompt do batch. Se não vierem, **infira a keyword-alvo do título e do slug** e diga que inferiu.
- **`perguntas_paa`** (opcional) — as perguntas do "People Also Ask" que a `planejar-pauta` entrega junto com a pauta. Se **não** vier — ausente **ou** com o valor literal `—`, que a `planejar-pauta` emite quando a SERP não trouxe bloco PAA — marque o check de cobertura de PAA como `· (não verificado)` — nunca como aprovado e nunca como ❌.
- **Modo** — `batch` (sem humano, vindo do `criar-posts-batch.py`) ou `interativo` (single-post, humano presente). Muda o comportamento no veredito (ver abaixo).

## Camada 1 — Trava de segurança do MCP (bloqueante)

Estes cenários fazem o servidor devolver `MCP error -32603: Something went wrong` (genérico, sem detalhe). **Corrija ANTES de chamar o MCP — sempre, em qualquer modo:**

| # | Trava | Regra | Correção |
|---|---|---|---|
| 1 | Em-dash no `meta_description` | `—` (U+2014) proibido em `meta_description` | trocar por vírgula, ponto ou hífen simples `-` |
| 2 | `meta_description` longo | máximo **155 chars** (limite real ~160, margem de segurança) | reescrever mais curto mantendo a keyword |
| 3 | Símbolo Unicode no `title`/`slug` | proibidos `≠ ≈ ≤ ≥ ∈ → ← ⇒` e similares | reescrever em palavras: "não é", "aproximadamente", etc. Hífen `-` é OK |

Acentos comuns (ç, á, ã…) e em-dash em `title`/`body`/`excerpt` passam normal — não mexa.

Se qualquer item da camada 1 estiver presente, **corrija o campo no draft** e registre no relatório. Nunca chame o MCP com um desses pendentes.

## Camada 2 — Checklist de SEO on-page

Marque cada item ✅ / ⚠️ / ❌ (convenções em `references/checklist.md`). Corrija os ⚠️ quando a correção for segura — ver "Veredito".

**Keyword-alvo (o que mais importa):**
- [ ] keyword-alvo no `title` — de preferência perto do início.
- [ ] keyword-alvo no **primeiro parágrafo** do body (primeiras ~100 palavras).
- [ ] **abertura citável**: as 1-3 primeiras frases respondem a keyword-alvo em definição direta, antes de contexto ou storytelling. Teste: a frase de abertura faz sentido sozinha, fora do post. É o trecho que a AI Overview extrai pra citar.
- [ ] keyword-alvo em **pelo menos 1 H2**.
- [ ] keyword-alvo no `slug` (kebab-case, curto, sem stopwords supérfluas).
- [ ] keyword-alvo no `meta_description` e no `meta_title`.
- [ ] **sem keyword stuffing** — densidade natural (~0,5–2%). Repetição forçada é penalidade, não otimização.
- [ ] keywords secundárias / long-tail distribuídas pelos H2 (não empilhadas num lugar só).

**Title & meta:**
- [ ] `meta_title` ≤ 60 chars, com a keyword, atrativo (não precisa ser idêntico ao `title`).
- [ ] `meta_description` 120–155 chars, com a keyword + um benefício/promessa que dê vontade de clicar.
- [ ] `title` tem gancho (impacto ou prático), no tom da marca — não é só a keyword crua.
- [ ] `excerpt` ≤ 500 chars, vende o post.

**Estrutura & escaneabilidade:**
- [ ] body começa em `##` (H2) — o `title` é o H1, não repita H1 no corpo.
- [ ] hierarquia de headings sem pulo de nível (H2 → H3, nunca H2 → H4).
- [ ] parágrafos curtos, listas e **negrito** em termos-chave — escaneável.
- [ ] tem blocos de código/exemplo prático quando o tema é mão-na-massa (` ```lang `).
- [ ] profundidade compatível com a intenção: tema informacional competitivo pede corpo robusto (≈800+ palavras); não publique conteúdo raso contra SERP densa.
- [ ] **cobertura de PAA**: com `perguntas_paa` na entrada, pelo menos 2 dessas perguntas aparecem como H2, em texto literal ou quase — é o H2 que casa com a SERP e ganha featured snippet. Sem o campo, `· (não verificado)`.

**Links & mídia:**
- [ ] **pelo menos 1 link interno** para post relacionado do blog (use `ListPosts` para achar o slug do pilar/posts irmãos quando a keyword tiver cluster).
- [ ] fontes externas com link inline `[texto](url)` (regra da brand voice).
- [ ] imagens no body têm `alt` descritivo com a keyword quando fizer sentido.

**Intenção & canibalização:**
- [ ] o conteúdo casa com a **intenção** da keyword (informational para blog). Se a SERP da keyword for de outra intenção (ex.: termo dominado por outro nicho), sinalize — pode ser keyword errada.
- [ ] **não canibaliza** post existente: `ListPosts` e cheque se já há post mirando a mesma keyword-alvo. Se houver, avise que talvez seja reforço do existente, não post novo.

## Veredito

Monte um relatório compacto e decida:

**Modo `batch` (sem humano — vindo do `criar-posts-batch.py`):**
1. **Sempre** aplique as correções da **camada 1** (travas do MCP) — bloqueante.
2. Aplique as correções **seguras** da camada 2 que não mudam o sentido do conteúdo: ajustar `meta_title`/`meta_description`/`excerpt`/`slug`, inserir a keyword no primeiro parágrafo ou num H2 se faltar e couber naturalmente, adicionar `alt`, corrigir hierarquia de heading, adicionar link interno óbvio.
3. Itens que exigiriam **reescrever o post ou mexer na estrutura de H2** (profundidade insuficiente, intenção errada, canibalização, **cobertura de PAA** — criar/renomear H2 pra cobrir as `perguntas_paa` é reescrita, não correção segura) → **não bloqueie o batch**: registre como aviso (`❌` não-bloqueante) no relatório e siga para a publicação. Bloquear o batch inteiro num julgamento subjetivo é pior que publicar com aviso.

**Modo `interativo` (single-post, humano presente):**
1. Mostre o relatório com os ⚠️/❌ e as correções **propostas**. Aplique as seguras; para qualquer correção que **mude o sentido** do texto ou a estrutura de H2 (incluindo PAA), pergunte antes.
2. Só libere para o passo 6 (publicação) depois do `ok`.

## Saída

Nesta ordem: (1) **relatório de SEO** no formato de `references/checklist.md` — camada 1 + camada 2, com ✅/⚠️/❌ e o que foi corrigido; (2) **campos finais** prontos para o `CreatePost`, só os que mudaram, com o antes/depois de `title`/`slug`/`meta_*` se foram tocados; (3) **veredito de uma linha**: `PUBLICAR` (passou ou foi corrigido) ou `SEGURAR` (problema sério em modo interativo aguardando decisão do usuário).

## Passo opcional (pago) — auditoria do HTML publicado

**Fora do gate.** Roda só DEPOIS do `PublishPost`, só em modo `interativo`, e só quando o usuário pedir auditoria do post no ar. Nunca no meio do batch: é chamada paga e o draft ainda nem tem URL. Serve pra pegar o que o Markdown esconde — o tema do CMS pode injetar H1 duplicado, truncar a meta ou renderizar DOM gigante pra pouco texto.

Uma chamada resolve:

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/on_page/instant_pages",
  data: [{ url: "https://blog.beerandcode.com.br/<slug>", enable_javascript: false }]
})
```

Leia de `items[0]`:
- `onpage_score` + `checks` — booleanos com **polaridade invertida entre si, não trate todos igual**: `no_h1_tag`, `title_too_long`, `duplicate_meta_tags`, `low_content_rate` e `low_character_count` são defeitos (`true` = ⚠️); já `seo_friendly_url_keywords_check` é o oposto — significa "URL consistente com a meta tag `title`", então `true` = ✅ e **`false` = ⚠️** (proponha slug novo). Esses checks só vêm preenchidos para páginas com o check `canonical` = true; campo ausente → `· (não verificado)`, nunca ✅.
- `meta.htags` — a hierarquia H1-H6 **real** servida (confere o check de heading da camada 2 contra o HTML, não contra o Markdown).
- `meta.content.plain_text_word_count` — profundidade medida, no lugar da estimativa de "≈800+ palavras".
- `meta.content.title_to_content_consistency` e `.description_to_content_consistency` — float 0-1. **< 0,6 = ⚠️**: proponha reescrita do campo e aplique via `UpdatePost`.
- `meta.social_media_tags` — og:/twitter: presentes.

**Como chamar o `dfs-mcp`**: é um gateway genérico — tudo passa por `api_request` com `method` + `path` + `data`, e `data` é **sempre um array**, mesmo pra uma tarefa só. As tools são *deferred*: antes da primeira chamada rode `ToolSearch({query: "select:mcp__dfs-mcp__api_request,mcp__dfs-mcp__docs_search", max_results: 5})`, senão dá `InputValidationError`. No modo `.ai` (default) a resposta vem achatada: leia `items` direto na raiz — **não** existe `tasks[].result[]`. Sucesso é `status_code: 20000`. Precisou de um campo ou endpoint que esta skill não cobre, confirme com `docs_search` (grátis) em vez de inventar.

## Pré-requisitos

- MCP `beer-and-code-blog` carregado (para `ListPosts`/`ListTags` nos checks de canibalização e link interno). Se não estiver, faça a revisão de conteúdo mesmo assim e marque os checks que dependem dele como "não verificado".
- **O gate não precisa do `dfs-mcp` (DataForSEO).** Esta skill revisa o post contra a keyword **já decidida** na pauta — não refaz pesquisa de keyword. Se a keyword estiver claramente errada, aponte e sugira, mas não gaste chamada paga no meio do batch. O único uso de API é o passo opcional pago acima, sempre a pedido.
