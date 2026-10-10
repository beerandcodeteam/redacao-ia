---
name: cacar-news-jacking
description: Caça temas de news-jacking para o blog Beer & Code (blog.beerandcode.com.br) — detecta notícias/lançamentos/dramas de IA em ascensão ANTES da SERP saturar e devolve candidatos de pauta ranqueados, já com títulos otimizados pra CTR. Cruza detecção em tempo real (Hacker News, OpenRouter, Polymarket, GitHub, Reddit, NewsAPI/GDELT, RSS dos labs + X/Twitter via Grok) com qualificação de SEO (DataForSEO + GSC). Acionar quando o usuário pedir "caçar tema", "o que tá quente", "tem notícia pra surfar", "achar tema de news-jacking", "tema quente de IA", "o que postar hoje" ou equivalente. Entrega candidatos ranqueados (não escreve nem publica — para isso use planejar-pauta e depois criar-post-blog).
---

# Caçar news-jacking — Beer & Code

Acha o tema quente **antes de virar busca saturada** e devolve candidatos de pauta ranqueados, no formato que alimenta a `planejar-pauta`. O diferencial do blog é chegar primeiro em termo de cauda-longa de baixa concorrência (ver memória `project_padrao_vencedor_newsjacking`): posts como `claude-fable-5-vs-opus-4-8` (50 cliques/1005 imp) e `fable-5-bloqueado-openrouter-fusion` (CTR 6,23%) venceram por **velocidade + título com gancho**.

Esta skill **detecta, qualifica e ranqueia**. Ela não escreve nem publica. Fluxo: `cacar-news-jacking` → usuário aprova candidatos → `planejar-pauta` (vira pauta em campos) → `criar-post-blog`.

## Constantes do projeto (não perguntar)

| recurso | valor |
|---|---|
| GSC site_url | `https://blog.beerandcode.com.br/` |
| GA4 property | `properties/<GA4_PROPERTY_ID>` — o ID está em `.env` (`grep GA4_PROPERTY_ID .env`); se faltar, descubra com `mcp__analytics-mcp__get_account_summaries` (property "Blog Beer and Code") |
| DataForSEO (server `dfs-mcp`) location / language | `location_name: "Brazil"` / `language_code: "pt"` — vão **dentro** do `data[]` do `api_request` |
| Domínio para ranked keywords | `blog.beerandcode.com.br` |
| Arquivo de segredos | `./.env` (raiz) ou `~/.claude/newsjack.env` — script carrega ambos |
| Script de detecção | `scripts/detect.sh` (relativo a esta skill) |
| Estado/snapshots | `state/` (relativo a esta skill) |

Os outros domínios do GSC (`beerandcode.com.br`, `loja...`) **não** são deste blog — não misture.

## Inputs

- **Foco** (opcional) — recorte temático. Default: IA aplicada / LLMs / Claude/OpenAI/Gemini / coding agents / Laravel-PHP. Se o usuário der um foco ("só Claude", "modelos open source"), passe como `-q` pro script.
- **Janela** (opcional) — quão recente. Default: 48h. Mais que isso já não é news-jacking, é evergreen (manda pra `planejar-pauta` direto).

## Pipeline

### 0. Checagem de ambiente (rápida)

- O script exige `jq` e `curl` no PATH — se faltar, avise.
- Confirme que `~/.claude/newsjack.env` existe. Se não existir, avise o usuário e siga **só com as fontes sem credencial** (HN, OpenRouter, Polymarket, GitHub sem token, GDELT) — diga quais sinais ficaram de fora. Variável ausente = o detector pula aquela fonte com aviso e segue.

### 1. DETECTAR (rodar o script)

Rode o detector — ele bate em todas as fontes em uma só passada e já marca o que é **novo** desde o último run:

```bash
bash .claude/skills/cacar-news-jacking/scripts/detect.sh            # foco default
bash .claude/skills/cacar-news-jacking/scripts/detect.sh -q "claude OR anthropic OR fable"   # foco custom
```

O script cobre: **Hacker News** (stories recentes com tração), **OpenRouter** (diff do catálogo → detecta modelo *novo* ou *removido/bloqueado* — é o sinal de ouro pro tema campeão do blog), **GitHub** (releases de repos-chave), **Reddit** (top do dia nos subs de IA — OAuth se houver app, senão RSS best-effort), **notícias** (NewsAPI ou GDELT). Leia a saída em markdown.

