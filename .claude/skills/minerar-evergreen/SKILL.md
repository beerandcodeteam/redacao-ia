---
name: minerar-evergreen
description: Minera temas EVERGREEN (duráveis, não perecíveis) para o blog Beer & Code (blog.beerandcode.com.br) — garimpa keywords de demanda estável/crescente que trazem tráfego por anos, ao contrário do news-jacking que seca em semanas. Descobre do zero cruzando expansão de keywords no DataForSEO, striking-distance no Search Console (termos que já pingam impressão sem post dedicado), gap de conteúdo vs concorrentes, e um gate de durabilidade na curva histórica de volume (12 meses de monthly_searches + Google Trends; curva plana/subindo = evergreen, pico-e-morte = descarta). Acionar quando o usuário pedir "minerar evergreen", "achar tema evergreen", "pauta durável", "conteúdo que dura", "o que plantar pro longo prazo", "temas perenes", "construir baseline de SEO" ou equivalente. Entrega candidatos ranqueados no formato de campos da planejar-pauta (não escreve nem publica — para isso use planejar-pauta e depois criar-post-blog).
---

# Minerar evergreen — Beer & Code

Descobre o tema **durável** — o que as pessoas continuam buscando daqui a 1-2 anos — e devolve candidatos de pauta ranqueados, no mesmo formato que alimenta a `planejar-pauta`. É o **par simétrico** do `cacar-news-jacking`: aquele caça hype perecível de 48h; este garimpa demanda estável que constrói o **baseline** de tráfego que sobrevive quando o hype de modelo seca.

Por que existe: hoje ~54% dos cliques do blog vêm de 2 clusters de news-jacking (Fable/GPT), tração efêmera em cima de areia — evergreen é o piso (memória `project_seo_roadmap`). Esta skill **descobre, qualifica e ranqueia**; não escreve nem publica. Fluxo: `minerar-evergreen` → usuário aprova candidatos → `planejar-pauta` (vira pauta em campos) → `criar-post-blog`.

## Constantes do projeto (não perguntar)

| recurso | valor |
|---|---|
| GSC site_url | `https://blog.beerandcode.com.br/` |
| GA4 property | `properties/<GA4_PROPERTY_ID>` — o ID está em `.env` (`grep GA4_PROPERTY_ID .env`); se faltar, descubra com `mcp__analytics-mcp__get_account_summaries` (property "Blog Beer and Code") |
| DataForSEO location / language | `location_code: 2076` (Brazil) + `language_code: "pt"` — vão **dentro** de cada task do `data`, não como parâmetro de tool. `location_name: "Brazil"` é equivalente e alguns payloads desta skill usam ele: proposital. Proibido é **misturar os dois na mesma task** — isso quebra a chamada |
| Domínio para ranked keywords | `blog.beerandcode.com.br` (sem `https://`, sem `www`) |

Os outros domínios do GSC (`beerandcode.com.br`, `loja...`) **não** são deste blog — não misture.

## Como falar com o DataForSEO (server `dfs-mcp`) — ler uma vez

Não existem mais tools por endpoint. **Tudo** passa por `mcp__dfs-mcp__api_request({ method, path, data })`.

- As tools do `dfs-mcp` são **deferred**. Antes da primeira chamada, rode:
  `ToolSearch({ query: "select:mcp__dfs-mcp__api_request,mcp__dfs-mcp__docs_search,mcp__dfs-mcp__docs_index,mcp__dfs-mcp__docs_list_sections", max_results: 5 })`. Sem isso a chamada falha com `InputValidationError`.
