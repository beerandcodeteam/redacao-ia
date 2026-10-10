# Pesquisa 05 — Confiabilidade, Evals, Segurança e Identidade de agentes em produção

Data da pesquisa: 12/09/2026. Janela priorizada: março–setembro/2026.
Método: 22 buscas web + ~30 fetches de fontes primárias (arXiv, blogs de engenharia Anthropic/Microsoft/Cloudflare/Okta, docs Google Cloud, spec MCP, OWASP, OpenTelemetry, IETF). O acervo do blog (acervo-slugs.txt, ~300 slugs) foi lido integralmente antes da pesquisa; cada técnica traz "Gap vs blog" checado contra ele.

Convenções: **shipping** = produto/spec publicado e utilizável; **roadmap/beta** = anunciado mas não GA; **paper** = arXiv sem evidência de uso em produção; **fonte secundária** = não consegui abrir o documento primário.

---

### 1. Evals de trajetória com user simulator e métrica pass^k

- **O que é**: Em vez de avaliar a resposta final, o eval roda o agente contra um simulador de usuário (um LLM com persona + cenário + critérios de sucesso) por N turnos, e a nota é dada sobre (a) o estado final do ambiente (banco de dados, CRM, ticket) e (b) a trajetória (quais tools, em que ordem, com quais argumentos). A métrica de confiabilidade é pass^k (probabilidade de acertar TODAS as k execuções), não pass@k (pelo menos uma). τ²-bench é a referência: domínios airline/retail/telecom/banking_knowledge, cada um com política escrita, tools, tarefas e simulador; em 2026 ganhou avaliação de voz full-duplex (APIs realtime da OpenAI/Gemini/xAI), domínio de RAG (banking_knowledge) e 75+ correções de tarefas.
- **Quem está usando/shipping**: Sierra (tau2-bench, MIT, GitHub atualizado em 2026); Anthropic recomendou explicitamente user simulators, grading de estado do ambiente e pass^k no post "Demystifying evals for AI agents" (09/01/2026). Papers 2026 derivados: τ-Banking, CRAB-Bench (jun/2026), T1-Bench (jun/2026), SAGE (simulador knowledge-grounded), "Beyond Cooperative Simulators" (mai/2026, personas não cooperativas). "Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents" (31/03/2026) mostra que ranking de capacidade e ranking de confiabilidade divergem em horizonte longo.
- **Maturidade**: early adopters → mainstream em labs; em times de produto ainda é minoria. Evidência: benchmark open-source maduro com domínios reais, recomendação oficial da Anthropic, múltiplos papers derivados em 6 meses.
- **Aplicação em agente de vendas / motor de resolução**: criar um "domínio τ²" próprio: política comercial (desconto máximo, quando escalar para humano), tools reais mockadas (CRM, tabela de preço, agenda), 50–200 tarefas com critério `evaluation_criteria.actions` (ex.: "deve chamar `create_deal` com `discount <= 10`" e "NÃO deve chamar `send_proposal` antes de `qualify_lead`"). Simulador de usuário com personas hostis (cliente que mente sobre orçamento, cliente que tenta prompt injection). Rodar k=5 e reportar pass^5 como gate de release.
- **Gap vs blog**: adjacente a `tutoriais/avaliacao-de-agentes-de-ia-evals-honestos`, `tutoriais/evals-para-agentes-de-ia-llm-as-a-judge`, `tutoriais/model-graders-...` e `tutoriais/llm-as-a-judge-avaliacao-automatizada-agente-ofertas`. Nenhum deles cobre simulador de usuário multi-turn, grading de estado do ambiente ou pass^k. Ângulo novo: "monte seu τ²-bench para o seu agente de vendas em Laravel: política + tools + simulador + pass^k".
- **Fontes**:
  - https://github.com/sierra-research/tau2-bench (README com updates 2026)
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (09/01/2026)
  - https://arxiv.org/abs/2603.29231 (31/03/2026)
  - https://arxiv.org/pdf/2606.01815 (CRAB-Bench, jun/2026); https://arxiv.org/pdf/2606.11070 (T1-Bench, jun/2026); https://arxiv.org/pdf/2605.12894 (mai/2026)

---

### 2. Replay de traces de produção como teste de regressão de trajetória (evals de tool-call em CI)

- **O que é**: Traces reais (span de agente → spans de LLM → spans de tool) são amostrados por estrato (intenção, capability), rotulados e congelados como golden dataset. No CI, cada PR roda camada 1 (asserções determinísticas sobre seleção de tool, schema dos argumentos, ordem, ausência de efeito colateral proibido), camada 2 (LLM-judge calibrado ≥85% de concordância com humanos sobre a trajetória completa, gate de regressão ~3% vs. baseline) e camada 3 (online, 5–10% do tráfego, judge assíncrono, alerta por queda em 24h). Traces que falham em produção voltam para o dataset offline.
- **Quem está usando/shipping**: framework em 3 níveis documentado por Kunal Ganglani (12/07/2026, atualizado 16/08/2026); Confident AI/DeepEval ("trace-based evals", tool-calling metrics, 2026); LangSmith/Arize Phoenix/Braintrust suportam replay de traces (citados pela Anthropic em jan/2026). OpenTelemetry `gen_ai.evaluation.result` é o carrier padrão do score (ver técnica 6).
- **Maturidade**: early adopters. Tooling existe; a prática de sampling estratificado + gate de regressão ainda é artesanal (fontes são blogs de praticantes e vendors, não spec).
- **Aplicação em agente de vendas / motor de resolução**: pipeline Laravel: job semanal amostra 20 traces por intenção do Langfuse/OTel → fila de revisão humana → grava em `eval_cases` com `expected_tool_sequence` e `forbidden_side_effects` → GitHub Actions roda o agente em modo dry-run (tools mockadas a partir do trace) e compara. Bloqueia merge se `create_deal` for chamado sem `qualify_lead` ou se o argumento `discount` sair da alçada.
- **Gap vs blog**: adjacente a `tutoriais/pipeline-eval-continuo-prompts-producao` (foca em prompts, não em trajetória/tools) e `tutoriais/pipeline-revisao-pr-github-actions-claude` (revisa código, não agente). Ângulo novo: "trace de produção vira teste: asserções de tool-call (argumento, ordem, efeito colateral) e gate de regressão no CI".
- **Fontes**:
  - https://www.kunalganglani.com/blog/evaluate-ai-agents-production (12/07/2026)
  - https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide (2026)
  - https://www.confident-ai.com/knowledge-base/compare/best-ci-cd-tools-testing-ai-agents-before-production-2026
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (ferramentas citadas)

