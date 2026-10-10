# Batch setembro semana-1 (31/08 → 02/09) — entrada para criar-posts-batch.py
# Fonte: pautas/setembro/semana-1.md (9 posts novos; os 12 refreshes ficam fora, ver refresh-setembro-semana-1.md)
# CTA fixo de todos os posts → https://beerandcode.com.br/landing-pages/ai-engineering-lab
#   Passado via --cta-url/--cta-label/--cta-pitch. Inline no primeiro terço, sem heading próprio.
#
# ATENÇÃO — formato: o parser do script só lê valores de UMA linha e ignora `bullets`/`delimitacao`.
# Por isso a estrutura de H2 e a delimitação anti-canibalização estão embutidas dentro do `resumo`.
# Os 9 temas passaram por dedup contra o acervo em 31/08; a parte "NÃO CANIBALIZAR" não é decorativa.

## Engenharia de prompt acabou. O que veio depois se chama engenharia de contexto
- publicar_em: 2026-08-31T14:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Hub da head keyword do cluster (9.900 buscas/mês, KD 5). Entrega o que a busca pede — as técnicas de prompt que sobreviveram — e reposiciona: em sistema real o problema não é a frase, é o que entra na janela de contexto. Estrutura (H2): As técnicas que sobreviveram (e as que viraram folclore) | Por que prompt bom não salva contexto ruim | O que realmente entra na janela: ordem, corte, recência | Prompt de sistema vs. instrução de turno | Do prompt à arquitetura: o que muda quando vira produto. NÃO CANIBALIZAR: este post é o HUB da head "engenharia de prompt", não um post sobre contexto. É PROIBIDO reescrever o conteúdo de `engenharia-de-contexto-o-que-vai-no-prompt` (o que entra e sai da janela), `ferramentas-de-engenharia-de-contexto-em-producao` (ferramental) e `limite-de-tokens-chatgpt-ia-esquece` (estouro de janela) — cite e linke os três, cada um como aprofundamento de uma seção diferente.
- hook: Ninguém mais ganha dinheiro escrevendo prompt bonito. Ganha quem decide o que entra na janela de contexto — e o que fica de fora.
- keyword_principal: engenharia de prompt
- keywords_secundarias: técnicas de prompt, prompt de sistema, prompt engineering português
- tags: ia, llm, prompt, contexto, arquitetura

## O que é um LLM: a explicação para quem vai construir, não para quem vai postar
- publicar_em: 2026-08-31T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Fundamento sem analogia de papagaio, para 9.900 buscas/mês (KD 25). Tokens, probabilidade, janela, temperatura e por que o modelo é stateless — cada conceito fechando com a consequência prática de arquitetura que ele impõe. É o post de entrada do cluster e a base que faz os outros posts do blog fazerem sentido. Estrutura (H2): O que o modelo realmente faz a cada token | Por que ele é stateless (e o que isso te obriga a construir) | Janela de contexto: o recurso que você administra | Temperatura, top-p e a ilusão de controle | O que isso significa na hora de arquitetar. NÃO CANIBALIZAR: não virar dicionário — `glossario-ai-engineer-2026-30-termos` e `glossario-ai-engineer-vol-2-2026` já ocupam o formato de lista de termos. Aqui é fundamento operacional de UM conceito, com profundidade, não 30 verbetes.
- hook: Você não precisa entender transformer pra usar um LLM. Precisa entender três coisas — e nenhuma delas é transformer.
- keyword_principal: o que é llm
- keywords_secundarias: llm o que é, large language model, como funciona um llm
- tags: ia, llm, fundamentos, arquitetura

## Fine-tuning, RAG ou prompt: qual dos três o seu problema pede
- publicar_em: 2026-08-31T20:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A decisão que mais gente erra pra cima, numa keyword de 2.900 buscas/mês com KD 4. Critério objetivo pra escolher entre os três caminhos, quanto custa cada um com números, e por que fine-tuning quase nunca é a resposta em 2026. É o framework de decisão do módulo 1 do AI Engineering Lab. Estrutura (H2): O que cada um realmente muda no comportamento | A árvore de decisão em 4 perguntas | Quanto custa cada caminho, com números | Os 3 casos raros em que fine-tuning ganha | O erro clássico: treinar pra resolver problema de recuperação. NÃO CANIBALIZAR: é post de DECISÃO com custo, não explicação de RAG. `o-que-e-rag` já cobre o que é RAG e onde ele termina — linkar, não reexplicar. Idem `rag-do-zero-chunking-embeddings-busca` para o pipeline.
- hook: "Vamos treinar um modelo nosso." Ok — me diz o que você tenta ensinar que um bom contexto não resolveria por 3% do preço.
- keyword_principal: fine tuning
- keywords_secundarias: rag vs fine tuning, fine tuning llm, quando usar fine tuning
- tags: ia, llm, rag, fine-tuning, arquitetura

