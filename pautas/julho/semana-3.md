# Pauta Beer & Code — Julho Semana 3 (evergreen minerado em 13/07 — publica 14–16/07/2026)

> Pauta 100% **evergreen** (par do news-jacking): construir o baseline de tráfego que sobrevive quando o hype de modelo seca. Origem: mineração de 13/jul (gap vs Alura + expansão de seeds, gate de durabilidade no Trends 24m).
> #1 ancora o **cluster Laravel** (o blog tem 27 posts de Laravel e nenhum respondendo o head informacional "o que é laravel"). #2 abre a frente **segurança de LLM**, que o blog tangencia (guardrails, malware em repo, jailbreak) mas nunca atacou pela keyword com demanda.
> #3 (add 13/07) entra no funil **Claude Design → Claude Code**: head gigante em decay de lançamento (abr 135k → jun 74k/mo), SERP genérica saturada (doc oficial + Alura + AI Overview), mas o ângulo dev está vazio no BR. Tratar como evergreen-com-manutenção: atualizar a cada release grande (próximo check: set/26).
> ⚠️ Regra de título evergreen: casar a intenção informacional ("o que é X"), não drama de news-jack.
> Anti-canibalização: #1 NÃO repetir conteúdo de deploy/filas/boost — é hub que resume e linka. #2 cross-link OBRIGATÓRIO com guardrails-para-agentes-de-ia, claude-code-malware-repo-limpo (caso real de indirect injection via repo) e fable-5-jailbreak (jailbreak ≠ prompt injection — explicar a diferença no post).

## [#1] O que é Laravel — e por que ele virou o framework da era da IA
- publicar_em: 2026-07-14T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Responde o head informacional "o que é laravel" (480→1.000/mo, KD 13, +212% a/a, curva subindo) e usa a segunda metade pra tese editorial da marca: por que Laravel é a melhor stack pra desenvolver web na era da IA (AI SDK first-party, Boost/MCP oficial, ecossistema de agente maduro, produtividade full-stack). Vira o hub do cluster Laravel+IA, linkando laravel-ai-sdk, laravel-boost, guia-rag-backend-pgvector, filas, deploy e multi-agent.
  Nota de dados: o ângulo puro de opinião não tem demanda ("melhor framework php" 20/mo, "laravel vale a pena" 10/mo) — por isso a âncora é o termo informacional; a tese entra como diferencial editorial, não como keyword.
- hook: Laravel é "aquele framework PHP" pra quem parou em 2015. Em 2026, é a stack onde o agente lê seu schema via MCP oficial, o SDK de IA é first-party e um dev sobe um produto com RAG em um fim de semana. Aqui vai o que ele é — e por que a era da IA jogou a favor dele.
- bullets:
  - O que é Laravel (e o que ele resolve que PHP puro não resolve)
  - Laravel para que serve em 2026: do CRUD ao produto com IA em produção
  - Por que a era da IA jogou a favor do Laravel: AI SDK first-party, Boost (MCP oficial), convenções que o agente entende
  - Laravel vs a concorrência (Django, Node, Rails) no critério que importa agora: velocidade de entrega com agente no loop
  - Por onde começar: instalação, primeiro projeto e o caminho pros guias práticos do blog (RAG, filas, deploy, multi-agent)
- keyword_principal: o que é laravel
- keywords_secundarias: laravel o que é, laravel para que serve, framework php, laravel framework, laravel ia
- tags: laravel, php, ia
- dificuldade: medium
- volume: ~480/mo nominal (1.000/mo em mai-jun/26), KD 13, +212%/12m, curva 📈. SERP ganhável: domínio já rankeia pra 27 termos Laravel e tem autoridade no pilar.

