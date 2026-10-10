# Pauta Beer & Code — Julho Semana 3 (batch: news-jacking + evergreen — publica 13–15/07/2026)

> Merge da caça de news-jacking de 13/07 (3 posts, janelas quentes) com a pauta evergreen minerada em 13/07 (2 posts, baseline de tráfego que sobrevive quando o hype seca).
> **Evergreen:** #4 ancora o **cluster Laravel** (o blog tem 27 posts de Laravel e nenhum respondendo o head informacional "o que é laravel"). #5 abre a frente **segurança de LLM**, que o blog tangencia (guardrails, malware em repo, jailbreak) mas nunca atacou pela keyword com demanda.
> ⚠️ Regra de título evergreen: casar a intenção informacional ("o que é X"), não drama de news-jack.
> Anti-canibalização: #4 NÃO repetir conteúdo de deploy/filas/boost — é hub que resume e linka. #5 cross-link OBRIGATÓRIO com guardrails-para-agentes-de-ia, claude-code-malware-repo-limpo (caso real de indirect injection via repo) e fable-5-jailbreak (jailbreak ≠ prompt injection — explicar a diferença no post).

## [#1] OpenAI matou o limite de 5h do Codex — e a Anthropic respondeu em horas
- publicar_em: 2026-07-13T15:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO (mudança visível no produto + confirmação em massa). OpenAI removeu o limite de 5 horas do Codex; Anthropic estendeu acesso/limites do Claude Code (promoção Mai–Jul). Guerra de rate limits entre os dois coding agents mais usados — o leitor quer saber o que ganhou de graça e qual assinatura compensa agora. Formato vivo — atualizar se houver contra-resposta. O concorrente PT que rankeia (Apidog, set/2025) ainda descreve o limite de 5h que acabou de morrer. Link interno: claude-code-preco-2026 e melhor-ia-para-programar-2026-claude-code-vs-codex.
- hook: Pela primeira vez os dois labs estão competindo em quem te deixa usar MAIS o agente — e quem paga assinatura dos dois precisa refazer a conta.
- bullets:
  - O que a OpenAI mudou no Codex (e o que continua limitado)
  - A resposta da Anthropic: o que foi estendido no Claude Code
  - Quanto de uso real você ganha em cada plano agora
  - Por que os dois labs estão queimando margem ao mesmo tempo
  - Qual assinatura compensa em julho de 2026 (a conta refeita)
- keyword_principal: codex limite de uso
- keywords_secundarias: codex sem limite de 5 horas, claude code limite semanal, claude code limites 2026, codex vs claude code limites
- tags: openai, codex, claude-code, anthropic
- dificuldade: easy
- volume: ~0 BR, KD n/a (termo recém-nascido); GSC já mostra o blog em posição 1 pra "claude code limites"; SERP tem concorrente PT desatualizado (Apidog descreve o limite antigo) = brecha direta

## [#2] GPT-5.6 Sol está banindo contas por "ameaça de cibersegurança" — até planilha de Excel virou flag
- publicar_em: 2026-07-13T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO como relato massivo (r/OpenAI 275 ups + r/singularity 637 ups); posicionamento oficial da OpenAI ainda não existe — marcar "em apuração". Usuários do GPT-5.6 Sol relatam bans automáticos por "cybersecurity threat" em tarefas inofensivas, com appeal negado em ~2h. Conecta com o histórico: o Sol nasceu restrito a pedido do governo dos EUA. Formato vivo. Link interno: gpt-5-6-aval-governo-eua e gpt-5-6-sol-terra-luna-qual-usar.
- hook: O modelo que o governo americano segurou por 12 dias chegou ao público com o dedo no gatilho: devs estão perdendo a conta por pedir macro de Excel.
- bullets:
  - O que está acontecendo: os relatos e o padrão dos bans
  - Por que o Sol é paranoico: a herança do lançamento restrito
  - O que dispara o flag (e o que os banidos tinham em comum)
  - Appeal negado em 2h: como funciona (e por que não funciona)
  - Como se proteger: o que evitar no Sol enquanto isso não estabiliza
- keyword_principal: gpt 5.6 sol banindo contas
- keywords_secundarias: gpt 5.6 sol ban, conta banida openai, gpt 5.6 sol seguro usar, openai banimento cybersecurity
- tags: openai, gpt-5-6, noticias-ia
- dificuldade: easy
- volume: ~0 BR, KD n/a; SERP atual só cobre o bloqueio do governo (junho) — ninguém cobriu o ban de usuários; janela escancarada

## [#3] Claude resolveu 2 problemas de física em 2 semanas — um deles parado há 6 meses
- publicar_em: 2026-07-14T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO (Tachikawa relatou publicamente; caso Parisi coberto por Correio Braziliense e Meteored). Yuji Tachikawa, físico teórico de ponta, relata que o Fable 5 destravou um problema em que ele e colaboradores estavam presos há 6 meses — duas semanas depois de Giorgio Parisi (Nobel) usar Claude pra provar uma conjectura de 10 anos. Ninguém em PT conectou os dois casos. Ângulo do blog: não é "IA substituiu o físico" — é COMO os pesquisadores estão usando (verificação, intuição humana + força bruta do modelo), aplicável a qualquer trabalho técnico. Link interno: claude-fable-5-vs-opus-4-8 e fable-5-voltou.
- hook: Em duas semanas, dois físicos de elite — um Nobel incluso — creditaram ao Claude a solução de problemas que os travavam há meses ou anos. Padrão não é sorte.
- bullets:
  - Os dois casos: Tachikawa (6 meses travado) e Parisi (conjectura de 10 anos)
  - O que exatamente o Fable 5 fez — e o que ficou com os humanos
  - Por que agora: o que mudou nos modelos de fronteira
  - Sorte ou capacidade? Como os físicos verificaram o resultado
  - O que copiar do método deles no seu trabalho técnico
- keyword_principal: claude resolveu problema de física
- keywords_secundarias: ia resolve problema de física, claude fable 5 física, giorgio parisi claude, yuji tachikawa claude
- tags: anthropic, claude, noticias-ia
- dificuldade: medium
- volume: ~0 BR, KD n/a; SERP fraca (top orgânico é Instagram; portais cobrem só o caso Parisi) — long-tail ganhável e o ângulo "dois casos + método" é inédito em PT

## [#4] O que é Laravel — e por que ele virou o framework da era da IA
- publicar_em: 2026-07-14T15:00:00-03:00
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

## [#5] Prompt injection: o que é e os principais ataques de 2026 (e como se defender)
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