## LangGraph, Mem0, LangChain, MCP: do que você realmente precisa
- publicar_em: 2026-09-01T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Mapa honesto do ecossistema de orquestração e memória (langgraph tem 5.400 buscas/mês, KD 20 — o único nome de framework com volume real no Brasil). O que cada ferramenta resolve, o que cobra em complexidade, o ponto em que deixa de ser overhead, e o caso em que a resposta é "nenhuma delas". Estrutura (H2): O que cada uma faz, em uma frase, sem marketing | Orquestração: quando LangGraph paga o próprio peso | Memória: Mem0 vs. uma tabela no Postgres | MCP: o que mudou e o que ainda é hype | A árvore de decisão: 5 perguntas antes de instalar qualquer coisa. NÃO CANIBALIZAR: o escopo é ORQUESTRAÇÃO e MEMÓRIA. Observabilidade fica de fora — `observabilidade-agentes-ia-langsmith-langfuse-helicone` já cobre. Ferramental de contexto fica de fora — `ferramentas-de-engenharia-de-contexto-em-producao` já cobre. No trecho de memória, linkar `pgvector-postgres-memoria-do-seu-agente` em vez de repetir o argumento do Postgres.
- hook: Você abriu 6 abas de documentação e ainda não escreveu uma linha. O problema não é escolher a ferramenta errada — é achar que precisa de uma.
- keyword_principal: langgraph
- keywords_secundarias: langgraph vale a pena, mem0, langchain alternativa, ferramentas para agentes de ia
- tags: ai-agents, llm, arquitetura, ferramentas, mcp

## Por que a IA alucina no seu sistema (e o que grounding resolve de verdade)
- publicar_em: 2026-09-01T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Alucinação não é bug do modelo, é ausência de amarra. As técnicas que prendem a resposta no dado real e a validação em tempo real que permite botar o sistema na frente de cliente pagante. Keyword de 210 buscas/mês com KD 9 — a menor dificuldade da semana, ranqueia rápido. Módulo 8 do AI Engineering Lab, sem post equivalente no acervo. Estrutura (H2): Por que "alucinação" é o nome errado do problema | Grounding: prender a resposta no dado que é seu | Validação em tempo real vs. rezar no try/catch | Citação de fonte: o padrão que corta reclamação de cliente | O que ainda vai escapar (e como falhar de forma segura). NÃO CANIBALIZAR: não deixar virar post de RAG. RAG entra como UMA das amarras, em uma seção só, com link para `o-que-e-rag` e `rag-nao-funciona-causas-e-conserto`.
- hook: O modelo não mentiu. Ele completou. A diferença entre as duas coisas é o que separa demo de produto.
- keyword_principal: alucinação de ia
- keywords_secundarias: por que a ia alucina, como evitar alucinação da ia, grounding llm
- tags: ia, llm, rag, guardrails, arquitetura

## Quanto custa um agente de IA em produção: a conta real de tokens
- publicar_em: 2026-09-01T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: A planilha que ninguém mostra — quanto custa cada camada do agente (system prompt, histórico, tool results, retries) num mês real de uso, e onde some 80% do dinheiro. Fecha com compressão de prompt, pruning de histórico e seleção de contexto, com números antes e depois. Módulo 11 do AI Engineering Lab. Ancora no cluster de custo, que já traz 836 cliques/90d ao blog. Estrutura (H2): Onde o token vai embora: anatomia de uma chamada cara | O custo escondido do histórico que ninguém poda | Tool results: o maior vilão do contexto | Compressão e pruning na prática, com números antes/depois | O cálculo de margem: quando o produto não fecha a conta. NÃO CANIBALIZAR: é a conta de token de UM agente em produção. Não é preço de mercado — `ia-vai-ficar-mais-cara` cobre isso. Não é economia de uso de ferramenta — `como-economizar-tokens-claude-code-codex-cursor` cobre isso. Linkar os dois.
- hook: Seu protótipo custou R$ 12 no primeiro dia. Em produção, com 200 usuários, ele custa R$ 4.000 por mês — e ninguém no time sabe explicar por quê.
- keyword_principal: quanto custa um agente de ia
- keywords_secundarias: custo de api de ia, reduzir custo llm, economizar tokens
- tags: ai-agents, custo, llm, arquitetura

