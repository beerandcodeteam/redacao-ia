---
name: planejar-pauta
description: Valida, prioriza e enriquece uma lista de temas/pautas para o blog Beer & Code (blog.beerandcode.com.br) ANTES de escrever, cruzando Search Console (tração real do domínio), DataForSEO (volume, dificuldade, intenção, concorrência na SERP) e Google Analytics (engajamento do conteúdo atual). Acionar quando o usuário trouxer uma lista de temas, pautas ou ideias de post e pedir para analisar, validar, priorizar, otimizar a pauta, escolher o que escrever primeiro, achar a melhor keyword/ângulo, ou decidir se um tema vale a pena. Entrega um relatório acionável (não escreve nem publica o post — para isso, use a skill criar-post-blog).
---

# Planejar pauta do blog Beer & Code

Pega uma lista de temas candidatos e devolve um **relatório de pauta priorizado**: para cada tema, qual keyword-alvo, qual ângulo, que estrutura, e o quão urgente é escrever — decidido por dados, não por achismo.

Esta skill **só analisa e recomenda**. Ela não escreve, não cria draft, não publica. Quando o usuário aprovar um tema do relatório, o caminho é a skill `criar-post-blog`.

## Inputs

- **Lista de temas** (obrigatório) — uma lista de ideias/títulos/assuntos. Se vier um só, tudo bem. Se vier vago ("uns posts sobre IA"), peça 1 linha por tema antes de começar.
- **Objetivo do ciclo** (opcional) — o que o usuário quer priorizar: tráfego rápido (quick wins), autoridade num pilar, ou volume bruto. Default: equilíbrio (ver scoring). Se não disser, assuma o default e diga que assumiu.
- **Janela de dados** (opcional) — período do GSC/GA a analisar. Default: últimos 90 dias.

## Constantes do projeto (não perguntar ao usuário)

| recurso | valor |
|---|---|
| GSC site_url | `https://blog.beerandcode.com.br/` |
| GA4 property | `properties/<GA4_PROPERTY_ID>` — o ID está em `.env` (`grep GA4_PROPERTY_ID .env`); se faltar, descubra com `mcp__analytics-mcp__get_account_summaries` (property "Blog Beer and Code") |
| DataForSEO locale BR | `location_name: "Brazil"` + `language_code: "pt"` (equivalente: `location_code: 2076`) |
| Domínio para ranked keywords | `blog.beerandcode.com.br` (sem `https://`, sem `www`) |

Os outros domínios do GSC/GA (`beerandcode.com.br`, `loja...`) **não** são deste blog — não misture.

## Como falar com o DataForSEO (ler uma vez, vale pra skill inteira)

O server MCP é **`dfs-mcp`** e é um gateway genérico: **não existe uma tool por endpoint**. Tudo passa por `mcp__dfs-mcp__api_request` com `method` + `path` + `data`.

- **Antes da primeira chamada** carregue os schemas (tools *deferred*; sem isso dá InputValidationError):
  `ToolSearch({query: "select:mcp__dfs-mcp__api_request,mcp__dfs-mcp__docs_search,mcp__dfs-mcp__docs_index,mcp__dfs-mcp__docs_list_sections", max_results: 5})`
- `data` é **sempre um array** de tasks, mesmo pra uma só; o locale vai dentro do objeto.
- **Modo `.ai` (default)**: a resposta vem enxuta e **achatada** — leia `items` direto na raiz, **nunca** `tasks[0].result[0]`. Sucesso é `status_code: 20000` (erro de payload: 40501). `noAiMode: true` traz o schema completo e incha o contexto: só em último caso, em poucas keywords.
- Precisou de endpoint que esta skill não cobre? Ache o path com `docs_list_sections`/`docs_index` — **não invente path**. `docs_search` em endpoint grande (ranked_keywords, competitors_domain) estoura o contexto; só pra campo específico.
- Nome de campo de filtro/`order_by` não bate? `GET /v3/dataforseo_labs/available_filters` devolve o mapa campo→tipo por endpoint, e `GET /v3/dataforseo_labs/locations_and_languages` o locale — **os dois são grátis**. Conferir custa zero; chutar custa uma chamada 40501.