---

### 3. Red-teaming automatizado orquestrado por agente (attacker-LLM contra o seu agente)

- **O que é**: Um LLM atacante recebe um objetivo em linguagem natural ("faça o agente enviar a lista de leads para um e-mail externo"), escolhe técnicas, compõe transformações, executa multi-turn contra o alvo (inclusive via tools/MCP) e gera findings estruturados mapeados a taxonomias (OWASP ASI). Diferente de uma suíte estática de prompts adversariais: é adaptativo, explora a superfície de tools e roda em horas. AgentDojo (poisoning de recursos externos), PI-Hunter (localização de injeções, jun/2026) e o plugin MCP do Promptfoo são os blocos.
- **Quem está usando/shipping**: OpenAI anunciou a aquisição da Promptfoo em 09/03/2026 (350k devs, 25% da Fortune 500; integração ao OpenAI Frontier; compromisso de manter o open source). Microsoft AI Red Teaming Agent (PyRIT multi-turn no Azure AI Foundry). Paper "Redefining AI Red Teaming in the Agentic Era: From Weeks to Hours" (mai/2026). Promptfoo tem doc dedicada ao OWASP Agentic Top 10.
- **Maturidade**: early adopters → mainstream em enterprise (aquisição por lab de fronteira é o sinal mais forte). Ferramentas OSS disponíveis hoje.
- **Aplicação em agente de vendas / motor de resolução**: job noturno com Promptfoo (`redteam` + plugin MCP) contra o ambiente de staging do agente, com objetivos específicos do domínio: exfiltrar CRM via tool de e-mail, obter desconto acima da alçada, fazer o agente executar instrução vinda do campo "observações" do lead (vetor ForcedLeak/PipeLeak). Findings mapeados a ASI01/ASI02/ASI03 viram issues.
- **Gap vs blog**: adjacente a `tutoriais/prompts-resilientes-evals-adversariais-edge-cases` (casos adversariais estáticos) e aos 2 posts de prompt injection. Ângulo novo: atacante autônomo + superfície de tools/MCP + mapeamento OWASP ASI; e a notícia "OpenAI comprou a Promptfoo — o que muda para quem usa".
- **Fontes**:
  - https://openai.com/index/openai-to-acquire-promptfoo/ (09/03/2026); https://www.promptfoo.dev/blog/promptfoo-joining-openai/
  - https://techcrunch.com/2026/03/09/openai-acquires-promptfoo-to-secure-its-ai-agents/
  - https://www.promptfoo.dev/docs/red-team/owasp-agentic-ai/
  - https://arxiv.org/pdf/2606.12737 (PI-Hunter, jun/2026); https://arxiv.org/pdf/2605.04019 (mai/2026)

---

### 4. Agente como principal: identidade própria + On-Behalf-Of token exchange

- **O que é**: O agente deixa de usar a credencial do usuário ou uma service account compartilhada e passa a ter identidade própria no IdP (registrado, com dono humano, desativável). Quando age por um usuário, faz token exchange (RFC 8693) e o token resultante carrega `sub` = usuário e `act` = agente (cadeia de delegação auditável), com audience do serviço de destino e escopo por tool. Credenciais de terceiros (Google, HubSpot, Pipedrive) ficam num Token Vault; o agente nunca vê o refresh token. Em infraestrutura, a identidade do agente é SPIFFE (X.509 de 24h rotacionado) e vira principal direto em políticas IAM.
- **Quem está usando/shipping**:
  - Auth0 (Okta), 21/05/2026: Auth for MCP (GA), On-Behalf-Of Token Exchange (GA), Token Vault com Organizations (EA jun/2026), **Agent as Principal** (developer preview jun/2026), FGA Permissions Index (preview).
  - Okta Agent SSO, 24/08/2026 (GA): agente compatível com Cross App Access é registrado como identidade de primeira classe no Universal Directory; Okta for AI Agents (GA mai/2026) com dono humano e kill switch.
  - Google Cloud Agent Identity: SPIFFE ID `spiffe://agents.global.proj-N.system.id.goog/resources/...`, cert 24h, principal em IAM, suportado em Agent Runtime, Gemini Enterprise e Cloud Run; audit log distingue "como si mesmo" vs "em nome do usuário" (doc atualizada 11/09/2026; estágio preview/GA não declarado na página).
  - Microsoft Entra Agent ID citado no blog de segurança da Microsoft (30/06/2026).
  - IETF: draft-oauth-ai-agents-on-behalf-of-user-02 (WSO2, ago/2025, individual draft — **não adotado por WG**, expirado fev/2026): parâmetros `requested_actor`/`actor_token` e consentimento front-channel, complementar ao RFC 8693.
  - Stacklok (04/08/2026): modelo em 3 camadas SPIFFE/SPIRE + ReBAC (OpenFGA/SpiceDB) + gateway MCP.
