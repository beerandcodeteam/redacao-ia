# Pesquisa 01 — Arquitetura e Runtime de agentes em produção (estado em 12/09/2026)

Escopo: técnicas de arquitetura/runtime para agentes que operam como sistema de produção (agente de vendas, motor de resolução de suporte, agente operacional). Prioridade: últimos 6 meses (mar–set/2026). Método: 20 buscas + ~35 fetches em fontes primárias (docs oficiais Anthropic/OpenAI/Google/Microsoft/AWS/Cloudflare, blogs de engenharia Stripe/Sierra/Decagon/Temporal/Inngest/Restate/Pydantic, arXiv, releases Kong/Solo.io). Acervo do blog (~330 slugs) lido antes; cada técnica traz o confronto com o que já existe.

Convenção de maturidade:
- **experimental**: preview/alpha ou paper sem implementação
- **early adopters**: beta pública com clientes nomeados, ou GA recente (< 6 meses)
- **mainstream**: GA há mais de 6 meses, múltiplos vendors, adoção documentada

Legenda: [SHIPPING] = disponível e usável hoje; [PREVIEW] = beta/alpha/research preview; [PAPER] = proposta sem produção; [RUMOR] = não confirmado em fonte primária.

---

### 1. Durable execution como backbone do loop do agente (workflow = loop, activity = chamada)

- **O que é**
  O loop do agente (decidir → chamar tool → observar) roda dentro de um *workflow* durável; cada chamada de LLM e cada tool call é uma *activity* cujo resultado é gravado num histórico de eventos imutável. Se o processo cai, o runtime **reexecuta o workflow de forma determinística a partir do histórico** (replay), pulando as activities já concluídas, e o agente retoma no passo exato. Enquanto espera (aprovação humana, webhook, sleep de dias) o workflow não ocupa compute. O histórico ainda permite *branching*: Temporal cita testar 100 variantes de prompt no passo 92 de um agente de 100 passos custando 900 passos em vez de 10.000.
  Variantes do modelo: Temporal (event history + replay), Restate (journal por função, binário único), Inngest (`step.run` com cache de resultado, `waitForEvent`), Vercel Workflow DevKit (`"use workflow"`/`"use step"`, cada step vira rota isolada), Microsoft Durable Task extension para Agent Framework (Azure Durable Functions ou self-hosted).

- **Quem está usando/shipping**
  - Temporal — "Building AI agents that overcome the complexity cliff" (10/03/2026); integração OpenAI Agents SDK GA em 23/03/2026 (Python); "Temporal and agentic sandboxes: the OpenAI Agents SDK" (16/04/2026); clientes citados: OpenAI, Abridge, Lovable, Replit, Hebbia. Temporal levantou US$ 300M a US$ 5B em 17/02/2026 (fonte secundária).
  - Restate + Pydantic AI — "Build durable agents with Restate and Pydantic AI" (12/05/2026): journaling de cada step, Virtual Objects por sessão, *awakeables* para aprovação humana com timeout que sobrevive a restart.
  - Inngest — "Durable Execution: The Key to Harnessing AI Agents" (19/02/2026).
  - Vercel Workflow DevKit — anúncio 23/10/2025; GA do pacote `workflow` com 200k+ downloads semanais e Python SDK em beta (fonte: comunidade Vercel/GitHub, 2026). AI SDK v7 adiciona `WorkflowAgent`.
  - Microsoft — Durable Task extension para Agent Framework (public preview; docs learn.microsoft.com/agent-framework/hosting/azure-functions), dois modos: Azure Functions ou bring-your-own-compute.

- **Maturidade**: **early adopters → mainstream** no ecossistema Python/TS. Evidência: integração oficial Temporal×OpenAI Agents SDK em GA; quatro vendors independentes (Temporal, Restate, Inngest, Vercel) com posts 2026 dedicados a agentes; Microsoft embutindo no framework oficial. Para PHP/Laravel ainda é **early adopters** (Temporal tem SDK PHP oficial, mas nenhum dos posts 2026 cobre PHP).

- **Aplicação em agente de vendas / motor de resolução**
  Motor de resolução: o ticket vira um workflow; cada tentativa de resolução (consulta CRM, proposta de reembolso, espera da resposta do cliente por 48h, escalação) é activity/sinal. Um crash do worker no meio de um reembolso não duplica o reembolso (activity idempotente, resultado no histórico). Agente de vendas: follow-up em cadência (`sleep 3 dias`, `waitForEvent('reply')`) sem fila customizada; troca de prompt testada com replay do histórico real de leads.

- **Gap vs blog**
  Adjacente a `noticias/agente-ia-estado-entre-execucoes` (estado entre execuções), `tutoriais/filas-laravel-2026-horizon-redis-tracing` (filas) e `tutoriais/sistemas-multiagentes-orquestracao-assincrona`. **Ângulo novo**: persistir estado ≠ durable execution. O post existente trata de *guardar estado*; o que falta é **replay determinístico a partir de event history**, o conceito de *complexity cliff* (quando reiniciar do zero deixa de ser opção por efeitos colaterais), idle a custo zero, e branching de histórico para testar prompts. Para o público Laravel: comparar Temporal PHP SDK vs "event sourcing caseiro com jobs Horizon" — nenhum post cobre.

- **Fontes**
  - https://temporal.io/blog/building-ai-agents-that-overcome-the-complexity-cliff (10/03/2026)
  - https://temporal.io/blog/announcing-openai-agents-sdk-integration (GA 23/03/2026)
  - https://temporal.io/blog/introducing-temporal-and-agentic-sandboxes-openai-agents-sdk (16/04/2026)
  - https://docs.temporal.io/develop/python/integrations/openai-agents
  - https://pydantic.dev/articles/restate-durable-execution-pydanticai (12/05/2026)
  - https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents (19/02/2026)
  - https://vercel.com/blog/introducing-workflow (23/10/2025); https://github.com/vercel/workflow
  - https://learn.microsoft.com/en-us/agent-framework/hosting/azure-functions
  - https://techcommunity.microsoft.com/blog/appsonazureblog/bulletproof-agents-with-the-durable-task-extension-for-microsoft-agent-framework/4467122

---

### 2. Sessão como event log append-only, harness stateless, sandbox descartável (três zonas de confiança)

- **O que é**
  Arquitetura em que (a) a **sessão** é um log de eventos imutável e durável que vive fora do container e fora da janela de contexto; (b) o **harness** (loop, roteamento de tools, montagem de contexto) é stateless e recuperável por `wake(sessionId)` — relê o log e continua; (c) o **sandbox** onde código/tools executam é descartável e tratado como não confiável. Credenciais nunca entram no sandbox: um *credential proxy* injeta tokens na borda de rede (o sandbox vê placeholders). Esse mesmo padrão foi encontrado por arqueologia de código em três harnesses open-source independentes: "append-only, replayable session records for crash recovery" é um dos cinco pontos de convergência.

