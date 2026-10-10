# Dossiê: técnicas de construção de agentes (2026) que o blog ainda não cobre

**Para:** Lucas / Beer & Code
**Data:** 12/09/2026
**Pergunta:** quais técnicas recentes de construção de agentes de IA como solução em sistemas (agente de vendas, motor de resolução, agente operacional) ainda não têm conteúdo no blog?

**Método.** Acervo completo lido antes da pesquisa: 281 posts no sitemap (153 notícias, 123 tutoriais, 5 pacotes) mais a pauta de setembro e os 9 capítulos da aula de Arquitetura de Soluções de IA. Seis pesquisadores em paralelo, um por eixo, com ~130 buscas e ~150 fetches em fontes primárias (docs oficiais, blogs de engenharia, specs, arXiv). Cada técnica foi confrontada com os slugs existentes; o que já estava coberto saiu, o que era adjacente ganhou o ângulo novo explícito.

**Regra de uso.** Toda afirmação factual tem data e fonte nos relatórios detalhados em [`pesquisa-tecnicas-agentes-2026/`](pesquisa-tecnicas-agentes-2026/). O que é preview/paper/rumor está marcado. Taxas de resolução de vendors (Sierra "90%", Intercom "76%") são marketing e não devem virar fato no post.

---

## 1. Resumo executivo

1. **O acervo cobre bem o "como montar o agente"** (tool calling, RAG, memória, harness, evals, guardrails, MCP, multi-agent, custo). O que falta é quase todo o **"como operar o agente como sistema"**: autorização fora do modelo, execução durável/transacional, identidade do agente, procedimento executável, simulação honesta, memória governada, protocolos de comércio e modalidades (voz, browser).
2. **Convergência de indústria em 2026:** a decisão "pode executar esta ação com estes argumentos?" saiu do prompt e foi para um motor de política determinístico entre o agente e a tool (AWS AgentCore Policy GA 03/03, Salesforce Agent Script GA jun, Cloudflare WriteGuard ago, Anthropic permission `auto` 10/09). Nenhum post do blog trata autorização como camada separada de guardrail.
3. **Ação com efeito colateral virou transação distribuída:** durable execution (Temporal×OpenAI Agents SDK GA 23/03), interrupt/resume serializável, idempotency key antes da primeira escrita, ledger de estados, compensação. O blog tem "guardar estado entre execuções"; não tem replay, alçada nem saga.
4. **SOP virou artefato executável:** Decagon AOP, Intercom Fin Procedures (cobradas como outcome desde 12/03), Sierra Journeys e Anthropic SKILL.md (padrão aberto, `/v1/skills`) convergiram em "linguagem natural para o flexível, código para o rígido". O blog fala de skills só no contexto de Claude Code.
5. **Simulação e eval ganharam ceticismo científico:** três papers de 2026 mostram que o cliente simulado "nunca vai embora" (resistência cai 46%), varia 9 p.p. conforme o LLM simulador e é manipulável. Verificadores de política como sub-agente (PolicyGuide, 20/08) sobem Pass^4 de 0,42 para 0,62 no τ²-bench. Os 5 posts de eval do blog não questionam o simulador nem usam pass^k.
6. **Memória virou superfície de ataque e de compliance:** memory poisoning é OWASP ASI06; memória convergiu para filesystem versionado com `redact` (Anthropic, OpenAI, Letta); consolidação offline (Dreams, research preview) separa escrever de curar; LGPD exige eliminação inclusive de memória derivada. Os 4 posts de memória do blog tratam só de gravar e ler.
7. **Agente precisa de identidade própria:** Auth0 On-Behalf-Of GA (21/05), Okta Agent SSO GA (24/08), Google Agent Identity via SPIFFE; MCP 2026-07-28 proíbe passthrough de token. O blog só tem "MCP com OAuth".
8. **Comércio agêntico chegou ao lado do merchant:** UCP (Google/Shopify) e ACP (OpenAI/Stripe) definem como um agente de terceiro compra de você; Shopify auto-shipou `/.well-known/ucp` em todas as lojas (28/05). A lição do pivot da OpenAI (fim do Instant Checkout em mar/2026): discovery converte, checkout em-chat não. Zero no acervo.
9. **O canal ganhou agente nativo:** Meta Business Agent global (03/06, cobrança por token desde 01/08) muda build vs buy dos 3 posts de WhatsApp. Voz speech-to-speech com SIP e MCP (gpt-realtime-2, 07/05) não aparece em nenhum post.
10. **Seis posts existentes precisam de refresh por fato novo** (ver seção 5): Agent Builder descontinuado, spec MCP de julho, fine-tuning self-serve da OpenAI desligando, Digital Omnibus, Meta Business Agent, fim do Claude in Slack antigo.