- **Maturidade**: shipping nos 3 grandes IdPs/clouds em 2026; o padrão de "agente como principal" está em preview na Auth0 e GA na Okta/Google. O draft IETF é roadmap. Early adopters em empresas; mainstream até 2027 é projeção, não fato.
- **Aplicação em agente de vendas / motor de resolução**: o agente `sales-agent@empresa` é um principal; ao atender o vendedor Lucas, troca o token do Lucas por um token `sub=lucas, act=sales-agent, aud=crm-api, scope=deals:read deals:write:max_discount_10`. O CRM loga os dois. Token Vault guarda o OAuth do Pipedrive por organização (multi-tenant). Kill switch revoga o agente sem tocar no usuário. Em Laravel: middleware que valida `act` e `aud` antes de cada handler de tool.
- **Gap vs blog**: adjacente a `tutoriais/mcp-em-producao-oauth-schema-gateway` (OAuth no servidor MCP) e `noticias/1password-for-claude` (segredos). Nenhum post trata o agente como identidade separada, cadeia `act`, Token Vault, SPIFFE ou kill switch. Ângulo novo: "seu agente precisa de CPF próprio: agente como principal, OBO e o fim da service account compartilhada".
- **Fontes**:
  - https://www.okta.com/newsroom/articles/auth0-may-2026-product-innovations/ (21/05/2026)
  - https://www.okta.com/newsroom/press-releases/okta-brings-first-class-identity-to-ai-agents-with-agent-sso/ (24/08/2026)
  - https://docs.cloud.google.com/iam/docs/agent-identity-overview (atualizado 11/09/2026)
  - https://www.ietf.org/archive/id/draft-oauth-ai-agents-on-behalf-of-user-02.txt (26/08/2025)
  - https://stacklok.com/blog/agentic-identity-explained-how-to-apply-spiffe-and-relationship-based-authorization-to-ai-agents-in-2026/ (04/08/2026)
  - https://mojoauth.com/blog/oauth-2-0-token-exchange-rfc-8693-for-agent-delegation-a-worked-example (exemplo prático RFC 8693)

---

### 5. MCP 2026-07-28: autorização endurecida, core stateless e Enterprise-Managed Authorization

- **O que é**: Maior revisão da spec desde o lançamento. Autorização: servidor MCP é formalmente OAuth 2.1 resource server; MUST implementar Protected Resource Metadata (RFC 9728); cliente MUST usar Resource Indicators (RFC 8707) para amarrar o token a um servidor específico (anti "token meant for another server"); validação de `iss` obrigatória (RFC 9207, contra mix-up); `application_type` OIDC na registração; credenciais vinculadas ao issuer; regras de acúmulo de escopo/step-up e descoberta `.well-known`. Proibição de passthrough de token → token exchange vira obrigatório em cada hop. Core stateless (sem `initialize`/`Mcp-Session-Id`, metadata em `_meta`), Tasks vira extensão opt-in com handles (`tasks/get|update|cancel`), **Enterprise-Managed Authorization (EMA)** é extensão nomeada para controle central por time de identidade. Roots, Sampling e Logging entram em deprecação (12 meses).
- **Quem está usando/shipping**: spec final publicada 28/07/2026 (RC travado 21/05/2026). GitHub MCP Server anunciou suporte em 23/07/2026. WorkOS, Descope, Cerbos, Aembit publicaram guias de migração (jul–ago/2026). Cerbos aponta que escopos OAuth não resolvem autorização por argumento de tool ("what's still missing").
- **Maturidade**: shipping (spec) / early adopters (servidores migrados). Evidência: changelog oficial + adoção pelo GitHub.
- **Aplicação em agente de vendas / motor de resolução**: se o CRM é exposto como servidor MCP: publicar `/.well-known/oauth-protected-resource`, exigir `resource=` do cliente, validar `iss`/`aud` em cada request, trocar token (RFC 8693) antes de chamar a API do CRM, mover operações longas (gerar proposta em PDF) para Tasks. Com EMA, o time de TI controla quais agentes falam com quais servidores sem tocar no código.
- **Gap vs blog**: adjacente a `tutoriais/mcp-em-producao-oauth-schema-gateway`, `tutoriais/como-criar-mcp-server`, `tutoriais/como-criar-um-servidor-mcp-do-zero`, `noticias/o-que-e-mcp`. Nenhum cobre a spec 2026-07-28. Ângulo novo: "o que quebra no seu servidor MCP com a spec de julho/2026 (RFC 9728/8707/9207, stateless, Tasks) e como migrar em PHP".
- **Fontes**:
  - https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
  - https://github.blog/changelog/2026-07-23-github-mcp-server-supports-the-next-mcp-specification/
  - https://workos.com/blog/mcp-2026-spec-agent-authentication
  - https://www.cerbos.dev/blog/mcp-authorization-standards
  - https://stacktr.ee/blog/mcp-2026-spec-changes (lista de breaking changes)

---

### 6. OpenTelemetry GenAI semantic conventions para agentes + agent SLOs e custo por trajetória