- **Quem está usando/shipping**
  - Anthropic Claude Managed Agents [PREVIEW/beta pública, header `managed-agents-2026-04-01`] — docs oficiais: "Event history is persisted server-side and can be fetched in full"; "stateful by design: sessions are long-running, resume cleanly after pauses". Vaults (beta, 09/06/2026): "storing placeholders in the sandbox while attaching real keys at the network boundary". Análise independente da Pluto Security (abr/2026) descreve sandbox gVisor, proxy MITM com JWT, metadata endpoints bloqueados.
  - Cloudflare Project Think (15/04/2026, experimental): sessões persistentes em árvore (fork, compaction não destrutiva, FTS5) num SQLite co-localizado por agente; fibers com `stash()`/`onFiberRecovered`.
  - Sierra Agency (29/07/2026): runners hibernam e restauram estado "via checkpoint events from an append-only output queue"; "Agents should not have any API keys or other secrets accessible to them by default" — inferência via proxy externo que injeta credenciais JIT.
  - arXiv 2608.23953 (25/08/2026): convergência em deepagents (LangChain), pi (Earendil) e dsh (DeepSeek).

- **Maturidade**: **early adopters**. Anthropic em beta; Cloudflare experimental; Sierra em produção interna (Pinecone, Ghostwriter) mas proprietário. O padrão em si (event log + replay) é maduro em outros domínios; a aplicação a agentes com sandbox-como-zona-hostil é de 2026.

- **Aplicação em agente de vendas / motor de resolução**
  Motor de resolução com 3 camadas: log da conversa+tool calls em Postgres (append-only, auditável por compliance), worker do loop stateless (pode escalar horizontalmente e morrer à vontade), execução de ações sensíveis (emitir crédito, alterar pedido) atrás de proxy que injeta o token do ERP — o LLM nunca vê a chave. Um prompt injection que "convença" o agente a exfiltrar credenciais não tem o que exfiltrar.

- **Gap vs blog**
  Adjacente a `tutoriais/anatomia-de-um-agent-harness-state-tool-execution-feedback-loops-e-guardrails` e `tutoriais/anatomia-de-um-harness-em-producao-as-6-camadas-que-separam-poc-de-sistema-confiavel` (camadas do harness) e a `tutoriais/prompt-injection-agente-site-raspado-system-prompt`. **Ângulo novo**: os posts descrevem *componentes* do harness; não descrevem a **separação em zonas de confiança** (sessão/harness/sandbox), a recuperação por *replay do log* nem o **credential proxy na borda de rede** como defesa estrutural (vs. guardrail no prompt). O paper arXiv dá a evidência empírica de que isso é convergência de indústria, não opinião.

- **Fontes**
  - https://platform.claude.com/docs/en/managed-agents/overview
  - https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes
  - https://claude.com/blog/whats-new-in-claude-managed-agents (09/06/2026 — vaults, scheduled deployments)
  - https://pluto.security/blog/inside-claude-managed-agents/ (abr/2026, análise terceira)
  - https://blog.cloudflare.com/project-think/ (15/04/2026)
  - https://sierra.ai/blog/agency-secure-scalable-sandboxes-for-agents (29/07/2026)
  - https://arxiv.org/html/2608.23953 (25/08/2026)

---

### 3. Harness × Runtime: separação de camadas e runtimes que hospedam harnesses de terceiros

- **O que é**
  Em 2026 a indústria estabilizou uma separação: **harness** = camada de aplicação que transforma modelo em agente (loop, montagem de prompt, dispatch de tools, compaction, subagentes, parsing); **runtime** = camada de infraestrutura onde o agente executa (isolamento de processo/sessão, sandbox, limites de recurso, egress de rede, brokering de credenciais, checkpoint durável, escala, telemetria/auditoria). Guardrails de entrada/saída ficam no harness; egress, sandbox e credenciais ficam no runtime. Consequência prática: runtimes passaram a hospedar **harnesses de terceiros** — o mesmo runtime roda Claude Code, Codex, Pi, Project Think; o Microsoft Agent Framework ganhou conectores para Claude Agent SDK e GitHub Copilot SDK.

- **Quem está usando/shipping**
  - Credal — "Agent Harness vs Agent Runtime" (21/04/2026): define as duas listas de responsabilidades.
  - Cloudflare — "Bringing more agent harnesses and frameworks to Cloudflare, starting with Flue" (17/06/2026): três camadas explícitas (Framework: Flue; Harness: Pi, Project Think, Claude Code, OpenCode, Codex; Runtime: Agents SDK com fibers, Code Mode, filesystem virtual em SQLite).
  - Microsoft Agent Framework 1.0 GA (02/04/2026) com "Agent Harness" (compaction automática, file memory, shell/fs, approvals) e "Hosted Agents" no Foundry (scale-to-zero, VM por sessão); Harness e Hosted Agents em GA (InfoQ, ago/2026, pós-Build 02–03/06/2026). Frase de Wes Steyn (Microsoft): "A model on its own can only generate text."
  - Anthropic — docs posicionam Managed Agents como "pre-built, configurable agent harness that runs in managed infrastructure" vs Messages API para "custom agent loops".
  - AWS AgentCore — "managed harness" declarativo (modelo+tools+instruções por config), disponível inclusive em GovCloud (ago/2026).

- **Maturidade**: **mainstream** como vocabulário e como produto (Microsoft GA, AWS GA, Cloudflare GA do Agents SDK; Anthropic beta). A convergência de *nomes* ("harness") aconteceu em 2026 — em 2025 cada vendor chamava de outra coisa.

- **Aplicação em agente de vendas / motor de resolução**
  Decisão de arquitetura: escrever o harness (regras de negócio, tom, tools do CRM) e **alugar o runtime** (Managed Agents, Hosted Agents, Cloudflare) — ou o inverso, usar harness pronto (Claude Agent SDK) sobre runtime próprio (K8s + gVisor). O mesmo harness de suporte roda em sandbox leve no dev e em cluster endurecido na prod, só mudando política de rede e limites.

- **Gap vs blog**
  O blog já tem `noticias/o-que-e-harness-de-ia`, `noticias/harness-ia-nao-basta`, `noticias/o-que-e-harness-engineering-e-por-que-seu-claude-code-trava-em-tarefas-longas`, `tutoriais/anatomia-de-um-harness-em-producao-...`, `tutoriais/harness-laravel-claude-do-zero-loop-autonomo`. **Todos tratam o harness.** Nenhum define a **camada runtime** como coisa separada nem cobre o fenômeno "runtime hospedando harness alheio" (Claude Code rodando dentro do Cloudflare; MAF conectando Claude Agent SDK). Ângulo novo: "você escreveu o harness; onde ele roda? — a lista de 8 responsabilidades do runtime que não cabem no harness".