---

## 2. Ranking consolidado

Critério: relevância para quem constrói agente em produção × frescor (peso em mar–set/2026) × ausência no blog × encaixe com o público (Laravel/PHP + Claude, pt-BR). Técnicas que apareceram em mais de um eixo foram fundidas. A coluna "eixo" aponta o relatório detalhado e o número da técnica lá.

| # | Tema (como post) | Maturidade | Frescor | Gap | Eixos |
|---|---|---|---|---|---|
| 1 | Alçada fora do prompt: teto de desconto e reembolso como política determinística (Cedar, `available when`, risk tiers, permission `auto`) | GA em 4 vendors | 10/09 | limpo | 01#8, 02#5, 05#7, 03#6 |
| 2 | Tool que move dinheiro é transação: durable execution, interrupt/resume, idempotency key, ledger, compensação | GA (Temporal) / padrão | mar–set | limpo | 01#1, 03#5, 03#10, 05#8 |
| 3 | SOP vira SKILL.md: procedimento executável híbrido (AOP, Fin Procedures, Journeys, Skills via API) | mainstream vendors | mar | limpo | 03#1, 01#7 |
| 4 | A descrição da tool é seu system prompt invisível: tool poisoning, rug pull e o incidente Copilot Studio | ameaça mainstream | 30/06 | limpo | 05#9 |
| 5 | Seu servidor MCP de 2025 quebra na spec 2026-07-28: stateless, MRTR, Tasks, RFC 9728/8707/9207 | spec final | 28/07 | 4 posts desatualizados | 05#5, 06#1, 01#10 |
| 6 | O cliente simulado nunca vai embora: simulador como componente sob teste + τ² próprio com pass^k | papers + prática | jun–ago | adjacente (evals) | 02#6, 03#7, 05#1 |
| 7 | Verificador de política como sub-agente: omissão procedimental, não só ação proibida (PolicyGuard/PolicyGuide) | paper com números | 20/08 | adjacente (guardrails) | 03#3 |
| 8 | Quem pode escrever na memória do seu agente: memory poisoning (ASI06), stores read-only, origin-bound, TTL | ameaça mainstream / defesa early | 03/09 | adjacente (injection) | 04#9, 05#10 |
| 9 | Memória como filesystem versionado, não como vetor: Memory Stores, `redact`, LGPD e memória derivada | beta pública + SDK PHP | 23/04 | adjacente (pgvector) | 04#4, 04#10, 03#12 |
| 10 | Dreams: consolidação offline de memória como job separado (e como fazer com pgvector + Horizon) | research preview | mai | limpo | 04#1, 01#12 |
| 11 | Seu agente precisa de CPF: agente como principal, OBO token exchange (RFC 8693), Token Vault, kill switch | GA Okta/Auth0/Google | 24/08 | limpo | 05#4 |
| 12 | A Meta lançou o agente nativo do WhatsApp: build vs buy vs híbrido, handoff e cobrança por token | mainstream PME | 03/06, 01/08 | 3 posts pré-Meta | 02#9, 06#5 |
| 13 | Seu e-commerce como merchant UCP/ACP: `/.well-known/ucp`, checkout MCP, Web Bot Auth, e por que o checkout em-chat falhou | early→mainstream | jan–mai | limpo | 02#1, 06#7, 02#2, 02#4 |
| 14 | Agente de voz com tool calling: S2S, SIP, MCP, orçamento de latência e Voice Sims | mainstream inbound | 07/05, jul | limpo | 03#11, 06#6 |
| 15 | Agent gateway: identidade e custo por agente, A2A governado (Kong 2.0 GA, agentgateway, Sierra) | GA 01/09 | 01/09 | adjacente (MCP gateway) | 01#6, 06#8 |
| 16 | Agente acordado por evento, não por chat: webhook/CDC/fila, notify-question-review, agent inbox, outbound | early adopters | jun | adjacente (cron) | 01#9, 06#10 |
| 17 | GEPA no juiz, não no agente: Decagon e Nubank (KDD'26) com 20–100 exemplos | produção em escala | 25/03, 07/06 | adjacente (evals) | 04#3 |
| 18 | "Resolução" como máquina de estados com reversão: Intercom vs Zendesk, 5 métricas anti-deflection, outcome pricing e holdout | mainstream pricing | 12/03, 19/05 | limpo | 03#4, 02#11 |
| 19 | Arquitetura de SDR agent 2026: sinais, waterfall de enriquecimento, máquina de estados do lead, handoff com contexto | mainstream | abr | limpo | 02#10 |
| 20 | Browser agent DOM-first com `browser_toolset_20260801`: quando usar em vez de API, o que deixar desligado | GA | 01/08, 26/08 | limpo | 06#2 |
| 21 | Zonas de confiança: sessão append-only, harness stateless, sandbox microVM, credential proxy, CaMeL pragmático | beta / convergência | abr–ago | adjacente (harness) | 01#2, 01#4, 01#5, 05#11 |
| 22 | Tool search nativo (`defer_loading`, regex/BM25/embeddings) e a lacuna do Agent SDK | GA | ago | adjacente forte (progressive disclosure) | 06#3 |
| 23 | Resposta é interface: MCP Apps (Claude + ChatGPT), A2UI v0.9, AG-UI | mainstream hosts | jan–jul | adjacente (card clicável) | 06#4, 06#9 |
| 24 | Trace como evidência: OTel GenAI semconv, agent SLOs, Art. 12 do AI Act e OWASP Agent Control Standard | development / publicado 01/09 | 01/09 | adjacente (observabilidade, compliance) | 05#6, 05#13 |
| 25 | Agente que aprende piora no básico: playbooks evolutivos (ACE/ReasoningBank), skills destiladas, erosão de 41,8% | papers ICLR 2026 | abr–jul | adjacente (improvement loop) | 04#2, 04#5, 04#12 |
| 26 | OpenAI desligou o fine-tuning self-serve: Agent RFT, REPO (A/B com 9.653 conversas) e o critério "reward verificável" | news com datas | 07/05, 02/07 | 4 posts de FT a rever | 04#7, 02#7 |
| 27 | Circuit breaker de tokens e speculative tool calling | prática / paper | mai–jul | adjacente (6 posts de custo) | 05#12, 04#6 |
| 28 | Harness × Runtime: as 8 responsabilidades que não cabem no harness | mainstream vocabulário | abr–ago | adjacente (5 posts de harness) | 01#3 |
| 29 | Por que os números de memória mentem: Zep vs Mem0, 32% vs 93%, e como montar seu LongMemEval | disputa pública | mai | limpo | 04#8 |
| 30 | Vendedor defensivo: negociação agente-a-agente, vendedores LLM são acomodativos | papers | mai–jul | limpo | 02#8 |
| 31 | Red-teaming autônomo: OpenAI comprou a Promptfoo, plugin MCP, mapeamento OWASP ASI | mainstream enterprise | 09/03 | adjacente (evals adversariais) | 05#3 |
| 32 | O que seu site publica para agentes: AGENTS.md fora do repo, llms.txt (vale?), `.well-known`, MCP Registry | misto | mai | adjacente (CLAUDE.md) | 06#11 |
| 33 | Rollout em 4 estágios e por que não dá pra shadow uma ação | prática | 2026 | adjacente (níveis de autonomia) | 03#9 |
| 34 | Trace de produção vira teste: asserções de tool-call, volume/risk set, snapshot com pin de modelo | early | jul–ago | adjacente (pipeline de eval) | 05#2, 03#8 |
| 35 | Agente que constrói agente: Ghostwriter, Duet e o Hyper-τ-bench (23,9% sozinho vs 82,2% com humano) | early | 08/09 | limpo | 03#2 |
| 36 | Memória bi-temporal em Postgres antes de comprar grafo | early→mainstream | 2025–26 | adjacente (graph é hype) | 04#11 |
| 37 | Mandatos assinados e compra sem humano: AP2 v0.2, Agent Pay for Machines, MPP/x402 | v0.x / anúncio | abr–jun | limpo, baixo | 02#3 |
| 38 | WebMCP: o site expõe tools ao agente do navegador (só Canary) | experimental | fev–mar | limpo, baixo | 06#12 |

---

## 3. Os clusters (o que cada um é e por que importa)

### 3.1 Controle de ação: autorização, transação e procedimento (temas 1, 2, 3, 7, 15, 21)

É o maior gap e o mais coerente com o evento de 19/09. A aula já ensina guardrail de entrada e saída; a indústria em 2026 adicionou **três camadas entre o LLM e o sistema de registro** que o blog não descreve:

- **Autorização por política (tema 1).** O limite "até 15% de desconto sem aprovação" deixa de ser instrução no prompt e vira política avaliada por código antes da tool rodar. AWS AgentCore Policy traduz linguagem natural para Cedar e aplica no gateway (GA 03/03/2026). Salesforce Agent Script gateia quais tools o modelo enxerga com `available when`, testável sem LLM (GA jun/2026, parser open source). Cloudflare WriteGuard classifica tools em risk tiers (beta 05/08). Anthropic Managed Agents ganhou `permission_policy: auto` em ~10/09: o servidor classifica cada chamada em run/deny/pause e grava `evaluated_permission` + `reason_code` para auditoria. Armadilha documentada: só `user.message` conta como intenção, então repassar input do cliente final nesse campo pode liberar uma chamada. Dado de fatiga: 93% de aprovação automática em prompts de permissão; revisar 1–2 ações por vez é o ótimo (paper 25/08).
- **Execução durável e transacional (tema 2).** Loop do agente dentro de um workflow durável (Temporal, Restate, Inngest, Vercel Workflow): cada tool call é activity com resultado no histórico; crash não duplica reembolso; espera de 48h não custa compute; replay de histórico real para testar prompt novo. Temporal tem SDK PHP oficial e nenhum post em pt-BR. Complemento: interrupt/resume como estado serializável (OpenAI `RunState`, LangGraph `Command(resume)`, Managed Agents `user.tool_confirmation`), e o kit de pagamento aplicado a tool call: idempotency key gerada antes da primeira escrita, ledger PLANNED→COMMITTED com OUTCOME_UNKNOWN, compensação como ação de domínio. Blueprint Commerce Agents da Anthropic (02/09/2026) como âncora.
- **Procedimento executável (tema 3).** Política de atendimento como artefato versionado: passos em linguagem natural + if/else + código para regra dura + conectores escopados. Decagon AOP, Intercom Fin Procedures, Sierra Journeys, Anthropic SKILL.md (40+ adotantes, `/v1/skills`, Managed Agents com `version` pinável). Post natural: "SKILL.md como SOP de atendimento via API, não via Claude Code", com checklist SOP→procedimento em 5 passos e o padrão Stripe Minions (nó determinístico obrigatório + nó agêntico de escopo fechado + orçamento de 2 tentativas).
- **Verificador de política (tema 7).** Guardrail por argumento não pega omissão de passo (pulou verificação de identidade). PolicyGuide (20/08/2026) compila a política num grafo e verifica a cada turno: Pass^4 médio 0,42→0,62 no τ²-bench. Encaixa como middleware antes do dispatch no harness Laravel.

### 3.2 Confiar no número: simulação, eval e rollout (temas 6, 17, 18, 33, 34, 35)

O blog tem 5 posts de eval, todos single-turn ou sobre o juiz. Falta:

- **Simulador como componente sob teste (tema 6).** Em 2.790 conversas reais de vendas, simuladores LLM puxam não-compradores para o frame de compra: resistência 25,1%→13,5%, deliberação 21,9%→40,1% (16/06/2026). Variância de 9 p.p. conforme o LLM simulador; viés dialetal (28/01). CustomerSim/UserGRPO sobe aderência à persona de 0,417 para 0,652. Ângulo: calibrar o simulador contra conversões reais antes de confiar no eval; montar um τ²-bench próprio (política + tools mockadas + 50–200 tarefas + pass^5 como gate), como a Anthropic recomendou em 09/01/2026.
- **GEPA no juiz (tema 17).** Decagon (25/03) e Nubank (KDD'26, 07/06) usaram otimização reflexiva de prompt no juiz, não no agente: eval 68,9%→88,9%, κ 0→0,745; ótimo com 20–100 exemplos, 500 piora. Caso brasileiro em fonte primária.
- **Resolução como máquina de estados (tema 18).** Intercom: confirmed vs assumed, dedução por recontato; Zendesk: 72h + avaliação por IA. Kit de 5 métricas anti-deflection (recontato em 7d, ações incorretas, precisão/recall de escalação). Do lado de vendas: eventos de outcome idempotentes + holdout para atribuição; sem holdout não há número defensável.
- **Rollout e replay (temas 33, 34).** Shadow testa resposta, não ação: "ou o dinheiro sai ou não sai". Conversa anotada vira teste de regressão com mock de API; snapshot imutável inclui versão do modelo (Sierra ADLC).

### 3.3 Memória governada (temas 8, 9, 10, 25, 29, 36)

- **Poisoning (tema 8).** OWASP ASI06; MPBench (03/06) e Calgary (03/09, 2.614 trajetórias): slow drift e backdoor escapam de eval por turno. A Anthropic avisa nas docs que store `read_write` + input não confiável é risco. Defesas: store de política `read_only`, write gate estruturado, TTL em memória derivada de fonte externa, origem verificada no momento da escrita (TMA-NM, 0% de sucesso em 8 modelos).
- **Filesystem versionado (tema 9).** Anthropic Memory Stores (beta 23/04: `/mnt/memory/<slug>/`, `memver_…`, `redact`, `content_sha256`), Claude Code auto memory, Letta MemFS em git, OpenAI `MEMORY.md`. Vetor virou índice sobre isso, não a memória. SDK PHP oficial já cobre. LGPD: eliminação (art. 18 VI) inclusive da memória derivada por consolidação.
- **Dreams (tema 10).** Job assíncrono lê store + 1–100 sessões e produz store novo (input imutável). Como reproduzir com pgvector + job noturno + revisão antes de promover.
- **Erosão (tema 25).** Agente que evolui playbook/skills cai para 41,8% de retenção em tarefas simples; exige suíte de regressão básica como gate de promoção.

### 3.4 Identidade e protocolo (temas 4, 5, 11, 15, 22, 23, 24, 32)

- **Tool poisoning (tema 4).** Microsoft observou em produção (30/06/2026) descrições de tools em servidores MCP de terceiros alteradas para exfiltrar resumos de faturas via Copilot Studio. Checklist: hash/pin das descrições aprovadas, re-aprovação em mudança, allowlist de egress, HITL em tools de escrita.
- **MCP 2026-07-28 (tema 5).** Core stateless (sem `initialize`/sessão), MRTR substitui elicitation server-initiated, Tasks vira extensão, `ttlMs`/`cacheScope`, RFC 9728/8707/9207 obrigatórios, passthrough de token proibido, Sampling/Roots/DCR deprecados em 12 meses. GitHub MCP já suporta. Os 4 posts de MCP do blog presumem sessão e handshake.
- **Agente como principal (tema 11).** Token com `sub` = usuário e `act` = agente, audience por serviço, escopo por tool, Token Vault para o OAuth do Pipedrive, kill switch que revoga o agente sem tocar no usuário. Middleware Laravel valida `act` e `aud` antes de cada handler.
- **Trace como evidência (tema 24).** OTel GenAI: spans `invoke_agent`/`execute_tool`, evento `gen_ai.evaluation.result` (tudo ainda `Status: Development`). Digital Omnibus adiou Anexo III para 02/12/2027 mas Art. 12 segue exigindo log automático; OWASP Agent Control Standard publicado em 01/09/2026.

### 3.5 Vendas e comércio (temas 12, 13, 19, 30, 37)

- **Meta Business Agent (tema 12).** Agente nativo global desde 03/06, cobrança por token desde 01/08, Business Agent Platform para enterprise. Pix no chat só em fontes secundárias BR. Arquitetura híbrida: Meta atende tier 1, webhook de lead qualificado dispara seu agente Laravel com carrinho e pagamento.
- **Lado merchant (tema 13).** UCP: manifesto em `/.well-known/ucp`, capability negotiation, máquina de estados `requires_escalation`; Shopify expõe Catalog/Cart/Checkout como MCP. ACP sobreviveu como discovery após o fim do Instant Checkout (Walmart: conversão ~3x pior em-chat). Stripe Shared Payment Tokens com `max_amount` como guardrail de última linha, mas sem Brasil. Web Bot Auth (RFC 9421) para o seu site autenticar o agente que chega; Ninth Circuit reverteu a injunção Amazon v. Perplexity em 04/08.
- **SDR agent (tema 19).** Sete blocos convergidos: sinais → enriquecimento em waterfall → buying committee → outreach condicionado → sequência → qualificação → handoff com contexto no CRM. HubSpot Prospecting Agent a US$ 1/lead, Agentforce SDR GA. Para Laravel: máquina de estados do lead + `schedule_meeting` gateada por qualificação.
- **Vendedor defensivo (tema 30).** Vendedores LLM são acomodativos e manipuláveis por "paciência" no prompt (90% da variância de surplus). Decisões: não negociar preço livremente, validar racionalidade do acordo, detectar quando o outro lado é agente.

### 3.6 Modalidade e runtime (temas 14, 16, 20, 21, 27, 28)

- **Voz (tema 14).** gpt-realtime-2 fora de beta (07/05): 128K, SIP, MCP remoto; 2.1 com reasoning configurável (jul). Regra: tool < 200 ms ou fala de preenchimento. Sierra Voice Sims: dois loops de áudio com ruído e DTMF. Nada de voz no acervo.
- **Event-driven (tema 16).** Acordar por webhook/CDC/fila, três níveis de HITL (notify/question/review), agent inbox, fusão de eventos do mesmo cliente, agente outbound. O post de tracking 24/7 é cron; isto é evento. Claude Tag (23/06) como padrão replicável: identidade por canal, memória de canal, tarefas agendadas para si, modo ambient.
- **Browser DOM-first (tema 20).** `browser_toolset_20260801` GA: refs de accessibility tree, `javascript_exec` desligado por padrão; DOM-first 12–17 p.p. mais confiável que visão. Regra API > MCP > browser DOM > visão.
- **Zonas de confiança (tema 21).** Sessão append-only fora do container, harness stateless com `wake(sessionId)`, sandbox descartável, credential proxy na borda de rede (o LLM vê placeholder). Convergência confirmada por arqueologia em 3 harnesses open-source (arXiv 25/08). Versão pragmática de CaMeL: planner só vê instrução confiável, LLM em quarentena só devolve dados tipados, PHP executa com taint.

---

## 4. Janelas de news-jacking abertas (datas dos últimos 30 dias)

| Data | Fato | Tema |
|---|---|---|
| 10/09 | Managed Agents permission policy `auto` | 1 |
| 08/09 | Hyper-τ-bench (Sierra): agentes que constroem agentes | 35 |
| 03/09 | Estudo Calgary: memory poisoning escapa de eval por turno | 8 |
| 02/09 | Anthropic Commerce Agents blueprint | 2, 13 |
| 01/09 | Kong AI Gateway 2.0 GA; OWASP Agent Control Standard | 15, 24 |
| 26/08 | Claude in Chrome GA | 20 |
| 25/08 | arXiv: convergência de harnesses; "unidade de verificação" 1–2 ações | 21, 1 |
| 24/08 | Okta Agent SSO GA | 11 |
| 20/08 | PolicyGuide | 7 |
| 17/08 | A2A entra na AAIF | 15 |

---

## 5. Ações fora da pauta: posts existentes com fato novo

| Post | O que mudou | Fonte |
|---|---|---|
| `como-implementar-agent-builder-e-chatkit-da-openai-com-laravel` | OpenAI descontinua Agent Builder e Evals hospedado: read-only 31/10/2026, desligamento 30/11/2026 | developers.openai.com/api/docs/deprecations (anúncio 03/06) |
| `como-criar-mcp-server`, `como-criar-um-servidor-mcp-do-zero`, `mcp-em-producao-oauth-schema-gateway`, `o-que-e-mcp` | Spec 2026-07-28: stateless, MRTR, Tasks como extensão, auth endurecida, deprecações | modelcontextprotocol.io/specification/2026-07-28/changelog |
| `o-que-e-fine-tuning`, `fine-tuning-rag-ou-prompt-qual-escolher`, `quando-usar-rag-fine-tuning-ou-contexto`, `rag-fine-tuning-juntos-arquitetura-hibrida-96` | OpenAI desliga fine-tuning self-serve: sem novas orgs 07/05, restrição 02/07, fim 06/01/2027 | developers.openai.com/api/docs/deprecations |
| `compliance-eu-ai-act-nist-rmf-checklist-18-itens-brasil`, `adocao-segura-ia-empresa-eu-ai-act-nist-rmf` | Digital Omnibus: alto risco Anexo III adiado para 02/12/2027; OWASP Agentic Top 10 e ACS (01/09) | gibsondunn.com (27/05); genai.owasp.org (01/09) |
| `como-criar-um-agente-de-ia-para-whatsapp`, `agente-bolao-copa-whatsapp-evolution-api-n8n`, `tutorial-...-twilio-...-whatsapp` | Meta Business Agent global (03/06), cobrança por token (01/08) | about.fb.com/news/2026/06/meta-business-agent |
| `criar-bot-no-slack-com-claude` | Claude in Slack antigo encerrado em 03/08/2026; substituído por Claude Tag | anthropic.com/news/introducing-claude-tag (23/06) |

---

## 6. O que não afirmar (ressalvas dos pesquisadores)

- Datas de lançamento dos Managed Agents (08/04) e self-hosted sandboxes (19/05) vêm de fontes secundárias; o header `managed-agents-2026-04-01` e as docs confirmam existência, não a data.
- "Context Builder / Tool Router / Eval" como componentes internos do harness da Anthropic: só em Medium/dev.to. Não usar.
- Resolution rates de vendors (Sierra até 90%, Intercom 76%, voz 72%) são marketing ou secundárias.
- "Bessemer: 41% híbrido / 61% outcome até fim de 2026" não consta no playbook da Bessemer.
- Pix nativo via Meta Business Agent: só fontes BR secundárias, sem doc oficial.
- Stripe SPT / Link Agent Wallet: Brasil fora da lista oficial.
- Agent Pay for Machines, AP2 v0.2, MPP/x402: anúncio e v0.x, sem volume publicado.
- "Rakuten 97% menos erros" e "Sierra Company Brain": só secundárias.
- Advisory NSA/DoD de 02/06 sobre tool poisoning: não localizado o PDF primário.
- OTel GenAI: todos os documentos ainda `Status: Development`; campos podem mudar.
- A2A v1.0: data exata (12/03 vs 09/04) diverge entre fontes secundárias.
- Não há RFT de vendas anunciado por OpenAI/Anthropic; o que existe é REPO (ACL Industry) com A/B real.
- Speculative tool calling, CaMeL/NOVA/Parallax, Trace2Skill, origin-bound memory: papers sem produto GA.

---

## 7. Próximo passo sugerido

Rodar `planejar-pauta` sobre os temas 1–20 para cruzar com Search Console e DataForSEO (volume, KD, striking distance) antes de escrever. Este dossiê responde "o que existe e o que falta"; não responde "o que o Google vai premiar". Os 6 relatórios detalhados em [`pesquisa-tecnicas-agentes-2026/`](pesquisa-tecnicas-agentes-2026/) já trazem, por técnica, a delimitação anti-canibalização ("adjacente a qual slug, qual ângulo novo") que a `criar-post-blog` precisa.
