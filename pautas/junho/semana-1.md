# Pauta — Junho, Semana 1 (01–07/06/2026)

> Tema da semana: **arquitetar soluções de software com agents de IA** — do conceito à
> construção (MCP, tool calling, RAG, engenharia de contexto/prompt), com os temas que
> estão em alta no dev. 21 posts, 3/dia. Objetivo: autoridade no pilar.
>
> Sinais: GSC 90d + DataForSEO (Brazil, pt). Vol "~0" = volume desprezível em pt-BR
> (aposta de autoridade, não busca). "quick-win" = blog já rankeia no GSC, só falta post.

<!-- ===================== Segunda 01/06 ===================== -->

## O que é um agente de IA (e o que é só um wrapper de prompt)
- publicar_em: 2026-06-01T09:00:00-03:00
- autor: lucas
- categoria: Notícias
- resumo: Definição honesta de agente de IA contra o hype de LinkedIn: o loop percepção→decisão→ação→observação e os 4 blocos mínimos (modelo, ferramentas, memória, orquestração). Post-pilar que abre a semana e ancora o vocabulário — todos os outros posts linkam de volta pra cá.
- hook: 90% dos "agents" que você vê no LinkedIn são só um if com esteroides. Um agente de verdade tem quatro blocos mínimos — e faltar um deles é o que faz o seu virar burro depois da terceira mensagem.
- bullets:
  - O que separa um agente de um wrapper de prompt (o loop percepção→decisão→ação→observação).
  - Os 4 blocos mínimos: modelo, ferramentas, memória e orquestração.
  - Por que faltar um deles quebra tudo — sintoma por sintoma.
  - Agente × chatbot × automação: onde traçar a linha.
  - Mapa da semana: o que cada bloco vai destrinchar nos próximos posts.
- keyword_principal: o que é um agente de ia
- keywords_secundarias: agentes de ia, o que são agentes de ia, agente de ia vs chatbot
- tags: ia, ai-agents, llm, agentes
- dificuldade: easy
- volume: ~1.000/mo (KD 10, +296%/ano) · head `agentes de ia` 8.100/mo

---

## O que é MCP (Model Context Protocol) e por que virou o padrão de tools
- publicar_em: 2026-06-01T12:00:00-03:00
- autor: lucas
- categoria: Notícias
- resumo: Explicação direta do Model Context Protocol — o "USB-C dos agents": um padrão para conectar modelos a ferramentas e dados sem reescrever integração a cada vez. Por que a indústria adotou em massa e o que isso muda em quem constrói agente. Encaixa no pilar de tools da semana.
- hook: Antes do MCP, cada agente falava com cada ferramenta no seu próprio dialeto. O MCP é o protocolo que parou essa Torre de Babel — e entender ele é pré-requisito pra arquitetar agente em 2026.
- bullets:
  - O que é o MCP, em uma frase sem marketing (o "USB-C" entre modelo e ferramenta).
  - O problema que ele resolve: integração N×M virou N+M.
  - As 3 peças: host, client e server.
  - O que um MCP server expõe (tools, resources, prompts).
  - Quando você precisa de MCP — e quando é overkill.
- keyword_principal: o que é mcp
- keywords_secundarias: model context protocol, mcp ia, mcp server
- tags: ia, ai-agents, mcp, llm, claude
- dificuldade: easy
- volume: ~1.900/mo (KD baixo, +175%/ano) · head `mcp` 18.100/mo

---

## Engenharia de contexto: o que vai no prompt (e o que NÃO vai)
- publicar_em: 2026-06-01T15:00:00-03:00
- autor: lucas
- categoria: Notícias
- resumo: O recurso mais escasso de um agente é a janela de contexto. Este post mostra como decidir o que entra no prompt e o que fica de fora — system prompt, exemplos, histórico, dados recuperados — e por que encher de contexto degrada a resposta. Quick-win: o blog já rankeia para "engenharia de contexto".
- hook: Seu agente não fica burro por falta de contexto. Fica burro por excesso. Engenharia de contexto é decidir o que NÃO entra no prompt.
- bullets:
  - Contexto é orçamento, não armário: cada token tem custo e ruído.
  - O que merece estar no system prompt vs no turno vs recuperado sob demanda.
  - Context rot: por que jogar tudo no prompt piora a resposta.
  - Engenharia de contexto × engenharia de prompt: a diferença.
  - Um checklist do que cortar quando o agente começa a alucinar.
