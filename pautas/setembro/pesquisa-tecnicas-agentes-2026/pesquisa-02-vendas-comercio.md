# Pesquisa 02 — Agentes de vendas e comércio agêntico (estado em 12/09/2026)

Escopo: técnicas para construir agentes que VENDEM (SDR/AE, conversacional em WhatsApp/Instagram/voz, checkout dentro de agentes de terceiros) como sistema de produção. Janela priorizada: mar–set/2026. Método: 30+ buscas/fetches em fontes primárias (specs no GitHub, docs Stripe/Shopify/Google, blogs de engenharia Salesforce/Cloudflare/Sierra, arXiv, ACL Industry). Quando a fonte é secundária (blog de terceiro, imprensa), está marcado.

Acervo do blog lido integralmente antes da pesquisa (`acervo-slugs.txt`). Nenhum slug atual cobre protocolos de comércio agêntico (ACP/UCP/AP2), tokens de pagamento delegado, identidade de agente comprador, simulador de cliente, RL de agente de vendas, negociação agente-a-agente, SDR agent ou pricing por resultado. Os adjacentes estão apontados técnica a técnica.

Legenda de maturidade: **experimental** (paper/preview, sem produção relatada) · **early adopters** (em produção em poucas empresas nomeadas, spec em beta/v0.x) · **mainstream** (padrão de mercado, GA, adoção ampla).

---

### 1. Checkout agêntico via protocolo aberto (ACP + UCP): o lado do MERCHANT

- **O que é**
  Dois padrões abertos definem como um agente de terceiros (ChatGPT, Gemini, Copilot, o seu agente) descobre catálogo, negocia capacidades e fecha compra num merchant sem scraping. **ACP** (OpenAI+Stripe, Apache 2.0) expõe APIs REST: Agentic Checkout (criar/atualizar/completar sessão), Cart, Feed (catálogo), Orders, Delegate Payment, Delegate Auth (OAuth 2.0) e compat com MCP. **UCP** (Google+Shopify) publica um manifesto JSON em `/.well-known/ucp` com *capability negotiation* (interseção das capacidades do merchant e do agente, nomes em reverse-domain como `dev.ucp.shopping.fulfillment`), máquina de estados de checkout (`incomplete` → `requires_escalation` com `continue_url` → `ready_for_complete`), *payment handlers* versionados independentemente e bindings REST/MCP/A2A/Embedded (JSON-RPC 2.0). Os dois convergiram para "discovery-first": o agente descobre e monta carrinho; o checkout pode ser em-chat ou escalado pro site do merchant.