- `data` é sempre um **array** de tasks, mesmo pra uma só: `data: [{...}]`. Sucesso é `status_code: 20000`.
- **Modo `.ai` (default)**: a resposta já vem enxuta, com `items` **na raiz**. Não navegue `tasks[].result[]` — isso não existe aqui. `noAiMode: true` só em último caso: traz o schema cru e incha o contexto.
- Duas formas de resposta: **achatada** (`items[].keyword_info…`) em keyword_overview / keyword_suggestions / keyword_ideas / top_searches; **aninhada** (`items[].keyword_data.…`) em ranked_keywords / related_keywords / domain_intersection. `filters` e `order_by` usam o mesmo prefixo da forma correspondente.
- Filtro: `filters: [[campo, op, valor], "and", [campo, op, valor]]` (o "and"/"or" é elemento do array). Máx. 8 condições, 3 regras de `order_by`, `limit` 1000. Faixa numérica = duas condições (`>=` e `<=`); `in` é conjunto de valores exatos, **não** intervalo.
- Nome de campo de filtro não bate? `GET /v3/dataforseo_labs/available_filters` devolve o mapa campo→tipo por endpoint; locale em `GET /v3/dataforseo_labs/locations_and_languages`. Os dois são **gratuitos**.
- Precisa de um endpoint que esta skill não cobre? `mcp__dfs-mcp__docs_list_sections` → `docs_index({section})` pra achar o path, `docs_search({url})` pra ler. **Nunca invente path.** Evite `docs_search` em `ranked_keywords`/`competitors_domain`: docs gigantes, estouram o contexto.

## Gate de DOR (topo de funil) — aplicar antes de qualquer outro

O que funciona como evergreen neste blog é **dor de consciência baixa**: quem busca ainda não escolheu produto, mas tem um problema concreto ("como economizar tokens" +340%, "qual a melhor IA para programar" +278%). Pauta centrada em produto ("o que é o Codex", "como instalar o Claude Code", "preço do Claude") foi rejeitada em 13/09/2026: é news-jacking disfarçado, morre quando a ferramenta muda.

- **Semear com verbos de problema**, não com nome de ferramenta: economizar, gastar menos, qual usar, vale a pena, por que erra/esquece/alucina, como fazer X com IA, de graça, sem pagar.
- **Filtro por candidato**: "isso é uma dor ou é um produto?" Produto só entra como **spoke** de um hub de dor (ex.: "como gastar menos tokens no Claude" é spoke de "como economizar tokens"; "o que é o Codex" não entra).
- **Título casa a dor**, o produto aparece na resposta. "Claude ou ChatGPT: qual usar" passa; "Como instalar o Codex CLI" não passa.
- **GSC com filtro `contains: como`** (e `por que`, `qual`) é a fonte mais barata de dor já provada no domínio: variações com impressão em pos 5-15 e zero clique são o primeiro lugar pra olhar.
- Antes de propor post novo de dor, rode `list-posts` com a raiz da dor (agente, prompt, alucina, token, gratuit): o blog já cobre muitas dores que **não rankeiam** por título errado ou canibalização. Nesse caso o veredito é `atualizar existente`, não post novo.

## Inputs

- **Foco / pilar** (opcional) — recorte temático pra semear a mineração. Default: os pilares do blog — IA aplicada, LLMs, Claude/OpenAI/Gemini API, RAG, embeddings, agentes de IA, engenharia de prompt/contexto, SDD/evals, Laravel/PHP. Se o usuário der foco ("só RAG", "Laravel"), semeie só com aquilo.
- **Nº de candidatos** (opcional) — quantos temas entregar. Default: top 8.
- **Concorrentes** (opcional) — domínios pra gap analysis. Se não vier, descubra no passo 1c com `competitors_domain`.

## Pipeline

### 0. Baseline do domínio (uma vez, no início)