Complemente via `WebFetch` (URLs em `references/sources.md`): **RSS dos labs** (blogs OpenAI/Anthropic/Google/Mistral — anúncio oficial é o gatilho mais forte de todos) e, quando houver rumor de lançamento, a **página do Polymarket** do evento pra pegar as odds/data (a API do Polymarket não expõe os mercados de IA de forma confiável, então não está no script).

### 2. X/Twitter via Grok (handoff manual)

O X é onde a notícia de IA quebra primeiro. Gere o prompt a partir de `references/grok-prompt.md` (preencha {HORAS}/{FOCO}/{DATA_ISO}) e **mostre pro usuário copiar e colar no chat do Grok** — o app do Grok tem X Search nativo. Espere ele devolver as tendências, deduplique contra o `detect.sh` (o que for exclusivo do X ganha bônus de velocidade) e some como candidatos. Se o usuário pular, siga sem — HN/Reddit/News já cobrem muito.

### 3. QUALIFICAR cada candidato

Junte os sinais de todas as fontes, **deduplique** (a mesma notícia aparece em HN + Reddit + News) e qualifique em lote.

> **Como falar com o DataForSEO (server `dfs-mcp`).** Acabou a tool-por-endpoint: tudo passa por `mcp__dfs-mcp__api_request` com `method` + `path` REST + `data`, e `data` é **sempre um array** de tasks, mesmo com uma só. As tools são *deferred* — antes da primeira chamada:
> `ToolSearch({query: "select:mcp__dfs-mcp__api_request,mcp__dfs-mcp__docs_search,mcp__dfs-mcp__docs_index,mcp__dfs-mcp__docs_list_sections", max_results: 5})`
> A resposta vem no **modo .ai** (default): já enxuta, com `items` na raiz — leia `items[]` direto, **não** navegue `tasks[].result[]`. Sucesso = `status_code: 20000`. `noAiMode: true` só em último caso (schema completo, estoura contexto). Endpoint que esta skill não cobre? Ache o path com `docs_index`/`docs_search` — não invente path. Na dúvida sobre filtro ou grafia de location/language, confira nos dois endpoints **gratuitos**: `GET /v3/dataforseo_labs/available_filters` e `GET /v3/dataforseo_labs/locations_and_languages`.

**3a. Volume, KD, intenção e — principalmente — aceleração**

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/dataforseo_labs/google/keyword_overview/live",
  data: [{ keywords: ["<termo quente>", "<variação 1>", "<variação 2>"],
           location_name: "Brazil", language_code: "pt",
           include_serp_info: true }]
})
```

Aceita até 700 keywords — mande **todos** os candidatos numa chamada só. Case cada resultado pelo campo `keyword` (o `items` não preserva ordem nem tamanho da entrada). Leia:

- `keyword_info.search_volume`, `keyword_properties.keyword_difficulty`, `search_intent_info.main_intent`;
- **`keyword_info.search_volume_trend.{monthly,quarterly}` + os últimos meses de `keyword_info.monthly_searches`** — a derivada, não o valor absoluto. É esse o número que vale em tema recém-nascido;
- **`serp_info.se_results_count` e `serp_info.serp_item_types`** — só existem porque o payload manda `include_serp_info: true` (flag que **não** encarece a chamada; só `include_clickstream_data` dobra o preço). Sem ela o `serp_info` volta `null` **sempre** e o `se_results_count` fica sem fonte alguma — no modo `.ai` a SERP do 3c corta os metadados de topo —, e o critério "Janela fechando" do passo 4 fica sem número. Com a flag ligada, `serp_info: null` = a base ainda não tem SERP pro termo (normal em recém-nascido): janela provavelmente aberta, confirme no 3c.

**Triagem de graça:** `serp_item_types` já lista `featured_snippet` / `people_also_ask` / `ai_overview` / `organic`. Descarte aqui quem já tem a SERP montada e **rode o 3c (pago) só nos sobreviventes** — é o que derruba o custo da skill.

⚠️ **Volume BR ~0 é o estado normal de um termo com 48h de vida — nunca descarte por isso.** Termo ainda sem registro no banco nem aparece em `items`, e isso também não reprova. O que reprova é curva *caindo*. Para KD de lista grande e barata: `path: "/v3/dataforseo_labs/google/bulk_keyword_difficulty/live"`, mesmo `data` (até 1000 kws, 1 request).

Para variações long-tail (`keywords_secundarias`): `path: "/v3/dataforseo_labs/google/keyword_suggestions/live"` com `data: [{ keyword: "<seed>", location_name: "Brazil", language_code: "pt", limit: 30 }]` — campo `keyword` **singular**. Em termo recém-nascido volta pouco ou nada; aí as perguntas do PAA (3c) são a fonte confiável.

**3b. Demanda dentro das IAs — o sinal que chega antes do Google**

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/ai_optimization/ai_keyword_data/keywords_search_volume/live",
  data: [{ keywords: ["<termo quente>"], location_name: "Brazil", language_code: "pt" }]
})
```

