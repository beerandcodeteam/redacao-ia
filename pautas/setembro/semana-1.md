# Pauta — semana de 31/08 a 02/09/2026

Origem: `planejar-pauta` (31/08/2026). Vertente: engenharia de IA aplicada / arquitetura
de agentes — derivada dos 11 módulos do **AI Engineering Lab 3ª Edição** (19–20/09/2026,
`https://beerandcode.com.br/landing-pages/ai-engineering-lab`).

**Objetivo do ciclo:** quick wins. Evento em 19/09 — prioridade para KD baixo e clusters
onde o domínio já tem tração.

**Estes 9 passaram por dedup contra o acervo** (busca híbrida no MCP do blog + cruzamento
com as 130 páginas do GSC). São os únicos temas da vertente sem post equivalente
publicado. Cada entrada traz a linha `delimitacao:` — o que NÃO escrever, para não
sobrepor post existente.

A rodada original tinha 21 temas. Os 12 cortados viraram
[`refresh-setembro-semana-1.md`](refresh-setembro-semana-1.md), porque já existiam no
blog com o mesmo ângulo — e estão parados, o que rende mais em refresh do que em post
novo.

**Cortado antes do dedup:** cluster `claude code` (head KD 67, top 10 com média de 132.492
backlinks), `guardrails` (22.200/mo mas é guarda-corpo rodoviário), `prompt engineering`
em inglês (navigational, KD 35), `chatbot com ia` e `ia para empresas` (CPC R$ 17–20,
intenção de agência), `model context protocol` (KD 70, −70% a/a), `mcp` (KD 69).

---

## Engenharia de prompt acabou. O que veio depois se chama engenharia de contexto
- publicar_em: 2026-08-31T14:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Hub da head keyword do cluster. Entrega o que a busca pede (as técnicas que
  funcionam) e reposiciona: em sistema real o problema não é a frase, é o que entra na
  janela. Puxa link para os três posts de contexto que já existem e estão sem tráfego.
- hook: Ninguém mais ganha dinheiro escrevendo prompt bonito. Ganha quem decide o que
  entra na janela de contexto — e o que fica de fora.
- bullets:
  - As técnicas que sobreviveram (e as que viraram folclore)
  - Por que prompt bom não salva contexto ruim
  - O que realmente entra na janela: ordem, corte, recência
  - Prompt de sistema vs. instrução de turno
  - Do prompt à arquitetura: o que muda quando vira produto
- keyword_principal: engenharia de prompt
- keywords_secundarias: técnicas de prompt, prompt de sistema, prompt engineering português
- tags: ia, llm, prompt, contexto, arquitetura
- dificuldade: easy
- volume: 9.900/mo (KD 5, −45%/ano — ainda 5 dígitos)
- delimitacao: é o HUB da head `engenharia de prompt`, não um post de contexto. Não
  reescrever `engenharia-de-contexto-o-que-vai-no-prompt` (o que entra/sai da janela),
  `ferramentas-de-engenharia-de-contexto-em-producao` (ferramental) nem
  `limite-de-tokens-chatgpt-ia-esquece` (estouro de janela) — linkar para os três.

## O que é um LLM (a explicação que serve para quem vai construir, não para quem vai postar)
- publicar_em: 2026-08-31T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Fundamento sem analogia de papagaio: tokens, probabilidade, janela, temperatura
  e por que o modelo é stateless. A base que faz os outros posts do blog fazerem sentido
  e o ponto de entrada natural do cluster.
- hook: Você não precisa entender transformer pra usar um LLM. Precisa entender três
  coisas — e nenhuma delas é transformer.
- bullets:
  - O que o modelo realmente faz a cada token
  - Por que ele é stateless (e o que isso te obriga a construir)
  - Janela de contexto: o recurso que você administra
  - Temperatura, top-p e a ilusão de controle
  - O que isso significa na hora de arquitetar
- keyword_principal: o que é llm
- keywords_secundarias: llm o que é, large language model, como funciona um llm
- tags: ia, llm, fundamentos, arquitetura
- dificuldade: easy
- volume: 9.900/mo (KD 25, +22%/ano)
- delimitacao: não virar dicionário — `glossario-ai-engineer-2026-30-termos` e
  `glossario-ai-engineer-vol-2-2026` já ocupam esse formato. Aqui é fundamento operacional
  de um conceito só, com consequência de arquitetura em cada seção.

## Fine-tuning, RAG ou prompt: qual dos três o seu problema pede
- publicar_em: 2026-08-31T20:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A decisão que mais gente erra pra cima. Critério objetivo pra escolher entre os
  três, quanto custa cada caminho, e por que fine-tuning quase nunca é a resposta em 2026.
  É o framework de decisão do módulo 1 do Lab, numa keyword de KD 4.
