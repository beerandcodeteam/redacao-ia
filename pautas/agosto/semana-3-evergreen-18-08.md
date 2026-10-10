# Pauta evergreen — semana de 18/08/2026

Origem: `minerar-evergreen` (16/08/2026). Seeds aprovados pelo Lucas.

**Sinal ausente na mineração:** MCP `dataforseo` estava pendente de aprovação — não há
volume BR, KD nem gate de durabilidade (Google Trends). Qualificação feita com GSC
(tração real), dedup no MCP do blog e recon de SERP. Rodar o gate antes de escrever, se
o DataForSEO subir.

---

## O que é o Laravel AI SDK: guia prático do SDK de IA nativo do Laravel
- publicar_em: 2026-08-18T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Hub do cluster Laravel + IA. Explica o que é o AI SDK first-party do Laravel
  (texto, embeddings, completions sobre OpenAI, Gemini e Anthropic), com código rodando
  do zero ao primeiro agente. Durável porque é feature de framework, não release de
  modelo. SERP em português vazia — todo o conteúdo existente está em inglês.
- hook: O Laravel virou o framework onde o SDK de IA vem na caixa. Só que tudo que existe
  sobre isso está em inglês — e a maioria mistura o SDK oficial com o Prism sem explicar
  onde um acaba e o outro começa.
- bullets:
  - O que é o Laravel AI SDK e o que ele resolve (e o que NÃO resolve)
  - Instalação e primeira chamada: texto, embeddings e structured output
  - Trocando de provider (OpenAI, Gemini, Anthropic) sem tocar no código de domínio
  - Onde o SDK oficial trava: tool calling multi-provider, loop agêntico, streaming
  - Integrando com o que você já tem: Laravel Boost, fila, cache e observabilidade
- keyword_principal: laravel ai sdk
- keywords_secundarias: sdk de ia laravel, laravel inteligencia artificial, como usar ia no laravel, laravel ai
- tags: laravel, php, ia, llm, produto-ia
- dificuldade: medium
- volume: nao medido (DataForSEO indisponivel). Sinal indireto: autoridade Laravel ativa
  no GSC (laravel excel 161 impr/pos 5,7; eager loading 132 impr/pos 8,7) e SERP pt-BR vazia.
- interlinks: o-que-e-laravel, laravel-boost-mcp-oficial-laravel, rag-hibrido-na-pratica-bm25-embeddings-reranker

## Laravel AI SDK ou Prism PHP: qual usar em cada caso
- publicar_em: 2026-08-20T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Primeiro spoke do cluster. Decisao perene que todo dev Laravel vai enfrentar: o
  SDK oficial cobre prompt-to-text; o Prism entra quando precisa de tool calling
  multi-provider, controle de loop agentico com step limit, RAG com pgvector e SSE.
  Formato "X vs Y" e o mais duravel do evergreen.
- hook: Os dois fazem IA no Laravel e a internet trata como concorrentes. Nao sao — sao
  camadas. O erro caro e escolher o de baixo e descobrir o teto tres sprints depois.
- bullets:
  - A diferenca real: baseline first-party vs camada agentica
  - Tabela de decisao por requisito (tool calling, streaming, RAG, multi-provider)
  - Codigo lado a lado: mesma tarefa nos dois
  - O teto do SDK oficial: onde exatamente voce bate a cabeca
  - Da pra usar os dois no mesmo app? (sim, e como isolar)
- keyword_principal: laravel ai sdk vs prism
- keywords_secundarias: prism php laravel, prism ou laravel ai, melhor pacote de ia para laravel, prism php o que e
- tags: laravel, php, ia, llm, ai-agents, prism
- dificuldade: medium
- volume: nao medido. SERP pt-BR inexistente; discussao toda em ingles (prismphp.com,
  Laravel News, dev.to).
- interlinks: post-hub (laravel ai sdk), ferramentas-de-ia-backend-top-12-testadas-2026 (ja
  cita Prism — linkar, nao repetir o review)