- **O que é**: Vocabulário vendor-neutral: span `invoke_agent` (raiz) → spans `chat` (cada chamada LLM, com `gen_ai.request.model`, `gen_ai.usage.input_tokens/output_tokens`, `gen_ai.response.finish_reasons`) → spans `execute_tool` (`gen_ai.tool.name`, `gen_ai.tool.type`, `gen_ai.tool.call.id`, `gen_ai.tool.call.arguments/result` opt-in por sensibilidade), mais `create_agent`, `gen_ai.conversation.id`, eventos de conteúdo e o evento `gen_ai.evaluation.result` (score + label + explicação do avaliador). Há documento separado para MCP. Com isso, custo por trajetória = soma dos tokens dos spans `chat` filhos de um `invoke_agent`; e SLOs de agente deixam de ser só latência/erro: taxa de sucesso de tool-call, score de judge, taxa de disparo de guardrail, custo por interação resolvida, cada um com seu error budget.
- **Quem está usando/shipping**: OTel moveu as convenções GenAI para repositório próprio (criado 05/05/2026, migração concluída em junho) para iterar independente; **todos os documentos continuam `Status: Development`**, sem release taggeado (verificado em commit de 30/07/2026; ainda sem release em 21/08/2026). Blog oficial do OTel (2026) mostra traces de Claude Code (beta), Codex e Copilot. Datadog anunciou suporte nativo às convenções. Agent SLOs: apenas blogs de praticantes/vendors (FutureAGI, Velsof, BuildMVPFast), sem spec.
- **Maturidade**: early adopters (convenções em uso real por vendors e CLIs, mas marcadas Development — campos podem mudar). Agent SLOs: experimental/prática emergente.
- **Aplicação em agente de vendas / motor de resolução**: instrumentar o agente Laravel com spans `invoke_agent`/`execute_tool` (SDK OTel PHP), exportar para Langfuse/Grafana/Datadog; dashboards por `gen_ai.conversation.id`; SLO "≥97% de `execute_tool` sem erro", "custo por deal qualificado ≤ X", "score do judge ≥ 0,85"; alertas por burn rate. Eval offline grava `gen_ai.evaluation.result` no mesmo trace.
- **Gap vs blog**: adjacente a `tutoriais/observabilidade-agentes-ia-langsmith-langfuse-helicone` (ferramentas) e `tutoriais/observabilidade-em-sistemas-modernos` (genérico), `tutoriais/filas-laravel-2026-horizon-redis-tracing`. Nenhum cobre o padrão OTel GenAI, os nomes de span/atributo, o evento de avaliação, nem SLOs específicos de agente. Ângulo novo: "pare de depender do vendor: OTel GenAI para agentes (spans, custo por trajetória, evento de eval) + 5 SLOs que só agente tem".
- **Fontes**:
  - https://opentelemetry.io/blog/2026/genai-observability/
  - https://github.com/open-telemetry/semantic-conventions-genai ; https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-events.md
  - https://hidekazu-konishi.com/entry/opentelemetry_genai_semantic_conventions_guide.html (status por documento, verificado 31/07/2026)
  - https://www.datadoghq.com/blog/llm-otel-semantic-convention/
  - https://futureagi.com/blog/ai-agent-reliability-metrics-2026/ ; https://www.buildmvpfast.com/blog/ai-agent-error-budget-sre-reliability-autonomous-2026 (secundárias)

---

### 7. Autorização determinística pré-ação e risk tiers por tool (fora do modelo)

- **O que é**: Um hook síncrono fora do LLM intercepta cada tool call antes de executar, avalia argumentos contra política declarativa (deny-by-default), registra decisão assinada e só então libera. Complementa com classificação de risco por tool (read-only / minimal / contained write / critical) que decide: passa, enriquece com atribuição humano+agente e audita, ou bloqueia antes do handler. Pesquisa de ago/2026 sobre "unidade de verificação" mostra que revisar 1–2 ações por vez maximiza a discriminação do monitor; janelas maiores só aumentam rejeição (falsos positivos), o que empurra times a desligar a supervisão. Dado de produto: em Claude Code, usuários aceitavam 93% dos prompts de permissão e prestavam menos atenção quanto mais prompts viam (fatiga de aprovação).
- **Quem está usando/shipping**: Cloudflare WriteGuard (private beta, 05/08/2026; InfoQ 18/08/2026): proxy atrás do MCP portal, risk tiers, atribuição, audit events scrubbed. Paper "Before the Tool Call" / Open Agent Passport (21/03/2026, Apache 2.0): 0% de sucesso em 879 tentativas de engenharia social sob política restritiva vs 74,6% sob permissiva; mediana de 53 ms. Oracle (blog AI & Data Science, 2026): verificação formal de política como checkpoint determinístico. SAP: padrão Plan-Validate-Execute. "More Rejective, Not More Discriminative" (25/08/2026). Anthropic "Claude Code auto mode" (engineering blog) e "How we contain Claude across products" (28/05/2026): sandboxes (gVisor, Seatbelt, Bubblewrap, VM) e egress control com a tese de "blast radius = probabilidade × dano".
- **Maturidade**: early adopters (WriteGuard em beta; OAP é paper + spec OSS; sandboxing da Anthropic é shipping interno). Conceito consolidado, produtos ainda imaturos.
- **Aplicação em agente de vendas / motor de resolução**: tabela `tool_policies` em Laravel: `send_email` = contained write (exige `to` em domínio do lead e anexa atribuição), `apply_discount` = critical se `> 10%` (bloqueia e abre aprovação humana), `read_deal` = read-only (passa). Middleware roda antes do handler; decisão vai para o trace OTel. Aprovação humana só para critical, em lotes de 1–2 ações, para evitar fatiga.
- **Gap vs blog**: adjacente a `tutoriais/guardrails-para-agentes-de-ia` (guardrails de I/O, não policy engine por tool), `noticias/claude-code-auto-mode-padrao` (notícia), `noticias/4-niveis-autonomia-agentic-code`. Ângulo novo: "policy engine determinística antes do tool call: risk tiers, deny-by-default, e por que aprovar tudo é igual a não aprovar nada (dados de fatiga)".
- **Fontes**:
  - https://blog.cloudflare.com/mcp-portal-writeguard-private-beta/ (05/08/2026); https://www.infoq.com/news/2026/08/cloudflare-writeguard-mcp-safety/ (18/08/2026)
  - https://arxiv.org/abs/2603.20953 (21/03/2026)
  - https://arxiv.org/abs/2608.23941 (25/08/2026)
  - https://www.anthropic.com/engineering/how-we-contain-claude (28/05/2026); https://anthropic.com/engineering/claude-code-auto-mode
  - https://blogs.oracle.com/ai-and-datascience/from-ai-assistance-to-governed-ai-action-formal-policy-verification-for-agentic-systems
  - https://community.sap.com/t5/security-and-compliance-blog-posts/plan-then-execute-an-architectural-pattern-for-responsible-agentic-ai/ba-p/14239753

---

### 8. Execução reversível: saga/compensação, checkpoint e idempotência em ações de agente