- hook: "Vamos treinar um modelo nosso." Ok — me diz o que você tenta ensinar que um bom
  contexto não resolveria por 3% do preço.
- bullets:
  - O que cada um realmente muda no comportamento
  - A árvore de decisão em 4 perguntas
  - Quanto custa cada caminho, com números
  - Os 3 casos raros em que fine-tuning ganha
  - O erro clássico: treinar pra resolver problema de recuperação
- keyword_principal: fine tuning
- keywords_secundarias: rag vs fine tuning, fine tuning llm, quando usar fine tuning
- tags: ia, llm, rag, fine-tuning, arquitetura
- dificuldade: medium
- volume: 2.900/mo (KD 4)
- delimitacao: é post de DECISÃO com custo, não explicação de RAG. `o-que-e-rag` já cobre
  "onde RAG termina e a memória (e o fine-tuning) começam" — linkar, não repetir.

## LangGraph, Mem0, LangChain, MCP: do que você realmente precisa
- publicar_em: 2026-09-01T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Mapa honesto do ecossistema de orquestração e memória — o que cada uma resolve,
  o que cobra em complexidade, e o ponto em que deixa de ser overhead. Com o caso em que
  a resposta é "nenhuma delas".
- hook: Você abriu 6 abas de documentação e ainda não escreveu uma linha. O problema não
  é escolher a ferramenta errada — é achar que precisa de uma.
- bullets:
  - O que cada uma faz, em uma frase, sem marketing
  - Orquestração: quando LangGraph paga o próprio peso
  - Memória: Mem0 vs. uma tabela no Postgres
  - MCP: o que mudou e o que ainda é hype
  - A árvore de decisão: 5 perguntas antes de instalar qualquer coisa
- keyword_principal: langgraph
- keywords_secundarias: langgraph vale a pena, mem0, langchain alternativa, ferramentas para agentes de ia
- tags: ai-agents, llm, arquitetura, ferramentas, mcp
- dificuldade: medium
- volume: 5.400/mo (KD 20, +22%/ano) — único nome de framework com volume real no BR
- delimitacao: escopo é ORQUESTRAÇÃO e MEMÓRIA. Observabilidade fica de fora
  (`observabilidade-agentes-ia-langsmith-langfuse-helicone`) e ferramental de contexto
  também (`ferramentas-de-engenharia-de-contexto-em-producao`). Memória: linkar
  `pgvector-postgres-memoria-do-seu-agente` em vez de repetir o argumento do Postgres.

## Por que a IA alucina no seu sistema (e o que grounding resolve de verdade)
- publicar_em: 2026-09-01T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Alucinação não é bug do modelo, é ausência de amarra. As técnicas que prendem a
  resposta no seu dado real e a validação que permite botar o sistema na frente de cliente
  pagante. Módulo 8 do Lab. Sem post equivalente no acervo.
- hook: O modelo não mentiu. Ele completou. A diferença entre as duas coisas é o que
  separa demo de produto.
- bullets:
  - Por que "alucinação" é o nome errado do problema
  - Grounding: prender a resposta no dado que é seu
  - Validação em tempo real vs. rezar no try/catch
  - Citação de fonte: o padrão que corta reclamação de cliente
  - O que ainda vai escapar (e como falhar de forma segura)
- keyword_principal: alucinação de ia
- keywords_secundarias: por que a ia alucina, como evitar alucinação da ia, grounding llm
- tags: ia, llm, rag, guardrails, arquitetura
- dificuldade: easy
- volume: 210/mo (KD 9, +24%/ano)
- delimitacao: não deixar virar post de RAG. RAG entra como UMA das amarras, em uma seção,
  com link para `o-que-e-rag` e `rag-nao-funciona-causas-e-conserto`.

## Quanto custa um agente de IA em produção: a conta real de tokens
- publicar_em: 2026-09-01T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: A planilha que ninguém mostra — quanto custa cada camada (system prompt,
  histórico, tool results, retries) num mês real, e onde some 80% do dinheiro. Fecha com
  compressão de prompt, pruning e seleção de contexto. Módulo 11 do Lab.
- hook: Seu protótipo custou R$ 12 no primeiro dia. Em produção, com 200 usuários, custa
  R$ 4.000/mês — e ninguém no time sabe explicar por quê.
- bullets:
  - Onde o token vai embora: anatomia de uma chamada cara
  - O custo escondido do histórico que ninguém poda
  - Tool results: o maior vilão do contexto
  - Compressão e pruning na prática, com números antes/depois
  - O cálculo de margem: quando o produto não fecha a conta