## [#2] Prompt injection: o que é e os principais ataques de 2026 (e como se defender)
- publicar_em: 2026-07-15T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Cobre o head "prompt injection" (3.600/mo nominal, 8.100 em jun/26, KD 36) com taxonomia dos ataques que marcaram 2026: injection direta, indireta (via documento/página/repo — linkar o caso real do claude-code-malware-repo-limpo), tool poisoning via MCP, e exfiltração de dados por agente. Fecha com o checklist de defesa em camadas (validação de entrada/saída, allowlist de tools, sandbox, human-in-the-loop) amarrando no post de guardrails. Durabilidade: baseline do Trends 3-4x maior que 2024 mesmo após o pico de mai/26 — tema de segurança é perene; título com "2026" pede refresh anual (marcar na pauta de jan/27).
- hook: Seu agente lê um README e obedece a uma instrução escondida nele. Isso não é ficção — foi o padrão de ataque que mais cresceu em 2026, e a busca por "prompt injection" multiplicou por 8 no Brasil. O guia do que é, como os ataques funcionam e o que de fato defende.
- bullets:
  - O que é prompt injection (e por que jailbreak é outra coisa — link fable-5-jailbreak)
  - Injection direta vs indireta: o ataque que vem do usuário e o que vem dos SEUS dados
  - Os ataques de 2026 na prática: repo envenenado, tool poisoning via MCP, exfiltração por agente com acesso a e-mail/browser
  - Por que filtro de palavra não resolve: o problema é o modelo não separar instrução de dado
  - Defesa em camadas: guardrails de entrada/saída, allowlist de tools, sandbox e human-in-the-loop (link guardrails-para-agentes-de-ia e mcp-em-producao)
- keyword_principal: prompt injection
- keywords_secundarias: o que é prompt injection, ataques prompt injection, prompt injection exemplos, indirect prompt injection, jailbreak llm
- tags: seguranca-ia, llm, ai-agents, prompt-engineering
- dificuldade: medium
- volume: ~3.600/mo (8.100 em jun/26), KD 36, +1.273%/12m, curva 📈 com baseline pós-pico 3-4x acima de 2024. Nota: DataForSEO marca intent "transactional" — é ruído do classificador (foreign intent = informational); as secundárias não têm dado no DB, a demanda concentra no head.

## [#3] Claude Design para devs: do protótipo ao código com Claude Code
- publicar_em: 2026-07-16T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Guia do Claude Design (Anthropic Labs, lançado 17/abr/26, update major 17/jun) pelo olhar de quem escreve código: como ele extrai o design system do seu codebase, o round-trip protótipo → Claude Code → canvas, e quando usar Design em vez de ir direto no Code. Todo o top 10 da SERP BR (doc oficial, Alura, Anima, StartSe) fala com founder/PM/designer — ninguém cobre o workflow de dev. Não competir com "o que é" (AI Overview + doc oficial comem o clique); a brecha é o funil dev, onde o blog já tem autoridade (claude code x codex, agent harness, mcp).
  Related searches mostram demanda por "claude design preço / é pago" — cobrir como H2/FAQ dentro do post, não como post separado.
- hook: Todo mundo já explicou o Claude Design pra designer e pra PM. Ninguém explicou pra quem vai receber esse protótipo e transformar em produção.
- bullets:
  - O que é o Claude Design e por que dev deveria ligar (2 min de contexto)
  - Design system a partir do SEU codebase: como funciona a extração
  - O round-trip com Claude Code: protótipo → código → de volta pro canvas
  - Claude Design vs ir direto no Claude Code: quando cada um ganha
  - Limites dos planos (Pro/Max), preço, pegadinhas de token e o que muda com o update de junho
- keyword_principal: claude design como usar
- keywords_secundarias: claude design, claude ia design, claude code design, claude design vs figma
- tags: claude, anthropic, claude-code, ferramentas-de-dev
- dificuldade: medium
- volume: ~590/mo na principal (abr 4.4k → mai 2.4k, decay de lançamento) + head "claude design" ~27.100/mo nominal (jun 74k). Curva ainda é pico-pós-launch, não evergreen provado — aposta: estabiliza como baseline tipo "claude code". GSC: zero tração atual, zero canibalização.
