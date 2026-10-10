# Pesquisa 06 — Protocolos, Interoperabilidade, Interface e Modalidades de agentes (estado em 12/09/2026)

Escopo: técnicas de 2026 (prioridade últimos 6 meses) para agentes em produção (agente de vendas, motor de resolução). Acervo do blog lido na íntegra (~280 slugs) antes de pesquisar. Método: 16 buscas + 13 fetches de fontes primárias (specs, blogs de engenharia, docs oficiais, changelogs). Tudo que é roadmap/rumor está marcado; o resto é shipping com link.

Convenção de maturidade: **experimental** (flag/preview, spec instável) · **early adopters** (GA ou spec estável, mas poucos cases públicos) · **mainstream** (clientes grandes, múltiplos vendors, migração forçada).

---

### 1. MCP 2026-07-28: núcleo stateless, MRTR e extensões (a "segunda geração" do MCP)

- **O que é**
  Revisão da spec publicada em 28/07/2026 (RC em junho) que remove sessões (`Mcp-Session-Id`) e o handshake `initialize`; cada request carrega versão e capabilities em `_meta` (`io.modelcontextprotocol/protocolVersion`, `clientCapabilities`, `clientInfo`). Novo RPC obrigatório `server/discover`. Server-initiated requests (elicitation, sampling, roots) foram substituídas pelo padrão **MRTR (Multi Round-Trip Requests)**: o servidor devolve `resultType: "input_required"` com `inputRequests`; o cliente reenvia a chamada original com `inputResponses`. Todos os results ganham `resultType` obrigatório. Notificações push viram um único stream `subscriptions/listen` (opt-in por tipo). Listas (`tools/list` etc.) agora trazem `ttlMs` e `cacheScope` (cacheáveis por intermediários) e devem ter ordem determinística para preservar prompt cache. Headers `Mcp-Method`/`Mcp-Name` obrigatórios no POST. Resumabilidade SSE (`Last-Event-ID`) removida. **Tasks** saíram do core e viraram extensão (`io.modelcontextprotocol/tasks`, polling via `tasks/get`, input via `tasks/update`). **Deprecados** (janela mínima de 12 meses): Sampling, Roots, Logging, HTTP+SSE, e Dynamic Client Registration (RFC 7591) em favor de Client ID Metadata Documents. Auth endurecida: `iss` (RFC 9207) obrigatório de validar, credenciais chaveadas por issuer.
  Extensões oficiais hoje: **MCP Apps** (`io.modelcontextprotocol/ui`), **Tasks**, **OAuth Client Credentials** (M2M) e **Enterprise-Managed Authorization (EMA)**. Extensões são negociadas no campo `extensions` das capabilities e são sempre opt-in.