## JSON que não quebra: contratos estáveis na saída do LLM
- publicar_em: 2026-09-02T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Como garantir saída estruturada de verdade — schema, structured outputs, validação e retry — para o retorno do modelo entrar nos sistemas internos sem parser defensivo e sem try/catch rezando. Módulo 5 do AI Engineering Lab. Volume direto baixo; o post captura long-tail de erro e serve conversão. Estrutura (H2): Por que o modelo quebra o JSON (e quando) | Structured outputs vs. "responda em JSON, por favor" | Desenhando o schema que o modelo consegue cumprir | Validação e retry sem loop infinito | Versionando o contrato quando o schema muda. NÃO CANIBALIZAR: este post é sobre a SAÍDA do modelo. `tool-use-na-pratica-desenhando-ferramentas-llm` já cobre schema strict no desenho da tool, que é a ENTRADA — linkar e deixar a divisão explícita no texto.
- hook: Se o seu código tem um try/catch em volta de um json_decode da resposta do modelo, você não tem contrato. Tem esperança.
- keyword_principal: structured output llm
- keywords_secundarias: json llm, saída estruturada ia, function calling schema
- tags: llm, tool-use, arquitetura, api, ia

## Roteamento de intenção: como o agente decide qual caminho seguir
- publicar_em: 2026-09-02T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: O mecanismo por trás da escolha de rota — classificação de intenção, roteador determinístico vs. roteador por LLM, e como deixar a decisão auditável em vez de mágica. Módulo 6 do AI Engineering Lab, sem post equivalente no acervo. Volume direto não mensurável; é pauta de conversão e autoridade. Estrutura (H2): Roteador determinístico vs. roteador por LLM | Classificação de intenção que aguenta ambiguidade | O fallback: o que fazer quando nenhuma rota serve | Deixando a decisão auditável | Medindo acerto de rota sem rotular tudo na mão. NÃO CANIBALIZAR: é sobre escolha de ROTA entre fluxos. `agentic-rag-quando-o-agente-decide-o-que-buscar` cobre a decisão de buscar ou não, que é um caso particular de roteamento — entra como link e exemplo, não como seção inteira.
- hook: "Ele decide sozinho qual fluxo usar." Ótimo. Agora me mostra o log de por que ele escolheu o fluxo errado ontem às 14h.
- keyword_principal: classificação de intenção llm
- keywords_secundarias: roteamento de agente de ia, router llm, intent classification
- tags: ai-agents, arquitetura, llm, roteamento

## Seu problema não precisa de um agente: o teste dos 3 minutos
- publicar_em: 2026-09-02T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Framework de decisão pra cortar escopo antes de gastar seis semanas: dado o problema na sua frente, o que ele realmente pede — um if, uma query, um prompt, um fluxo determinístico ou um agente. Cinco casos reais com o veredito de cada um. Módulo 2 do AI Engineering Lab. Fecha a semana e é o post que carrega o CTA mais forte, relinkando os outros 8. Estrutura (H2): As 4 perguntas do teste dos 3 minutos | if vs. query vs. prompt vs. fluxo vs. agente | 5 casos reais e o veredito de cada um | O custo de errar pra cima (e por que ninguém mede) | O que fazer quando a pressão vem de cima. NÃO CANIBALIZAR: é sobre NÃO construir agente nenhum. `o-que-e-um-agente-de-ia` define o que é agente e `agentic-code-vs-vibe-coding-vs-sdd-tabela-decisao` escolhe entre paradigmas de código — os dois já pressupõem que você vai construir. Linkar ambos como o passo seguinte de quem passou no teste.
- hook: Metade dos "projetos de IA" que eu revisei em 2026 se resolviam com um if e um SELECT. A outra metade virou agente porque o time queria dizer que tinha IA.
- keyword_principal: quando usar agente de ia
- keywords_secundarias: quando não usar ia, automação vs agente de ia, ia é a resposta errada
- tags: ai-agents, arquitetura, produto-ia, ia