- **O que é**: Cada tool com efeito colateral declara (a) chave de idempotência, (b) ação compensatória (ou "irreversível" explícito: e-mail enviado, cobrança capturada, webhook entregue) e (c) checkpoint de estado pré-ação. O orquestrador trata a trajetória como saga: se um passo posterior falha ou a verificação pós-ação detecta divergência, executa a cadeia de compensação em ordem inversa. Para irreversíveis, a regra é rehearsal em sandbox (dry-run) + aprovação humana antes, não rollback depois. Arquiteturas como Parallax (abr/2026) colocam "reversible execution" como princípio: captura de estado antes de cada ação para rollback se a validação falhar. DeltaBox (mai/2026) traz checkpoint/rollback de sandbox em milissegundos para agentes stateful.
- **Quem está usando/shipping**: conceito vem de durable execution (Temporal/Restate) e está sendo redescoberto por times de agentes (Medium, mai–jun/2026; "Agent Rollbacks Need Rehearsals", 2026; série "Enterprise Agent Control Plane" part 4, 25/07/2026). Claude Managed Agents (beta pública, abr/2026) oferece checkpointing e sandbox. Papers: Parallax (14/04/2026), DeltaBox (mai/2026). **Não encontrei produto GA que implemente saga para tool calls de agente de forma genérica** — é padrão de arquitetura, não feature.
- **Maturidade**: early adopters (padrão conhecido em sistemas distribuídos; aplicação a agentes é 2026 e majoritariamente em blogs de praticantes e papers).
- **Aplicação em agente de vendas / motor de resolução**: `create_deal` → compensação `delete_deal(id)`; `schedule_meeting` → `cancel_meeting`; `send_proposal` = irreversível → dry-run gera o PDF e mostra ao vendedor antes; `apply_credit` no motor de resolução → `reverse_credit`. Chave de idempotência = hash(conversation_id, step, args) para sobreviver a retries da fila. Implementável com jobs encadeados no Laravel (Bus::chain + catch) ou Temporal.
- **Gap vs blog**: não há post sobre compensação/rollback/idempotência em ações de agente. `tutoriais/agente-de-ia-loop-infinito` e `noticias/agente-ia-estado-entre-execucoes` tocam estado/loops, não reversibilidade. Ângulo novo: "toda tool com efeito colateral precisa de três coisas: idempotency key, compensação e dry-run — saga para agentes em Laravel".
- **Fontes**:
  - https://arxiv.org/abs/2604.12986 (Parallax, 14/04/2026)
  - https://arxiv.org/pdf/2605.22781 (DeltaBox, mai/2026)
  - https://digitalthoughtdisruption.com/2026/07/25/execute-verify-rollback-agent-actions/ (25/07/2026)
  - https://nittikkin.medium.com/agent-workflows-are-rediscovering-durable-execution-be110661ed8c (mai/2026); https://medium.com/@rahulponnusamy/beyond-try-except-implementing-the-saga-pattern-in-2026-ai-agents-92dcb7c0bf48 (jun/2026)
  - https://www.helpnetsecurity.com/2026/04/09/claude-managed-agents-bring-execution-and-control-to-ai-agent-workflows/ (09/04/2026)

---

### 9. Tool poisoning e rug pull em MCP: o canal de metadados como vetor, e as defesas

- **O que é**: A descrição de uma tool MCP tem a mesma autoridade que o system prompt, mas ninguém a lê. Tool poisoning = instruções maliciosas na descrição no registro; rug pull = servidor muda a descrição depois de aprovada, sem re-aprovação (CVE-2025-54136, Cursor, CVSS 8.8); tool shadowing e cross-server = um servidor malicioso altera o comportamento de tools de outro. Em 2026 virou técnica de exfiltração em produção: Microsoft observou atacantes atualizando silenciosamente descrições em servidores MCP de terceiros usados por agentes do Copilot Studio em times financeiros, que passaram a coletar e exfiltrar resumos de faturas. Defesas: allowlist de publishers/tool IDs, tratar descrição como system prompt sob change review (diff + hash/pin de versão, re-aprovação em mudança), scanning de metadados (Prompt Shields), DLP nos parâmetros, egress allowlist, HITL para tools de escrita, identidade própria para o agente, telemetria centralizada. ETDI (paper 2025) propõe definições de tool assinadas via OAuth.
- **Quem está usando/shipping**: Microsoft Security Blog (30/06/2026) e The Hacker News (jun/2026); CSA research notes (01/07 e 11/07/2026); Cloudflare "How Cloudflare detects MCP traffic" (ago/2026, detecção de shadow MCP). OWASP ASI04 (supply chain) e ASI02 (tool misuse). MCPTox benchmark (ago/2025) mediu ~5,5% de tools envenenadas em 1.899 servidores. **Fonte secundária**: advisory conjunto NSA/DoD de 02/06/2026 citando tool poisoning/rug pull — reportado por ITECS e Practical DevSecOps; não localizei o PDF primário, tratar como "reportado".
- **Maturidade**: ameaça mainstream (incidentes reais + guidance de Microsoft/CSA/Cloudflare); defesas em early adopters (WriteGuard beta, ETDI paper, allowlists manuais).
- **Aplicação em agente de vendas / motor de resolução**: todo servidor MCP de terceiro (CRM, e-mail, calendário) passa por gateway próprio que guarda hash das descrições aprovadas; se o `tools/list` retornar descrição diferente, bloqueia e abre revisão. Tools de envio externo (e-mail, webhook) só com destino em allowlist. Agente usa identidade própria (técnica 4) para que a exfiltração apareça no audit log como ação do agente.
- **Gap vs blog**: adjacente a `noticias/prompt-injection-o-que-e-ataques-2026`, `tutoriais/prompt-injection-agente-site-raspado-system-prompt` (injeção via conteúdo raspado) e `tutoriais/mcp-em-producao-oauth-schema-gateway` (schema/gateway, sem poisoning). Ângulo novo: "a descrição da tool é o seu system prompt invisível: tool poisoning, rug pull e o incidente Copilot Studio de junho/2026 — com checklist de pin/hash".
- **Fontes**:
  - https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/ (30/06/2026)
  - https://thehackernews.com/2026/06/microsoft-warns-poisoned-mcp-tool.html
  - https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-tool-description-poisoning-20260711-cs/ (11/07/2026); https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-tool-poisoning-auto-execution-20260701/
  - https://blog.cloudflare.com/mcp-security-updates/ (ago/2026)
  - https://arxiv.org/pdf/2508.14925 (MCPTox); https://arxiv.org/pdf/2506.01333 (ETDI); https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks (origem do termo, 2025)
  - https://itecsonline.com/post/mcp-tool-poisoning-enterprise-ai-agent-security-2026 (secundária, NSA/DoD)

