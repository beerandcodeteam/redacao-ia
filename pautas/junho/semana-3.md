# Pauta Beer & Code — Semana 3 (Seg 15/06 a Dom 21/06/2026)

> 21 posts (3/dia). Gerado pela skill planejar-pauta cruzando GSC + DataForSEO + GA4.
> Top 5 por ROI: #1 Harness, #8 Claude Code hooks, #2 Claude Agent SDK, #7 Codex CLI, #3 Opus 4.8 vs Minimax vs Qwen.

## O que é Harness de IA? O ambiente que faz seu agente parar de travar
- publicar_em: 2026-06-15T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Post definitional de topo de funil sobre "harness de IA" — o ambiente que roda o agente (loop, ferramentas, estado, guardrails). Captura a query "o que é harness" (KD 5, subindo 400%/ano) e serve de hub que linka os posts avançados de anatomia de harness.
- hook: Todo mundo fala em prompt. Quase ninguém fala no que de fato faz o agente funcionar em produção: o harness.
- bullets:
  - O que é harness de IA (e por que não é o prompt)
  - As camadas: loop, tools, estado, feedback, guardrails
  - Harness vs framework vs agente: o que é o quê
  - Exemplo concreto: o que acontece numa volta do loop
  - Quando você precisa de um harness próprio
- keyword_principal: o que é harness
- keywords_secundarias: harness de ia, harness ia o que é, agent harness, harness engineering
- tags: ia, ai-agents, harness, agentes-de-ia
- dificuldade: easy
- volume: ~390/mo (KD 5, +400%/ano)

## Claude -p vai morrer: como migrar para o Claude Agent SDK
- publicar_em: 2026-06-15T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: O modo headless `claude -p` está sendo substituído pelo Claude Agent SDK. Guia prático de migração, o que muda no uso com seu plano Claude e como rodar agentes headless do jeito novo.
- hook: Se o seu pipeline depende de `claude -p`, ele tem prazo de validade. A boa notícia: o que vem é melhor.
- bullets:
  - Por que a Anthropic está aposentando o `claude -p`
  - O que é o Claude Agent SDK e o que muda na prática
  - Migrando um script headless passo a passo
  - Usar o Agent SDK com seu plano Claude (sem API key avulsa)
  - Erros comuns na migração e como evitar
- keyword_principal: claude agent sdk
- keywords_secundarias: claude code headless, claude -p, agent sdk, claude agent sdk plano
- tags: ia, claude, claude-code, anthropic, ai-agents
- dificuldade: medium
- volume: ~390/mo (KD 25, +8700%/ano)

## Opus 4.8 vs Minimax M3 vs Qwen 3: paguei caro, paguei barato e rodei de graça
- publicar_em: 2026-06-15T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Construí o mesmo app (encurtador de links) 3 vezes, com zero intervenção humana, usando Claude Opus 4.8 (US$100/mês), Minimax M3 (US$20) e Qwen 3.6 local numa RTX 4080. Resultado, tempo e veredito honesto sobre modelo pago vs barato vs local. Baseado no vídeo próprio.
- hook: Eu esperava que o caro fosse destruir e o de graça fosse ruim. Acertei numa coisa e errei feio na outra.
- bullets:
  - O setup: mesma spec, ralph.sh e contexto zerado por fase
  - Claude Opus 4.8: 46 min, código impecável, front mediano
  - Minimax M3: 3h56, melhor front, mas bateu limite de token
  - Qwen 3.6 local: 26 horas para entregar… nada
  - Veredito: por que local ainda não paga seu boleto em 2026
- keyword_principal: claude opus 4.8 vs minimax
- keywords_secundarias: minimax m3, qwen 3 local, modelo de ia local, modelos de ia open source
- tags: ia, llm, claude, anthropic, modelos-open-source
- dificuldade: medium
- volume: nicho (qwen 49k/mo amplo); aposta de formato comparativo (campeão de CTR)

## Agentic RAG: quando seu RAG precisa virar agente
- publicar_em: 2026-06-16T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Diferença entre RAG clássico e Agentic RAG, quando o agente decide buscar/re-buscar, e como montar isso sem explodir custo. Bom volume (1.000/mo) e KD baixo (19).
- hook: RAG tradicional busca uma vez e reza. Agentic RAG decide quando buscar, o que buscar e quando parar.
- bullets:
  - RAG clássico vs Agentic RAG: o que muda
  - O loop de decisão: query rewriting, re-retrieval, self-check
  - Arquitetura mínima de um agentic RAG
  - Custo e latência: onde mora a armadilha
  - Quando NÃO usar agentic RAG