- **Fontes**
  - https://credal.ai/blog/agent-harness-vs-agent-runtime (21/04/2026)
  - https://blog.cloudflare.com/agents-platform-flue-sdk/ (17/06/2026)
  - https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/ (jun/2026)
  - https://www.infoq.com/news/2026/08/agent-framework-harness-ga/ (ago/2026)
  - https://platform.claude.com/docs/en/managed-agents/overview
  - https://aws.amazon.com/about-aws/whats-new/2026/08/agentcore-memory-policy-harness-govcloud/ (ago/2026)

---

### 4. Execução dividida: control plane do vendor, sandbox no perímetro do cliente (self-hosted sandbox + work queue)

- **O que é**
  O vendor mantém orquestração, modelo e histórico de sessão; a **execução de tools** (bash, filesystem, processos, egress) acontece em infraestrutura do cliente. Mecanismo: o ambiente self-hosted funciona como **fila de trabalho** — a sessão é enfileirada como work item, um worker do cliente faz claim, baixa skills/memória, executa as tool calls e posta os resultados de volta ao control plane. Três padrões de deploy: worker always-on, worker acordado por webhook (`session.status_run_started`), ou sandbox-por-sessão (processo efêmero que executa um work item e sai). Complemento: **MCP tunnels** para o modelo alcançar MCP servers privados sem expô-los à internet.

- **Quem está usando/shipping**
  - Anthropic — self-hosted sandboxes em **beta pública** (anunciado em Code with Claude Londres, 19/05/2026, segundo fontes secundárias; docs oficiais confirmam o modelo work-queue e a lista de provedores: AWS Lambda MicroVMs, Blaxel, Cloudflare, Daytona, E2B, Fly.io, GKE Agent Sandbox, Modal, Namespace, Superserve, Vercel + genérico). Com self-hosted, Managed Agents passa a ser elegível a **ZDR e HIPAA BAA** (a versão cloud não é). Memory stores em self-hosted desde ago/2026 (fonte secundária, 19–20/08/2026). MCP tunnels em **research preview**.
  - Kubernetes SIG Agent Sandbox publica guia de uso "Anthropic Managed Agents" (agent-sandbox.sigs.k8s.io).
  - Microsoft Foundry Hosted Agents: modelo inverso (tudo no vendor), com VM por sessão e filesystem persistente.

- **Maturidade**: **early adopters** (beta pública; lista de 11 provedores integrados indica tração de ecossistema, mas sem GA).

- **Aplicação em agente de vendas / motor de resolução**
  Empresa com dados de cliente sob LGPD/residência BR: o agente de resolução raciocina no vendor, mas consulta o banco de pedidos e executa o reembolso **dentro da VPC da empresa**; tool inputs/outputs ainda trafegam ao control plane (limitação documentada — "Tool inputs/outputs flow to Anthropic's control plane"), logo PII precisa ser minimizada antes de retornar. Padrão webhook-triggered evita worker ocioso pago.

- **Gap vs blog**
  `tutoriais/aws-bedrock-o-que-e-claude-producao-governanca` cobre governança via Bedrock; `tutoriais/mcp-em-producao-oauth-schema-gateway` cobre MCP. **Não existe** nada sobre o modelo work-queue/split execution nem sobre MCP tunnels. Ângulo: "seu agente pensa na Anthropic e executa no seu K8s — o que atravessa a fronteira e o que não atravessa".

- **Fontes**
  - https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes
  - https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview (research preview)
  - https://agent-sandbox.sigs.k8s.io/docs/use-cases/anthropic-managed-agents/
  - https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/ (Hosted Agents)
  - Secundárias para datas (19/05 e 19–20/08/2026): https://mer.vin/2026/05/claude-managed-agents-self-hosted-sandboxes-and-private-mcp-tunnels/ ; https://explainx.ai/blog/claude-managed-agents-memory-domain-controls-console-update-august-2026

---

### 5. Sandbox em microVM como fronteira de confiança + CodeAct em microVM (Hyperlight, Firecracker, gVisor, Code Mode)

- **O que é**
  Código gerado pelo modelo executa em isolamento de hardware ou quase-hardware: **Firecracker** (microVM com kernel próprio — E2B, Vercel Sandbox, AWS Lambda MicroVMs), **gVisor** (kernel em user-space com filtragem de syscalls — Modal, sandbox cloud da Anthropic), **Hyperlight** (microVM ultraleve da Microsoft, sem SO convidado). Em 2026 o sandbox deixou de ser só "rodar Python com segurança" e virou **fronteira arquitetural**: egress por proxy filtrante, credenciais injetadas JIT fora do sandbox, snapshot/restore de memória. **CodeAct** (modelo escreve um programa que chama `call_tool()` várias vezes num único turno, em vez de N rodadas de tool calling) foi embutido nesses sandboxes: Microsoft reporta −52% latência e −64% tokens (alpha, `agent-framework-hyperlight`); Cloudflare `@cloudflare/codemode` roda código do LLM em Dynamic Workers.

- **Quem está usando/shipping**
  - Microsoft Agent Framework — CodeAct sobre Hyperlight, **alpha** (Build, jun/2026).
  - Cloudflare — Code Mode / Dynamic Workers no Agents SDK (Project Think 15/04/2026; Flue 17/06/2026).
  - Sierra Agency (29/07/2026) — "hardened container" (non-root, rootfs read-only), egress proxy filtrante, hibernação de runners, p99 40ms no message queue.
  - Modal (jun/2026) — comparativo: gVisor (Modal), Firecracker (E2B, Vercel), Sysbox (Daytona); snapshots de fs/memória/GPU.
  - Anthropic — sandbox cloud em gVisor (análise Pluto); lista de 11 provedores de sandbox self-hosted.
  - OpenAI Agents SDK — "agentic sandboxes" com Modal, Daytona, Docker, E2B (Temporal blog, 16/04/2026).

- **Maturidade**: sandbox microVM = **mainstream** (E2B, Modal, Vercel Sandbox em GA; OpenAI/Anthropic/Microsoft integram). CodeAct-em-microVM = **experimental/early** (MS alpha; Cloudflare experimental).

- **Aplicação em agente de vendas / motor de resolução**
  Motor de resolução que precisa cruzar planilha de pedidos com política de devolução: em vez de 8 tool calls sequenciais (buscar pedido, buscar itens, calcular, ...), um script de 20 linhas no sandbox faz tudo e devolve um JSON — menos latência no chat e menos tokens. A fronteira importa porque o script é gerado a partir de texto do cliente: egress bloqueado, sem credenciais, tempo de vida de segundos.

- **Gap vs blog**
  Adjacente forte: `tutoriais/programmatic-tool-calling` e `tutoriais/programmatic-tool-calling-futuro-agente` (o *padrão* de chamar tools via código) e `noticias/agente-openai-fugiu-sandbox-hugging-face` (incidente). **O que não existe**: a camada de **isolamento** — Firecracker vs gVisor vs Hyperlight, por que "container Docker não é sandbox", egress proxy, credenciais JIT, snapshot/restore, e o fato de CodeAct estar sendo *embutido em microVM* pelos vendors (MS −64% tokens). Ângulo: "programmatic tool calling você já conhece; agora onde isso executa e quem paga se escapar".