---

### 10. Memory poisoning: autoridade de memória vinculada à origem (origin-bound)

- **O que é**: Agente com memória persistente pode ser envenenado por (a) interação query-only (MINJA), (b) página web que o agente visita durante operação normal (eTAMP), ou (c) "lavagem": conteúdo não confiável vira confiável ao passar pela sumarização do próprio agente, por output de tool confiável que ecoa o atacante, ou por corroboração fabricada (vários "fontes" repetindo). Defesa proposta: TMA-NM (jun/2026) — controle de fluxo de informação não-maleável: a autoridade de uma memória é ligada à origem verificada no momento da escrita (write-time origin binding), não ao conteúdo nem ao histórico de derivação; gates de corroboração resistentes a Sybil; modelo formal em TLA+. Resultado: 0% de sucesso de ataque em 8 modelos, enquanto defesas existentes falharam até 68% sob lavagem. A-MemGuard propõe detecção por consenso na recuperação.
- **Quem está usando/shipping**: papers (jan/2026 arXiv 2601.05504; jun/2026 2606.04329 e 2606.24322; jul/2026 2607.06595; survey abr/2026 2604.16548; benchmark AgentLAB fev/2026). OWASP ASI06 "Memory & Context Poisoning" (dez/2025) formaliza o risco. **Nenhum produto shipping com origin-bound memory encontrado**; mem0/Zep não anunciaram.
- **Maturidade**: experimental (pesquisa ativa, ameaça reconhecida por OWASP, defesa sem produto).
- **Aplicação em agente de vendas / motor de resolução**: a memória do cliente (pgvector/mem0) ganha coluna `origin` (usuário autenticado / CRM / e-mail recebido / web) e `trust_level`; escrita a partir de e-mail/web nunca promove a "instrução"; sumarização preserva a origem mínima dos insumos; fatos que mudam política (ex.: "este cliente tem desconto aprovado de 30%") só podem ter origem CRM/humano. Motor de resolução: "observações" de ticket são dados, nunca memória de política.
- **Gap vs blog**: adjacente a `tutoriais/memoria-de-agente-de-ia`, `tutoriais/memoria-agente-assistente-compras`, `tutoriais/pgvector-postgres-memoria-do-seu-agente`, `tutoriais/trust-layer-agente-reputacao-fonte` (reputação de fonte para RAG, não para escrita em memória). Ângulo novo: "quem pode escrever na memória do seu agente? memory poisoning, lavagem por sumarização e o esquema origin-bound".
- **Fontes**:
  - https://arxiv.org/abs/2606.24322 (23/06/2026)
  - https://arxiv.org/pdf/2606.04329 (jun/2026); https://arxiv.org/abs/2601.05504 (jan/2026); https://arxiv.org/html/2607.06595v1 (jul/2026)
  - https://arxiv.org/pdf/2604.16548 (survey, abr/2026); https://arxiv.org/pdf/2602.16901 (AgentLAB, fev/2026)
  - https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ (ASI06)

---

### 11. Defesas arquiteturais contra injection: CaMeL, NOVA e Parallax (separar quem pensa de quem age)

- **O que é**: Em vez de filtrar prompts, a arquitetura garante integridade de fluxo de controle. CaMeL (Google DeepMind, 2025): LLM privilegiado extrai um programa (control flow) da query confiável; LLM em quarentena processa dados não confiáveis sem tools; interpretador customizado rastreia capabilities (proveniência) de cada valor e aplica política antes de cada tool call — dados não confiáveis nunca alteram o fluxo. NOVA / "CaMeLs Can Use Computers Too" (jan/2026, rev. jun/2026): estende a agentes de computer-use com plano ramificado single-shot antes da execução e modelo de percepção que só resolve valores (coordenadas); vulnerável a "branch steering". Parallax (abr/2026): separação cognitivo-executiva, validador independente multi-tier entre raciocínio e execução, labels de sensibilidade propagados, execução reversível; avaliação "assume-compromise" (o agente já está comprometido) — OpenParallax (Go) bloqueou 98,9% de 280 casos, zero falsos positivos.
- **Quem está usando/shipping**: papers (CaMeL está no syllabus de segurança do MIT 6.5660/2026; NOVA e Parallax são arXiv 2026 com implementação de referência). **Nenhum framework mainstream (LangGraph, Agents SDK, Claude Agent SDK) implementa CaMeL nativamente** — o que existe em produto são aproximações: WriteGuard/OAP (técnica 7), dual-LLM manual.
- **Maturidade**: experimental/early adopters (conceito influente, adoção por reimplementação parcial).
- **Aplicação em agente de vendas / motor de resolução**: versão pragmática: (1) LLM "planner" só vê a instrução do vendedor e devolve um plano estruturado (JSON de tool calls com placeholders); (2) LLM "quarantined" lê e-mail/lead/ticket e só pode retornar dados tipados (nunca tool calls); (3) código PHP determinístico executa o plano, com taint: qualquer argumento derivado de dado não confiável não pode ir para `to` de e-mail ou para `discount`. Combina com structured output do blog.
- **Gap vs blog**: adjacente aos 2 posts de prompt injection e a `tutoriais/json-que-nao-quebra-structured-output-llm`, `tutoriais/plan-and-execute-pattern-cortou-90-custo-agente` (plan-and-execute por custo, não por segurança). Ângulo novo: "prompt injection não se resolve com prompt: dual-LLM + taint tracking (CaMeL/Parallax) em um agente Laravel".
- **Fontes**:
  - https://arxiv.org/abs/2503.18813 (CaMeL); https://css.csail.mit.edu/6.5660/2026/readings/camel.pdf
  - https://arxiv.org/abs/2601.09923 (NOVA, 14/01/2026, rev. 04/06/2026)
  - https://arxiv.org/abs/2604.12986 (Parallax, 14/04/2026)
  - https://arxiv.org/pdf/2603.11088 (survey ataque/defesa agentic, mar/2026)