## Pipeline

Quatro passos. O passo 1 e 2 podem rodar em paralelo por tema; o 3 sintetiza; o 4 entrega.

### 1. Baseline do domínio (uma vez, no início)

Antes de olhar tema por tema, levante o terreno que o blog já pisa. Isso evita recomendar tema que canibaliza post existente e revela *quick wins* (temas onde já existe tração e só falta conteúdo dedicado).

- **GSC — o que o blog já recebe:** `mcp__gscServer__get_search_analytics` (site `https://blog.beerandcode.com.br/`, dimensão `query` e depois `page`, janela default 90d). Guarde as queries com impressão e a posição média de cada uma.
- **DataForSEO — o que o domínio já rankeia hoje:**

```
mcp__dfs-mcp__api_request({ method: "POST",
  path: "/v3/dataforseo_labs/google/ranked_keywords/live",
  data: [{ target: "blog.beerandcode.com.br", location_name: "Brazil", language_code: "pt",
           item_types: ["organic"], limit: 100,
           order_by: ["ranked_serp_element.serp_item.rank_group,asc"] }] })
```

Keyword em `items[].keyword_data.keyword` (endpoint aninhado: filtros e `order_by` de keyword pedem o prefixo `keyword_data.`); posição em `items[].ranked_serp_element.serp_item.rank_group` — **é essa** que vale pra striking distance, `rank_absolute` conta AI overview/PAA/vídeo e engana. O KD aqui vem `null` com frequência; se for critério de corte, pegue no passo 2a.

- **Trajetória do domínio** (o ciclo passado funcionou ou não):

```
mcp__dfs-mcp__api_request({ method: "POST",
  path: "/v3/dataforseo_labs/google/historical_rank_overview/live",
  data: [{ target: "blog.beerandcode.com.br", location_name: "Brazil", language_code: "pt" }] })
```

Devolve mês a mês `count`, `etv`, `pos_4_10`, `pos_11_20`, `is_new`, `is_lost`, `is_up`, `is_down`. Abra o relatório com essa linha (ex.: ETV 4,7 em mar → 35,7 em ago) e use `is_lost`/`is_down` como **fila de refresh**: keyword que o blog tinha e perdeu é "otimizar post existente", não pauta nova.

- **GA4 — o que o conteúdo atual entrega depois do clique:**

```
mcp__analytics-mcp__run_report({ property_id: "properties/<GA4_PROPERTY_ID>",
  date_ranges: [{ start_date: "90daysAgo", end_date: "today" }],
  dimensions: ["pagePath"],
  metrics: ["screenPageViews", "userEngagementDuration", "engagementRate", "bounceRate"],
  order_bys: [{ metric: { metric_name: "screenPageViews" }, desc: true }], limit: 50 })
```

`userEngagementDuration` é o **total** em segundos, não a média — o engajamento por leitura é `userEngagementDuration / screenPageViews`. Cruze com o GSC por `pagePath`:

- **Muita impressão + engajamento alto** → o pilar funciona. Tema vizinho herda a força: sobe no scoring.
- **Muita impressão + engajamento baixo / `bounceRate` alto** → a página atrai e não entrega. Isso é **refresh do post existente**, não pauta nova — mesmo que a keyword pareça boa.
- **Post recente sem tração nenhuma em 90d** → o ângulo não pegou. Não repita o formato num tema irmão.

### 2. Análise por tema

Para **cada tema da lista**, colete (agrupe keywords em lote e filtre no servidor — ver "Custo"):

**a) Keyword-alvo e métricas**

- Defina 1 keyword-alvo principal + 2–4 variações plausíveis para o tema.
- **Volume + KD + intenção + formato da SERP num tiro só** (até 700 keywords por chamada — mande as variações de todos os temas juntas):

