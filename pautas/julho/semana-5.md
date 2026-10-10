# Pautas — semana 5 de julho/2026 (caçada de técnica: integração de agentes)

Origem: `cacar-news-jacking` (24/07/2026, foco "técnica nova que muda a integração de agentes").
Aprovadas pelo Lucas para criação E PUBLICAÇÃO (goal: publicar posts 1-4).

## Harness engineering não basta: o manifesto que explica por que as "fábricas de software" com IA falham
- publicar_em: 2026-07-25T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO (repo público da HumanLayer, HN 373 pts em 23/07). O manifesto
  "Why Software Factories Fail" ataca a promessa do momento: harness + loops dão
  velocidade, mas nenhum modelo mantém qualidade de código sem humano no loop — porque
  o RL otimiza contra "testes passam em segundos" e não pune arquitetura ruim que só
  aparece em semanas ("there is no penalty for eroding codebase maintainability"). A
  resposta proposta é Advanced Context Engineering: 4 fases de planejamento (product
  review, system architecture, program design, vertical slices), review ANTES do código,
  expectativa realista de 2-3x (não 10-100x); ~40% das tarefas seguem oneshot, 60% ganham
  estrutura. Fechar com o arco: 33k tokens de overhead do Claude Code antes de ler o
  prompt (HN 705 pts, systima.ai) → Anthropic corta 80% do system prompt pro Claude 5 —
  o harness está emagrecendo e o contexto virou o trabalho. Fonte primária:
  https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/wsff.md
  Links internos: subagentes-na-pratica-dividindo-contexto-token-budget,
  claude-code-monorepo, claude-md-clausulas-karpathy.
- hook: Todo mundo no Brasil está aprendendo o que é harness engineering — Alura,
  Databricks e metade do YouTube dev. Aí o manifesto mais votado da semana no HN chega
  dizendo: harness não basta, e as fábricas de software 100% autônomas estão quebrando.
  Quem tá certo?
- bullets:
  - A promessa da "software factory" e por que ela está falhando na prática
  - A raiz: RL premia teste verde em segundos e ignora a arquitetura que apodrece em semanas
  - Advanced Context Engineering: as 4 fases de planejamento que substituem o "oneshot e reza"
  - Vertical slices e review antes do código: o fluxo na prática (com o realismo dos 2-3x)
  - O arco completo: dos 33k tokens de overhead ao corte de 80% do system prompt — pra onde o harness vai
- keyword_principal: harness ia
- keywords_secundarias: harness engineering, context engineering, advanced context engineering, engenharia de contexto, software factory ia
- tags: ai-agents, harness, contexto, agentic-code, claude-code
- dificuldade: medium
- volume: 390/mês BR em "harness ia" (pico 1.900 em maio, KD 9) + 720/mês "context engineering" (KD 39); SERP dominada pelo ângulo "o que é" (Alura/Databricks/Distrito) — entramos pelo ângulo contrário, que ninguém tem

## Este modelo local sabe quando está errado — e chama a nuvem sozinho: por dentro do Cactus Hybrid
- publicar_em: 2026-07-25T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO (repo cactus-compute/cactus-hybrid, HN 185 pts em 22/07). A Cactus
  pós-treinou o Gemma 4 com "probes" de confiança embutidas no checkpoint: cada geração
  sai com score 0-1 estruturado (não extraído do texto da resposta), e abaixo do
  threshold (ex.: 0,85) a query roteia pro modelo grande na nuvem. Resultado: Gemma 4
  E2B Hybrid iguala o Gemini 3.1 Flash-Lite roteando só 15-55% das queries (ChartQA
  15-20%, MMBench 30-35%, MMLU-Pro 45-55% de handoff; AUROC 0,814 vs 0,549 da entropia
  de tokens). É um padrão novo de integração — local-first com escalonamento por
  confiança — que muda a conta de custo, latência e privacidade de qualquer app com LLM.
  Mostrar o snippet `if confidence < 0.85: answer = ask_a_bigger_model(prompt)` e a
  conta de custo. Fonte: https://github.com/cactus-compute/cactus-hybrid
  Link interno: claude-opus-4-8-vs-minimax-m3-vs-qwen-3-local.
- hook: O maior defeito de rodar modelo pequeno local nunca foi a qualidade média — foi
  ele errar com a mesma confiança com que acerta. A Cactus atacou exatamente isso: um
  Gemma 4 que devolve a resposta E o quanto confia nela. Quando a confiança cai, a nuvem
  entra. Só quando precisa.
- bullets:
  - O problema real do on-device: errar sem avisar
  - Como funciona a probe de confiança embutida no checkpoint (e por que não é "pedir pro modelo se avaliar")
  - Os números: igualar o Flash-Lite roteando 15-55% das queries (AUROC 0,814)
  - O padrão de integração: local-first + threshold + fallback — com o código do router
  - A conta: quanto isso corta de custo de API (e onde o padrão quebra)
- keyword_principal: cactus hybrid
- keywords_secundarias: modelo local que sabe quando erra, llm local vs nuvem, roteamento por confiança llm, gemma 4 on-device
- tags: llm, modelos-open-source, ia, ai-engineer, custos
- dificuldade: easy
- volume: ~0 BR, sem KD (nasceu há 48h); zero conteúdo PT — janela de chegar primeiro; tema de fundo (local vs nuvem) tem demanda durável