- **Fontes**
  - https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/ (CodeAct/Hyperlight, alpha)
  - https://blog.cloudflare.com/project-think/ (15/04/2026)
  - https://sierra.ai/blog/agency-secure-scalable-sandboxes-for-agents (29/07/2026)
  - https://modal.com/resources/best-microvm-sandboxes-ai-code-execution (jun/2026)
  - https://temporal.io/blog/introducing-temporal-and-agentic-sandboxes-openai-agents-sdk (16/04/2026)
  - https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes (lista de provedores)
  - https://manveerc.substack.com/p/ai-agent-sandboxing-guide (2026, secundária, taxonomia em camadas)

---

### 6. Agent gateway: data plane única para LLM + MCP + A2A com identidade e custo por agente

- **O que é**
  Evolução do "AI gateway" (proxy para LLMs com virtual keys, rate limit, fallback) para **agent gateway**: o mesmo proxy governa três tipos de tráfego — agente→LLM, agente→tool (MCP) e agente→agente (A2A) — com **identidade por agente** (não por usuário ou por app), políticas globais de quem fala com quem, inspeção de streams em tempo real (policy violations, prompt injection), alocação de custo por agente e audit log unificado. Internamente (Sierra) o MCP gateway vira catálogo de tools com permissão por agente e por workflow, identidades separadas para humano (interativo) e service account (automação), e auditoria multi-passo (candidatos determinísticos → triagem por modelo rápido → classificação de sensibilidade).

- **Quem está usando/shipping**
  - Kong — "Kong Agent Gateway" no AI Gateway 3.14 (14/04/2026): LLM + MCP + A2A numa control plane; AI Gateway 2.0 **GA em 01/09/2026** com MCP server bundling, políticas identity-aware, custo por modalidade.
  - agentgateway (Solo.io → Linux Foundation, ago/2025): proxy Rust para MCP/A2A/LLM; contribuidores AWS, Cisco, IBM, Microsoft, Red Hat.
  - Sierra — "Building Sierra's MCP Gateway: an engineering iceberg" (22/07/2026): 45+ sistemas, 89% dos funcionários usam, 67% dos commits vêm de outros times.
  - Portkey adquirida pela Palo Alto Networks (29/05/2026), integrada ao Prisma AIRS como "AI Gateway control plane for enterprise AI and agents" (fonte secundária).
  - AWS AgentCore Gateway + Policy (ver técnica 8).
  - Cloudflare AI Gateway: metadata customizada para quebrar custo por agente.

- **Maturidade**: **mainstream** para LLM gateway; **early adopters** para a camada MCP/A2A por agente (Kong 3.14 abr/2026, 2.0 set/2026; agentgateway sem GA formal declarado).

- **Aplicação em agente de vendas / motor de resolução**
  Agente de vendas e agente de suporte compartilham o CRM, mas com identidades distintas no gateway: vendas pode `create_deal`, suporte não; suporte pode `issue_credit` até um teto, vendas não. Custo de tokens e de tool calls sai por agente, não por API key global. Quando o agente de vendas delega ao de suporte (A2A), a política global diz se essa conversa é permitida e loga os dois lados.

- **Gap vs blog**
  `tutoriais/mcp-em-producao-oauth-schema-gateway` cobre gateway **MCP** (OAuth, schema). **Ângulo novo**: (1) identidade e política **por agente** e não por usuário; (2) tráfego **A2A** governado; (3) custo alocado por agente; (4) lições da Sierra ("80% do workflow arredonda para 0%", dual identity humano/service account). Nenhum post cobre Kong Agent Gateway nem agentgateway/LF.

- **Fontes**
  - https://konghq.com/blog/product-releases/kong-agent-gateway (14/04/2026)
  - https://konghq.com/blog/product-releases/kong-ai-gateway-2-0-agentic-ai (GA 01/09/2026)
  - https://konghq.com/company/press-room/press-release/kong-ai-gateway-now-supports-agent-to-agent-traffic-becoming-the-most-comprehensive-ai-gateway-for-the-agentic-era
  - https://agentgateway.dev/ ; https://www.solo.io/blog/solo-contributes-agentgateway-linux-foundation (ago/2025)
  - https://sierra.ai/blog/building-sierras-mcp-gateway-an-engineering-iceberg (22/07/2026)
  - Portkey/PANW (secundária): https://www.braintrust.dev/articles/ai-gateway-comparison-2026

---

### 7. Blueprint híbrido: workflow determinístico com nós agênticos e orçamento de iteração fixo (state machine × loop)

- **O que é**
  Em vez de "loop autônomo até resolver" ou "máquina de estados rígida", o sistema é um **grafo onde alguns nós são código determinístico obrigatório** (lint, validação de identidade, push, checagem de política) e outros são **loops agênticos com escopo limitado** (tools restritas, contexto recortado, subtarefa definida). Limites explícitos de retentativa: Stripe dá ao agente **uma** iteração extra contra CI após falha sem autofix; depois do segundo push vai para revisão humana. Decagon chama de Agent Operating Procedures: linguagem natural do time de negócio "compila" para workflow validado com passos sensíveis (reembolso, verificação de identidade) executados em código. Na academia, o arXiv 2604.11378 formaliza o espectro "Agent Loop (|U|≤1) → Graph Harness (DAG imutável por versão, recuperação em 3 níveis)" e o arXiv 2606.20058 mede DAG Plan&Execute vs ReAct em 208 cenários até 200 agentes — "scale, not task complexity, dominates orchestration performance"; ReAct foi mais robusto a falhas em escala enterprise, e um Task Manager com priorização/merge de eventos reduziu latência de fila alta prioridade em 14–75%.

- **Quem está usando/shipping**
  - Stripe Minions — Parte 1 (09/02/2026) e Parte 2 (19/02/2026): ~1.300 PRs/semana, blueprints = "collection of agent skills interwoven with deterministic code", devboxes pré-aquecidos (10s), fork do goose (Block), Toolshed com 400+ tools via MCP.
  - Decagon — AOPs (posts 2025; Agent Versioning 05/11/2025; Spring 2026: Proactive Agents + Agent Workbench, mar/2026).
  - arXiv 2604.11378 (13/04/2026) [PAPER — "position paper and design proposal", sem implementação]; arXiv 2606.20058 (18/06/2026) [PAPER com benchmark de 208 cenários]; arXiv 2604.17025 CAAF (18/04–04/05/2026) [PAPER com código Apache-2.0, "harness as an asset": invariantes de domínio em registro legível por máquina].

- **Maturidade**: **mainstream** na prática (Stripe, Decagon, Sierra em produção); **experimental** na formalização (papers 2026 sem consenso — um paper defende DAG, outro mostra ReAct mais robusto em escala).