- keyword_principal: engenharia de contexto
- keywords_secundarias: context engineering, janela de contexto, o que é engenharia de contexto
- tags: ia, ai-agents, llm, engenharia-de-contexto, prompt
- dificuldade: medium
- volume: `context engineering` ~590/mo (KD 65, +7.100%/ano) · QUICK-WIN: blog em pos.6 `engenharia de contexto anthropic`, pos.23 `engenharia de contexto`

---

<!-- ===================== Terça 02/06 ===================== -->

## Tool calling na prática: como o agente decide chamar uma ferramenta
- publicar_em: 2026-06-02T09:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: Anatomia do loop ReAct e do tool-calling — quando o agente decide buscar/agir vs. responder direto — com design de tools (contratos, schemas, idempotência) e exemplo prático de tool de busca em banco no Laravel via Claude API. Funde os ângulos de loop e de design de ferramentas num pilar só.
- hook: Entre "pensar" e "agir" existe um loop. Quem entende esse loop para de brigar com o modelo — e para de ver o agente alucinar parâmetros de ferramenta.
- bullets:
  - Anatomia do ReAct / tool-calling: o ciclo de decisão por dentro.
  - Quando o agente decide chamar uma tool vs. responder direto.
  - Design de tools: contratos claros, schemas e idempotência.
  - Erros comuns que fazem o modelo alucinar parâmetros — e a correção.
  - Exemplo prático: tool de busca em banco no Laravel com Claude API (tool use).
- keyword_principal: tool calling
- keywords_secundarias: function calling, tool use claude api, react agente
- tags: ia, ai-agents, llm, claude, laravel, php
- dificuldade: medium
- volume: ~170/mo (KD baixo, +1.340%/ano — maior curva do lote)

---

## MCP na prática: criando seu primeiro MCP server
- publicar_em: 2026-06-02T12:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: Walkthrough de construção de um MCP server do zero — expondo uma tool e um resource — e plugando num cliente (Claude). O recorte "como criar" foge da intenção navegacional do termo cru e entrega o que o dev brasileiro não acha em PT-BR.
- hook: Todo mundo sabe consumir MCP server dos outros. Hoje você vai escrever o seu — e ver seu agente chamar uma ferramenta que você mesmo expôs.
- bullets:
  - O que um MCP server precisa expor (tools, resources, prompts).
  - Estrutura mínima de um server (handshake e capabilities).
  - Expondo sua primeira tool com schema validável.
  - Conectando o server a um cliente e testando o handshake.
  - Erros comuns de quem está começando com MCP.
- keyword_principal: mcp server
- keywords_secundarias: como criar mcp server, model context protocol, mcp tutorial
- tags: ia, ai-agents, mcp, llm, tutorial
- dificuldade: medium
- volume: ~5.400/mo (KD 29, intenção navegacional → recorte "como criar")

---

## Engenharia de prompt: o guia honesto (sem fórmula mágica)
- publicar_em: 2026-06-02T15:00:00-03:00
- autor: lucas
- categoria: Notícias
- resumo: Guia direto de engenharia de prompt aplicada a quem constrói software com IA — estrutura, instruções, exemplos (few-shot), formato de saída — sem as listas de "100 prompts mágicos". Maior volume×viabilidade da semana (KD 2). Conecta com engenharia de contexto e tool calling.
- hook: Engenharia de prompt não é decorar fórmula. É escrever instrução como quem escreve contrato: sem ambiguidade, com exemplo, e testável.
- bullets:
  - Os blocos de um bom prompt: papel, tarefa, restrições, formato.
  - Zero-shot vs few-shot: quando o exemplo paga o custo de tokens.
  - Por que pedir o formato de saída resolve metade dos bugs.
  - Prompt de produto × prompt de chat: o que muda.
  - Erros que fazem o modelo "desobedecer" (e não é culpa do modelo).