```
mcp__dfs-mcp__api_request({ method: "POST",
  path: "/v3/dataforseo_labs/google/keyword_overview/live",
  data: [{ keywords: ["engenharia de contexto", "o que é engenharia de contexto"],
           location_name: "Brazil", language_code: "pt", include_serp_info: true }] })
```

Leia `items[].keyword_info.search_volume` / `.cpc` / `.search_volume_trend.yearly`, `keyword_properties.keyword_difficulty`, `search_intent_info.main_intent`, `serp_info.serp_item_types` (`ai_overview`, `featured_snippet`, `people_also_ask`, `video`) e `serp_info.se_results_count`. **Case pelo campo `keyword`, nunca pelo índice** — keyword sem registro some do `items`.

Pra KD em massa (até 1000 kws) use `.../bulk_keyword_difficulty/live`, mas com **payload próprio**: só `keywords` + `location_name` + `language_code` (+ `tag` opcional). Mandar `include_serp_info` aí dá 40501 "Invalid Field". Ele devolve só `items[].keyword` e `items[].keyword_difficulty` — volume e intenção continuam vindo do `keyword_overview`.

- **Perguntas reais que viram H2** — filtro no servidor, não depois:

```
mcp__dfs-mcp__api_request({ method: "POST",
  path: "/v3/dataforseo_labs/google/keyword_suggestions/live",
  data: [{ keyword: "engenharia de contexto", location_name: "Brazil", language_code: "pt",
           include_serp_info: true, limit: 40,
           filters: [["keyword", "regex", "(^| )(o que|oque|como|por que|porque|qual|quais|quando|onde|quanto|vale a pena)( |$)"],
                     "and", ["keyword_info.search_volume", ">=", 50]],
           order_by: ["keyword_info.search_volume,desc"] }] })
```

Aqui `keyword` é **singular**. Pra expandir o universo temático (keywords que não contêm a seed): `.../related_keywords/live` (`keyword` singular, `depth: 2`, resposta **aninhada** em `keyword_data.`) ou `.../keyword_ideas/live` (`keywords` array).

- **Varredura de decisão:** repita a chamada acima com as seeds `"<tema> vs"`, `"melhor <tema>"`, `"alternativa <tema>"`, trocando o regex por só `[["keyword_info.search_volume", ">", 50]]`. Comparação é o padrão vencedor do blog — não deixe as variações só no informacional.
- **Intenção, quando não estiver óbvia** (barato, aceita lote; **não aceita location**):

```
mcp__dfs-mcp__api_request({ method: "POST",
  path: "/v3/dataforseo_labs/google/search_intent/live",
  data: [{ keywords: ["claude code vs cursor", "o que é rag"], language_code: "pt" }] })
```

Lê-se `items[].keyword_intent.label` + `.probability`. **Corte:** descarte só se `navigational`/`transactional` com probability > 0.6 **e** sem intenção informacional secundária. Keyword de comparação costuma dar navigational fraco (~0.47) com informacional atrás — isso é pauta boa. As secundárias (`secondary_keyword_intents`) só aparecem com `noAiMode: true`; use em poucas keywords, só na dúvida real.

**b) Tração atual (GSC)**
- O domínio já recebe impressão para essa keyword ou variações (cruze com o baseline do passo 1)?
- Em que posição média? **Posição 5–20 com impressões e sem post dedicado = quick win** (alta prioridade).
- Existe post já rankeando para essa query? Se sim, **não é pauta nova — é otimização de existente**; sinalize como "canibalização / melhor reforçar o post X" em vez de escrever novo.

**c) Concorrência na SERP** (só na keyword-alvo principal de cada tema)

```
mcp__dfs-mcp__api_request({ method: "POST",
  path: "/v3/serp/google/organic/live/advanced",
  data: [{ keyword: "o que é rag", location_name: "Brazil", language_code: "pt",
           depth: 10, load_async_ai_overview: true }] })
```