- **GSC** — `mcp__gscServer__get_search_analytics` (dimensão `query` e depois `page`, janela 90d, row_limit alto). Guarde queries com impressão + posição. **Filtre ruído** (memória `feedback_seo_falsos_quick_wins`): ignore queries de marca ("beer and code", "beerandcode") e o falso quick win `quanto-ganha-engenheiro-de-ia-brasil-2026` (compete com Forbes/Glassdoor, CTR-teto).
- **DataForSEO** — onde o domínio já rankeia + posição:

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/dataforseo_labs/google/ranked_keywords/live",
  data: [{ target: "blog.beerandcode.com.br", location_code: 2076, language_code: "pt",
           item_types: ["organic"], limit: 100,
           order_by: ["keyword_data.keyword_info.search_volume,desc"] }]
})
```

A posição está em `items[].ranked_serp_element.serp_item.rank_group` (orgânica pura — **é este** o campo de striking distance) e `.rank_absolute` (conta AI overview/PAA/vídeo). Não existe campo `position`.

Saída: mapa de "onde já temos força" — insumo pro striking-distance (passo 1b) e pra evitar canibalização.

### 1. MINERAR (descobrir candidatos do zero)

Junte candidatos de **três frentes** e deduplique. **Filtre no servidor**, não no modelo: piso de volume ≥ 100 (BR é mercado pequeno), intenção informacional, KD controlado. Isso corta o payload em uma ordem de grandeza.

**a) Expansão de seeds (DataForSEO)** — para cada seed do foco:

Perguntas reais (viram H2 do post e definem o formato do título):

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/dataforseo_labs/google/keyword_suggestions/live",
  data: [{ keyword: "rag", location_code: 2076, language_code: "pt", limit: 40,
           filters: [["keyword","regex","^(o que|oque|como|por que|porque|para que|qual|quais|quando|vale a pena)\\b"],"and",
                     ["keyword_info.search_volume",">=",100],"and",
                     ["search_intent_info.main_intent","=","informational"]],
           order_by: ["keyword_info.search_volume,desc"] }]
})
```

Pra pegar pergunta em **qualquer posição** da frase ("claude code o que é"), troque o regex por `"(^| )(o que|oque|como|por que|qual|quais|quando|vale a pena)( |$)"`. `keyword` aqui é **string singular** e o resultado sempre **contém** a seed.

Universo temático mais amplo (não precisa conter a seed — traz a mesma categoria):

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/dataforseo_labs/google/keyword_ideas/live",
  data: [{ keywords: ["rag","embeddings","agentes de ia"], location_code: 2076, language_code: "pt", limit: 200,
           filters: [["keyword_info.search_volume",">=",100],"and",
                     ["keyword_properties.keyword_difficulty","<=",35],"and",
                     ["search_intent_info.main_intent","<>","navigational"]],
           order_by: ["keyword_info.search_volume,desc","keyword_properties.keyword_difficulty,asc"] }]
})
```

Complemento: `/v3/dataforseo_labs/google/related_keywords/live` (campo `keyword` singular, `depth: 2`, `limit: 50`) — vem das "pesquisas relacionadas" e traz de graça `avg_backlinks_info`, `serp_info` e `core_keyword`, usados nos passos 2 e 3. Prefixo obrigatório: `filters: [["keyword_data.keyword_info.search_volume",">=",100]]`.

O que **cresce** na categoria: `/v3/dataforseo_labs/google/top_searches/live`. Esse endpoint **não tem campo de seed** — sem `filters` ele dumpa o Brasil inteiro. Sempre mande `filters: [["keyword","like","%rag%"],"and",["keyword_info.search_volume",">",100]]` e `order_by: ["keyword_info.search_volume_trend.yearly,desc"]`.

**b) Striking-distance (GSC + DataForSEO)** — termos evergreen onde o blog já pinga impressão em **posição 5-20 sem post dedicado**. É o ganho mais rápido que existe — demanda já provada, só falta conteúdo. Além do GSC, peça a faixa direto ao ranked_keywords, filtrada no servidor:

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/dataforseo_labs/google/ranked_keywords/live",
  data: [{ target: "blog.beerandcode.com.br", location_code: 2076, language_code: "pt",
           item_types: ["organic"], limit: 200,
           filters: [["ranked_serp_element.serp_item.rank_group",">=",5],"and",
                     ["ranked_serp_element.serp_item.rank_group","<=",20],"and",
                     ["keyword_data.keyword_info.search_volume",">=",50]],
           order_by: ["keyword_data.keyword_info.search_volume,desc"] }]
})
```