- keyword_principal: engenharia de prompt
- keywords_secundarias: prompt engineering, few shot, engenharia de prompt o que é
- tags: ia, llm, prompt, engenharia-de-prompt
- dificuldade: easy
- volume: ~9.900/mo (KD 2 — maior volume×viabilidade da semana; -18%/ano)

---

<!-- ===================== Quarta 03/06 ===================== -->

## Programmatic tool calling: quando o agente escreve código em vez de chamar tool a tool
- publicar_em: 2026-06-03T09:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: Em vez de o modelo chamar 12 tools em sequência (cada uma custando um turno e enchendo o contexto), ele escreve um pequeno programa que orquestra as chamadas e devolve só o resultado. O padrão "code mode" / programmatic tool calling que está mudando como se arquiteta agente. Tema em alta no dev — aposta de autoridade.
- hook: Chamar 12 tools uma a uma é caro, lento e entope o contexto. E se o agente escrevesse o código que chama as 12 de uma vez e te devolvesse só a resposta?
- bullets:
  - O custo escondido do tool calling clássico: turnos, latência e tokens.
  - O que é programmatic tool calling / "code mode".
  - Como o modelo orquestra chamadas via código em sandbox.
  - O que melhora: menos round-trips, contexto mais limpo, composição.
  - Riscos e guardrails: execução de código não é de graça.
- keyword_principal: programmatic tool calling
- keywords_secundarias: code mode, tool calling, mcp code execution
- tags: ia, ai-agents, tool-calling, mcp, llm
- dificuldade: hard
- volume: ~0/mo em pt-BR (tema em alta no dev internacional — aposta de autoridade)

---

## Progressive disclosure: como não afogar seu agente em 50 ferramentas
- publicar_em: 2026-06-03T12:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: Colocar 50 tools no contexto do agente degrada a escolha e estoura tokens. Progressive disclosure carrega ferramentas sob demanda — o agente descobre o que precisa quando precisa. Padrão central de arquitetura de agentes que escalam. Tema em alta — aposta de autoridade.
- hook: Você deu 50 ferramentas pro seu agente e ele ficou pior. Claro: ninguém escolhe bem entre 50 opções — nem você, nem o modelo.
- bullets:
  - Por que mais tools no contexto = pior decisão e mais tokens.
  - O que é progressive disclosure de ferramentas.
  - Carregar tools sob demanda: busca, namespaces, hierarquia.
  - Como o agente "descobre" a ferramenta certa na hora certa.
  - Aplicando o padrão num agente com muitas integrações.
- keyword_principal: progressive disclosure
- keywords_secundarias: progressive disclosure agentes, tool calling, arquitetura de agentes
- tags: ia, ai-agents, tool-calling, arquitetura, llm
- dificuldade: hard
- volume: ~0/mo em pt-BR (termo de design de agentes em alta — aposta de autoridade)

---

## System prompt: a espinha dorsal do comportamento do agente
- publicar_em: 2026-06-03T15:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: O system prompt define quem o agente é, o que pode e o que nunca deve fazer. Este post mostra como estruturar um system prompt de produção — papel, políticas, formato, ferramentas — e por que ele é diferente de um prompt de chat qualquer. Crescendo +333%/ano.
- hook: O system prompt não é "onde você manda o modelo ser legal". É a constituição do agente — e a maioria está mal escrita.
- bullets:
  - O que vive no system prompt vs no turno do usuário.
  - Estrutura de um system prompt de produção (papel, políticas, formato).
  - Como declarar limites e o que o agente NÃO pode fazer.
  - System prompt e tools: dando contexto sem inflar.
  - Versionar e testar system prompt como código.
- keyword_principal: system prompt
- keywords_secundarias: prompt de sistema, system prompt llm, engenharia de prompt
- tags: ia, ai-agents, llm, prompt, system-prompt
- dificuldade: medium
- volume: ~210/mo (KD 19, +333%/ano)

---

<!-- ===================== Quinta 04/06 ===================== -->

