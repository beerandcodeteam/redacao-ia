# Pauta news-jacking — 17/07/2026 (publicar HOJE, horários escalonados)

## Kimi K3 chegou: o "Fable 5 chinês" que bate Opus 4.8 custando 5x menos — o que é real nos benchmarks
- publicar_em: 2026-07-17T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Cobertura do lançamento do Kimi K3 (Moonshot AI): 2,8T parâmetros, 1M de contexto, pesos abertos, 3º lugar na ArtificialAnalysis batendo Claude Opus 4.8, topo do Frontend Code Arena, preço US$ 3/15 por milhão de tokens. VERIFICADO: lançamento, benchmarks ArtificialAnalysis, preço e disponibilidade no OpenRouter (`moonshotai/kimi-k3`). Separar benchmark real de hype ("benchmaxxed" — ceticismo recorrente da comunidade com modelo chinês). Formato vivo: atualizar quando saírem testes independentes. Contexto geopolítico: fala de Xi Jinping na WAIC reafirmando aposta em open source. Links internos: glm-5-2-open-source-melhor-codigo, claude-opus-4-8-vs-minimax-m3-vs-qwen-3-local, fable-5-voltou, claude-sonnet-5-como-interpretar-benchmarks.
- hook: A cada trimestre a China solta um modelo que "mata" os fechados — mas dessa vez o Kimi K3 chegou em 3º na ArtificialAnalysis, acima do Opus 4.8, custando 5x menos. Hype ou virada de jogo?
- bullets:
  - O que é o Kimi K3: 2,8T parâmetros, 1M de contexto e Kimi Delta Attention
  - Os benchmarks: onde ele bate Opus 4.8 e GPT-5.6 (e onde não bate)
  - US$ 3/15 por milhão de tokens: a conta contra Claude e GPT na prática
  - Como testar agora: app, OpenRouter e pesos abertos (roda local?)
  - "Benchmaxxed" ou real? O que a comunidade já achou de estranho
- keyword_principal: kimi k3
- keywords_secundarias: kimi k3 vs claude, kimi k3 benchmark, kimi k3 preço, kimi ai em português, moonshot ai
- tags: ia, llm, open-source, benchmarks, kimi, moonshot-ai
- dificuldade: medium
- volume: ~0 BR ainda (termo de ~24h), KD n/a; proxy "kimi k2" = 6.600/mês KD 47 com pico de 22.200 no mês de lançamento — janela aberta, zero artigo PT-BR no top 10 orgânico

## Claude agora faz login sozinho nos seus sites: como funciona o 1Password for Claude (sem expor senha nenhuma)
- publicar_em: 2026-07-17T16:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Anthropic + 1Password lançaram acesso agêntico a credenciais: Claude completa tarefas logadas (reservas, contas, browser) com credenciais injetadas em runtime, sem o modelo ver o segredo (arquitetura zero-exposure). VERIFICADO: anúncio oficial 1Password/Anthropic de 16/07. Diferencial vs TecMundo (que só deu a notícia crua): o ângulo dev — shell plugin do Claude Code, segredos fora do contexto do agente, MCP + 1Password, superfícies de ataque e limites. PAA do Google já pergunta "How to use 1Password with Claude Code". Links internos: claude-code-preco-2026, anthropic-verificacao-de-identidade-claude.
- hook: Dar sua senha pra uma IA é pesadelo de segurança. A 1Password e a Anthropic dizem ter resolvido: o Claude loga por você sem nunca ver a credencial. Como isso funciona por baixo?
- bullets:
  - O que foi lançado: 1Password for Claude e o "Agentic Mode" explicados
  - Zero-exposure na prática: como a credencial chega no browser sem passar pelo modelo
  - Pra dev: Claude Code + 1Password (shell plugin, API keys fora do contexto, MCP)
  - O que pode dar errado: limites, superfícies de ataque e o que a 1Password promete
  - Vale ativar? Cenários reais de uso (e quando não usar)
- keyword_principal: 1password claude
- keywords_secundarias: claude 1password, claude faz login sozinho, 1password for claude, claude code 1password
- tags: ia, claude, anthropic, seguranca-ia, agentes
- dificuldade: easy
- volume: ~0 BR (termo de ~24h), KD n/a; notícia crua já coberta por portal generalista — o ângulo dev é a brecha

## IPO da Anthropic em outubro: o que muda pra quem usa Claude (preços, limites e o risco Kimi K3)
- publicar_em: 2026-07-17T19:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A Anthropic agendou reuniões com investidores mirando IPO em 22/10/2026 (TradingView), após avaliação de ~US$ 965B. VERIFICADO: S-1 confidencial (junho), reuniões com investidores (CNBC, 16/07), data-alvo. RUMOR: precificação final e ticker. Diferencial: a SERP é 100% finanças (WSJ, InfoMoney, B3) — nosso ângulo é o dev: pressão por receita → o que pode acontecer com preço do Claude Code, limites de uso, foco enterprise, e a tensão com modelos abertos 5x mais baratos (Kimi K3, GLM 5.2) espremendo a avaliação. Formato vivo: atualizar no anúncio formal. Links internos: claude-code-preco-2026, codex-limite-de-uso, kimi-k3 (post do dia), anthropic-acesso-bloqueado-brasil.
- hook: A empresa por trás do Claude quer abrir capital em outubro avaliada em quase US$ 1 trilhão — no mesmo mês em que um modelo aberto chinês bateu o Opus custando 5x menos. Pra quem paga assinatura, isso importa (muito).
- bullets:
  - O que está confirmado: S-1, reuniões com investidores e a data-alvo de 22/10
  - US$ 965 bilhões: de onde vem essa avaliação (e por que ela está sob ataque)
  - O efeito Kimi K3/GLM: modelos abertos espremendo o preço da inteligência
  - O que muda pra quem usa Claude: preços, limites e foco enterprise pós-IPO
  - Dá pra investir do Brasil? A resposta curta (e o alerta de golpe pré-IPO)
- keyword_principal: anthropic ipo
- keywords_secundarias: ipo anthropic, anthropic ipo data, anthropic abre capital, ipo da anthropic vale a pena
- tags: ia, anthropic, claude, mercado, ipo
- dificuldade: medium
- volume: 480/mês oficial mas 2.900 em junho e acelerando (+303% m/m), competição LOW, KD n/a; intenção navigational/informational — mirar long-tail "o que muda" onde a SERP financeira não compete