- **Aplicação em agente de vendas / motor de resolução**
  Motor de resolução: nó determinístico `verificar_identidade` → nó agêntico `diagnosticar` (tools: ler pedido, ler histórico) → nó determinístico `checar_politica_reembolso(valor, prazo)` → nó agêntico `redigir_resposta` → nó determinístico `enviar + registrar`. O agente nunca decide *se* verifica identidade; decide *como* diagnosticar. Orçamento: no máximo 2 rodadas de diagnóstico antes de escalar.

- **Gap vs blog**
  Adjacente a `noticias/plan-and-execute-pattern-cortou-90-custo-agente` (planner/executor), `noticias/anti-patterns-agentes-ia-producao`, `noticias/chatbot-nao-e-agente-teste-3-turnos`, `tutoriais/multi-agent-laravel-3-padroes-orchestrator-hierarchical-swarm`. **Ângulo novo**: não é planner/executor nem multi-agent — é **nó determinístico obrigatório intercalado com nó agêntico de escopo fechado**, com orçamento de iteração explícito (regra "2 pushes e vai pra humano" da Stripe) e a evidência contraditória dos papers (DAG vs ReAct em escala). O conceito AOP (negócio escreve em linguagem natural, engenharia fixa os passos em código) também não aparece no acervo.

- **Fontes**
  - https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents (09/02/2026)
  - https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2 (19/02/2026)
  - https://decagon.ai/blog/why-we-built-aop ; https://decagon.ai/blog/decagon-agent-versioning (05/11/2025) ; https://decagon.ai/blog/spring26-product-launch (mar/2026) ; https://decagon.ai/blog/agent-workbench
  - https://arxiv.org/html/2604.11378v1 (13/04/2026)
  - https://arxiv.org/abs/2606.20058 (18/06/2026)
  - https://arxiv.org/abs/2604.17025 (abr–mai/2026)

---

### 8. Autorização de tool call por política fora do modelo (Cedar a partir de linguagem natural, interceptação no gateway)

- **O que é**
  A decisão "este agente pode executar esta tool com estes argumentos para este principal?" é tomada por um **motor de políticas determinístico** que intercepta a chamada **entre o agente e a tool**, independente do raciocínio do LLM. AWS AgentCore Policy traduz regras em linguagem natural para **Cedar** (linguagem de autorização open-source) e as aplica no AgentCore Gateway. Exemplo documentado: só principais com role `refund-agent` acessam a tool de reembolso, e só para valores < US$ 200. Complementos: AgentCore Memory com fine-grained access control por usuário/tenant via Gateway (ago/2026); Managed Agents com `allowed_domains`/`blocked_domains` em web_search/web_fetch.

- **Quem está usando/shipping**
  - AWS — AgentCore Policy preview 02/12/2025, **GA 03/03/2026**; Evaluations GA 31/03/2026; Memory FGAC ago/2026.
  - Kong AI Gateway 2.0 (01/09/2026) — "identity-aware AI policies".
  - Decagon AOP — validação de passos sensíveis em código (produto).
  - Sierra MCP Gateway — permissão por agente e por workflow (22/07/2026).

- **Maturidade**: **early adopters → mainstream** (GA na AWS há 6 meses; Kong GA set/2026).

- **Aplicação em agente de vendas / motor de resolução**
  O limite de desconto do agente de vendas (ex.: ≤ 15% sem aprovação) e o teto de reembolso do agente de suporte deixam de ser instrução no system prompt (burlável) e viram política Cedar no gateway: se o modelo chamar `apply_discount(25)`, a chamada é negada antes de chegar ao ERP, e o evento é auditado. Compliance revisa a política, não o prompt.

- **Gap vs blog**
  `tutoriais/guardrails-para-agentes-de-ia` e `noticias/kimi-k3-guardrails` tratam guardrails (entrada/saída, conteúdo). **Ângulo novo**: **autorização** (quem pode chamar o quê com quais argumentos) como camada separada de guardrail de conteúdo, executada no gateway e não no prompt; Cedar gerado a partir de linguagem natural; exemplo numérico de reembolso. Não há post sobre AgentCore Policy.

- **Fontes**
  - https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/ (02/12/2025; atualização GA 03/03/2026)
  - https://aws.amazon.com/about-aws/whats-new/2026/08/agentcorememory-fine-grained-access-control/ (ago/2026)
  - https://konghq.com/blog/product-releases/kong-ai-gateway-2-0-agentic-ai (01/09/2026)
  - https://sierra.ai/blog/building-sierras-mcp-gateway-an-engineering-iceberg (22/07/2026)

---

### 9. Agentes ambientes / event-driven: acordar por evento (webhook, CDC, fila), não por chat — com HITL notify/question/review

- **O que é**
  O agente não tem "usuário digitando"; ele é **acordado por eventos** (webhook de CRM, mudança em tabela via CDC, mensagem em fila, alerta de monitoramento) e pode processar vários eventos concorrentes. Para não virar caos, o padrão inclui três níveis de human-in-the-loop: **notify** (age e avisa), **question** (para e pergunta), **review** (propõe e espera aprovação) — e uma "agent inbox" onde humanos veem o que o agente precisa. Em infraestrutura: EventBridge/SQS → Lambda → AgentCore Runtime; no Managed Agents, **webhooks** de ciclo de vida (`session.status_run_started`, eventos de deployment/run) permitem que o worker só gaste compute quando há trabalho; o arXiv 2606.20058 adiciona um Task Manager que infere prioridade, **funde eventos relacionados** e faz preempção.

- **Quem está usando/shipping**
  - Anthropic Managed Agents — scheduled deployments (cron, beta 09/06/2026) + webhooks de sessão/deployment + budget por run; clientes: Rakuten, Actively AI (busca agêntica para vendas), Ando (vendas/contratação), Notion, Browserbase, KERNEL, Milana.
  - AWS — sample oficial "ambient agents on AgentCore" (EventBridge 15 min + API Gateway/Slack → Lambda → AgentCore Runtime; padrões Notify e Question implementados, Review documentado como próximo passo).
  - LangChain — "ambient agents" + agent inbox (conceito 2025; reafirmado por Harrison Chase em Sequoia Training Data).
  - Decagon Proactive Agents (mar/2026) — outbound voice + user memory: o agente inicia a conversa.
  - Microsoft — "change-driven architecture enables ambient AI agents" (Tech Community, 2026; não consegui extrair o corpo, título confirmado).

- **Maturidade**: **early adopters**. Primitivas (webhooks, cron, filas) são maduras; o empacotamento como produto de agente é 2026 (Managed Agents beta; AgentCore sample; Decagon GA).

- **Aplicação em agente de vendas / motor de resolução**
  Vendas: evento `deal.stage_changed → proposta_enviada` acorda o agente, que lê o histórico, agenda follow-up em 3 dias (sleep durável) e, se o lead responder com objeção de preço, entra em modo **question** (pergunta ao vendedor se pode dar desconto) em vez de decidir. Suporte: evento `ticket.created` + CDC em `orders.status=delayed` dispara resolução proativa antes do cliente reclamar; eventos do mesmo cliente são **fundidos** (Task Manager) para não gerar 3 respostas.