---

### 12. Controle de custo/latência em runtime: speculative tool calling, cascades e circuit breaker de orçamento

- **O que é**: Três mecanismos de runtime (não de pricing): (a) **Speculative tool calling / async I/O** — o agente dispara tool calls prováveis antes de ter a informação completa do usuário e continua raciocinando enquanto aguarda I/O; 1,3–1,7× de speedup em modelos cloud e 1,6–2,2× em modelos edge de 3B (UC Berkeley, mai/2026); "Cost-Aware Speculative Execution" (jun/2026) modela quando especular vale o custo; SPORK (jul/2026) prediz a próxima tool call antes do decode terminar. Risco: especular tools com efeito colateral — exige dry-run/idempotência (técnica 8); "Ghost Tool Calls" (jun/2026) trata privacidade de chamadas especulativas. (b) **Cascades/routing** — pequeno→grande por confiança; paper Brick (jun/2026) argumenta que cascade é estruturalmente desperdiçador em agentes porque 1 request vira N chamadas. (c) **Orçamento com circuit breaker** — token budget por tarefa/por passo/por tool, detector de loop, disparo por velocidade de gasto (tokens/min), pausa antes da próxima chamada; relatos de 2026 de agentes em loop queimando dezenas de milhares de dólares numa noite; Cloudflare AI Gateway (identity-aware, open beta 05/08/2026) dá atribuição de gasto por identidade e budgets; Wallets (04/08/2026) dá allowance por agente.
- **Quem está usando/shipping**: speculative = papers (UC Berkeley e outros, mai–jul/2026), sem produto GA; budgets/circuit breaker = prática de campo (blogs de praticantes 2026) + gateways (Cloudflare AI Gateway, Portkey, LiteLLM); routing = mainstream via OpenRouter/gateways.
- **Maturidade**: speculative tool calling experimental; budget circuit breaker early adopters → mainstream; routing mainstream.
- **Aplicação em agente de vendas / motor de resolução**: budget por conversa (ex.: 150k tokens) e por tarefa delegada a subagente; contador em Redis; breaker dispara se >30k tokens/min ou se a mesma tool for chamada 3× com os mesmos argumentos (loop); especulação só em tools read-only (buscar preço, buscar histórico) enquanto o usuário digita; roteamento Haiku→Sonnet por classificação de intenção já existente no blog.
- **Gap vs blog**: adjacente a `tutoriais/reduzir-custo-api-de-ia`, `tutoriais/cortando-custo-em-80-prompt-caching-batch-...`, `tutoriais/quanto-custa-agente-ia-producao-conta-tokens`, `noticias/custo-agente-ia-producao-2026-planilha-tco`, `noticias/plan-and-execute-pattern-cortou-90-custo-agente`, `tutoriais/agente-de-ia-loop-infinito`, `tutoriais/classificacao-de-intencao-llm-roteamento-de-agente`. Todos tratam de preço/arquitetura; nenhum de controle em runtime (breaker, budget por tarefa) nem de speculative tool calling. Ângulo novo: "circuit breaker de tokens: orçamento por tarefa, detector de loop e kill switch em Laravel" e, separado, "speculative tool calling: o agente que chama a tool antes de você terminar a frase".
- **Fontes**:
  - https://arxiv.org/abs/2605.13360 (13/05/2026); https://arxiv.org/abs/2606.07846 (jun/2026); https://arxiv.org/pdf/2607.03333 (SPORK, jul/2026); https://arxiv.org/pdf/2606.02483 (Ghost Tool Calls); https://arxiv.org/pdf/2606.13241 (Brick)
  - https://agnt.one/blog/cloudflare-agents-week-august-2026 (AI Gateway identity-aware, Wallets, ago/2026)
  - https://www.getreadyforagents.com/blog/agent-cost-runaway-detection-token-enforcement-production/ ; https://clord.dev/blog/agent-spend-needs-circuit-breakers-2026/ ; https://auxot.com/blog/agent-cost-circuit-breakers (secundárias, praticantes)

---

### 13. Governança 2026: Digital Omnibus adiou o alto risco, Art. 12 exige logs automáticos, e OWASP lançou o Agent Control Standard

- **O que é**: (a) **EU AI Act**: o Digital Omnibus on AI teve acordo de trílogo em 07/05/2026, aprovação do Parlamento em 16/06, adoção do Conselho em 29/06 e — segundo sumários de escritórios (A&O Shearman, Lexology) — publicação no Jornal Oficial em 24/07/2026 com entrada em vigor em 27/07/2026. Efeito: obrigações de alto risco Anexo III passam de 02/08/2026 para **02/12/2027**; Anexo I para 02/08/2028. Continuam em 02/08/2026 as obrigações de transparência do Art. 50 (conteúdo gerado por IA). Para agentes em uso de alto risco: Art. 12 exige registro automático de eventos durante toda a vida do sistema; Art. 13 exige documentação de como o deployer interpreta os logs; Arts. 19/26 retenção mínima de 6 meses. O ponto técnico levantado em abr/2026: logs de aplicação em infra controlada pelo próprio deployer não são à prova de adulteração — evidência fraca em auditoria. (b) **OWASP**: Top 10 for Agentic Applications (09/12/2025; ASI01 Goal Hijack … ASI10) e, em **01/09/2026**, o **Agent Control Standard (ACS)**: agentes devem ser inspecionáveis, rastreáveis, instrumentáveis e controláveis em runtime; define como plataformas expõem hooks de middleware e políticas declarativas portáveis entre frameworks. Também em set/2026: LLM Top 10 2026.
- **Quem está usando/shipping**: lei publicada (UE); OWASP ACS publicado há 11 dias (adoção ainda zero, é o momento de news-jacking); Auth0 publicou "lessons from OWASP Agentic Top 10"; Promptfoo/DeepTeam mapeiam testes ao Top 10.
- **Maturidade**: AI Act = mainstream (lei); ACS = experimental (recém-publicado).
- **Aplicação em agente de vendas / motor de resolução**: agente de vendas B2B raramente é Anexo III; motor de resolução que decide crédito/elegibilidade pode ser. Independente disso: trace OTel (técnica 6) com hash encadeado ou WORM storage (S3 Object Lock/OCI retention) cobre Art. 12 com integridade; retenção ≥ 6 meses; explicação da decisão = trajetória + política aplicada (técnica 7). Mapear controles do sistema para ASI01–ASI10 e ACS como checklist de due diligence para clientes.
- **Gap vs blog**: adjacente a `tutoriais/compliance-eu-ai-act-nist-rmf-checklist-18-itens-brasil` e `tutoriais/adocao-segura-ia-empresa-eu-ai-act-nist-rmf` (ambos anteriores ao Omnibus; não cobrem OWASP Agentic/ACS). Ângulo novo: (1) notícia "o prazo de alto risco do AI Act mudou para dezembro/2027 — o que NÃO mudou para quem tem agente" e (2) "OWASP Agent Control Standard: os 10 riscos de agente e o padrão de controle recém-lançado".
- **Fontes**:
  - https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ (27/05/2026)
  - https://www.aoshearman.com/en/insights/ao-shearman-on-data/digital-omnibus-on-ai-the-trilogue-deal-is-done-what-made-it-what-didnt-and-what-changed ; https://www.twobirds.com/en/insights/2026/digital-omnibus-on-ai-provisional-agreement-reached-at-the-may-trilogue
  - https://www.helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements/ (16/04/2026); https://artificialintelligenceact.eu/article/26/
  - https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/ (01/09/2026); https://genai.owasp.org/resource/agent-control-standard-acs/
  - https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/ (09/12/2025); https://auth0.com/blog/owasp-top-10-agentic-applications-lessons/