## O que e o OpenRouter: um endpoint para 500 modelos (e quando isso vale a pena)
- publicar_em: 2026-08-25T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Primeiro dos tres de infraestrutura, e o de SERP mais fraca em pt-BR. Explica o
  gateway unificado, as DUAS camadas de roteamento (modelo e provider), failover
  automatico e o padrao de fallback que segura producao. Duravel: OpenRouter e camada de
  infra, nao modelo — nao tem curva de pico-e-morte.
- hook: Voce ja usou OpenRouter sem saber: e o lugar onde modelo fantasma roda disfarcado
  antes de ter nome. Mas a pergunta que importa nao e "o que e" — e se colocar um
  intermediario entre seu app e o modelo vale a latencia extra.
- bullets:
  - O que e o OpenRouter e o problema real que ele resolve (uma chave, 500 modelos)
  - As duas camadas de roteamento: qual modelo responde vs qual provider serve
  - Failover e rate limit: o padrao que evita o app cair quando um provider some
  - A conta honesta: markup, latencia adicional e quando ir direto na API
  - Migrando de provider unico pra gateway sem reescrever o codigo de dominio
- keyword_principal: openrouter o que e
- keywords_secundarias: como usar openrouter, openrouter tutorial, openrouter vale a pena, roteamento de llm
- tags: ia, llm, openrouter, produto-ia, arquitetura-de-software
- dificuldade: easy
- volume: nao medido. SERP pt-BR rasa (searchops.io, ferramentasai.com.br, 1 video) — sem
  doc oficial gigante dominando. Melhor janela dos tres de infra.
- interlinks: longcat-2-0-owl-alpha-openrouter, fable-5-bloqueado-openrouter-fusion,
  laguna-s-2-1-poolside-benchmarks (tag openrouter ja existe no blog)

## AWS Bedrock na pratica: rodar Claude em producao com governanca (e a conta em real)
- publicar_em: 2026-08-27T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Segundo de infraestrutura. A SERP pt-BR e ocupada pela propria AWS e pelos docs
  da Anthropic — ambos vendedor ou referencia, nenhum tomando decisao. O angulo defensavel
  e o brasileiro: disponibilidade de modelo por regiao, sa-east-1, latencia real, custo em
  BRL com cambio e IOF, e quando NAO usar Bedrock.
- hook: A AWS escreve documentacao otima sobre como ligar o Bedrock. Ninguem escreve sobre
  o modelo que voce quer nao estar disponivel na sua regiao, nem sobre quanto a conta muda
  quando o dolar mexe.
- bullets:
  - O que o Bedrock resolve que a API direta nao resolve (IAM, VPC, auditoria, LGPD)
  - Model Access e a armadilha da regiao: o que existe em sa-east-1 e o que nao existe
  - Do zero a primeira chamada: credencial, permissao e SDK
  - Claude Code apontando pro Bedrock: quando isso faz sentido num time
  - A conta real em BRL vs API direta — e os tres cenarios em que Bedrock nao compensa
- keyword_principal: aws bedrock o que e
- keywords_secundarias: como usar aws bedrock, bedrock claude, amazon bedrock tutorial, bedrock preco
- tags: ia, llm, aws, infraestrutura, claude, produto-ia
- dificuldade: medium
- volume: nao medido. SERP dura (AWS blog Brasil + docs Anthropic pt-BR), mas nenhum
  concorrente editorial independente toma decisao ou fala de custo em BRL.
- interlinks: llm-local-vs-api-2026-planilha-90-dias, ia-vai-ficar-mais-cara

## Oracle OCI Generative AI: o que e, quais modelos tem e quando escolher em vez do Bedrock
- publicar_em: 2026-09-01T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Terceiro de infraestrutura e o de menor concorrencia editorial dos tres: os docs
  da Oracle em pt-BR dominam a SERP, mas nao existe UM post independente em portugues.
  Diferencial e experiencia real de producao na OCI. Fecha o trio comparando as tres
  camadas de acesso a modelo.