- keyword_principal: quanto custa um agente de ia
- keywords_secundarias: custo de api de ia, reduzir custo llm, economizar tokens
- tags: ai-agents, custo, llm, arquitetura
- dificuldade: medium
- volume: ~50/mo direto, mas ancora no cluster de custo que já traz 836 cliques/90d ao blog
- delimitacao: é a conta de token de UM agente em produção. Não é preço de mercado
  (`ia-vai-ficar-mais-cara`) nem economia de uso de ferramenta
  (`como-economizar-tokens-claude-code-codex-cursor`) — linkar os dois.

## JSON que não quebra: contratos estáveis na saída do LLM
- publicar_em: 2026-09-02T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Como garantir saída estruturada de verdade — schema, structured outputs,
  validação e retry — para o retorno do modelo entrar nos seus sistemas sem parser
  defensivo. Módulo 5 do Lab.
- hook: Se o seu código tem um `try/catch` em volta de um `json_decode` da resposta do
  modelo, você não tem contrato. Tem esperança.
- bullets:
  - Por que o modelo quebra o JSON (e quando)
  - Structured outputs vs. "responda em JSON, por favor"
  - Desenhando o schema que o modelo consegue cumprir
  - Validação e retry sem loop infinito
  - Versionando o contrato quando o schema muda
- keyword_principal: structured output llm
- keywords_secundarias: json llm, saída estruturada ia, function calling schema
- tags: llm, tool-use, arquitetura, api, ia
- dificuldade: medium
- volume: ~10/mo direto — pauta de conversão; capta long-tail de erro
- delimitacao: é sobre a SAÍDA do modelo. `tool-use-na-pratica-desenhando-ferramentas-llm`
  já cobre schema strict no desenho da tool (entrada) — linkar, não repetir.

## Roteamento de intenção: como o agente decide qual caminho seguir
- publicar_em: 2026-09-02T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: O mecanismo por trás da escolha de rota — classificação de intenção, roteador
  determinístico vs. por LLM, e como deixar a decisão auditável em vez de mágica.
  Módulo 6 do Lab. Sem post equivalente no acervo.
- hook: "Ele decide sozinho qual fluxo usar." Ótimo. Agora me mostra o log de por que ele
  escolheu o fluxo errado ontem às 14h.
- bullets:
  - Roteador determinístico vs. roteador por LLM
  - Classificação de intenção que aguenta ambiguidade
  - O fallback: o que fazer quando nenhuma rota serve
  - Deixando a decisão auditável
  - Medindo acerto de rota sem rotular tudo na mão
- keyword_principal: classificação de intenção llm
- keywords_secundarias: roteamento de agente de ia, router llm, intent classification
- tags: ai-agents, arquitetura, llm, roteamento
- dificuldade: medium
- volume: sem volume mensurável — pauta de conversão
- delimitacao: é escolha de ROTA entre fluxos. `agentic-rag-quando-o-agente-decide-o-que-buscar`
  cobre a decisão de buscar ou não — caso particular, entra como link.

## Seu problema não precisa de um agente: o teste dos 3 minutos
- publicar_em: 2026-09-02T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Framework de decisão pra cortar escopo antes de gastar seis semanas: dado o
  problema, o que ele pede — um `if`, uma query, um prompt, um fluxo determinístico ou um
  agente. Módulo 2 do Lab. **É o post que carrega o pitch cheio do Lab** e fecha a semana
  relinkando os outros 8.
- hook: Metade dos "projetos de IA" que eu revisei em 2026 se resolviam com um `if` e um
  SELECT. A outra metade virou agente porque o time queria dizer que tinha IA.
- bullets:
  - As 4 perguntas do teste dos 3 minutos
  - `if` vs. query vs. prompt vs. fluxo vs. agente
  - 5 casos reais e o veredito de cada um
  - O custo de errar pra cima (e por que ninguém mede)
  - O que fazer quando a pressão vem de cima
- keyword_principal: quando usar agente de ia
- keywords_secundarias: quando não usar ia, automação vs agente de ia, ia é a resposta errada
- tags: ai-agents, arquitetura, produto-ia, ia
- dificuldade: easy
- volume: ~0 — pauta de distribuição (TabNews/LinkedIn) e conversão, não de SEO
- delimitacao: é sobre NÃO construir agente nenhum. `o-que-e-um-agente-de-ia` define o que
  é agente e `agentic-code-vs-vibe-coding-vs-sdd-tabela-decisao` escolhe entre paradigmas
  de código — ambos pressupõem que você vai construir. Linkar os dois.

---

## CTA

Os 8 primeiros levam CTA leve (uma linha + link para a landing do Lab). O post de 02/09
17:00 (teste dos 3 minutos) leva o pitch cheio — usar a skill `montar-cta-pitch`.