## Quando usar RAG (e quando fine-tuning ou contexto resolvem melhor)
- publicar_em: 2026-06-04T09:00:00-03:00
- autor: lucas
- categoria: Notícias
- resumo: RAG virou resposta automática pra tudo — e quase sempre é a escolha errada. Este post dá o mapa de decisão entre RAG, fine-tuning e simplesmente colocar no contexto, com os critérios que importam: volatilidade do dado, custo, rastreabilidade e tamanho.
- hook: "Joga um RAG nisso" é a resposta preguiçosa de 2026. Metade das vezes, um bom contexto ou um fine-tuning resolvia melhor e mais barato.
- bullets:
  - O que RAG resolve de verdade (e o que não resolve).
  - RAG × fine-tuning × contexto longo: o mapa de decisão.
  - Critérios: o dado muda? precisa de fonte? cabe no contexto?
  - Sinais de que você NÃO precisa de RAG.
  - Custo real de manter um pipeline de RAG em produção.
- keyword_principal: quando usar rag
- keywords_secundarias: rag vs fine tuning, fine tuning, rag ou fine tuning
- tags: ia, rag, fine-tuning, llm, agentes
- dificuldade: medium
- volume: `fine tuning` ~2.900/mo (intenção info) · `quando usar rag` ~0 (long-tail do pilar RAG)

---

## Como implementar RAG do zero: chunking, embeddings e busca
- publicar_em: 2026-06-04T12:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: O passo a passo de um RAG que funciona — como quebrar documentos (chunking), gerar embeddings, indexar e buscar — com as decisões que definem qualidade (tamanho do chunk, overlap, modelo de embedding). Mão na massa, ligado ao post de pgvector.
- hook: RAG não é mágica: é quebrar texto direito, virar vetor e buscar bem. Errar o chunking é onde 80% dos RAGs nascem ruins.
- bullets:
  - O pipeline de RAG em 4 etapas: ingest → chunk → embed → retrieve.
  - Chunking: tamanho, overlap e por que isso decide a qualidade.
  - Escolhendo um modelo de embedding (e quando trocar).
  - Indexando e buscando por similaridade.
  - Medindo se a recuperação está boa antes de culpar o modelo.
- keyword_principal: chunking
- keywords_secundarias: rag llm, como implementar rag, embeddings
- tags: ia, rag, embeddings, chunking, llm
- dificuldade: medium
- volume: `chunking` ~590/mo + `rag llm` ~590/mo (KD 21) · long-tail `como implementar rag` ~0

---

## Reranking: o passo que faz seu RAG parar de devolver lixo
- publicar_em: 2026-06-04T15:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: A busca vetorial traz 20 candidatos "parecidos" — mas parecido não é relevante. O reranker reordena por relevância real antes de mandar pro modelo. Este post mostra cross-encoder vs busca híbrida e quando cada um vale. Quick-win: o blog já rankeia para reranker.
- hook: Seu RAG traz 20 trechos "parecidos" e o modelo responde com o errado. O problema não é a busca — é a falta de um reranker.
- bullets:
  - Por que similaridade vetorial ≠ relevância.
  - O que um reranker faz: reordenar antes de gerar.
  - Cross-encoder vs bi-encoder: o trade-off precisão × custo.
  - Busca híbrida (BM25 + vetorial) e quando ela basta.
  - Onde encaixar o reranker no pipeline de RAG.
- keyword_principal: reranker
- keywords_secundarias: cross encoder reranker, busca híbrida, reranking rag
- tags: ia, rag, reranking, embeddings, llm
- dificuldade: medium
- volume: ~0/mo no DFS, mas QUICK-WIN — blog em pos.3 `cross encoder reranker`, pos.10 `bm25 reranker` (GSC)

---

<!-- ===================== Sexta 05/06 ===================== -->