- **Gap vs blog**
  `tutoriais/tracking-247-do-reativo-ao-agente-agendado` cobre **cron/agendamento**. **Ângulo novo**: disparo por **evento** (webhook/CDC/fila) em vez de horário; a taxonomia notify/question/review; agent inbox; fusão de eventos relacionados e preempção; agente **outbound** que inicia a conversa (Decagon). `tutoriais/como-criar-um-agente-de-ia-para-whatsapp` e `tutoriais/criar-bot-no-slack-com-claude` são reativos (chat).

- **Fontes**
  - https://platform.claude.com/docs/en/managed-agents/scheduled-deployments ; https://platform.claude.com/docs/en/managed-agents/webhooks
  - https://claude.com/blog/whats-new-in-claude-managed-agents (09/06/2026)
  - https://github.com/aws-samples/sample-ambient-agents-on-agentcore
  - https://sequoiacap.com/podcast/training-data-harrison-chase-2 (ambient agents / agent inbox)
  - https://decagon.ai/blog/spring26-product-launch (mar/2026)
  - https://arxiv.org/abs/2606.20058 (18/06/2026 — Task Manager: priority inference, related-event merging, preemption)
  - https://techcommunity.microsoft.com/blog/linuxandopensourceblog/beyond-the-chat-window-how-change-driven-architecture-enables-ambient-ai-agents/4475026 (título confirmado; corpo não extraído)

---

### 10. Tool call assíncrona com handle durável: MCP Tasks, Responses API background, Interactions API background

- **O que é**
  Padrão "call-now, fetch-later" para operações que não cabem num round-trip RPC (CI, aprovação humana, batch, job externo). O servidor devolve imediatamente um **handle durável** (`taskId`) com status (`working`, `input_required`, `completed`, `failed`, `cancelled`), TTL e intervalo de polling; o cliente faz `tasks/get`, responde a pedidos de input via `tasks/update` (elicitation no meio do voo, sem segunda conexão) e pode `tasks/cancel` (cooperativo). O ID sobrevive a desconexão/crash do cliente. O mesmo formato aparece nas APIs de modelo: OpenAI Responses `background=true` (poll do response object), Google Interactions API `background=True` (offload do loop de raciocínio ao servidor, `previous_interaction_id`), Anthropic dreams (job assíncrono com `pending/running/completed`).

- **Quem está usando/shipping**
  - MCP — Tasks introduzido como experimental na revisão 2025-11-25; **promovido a extensão standalone `io.modelcontextprotocol/tasks` na revisão de 28/07/2026** (capability única, métodos `tasks/get|update|cancel`, `notifications/tasks` opcional). Suporte de cliente "varia" (client matrix oficial). Cornelia Davis (Temporal) em palestra de ago/2026: "MCP Tasks (async): why aren't any agents supporting them?" — adoção de clientes ainda é o gargalo.
  - OpenAI — Responses API background mode (docs 2026), compaction server-side com `context_management.compact_threshold`.
  - Google — Interactions API (beta desde 11/12/2025) integrada ao ADK via `use_interactions_api=True`.
  - Anthropic — dreams (research preview) usa o padrão job+poll.

- **Maturidade**: spec **shipping** (jul/2026); adoção em clientes **experimental** (reconhecido publicamente pela Temporal). Background mode das APIs de modelo: **early adopters/mainstream**.

- **Aplicação em agente de vendas / motor de resolução**
  Tool `abrir_chamado_logistica` que depende de confirmação de um humano da transportadora: em vez de timeout de 30s, o MCP server devolve task em `working`; quando a transportadora responde, vai a `completed` e o agente retoma a conversa com o cliente. Se precisar de dado adicional, `input_required` devolve uma elicitation que o harness repassa ao cliente final. Sem isso, cada equipe reinventa fila+webhook+tabela de jobs.

- **Gap vs blog**
  `noticias/o-que-e-mcp`, `tutoriais/como-criar-mcp-server`, `tutoriais/como-criar-um-servidor-mcp-do-zero`, `tutoriais/mcp-em-producao-oauth-schema-gateway` — nenhum cobre Tasks (a extensão é de jul/2026, posterior). **Ângulo novo**: implementar um MCP server que devolve task em vez de bloquear; lifecycle `input_required`; e o paralelo com background mode de Responses/Interactions. Também vale a nota honesta: "spec pronta, clientes atrasados".

- **Fontes**
  - https://modelcontextprotocol.io/extensions/tasks/overview ; https://github.com/modelcontextprotocol/ext-tasks (revisão 2026-07-28)
  - https://aaif.io/blog/handle-long-running-mcp-tool-calls-with-the-mcp-tasks-extension
  - https://www.sean-weldon.com/blog/2026-08-08-mcp-tasks-async-why-arent-any-agents-supporting-them-cornelia-davis-temporal (08/08/2026, notas de palestra — secundária)
  - https://developers.openai.com/api/docs/guides/background ; https://developers.openai.com/api/docs/guides/compaction
  - https://developers.googleblog.com/building-agents-with-the-adk-and-the-new-interactions-api/ (11/12/2025)

---

### 11. Hibernação de agente: sessão ociosa sem compute (actor por sessão + scale-to-zero + fibers)

- **O que é**
  Agentes conversacionais passam a maior parte do tempo **esperando** o humano. O runtime trata cada sessão como um **ator com identidade durável** (singleton — sempre o mesmo objeto para o mesmo ID, sem race), com estado em storage local (SQLite co-localizado no Cloudflare; volume persistente na Sierra), que **hiberna** quando ocioso e **restaura** do checkpoint ao próximo evento. Sierra mede "2 to 4 orders of magnitude difference between active instances in 8 hours versus 8 days". Para trabalho longo dentro de um turno, Cloudflare adicionou `keepAlive()` (mar/2026, experimental) e **fibers** (`runFiber`, `stash`, `onFiberRecovered`) que checkpointam o instruction pointer e sobrevivem a eviction. Microsoft Hosted Agents: "pay nothing while the agent is idle".

- **Quem está usando/shipping**
  - Cloudflare Agents SDK sobre Durable Objects (GA) + Project Think fibers (15/04/2026, experimental).
  - Sierra Agency (29/07/2026): runner hibernation, control plane stateless + fleet stateful em K8s, p50 8ms / p99 40ms.
  - Microsoft Foundry Hosted Agents (GA): scale-to-zero, filesystem persistente entre escalas, VM por sessão.
  - Temporal/Restate: workflow ocioso não consome worker (técnica 1).
  - Anthropic Managed Agents: "sessions... resume cleanly after pauses" (beta).

- **Maturidade**: **mainstream** (Durable Objects, Hosted Agents GA); fibers **experimental**.