Cruze com `list-posts` do MCP do blog pra confirmar que não há post dedicado.

**c) Gap de conteúdo (DataForSEO)** — primeiro descubra quem disputa a mesma SERP (`/v3/dataforseo_labs/google/competitors_domain/live`, `data: [{ target: "blog.beerandcode.com.br", location_code: 2076, language_code: "pt", limit: 20, exclude_top_domains: true }]` — o `exclude_top_domains` tira wikipedia/youtube/reddit). Depois, o gap contra cada concorrente:

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/dataforseo_labs/google/domain_intersection/live",
  data: [{ target1: "www.alura.com.br", target2: "blog.beerandcode.com.br",
           location_code: 2076, language_code: "pt",
           intersections: false, item_types: ["organic"], limit: 30,
           filters: [["first_domain_serp_element.rank_group","<=",10],"and",
                     ["keyword_data.keyword_info.search_volume",">",100],"and",
                     ["keyword_data.keyword_info.search_volume","<",10000],"and",
                     ["keyword_data.search_intent_info.main_intent","=","informational"]],
           order_by: ["keyword_data.keyword_info.search_volume,desc"] }]
})
```

**A ordem importa**: `intersections: false` + concorrente em `target1` + blog em `target2` = o que ele rankeia e nós não; invertido, é o gap ao contrário. Os filtros não são opcionais — sem teto de volume volta cabeça-de-cauda impossível ("canva", "claude"), sem `rank_group <= 10` volta ruído. Descarte manualmente as queries de **marca do concorrente**.

### 2. GATE de durabilidade (o que separa evergreen de news-jack)

**Trava obrigatória.** O gate primário **não custa chamada extra**: `keyword_overview` (e `keyword_suggestions`/`related_keywords`) já devolve `keyword_info.monthly_searches` (12 meses de volume absoluto BR) e `keyword_info.search_volume_trend {monthly, quarterly, yearly}`.

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/dataforseo_labs/google/keyword_overview/live",
  data: [{ keywords: ["o que e rag","langchain tools","claude ai"], location_code: 2076, language_code: "pt",
           include_serp_info: true }]
})
```
`keywords` é array (até 700 numa chamada). Case o resultado pelo campo `keyword` — keyword sem registro no banco **some** do `items`, a ordem não é garantida.

Leitura da curva (`monthly_searches` + `search_volume_trend.yearly`):

- **Plana ou subindo** (`yearly >= 0`, sem pico único > 3× a mediana) → evergreen legítimo. **Passa.** (medido: "o que é rag", yearly +52, 2400 → 4400)
- **Queda forte** (`yearly` muito negativo) → tema morto travestido de evergreen. **Descarta.** (medido: "langchain tools", yearly −81, 260 → 50)
- **Curva de foguete** (`yearly` na casa das centenas/milhares) → não é evergreen, é hype. **Reencaminha pro `cacar-news-jacking`.** (medido: "claude ai", yearly +646, 246k → 1,83M)
- **Sazonal previsível** (sobe todo ano na mesma época) → passa, mas marca a sazonalidade na pauta.

**Fallback obrigatório — `search_volume_trend.yearly` vem ausente com frequência** (medido: 3 de 10 itens do ranked_keywords do blog, 1 de 5 do keyword_suggestions). Quando faltar, **derive a tendência à mão**: média dos **3 meses mais recentes** de `monthly_searches` contra a média dos **3 mais antigos** da série de 12 — queda ≥ 20% = queda forte (descarta), alta ≥ 20% = subindo, entre os dois = plana. **NUNCA trate `yearly` ausente como 0** — o 0 cai na regra "passa" e aprova um pico-e-morte como evergreen (medido: "claude design como usar", 10 → 4400 → 1000, passaria pelo gate).

