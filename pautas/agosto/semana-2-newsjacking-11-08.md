# Pautas — semana 2 de agosto/2026 (caçada de news-jacking)

Origem: `cacar-news-jacking` (11/08/2026, foco default: IA aplicada / LLMs / coding agents).
Sinais: detect.sh (HN, OpenRouter, GitHub, Reddit OAuth, NewsAPI) + GSC 14d + DataForSEO + SERP BR.
CTA: todos os 4 posts levam link para https://beerandcode.com.br/ (decisão do Lucas, 11/08).

Ordem de publicação: TODOS em 11/08 (decisão do Lucas — news-jacking não sobrevive a fila de 3 dias).
Watermark 09h (backdatado, publicado 11:31) → Muse Glimmer 12h → Riemann 15h → Patente Mistral 17h.

Fora desta pauta, atualizar posts existentes: `openai-astra-rastreador` (OpenAI pausou o Astra),
`claude-hackeou-3-empresas` (academia AU), `deepseek-v4-flash-0731` (US$ 0,14/M tokens).

---

## Claude agora assina tudo que escreve: a marca d'água invisível que sobrevive ao copia-e-cola
- publicar_em: 2026-08-11T18:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO — a Anthropic passou a embutir marca d'água imperceptível em todo texto gerado
  pelos modelos Claude lançados na UE a partir de 02/08/2026, mais metadados assinados em arquivos.
  O anúncio saiu só num artigo de suporte (support.claude.com, "Como Claude marca conteúdo gerado
  por IA"), sem post no blog oficial da Anthropic — isso é parte do gancho. Post explica o que é
  (não é caractere invisível de largura zero), se pega na API e no Claude Code, o que a detecção
  realmente prova, e testa na prática se copiar/colar/traduzir remove. Formato vivo: atualizar
  conforme a Anthropic expandir para fora da UE.
  Fontes: support.claude.com (artigo oficial, 10/08); TudoCelular 11/08; antihype.com.br 10/08.
- hook: A Anthropic não anunciou no blog. Escondeu num artigo de suporte. E desde 2 de agosto, todo
  texto que o Claude escreve pra você sai com uma assinatura que você não vê — e que o Ctrl+C não apaga.
- bullets:
  - O que é a marca d'água do Claude (e por que não é o "caractere invisível" que você já viu)
  - Pega na API e no Claude Code? O que muda pra quem gera conteúdo em escala
  - Só na União Europeia? O recorte de 02/08/2026 e o que isso significa no Brasil
  - Testamos: copiar, colar, reescrever e traduzir — a marca sobrevive?
  - O que a detecção prova (e o que ela NÃO prova) antes de você acusar alguém
- keyword_principal: marca d'água claude texto
- keywords_secundarias: como remover marca d'água do claude, claude marca d'água api, claude watermark detector, anthropic marca d'água invisível, claude marca d'água união europeia
- tags: anthropic, claude, ia, seguranca, regulacao
- dificuldade: easy
- volume: sem dados no DataForSEO (termo de 18h), mas demanda provada na SERP — o #4 orgânico é um
  removedor de marca d'água com 1.247 avaliações. Janela fechando: TudoCelular publicou há 3h e
  antihype há 15h, nenhum com tratamento técnico. Atacar a cauda longa, não o head.

## Muse Glimmer 30B cabe mesmo numa RTX 3090? A Meta diz uma coisa, quem testou diz outra
- publicar_em: 2026-08-12T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO — a Meta Superintelligence Labs soltou o Muse Glimmer, modelo denso de 30B com
  pesos abertos sob Apache 2.0 e encoder de percepção de 1,8B para entrada de imagem, otimizado
  para workflows de agente locais. A imprensa BR (TecMundo) diz que "ainda requer um PC poderoso";
  a comunidade do r/LocalLLaMA afirma rodar numa única RTX 3090 e bater o 3.6-27B. Post resolve a
  contradição com números de VRAM por quantização e tokens/s reais, e compara com o Qwen 3.8.
  Fontes: developer.meta.com (oficial); CNBC 10/08; ollama.com/blog/muse-glimmer; unsloth.ai;
  AMD e NVIDIA developer blogs (10/08); r/LocalLLaMA (threads de 10-11/08).
- hook: O TecMundo disse que precisa de um PC poderoso. O r/LocalLLaMA disse que cabe numa 3090 e
  ainda bate o 3.6-27B. Os dois não podem estar certos — então fomos atrás do número.
- bullets:
  - O que a Meta entregou de fato: 30B denso, Apache 2.0, encoder de imagem de 1,8B
  - A conta de VRAM: quanto o Glimmer come em FP16, Q8 e Q4 — e onde ele estoura numa 3090
  - Tokens/s real: o que NVIDIA e AMD prometem vs. o que a comunidade mediu
  - Muse Glimmer vs Qwen 3.8: qual dos dois merece o seu disco
  - Como rodar hoje no Ollama e no Unsloth, passo a passo
- keyword_principal: muse glimmer rtx 3090
- keywords_secundarias: muse glimmer requisitos, muse glimmer como rodar local, muse glimmer vs qwen 3.8, muse glimmer 30b português, muse glimmer quantização
- tags: meta, ia, llm-local, hardware, ollama
- dificuldade: medium
- volume: sem dados no DataForSEO (24h de vida). O head "muse glimmer" já está tomado por Meta,
  TecMundo, Exame, Ollama, AMD e NVIDIA — a jogada é a cauda longa. GSC mostra 550 impressões em
  "muse code" na posição 7,9: o cluster Muse já traciona no domínio. Link interno obrigatório para
  o post muse-code-meta-terminal-bench.

## Claude empurrou a hipótese de Riemann de 41,6% para 67,2% — e o GPT-5.6 Sol respondeu com 0,002%
- publicar_em: 2026-08-12T15:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO — a Anthropic publicou resultados sobre as capacidades matemáticas do Claude,
  incluindo o aumento do limite inferior da fração de zeros da função zeta que satisfazem a
  hipótese de Riemann, de 41,6% para 67,2%. Em seguida, um usuário do GPT-5.6 Sol reivindicou
  melhora de 0,002% sobre o resultado. Post explica o que foi realmente provado, o que não foi, e
  por que a briga entre os labs importa menos que a metodologia. Cuidado editorial: "a IA resolveu
  Riemann" é manchete errada e o post precisa desmontar isso explicitamente.
  Fontes: post oficial da Anthropic sobre capacidades matemáticas (HN 230 pts); r/singularity
  (threads de 10-11/08, 1012 e 377 ups).
- hook: Um limite matemático que levou décadas para sair do lugar andou 25 pontos em um paper. Aí a
  torcida do outro lab apareceu com 0,002% a mais — e a discussão virou sobre quem chegou primeiro,
  não sobre o que foi provado.
- bullets:
  - O que a hipótese de Riemann afirma (em português, sem pré-requisito)
  - O que o Claude provou de fato: 41,6% → 67,2% e o que esse número significa
  - Como o resultado foi obtido — e por que "a IA resolveu Riemann" é manchete errada
  - A resposta do GPT-5.6 Sol: 0,002% é avanço ou é ruído de disputa?
  - O que muda pra quem usa LLM em problema difícil de verdade
- keyword_principal: claude hipótese de riemann
- keywords_secundarias: ia resolveu hipótese de riemann, claude matemática riemann, gpt 5.6 sol riemann, claude função zeta, ia prova matemática 2026
- tags: anthropic, claude, openai, ia, pesquisa
- dificuldade: medium
- volume: sem dados no DataForSEO. Formato já validado no blog duas vezes (fable-5-conjectura-jacobiana,
  gpt-5-6-conjectura-de-maxwell — "conjectura de jacobiano" pinga em pos 9,8 no GSC). Riemann é
  problema distinto, então não canibaliza: linkar os três posts como série.

## A Mistral patenteou a chamada de ferramenta por código — e o seu agente está no meio disso
- publicar_em: 2026-08-13T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO — veio à tona uma patente da Mistral sobre "code implemented tool calls", o
  padrão em que o modelo escreve código que invoca ferramentas em vez de emitir JSON de tool call.
  É exatamente o mecanismo por trás de boa parte dos coding agents em produção hoje (inclusive o
  programmatic tool calling da própria Anthropic). Post explica o que a patente cobre, o que ela
  provavelmente não cobre, prior art, e o risco real (ou a falta dele) para quem constrói agente.
  Zero cobertura em português até agora — janela totalmente aberta.
  Fonte: discussão no Hacker News (223 pts, 10/08) + o documento da patente. IMPORTANTE: ler a
  patente na fonte primária antes de escrever; não confiar no resumo do HN.
- hook: Se o seu agente pede pro modelo escrever Python que chama as suas funções em vez de cuspir
  JSON, você está usando o padrão que a Mistral acaba de reivindicar como invenção.
- bullets:
  - O que é "code implemented tool call" e por que virou o padrão dos coding agents
  - O que a patente da Mistral reivindica, cláusula por cláusula, em português
  - Prior art: quem já fazia isso antes — e por que isso importa
  - O risco prático pra quem roda agente em produção no Brasil
  - Alternativas de arquitetura se você quiser dormir tranquilo
- keyword_principal: mistral patente tool call
- keywords_secundarias: code implemented tool calls, patente chamada de ferramenta ia, mistral patente agentes, tool calling patente, agente ia patente mistral
- tags: mistral, ia, agentes, arquitetura
- dificuldade: hard
- volume: sem dados no DataForSEO e zero concorrência em português — janela totalmente aberta.
  Volume baixo por natureza, mas é o candidato de maior fit com o pilar de agentes e o de menor
  risco de alguém chegar antes.