- **Aplicação em agente de vendas / motor de resolução**
  Agente de suporte em WhatsApp com 50 mil conversas abertas, das quais 300 ativas por minuto: modelo actor-por-conversa com hibernação paga 300, não 50 mil. A identidade singleton por `conversation_id` elimina a corrida clássica de duas mensagens do mesmo cliente chegando em workers diferentes e gerando duas respostas.

- **Gap vs blog**
  Adjacente a `noticias/custo-agente-ia-producao-2026-planilha-tco` e `tutoriais/quanto-custa-agente-ia-producao-conta-tokens` (custo, mas de **tokens**). **Ângulo novo**: custo de **compute ocioso** e o modelo actor-por-sessão (singleton + SQLite local + hibernação) como resposta; fibers como checkpoint de turno longo. Nada no acervo sobre Durable Objects/Agents SDK da Cloudflare.

- **Fontes**
  - https://developers.cloudflare.com/agents/ ; https://developers.cloudflare.com/agents/runtime/execution/durable-execution/
  - https://blog.cloudflare.com/project-think/ (15/04/2026)
  - https://www.infoq.com/news/2026/04/cloudflare-project-think/
  - https://sierra.ai/blog/agency-secure-scalable-sandboxes-for-agents (29/07/2026)
  - https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/ (Hosted Agents scale-to-zero)

---

### 12. Consolidação de memória offline ("dreaming"): job assíncrono que reescreve o memory store a partir de transcrições

- **O que é**
  Em vez de o agente só escrever memórias incrementais durante a sessão (acumulando duplicatas, contradições e entradas obsoletas), um **job separado e assíncrono** lê o memory store + 1–100 transcrições de sessões passadas e produz um **novo store** (deduplicado, contradições resolvidas pelo valor mais recente, novos insights). O store de entrada nunca é modificado — o time revisa o output e decide trocar ou descartar. Aceita `instructions` de síntese ("foque em preferências X; ignore notas pontuais"). Leva minutos a horas; cobrado por tokens do modelo escolhido. Paralelo na AWS: "episodic" strategy no AgentCore Memory (aprender com experiências passadas para tarefas similares).

- **Quem está usando/shipping**
  - Anthropic — Dreams, **research preview** (header `dreaming-2026-04-21`), modelos suportados incluem Opus 5, Fable 5, Opus 4.8, Sonnet 5; endpoints `/v1/dreams` com lifecycle `pending/running/completed/failed/canceled`, `session_id` exposto para assistir o pipeline.
  - AWS AgentCore Memory — episodic strategy (2026, "whats-new" da AWS, sem data precisa extraída).

- **Maturidade**: **experimental** (research preview com request access).

- **Aplicação em agente de vendas / motor de resolução**
  Agente de vendas que anota "cliente prefere boleto", depois "cliente mudou para cartão", depois "cliente reclamou do boleto": sem consolidação, as três coexistem e o modelo escolhe errado. Um dream semanal sobre as 100 últimas sessões gera o store limpo; o gestor revisa no Console antes de promover. Em suporte: consolidar padrões de resolução recorrentes em "insights" operacionais.

- **Gap vs blog**
  `tutoriais/memoria-de-agente-de-ia`, `tutoriais/memoria-agente-assistente-compras`, `tutoriais/pgvector-postgres-memoria-do-seu-agente`, `tutoriais/langgraph-mem0-langchain-mcp-do-que-voce-precisa` cobrem **escrita/leitura** de memória. **Ângulo novo**: **consolidação como job batch separado** (write-time vs. consolidation-time), output revisável/descartável, e como reproduzir o padrão com pgvector + job noturno para quem não está no Managed Agents.

- **Fontes**
  - https://platform.claude.com/docs/en/managed-agents/dreams (research preview; header `dreaming-2026-04-21`)
  - https://platform.claude.com/docs/en/managed-agents/memory
  - https://aws.amazon.com/about-aws/whats-new/2026/08/agentcore-memory-policy-harness-govcloud/ ; https://aws.amazon.com/about-aws/whats-new/2026/08/agentcorememory-fine-grained-access-control/

---

## Observações transversais (não são técnicas, mas afetam a pauta)

1. **Visual builder perdeu para código.** OpenAI anunciou em 03/06/2026 o fim do Agent Builder (canvas visual) e do Evals hospedado — read-only em 31/10/2026, desligamento em 30/11/2026; recomendação oficial: Agents SDK (código) ou Workspace Agents no ChatGPT. ChatKit e Connector Registry continuam. Lição arquitetural: superfícies proprietárias de orquestração são descartáveis; tools expostas via MCP sobrevivem à troca de framework. O blog tem `tutoriais/como-implementar-agent-builder-e-chatkit-da-openai-com-laravel` — **esse post precisa de atualização/aviso de descontinuação**. Fonte: https://developers.openai.com/api/docs/deprecations (via https://mcp.directory/blog/openai-agentkit-deprecation-2026).

2. **O que mudou em 2026 nas plataformas (resumo factual):**
   - Anthropic: Managed Agents (beta, header 2026-04-01); self-hosted sandboxes (beta pública, 19/05/2026 segundo secundárias); MCP tunnels (research preview); vaults + scheduled deployments (09/06/2026); dreams (research preview); memory stores em self-hosted (ago/2026, secundária); disponível também via Claude Platform on AWS.
   - OpenAI: Agent Builder/Evals descontinuados (03/06/2026); Agents SDK + Responses API (background mode, compaction server-side) são o caminho; "agentic sandboxes" no Agents SDK (Modal/Daytona/Docker/E2B); integração Temporal GA (23/03/2026).
   - Google: A2A v1.0 (início 2026: Signed Agent Cards, multi-tenancy, JSON-RPC + gRPC, negociação de versão) [datas exatas de v1.0 vêm de fonte secundária — Stellagent]; 150+ organizações, 22k stars em 09/04/2026; A2A em produção em Azure AI Foundry e Bedrock AgentCore; Interactions API (beta dez/2025) integrada ao ADK. **Não encontrei anúncio Google I/O 2026 específico de Agent Engine** — o post "What's new with Agents" recuperado é de 20/05/2025.
   - Microsoft: Agent Framework 1.0 GA (02/04/2026, AutoGen + Semantic Kernel); Agent Harness e Hosted Agents GA (Build jun/2026 → ago/2026); CodeAct/Hyperlight alpha; Durable Task extension preview; conectores Claude Agent SDK e Copilot SDK.
   - AWS: AgentCore Policy GA (03/03/2026), Evaluations GA (31/03/2026), Memory FGAC e episodic (ago/2026), managed harness; GovCloud (ago/2026).
   - Cloudflare: Project Think (15/04/2026, experimental), `keepAlive()` (mar/2026), Flue + hospedagem de harnesses (17/06/2026).
   - Kong: Agent Gateway 3.14 (14/04/2026), AI Gateway 2.0 GA (01/09/2026).
   - MCP: revisão 2026-07-28 — Tasks vira extensão standalone.