---

## Contexto transversal: incidentes que ancoram o eixo (para abrir posts)

- **ForcedLeak (Salesforce Agentforce, CVSS 9.4, Noma Security, divulgado set/2025) e PipeLeak (Capsule Security, 2026)**: injeção indireta via formulário Web-to-Lead → agente lê o lead → chama `GetLeadsInformation` → envia CRM para fora por e-mail; sem cap de volume; Salesforce passou a exigir HITL por default em ações de e-mail. É o cenário exato de agente de vendas. Fontes: https://thehackernews.com/2025/09/salesforce-patches-critical-forcedleak.html ; https://www.capsulesecurity.io/blog-post/pipeleak-the-lead-that-stole-your-database-exploiting-salesforce-agentforce-with-indirect-prompt-injection ; https://venturebeat.com/security/microsoft-salesforce-copilot-agentforce-prompt-injection-cve-agent-remediation-playbook (2026).
- **Copilot Studio + MCP envenenado (Microsoft, 30/06/2026)**: ver técnica 9.
- **Anthropic "How we contain Claude across products" (28/05/2026)**: tese do blast radius; o blog já tem `noticias/claude-code-auto-mode-padrao`, mas não o post de contenção.

---

## Ranking do eixo
Critério: relevância para quem constrói agente em produção × frescor (últimos 6 meses) × ausência no blog.

1. **Tool poisoning / rug pull em MCP (técnica 9)** — incidente real em produção (Microsoft, 30/06/2026), guidance CSA (jul/2026), Cloudflare (ago/2026); zero cobertura no blog; liga direto com MCP em produção que o público já usa.
2. **Agente como principal + OBO token exchange (técnica 4)** — Auth0 (mai/2026), Okta Agent SSO GA (24/08/2026), Google Agent Identity (set/2026); tema ausente; muda arquitetura de qualquer agente que toca CRM/e-mail.
3. **Autorização determinística pré-ação + risk tiers (técnica 7)** — WriteGuard (ago/2026), OAP (mar/2026), paper de ago/2026 sobre unidade de verificação, dados de fatiga de aprovação; ausente; é a peça que falta entre "guardrails" e "auto mode".
4. **Evals de trajetória com user simulator + pass^k (técnica 1)** — τ²-bench com voz/RAG em 2026, recomendação Anthropic jan/2026; blog tem 4 posts de evals mas nenhum multi-turn/estado/pass^k.
5. **MCP spec 2026-07-28 (técnica 5)** — fresco (jul/2026), breaking changes concretas; blog tem 4 posts de MCP desatualizados em relação à spec.
6. **OTel GenAI semconv + agent SLOs (técnica 6)** — repositório novo (mai–jun/2026), evento de eval, Datadog/Claude Code; blog só tem vendors.
7. **Governança: Omnibus + ACS (técnica 13)** — ACS publicado em 01/09/2026 (news-jacking), Omnibus em vigor desde jul/2026; blog tem 2 posts de compliance a atualizar.
8. **Replay de produção como regressão em CI (técnica 2)** — muito prático, mas fontes são praticantes/vendors (menos "primário"); complementa pipeline de eval existente.
9. **Execução reversível / saga (técnica 8)** — ausente e muito relevante para vendas (deal, reunião, proposta), mas maturidade baixa e fontes majoritariamente blogs.
10. **Custo/latência em runtime: breaker + speculative (técnica 12)** — breaker é prático e ausente; speculative tool calling é fresco (mai–jul/2026) mas só paper; blog já tem 6 posts de custo (risco de canibalizar).
11. **Red-teaming automatizado (técnica 3)** — aquisição Promptfoo (mar/2026) é boa notícia, mas há 6 meses; blog tem evals adversariais.
12. **Memory poisoning origin-bound (técnica 10)** — fresco (jun–jul/2026) e ausente, mas 100% paper; bom como post conceitual ligado aos 3 posts de memória.
13. **CaMeL/NOVA/Parallax (técnica 11)** — conceito forte, mas CaMeL é 2025 e nenhum framework shipping; melhor como seção dentro do post de prompt injection arquitetural do que post próprio.

Sugestão de pares que viram um post só: 9+7 ("gateway MCP com hash de descrição + risk tiers"), 4+5 ("identidade de agente na spec MCP de julho"), 6+13 ("trace OTel como evidência de Art. 12").