## Montando um agente mínimo viável com Claude API + Laravel
- publicar_em: 2026-06-05T09:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: Walkthrough de um agente funcional em PHP puro com Laravel, sem framework de agente nenhum — o loop básico prompt→tool use→resposta direto na Claude API. Recorte Laravel que ninguém cobre em PT-BR; continuação natural do longform "ChatGPT vs API".
- hook: Vou montar um agente funcional em PHP sem framework de agent nenhum. Só pra provar que dá — e que você não precisa de LangChain pra ter um loop que funciona.
- bullets:
  - O loop básico de um agente: prompt → tool use → resposta.
  - Chamando a Claude API direto do Laravel (sem SDK de agente).
  - Registrando e executando uma tool no Laravel.
  - Tratando a resposta e fechando o ciclo de tool use.
  - Quando vale (e quando não vale) trazer um framework de agente.
- keyword_principal: claude api laravel
- keywords_secundarias: claude api, claude api php, agente de ia em php
- tags: ia, ai-agents, claude, laravel, php, tutorial
- dificuldade: medium
- volume: head `claude api` 4.400/mo (KD 42, +404%/ano); recorte laravel livre

---

## pgvector no Postgres: onde guardar a memória do seu agente
- publicar_em: 2026-06-05T11:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: Antes de assinar um serviço gerenciado de memória, o post mostra que o Postgres que o dev Laravel já tem resolve 80% do problema com pgvector. Instalação, uso e critérios de decisão (volume, compliance, time) — pgvector vs. serviço gerenciado. Melhor post "rankeável" da semana.
- hook: Antes de assinar o Mem0, pergunte: seu Postgres já não resolve 80% disso? Spoiler — com pgvector, quase sempre resolve.
- bullets:
  - O que é pgvector e por que ele basta pra maioria dos agentes.
  - Instalando pgvector no Postgres de uma app Laravel.
  - Guardando e buscando embeddings por similaridade na prática.
  - pgvector × serviço gerenciado: critérios de decisão (volume, compliance, time).
  - Quando NÃO usar pgvector — os limites honestos.
- keyword_principal: pgvector
- keywords_secundarias: pgvector laravel, pgvector postgres, busca por similaridade
- tags: ia, rag, embeddings, laravel, php, postgres
- dificuldade: medium
- volume: ~1.300/mo (KD 23, +60%/ano) · CPC R$7,55

---

## Agentic RAG: quando o próprio agente decide o que buscar
- publicar_em: 2026-06-05T15:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: No RAG clássico você busca antes de perguntar. No agentic RAG o agente decide se busca, o que busca e quantas vezes — usando a recuperação como uma tool. Evolução natural de quem já entende tool calling e RAG; junta os dois pilares da semana.
- hook: RAG clássico busca sempre, mesmo quando não precisa. Agentic RAG dá ao agente o direito de decidir — e de buscar de novo quando a primeira resposta não bastou.
- bullets:
  - RAG clássico (retrieve-then-read) × agentic RAG (retrieve-as-tool).
  - A recuperação como uma ferramenta que o agente chama.
  - Multi-hop: buscar, ler, refinar a query e buscar de novo.
  - Quando agentic RAG paga o custo de latência extra.
  - Juntando tool calling + RAG num agente só.
- keyword_principal: agentic rag
- keywords_secundarias: rag agentico, agentic rag o que é, rag com agentes
- tags: ia, ai-agents, rag, llm, agentes
- dificuldade: hard
- volume: ~1.000/mo (KD 19, intenção info)

---

<!-- ===================== Sábado 06/06 ===================== -->

## 5 anti-patterns que quebram seu agente em produção
- publicar_em: 2026-06-06T09:00:00-03:00
- autor: lucas
- categoria: Notícias
- resumo: Funcionava na demo, virou pesadelo em produção. Os 5 erros mais caros de arquitetura de agente — context stuffing, tools sem timeout, retry burro, zero observabilidade, ausência de guardrails — cada um com o sintoma e a correção. Liga no foothold de observabilidade do blog.
- hook: Funcionava lindo na demo. Em produção, virou uma conta de US$ 3 mil e um loop infinito. Os 5 anti-patterns que levam todo agente pra esse buraco.
- bullets:
  - Context stuffing: entupir o prompt e culpar o modelo.
  - Tools sem timeout nem idempotência.
  - Retry burro: repetir a mesma chamada que já falhou.
  - Zero observabilidade: você não sabe por que ele errou.
  - Sem guardrails: o agente faz o que não devia.