Devolve `ai_search_volume` + `ai_monthly_searches` (12 meses). Caso real: "claude code" saiu de 5 (ago/25) para 140 (jul/26) com volume Google modesto — é demanda real acelerando. **Google chapado + IA subindo = surfar agora.** Os dois chapados = a velocidade das fontes decide sozinha.

**3c. Confirmar a SERP dos sobreviventes**

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/serp/google/organic/live/advanced",
  data: [{ keyword: "<keyword-alvo>", location_name: "Brazil", language_code: "pt",
           depth: 10, load_async_ai_overview: true }]
})
```

`depth: 10` = página 1 (e é o próprio default; não suba — cada bloco de 10 resultados é cobrado). Uma chamada por candidato **que passou na triagem do 3a**, jamais por variação. `items[]` vem achatado, cada item com seu `type`:

- **`featured_snippet` / `people_also_ask` / `ai_overview` presentes = SERP madura, janela FECHANDO** — o Google já organizou a resposta. Só `organic` + `related_searches` = dez links azuis = **janela aberta**, news-jacking clássico funciona.
- `people_also_ask` → `items[].title` são as perguntas exatas em pt-BR: viram os H2 do post, direto no campo `bullets` da camada 2. Só as perguntas interessam e elas vêm sem clique nenhum — **não** mande `people_also_ask_click_depth`, que cobra a mais só pelas respostas, descartadas aqui.
- `ai_overview` → `references[].domain/url/title` = quem o Google cita (lista diferente de quem rankeia). Referências todas gringas = brecha em pt-BR, e o post precisa abrir com definição direta e citável.
- Top 10 raso, desatualizado ou só em inglês = entra fácil.

**3d. GSC** — o domínio já recebe impressão pra esse termo/variações? Em que posição? (cruze com `get_search_analytics`). Posição 5–20 sem post dedicado = quick win.

**3e. Dedup contra o blog** — `mcp__beer-and-code-blog__list-posts`. Se já existe post no tema, **NÃO é pauta nova — é atualizar o existente** (regra anti-canibalização, ver memória `project_virada_intencionalidade_ctr`). Sinalize "atualizar post X".

### 4. PONTUAR

Pontue 0–100 por candidato combinando os sinais (rubric, sem fórmula fechada):

| sinal | peso | leitura |
|---|---|---|
| **Velocidade / frescor** | alto | Subindo agora em várias fontes, anúncio oficial recente, mercado precificando lançamento iminente. É o coração do news-jacking. Ancore com número: `search_volume_trend.monthly` e a curva de `ai_monthly_searches` — "volume 0" e "volume acelerando de 8 pra 140" não são a mesma coisa. |
| **Janela fechando** | alto | Medir, não achar: `se_results_count` (só existe com `include_serp_info: true` no 3a) na casa das centenas, não dos milhões, + SERP **sem** `featured_snippet`/`people_also_ask`/`ai_overview` = janela escancarada. Com PAA/AI Overview montados, ou concorrente forte já publicado → fechando. Ver 3 posts no HN não significa que a SERP BR saturou. |
| **Viabilidade (KD × brecha SERP)** | alto | KD baixo/médio + top 10 raso = entra fácil. Dominado por gigante/doc oficial = difícil. |
| **Potencial de CTR** | médio | O ângulo rende título com número/comparação/drama? (ver fórmula abaixo) |
| **Quick win (GSC)** | médio | Já pinga impressão sem post dedicado → bônus. |
| **Fit com o pilar** | médio | Dentro do escopo técnico do blog soma; fora subtrai. |
| **Canibalização** | trava | Já existe post → rebaixa para "atualizar existente". |

### 5. ENTREGAR

Siga `references/output-template.md`. Duas camadas:

1. **Radar (chat)** — tabela dos candidatos com fonte, sinal de velocidade, volume/KD, janela (aberta/fechando), veredito (`surfar agora` / `surfar se acelerar` / `atualizar post existente` / `evergreen → planejar-pauta` / `descartar`). Top 3 "surfar agora" no fim.
2. **Pauta dos aprovados (formato de campos)** — só os "surfar agora", no formato fixo da `planejar-pauta` (`## Título` + `publicar_em`/`autor`/`categoria`/`resumo`/`hook`/`bullets`/`keyword_principal`/`keywords_secundarias`/`tags`/`dificuldade`/`volume`). Pronto pra `pautas/<mês>/semana-N.md`.