- **Quem está usando/shipping**
  - ACP: releases `2026-01-16` (capability negotiation), `2026-01-30` (extensions, discounts, payment handlers), `2026-04-17` (cart, feed, orders, auth, MCP); status "beta". Maintainers OpenAI e Stripe; Meta listada como co-autora em fontes secundárias. Merchants via Stripe Agentic Commerce Suite: URBN, Etsy, Coach, Revolve, Wix/WooCommerce/BigCommerce (dez/2025).
  - UCP: anunciado 11/01/2026 (NRF), atualizado 19/03/2026 (Cart, Catalog, Identity Linking, onboarding via Merchant Center — fonte secundária), ligado ao **Universal Cart** do Google (I/O, mai/2026, rollout US; Canadá/Austrália; verticais hotel e food delivery anunciadas). Shopify expõe Catalog/Cart/Checkout/Order **MCPs** sobre UCP (Spring '26 Edition) e `@shopify/ucp-cli`.
  - **Fato importante (mar/2026):** OpenAI encerrou o *Instant Checkout* em-chat (06–24/03/2026). Walmart reportou no Shoptalk conversão ~3x pior dentro do ChatGPT do que no site; ~30 merchants Shopify estavam live contra "1 milhão" prometidos (Forrester via CNBC/Forbes). ACP sobreviveu como camada de *feed + discovery + apps de merchant dentro do ChatGPT* (Target, DoorDash, Instacart, Expedia).
- **Maturidade:** early adopters (specs em beta/v0.x, produção em grandes varejistas; o modelo de negócio ainda oscila — ver pivot da OpenAI).
- **Aplicação em agente de vendas**
  Dois lados: (a) se você VENDE, implementar o endpoint ACP/UCP do merchant (Laravel: rotas de checkout session + manifesto `/.well-known/ucp` + webhooks de order) transforma seu catálogo em "vendável por qualquer agente"; (b) se você CONSTRÓI o agente, consumir Catalog/Cart/Checkout MCP da Shopify em vez de scraping. A máquina de estados `requires_escalation` é exatamente o ponto de handoff humano/checkout hospedado que um agente de WhatsApp precisa.
- **Gap vs blog**
  Não existe nenhum post sobre ACP/UCP/Instant Checkout. Adjacentes: `arquitetura-agente-compara-ofertas-amazon-mercado-livre-magalu` e `scraping-api-mcp-trade-off-fontes-dados-agente` tratam o agente como COMPRADOR consumindo dados; `renderizacao-que-converte-json-agente-card-clicavel` trata UI. Ângulo novo: **ser o lado servidor** — expor seu catálogo Laravel como merchant ACP/UCP, com a lição do fracasso do Instant Checkout (discovery converte, checkout em-chat não necessariamente).
- **Fontes**
  - https://github.com/agentic-commerce-protocol/agentic-commerce-protocol (releases 2026-01-16, 2026-01-30, 2026-04-17)
  - https://docs.stripe.com/agentic-commerce/acp
  - https://shopify.engineering/UCP (11/01/2026)
  - https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/ (11/01/2026)
  - https://ucp.dev/ ; https://shopify.dev/docs/agents ; https://www.shopify.com/editions/spring2026
  - https://thenextweb.com/news/google-universal-cart-agent-payments-shopping-io-2026 (mai/2026, secundária)
  - https://www.cnbc.com/2026/03/24/openai-revamps-shopping-experience-in-chatgpt-after-instant-checkout.html ; https://www.forbes.com/sites/jasongoldberg/2026/03/10/why-openais-checkout-retreat-spells-trouble-for-its-commerce-strategy/ ; https://www.agenticcommercefeed.com/blog/2026-03-16-openai-kills-instant-checkout (secundária, cita Shoptalk)
  - https://stripe.com/blog/agentic-commerce-suite (11/12/2025)

---

### 2. Pagamento delegado com credencial escopada: Shared Payment Tokens e agentic network tokens

- **O que é**
  Primitiva em que o agente nunca vê o PAN do cliente. O cliente autoriza no agente (wallet/Link); o agente emite ao vendedor um **Shared Payment Token** (`spt_...`) com `usage_limits` (`currency`, `max_amount`, `expires_at`), escopado ao *profile* Stripe do vendedor; o vendedor cria `PaymentIntent` com `payment_method_data[shared_payment_granted_token]=spt_123` e `confirm=true`; Stripe clona um `PaymentMethod` e o resto (refund, disputa) funciona como cartão normal. Webhook `shared_payment.granted_token.deactivated` quando consumido/expirado/revogado. Por baixo, desde 03/03/2026 o SPT pode ser lastreado em **agentic network tokens** de Mastercard Agent Pay e Visa Intelligent Commerce (token vinculado a agente + escopo de merchant + política de consentimento) e em BNPL (Affirm, Klarna). Radar anexa sinais de risco para diferenciar "agente de alta intenção" de bot.
- **Quem está usando/shipping**
  - Stripe: SPT em preview (`Stripe-Version: 2026-04-22.preview`), disponível US/CA/33 países europeus — Brasil NÃO está na lista. Link Agent Wallet (Sessions, 29/04/2026) aprova compras para agentes Claude e OpenAI via SPT; `npx @stripe/link-cli spend-request create` emite SPT one-time para teste em live mode.
  - Visa Intelligent Commerce integrado ao ChatGPT e Codex (Visa Payments Forum, 10/06/2026): limites por transação/dia/semana, allowlist de merchants, aprovação para valores altos.
  - Mastercard Agent Pay em produção em Singapura e Malásia (fonte secundária, eco.com).
- **Maturidade:** early adopters (API em preview, redes em produção regional, ainda sem Brasil/Pix).
- **Aplicação em agente de vendas**
  É o "pagamento dentro da conversa" sem o agente virar PCI-scope: o agente negocia, fecha preço, e o `max_amount` do token é o teto duro do que ele pode cobrar — um guardrail financeiro que não depende do prompt. No Brasil hoje o equivalente pragmático é link Pix/cartão gerado dentro do chat (ver técnica 9), mas a arquitetura "token escopado ao valor negociado" é o alvo de projeto.
- **Gap vs blog**
  Nenhum post sobre pagamentos. `alucinacao-ecommerce-caro-llm-inventa-cupom-estoque` trata alucinação de preço, não de como cobrar. Ângulo novo: o `max_amount` do SPT como guardrail de última linha + mapa do que (não) chega ao Brasil.
- **Fontes**
  - https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens (variante seller; preview 2026-04-22)
  - https://stripe.com/blog/supporting-additional-payment-methods-for-agentic-commerce (03/03/2026)
  - https://thepaypers.com/payments/news/stripe-launches-link-wallet-for-autonomous-ai-agent-payments (abr/2026, secundária)
  - https://www.digitalcommerce360.com/2026/06/12/visa-openai-agent-led-payments/ (10/06/2026)
  - https://eco.com/support/en/articles/15192001-what-is-mastercard-agent-pay-ai-agent-commerce-protocol-in-2026 (secundária)

---

### 3. Mandatos assinados e compras "human-not-present" (AP2 v0.2, Agent Pay for Machines, MPP/x402)

- **O que é**
  Para o agente comprar SEM humano no loop, o padrão é o usuário assinar antes um **mandato** (Verifiable Digital Credential) que descreve intenção e limites; o agente depois produz um mandato fechado com o carrinho final e o pagamento, e a cadeia assinada vira trilha de auditoria. AP2 (Google) define Checkout Mandate e Payment Mandate em estados *open*/*closed*, papéis (shopping agent, merchant agent, credentials provider, payment processor), extensão A2A, uso com MCP e pagamento por cartão ou **x402** (HTTP 402 em USDC). Na camada máquina-a-máquina: **MPP** (Stripe+Tempo, 18/03/2026) padroniza descoberta de preço, autorização, assinatura e reconciliação para agentes pagando APIs; **Mastercard Agent Pay for Machines** (10/06/2026) faz credenciamento, permissioning e controles de gasto programáticos com permissões registradas em Polygon/Solana/Base.
- **Quem está usando/shipping**
  AP2 v0.2.0 (28/04/2026) — foco em Human Not Present; doado à FIDO Alliance. AP4M: 30+ parceiros (Adyen, Stripe, Coinbase, Cloudflare, Checkout.com) — anúncio, sem GA declarado. x402 Foundation (Coinbase+Cloudflare). Tudo ainda é v0.x/anúncio; nenhum caso de varejo B2C em escala reportado.
- **Maturidade:** experimental → early adopters (specs vivas, pilotos; "agente compra ingresso sozinho quando abre" é o caso de uso anunciado, não medido).
- **Aplicação em agente de vendas**
  Do lado vendedor: preparar o merchant para aceitar compra de um *buyer agent* com mandato (validar assinatura, respeitar limites do mandato, emitir recibo verificável). Do lado de um agente de recompra/reposição (B2B, suprimentos): mandato de intenção + x402/MPP para pagar fornecedores ou APIs sem humano. É a base técnica para "agente vendendo para agente" (técnica 8) ter liquidação.
- **Gap vs blog**
  Nenhum post. Adjacente distante: `tracking-247-do-reativo-ao-agente-agendado` (agente agendado que monitora) — ângulo novo é o agente agendado que *paga* dentro de um mandato assinado.
- **Fontes**
  - https://ap2-protocol.org/ ; https://github.com/google-agentic-commerce/AP2/releases (v0.2.0 em 28/04/2026)
  - https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol (16/09/2025)
  - https://stripe.com/blog/machine-payments-protocol (18/03/2026) ; https://docs.stripe.com/payments/machine/mpp ; https://docs.stripe.com/payments/machine/x402
  - https://www.mastercard.com/global/en/news-and-trends/press/2026/june/mastercard-launches-agent-pay-for-machines.html (10/06/2026) ; https://fortune.com/2026/06/10/mastercard-ai-payments-protocol-launch-agentic-finance/
  - https://workos.com/blog/x402-vs-stripe-mpp-how-to-choose-payment-infrastructure-for-ai-agents-and-mcp-tools-in-2026 (secundária, comparação técnica)

---

### 4. Identidade do agente comprador: Web Bot Auth, Visa TAP e o precedente Amazon v. Perplexity

- **O que é**
  Merchant precisa responder "esse tráfego é um agente legítimo agindo por um cliente ou um bot?". Resposta em produção: **HTTP Message Signatures (RFC 9421)** sobre **Web Bot Auth** — o agente assina cada request com Ed25519, inclui `keyid` (diretório público da rede), `nonce` anti-replay e uma tag indicando `agent-browser-auth` (navegando) ou `agent-payer-auth` (pagando). Visa **Trusted Agent Protocol** e Mastercard Agent Pay usam esse esquema; Cloudflare valida na borda (timestamp, nonce, tag, assinatura) e prepara *managed rulesets* que liberam agentes registrados e bloqueiam o resto. Shopify também aplica *trust tiers*: agentes autenticados com tier maior desbloqueiam checkout direto e rate limits maiores.
- **Quem está usando/shipping**
  TAP anunciado 14/10/2025 (Adyen, Checkout.com, Shopify, Stripe, Worldpay, Microsoft...). Cloudflare blog atualizado 15/07/2026. IETF: drafts de Web Bot Auth com prazo de BCP sobre gestão de chaves até ago/2026 (secundária). Jurisprudência: Amazon obteve injunção contra o Comet da Perplexity (10/03/2026, CFAA), **revertida pelo Ninth Circuit em 04/08/2026** — agente agindo por usuário autenticado não é "acesso não autorizado" per se. Ou seja: a disputa técnica (quem autentica o agente) está substituindo a disputa jurídica (pode ou não).
- **Maturidade:** early adopters (spec em IETF, validação na borda disponível, diretórios operados por Visa/Mastercard).
- **Aplicação em agente de vendas**
  Se o seu e-commerce recebe agentes: middleware que verifica assinatura e diferencia política (catálogo aberto a qualquer agente; checkout só a agentes com `agent-payer-auth` válido). Se você constrói o agente comprador: registrar chave no diretório e assinar requests — sem isso, em 2026 você cai em WAF. Para o agente vendedor no WhatsApp isso é menos crítico, mas define como você trata *buyer agents* que chegam no seu site.
- **Gap vs blog**
  Adjacente: `trust-layer-agente-reputacao-fonte` (reputação da FONTE que o agente lê) e `prompt-injection-agente-site-raspado-system-prompt`. Ângulo novo invertido: **o seu site autenticando o agente que chega**, com RFC 9421 e o caso Amazon v. Perplexity como moldura.
- **Fontes**
  - https://blog.cloudflare.com/secure-agentic-commerce/ (24/10/2025, atualizado 15/07/2026)
  - https://www.businesswire.com/news/home/20251014144421/en (TAP, 14/10/2025)
  - https://shopify.dev/docs/agents (trust tiers, signed-request verification)
  - https://www.cnbc.com/2026/03/10/amazon-wins-court-order-to-block-perplexitys-ai-shopping-agent.html ; https://www.engadget.com/2230471/perplexity-has-successfully-overturned-amazon-injunction-on-its-ai-shopping-bot/ (04/08/2026)

---

### 5. Guardrails determinísticos de autoridade de preço e promessa (Agent Script, `available when`, liability)

- **O que é**
  Separar o que o modelo PODE decidir do que ele só pode EXECUTAR sob condição verificada. O Salesforce **Agent Script** materializa isso: arquivo único, indentado, em que `→` marca lógica determinística pré-LLM e `|` texto de prompt; `available when` gateia quais ações o modelo enxerga (ex.: `apply_discount` só aparece se `order.verified && discount_policy.allows(tier)`); instruções condicionais reescrevem o prompt a cada iteração conforme o estado; variáveis "pinadas" impedem o modelo de extrair IDs críticos. Como os gates são determinísticos, são testáveis **sem chamar o LLM**. Três posturas na mesma gramática: totalmente scriptado, misto, agêntico. O pano de fundo jurídico é *Moffatt v. Air Canada* (chatbot inventou política de reembolso; empresa responsabilizada) e, em 2026, o fato de todos os protocolos de comércio agêntico manterem o merchant como *merchant of record* — chargeback de "o agente entendeu errado" cai no vendedor, com Visa apertando o limiar de disputas de 2,2% para 1,5% em 01/04/2026 (secundária).
- **Quem está usando/shipping**
  Agent Script GA no Summer '26 (jun/2026); parser, linter, compilador, LSP e extensão VS Code open source Apache 2.0 (github.com/salesforce/agentscript); runtime proprietário. Sales Cloud rebatizado **Agentforce Sales** (Spring '26) com SDR Agent. Stripe Radar em SPT como guardrail de fraude.
- **Maturidade:** mainstream como PADRÃO (gating determinístico de tools); early adopters como LINGUAGEM (Agent Script).
- **Aplicação em agente de vendas**
  Agente de vendas não recebe tool `dar_desconto(percent)`. Recebe `propor_oferta(offer_id)` onde as ofertas elegíveis são computadas fora do modelo (regras de margem, estoque, campanha). Promessas (prazo, garantia, devolução) saem de um `policy_lookup` com texto canônico, não de geração livre. Testes unitários dos gates rodam no CI sem LLM; evals de conversa só cobrem o que sobrou.
- **Gap vs blog**
  Adjacentes fortes: `guardrails-para-agentes-de-ia` (genérico), `alucinacao-ecommerce-caro-llm-inventa-cupom-estoque` (o problema), `tool-use-na-pratica-desenhando-ferramentas-llm`, `system-prompt-comportamento-do-agente`. Ângulo novo: **autoridade de preço como design de tool + gates testáveis sem modelo**, com Agent Script como referência de sintaxe e o cenário de chargeback/merchant of record em 2026.
- **Fontes**
  - https://www.salesforce.com/blog/agent-script-control-plane/ (30/04/2026)
  - https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html ; https://github.com/salesforce/agentscript ; https://developer.salesforce.com/blogs/2026/02/agent-script-decoded-intro-to-agent-script-language-fundamentals
  - https://developer.salesforce.com/blogs/2026/06/the-salesforce-developers-guide-to-the-summer-26-release (GA)
  - https://www.canlii.org/en/commentary/doc/2025CanLIIDocs1963 (Moffatt v Air Canada)
  - https://www.chargeflow.io/blog/ai-agent-chargeback-liability ; https://www.fintechwrapup.com/p/deep-dive-the-hidden-liability-of (secundárias)

---

### 6. Simulador de cliente com fidelidade de decisão (CustomerSim/UserGRPO, "Simulated Customers Never Walk Away", VISTA)

- **O que é**
  Evals de agente de vendas dependem de um LLM fazendo papel de cliente. A pesquisa de 2026 mostra que esse simulador **mente onde importa**: em 2.790 conversas de produção de um agente de vendas LLM (793 com pagamento verificado), simuladores reproduzem bem quem vai comprar, mas "puxam" não-compradores para o frame de compra — resistência expressa cai de 25,1% para 13,5%, deliberação sobe de 21,9% para 40,1%; cliente real que não compra *desengaja*, simulado *pergunta o preço*. Treinar ou avaliar persuasão contra isso otimiza uma paisagem de reward errada exatamente na retenção de quem iria embora. **CustomerSim** (360 personas, 5 categorias) mede aderência à persona e propõe **UserGRPO** (RL multi-turno, multi-objetivo: fluência + alinhamento de decisão), subindo alinhamento de 0,417 para 0,652; modelos de fronteira (Claude Opus 4.8, GPT-5.6 Sol) ficam abaixo de 74% de aderência. **VISTA** adiciona 6 métricas de realismo/cobertura e simulador híbrido UI+API em e-commerce. **UserIDA** separa *qual intenção* o usuário simulado deve expressar de *como* (86,6% de acurácia de intenção). Em produção, Sierra roda 35k+ simulações/dia, gera casos a partir de SOPs/transcrições e gate de release em CI.
- **Quem está usando/shipping**
  arXiv 2606.20708 (16/06/2026), 2605.08334 (08/05, rev. 29/07/2026), 2606.11079 (09/06/2026), 2608.09420 (10/08/2026); Sierra (blog 19/08/2025, produção). Salesforce Testing Center e Meta Business Agent Platform falam em "medição", sem detalhes públicos.
- **Maturidade:** simulação como prática = mainstream em CX; *decision fidelity* e simuladores treinados por RL = experimental (papers de jun–ago/2026).
- **Aplicação em agente de vendas**
  Pipeline de eval: personas derivadas de transcripts reais com outcome (comprou/não comprou), simulador calibrado para reproduzir a taxa de desistência real por segmento, judge que pontua não só "fechou" mas "respeitou política de desconto / fez handoff quando devia". Medir o viés do simulador contra outcomes reais antes de confiar no número.
- **Gap vs blog**
  Adjacentes: `avaliacao-de-agentes-de-ia-evals-honestos`, `evals-para-agentes-de-ia-llm-as-a-judge`, `llm-as-a-judge-avaliacao-automatizada-agente-ofertas`, `model-graders-usando-llms-para-avaliar-llms-e-os-3-erros-que-invalidam-o-seu-eval`, `prompts-resilientes-evals-adversariais-edge-cases`. Nenhum trata do **usuário simulado** como fonte de erro. Ângulo novo: "o cliente simulado nunca vai embora" — como calibrar o simulador de vendas contra conversões reais.
- **Fontes**
  - https://arxiv.org/abs/2606.20708 (16/06/2026)
  - https://arxiv.org/abs/2605.08334 (CustomerSim/UserGRPO, v2 29/07/2026)
  - https://arxiv.org/abs/2606.11079 (VISTA, 09/06/2026)
  - https://arxiv.org/abs/2608.09420 (UserIDA, 10/08/2026)
  - https://sierra.ai/blog/simulations-the-secret-behind-every-great-agent (19/08/2025)

---

### 7. RL do agente de vendas com rewards heterogêneas e A/B em produção (REPO, Personality-Aware RL)

- **O que é**
  Em vez de SFT em transcripts "bons", treinar a política de venda com reward composto: **REPO** (ACL 2026 Industry) combina reward model treinado em preferências, LLM-as-a-judge para nuances comportamentais e **regras regex determinísticas** para números, formato e guardrails (não prometer o que não pode). Domínio: business development e negociação de preço em OTA (agência de viagens online). Resultado em **A/B de produção com 9.653 conversas reais**: taxa de resposta +12,14 pp, sucesso da tarefa +5,94 pp; 93,33% dos bad cases corrigidos. Linha paralela: RL consciente de personalidade (embedding de 81 dimensões do usuário, Dueling DDQN, reward com "mudança de ideia" que reduz retratações pós-acordo) em diálogo persuasivo. Stack típico 2026 para quem não tem infra: base → SFT → DPO/ORPO em pares de preferência extraídos de transcripts com outcome.
- **Quem está usando/shipping**
  ACL 2026 Industry Track (jul/2026) — paper industrial com A/B real; arXiv 2601.06877 (jan/2026). Não há anúncio público de OpenAI/Anthropic de RFT específico para vendas; os RFT públicos seguem focados em tarefas verificáveis.
- **Maturidade:** early adopters (um paper industrial com A/B; a maioria das empresas ainda usa prompt + exemplos). Rumor/roadmap: nada de vendor sobre "RFT de vendas".
- **Aplicação em agente de vendas**
  Só faz sentido depois de (6): o reward precisa de simulador com fidelidade de decisão ou de outcome real (conversão, ticket, NPS). O componente regex/determinístico é o elo com a técnica 5: penalidade dura a qualquer promessa fora da política. DPO em pares (resposta que converteu vs. não converteu, mesmo contexto) é o ponto de entrada barato.
- **Gap vs blog**
  Adjacentes: `o-que-e-fine-tuning`, `fine-tuning-rag-ou-prompt-qual-escolher`, `rag-fine-tuning-juntos-arquitetura-hibrida-96`, `quando-usar-rag-fine-tuning-ou-contexto`. Nenhum trata de RL/DPO com reward de negócio. Ângulo novo: **treinar política de venda com reward misto (RM + judge + regex de guardrail)** e por que o A/B real é a única métrica que vale.
- **Fontes**
  - https://aclanthology.org/2026.acl-industry.34/ (REPO, jul/2026)
  - https://arxiv.org/abs/2601.06877 (Personality-Aware RL, jan/2026)
  - https://arxiv.org/abs/2606.20708 (por que o reward do simulador está errado)

---

### 8. Negociação agente-a-agente: seu agente vendedor contra buyer agents

- **O que é**
  Benchmarks de 2026 expõem como LLMs negociam quando há informação privada. **AgenticPay** (110+ tarefas, bilateral a many-to-many; métricas de viabilidade, eficiência e welfare) acha "gaps substanciais" em raciocínio estratégico de longo horizonte. **TERMS-Bench** (13 modelos, jogo bayesiano com counterpart instrumentado) mostra que alto *deal rate* esconde falhas em extração de surplus, uso de pistas, calibração de crenças e **compliance** com restrições. **"Counterparty Modeling is Not Strategy"**: agentes modelam bem as preferências do outro lado e não convertem isso em estratégia; âncoras superficiais de abertura determinam o acordo mais que utilidades; **vendedores são mais acomodativos**. **Supply chain (9.840 negociações, 9 modelos)**: a identidade do provedor prevê quem captura surplus melhor que capacidade (buyer share em self-play: OpenAI 40%, Google 50%, Qwen 70%); modelos fracos aceitam contratos irracionais em 19,2% dos casos; "paciência" no prompt explica 90% da variância na divisão de surplus.
- **Quem está usando/shipping**
  Pesquisa: arXiv 2602.06008 (05/02/2026, Dawn Song et al.), 2605.13909 (13/05, rev. 13/06/2026), 2605.16575 (15/05/2026), 2608.07538 (29/07/2026). Casos reais de agente-compra-de-agente em B2C ainda são anúncios (AP4M, Universal Cart) — nenhum volume publicado.
- **Maturidade:** experimental (benchmarks), com infraestrutura de pagamento (técnicas 2–3) chegando antes da competência estratégica dos modelos.
- **Aplicação em agente de vendas**
  Três decisões de projeto saem direto dos papers: (1) o agente vendedor **não negocia preço livremente** — recebe faixa e ofertas pré-computadas (liga com técnica 5), porque é sistematicamente acomodativo e manipulável por "paciência"; (2) verificação automática de racionalidade do acordo (margem, estoque) antes de confirmar, porque a exploitabilidade existe; (3) política explícita para detectar quando o outro lado é um agente (técnica 4) e mudar de modo (sem small talk, ofertas estruturadas).
- **Gap vs blog**
  Nenhum post sobre negociação ou buyer agents. `arquitetura-agente-compara-ofertas-amazon-mercado-livre-magalu` é o agente comprador comparando — ângulo novo é o **vendedor defensivo**: como não ser o lado acomodativo quando o cliente é um agente.
- **Fontes**
  - https://arxiv.org/abs/2602.06008 (AgenticPay, 05/02/2026)
  - https://arxiv.org/abs/2605.13909 (TERMS-Bench, mai–jun/2026)
  - https://arxiv.org/abs/2605.16575 (Counterparty Modeling, 15/05/2026)
  - https://arxiv.org/abs/2608.07538 (Supply chain bargaining, 29/07/2026)

---

### 9. Agente de vendas nativo do canal: Meta Business Agent + Business Agent Platform (WhatsApp/Instagram, Pix, cobrança por token)

- **O que é**
  A Meta passou a oferecer o agente de vendas DENTRO do WhatsApp/Instagram/Messenger: responde com base no catálogo, recomenda produto, **qualifica lead, agenda, fecha venda simples e faz handoff para humano**; para enterprise, a **Business Agent Platform** permite agente customizado com integrações (Shopify, Zendesk, Shopee, "centenas de sistemas"), "controles, guardrails e medição". Modelo de cobrança: grátis até 31/07/2026; desde **01/08/2026** cobrança por token para enterprise e tier WhatsApp Business Premium para PME (fontes secundárias BR + TechCrunch). No Brasil o agente chegou em 24/02/2026 (secundária) e o fluxo de pagamento é Pix/cartão gerado no chat (secundária — não achei doc oficial Meta sobre Pix nativo via agente).
- **Quem está usando/shipping**
  Lançamento global em 03/06/2026 (Conversations, Londres); "mais de 1 milhão de negócios" já usam (Meta). Concorrentes de plataforma (Omnichat, Zappy, Maxbot etc.) estão se reposicionando como camada acima.
- **Maturidade:** mainstream para PME (nativo, grátis→pago); early adopters para Business Agent Platform (APIs enterprise recém-abertas).
- **Aplicação em agente de vendas**
  Decisão build vs. buy mudou em jun–ago/2026: para PME, o agente nativo cobre o "tier 1"; construir só faz sentido quando você precisa de (a) estado de negociação próprio, (b) política de preço/estoque fora do catálogo Meta, (c) pagamento próprio (Pix via PSP, split), (d) handoff para CRM/Laravel. Arquitetura híbrida: Business Agent atende; webhook de "lead qualificado" dispara seu agente Laravel com estado, carrinho e link de pagamento.
- **Gap vs blog**
  Adjacentes diretos: `como-criar-um-agente-de-ia-para-whatsapp`, `tutorial-como-integrar-o-laravel-com-twilio-...-whatsapp`, `agente-bolao-copa-whatsapp-evolution-api-n8n`. Todos ensinam a CONSTRUIR o agente. Ângulo novo: **o que muda quando a Meta entrega o agente nativo e começa a cobrar por token** — quando ainda vale construir, como integrar via Business Agent Platform, e onde entra o carrinho/Pix/handoff seu.
- **Fontes**
  - https://whatsappbusiness.com/blog/introducing-meta-business-agent-ai/ (03/06/2026)
  - https://techcrunch.com/2026/06/03/metas-ai-agent-for-whatsapp-business-is-now-available-globally/
  - https://www.mobiletime.com.br/noticias/01/07/2026/whatsapp-cobra-respostas/ (cobrança, secundária BR)
  - https://www.maxbot.com.br/blog/meta-business-agent ; https://naweb.ia.br/meta-agentes-de-ia-whatsapp/ ; https://www.socialhub.pro/blog/whatsapp-business-pagamento-2026-meta-pix-direto-conversa-pme-brasil/ (secundárias BR; Pix no chat não confirmado em doc oficial)

---

### 10. Arquitetura de SDR agent em 2026: sinais → enriquecimento em cascata → outreach → handoff com contexto

- **O que é**
  O desenho convergiu em 7 blocos: (1) **monitoramento de sinais** (funding, vagas, troca de stack, visitas) como trigger em vez de lista estática; (2) **enriquecimento em waterfall** (agregar 20+ provedores, fallback ordenado por custo/cobertura; Clay "Claygent" pesquisa web e devolve JSON estruturado); (3) identificação do **buying committee** (ZoomInfo/Apollo); (4) geração de outreach condicionada a sinal + histórico do CRM; (5) sequência multicanal com gestão de mailbox/warmup/deliverability; (6) **qualificação estruturada** (budget, autoridade, timing) com decisão nurture/desqualificar/agendar; (7) **handoff com notas de discovery já no CRM** — onde a maioria das implantações vive ou morre. Modelo dominante em produção: híbrido — agente faz primeiro toque e qualificação, AE recebe só reunião quente.
- **Quem está usando/shipping**
  HubSpot Prospecting Agent (Spring Spotlight, abr/2026): monitoramento de contas, sourcing de comitê via ZoomInfo/Apollo, drafts para revisão, agendamento; early users com 2x a taxa de resposta do benchmark e +28% de reuniões ao substituir sequences para MQLs não agendados; **US$ 1 por lead recomendado**. Salesforce Agentforce SDR (Spring '26, GA): e-mail outbound personalizado, replies em thread, calendário, booking. 11x (Alice/Julian; e-mail, fone, SMS, WhatsApp, LinkedIn; 21+ provedores de dados) e Artisan (Ava; enriquecimento antes do envio, menor volume) — fontes secundárias/comparativas. Apollo lançou app no ChatGPT e "AI Assistant" (mai/2026, secundária).
- **Maturidade:** mainstream (categoria consolidada, GA nos dois grandes CRMs); o que ainda separa demo de produção é eval de conversa (6), guardrail de promessa (5) e handoff.
- **Aplicação em agente de vendas**
  Para dev Laravel: filas (Horizon) para sinais e enriquecimento, tabela de estado de lead com máquina de estados explícita (novo → enriquecido → contatado → respondeu → qualificado → agendado/handoff), tool `schedule_meeting` só disponível após qualificação (gate da técnica 5), e o handoff como evento com payload de contexto, não um "transferir para humano" textual.
- **Gap vs blog**
  Nenhum post sobre SDR/prospecção/enriquecimento. Adjacentes: `classificacao-de-intencao-llm-roteamento-de-agente` (roteamento), `tracking-247-do-reativo-ao-agente-agendado` (monitoramento agendado). Ângulo novo: a **máquina de estados do lead + waterfall de enriquecimento + handoff com contexto**, com os números públicos de HubSpot/Salesforce como baliza.
- **Fontes**
  - https://www.hubspot.com/company-news/spring-2026-spotlight ; https://community.hubspot.com/t5/Breeze-Library/Prospecting-Agent-Just-Became-a-Complete-Prospecting-Solution/ba-p/1267456 (abr/2026)
  - https://www.salesforce.com/products/innovation/spring-26-release/ ; https://salesforcedictionary.com/blogs/agentforce-sales-complete-2026-guide (secundária)
  - https://www.11x.ai/guides/artisan-vs-11x ; https://www.artisan.co/blog/the-best-ai-sdrs (vendors, viés comercial)
  - https://industry-lens.com/reports/11x-salesloft-apollo-io-accelerate (mai/2026, secundária)

---

### 11. Outcome-based pricing e atribuição: cobrar por reunião/lead/resolução e provar causalidade

- **O que é**
  Pricing por resultado exige três coisas técnicas: **verificabilidade** (evento de outcome observável pelo sistema — reunião *realizada*, não só agendada; lead *aceito* pelo AE), **atribuição** (o agente causou ou o humano que revisou/o baseline teria feito?) e **acordo prévio** sobre a definição. O padrão de mercado virou **híbrido**: assinatura-base + componente por resultado. Bessemer (09/02/2026) documenta exemplos: Intercom Fin US$ 0,99/resolução, EvenUp por pacote gerado, Leena AI por ticket fechado com mínimo. Em vendas: HubSpot US$ 1/lead recomendado; 11x por reunião agendada (secundária). Deloitte publicou em 04/06/2026 orientação contábil específica para reconhecimento de receita em outcome-based pricing de produto agêntico — sinal de que virou problema de CFO, não só de GTM. Para o lado de quem OPERA o agente (não vende software), a mesma mecânica vira métrica interna: custo por reunião qualificada, conversão por etapa, uplift vs. controle.
- **Quem está usando/shipping**
  Bessemer AI Pricing Playbook (09/02/2026); Deloitte DART (04/06/2026); HubSpot (abr/2026); Intercom (preço público). Estatísticas como "41% híbrido" e "61% terão outcome até fim de 2026" circulam em blogs atribuídas ao playbook — NÃO encontrei esses números no texto da Bessemer; tratar como não confirmados.
- **Maturidade:** mainstream em suporte (per resolution); early adopters em vendas (atribuição mais difícil — ciclo longo, humano no fechamento).
- **Aplicação em agente de vendas**
  Instrumentar o agente para emitir eventos de outcome assinados/idempotentes (meeting_held, lead_accepted, order_paid com `payment_intent`), holdout controlado (parte dos leads segue fluxo humano) para medir uplift, e dashboards de atribuição por etapa. Sem holdout não há atribuição defensável — nem para cobrar do cliente nem para justificar o agente internamente.
- **Gap vs blog**
  Adjacentes: `custo-agente-ia-producao-2026-planilha-tco`, `quanto-custa-agente-ia-producao-conta-tokens`, `reduzir-custo-api-de-ia` — todos do lado do CUSTO. Nenhum do lado da RECEITA/atribuição. Ângulo novo: **eventos de outcome + holdout + métricas de funil do agente** (e a armadilha dos números de mercado não verificados).
- **Fontes**
  - https://www.bvp.com/atlas/the-ai-pricing-and-monetization-playbook (09/02/2026)
  - https://dart.deloitte.com/USDART/home/publications/deloitte/industry/technology/accounting-outcome-based-pricing-agentic-ai (04/06/2026)
  - https://www.hubspot.com/company-news/spring-2026-spotlight (US$ 1/lead)
  - https://www.chargebee.com/blog/pricing-ai-agents-playbook/ ; https://pickaxe.co/post/ai-agent-pricing-models (secundárias; origem dos "41%/61%" não confirmada)

---

## Notas de rigor (o que NÃO afirmar)

- "Instant Checkout processa X bilhões" — falso em 2026; o produto foi descontinuado em mar/2026. O que existe é ACP como feed/discovery + apps de merchant no ChatGPT + Stripe Agentic Commerce Suite para outros agentes.
- SPT/Link Agent Wallet no Brasil — não disponível (lista oficial: US, CA, Europa).
- Pix nativo via Meta Business Agent — só fontes secundárias BR; não achei doc oficial da Meta.
- "Agent Pay for Machines em produção" — anúncio com parceiros (10/06/2026), sem GA/volumes.
- "Bessemer: 41% híbrido / 61% outcome" — não consta na página do playbook; circula em blogs.
- RFT de OpenAI/Anthropic para vendas — não há anúncio; o que existe é paper industrial (REPO) com A/B.
- Dados de 11x/Artisan vêm de páginas comparativas dos próprios vendors; tratar como marketing.

## Ranking do eixo
(relevância para quem constrói agente em produção × frescor × ausência no blog)

1. **Guardrails determinísticos de autoridade de preço/promessa (5)** — aplicável hoje em qualquer agente de WhatsApp; Agent Script GA jun/2026 dá vocabulário; zero cobertura do ângulo "tool sem poder de desconto + gates testáveis sem LLM".
2. **Simulador de cliente com fidelidade de decisão (6)** — papers jun–ago/2026, muda como se lê qualquer eval de venda; blog tem evals mas nunca questionou o usuário simulado.
3. **Checkout agêntico via ACP/UCP, lado merchant (1)** — padrão com releases abr–mai/2026 e a lição do pivot da OpenAI; tutorial "expor seu catálogo Laravel como merchant UCP" é inédito em pt-BR.
4. **Agente nativo Meta + cobrança por token (9)** — mais fresco (jun–ago/2026) e mais próximo do leitor; risco: parte das fontes BR é secundária.
5. **Arquitetura SDR agent (10)** — mainstream e sem post; números públicos HubSpot/Salesforce de 2026.
6. **Pagamento delegado com token escopado (2)** — conceito forte (max_amount como guardrail), mas sem Brasil limita o hands-on.
7. **Negociação agente-a-agente / vendedor defensivo (8)** — frescor alto (jul/2026), relevância prática ainda antecipatória.
8. **RL com rewards heterogêneas + A/B (7)** — ACL Industry jul/2026; público menor (quem já tem transcripts com outcome).
9. **Outcome-based pricing e atribuição (11)** — útil para o lado "vender o agente"; menos engenharia.
10. **Identidade do agente comprador / Web Bot Auth (4)** — relevante para quem tem e-commerce recebendo agentes; caso Amazon v. Perplexity (ago/2026) dá gancho de notícia.
11. **Mandatos human-not-present / AP4M / MPP-x402 (3)** — mais roadmap que produção; bom como seção de um post maior, fraco como post isolado.
