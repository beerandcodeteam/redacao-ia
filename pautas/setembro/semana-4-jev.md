# Batch setembro semana-4 — cluster Jev / TypeSafe AI (21/09/2026)
# Entrada para a skill `criar-posts-batch` (workflow), não para o criar-posts-batch.py.
#   O Parse do workflow é um agente e LÊ `bullets` e `volume` — por isso aqui eles
#   são campos de verdade, não texto embutido no resumo.
#
# Fonte: caçada de news-jacking de 21/09/2026 (detect.sh + DataForSEO + GSC).
# Gatilho: TypeSafe AI saiu de 2 anos de stealth em 15/09/2026 com o Jev, primeiro
#   "System One model". Fundada por co-criador do ChatGPT/RLHF, $40M de seed (DCVC).
#   Em 18/09 virou o modelo de adoção mais rápida da história do Vercel AI Gateway.
#
# CTA fixo dos 3 posts → Clã Beer and Code, https://beerandcode.com.br (passado via args.cta)
#
# ⚠️ AS TRAVAS "NÃO CANIBALIZAR" NÃO SÃO DECORATIVAS. Medidas na SERP BR em 21/09:
#   - `o que é jev` × `quando usar jev em vez de llm` servem 3 domínios em comum
#     (eigent.ai, meetcody.ai, aihubmix) → posts 1 e 3 brigam se não forem disjuntos.
#   - `laya vs jev` tem ZERO domínio orgânico em comum com os outros dois → post 2 livre.
#   - O post existente `classificacao-de-intencao-llm-roteamento-de-agente` (02/09) cobre
#     roteamento de intenção — o caso de uso nº1 do Jev. O post 3 NÃO pode reescrevê-lo.
#
# Fontes verificadas (base da pesquisa do passo 1):
#   https://typesafe.ai/blog/introducing-system-one-models-and-jev  (anúncio oficial)
#   https://dev.to/valyuai/how-to-use-jev-a-practical-guide-to-typesafes-system-one-model-g5e
#   https://www.langchain.com/blog/building-a-harness-with-jev
#   https://huggingface.co/convaiinnovations/laya  |  https://github.com/NandhaKishorM/laya
#   https://news.ycombinator.com/item?id=49765348  (thread da disputa de anterioridade)
#   https://danielmiessler.com/blog/early-thoughts-on-jev
#
# Números confirmados para reuso (NÃO inventar outros):
#   Jev: 70–500ms ponta a ponta | $0,042/MTok entrada | output grátis | até 255 opções
#        | 0% erro de tipo | RLCD | early access desde 15/09/2026 | infra na costa oeste EUA
#   Laya: 421M params (ModernBERT-large) | Apache 2.0 | 32,8ms P50 | ECE 0,081 vs 0,246 do Jev
#        | AG News 0,950 vs 0,910 | custo zero (self-host) | pip install laya

## Jev: o modelo de IA que não escreve nada — e por isso custa 100x menos
- publicar_em: 2026-09-21T11:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Post-hub do cluster Jev. Explica O QUE É e COMO CHAMAR o primeiro "System One model", lançado pela TypeSafe AI em 15/09/2026. Ele não gera texto: recebe o estado do programa mais perguntas tipadas e devolve escolha, nota ou probabilidade numa única passagem paralela — por isso não consegue alucinar, a garantia é de tipo e não de prompt. Precisa ter código Python rodando de verdade, não pseudocódigo.
- hook: Todo mundo passou três anos tentando fazer LLM devolver JSON válido. A TypeSafe olhou pro problema e perguntou outra coisa: e se o modelo simplesmente não pudesse escrever?
- bullets:
  - O que é um System One model (e por que ele não consegue alucinar)
  - O que muda quando você tira a autoregressão — 70-500ms, $0,042/MTok, output grátis
  - Choice, Score e Noul: os três primitivos com código Python rodando
  - Fan-out especulativo: por que a décima pergunta é quase de graça
  - As 5 armadilhas: literalidade extrema, zero aritmética, datas como texto, context rot, sem geração
- keyword_principal: o que é o jev ia
- keywords_secundarias: modelo jev, jev typesafe ai, system one model, jev python, jev preço
- tags: ia, llm, modelos-de-ia, ai-agents, custos, noticias
- volume: ~0 buscas BR (termo não existe na base do DataForSEO — normal em termo de 6 dias), KD n/d. SERP de `jev ia modelo` sem featured snippet, sem PAA próprio e sem AI Overview: janela aberta. Keyword deliberadamente `o que é o jev ia` e NÃO `o que é jev`: o termo cru está contaminado na SERP BR (gíria californiana no Reddit, Jogos Estudantis Valadarenses da UFJF) e já tem AI Overview montado. NÃO CANIBALIZAR: este post é o HUB conceitual + hands-on de chamada. É PROIBIDO ter seção "onde usar", "quando compensa" ou catálogo de casos de uso — isso é exclusivo do post `10 lugares onde trocar o LLM pelo Jev`; fecha com UMA frase e link pra ele. Também é proibido comparar com o Laya além de uma menção de uma linha com link pro post `Laya vs Jev`. LINKS INTERNOS obrigatórios: os dois posts irmãos deste batch e `o-que-e-um-llm-explicacao-para-quem-vai-construir`.