- **Quem está usando/shipping**
  - Spec + SDKs Tier 1 (TypeScript, Python, Go, C#) no dia 1; Rust em beta — blog oficial do MCP, 28/07/2026.
  - Cloudflare: servidores MCP saíram de Durable Objects para Workers comuns; `createMcpHandler` graduou para o SDK TS oficial — "The next generation of MCP", 06/08/2026.
  - ChatGPT Apps: callbacks OAuth estáveis + CIMD (changelog OpenAI 21/08/2026).
  - Anthropic Managed Agents: **MCP tunnels** (research preview) para servidores MCP privados dentro do perímetro do cliente + self-hosted sandboxes (public beta) — Code with Claude London, 19/05/2026.
- **Maturidade**: **mainstream em transição forçada**. Spec estável, SDKs oficiais prontos, clientes grandes já aceitam `2026-07-28`. Quem mantém servidor Streamable HTTP do jeito 2025 vai precisar migrar (stateless quebra suposições de sessão; elicitation antiga deixa de funcionar em clientes novos).
- **Aplicação em agente de vendas / motor de resolução**
  - Servidor MCP do CRM/ERP roda atrás de load balancer round-robin sem sticky session; estado cross-call vira handle explícito em argumento de tool (ex.: `quote_id`).
  - MRTR é o mecanismo certo para "preciso confirmar o CPF antes de emitir a 2ª via": a tool devolve `input_required`, o host coleta, reenvia. Substitui gambiarras de "tool que devolve pergunta em texto".
  - Tasks extension para operações longas (gerar proposta em PDF, reprocessar pedido) com polling e input mid-flight.
  - `ttlMs`/ordem determinística = prompt cache hit mais alto em agente que carrega 40+ tools a cada turno.
  - EMA/OAuth client credentials para o agente-backend (M2M) falar com o MCP do ERP sem usuário humano no loop.
- **Gap vs blog**
  Adjacente a `tutoriais/mcp-em-producao-oauth-schema-gateway`, `tutoriais/como-criar-mcp-server`, `tutoriais/como-criar-um-servidor-mcp-do-zero`, `noticias/o-que-e-mcp`. Todos são anteriores à spec 2026-07-28 e presumem sessão/handshake/elicitation server-initiated. **Ângulo novo**: guia de migração "seu servidor MCP de 2025 quebra em 2026-07-28: checklist (stateless, MRTR, `server/discover`, `resultType`, headers `Mcp-*`, deprecação de sampling/DCR)". Nenhum post cobre MRTR, Tasks como extensão, `ttlMs`/`cacheScope` ou o framework de extensões.
- **Fontes**
  - https://modelcontextprotocol.io/specification/2026-07-28/changelog (28/07/2026)
  - https://blog.modelcontextprotocol.io/posts/2026-07-28/ (28/07/2026) e RC: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
  - https://modelcontextprotocol.io/docs/extensions/overview (extensões oficiais, negociação)
  - https://blog.cloudflare.com/mcp-v2/ (06/08/2026)
  - https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/seps/2663-tasks-extension.md
  - Managed Agents sandboxes/tunnels (19/05/2026): https://mer.vin/2026/05/claude-managed-agents-self-hosted-sandboxes-and-private-mcp-tunnels/ (secundária; fonte primária é o keynote Code with Claude London)

---

### 2. Browser use toolset (DOM-first) e a bifurcação "DOM vs visão" nos browser agents

- **O que é**
  Em 01/08/2026 a Anthropic lançou dois *client toolsets* (uma entrada em `tools`, membros com schema fixo, execução do lado do dev): `computer_toolset_20260801` (sucessor estável do computer use beta) e `browser_toolset_20260801` (novo, GA, sem beta header). O browser toolset tem 31 membros: `navigate`, `read_page` (árvore de acessibilidade com refs `[ref_N]`, filtro `interactive`/`all`), `get_page_text`, `find` (busca por descrição natural, até 20 matches), `form_input`, cliques/teclado/scroll, abas, e membros **desabilitados por padrão** por risco: `javascript_exec`, `file_upload`, `read_console`, `read_network`. O modelo opera preferencialmente por refs do DOM (estável a reflow, menos tokens) e cai para screenshot+coordenadas só em canvas/iframe cross-origin. `toolset_name: "browser"` vem no `tool_use` e precisa ser ecoado no `tool_result`; várias chamadas num turno formam *batch action* executada em ordem com halt na primeira falha. Modelos: Opus 5, Sonnet 5, Mythos 5/5.1, Fable 5/5.1, Opus 4.8. Disponível na Claude API e Vertex; **não** em Bedrock/Foundry nem em Managed Agents.
  Em paralelo, o mercado consolidou a leitura de que stacks DOM-driven (Stagehand v3 CDP-nativo sem Playwright, Browserbase) são 12–17 p.p. mais confiáveis que stacks vision-only (Computer Use / CUA) em tarefas comuns, com visão reservada ao que o DOM não alcança.
- **Quem está usando/shipping**
  - Anthropic: `browser_toolset_20260801` GA (docs), Claude in Chrome GA para planos pagos em 26/08/2026 (GIGAZINE), Cowork side panel com prompt-injection checks (claude.com/blog, 12/08/2026).
  - Browserbase/Stagehand v3 (CDP direto, +44% velocidade; releases no GitHub); Browserbase reporta 99,96% de confiabilidade de sessão (benchmarks de terceiros, 2026).
  - OpenAI: Operator encerrado em 31/08/2025; **ChatGPT agent removido do ChatGPT no início de agosto/2026** sem aviso (Help Center da OpenAI, via Wikipedia consultada 27/08/2026); capacidade segue via computer-use tool no Agents SDK. "ChatGPT Work" (09/07/2026) aparece só em fontes terciárias — **não confirmado em fonte primária**, tratar como não verificado.
- **Maturidade**: **early adopters → mainstream** para DOM-first (toolset GA, SDKs maduros); **experimental/decadente** para vision-only em produção. Números de sucesso (78–90%) são de benchmarks de terceiros; ninguém sério roda checkout sem confirmação humana.
- **Aplicação em agente de vendas / motor de resolução**
  - Motor de resolução que precisa operar portal de transportadora/operadora **sem API** (abrir chamado, consultar fatura, emitir 2ª via): `browser_toolset` em container isolado, whitelist de domínios em duas camadas (antes do `navigate` e no proxy), `javascript_exec` desligado, credenciais injetadas pelo executor (nunca visíveis ao modelo).
  - Regra de decisão: API > MCP > browser DOM-first > visão. Browser só quando o custo de integrar API é maior que o custo de manter o fluxo + risco de prompt injection do conteúdo da página.
  - Ações irreversíveis (pagar, cancelar, enviar) sempre com `get_human_approval()` fora do loop do modelo.
- **Gap vs blog**
  Adjacente a `tutoriais/scraping-api-mcp-trade-off-fontes-dados-agente` (trade-off de fonte de dados, não de *ação*) e `noticias/screenpipe-agentes-gravacao-tela-privacidade`. Não há post sobre browser agents como atuador, toolsets nativos da API, refs de accessibility tree vs screenshot, nem sobre a decisão "quando usar browser em vez de API". **Ângulo novo**: "Browser agent em Laravel com `browser_toolset_20260801` + Playwright: o que ligar, o que deixar desligado, e por que DOM-first ganhou de visão".
- **Fontes**
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool (toolset 20260801, GA)
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference (client toolsets, versões)
  - https://claude.com/blog/cowork-chrome-side-panel (12/08/2026)
  - https://gigazine.net/gsc_news/en/20260827-claude-chrome-available/ (GA Claude in Chrome, 26/08/2026 — secundária)
  - https://www.browserbase.com/blog/stagehand-v3 e https://github.com/browserbase/stagehand/releases
  - https://en.wikipedia.org/wiki/OpenAI_Operator (linha do tempo com citações ao Help Center da OpenAI)
  - https://michaellivs.com/blog/state-of-browser-use-2026/ (State of Browser Use, maio/2026 — secundária, benchmarks)

---

### 3. Tool search / `defer_loading` e toolsets: catálogo de ferramentas carregado sob demanda

- **O que é**
  Feature nativa da Claude API (sem beta header): você envia **todas** as definições em `tools`, marca a maioria com `defer_loading: true` e inclui um tool search (`tool_search_tool_regex_20251119` — padrões Python `re.search`, 200 chars — ou `tool_search_tool_bm25_20251119` — linguagem natural, 500 chars). O modelo pesquisa nomes, descrições e argumentos; a API devolve `tool_reference` (até 5 por padrão, `limit` 1–10.000) e expande a definição completa **inline no corpo da conversa, não no prefixo**, então prompt cache é preservado. Limite de 10.000 tools deferidas por request. Também dá para implementar **tool search custom** (embeddings) devolvendo `tool_reference` num `tool_result` normal. Para MCP via connector, `defer_loading` vai no `mcp_toolset.default_config` ou por tool em `configs`. Os toolsets computer/browser deferem "como unidade" (todos os membros com o mesmo valor). Anthropic cita: setup típico com 5 servidores MCP gasta ~55k tokens de definições; tool search reduz >85%; precisão de seleção degrada acima de 30–50 tools.
  Contexto de mercado: a Anthropic empacotou isso em "Advanced Tool Use" (tool search + programmatic tool calling + advisor tool `advisor_20260301`).
- **Quem está usando/shipping**
  - Anthropic Claude API e Claude Platform on AWS (Bedrock só via InvokeModel); Claude Code passou a deferir até ferramentas built-in atrás de `ToolSearch` (issue #31002, 2026).
  - Claude Agent SDK Python ainda não expõe `defer_loading` (issue #525) — lacuna real para quem usa o SDK.
- **Maturidade**: **mainstream** (GA, todos os modelos de Haiku 4.5 em diante, SDKs em 8 linguagens incluindo PHP).
- **Aplicação em agente de vendas / motor de resolução**
  - Agente de atendimento que agrega CRM + ERP + logística + billing (200+ tools via MCP): manter 3–5 tools quentes (`buscar_pedido`, `abrir_ticket`), deferir o resto; namespacing `crm_`, `erp_` para um search pegar o grupo.
  - Tool search custom com pgvector: indexar descrições das tools e devolver `tool_reference` — encaixa no stack Laravel/pgvector do blog.
  - Cuidado: tool deferida não pode ter `cache_control`; breakpoint vai numa tool não deferida.
- **Gap vs blog**
  **Adjacente forte** a `tutoriais/progressive-disclosure-agente-50-ferramentas` (princípio implementado "na mão") e a `tutoriais/programmatic-tool-calling*`. **Ângulo novo**: a feature nativa (`defer_loading`, regex vs BM25 vs embeddings custom, interação com prompt cache e com `mcp_toolset`, limites 10k, erros 400 comuns, lacuna do Agent SDK Python). O post existente não menciona `tool_reference` nem o fato de a expansão acontecer fora do prefixo cacheado.
- **Fontes**
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference (propriedades `defer_loading`, `allowed_callers`, `input_examples`, `eager_input_streaming`)
  - https://www.anthropic.com/engineering/advanced-tool-use
  - https://github.com/anthropics/claude-agent-sdk-python/issues/525 ; https://github.com/anthropics/claude-code/issues/31002

---

### 4. MCP Apps: a resposta do agente é uma UI (e ChatGPT adotou a mesma spec)

- **O que é**
  Primeira extensão oficial do MCP (26/01/2026). Uma tool declara `_meta.ui.resourceUri` apontando para um resource `ui://...` (HTML/JS autocontido). O host renderiza num iframe sandboxado e conversa com a UI via JSON-RPC sobre `postMessage`; a UI pode chamar tools do servidor (com aprovação explícita do usuário), receber `hostContext` (tema, CSS variables) e atualizar o estado da conversa. Servidor deve devolver conteúdo textual útil para hosts sem suporte (graceful degradation). SDK: `@modelcontextprotocol/ext-apps`. Capability negociada como `io.modelcontextprotocol/ui` com `mimeTypes: ["text/html;profile=mcp-app"]`.
- **Quem está usando/shipping**
  - Hosts com suporte completo: Claude (web/desktop), ChatGPT ("fully compatible with the MCP Apps spec" em 22/02/2026; host CSS variables 28/05; `_meta.ui.visibility` substitui `openai/visibility` em 21/07/2026), Goose, VS Code Insiders (26/01/2026), Airia. Planejado: JetBrains, Kiro (AWS), Antigravity (DeepMind).
  - OpenAI Apps SDK/ChatKit continuam existindo (ChatKit Python 1.6.5, 19/05/2026), mas o substrato de UI inline convergiu para MCP Apps.
- **Maturidade**: **mainstream** nos dois maiores hosts de consumo; **early adopters** em hosts próprios (você implementar o host no seu produto ainda exige trabalho).
- **Aplicação em agente de vendas / motor de resolução**
  - Agente de vendas expõe `comparar_planos` que renderiza tabela interativa + botão "contratar" que dispara `criar_pedido` com aprovação do usuário — dentro do Claude/ChatGPT, sem app próprio.
  - Motor de resolução devolve formulário de troca/devolução em vez de pedir 6 campos em texto.
  - Distribuição: seu MCP server vira "app" instalável nos dois ecossistemas com um único bundle de UI.
- **Gap vs blog**
  Adjacente a `tutoriais/renderizacao-que-converte-json-agente-card-clicavel` (renderização custom no **seu** frontend a partir de JSON) e `tutoriais/como-implementar-agent-builder-e-chatkit-da-openai-com-laravel` (ChatKit, pré-convergência). **Ângulo novo**: padrão aberto, cross-host (Claude + ChatGPT + VS Code), iframe sandbox, ciclo de vida UI↔tool, `hostContext`, e como empacotar o MCP server Laravel com `ext-apps`. Nenhum post menciona MCP Apps.
- **Fontes**
  - https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/ (26/01/2026)
  - https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx
  - https://code.visualstudio.com/blogs/2026/01/26/mcp-apps-support
  - https://developers.openai.com/plugins/changelog (22/02, 28/05, 21/07, 21/08/2026)
  - https://pypi.org/project/openai-chatkit/ (1.6.5, 19/05/2026)

---

### 5. Meta Business Agent e Business Agent Platform: a Meta virou plataforma (e concorrente) do agente de WhatsApp

- **O que é**
  Em 03/06/2026 (Conversations, Londres) a Meta lançou globalmente o **Meta Business Agent**: agente da própria Meta que responde clientes no WhatsApp, Messenger e Instagram — responde perguntas do negócio, recomenda produtos do catálogo, agenda, qualifica leads, fecha vendas e faz handoff para humano. Para enterprise, o **Meta Business Agent Platform** permite configurar agentes próprios conectados a sistemas externos (Shopify, Zendesk, Shopee citados) com guardrails e controles. Pricing: ativação gratuita agora; assinatura paga (WhatsApp Business Premium) para pequenos e **cobrança por tokens consumidos** para grandes (TechCrunch). Brasil não é citado nominalmente no comunicado, mas o lançamento é global após 2 anos de teste em Índia e México. Não há documentação pública (nos textos verificados) sobre BYO-LLM/BYO-agent via Cloud API — **roadmap/indefinido**.
- **Quem está usando/shipping**: Meta (about.fb.com, 03/06/2026); "mais de 1 milhão de negócios" já no agente (número da Meta). Ecossistema de BSPs (Omnichat, ChatMaxima etc.) publicando guias de reposicionamento.
- **Maturidade**: **mainstream** para PME (produto de consumo da Meta); **early adopters** para a Platform enterprise (poucos detalhes técnicos públicos).
- **Aplicação em agente de vendas / motor de resolução**
  - Decisão de arquitetura nova para quem constrói agente WhatsApp com Cloud API/Evolution API: (a) usar o agente da Meta e integrar via Platform, (b) manter agente próprio e competir em qualidade/integração, (c) híbrido — Meta faz FAQ/catálogo, seu agente assume via handoff quando exige ERP/CRM/negociação.
  - Pricing por token da Meta versus seu custo de tokens na API do modelo — entra na planilha TCO.
  - Risco: o canal passa a ter um agente "nativo" que chega antes do seu.
- **Gap vs blog**
  Adjacente a `tutoriais/como-criar-um-agente-de-ia-para-whatsapp`, `tutoriais/agente-bolao-copa-whatsapp-evolution-api-n8n`, `tutoriais/tutorial-como-integrar-o-laravel-com-twilio-para-enviar-e-receber-mensagens-no-whatsapp`. Nenhum trata do Meta Business Agent (posterior). **Ângulo novo**: "A Meta lançou o agente nativo do WhatsApp: o que muda para quem já tem agente próprio — build vs buy vs híbrido, handoff e pricing por token".
- **Fontes**
  - https://about.fb.com/news/2026/06/meta-business-agent/ (03/06/2026)
  - https://techcrunch.com/2026/06/03/metas-ai-agent-for-whatsapp-business-is-now-available-globally/ (03/06/2026)
  - https://whatsappbusiness.com/blog/introducing-meta-business-agent-ai/

---

### 6. Voz speech-to-speech com tool calling e reasoning (gpt-realtime-2.1, Gemini Live, ElevenLabs Agents)

- **O que é**
  Arquitetura de agente de voz em 2026 é single-model full-duplex (áudio entra e sai do mesmo modelo), com tool calling no meio da fala e três transportes: WebRTC (browser), WebSocket (servidor) e **SIP** (telefonia — rotear ligação direto para a sessão). Novidade de julho/2026: **gpt-realtime-2.1 e 2.1-mini** com *reasoning configurável* (minimal→xhigh) dentro do realtime, p95 de latência −25% via cache, suporte a imagem + MCP server como fonte de tools; áudio cacheado a $0,30/1M tokens vs $10 fresco no mini. Orçamento de latência citado em guias de produção: tool call adiciona 400–800 ms se a tool responde em <200 ms; acima disso o usuário sente silêncio — daí o padrão "modelo segue falando enquanto executa a tool". Gemini Live API ficou GA no Vertex com `gemini-live-2.5-flash-native-audio` (dez/2025) e tool use nativo. ElevenLabs lançou **ElevenLabs Agents** (06/03/2026) com MCP nativo, *MCP tool scoping* por nó de workflow, filas de concorrência (até 1.800 s) e integração Avaya (changelog 17/08/2026).
- **Quem está usando/shipping**: OpenAI (MarkTechPost 06/07/2026 sobre o anúncio; docs Realtime), Google (Vertex GA; Firebase App Check obrigatório desde jul/2026), ElevenLabs (changelog 2026), plataformas LiveKit/Pipecat/Vapi/Retell em produção.
- **Maturidade**: **mainstream** para speech-to-speech com tools; **early adopters** para reasoning dentro do realtime (2 meses de vida).
- **Aplicação em agente de vendas / motor de resolução**
  - Motor de resolução por telefone (SIP → gpt-realtime) consultando pedido via MCP do ERP; regra de ouro: tools < 200 ms ou fala de preenchimento ("estou vendo seu pedido…").
  - Escolha de modelo: "mid-tier com system prompt curto vence frontier" para voz — Sonnet/mini em vez de Opus/2.1 full na maioria dos fluxos.
  - ElevenLabs Agents como camada de telefonia/WhatsApp Voice quando não se quer manter WebRTC.
- **Gap vs blog**
  **Não existe nada de voz no acervo.** Gap limpo. Ângulo sugerido: "Agente de voz com tool calling: orçamento de latência, SIP vs WebRTC, e por que reasoning no realtime só vale em 10% dos turnos".
- **Fontes**
  - https://openai.com/index/introducing-gpt-realtime/ (modelo base, 2025)
  - https://www.marktechpost.com/2026/07/06/openai-gpt-realtime-2-1-mini-reasoning-realtime-api/ (06/07/2026 — secundária sobre anúncio OpenAI)
  - https://ai.google.dev/gemini-api/docs/live-api/tools ; https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api
  - https://elevenlabs.io/docs/changelog/2026/8/17 ; https://elevenlabs.io/docs/changelog/2026/4/1
  - https://www.latent.space/p/realtime-api (manual prático)

---

### 7. Protocolos de comércio agêntico: UCP (Google/Shopify) vs ACP (OpenAI/Stripe)

- **O que é**
  **UCP — Universal Commerce Protocol** (Google, 11/01/2026; versão `2026-01-11`): padrão aberto (ucp.dev, GitHub) em que o merchant publica um manifesto JSON em `/.well-known/ucp` com *capabilities* (product discovery, checkout, order management), *extensions* (descontos etc.) e *payment handlers* separados dos *payment instruments*; bindings de transporte **REST, MCP e A2A**; compatível com AP2 (pagamentos agênticos). Co-desenvolvido com Shopify, Etsy, Wayfair, Target, Walmart; endossado por Stripe, Adyen, Visa, Mastercard, PayPal e 20+. Usado no checkout do Google AI Mode/Gemini via Merchant Center. **ACP — Agentic Commerce Protocol** (OpenAI + Stripe, 29/09/2025) alimentava o ChatGPT Instant Checkout; em março/2026 a OpenAI recuou do Instant Checkout v1 para "descoberta + checkout controlado pelo merchant". Em maio/2026 a **Shopify shipou para todas as lojas, sem opt-in**: `/llms.txt`, `/llms-full.txt`, `/agents.md` (canônico), `/.well-known/ucp`, `/api/ucp/mcp` e um sitemap agêntico (changelog 28/05/2026).
- **Quem está usando/shipping**: Google, Shopify (todas as lojas), Etsy/Walmart/Target (co-autores), PayPal (comunicado 2026). Lado ACP: OpenAI/Stripe, com pivot em março/2026.
- **Maturidade**: UCP **early adopters → mainstream** (shipping em massa pela Shopify); ACP **em reposicionamento**. A afirmação de terceiros "lojas com UCP+ACP capturam 40% mais tráfego agêntico" é de vendor (ucphub.ai) — **não verificada**.
- **Aplicação em agente de vendas / motor de resolução**
  - O seu agente de vendas deixa de ser só "chat no site": o negócio precisa ser **descoberto e comprado por agentes de terceiros** (Gemini, ChatGPT). Expor `/.well-known/ucp` + binding MCP (`/api/ucp/mcp`) em Laravel é o equivalente 2026 de ter sitemap.
  - Order management via UCP cobre o motor de resolução pós-compra (status, troca) quando o cliente pergunta ao Gemini, não ao seu chat.
- **Gap vs blog**
  Sem nada no acervo sobre comércio agêntico/UCP/ACP. Adjacente apenas tematicamente a `tutoriais/arquitetura-agente-compara-ofertas-amazon-mercado-livre-magalu` (agente consumidor, não merchant). **Ângulo novo**: "Seu e-commerce Laravel como merchant UCP: `/.well-known/ucp`, capabilities de checkout e o binding MCP".
- **Fontes**
  - https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/ (11/01/2026)
  - https://weaverse.io/blogs/shopify-agents-md-llms-txt-theme-template-customization-may-28-2026 ; https://dev.to/no7software-uk/shopify-quietly-auto-shipped-llmstxt-agentsmd-and-well-knownucp-engineering-override-33cg (maio/2026 — secundárias sobre changelog Shopify 28/05/2026)
  - https://www.semrush.com/blog/universal-commerce-protocol/ ; https://www.paz.ai/blog/ucp-vs-acp-which-agentic-commerce-protocol-should-retailers-choose (secundárias)

---

### 8. A2A v1.0 e a consolidação dos protocolos agente-agente na AAIF (ACP e AGNTCY morreram)

- **O que é**
  A2A (Agent2Agent): JSON-RPC 2.0 sobre HTTPS (também gRPC/REST) para agentes descobrirem uns aos outros via **Agent Card** (JSON com capabilities, skills, auth), delegarem *tasks* com ciclo de vida, streaming SSE e push notifications. **v1.0** saiu em 2026 (fontes secundárias divergem: 12/03 vs 09/04) e formalizou **Agent Cards assinados** (JWS RFC 7515 + JCS RFC 8785) para verificação de domínio; 150+ organizações apoiadoras (AWS, Google, Microsoft, Salesforce, SAP, ServiceNow); SDKs em Python, Go, Java, JS, .NET e Rust. Em **17/08/2026 o A2A entrou na Agentic AI Foundation (AAIF)**, ficando sob o mesmo teto que MCP, goose e AGENTS.md. Concorrentes acabaram: **ACP (IBM/BeeAI) fundiu-se ao A2A em 29/08/2025** (repo arquivado; BeeAI roda A2A); **AGNTCY "Agent Connect Protocol" (Cisco) arquivado em 11/04/2026**. A2UI v0.9 já declara A2A 1.0 como transporte. A AAIF (fundada dez/2025; platinum: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI) organiza AGNTCon+MCPCon Europa (Amsterdã, 17–18/09/2026) e NA (San José, 22–23/10/2026).
- **Quem está usando/shipping**: Google ADK, Microsoft (Copilot Studio/Foundry), Salesforce Agentforce, SAP, ServiceNow (comitê técnico); UCP usa A2A como binding. Casos públicos ainda são de grandes vendors; pouco case de PME.
- **Maturidade**: **early adopters** (spec estável, governança neutra, mas valor real só aparece quando há agentes de *outra* organização para falar).
- **Aplicação em agente de vendas / motor de resolução**
  - Seu agente de vendas publica um Agent Card assinado em `/.well-known/agent-card.json` e aceita tasks de agentes compradores (Gemini, Agentforce do cliente B2B).
  - Motor de resolução delega "reembolso" ao agente do PSP via A2A em vez de integrar a API proprietária de cada gateway.
  - Para orquestração **interna** (seus próprios subagentes), A2A é overengineering — MCP + SDK basta; a fronteira organizacional é o critério.
- **Gap vs blog**
  Adjacente a `tutoriais/multi-agent-laravel-3-padroes-orchestrator-hierarchical-swarm`, `tutoriais/sistemas-multiagentes-orquestracao-assincrona`, `tutoriais/langgraph-mem0-langchain-mcp-do-que-voce-precisa` (todos multi-agent *interno*). Nenhum menciona A2A, Agent Cards ou AAIF. **Ângulo novo**: "MCP vs A2A em 2026: quando a fronteira é organizacional — Agent Card assinado em Laravel e por que ACP/AGNTCY não existem mais".
- **Fontes**
  - https://a2a-protocol.org/latest/ (spec v1.0, comitê técnico, SDKs)
  - https://www.forbes.com/sites/janakirammsv/2026/08/19/agent2agent-joins-the-agentic-ai-foundation-alongside-mcp/ (19/08/2026 — 403 no fetch; confirmado por a2a-protocol.org e linuxfoundation.org)
  - https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation (dez/2025)
  - https://www.linuxfoundation.org/press/agentic-ai-foundation-announces-global-2026-events-program-anchored-by-agntcon-mcpcon-north-america-and-europe (02/04/2026)
  - https://www.ml4devs.com/what-is/acp-agent-communication-protocol/ (fusão ACP→A2A, 29/08/2025) ; https://medium.com/@mertbasar30/acp-is-not-one-protocol-... (AGNTCY arquivado 11/04/2026 — secundária)
  - https://arxiv.org/pdf/2606.31498 (Governance Gaps in MCP/A2A/ACP, jun/2026)

---

### 9. Generative UI declarativa: A2UI v0.9 (Google) e AG-UI (runtime de eventos)

- **O que é**
  Dois protocolos complementares, frequentemente confundidos. **AG-UI** (CopilotKit, aberto) é o *runtime*: stream tipado de eventos entre backend agêntico e frontend (`RUN_STARTED`, `TEXT_MESSAGE_CONTENT`, `TOOL_CALL_ARGS`, `TOOL_CALL_RESULT`, `STATE_DELTA`, `RUN_FINISHED`, erros). **A2UI** (Google, open source desde jan/2026; **v0.9 em 03/07/2026**, v0.9.1 atual, v1.0 RC publicado) é a *camada declarativa*: o agente devolve JSON descrevendo UI em termos de um **catálogo de componentes do próprio app** ("fala a língua do design system existente", não inventa componentes); renderers oficiais React (novo), Flutter, Lit, Angular + web-core compartilhado; transporte por MCP, WebSockets, REST, AG-UI e A2A 1.0; Agent SDK Python com cache, catálogos dinâmicos e streaming resiliente a JSON parcial. Sem código arbitrário do LLM — diferença central frente a MCP Apps (que entrega HTML/JS em iframe).
- **Quem está usando/shipping**: Google (ADK, Gemini Enterprise), CopilotKit (AG-UI + renderer), Vercel AI SDK 6 (Agent abstraction + UI streaming tipado, data parts — concorrente pragmático no ecossistema React/Next). InfoQ registra ceticismo sobre confiar UI ao LLM e uniformidade visual.
- **Maturidade**: **early adopters** (A2UI <1.0; AG-UI estável, adoção concentrada em CopilotKit/ADK).
- **Aplicação em agente de vendas / motor de resolução**
  - Quando o agente roda **dentro do seu produto** (não no Claude/ChatGPT): A2UI deixa o LLM montar "card de proposta + seletor de parcelas" só com componentes aprovados do seu design system — sem risco de HTML arbitrário.
  - AG-UI resolve o streaming de estado (progresso de resolução de ticket, aprovação humana) entre backend Laravel e frontend.
  - Regra: MCP Apps para distribuir em hosts de terceiros; A2UI/AG-UI para UI no seu próprio app.
- **Gap vs blog**
  Adjacente a `tutoriais/renderizacao-que-converte-json-agente-card-clicavel` (exatamente a versão artesanal deste padrão). **Ângulo novo**: padronizar o JSON que o post existente inventa — catálogo de componentes, renderer, fallback para JSON parcial em streaming, e o par AG-UI (runtime) × A2UI (declarativo) × MCP Apps (iframe).
- **Fontes**
  - https://www.infoq.com/news/2026/07/google-a2ui-genui/ (jul/2026)
  - https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/
  - https://atamel.dev/posts/2026/03-30_a2ui_with_adk/ (30/03/2026)
  - https://docs.ag-ui.com/concepts/generative-ui-specs
  - https://vercel.com/blog/ai-sdk-6 ; https://www.copilotkit.ai/blog/the-developer-s-guide-to-generative-ui-in-2026

---

### 10. Agente como colega de canal: o padrão Claude Tag (identidade compartilhada, memória de canal, modo ambient)

- **O que é**
  Lançado em 23/06/2026 (beta pública, Claude Team/Enterprise, Opus 4.8). Diferença de design frente ao "bot por usuário": **um** Claude por canal, visível a todos, com identidade própria, **memória do canal** (não precisa ser re-briefado), divisão de tarefas em etapas executadas em thread, **agendamento de tarefas para si mesmo**, e **modo ambient** opcional (age sem ser marcado: sinaliza threads paradas, traz updates). Admin define ferramentas/dados por canal, criando "identidades Claude separadas" com escopo. Substitui o Claude in Slack antigo (retirado em 03/08/2026; migração em 30 dias). Anthropic diz que 65% do código do seu time de produto passa pela versão interna. Roadmap: "expandir para outras plataformas" — **sem data, sem Teams confirmado**.
- **Quem está usando/shipping**: Anthropic (anthropic.com/news, 23/06/2026); cobertura TechCrunch, Fortune, VentureBeat (update de leitura completa da conversa + intervenção não solicitada).
- **Maturidade**: **early adopters** (beta, só planos Team/Enterprise).
- **Aplicação em agente de vendas / motor de resolução**
  - Motor de resolução interno: canal `#suporte-n2` com um agente compartilhado que tem memória dos incidentes do canal, abre tickets, e em modo ambient avisa "esse chamado está há 4h sem resposta".
  - Agente de vendas no canal `#deals`: lê o contexto do canal, atualiza CRM, agenda follow-up para si mesmo.
  - Para quem constrói o próprio bot (Slack/Teams/Discord): o padrão replicável é *identidade única por canal + memória escopada por canal + scheduler + gatilhos ambient com rate limit*.
- **Gap vs blog**
  **Adjacente direto** a `tutoriais/criar-bot-no-slack-com-claude` (bot request/response por usuário). **Ângulo novo**: o salto de "bot" para "colega" — multiplayer, memória de canal, ambient mode, tarefas agendadas, permissões por canal — e como reproduzir esses 4 mecanismos no seu bot Laravel. Também cabe news: fim do Claude in Slack antigo em 03/08/2026.
- **Fontes**
  - https://www.anthropic.com/news/introducing-claude-tag (23/06/2026)
  - https://techcrunch.com/2026/06/23/anthropics-claude-tag-is-learning-your-company-one-slack-message-at-a-time/
  - https://venturebeat.com/orchestration/anthropics-new-claude-tag-update-lets-its-slack-agent-read-the-full-conversation-and-jump-in-unprompted
  - https://fortune.com/2026/06/23/anthropic-claude-tag-virtual-employee-tool-slack/

---

### 11. Discovery para agentes: AGENTS.md, llms.txt, `/.well-known/*` e o MCP Registry (o "agent-ready backend")

- **O que é**
  Camada de arquivos/endpoints que um site, API ou repositório publica para ser entendido por agentes sem scraping: **AGENTS.md** (Markdown livre, "README para agentes"; 60k+ repositórios; governado pela AAIF; suportado por Codex, Jules, Cursor, Copilot, Gemini CLI, Devin etc.), **llms.txt / llms-full.txt** (Jeremy Howard, 2024; 844k+ sites incluindo Stripe, Cloudflare, Vercel, Anthropic — mas **nenhuma plataforma de IA confirmou que lê**; estudos mostram 8 de 9 sites sem mudança de tráfego), **`/.well-known/ucp`** e **`/.well-known/agent-card.json`** (A2A), e o **MCP Registry oficial** (registry.modelcontextprotocol.io, preview desde 08/09/2025, ~2.000 servidores, ainda **preview em jul/2026**, desenhado para ser consumido por sub-registries, não por usuário final). A virada de 2026: Shopify tornou `/agents.md` o arquivo canônico de discovery de **loja** (não só de repo), com `/llms.txt` redirecionando para ele — sinal de que AGENTS.md está saindo do repositório e indo para o produto. Na prática de API: OpenAPI→MCP automático (AutoMCP, Speakeasy Gram) funciona, mas o paper arXiv 2605.14312 (mai/2026) mostra falhas sistemáticas de planejamento/seleção/payload quando a spec tem "smells" (descrições vagas, erros opacos, paginação implícita) — a qualidade da descrição continua sendo o gargalo.
- **Quem está usando/shipping**: AAIF/OpenAI (AGENTS.md), Shopify (maio/2026), Anthropic/Cloudflare/Vercel (llms.txt), Speakeasy Gram (MCP cloud + Gram Functions), Stripe Agent Toolkit.
- **Maturidade**: AGENTS.md **mainstream em repos**, **experimental em produto**; llms.txt **mainstream em adoção, não comprovado em efeito**; MCP Registry **preview**.
- **Aplicação em agente de vendas / motor de resolução**
  - Backend Laravel "agent-ready": `/agents.md` descrevendo capabilities, `/.well-known/ucp` para comércio, Agent Card para A2A, servidor MCP publicado no registry (namespace verificado) — é assim que o agente do **cliente** encontra o seu negócio.
  - Design de API para LLM: erros com `code` + `next_action` legível, paginação explícita com `cursor`, descrições com verbos do domínio — diretamente derivado dos "smells" do paper.
- **Gap vs blog**
  Adjacente a `tutoriais/claude-md-clausulas-karpathy` (CLAUDE.md/AGENTS.md **para repo**) e a `tutoriais/tool-use-na-pratica-desenhando-ferramentas-llm` (descrição de tools). Nenhum post trata de discovery **de site/produto/API** para agentes externos, nem do MCP Registry, nem da evidência fraca do llms.txt. **Ângulo novo**: "O que seu site/API publica para agentes em 2026: AGENTS.md fora do repo, llms.txt (vale?), .well-known e registry — com ceticismo e dados".
- **Fontes**
  - https://agents.md/ ; https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
  - https://caseyrb.com/blog/state-of-llms-txt-adoption/ (medição em milhões de sites)
  - https://weaverse.io/blogs/shopify-agents-md-llms-txt-theme-template-customization-may-28-2026 (28/05/2026)
  - https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/ ; https://registry.modelcontextprotocol.io/ ; https://digitalthoughtdisruption.com/2026/07/20/mcp-registry-discover-verify-safely-connect-servers/ (status preview em 20/07/2026)
  - https://arxiv.org/abs/2605.14312 (Making OpenAPI Documentation Agent-Ready, mai/2026) ; https://arxiv.org/html/2507.16044v2 (AutoMCP)
  - https://www.speakeasy.com/blog/release-gram-functions ; https://docs.stripe.com/agents

---

### 12. WebMCP (`navigator.modelContext` → `document.modelContext`): o site expõe tools ao agente do navegador

- **O que é**
  Padrão W3C Web Machine Learning CG co-autorado por Google e Microsoft. O site registra ferramentas para agentes que rodam **no browser do usuário**: declarativo (atributos `toolname`, `tooldescription`, `toolparamdescription` em `<form>`, schema gerado do formulário) ou imperativo (`modelContext.registerTool({name, description, inputSchema, execute})`). Tools executam client-side na sessão já autenticada do usuário, com o browser mediando permissões. Shipou como **early preview no Chrome 146 (fev/2026), só em Canary atrás da flag `#enable-webmcp-testing`**; spec volátil (`provideContext`/`clearContext` removidos em mar/2026; getter migrou para `document.modelContext`, Chrome 150 mantém alias). Sem discovery pré-visita (`.well-known/webmcp` em discussão). Benchmarks de terceiros falam em 8–12× mais rápido que agente visual na mesma página — **não verificado independentemente**.
- **Quem está usando/shipping**: Google Chrome (Canary), Microsoft (co-autor; Edge esperado). Firefox/Safari engajados na spec, sem compromisso. Nenhum case de produção encontrado.
- **Maturidade**: **experimental**. Vale acompanhar, não vale apostar o roadmap de 2026.
- **Aplicação em agente de vendas / motor de resolução**
  - Versão futura do "agent-ready": seu checkout/área do cliente expõe `aplicar_cupom`, `rastrear_pedido` como WebMCP tools — o agente do browser (Claude in Chrome, Gemini no Chrome) usa em vez de clicar. Complementa `/.well-known/ucp` (server-side) com tools client-side na sessão do usuário.
  - Risco explícito de prompt injection e de tool registrada por script de terceiro na página — mesma superfície do browser_toolset, do outro lado.
- **Gap vs blog**: inexistente no acervo. Ângulo: explicador cético ("o que é, como testar no Canary, por que ainda não") — cabe como news/tutorial curto.
- **Fontes**
  - https://www.datacamp.com/tutorial/webmcp-tutorial
  - https://dev.to/ai-agent-economy/webmcp-in-2026-which-browsers-support-navigatormodelcontext-complete-compatibility-status-1oe4
  - https://www.openhermit.com/blog/navigator-modelcontext-2026 ; https://nohacks.co/blog/what-is-webmcp (secundárias)

---

## Temas pesquisados que NÃO entraram como técnica (e por quê)

- **E-mail agents (agente que lê e responde e-mail)**: não achei produto/protocolo novo de 2026 digno de "técnica"; o que há é guidance de segurança (Five Eyes/CISA maio/2026; OWASP jun/2026: prompt injection ainda é a maior causa de falha em agentes em produção; "lethal trifecta" = dado privado + input não confiável + vetor de exfiltração). O blog já tem `noticias/prompt-injection-o-que-e-ataques-2026` e `tutoriais/prompt-injection-agente-site-raspado-system-prompt`. Se virar post, o ângulo é "inbox agent = trifecta completa: arquitetura de quarentena (ler ≠ agir), sem exfiltração via link/imagem, aprovação para enviar". Fontes: https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/ ; https://airia.com/blog/ai-security-in-2026-prompt-injection-the-lethal-trifecta-and-how-to-defend/
- **RCS Business Messaging**: maduro, mas sem novidade 2026 relevante de protocolo; continua sendo RBM + Dialogflow/LLM; reach cross-platform desde iOS 18 (2024). Sem fonte primária de 2026 digna de nota.
- **Marketplaces/"app stores" de agentes**: paisagem fragmentada (GPT Store, Claude Skills/directory, MCP hubs, AWS/GCP Marketplace, Agentforce) e fontes majoritariamente de vendors; o que é verificável está coberto em #4 (ChatGPT App Directory via MCP Apps) e #11 (MCP Registry). Não há um padrão técnico novo além de registry + Agent Card.
- **Anthropic Managed Agents (sandboxes self-hosted, MCP tunnels)**: relevante, mas é eixo de infra/deploy; mencionado em #1 como vetor de interop (MCP privado acessado por agente hospedado).

---

## Ranking do eixo (relevância p/ quem constrói agente em produção × frescor × ausência no blog)

| # | Técnica | Frescor | Maturidade | Gap no blog | Justificativa curta |
|---|---------|---------|------------|-------------|---------------------|
| 1 | **MCP 2026-07-28 (stateless, MRTR, extensões, deprecações)** | jul–ago/2026 | mainstream (migração forçada) | adjacente, 4 posts desatualizados | Todo servidor MCP do acervo precisa migrar; MRTR resolve dor real (confirmar dado antes de agir); 12 meses de janela começaram agora |
| 2 | **Browser use toolset GA + DOM-first** | ago/2026 | early→mainstream | sem post sobre browser como atuador | Resolve "não tem API" com toolset nativo e segurança opinativa; decisão API>MCP>DOM>visão é conteúdo de arquitetura |
| 3 | **Tool search / defer_loading / toolsets** | GA 2026, docs atualizadas ago/2026 | mainstream | adjacente forte (progressive disclosure manual) | O post existente ensina o princípio; falta a feature nativa, cache, embeddings custom e lacuna do Agent SDK |
| 4 | **MCP Apps + compat ChatGPT** | jan–ago/2026 | mainstream nos hosts | adjacente (card clicável custom) | "Resposta = UI" virou padrão cross-host; distribuição Claude+ChatGPT com um bundle |
| 5 | **Meta Business Agent / Platform** | jun/2026 | mainstream PME | 3 posts de WhatsApp pré-Meta-agent | Muda a decisão build/buy de todo agente WhatsApp; pricing por token |
| 6 | **Voz speech-to-speech + tools + reasoning (gpt-realtime-2.1, Live, ElevenLabs)** | jul–ago/2026 | mainstream | zero no acervo | Gap limpo; motor de resolução por telefone é caso concreto |
| 7 | **UCP vs ACP (comércio agêntico) + Shopify auto-ship** | jan + mai/2026 | early→mainstream | zero no acervo | Agente de vendas precisa ser *vendível por outros agentes*; Laravel como merchant UCP |
| 8 | **A2A v1.0 + AAIF (ACP/AGNTCY mortos)** | ago/2026 | early adopters | adjacente (multi-agent interno) | Fronteira organizacional como critério MCP vs A2A; Agent Card assinado |
| 9 | **A2UI v0.9 + AG-UI** | jul/2026 | early adopters | adjacente (card clicável) | Padroniza o JSON→UI do post existente; ceticismo documentado |
| 10 | **Padrão Claude Tag (agente-colega)** | jun/2026 | early adopters (beta) | adjacente direto (bot Slack) | 4 mecanismos replicáveis; news do fim do Claude in Slack antigo |
| 11 | **Discovery: AGENTS.md fora do repo, llms.txt, .well-known, MCP Registry** | mai/2026 | misto | adjacente (CLAUDE.md p/ repo) | Bom post cético com dados; registry ainda preview |
| 12 | **WebMCP** | fev–mar/2026 | experimental | zero | Só Canary atrás de flag; explicador curto, não tutorial de produção |