- keyword_principal: agentic rag
- keywords_secundarias: rag agêntico, agentic retrieval, rag com agente, quando usar agentic rag
- tags: ia, rag, ai-agents, embeddings, llm
- dificuldade: medium
- volume: ~1.000/mo (KD 19)

## Ferramentas de engenharia de contexto que eu uso em produção
- publicar_em: 2026-06-16T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Lista prática e opinativa de ferramentas de engenharia de contexto (compressão, recuperação, gestão de janela, observabilidade de contexto). Captura "ferramentas de engenharia de contexto" (GSC 26 impr, pos 26.8 sem post dedicado).
- hook: Context engineering deixou de ser arte e virou stack. Estas são as ferramentas que seguram o agente em produção.
- bullets:
  - O que é engenharia de contexto (rápido)
  - Compressão e sumarização de contexto
  - Recuperação e roteamento de contexto
  - Observabilidade: vendo o que entra na janela
  - Meu stack atual e quando cada peça entra
- keyword_principal: ferramentas de engenharia de contexto
- keywords_secundarias: engenharia de contexto, context engineering, engenharia de contexto anthropic
- tags: ia, llm, engenharia-de-contexto, prompt-engineering, ai-agents
- dificuldade: medium
- volume: ~590/mo (context engineering, KD 37, +7100%/ano)

## Sistemas multiagentes: arquitetura e orquestração assíncrona na prática
- publicar_em: 2026-06-16T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: O que são sistemas multiagentes, quando vale dividir em vários agentes e como orquestrar de forma assíncrona. SERP fraca (brecha real) + baseado no cookbook async multi-agent da Anthropic.
- hook: Um agente que faz tudo é fácil de demonstrar e difícil de manter. A saída é dividir — e orquestrar direito.
- bullets:
  - O que é um sistema multiagente (e quando vale)
  - Padrões: supervisor, pipeline, fan-out
  - Orquestração assíncrona: por que não bloquear
  - Estado compartilhado e handoff entre agentes
  - Erros clássicos de multiagente em produção
- keyword_principal: sistemas multiagentes
- keywords_secundarias: orquestração de agentes, arquitetura multiagente, multi agente ia, async multi-agent
- tags: ia, ai-agents, multi-agentes, arquitetura, llm
- dificuldade: hard
- volume: ~140/mo (comp. baixa, SERP fraca, +56%/mês)

## Codex CLI: usando goals para guiar o agente da OpenAI
- publicar_em: 2026-06-17T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Como usar o recurso de goals no Codex para dar direção ao agente sem microgerenciar. Baseado no cookbook da OpenAI. Tópico em alta (codex cli 3.600/mo, +236%/ano).
- hook: Dar tarefa pro Codex é fácil. Dar um objetivo que ele persiga sozinho é o que separa demo de uso real.
- bullets:
  - O que são goals no Codex e por que importam
  - Goal vs prompt vs spec: a diferença prática
  - Configurando um goal passo a passo
  - Goals + verificação automática (testes/commit)
  - Quando o goal atrapalha em vez de ajudar
- keyword_principal: codex cli
- keywords_secundarias: openai codex, goals codex, codex goals, usar codex
- tags: ia, openai, codex, ai-agents, agentic-code
- dificuldade: medium
- volume: ~3.600/mo (KD 25, +236%/ano)

## Claude Code: hooks, slash commands e MCP que mudam seu fluxo
- publicar_em: 2026-06-17T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Guia prático dos três recursos que mais aceleram o Claude Code: hooks, slash commands e MCP. Já aparecemos em pos 3–6 para essas queries sem um post dedicado — quick-win claro.
- hook: A diferença entre quem usa Claude Code e quem voa com ele está em três recursos que quase ninguém configura.
- bullets:
  - Hooks: automatizando o que você repete
  - Slash commands custom: seus fluxos virando comando
  - MCP: plugando ferramentas e dados no agente
  - Receita combinando os três
  - settings.json: o que vale versionar