## Screenpipe grava tudo que você faz no PC e transforma em agentes — genial ou pesadelo de privacidade?
- publicar_em: 2026-07-25T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO (Launch HN YC S26, 23/07, +82 pts). O Screenpipe grava como você
  trabalha — eventos do SO (troca de app, cliques, pausas de digitação), screenshot +
  árvore de acessibilidade só quando algo muda, OCR como último recurso, áudio
  transcrito local (Parakeet/Whisper) — e transforma esses procedimentos em agentes que
  repetem seu fluxo. Tudo local: SQLite + MP4 + Markdown, API na porta 3030, stack Rust
  (MLX/ONNX), modelo próprio de redação de PII rodando com <1% CPU e <400 MB RAM.
  Paradigma: agente aprendido por demonstração, não por prompt — o contexto vem do seu
  trabalho real, não de um MCP estático. Cobrir também a treta: licença saiu de MIT pra
  source-available (comunidade FOSS reclamou), o alerta "nenhuma corporação sã permite
  isso" (EU AI Act) e a pergunta de segurança "o que impede um agente comprometido de
  ler todo o histórico?" (resposta: permissões por timeframe/modalidade). Marcar
  claramente o que é claim do fundador vs verificado. Fonte:
  https://news.ycombinator.com/item?id=49024620
  Links internos: 1password-for-claude (credenciais/agentes), claude-code-malware-repo-limpo
  (superfície de ataque de agente).
- hook: E se em vez de escrever prompt você só... trabalhasse, e o agente aprendesse
  olhando? É a aposta do Screenpipe: gravar sua tela o dia inteiro — localmente — e
  destilar seus procedimentos em agentes. A ideia é genial. As implicações são o motivo
  de metade do Hacker News estar em pânico.
- bullets:
  - O paradigma novo: agente por demonstração, não por prompt
  - Como a captura funciona por baixo (eventos do SO, acessibilidade, OCR de último recurso)
  - Privacidade: o que fica na máquina, o redator de PII e o que o EU AI Act tem a dizer
  - A treta da licença: de MIT pra source-available — e por que a comunidade FOSS reclamou
  - Vale usar? Cenários reais (SOP de time, onboarding, automação pessoal) e onde é cedo demais
- keyword_principal: screenpipe
- keywords_secundarias: screenpipe o que é, gravar tela com ia, agente de ia por demonstração, automatizar trabalho repetitivo com ia
- tags: ai-agents, agentes, produtividade, privacidade, ferramentas-de-ia
- dificuldade: easy
- volume: ~0 BR (produto lançou ontem); zero conteúdo PT; brand-keyword de cauda que cresce com o produto (YC S26)

## Se a IA escreve o código, a linguagem precisa mudar: Jacquard e a função que declara o que pode tocar
- publicar_em: 2026-07-25T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO (repo jbwinters/jacquard-lang, HN 102 pts em 13/07; v0.1 é release
  candidate de PESQUISA, não produção — deixar explícito). Jacquard é uma linguagem
  desenhada pro mundo onde a máquina escreve e o humano revisa: cada função declara os
  efeitos que pode executar na assinatura — `(text) ->{net} text` = pode tocar rede — e
  o runtime recusa qualquer efeito não autorizado via `--allow`, inclusive em código
  carregado dinamicamente. Revisor lê a assinatura, não o corpo: "what can this touch,
  and how sure are we". Extras: identidade por hash da estrutura canônica (comentário/
  formatação não mudam identidade — diff semântico), handlers multi-shot pra teste
  exaustivo, compilador OCaml que emite C, 794 testes. Ângulo: é o guardrail descendo do
  harness pra DENTRO da linguagem — a review de código de IA vira auditoria de
  capacidades. Fonte: https://github.com/jbwinters/jacquard-lang
  Links internos: pipeline-revisao-pr-github-actions-claude (review de código IA),
  claude-code-malware-repo-limpo (por que capability matters).
- hook: Seu code review de código gerado por IA tem um problema: você lê o diff, mas não
  sabe o que aquela função PODE fazer. A Jacquard inverte o jogo — a assinatura declara
  "essa função toca rede e disco" e o runtime bloqueia o resto. Não é linguagem pra você
  escrever. É linguagem pra IA escrever e você confiar.
- bullets:
  - O problema: revisar código de IA lendo corpo por corpo não escala
  - Efeitos na assinatura: `->{net}` como manifesto de autoridade da função
  - Runtime que nega por padrão: --allow explícito até pra código dinâmico
  - Identidade por hash canônico: diff que ignora cosmética e enxerga semântica
  - É pesquisa (v0.1), mas a ideia vai vazar pras linguagens que você já usa — o que observar
- keyword_principal: jacquard linguagem
- keywords_secundarias: linguagem de programação para ia, código gerado por ia review, effect system, capability based security
- tags: ai-agents, agentic-code, code-review, seguranca-ia, engenharia-de-software
- dificuldade: easy
- volume: ~0 BR (nicho novo); zero conteúdo PT; aposta de autoridade no pilar "código escrito por IA"