- keyword_principal: agentes de ia em produção
- keywords_secundarias: anti patterns agentes, agentes em produção, observabilidade ia
- tags: ia, ai-agents, producao, observabilidade, llm
- dificuldade: medium
- volume: ~0/mo direto (autoridade) · liga em `ferramentas de observabilidade` pos.79 (GSC, 39 impr)

---

## Guardrails para agentes de IA: validando o que entra e o que sai
- publicar_em: 2026-06-06T12:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: Um agente em produção precisa de cercas: validar a entrada, restringir o que as tools podem fazer e checar a saída antes de devolver ao usuário. Este post mostra os tipos de guardrail e onde encaixá-los. Recorte qualificado — o termo cru é dominado por barreira de estrada.
- hook: Um agente sem guardrails é um estagiário com acesso de admin e nenhuma supervisão. Funciona até o dia em que não funciona.
- bullets:
  - Os 3 pontos de guardrail: entrada, ação (tools) e saída.
  - Validação de input: prompt injection e dados fora do escopo.
  - Limitando o que cada tool pode executar.
  - Checando a saída antes de entregar (formato, política, alucinação).
  - Guardrail como código testável, não como "boa intenção".
- keyword_principal: guardrails para agentes
- keywords_secundarias: guardrails llm, guardrails ia, validação de agentes
- tags: ia, ai-agents, guardrails, seguranca, llm
- dificuldade: medium
- volume: recorte qualificado, vol baixo (head `guardrails` 22.200/mo é barreira de estrada + transactional — não mirar)

---

## Como avaliar seu agente: evals sem mentir pra si mesmo
- publicar_em: 2026-06-06T15:00:00-03:00
- autor: lucas
- categoria: Tutoriais
- resumo: "Funciona nos meus testes" não é avaliação. Este post mostra como montar evals honestos para um agente — golden set, métricas por etapa (recuperação, decisão de tool, resposta) e LLM-as-judge com cautela. Checklist replicável, asset salvável.
- hook: Todo mundo diz que o agente "tá bom". Medido como? Eval de agente que é só olhar 3 exemplos é torcida, não avaliação.
- bullets:
  - Por que "testei e funcionou" não é eval.
  - Montando um golden set com os seus casos reais.
  - Avaliando por etapa: recuperou certo? escolheu a tool certa? respondeu certo?
  - LLM-as-judge: quando ajuda e quando engana.
  - Custo, latência e acerto: as 3 métricas que importam.
- keyword_principal: avaliação de agentes de ia
- keywords_secundarias: llm evals, avaliar agente de ia, llm como juiz
- tags: ia, ai-agents, evals, avaliacao, llm
- dificuldade: hard
- volume: ~0/mo direto (autoridade — checklist salvável/compartilhável)

---

<!-- ===================== Domingo 07/06 ===================== -->

## O que é RAG (e onde ele termina e a memória começa)
- publicar_em: 2026-06-07T09:00:00-03:00
- autor: lucas
- categoria: Notícias
- resumo: Post-pilar sobre RAG — o que é, como funciona e por que RAG não é memória (e vice-versa). Delimita os dois conceitos e mostra como se complementam, abrindo a sequência de RAG prometida no canal. Não tratar como teaser: é a segunda maior keyword com intenção limpa da semana.
- hook: RAG não é memória. Memória não é RAG. E confundir os dois quebra o seu agente — começando pela conta no fim do mês.
- bullets:
  - O que é RAG, em uma frase que não é marketing.
  - Como funciona o ciclo recuperar → aumentar → gerar.
  - RAG × memória: onde um termina e o outro começa.
  - RAG × fine-tuning: quando cada um faz sentido.
  - O fio que amarra a semana: agente + tools + contexto + RAG.
- keyword_principal: o que é rag
- keywords_secundarias: rag vs memória, rag vs fine tuning, rag na prática
- tags: ia, rag, llm, embeddings, agentes
- dificuldade: easy
- volume: ~2.900/mo (KD 26, +89%/ano — 2º maior volume com intenção limpa)

---