- keyword_principal: claude code hooks
- keywords_secundarias: claude code slash commands, claude code mcp, claude code custom commands
- tags: ia, claude, claude-code, anthropic, mcp
- dificuldade: medium
- volume: long-tail de "claude code" (135k/mo); GSC pos 3–6

## Claude Code em monorepo e large codebase: como não estourar contexto
- publicar_em: 2026-06-17T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Estratégias para usar Claude Code em bases grandes e monorepos: escopo, CLAUDE.md, subagentes, navegação e o que fazer pra ele não se perder. Ride o tópico gigante "claude code".
- hook: Em projeto pequeno qualquer agente brilha. Em monorepo de 500 mil linhas é onde a engenharia de verdade aparece.
- bullets:
  - Por que large codebase quebra o agente
  - CLAUDE.md e convenções que dão contexto barato
  - Escopo por pacote e navegação inteligente
  - Subagentes para dividir o token budget
  - Migrações em escala: quando usar workflows
- keyword_principal: claude code monorepo
- keywords_secundarias: claude code large codebase, claude code base grande, claude code monorepo setup
- tags: ia, claude, claude-code, anthropic, monorepo
- dificuldade: hard
- volume: long-tail de "claude code" (135k/mo, KD 36)

## Loop engineering: o agente que melhora o próprio código
- publicar_em: 2026-06-18T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Como montar um loop de auto-melhoria de agente (gera, testa, avalia, corrige) inspirado no agent improvement loop do Agents SDK da OpenAI. Aposta de autoridade — volume BR ~0, mas tópico forte de cluster.
- hook: O pulo do gato não é o agente acertar de primeira. É ele perceber que errou e se corrigir sozinho.
- bullets:
  - O que é um agent improvement loop
  - Os 4 passos: gerar, executar, avaliar, refinar
  - O sinal de parada (testes + critério de sucesso)
  - Evals dentro do loop, não depois
  - Custo: quando o loop vira buraco negro
- keyword_principal: agent improvement loop
- keywords_secundarias: loop de agente, self-improving agent, agente que melhora sozinho, agent loop
- tags: ia, ai-agents, openai, agentic-code, evals
- dificuldade: hard
- volume: ~0 BR (aposta de autoridade; ride codex cli)

## Desenvolvedor de IA vs Engenheiro de IA: 7 diferenças que importam
- publicar_em: 2026-06-18T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Comparativo direto entre desenvolvedor de IA e engenheiro de IA: escopo, skills, salário e carreira. GSC mostra 37 impressões em pos 29 sem post dedicado — quick-win de cluster de carreira.
- hook: Os títulos parecem sinônimos. Na vaga, no salário e no dia a dia, não são.
- bullets:
  - As 7 diferenças (escopo, skills, entrega…)
  - Quem faz o quê no time de IA
  - Salário: onde cada um cai (linka post de salário)
  - Como migrar de dev para engenheiro de IA
  - Qual caminho escolher em 2026
- keyword_principal: desenvolvedor de ia vs engenheiro de ia
- keywords_secundarias: engenheiro de ia vs cientista de dados, diferença dev e engenheiro de ia
- tags: ia, carreira, ai-engineer, mercado-de-trabalho
- dificuldade: easy
- volume: GSC 37 impr (pos 29.4), sem post dedicado

## Engenheiro de IA: o que faz no dia a dia em 2026
- publicar_em: 2026-06-18T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: O que um engenheiro de IA realmente faz, ferramentas, rotina e como entrar na área. Captura "engenheiro de ia o que faz" (30/mo, +600%/ano) e reforça o cluster de carreira que já converte.
- hook: Spoiler: não é treinar modelo o dia inteiro. É bem mais perto de engenharia de software do que parece.
- bullets:
  - O que faz um engenheiro de IA (rotina real)
  - Ferramentas e stack do dia a dia
  - O que NÃO é função dele
  - Skills que o mercado paga em 2026
  - Como dar o primeiro passo
- keyword_principal: engenheiro de ia o que faz
- keywords_secundarias: o que faz um engenheiro de ia, engenheiro de ia 2026, ai engineer o que faz
- tags: ia, carreira, ai-engineer, mercado-de-trabalho
- dificuldade: easy
- volume: ~30/mo (+600%/ano)