**Toda recomendação passa pelo filtro de intencionalidade** (memória `project_virada_intencionalidade_ctr`): demanda provada, SERP ganhável, título com gancho de CTR, sem canibalização, link interno planejado.

### 6. CONFERIR (48–72h depois de o post ir ao ar)

Fecha o loop de aprendizado — rode numa sessão seguinte, quando o usuário quiser saber se o news-jack pegou:

- SERP da keyword-alvo (mesma chamada do 3c): o blog entrou no top 10 ou virou `ai_overview.references[]`?
- Visibilidade do domínio em respostas de IA:

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/ai_optimization/llm_mentions/target_metrics_lite/live",
  data: [{ platform: "google", location_name: "Brazil", language_code: "pt",
           target: [{ domain: "blog.beerandcode.com.br" }] }]
})
```

`platform: "google"` (AI Overview) é **obrigatório** — `chat_gpt` só tem cobertura US/inglês e volta vazio no BR. Baseline atual: `mentions: 1`, `ai_search_volume: 210`, ou seja quase zero: qualquer subida é mensurável. Anote em `state/` o acerto por tipo de gancho (modelo bloqueado / release / drama) pra calibrar o rubric do passo 4 com histórico do blog, não com heurística.

### Fórmula de título pra CTR

Os títulos campeões do blog ganham o clique por **número, comparação ou drama** — não por descrição neutra. Para cada candidato, proponha o título nesse padrão:

- **Comparação:** "X vs Y: o que muda (e vale trocar?)"
- **Drama/conflito:** "X foi bloqueado/banido/processado — o que aconteceu"
- **Número/lista:** "7 coisas que os americanos fizeram com X em 72h"
- **Pergunta com tensão:** "X vale a pena em 2026? Testei e o resultado surpreende"

Evite o título "explicativo neutro" (ex.: "O que é X") para tema quente — ele rankeia mas não converte (ver `quanto-ganha-engenheiro-de-ia`: 1266 imp, CTR 0,32%).

## Custo

- Rode `detect.sh` **uma vez** por sessão; ele já agrega tudo. Não refaça por tema.
- Keywords do DataForSEO vão todas numa chamada só (3a); baseline do GSC uma vez.
- `load_async_ai_overview: true` é cobrado à parte (+US$ 0,002 por request) e escala com o tamanho da lista — mais um motivo pro 3c rodar só nos sobreviventes da triagem do 3a.
- Se vierem >8 candidatos, avise do custo e qualifique os 5 de maior velocidade primeiro.

## Pré-requisitos do ambiente

- MCP `dfs-mcp` (tools *deferred* — sem o `ToolSearch` do passo 3 a primeira chamada morre com `InputValidationError`), `gscServer` e `beer-and-code-blog` carregados. Se faltar algum, siga com os demais e sinalize o sinal ausente.
- `WebFetch` habilitado (para RSS dos labs e APIs públicas sem credencial).

## Setup do env

O script carrega `$NEWSJACK_ENV`, `~/.claude/newsjack.env` e `./.env` (o que existir; tolera CRLF do Windows).

```
NEWSAPI_KEY=...           # newsapi.org free tier; se vazio, cai pro GDELT (sem chave, cobertura grosseira)
GITHUB_TOKEN=...          # PAT read-only; sobe rate limit do GitHub de 60 p/ 5000 req/h
REDDIT_CLIENT_ID=...      # app web OU script em reddit.com/prefs/apps
REDDIT_CLIENT_SECRET=...
REDDIT_USER_AGENT=beerandcode-newsjack/1.0 by /u/seu_user
# REDDIT_USERNAME / REDDIT_PASSWORD — opcionais (só p/ password grant; client_credentials já basta p/ ler)
```

**Reddit:** o Reddit gateou a criação de app **novo** em 2026 (Responsible Builder Policy), mas um app **existente** (web ou script, com secret) funciona via **OAuth client_credentials** — é o caminho primário: traz ups/comentários e **não toma 429**. Sem credencial, o script cai pro **RSS público** best-effort (sem ups, 429-prone). HN cobre boa parte do mesmo sinal de qualquer forma.