**Confirmação no Google Trends** (opcional, só quando a curva de 12 meses ficou ambígua — precisa de janela maior):

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/keywords_data/google_trends/explore/live",
  data: [{ keywords: ["rag"], location_name: "Brazil", language_code: "pt",
           date_from: "2024-01-01", item_types: ["google_trends_graph"] }]
})
```
Janela: `date_from`/`date_to` (`yyyy-mm-dd`) — sem eles o default é só 12 meses, pouco pro gate; peça 24-36 meses (`date_from` ignora `time_range`). Máx. 5 keywords/request, mas os `values` são normalizados pelo maior volume — **pra gate individual, 1 keyword por chamada**. O último ponto vem com `missing_data: true` (semana incompleta): ignore.

**Segundo eixo — durabilidade dentro das IAs** (para os finalistas, não para a lista toda):

```
mcp__dfs-mcp__api_request({
  method: "POST",
  path: "/v3/ai_optimization/ai_keyword_data/keywords_search_volume/live",
  data: [{ keywords: ["o que e rag","claude code"], location_name: "Brazil", language_code: "pt" }]
})
```
Devolve `ai_search_volume` + `ai_monthly_searches` (12 meses). Cruze com o Google: **Google estável + IA caindo** = evergreen em decadência, rebaixa. **Google morno + IA subindo forte** = evergreen **nascente**, sobe a prioridade — é a única janela em que um blog pequeno chega antes (medido: "claude code" foi de 5 para 140 em 12 meses na IA).

### 3. QUALIFICAR cada candidato

Mesma lógica da `planejar-pauta`, em lote pra economizar token:

- **Dedup por `core_keyword`** — `keyword_properties.core_keyword` agrupa variações que o Google trata como a mesma coisa (medido: "o que é rag" e "rag o que é" compartilham core). **Um post por core_keyword**: a variação de maior volume vira `keyword_principal`, as outras entram em `keywords_secundarias`. Faça isso **antes** de escrever a entrega, senão a própria skill entrega dois candidatos que vão canibalizar um ao outro.
- **KD e intenção** — o KD embutido vem `null` com frequência; se é critério de corte, rode `/v3/dataforseo_labs/google/bulk_keyword_difficulty/live` (`data: [{ keywords: [...até 1000], location_code: 2076, language_code: "pt" }]` — 1 request, devolve só `keyword` + `keyword_difficulty`). Intenção em lote: `/v3/dataforseo_labs/google/search_intent/live` (`data: [{ keywords: [...], language_code: "pt" }]` — **não aceita location**; campo `keyword_intent{label, probability}`). **Informational é o alvo**, mas descarte só se `navigational`/`transactional` vier com `probability > 0.6` **e** sem intenção informacional secundária — senão você joga fora keyword de comparação ("X vs Y"), padrão vencedor do blog.
- **Triagem de SERP de graça** — `serp_info.serp_item_types` e `se_results_count`: `keyword_overview` e `keyword_suggestions` **exigem** `include_serp_info: true` (sem a flag não vem bloco `serp_info` nenhum); `related_keywords` e `ranked_keywords` já trazem de graça. A flag **não** dobra o preço — só `include_clickstream_data` dobra. Leia **antes** de gastar chamada de SERP. `se_results_count` baixo = SERP rasa, janela aberta; `featured_snippet` = posição zero pra roubar; `ai_overview` + `video` = clique orgânico comprimido, o post precisa ser escrito pra ser **citado** (definição fechada na primeira frase).
- **SERP só nos finalistas** — `/v3/serp/google/organic/live/advanced`, `data: [{ keyword, location_code: 2076, language_code: "pt", depth: 10 }]` (`depth: 10` = página 1; nunca o default 100). Traz `ai_overview.references[]` (quem o Google cita), `people_also_ask` (perguntas literais → H2) e `related_searches`.
- **Dedup contra o blog** — `mcp__beer-and-code-blog__list-posts`. Se já existe post no tema → **não é pauta nova, é atualizar/reforçar o existente** (regra anti-canibalização). Sinalize "atualizar post X". Aproveite pra flagar **decay**: post evergreen antigo que escorregou de posição = candidato a refresh.

### 4. PONTUAR

Pontue 0-100 por candidato (rubric, sem fórmula fechada). **Pesos diferem do news-jacking**: aqui durabilidade e volume mandam, velocidade não conta.

| sinal | peso | leitura |
|---|---|---|
| **Durabilidade (curva de volume)** | alto | `monthly_searches` plano/subindo + `search_volume_trend.yearly >= 0` (ou, se `yearly` faltar, o fallback 3m recentes × 3m antigos do passo 2). É o coração do evergreen — sem isso, não entra. |
| **Volume real × viabilidade (KD)** | alto | Volume BR consistente + KD baixo/médio. Ao contrário do news-jack, aqui volume ~0 **não** é oportunidade — é sinal de tema sem demanda. |
| **Quick win (GSC striking-distance)** | alto | Já pinga impressão em pos 5-20 sem post dedicado → bônus forte. |
| **Brecha na SERP** | médio | Top 10 raso/desatualizado/sem ângulo prático = espaço. Só docs oficiais profundos = difícil. Gate duro: `avg_backlinks_info.referring_domains` do top 10 acima de ~300 = fora do alcance do domínio hoje, **independente do KD**. |
| **Fit com o pilar + potencial de cluster** | médio | Dentro do escopo soma. Bônus se ancora um **hub-and-spoke** (topic cluster) que constrói autoridade — ver padrão dos clusters SDD/engenharia de contexto nas memórias. |
| **Canibalização** | trava | Já existe post → rebaixa pra "atualizar existente". |

### 5. ENTREGAR

Siga `references/output-template.md`. Duas camadas:

1. **Radar (chat)** — tabela dos candidatos com fonte (seed/striking-distance/gap), volume/KD, durabilidade da curva, janela de SERP e veredito; fecha com o top 3 "escrever agora" e as otimizações de posts existentes que apareceram.
2. **Pauta dos aprovados** — só os "escrever agora", no formato fixo de campos da `planejar-pauta`. Os `bullets` saem das **perguntas reais** (keyword_suggestions / people_also_ask), não de invenção. Pronto pra `pautas/<mês>/semana-N.md`.

### Fórmula de título pra evergreen (≠ news-jacking)

**Atenção — regra invertida.** No news-jacking o título neutro perde (drama/número ganha o clique). No evergreen o título **casa a intenção informacional**, porque quem busca "o que é RAG" quer exatamente isso — e é o que o Google premia pra query informacional. Clickbait vazio continua fora, mas aqui o "explicativo" é o formato certo, não o erro. O formato sai da **forma da query** que veio no passo 1a:

- **Definição:** "O que é X? Guia prático com exemplo"
- **How-to:** "Como fazer Y em [stack]: passo a passo"
- **Decisão perene:** "X vs Y: quando usar cada um"
- **Erro/dor recorrente:** "Como resolver [problema] no [stack]"

## Custo

- Baseline do GSC + ranked_keywords: **uma vez** no passo 0, reaproveite.
- Deixe `noAiMode` no default (`false`) e filtre no **servidor** (`filters` + `limit`) — são as duas maiores alavancas de contexto.
- Agrupe keywords em chamadas **bulk** (`keywords: [...]` no keyword_overview / bulk_keyword_difficulty / search_intent). SERP só na keyword-alvo dos finalistas; Trends só quando a curva de 12 meses ficou ambígua; AI search volume só nos finalistas. Nunca ligue `include_clickstream_data` (dobra o preço).
- Se a mineração render >12 candidatos, avise do custo e qualifique os de maior durabilidade × volume primeiro.

## Pré-requisitos do ambiente

- MCP `dfs-mcp`, `gscServer`, `beer-and-code-blog` carregados. Rode o `ToolSearch` do bloco "Como falar com o DataForSEO" antes da primeira chamada. Se faltar algum MCP, siga com os demais e sinalize o sinal ausente (sem `dfs-mcp` não há gate de durabilidade — avise que o resultado fica fraco).
- Acesso de owner às propriedades do blog (já nas constantes).