`keyword` singular; `depth: 10` = página 1 (é o próprio default — não suba, cada bloco de 10 resultados é cobrado). `items[]` vem achatado com todos os elementos em ordem, cada um com `type`:

- `organic` → quem ocupa o top 10 e que tipo de conteúdo é (doc oficial, blog concorrente, fórum, vídeo) → **qual a brecha** (ângulo que ninguém cobre, conteúdo desatualizado, profundidade rasa).
- `people_also_ask` → os `title` dos sub-itens desse bloco são as **perguntas exatas em pt-BR do Google**: viram os H2 do post (campo `perguntas_paa`). Já vêm sem clique nenhum — **não ligue `people_also_ask_click_depth`**: ele cobra a mais e só compra as respostas (`expanded_element`), que a gente descarta.
- `ai_overview` → `references[].domain/url/title` = quem o Google cita na resposta de IA; sinal melhor de "quem ganha a SERP" do que o top 10 puro. Só gringos nas referências = brecha em pt-BR, e o post deve abrir com definição direta e citável.
- `related_searches` → variações reais para `keywords_secundarias`.

Opcional, pra saber se a SERP do pilar inteiro é ganhável: `.../serp_competitors/live` com `data: [{ keywords: [...até 200...], location_name: "Brazil", language_code: "pt", item_types: ["organic"], limit: 20 }]` → olhe `visibility` e `median_position`.

**d) Encaixe com a marca**
- O tema cabe no escopo do blog (IA aplicada, LLMs, Claude/OpenAI/Gemini, Laravel/PHP, RAG, agentes, embeddings, engenharia de prompt, ferramentas de dev)? Tema fora do pilar perde pontos de prioridade mesmo com bom volume.

### 3. Scoring e priorização

Pontue cada tema de 0 a 100 combinando os sinais. Não precisa de fórmula fechada — use o rubric e seja consistente entre os temas:

| sinal | peso | leitura |
|---|---|---|
| **Oportunidade de tração** | alto | Volume real **× viabilidade**. Volume alto com KD baixo/médio pontua muito. Volume alto com KD altíssimo (dominado por docs oficiais/gigantes) pontua pouco. |
| **Quick win (GSC)** | alto | Já recebe impressão em posição 5–20 sem post dedicado → bônus forte. É o ganho mais rápido que existe. |
| **Intenção** | médio | Informational = ideal para blog. Navigational/transactional forte (>0.6 sem informacional secundária) = penaliza. |
| **Brecha na SERP** | médio | Top 10 raso/desatualizado/sem ângulo prático = espaço para entrar. Top 10 só de docs oficiais profundos = difícil. |
| **Fit com o pilar da marca** | médio | Dentro do escopo técnico do blog soma; fora subtrai. |
| **Engajamento do pilar (GA4)** | médio | Posts vizinhos com `engagementRate` alto = o formato converte, o tema herda. Impressão alta com engajamento baixo no post existente = refresh, não pauta nova. Pilar sem nenhum post medido = sinal ausente, não penaliza. |
| **Ganhabilidade** | trava | `avg_backlinks_info.referring_domains` do top 10 — vem de graça no payload do `keyword_suggestions`/`related_keywords` (se não vier no `keyword_overview`, leia de lá). Acima de ~300 a SERP está fora do alcance deste domínio **por mais baixo que o KD diga**: `claude ai` = KD 37 e 2.976 ref. domains (impossível); `o que é rag` = KD 1 e 44 (entra). |
| **Canibalização** | trava | Se já existe post rankeando, rebaixa de "pauta nova" para "otimizar existente". |

Ajuste os pesos conforme o **objetivo do ciclo** declarado no input (quick wins → suba o peso de GSC; autoridade → suba volume+pilar).

### 4. Relatório

Siga `references/report-template.md`. Duas camadas:

1. **Tabela de triagem (chat)** — todos os temas com keyword-alvo, volume, KD, intenção, sinal de quick win e veredito (`escrever agora` / `escrever depois` / `otimizar post existente` / `reposicionar` / `descartar`). É o que justifica o corte: mostra por que cada tema entrou ou ficou de fora. Abra com a trajetória do domínio (passo 1) e feche com um **"comece por estes"** (top 3) e, se houver, as **otimizações de posts existentes** (inclusive as vindas de `is_lost`/`is_down`).

2. **Pauta dos aprovados (formato de campos)** — só os temas que sobreviveram à triagem, cada um no formato fixo abaixo. É o que alimenta `criar-post-blog`:

```
## <Título do post>
- publicar_em: <ISO 8601 com -03:00; 09:00 BRT default; posts no mesmo dia escalonam a hora>
- autor: <slug do autor, ex.: lucas>
- categoria: <uma das reais — confirme com ListCategories. Conceitual/explicativo → Notícias; mão-na-massa/código → Tutoriais; pacote Laravel → Pacotes>
- resumo: <2–4 linhas: o que o post entrega e o diferencial>
- hook: <1–2 frases no tom da marca>
- bullets:
  - <5 sub-itens = os H2 / promessas do post>
- perguntas_paa:
  - <3–5 perguntas literais do bloco people_also_ask da SERP — são elas que viram H2>
- keyword_principal: <keyword-alvo>
- keywords_secundarias: <2–4 variações / long-tail / termos de decisão (vs, melhor, alternativa)>
- tags: <tags reutilizáveis; confirme com ListTags na hora de criar>
- dificuldade: <easy | medium | hard>
- volume: <vol/mês + KD + tendência, ex.: ~1.300/mo (KD 23, +60%/ano)>
```

**Onde entregar:** mostre as duas camadas no chat. Se o usuário pedir para salvar, grave **só a camada 2** (a tabela de triagem é raciocínio, não pauta) em `pautas/<mês>/semana-N.md` — pergunte o caminho/nome se não estiver claro. Não use o formato de prosa/ficha antigo no arquivo.

## Custo (importante)

DataForSEO e GSC retornam payloads grandes. Para não estourar tokens:

- **Filtre no servidor, não no modelo:** `filters` + `order_by` + `limit` explícito na chamada (piso de volume ≥ 100 pra tema principal, ≥ 50 pra long-tail). Puxar lista crua e filtrar depois custa uma ordem de grandeza a mais.
- **Agrupe keywords** numa chamada só (`keyword_overview` até 700, `bulk_keyword_difficulty` e `search_intent` até 1000) em vez de 1 por keyword.
- **Limite SERP** ao top 10 (`depth: 10`), só na keyword-alvo principal. Nunca ligue `include_clickstream_data` (dobra o preço) nem `people_also_ask_click_depth` (cobra por clique e só traz resposta que a gente descarta).
- **`load_async_ai_overview` é cobrado à parte** (+$0,002 por request) e escala com o tamanho da lista — vale na keyword-alvo, não em varredura.
- Puxe o baseline do GSC **uma vez** no passo 1 e reaproveite; não refaça por tema.
- Se a lista for grande (>8 temas), avise o usuário do custo e ofereça rodar em lotes.

## Quando o tema não se sustenta

Se um tema tem volume ~zero, intenção errada (transactional forte), SERP com ref. domains fora do alcance ou impenetrável, **diga isso** com o número na frente e marque `descartar` ou `reposicionar` — sugira o recorte/keyword que salvaria o tema, se houver. Não infle prioridade de pauta ruim para agradar. O valor da skill é cortar o que não vale antes de gastar tempo escrevendo.

## Pré-requisitos do ambiente

- MCP `gscServer` (Search Console), `analytics-mcp` (GA4) e `dfs-mcp` (DataForSEO) carregados na sessão. Se algum faltar, avise qual e siga com os disponíveis, deixando claro no relatório qual sinal ficou de fora.
- Acesso de owner às propriedades do blog (já confirmado nas constantes acima).