3. **Rumor/roadmap vs shipping — marcações explícitas:**
   - [RUMOR/secundária] "Anthropic lançou Managed Agents em 08/04/2026" e "self-hosted em 19/05/2026 no Code with Claude Londres" — coerente com o header `2026-04-01` e com os docs, mas não achei o post oficial de lançamento; tratar datas como "reportadas".
   - [RUMOR/secundária] Descrição de "grading layer" e componentes "Context Builder / Tool Router / Trace / Eval" do harness da Anthropic vêm de posts Medium/dev.to (luhuidev) — **não confirmados em docs oficiais**; não usar como fato.
   - [PAPER] arXiv 2604.11378 (Graph Harness) se autodeclara position paper sem implementação.
   - [PREVIEW] Dreams, MCP tunnels, CodeAct/Hyperlight, Project Think fibers, Durable Task extension (MS).
   - [SHIPPING/GA] Temporal×OpenAI Agents SDK, MAF 1.0 + Harness + Hosted Agents, AgentCore Policy/Evaluations, Kong 3.14/2.0, MCP Tasks extension (spec), Cloudflare Agents SDK, E2B/Modal/Vercel Sandbox.

4. **Sierra "constellation of models"** (03/12/2025; 15+ modelos por papel: retrieval/classificação, tool calling, long-context, tom, supervisores) e **Decagon "network of specialized models"** são arquitetura relevante para motor de resolução, mas o blog já cobre roteamento por intenção (`tutoriais/classificacao-de-intencao-llm-roteamento-de-agente`) e multi-agent (3 posts). Possível ângulo residual: "modelo supervisor" como papel distinto — não listado como técnica por ser adjacente demais.

5. **Hyper-τ-bench** (Sierra, 08/09/2026, "evaluating agents that build agents") é fresquíssimo mas pertence ao eixo de evals, não de runtime.

---

## Ranking do eixo

Critério: relevância para quem constrói agente de vendas/suporte em produção × frescor (peso para mar–set/2026) × ausência no blog.

| # | Técnica | Relevância | Frescor | Ausência no blog | Nota |
|---|---------|-----------|---------|------------------|------|
| 1 | **Durable execution como backbone do loop** (Temporal/Restate/Inngest/WDK/MS) | Altíssima — resolve crash, espera longa e idempotência de ações com efeito colateral | Alto (GA Temporal×OpenAI mar/2026; Restate mai/2026) | Alta — post existente só "guarda estado", não replay/complexity cliff; zero sobre PHP SDK | Tema-âncora do eixo; público Laravel tem Temporal PHP SDK e ninguém escreveu |
| 2 | **Agent gateway com identidade/custo por agente + A2A** (Kong 3.14/2.0, agentgateway, Sierra) | Alta — é onde vendas e suporte compartilham CRM sem se atropelar | Altíssimo (Kong 2.0 GA 01/09/2026) | Alta — post de MCP gateway não cobre identidade por agente nem A2A | Pareia bem com #7 |
| 3 | **Blueprint híbrido determinístico+agêntico com orçamento de iteração** (Stripe, Decagon AOP, papers) | Altíssima — é a forma como as empresas que realmente operam agentes estruturam o fluxo | Alto (Stripe fev/2026; papers abr–jun/2026) | Média-alta — plan-and-execute existe, mas o padrão "nó obrigatório + escopo fechado + 2 tentativas" não | Caso Stripe (1.300 PRs/semana) dá gancho forte |
| 4 | **Sessão event-log + harness stateless + sandbox descartável + credential proxy** | Alta — segurança estrutural contra prompt injection e recuperação por replay | Alto (MA beta abr/2026; Agency jul/2026; arXiv ago/2026) | Alta — harness está coberto, zonas de confiança e credential proxy não | Conecta com #1 e #6 |
| 5 | **Agentes ambientes / event-driven com HITL notify-question-review** | Alta — vendas proativa e suporte preventivo são o próximo produto | Alto (scheduled deployments jun/2026; Decagon mar/2026; arXiv jun/2026) | Média — cron existe (`tracking-247`), evento/CDC/inbox/outbound não | Ângulo "evento, não horário" precisa ficar explícito para não duplicar |
| 6 | **Sandbox microVM como fronteira + CodeAct em microVM** | Alta — qualquer agente que executa código gerado | Alto (MS alpha jun/2026; Cloudflare abr/jun 2026; Modal jun/2026) | Média — programmatic tool calling existe (2 posts); isolamento/egress/JIT credentials não | Cuidado para não repetir PTC; foco no *onde* executa |
| 7 | **Autorização de tool call por política fora do modelo** (AgentCore Policy/Cedar) | Alta — teto de desconto/reembolso é o caso de uso mais concreto em vendas/suporte | Médio-alto (GA 03/03/2026; Kong 2.0 set/2026) | Alta — guardrails existem, autorização por política não | Pode virar seção do post #2 ou post próprio com exemplo Cedar |
| 8 | **Harness × Runtime como camadas; runtimes hospedando harnesses alheios** | Média-alta — decisão de "o que eu escrevo, o que eu alugo" | Alto (Credal abr/2026; Cloudflare/Flue jun/2026; MAF GA ago/2026) | Média — 5 posts de harness; camada runtime não definida | Risco de parecer "mais um post de harness" — precisa ser sobre runtime |
| 9 | **Execução dividida: control plane do vendor, sandbox no cliente (work queue, MCP tunnels)** | Média-alta — decisivo para LGPD/residência e HIPAA/ZDR | Alto (beta mai/2026; memória em self-hosted ago/2026) | Alta — nada no acervo | Muito específico de Managed Agents; maturidade beta |
| 10 | **Tool call assíncrona com handle durável (MCP Tasks ext., background modes)** | Média — resolve timeouts reais, mas clientes ainda não suportam | Altíssimo (spec 28/07/2026) | Alta — 4 posts de MCP, nenhum sobre Tasks | Honestidade obrigatória: spec pronta, adoção atrasada |
| 11 | **Hibernação / actor por sessão / fibers** | Média — custo de compute ocioso é real em suporte massivo | Alto (Project Think abr/2026; Agency jul/2026) | Alta — nada sobre Durable Objects | Pode ser fundido em #1 ou #4 |
| 12 | **Consolidação de memória offline (dreams)** | Média — relevante para vendas de ciclo longo | Alto (research preview abr/2026) | Média-alta — memória tem 4 posts, consolidação batch não | Maturidade baixa (research preview); bom como "o que vem" |

**Recomendação de ordem de produção** (se for 1 post por técnica): 1 → 3 → 2 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12. Se for agrupar: (1+11) "durável e ocioso"; (2+7) "gateway + política"; (4+6+9) "zonas de confiança, sandbox e execução dividida"; (5+10) "agente acordado por evento e tool que demora".

**Ação imediata fora da pauta**: revisar `tutoriais/como-implementar-agent-builder-e-chatkit-da-openai-com-laravel` com aviso de descontinuação do Agent Builder (30/11/2026).