## Como criar um servidor MCP do zero (passo a passo)
- publicar_em: 2026-06-19T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Tutorial mão na massa de criação de um servidor MCP (tools, resources, prompts) com stdio e HTTP. Constrói autoridade no cluster MCP e gera links internos que ajudam o `o-que-e-mcp` a sair da pos 61.
- hook: Entender o que é MCP é uma coisa. Subir o seu primeiro servidor e ver o agente usá-lo é outra.
- bullets:
  - Setup do projeto e SDK MCP
  - Expondo sua primeira tool
  - Resources e prompts: além das tools
  - Rodando via stdio e via HTTP
  - Conectando no Claude/Cursor e testando
- keyword_principal: como criar um servidor mcp
- keywords_secundarias: criar servidor mcp, mcp server tutorial, como fazer um mcp, servidor mcp python
- tags: ia, mcp, claude, anthropic, ai-agents
- dificuldade: medium
- volume: nicho (cluster MCP; suporte ao ranking de o-que-e-mcp)

## Construir um bot de Slack com Claude: um agente de dados no seu workspace
- publicar_em: 2026-06-19T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Tutorial de um bot de Slack que responde perguntas sobre seus dados usando Claude. Baseado no cookbook da Anthropic. Volume BR baixíssimo (~10/mo) — entra como tutorial de autoridade.
- hook: O melhor lugar pra colocar um agente de dados não é um dashboard novo. É onde o time já vive: o Slack.
- bullets:
  - Arquitetura: Slack + Claude + sua fonte de dados
  - Configurando o app e os eventos do Slack
  - Conectando o Claude Agent SDK
  - Dando acesso a dados com segurança
  - Deploy e limites de uso
- keyword_principal: criar bot no slack
- keywords_secundarias: bot slack ia, agente de ia no slack, chatbot slack claude, slack bot python
- tags: ia, claude, ai-agents, slack, anthropic
- dificuldade: medium
- volume: ~10/mo (aposta de autoridade/tutorial)

## Qual IA usar para programar em 2026: Claude Code vs Codex
- publicar_em: 2026-06-19T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Comparativo prático entre Claude Code e Codex para coding agêntico: força em cada cenário (repo real, terminal, custo). Formato comparativo (seu campeão de CTR) sobre dois tópicos gigantes em alta.
- hook: No fim do meu teste de modelos, dois sobraram de pé pra trabalho real: Claude e Codex. Qual é o seu?
- bullets:
  - Onde o Claude Code lidera (SWE-Bench Pro)
  - Onde o Codex lidera (coding de terminal)
  - Custo e planos lado a lado
  - Fluxo: hooks/MCP vs goals/loop
  - Veredito por tipo de dev
- keyword_principal: melhor ia para programar 2026
- keywords_secundarias: claude code vs codex, claude code ou codex, melhor ia para codar
- tags: ia, claude, openai, claude-code, codex
- dificuldade: medium
- volume: médio (KD alto; formato comparativo de alta tração)

## Como deixar sua empresa pronta para IA: o guia de prontidão (AI readiness)
- publicar_em: 2026-06-20T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Framework de prontidão para IA (dados, processos, pessoas, governança) com base no conceito de AI readiness do Gartner. Volume BR baixo, mas público decisor e ângulo de lead-gen.
- hook: Comprar licença de IA não deixa a empresa pronta pra IA. Quase sempre o gargalo nem é tecnológico.
- bullets:
  - O que é prontidão para IA (e o que não é)
  - As 4 dimensões: dados, processos, pessoas, governança
  - Diagnóstico rápido: onde sua empresa trava
  - Erros comuns na adoção de IA
  - Roteiro dos primeiros 90 dias
- keyword_principal: prontidão para ia
- keywords_secundarias: empresa pronta para ia, ai readiness, maturidade em ia, adoção de ia na empresa
- tags: ia, gestao, transformacao-digital, negocios
- dificuldade: easy
- volume: ~90/mo (ai readiness, +180%/ano; aposta lead-gen)

## Modelos de IA open source e locais valem a pena em 2026?
- publicar_em: 2026-06-20T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Análise honesta de quando rodar LLM open source/local compensa (custo, privacidade, qualidade) usando o aprendizado do teste prático com Qwen local. Ride o ângulo "de graça" do vídeo.
- hook: "Rodo um modelo local e paro de pagar API." A real é mais cara — e mais lenta — do que parece.
- bullets:
  - O que dá pra rodar local hoje (e em que hardware)
  - Custo real: GPU, RAM, tempo
  - Qualidade: onde o open source ainda perde
  - Casos em que local FAZ sentido (privacidade, escala)
  - Veredito: API top de linha vs local em 2026