## Laya vs Jev: a IA de decisão de $40 milhões contra a de graça que roda no seu notebook
- publicar_em: 2026-09-21T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Comparativo cabeça a cabeça entre o Jev (API paga, $40M de seed) e o Laya (Apache 2.0, 421M de parâmetros, roda offline). Dois dias depois do Jev sair do stealth, o autor do Laya apareceu no Hacker News alegando ter publicado a mesma arquitetura em março de 2025, com pesos, dataset e paper abertos. O post registra os dois lados da disputa sem arbitrar e compara os números publicados de cada um. MARCAR EXPLICITAMENTE NO TEXTO: VERIFICADO = lançamento, preço, licença e benchmarks publicados por cada lado; EM DISPUTA = a acusação de anterioridade, que o post registra sem julgar. Formato vivo — deixar o texto preparado para atualização conforme a briga evolui.
- hook: Seis dias de vida, $40 milhões de seed, e o Jev já tem um concorrente Apache-2.0 que roda offline e é 7x mais rápido no P50. A pergunta não é qual é melhor. É por que ninguém tinha percebido que esse trabalho não precisava de um LLM.
- bullets:
  - A thread do Hacker News — o que o autor do Laya publicou em março de 2025
  - Jev por dentro: RLCD, 70-500ms, $0,042/MTok, até 255 opções
  - Laya por dentro: 421M no ModernBERT-large, 32,8ms no P50, ECE 3x melhor, custo zero
  - Onde o Laya apanha: mais de 20 opções, precisa de fine-tuning e calibração por domínio
  - API paga vs self-hosted: a conta real por volume de chamadas
- keyword_principal: laya vs jev
- keywords_secundarias: jev open source, alternativa open source ao jev, laya typesafe, modelo system one open source
- tags: ia, llm, modelos-de-ia, modelos-open-source, benchmark, custos, noticias
- volume: ~0 buscas BR, KD n/d. Top 10 da SERP BR 100% em INGLÊS (Medium, Hacker News, Hugging Face, LinkedIn, Facebook) — zero concorrência em pt-BR. É o post mais ganhável dos três: brecha de idioma pura. ZERO domínio orgânico em comum com as SERPs dos outros dois posts, então não há risco de canibalização interna. NÃO CANIBALIZAR: não reexplicar o que é um System One model além de dois parágrafos de contexto com link pro post `Jev: o modelo de IA que não escreve nada`; aqui o assunto é a COMPARAÇÃO e a DISPUTA, não o fundamento.

## 10 lugares onde trocar o LLM pelo Jev paga a migração em uma semana
- publicar_em: 2026-09-21T15:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Catálogo de decisão. Dez tarefas que hoje rodam em LLM caro, o que cada uma custa por milhão de chamadas antes e depois, o payload real e a condição em que a migração NÃO vale. Os 10 casos: triagem de ticket, moderação de conteúdo, guardrail de saída de outro LLM, tagging de sessão, filtro pré-RAG, scoring de lead, detecção de churn, eval automatizado, classificação de severidade de bug e roteamento de modelo dentro do pipeline. Cada caso precisa de número, não de adjetivo.
- hook: A tarefa mais cara do seu pipeline provavelmente é a mais burra dele: decidir se um ticket é de billing ou de bug. Você paga modelo de fronteira pra isso.
- bullets:
  - O critério de 30 segundos — a pergunta cabe em escolha, nota ou sim/não?
  - Os 10 casos com a conta antes e depois
  - O padrão cascata: Jev na frente, LLM caro só quando sobra ($6.480 vs $30.400 por milhão de tickets)
  - Como medir se a migração deu certo sem rotular dez mil exemplos na mão
  - As 4 tarefas em que o Jev é a escolha errada: geração, contagem, auditoria e raciocínio de passo único
- keyword_principal: substituir llm por jev
- keywords_secundarias: quando usar jev em vez de llm, jev casos de uso, reduzir custo de classificação com ia, jev ou llm
- tags: ia, llm, ai-agents, custos, arquitetura, evals, tutoriais
- volume: ~0 buscas BR, KD n/d. SERP de `quando usar jev em vez de llm` tem AI Overview, mas só dois concorrentes pt-BR de aplicação (TabNews e Hora de Codar) — janela ainda aberta. NÃO CANIBALIZAR — DUAS TRAVAS OBRIGATÓRIAS: (1) este post NÃO explica o que é o Jev, não tem seção de fundamento e não descreve os primitivos do zero; abre pressupondo o conhecimento, com link pro post `Jev: o modelo de IA que não escreve nada` na primeira linha — a SERP mostra 3 domínios em comum entre as duas intenções, então a separação é o que decide se os dois rankeiam ou nenhum. (2) roteamento de INTENÇÃO de agente NÃO entra como um dos 10 casos próprios e NÃO pode ser desenvolvido aqui — o post `classificacao-de-intencao-llm-roteamento-de-agente` já ocupa essa intenção desde 02/09; citar em uma linha e linkar. O décimo caso é roteamento de MODELO (escolher qual LLM chamar), que é coisa diferente — deixar a distinção explícita no texto para o leitor e para o Google. LINKS INTERNOS obrigatórios: os dois posts irmãos, `classificacao-de-intencao-llm-roteamento-de-agente`, `reduzir-custo-api-de-ia` e `evals-para-agentes-de-ia-llm-as-a-judge`.