- hook: Todo mundo compara OpenAI com Anthropic. Quase ninguem no Brasil escreve sobre a
  nuvem que ja hospeda metade dos bancos daqui — e que tem servico de IA generativa
  gerenciado com credito de 300 dolares pra testar.
- bullets:
  - O que e o OCI Generative AI e onde ele entra num stack de IA
  - Quais modelos estao disponiveis de verdade (e o que "modelo basico pre-treinado" quer dizer)
  - O modelo de cobranca que confunde: transacao por caractere vs por token
  - Cluster dedicado vs on-demand: quando faz sentido pagar por cluster
  - Bedrock vs OCI vs OpenRouter: tabela de decisao por cenario
- keyword_principal: oracle generative ai
- keywords_secundarias: oci generative ai, oracle ia generativa, oracle cloud llm, oci genai preco
- tags: ia, llm, oracle, infraestrutura, produto-ia
- dificuldade: medium
- volume: nao medido. Volume provavelmente menor que Bedrock, mas concorrencia editorial
  proxima de zero em pt-BR (so docs.oracle.com). Verificar no DataForSEO antes de escrever.
- interlinks: post do Bedrock, post do OpenRouter, llm-local-vs-api-2026-planilha-90-dias

## 10 ferramentas do engenheiro de IA em 2026 (e o criterio pra escolher quando elas mudarem)
- publicar_em: 2026-09-03T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Entra na briga direta com Alura, Tera e Udemy na query de listicle. Diferencial
  contra eles: ferramenta testada em producao, com veredito e nota, nao lista de catalogo.
  Diferencial contra o proprio blog: aquele post e ferramenta pra dev BACKEND codar; este e
  stack de LLMOps pro ENGENHEIRO DE IA operar (gateway, vector store, evals,
  observabilidade, harness). Moldura de criterio segura a durabilidade quando a lista
  envelhecer.
- hook: Lista de ferramentas apodrece em doze meses — a sua inclusive. Por isso cada uma
  aqui vem com o criterio que a colocou na lista: quando o criterio muda, voce troca a
  ferramenta sozinho, sem esperar o proximo post.
- bullets:
  - As 5 camadas do stack de LLMOps (e por que ferramenta de codar nao entra nessa lista)
  - As 10, por camada: o que faz, quando entra, nota e veredito de uma linha
  - O criterio de escolha em cada camada — o que sobrevive a troca de ferramenta
  - 3 que viralizaram em 2026 e nao cumpriram
  - Stack minimo pra comecar (3 ferramentas) vs stack de time maduro
- keyword_principal: ferramentas de ia para engenheiro de ia
- keywords_secundarias: stack do engenheiro de ia, ferramentas ai engineer 2026, llmops ferramentas, melhores ferramentas de ia para devs
- tags: ia, ai-engineer, llm, evals, observabilidade, harness, produto-ia
- dificuldade: medium
- volume: nao medido. SERP com autoridade alta de dominio (Alura, Tera, Udemy, Google
  Cloud, KDnuggets) — briga aceita pelo Lucas em 16/08. Ressalva registrada: listicle de
  ferramenta nao passa no gate de durabilidade sem a moldura de criterio.
- ATENCAO CANIBALIZACAO: separar de `ferramentas-de-ia-backend-top-12-testadas-2026`
  (persona dev backend, ferramenta de codar). Este e persona AI engineer, camada LLMOps.
  Linkar cruzado nos dois, sem repetir ferramenta entre as listas.
- interlinks: ferramentas-de-ia-backend-top-12-testadas-2026,
  observabilidade-agentes-ia-langsmith-langfuse-helicone (camada de observabilidade ja
  coberta a fundo — linkar, nao reescrever), evals-para-agentes-de-ia-llm-as-a-judge,
  engenheiro-de-ia-2026-o-que-faz