- keyword_principal: modelos de ia open source
- keywords_secundarias: llm open source, modelo de ia local, rodar llm local, qwen local
- tags: ia, llm, modelos-open-source, infraestrutura
- dificuldade: medium
- volume: ~50–170/mo (KD 26, +53–80%)

## Async multi-agent: padrões de orquestração assíncrona em produção
- publicar_em: 2026-06-20T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Aprofundamento técnico nos padrões de orquestração assíncrona de múltiplos agentes (filas, paralelismo, agregação de resultados). Companion do post "Sistemas multiagentes" — DEVE mirar keyword diferente e cross-linkar para não canibalizar.
- hook: Rodar 50 agentes em paralelo é fácil. Costurar o resultado deles sem virar caos é o problema de verdade.
- bullets:
  - Por que assíncrono em multiagente
  - Padrões de fan-out/fan-in
  - Filas e backpressure entre agentes
  - Agregação e reconciliação de resultados
  - Observabilidade de execuções paralelas
- keyword_principal: orquestração de agentes
- keywords_secundarias: async multi-agent, orquestração assíncrona de agentes, paralelismo de agentes
- tags: ia, ai-agents, multi-agentes, arquitetura, async
- dificuldade: hard
- volume: nicho (aposta; cuidado de canibalização com "Sistemas multiagentes")

## Como criar evals para agentes de IA com LLM-as-a-judge
- publicar_em: 2026-06-21T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Como montar um pipeline de avaliação de agentes usando LLM-as-a-judge: dataset, critérios, scoring e CI. GSC mostra demanda em "ai agent evals"/"eval pipeline" (pos 5). Cluster forte que já temos base.
- hook: "Tá funcionando bem" não é métrica. Sem eval, você está fazendo deploy no escuro.
- bullets:
  - Por que eval de agente é diferente de teste unitário
  - Montando o dataset de avaliação
  - LLM-as-a-judge: prompt e critérios
  - Scoring e thresholds que fazem sentido
  - Rodando evals no CI
- keyword_principal: evals para agentes de ia
- keywords_secundarias: ai agent evals, llm as a judge, avaliação de agentes, eval pipeline
- tags: ia, ai-agents, evals, llm, qualidade
- dificuldade: medium
- volume: nicho (GSC pos 5; cluster com base existente)

## RAG híbrido na prática: BM25 + embeddings + reranker
- publicar_em: 2026-06-21T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: Como combinar busca lexical (BM25) com busca semântica e um reranker para subir a qualidade do RAG. Já rankeamos pos 3 em "cross encoder reranker" — cluster com tração comprovada.
- hook: Embedding sozinho erra mais do que você imagina. A combinação com BM25 e um reranker muda o jogo.
- bullets:
  - Por que busca semântica pura falha
  - BM25: o lexical que ainda salva o dia
  - Fusão de resultados (RRF)
  - Reranker (cross-encoder): o último filtro
  - Medindo o ganho de qualidade
- keyword_principal: rag híbrido
- keywords_secundarias: bm25 reranker, cross encoder reranker, busca híbrida rag, reranker langchain
- tags: ia, rag, embeddings, reranker, llm
- dificuldade: hard
- volume: nicho (já em pos 3 no cluster reranker)

## Effort Control no Claude Opus 4.8: controlando custo e raciocínio do agente
- publicar_em: 2026-06-21T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Como usar o Effort Control (high/xhigh/max) do Opus 4.8 para equilibrar custo, latência e qualidade nos seus agentes. Volume BR ~0 — aposta timely que ride o tema Opus 4.8.
- hook: Nem toda tarefa merece o modo "pensa o máximo". Effort Control é o botão de volume que faltava na conta.
- bullets:
  - O que é Effort Control e os 3 níveis
  - high vs xhigh vs max: quando cada um
  - Impacto em custo e latência
  - Escolhendo effort por tipo de tarefa
  - Exemplos práticos no produto
- keyword_principal: effort control claude
- keywords_secundarias: claude opus 4.8 effort, controlar custo agente ia, effort control opus
- tags: ia, claude, anthropic, opus-4-8, custo
- dificuldade: easy
- volume: ~0 BR (aposta timely; ride Opus 4.8)