## O blueprint completo: arquitetando uma solução de IA de ponta a ponta
- publicar_em: 2026-06-07T12:00:00-03:00
- autor: lucas
- categoria: Notícias
- resumo: Post de síntese que junta a semana num diagrama só — modelo, tools (MCP), contexto/prompt, RAG, guardrails e observabilidade — no agente que você consegue defender numa code review. Diagrama de referência + checklist de produção. Linka todos os posts da semana.
- hook: A semana inteira em um diagrama só: o agente que você consegue defender numa code review — e botar em produção sem rezar.
- bullets:
  - O blueprint: modelo + tools + contexto + memória/RAG + orquestração.
  - Onde MCP, tool calling e RAG se encaixam no fluxo.
  - O que vai no prompt vs o que é recuperado vs o que é tool.
  - Guardrails e observabilidade como camadas, não enfeite.
  - Checklist de produção: o que revisar antes de subir.
- keyword_principal: arquitetura de agentes de ia
- keywords_secundarias: como arquitetar agente de ia, blueprint de agente, solução de ia
- tags: ia, ai-agents, arquitetura, llm, agentes
- dificuldade: medium
- volume: `arquitetura de agentes de ia` ~40/mo (intenção comercial) → mirar síntese/autoridade, não a keyword crua

---

## Vibe coding: o que é, por que todo dev fala disso e onde ele quebra
- publicar_em: 2026-06-07T15:00:00-03:00
- autor: lucas
- categoria: Notícias
- resumo: Vibe coding — construir software conversando com a IA em vez de digitar cada linha — é o termo do momento. Este post explica o que é de verdade, onde acelera, e onde vira dívida técnica silenciosa. Maior volume da semana e asset compartilhável pra fechar o ciclo.
- hook: Vibe coding parece mágica até o dia em que você precisa debugar 4 mil linhas que ninguém entende — nem a IA que escreveu.
- bullets:
  - O que é vibe coding (e o que não é).
  - Por que explodiu: a barreira de entrada despencou.
  - Onde acelera de verdade: protótipo, glue code, exploração.
  - Onde vira armadilha: dívida técnica que ninguém revisou.
  - Vibe coding com responsabilidade: o que ainda exige engenheiro.
- keyword_principal: vibe coding
- keywords_secundarias: o que é vibe coding, vibe coding o que é, programar com ia
- tags: ia, vibe-coding, llm, desenvolvimento, agentes
- dificuldade: easy
- volume: ~27.100/mo (KD 59, +82%/ano — maior volume da semana; asset compartilhável)

---

### Quick-wins de internal-linking (de graça)

- **Engenharia de contexto** (Seg 15h) e **Reranking** (Qui 15h) são os 2 quick-wins: o blog
  já rankeia `engenharia de contexto anthropic` (pos.6), `cross encoder reranker` (pos.3) e
  `bm25 reranker` (pos.10). Linkar os posts novos ↔ os posts existentes desses temas reforça
  footholds que já estão na pág.1.
- O pilar **`o que é um agente de ia`** (Seg 09h) deve receber link de TODOS os 20 posts.
- **`o que é mcp`** (Seg 12h) e **`o que é rag`** (Dom 09h) são sub-pilares — concentram os
  links dos posts de tools e de RAG respectivamente.

### Ordem de produção (por impacto de SEO)

1. `o que é mcp` (Seg 12h) — maior tema em alta com intenção limpa.
2. `engenharia de prompt` (Ter 15h) — 9.900/mo, KD 2.
3. Reranking (Qui 15h) — quick-win, blog já em pos.3.
4. Engenharia de contexto (Seg 15h) — quick-win + explodindo.
5. `vibe coding` (Dom 15h) — maior volume e asset viral.
6. `o que é um agente de ia` (Seg 09h) — pilar que ancora tudo.
7. `agentic rag` (Sex 15h) · `o que é rag` (Dom 09h) · `pgvector` (Sex 11h) — núcleo RAG.
8. Demais (tool calling, mcp server, system prompt, RAG how-to, build Laravel).
9. Apostas de autoridade sem volume (programmatic tool calling, progressive disclosure, anti-patterns, evals, guardrails, blueprint) — escrever pelo posicionamento, promover por canal.
