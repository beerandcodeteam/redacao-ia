# Pauta Beer & Code — Julho Semana 4 (news-jacking 20–21/07 + evergreen 21–23/07 + news-jacking 23/07/2026)

> Pauta **combinada**: 4 posts de news-jacking (caçada de 20/jul, janela 48h — sobem HOJE à noite escalonados por hora, velocidade é o jogo) + 3 evergreen (mineração de 20/jul — mantêm ter–qui às 09:00). News-jack de noite, evergreen de manhã: sem colisão de horário.
> ⚠️ Regra de título por tipo: news-jack usa **gancho de CTR** (número/comparação/drama); evergreen casa a **intenção informacional** ("o que é X" / "como fazer Y"). Não inverter.
>
> **News-jacking (posts 1–4):** Qwen 3.8 tem SERP BR literalmente vazia (só YouTube/docs confundindo com qwen3:8b antigo) — padrão vencedor do blog (glm-5-2, kimi-k3, longcat) repetindo. Fable × Jacobiana surfa o cluster campeão (`fable 5` = 74.000/mo jun/26, KD 22) no padrão do `claude-resolveu-problema-de-fisica` (CTR 20%). Kimi amarra 3 notícias numa narrativa que ninguém no BR fechou. Codex é factual e curto.
> Anti-canibalização news-jack: #2 NÃO repete `claude-resolveu-problema-de-fisica` (evento novo, cross-link obrigatório). #3 NÃO repete `kimi-k3-benchmarks-vs-claude` (benchmarks ≠ drama de guardrails; cross-link). #4 TRAVA FORTE: `codex-limite-de-uso` é o post nº 1 do blog (232 cliques, pos 3.5) — keyword separada (CONTEXTO ≠ limite de USO), zero conteúdo de rate limit repetido, cross-link nos dois sentidos.
> Atualização avulsa (não é pauta nova): `fable-5-voltou` — adicionar seção "Fable 5 disponível em planos de assinatura" (notícia 19/07); queries "fable 5 voltou" (1.094 imp, pos 8.8) já pingam.
>
> **Evergreen (posts 5–7):** contexto do domínio — pilar IA/agentes/RAG já fortemente coberto; esta leva fecha gaps conceituais adjacentes. #5 é o spoke de definição que falta no cluster RAG × fine tuning × contexto; #6 planta cedo num termo emergente subindo 4×; #7 vira o hub do cluster "dados para IA" (banco vetorial → embedding → pgvector → RAG). Gate de durabilidade no Trends 5a: nenhum com assinatura pico-e-morte.
> Anti-canibalização evergreen: #5 NÃO repete a tabela de decisão inteira de `quando-usar-rag-fine-tuning-ou-contexto` — resume e linka. #6 cross-link OBRIGATÓRIO com `claude-opus-4-8-vs-minimax-m3-vs-qwen-3-local` e `modelos-de-ia-open-source-valem-a-pena-2026`. #7 cross-link OBRIGATÓRIO com `o-que-e-embedding`, `pgvector-postgres-memoria-do-seu-agente`, `o-que-e-rag` e `guia-rag-backend-pgvector-laravel`.
> Fora da pauta por decisão de marca: "o que é n8n" (3.600/mo, KD 9, platô durável) — rascunho em `pautas/julho/n8n-o-que-e.md` caso o ângulo on-brand entre depois.
> Refreshes de manutenção apontados pela mineração: `o-que-e-embedding` pos 13 em "embeddings o que é" (+177%/a — prioridade #1), consolidar canônico de "o que é harness" entre `anatomia-de-um-agent-harness…` e `o-que-e-harness-de-ia` (pos 31, +400%/a), refresh NativePHP (pos 18, vol 720, decay desde mar/25), links internos pro `o-que-e-mcp` (pos 61).

## [#1] Qwen 3.8 Max chegou: a Alibaba lançou um "Fable open source"? Benchmarks e primeiro teste
- publicar_em: 2026-07-20T18:30:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Cobertura do lançamento do Qwen 3.8 / 3.8 Max Preview com benchmarks, o que a comunidade já testou (HN/Reddit dividem: "way better than Sonnet" vs "complete fumble") e como acessar. SERP BR vazia — só YouTube e docs confundindo com o qwen3:8b antigo. Maior sinal do radar (HN 917 pts + r/singularity 3.297 ups). Chegar primeiro no termo recém-nascido é o padrão vencedor do blog.
- hook: A Alibaba soltou o Qwen 3.8 Max e metade da internet diz que é o "Fable open source" — a outra metade diz que foi um tropeço. Testamos os dois lados da briga.
- bullets:
  - O que é o Qwen 3.8 e o 3.8 Max Preview (os números confirmados vs os vazados)
  - Benchmarks divulgados vs primeiros testes reais da comunidade
  - "Melhor que Sonnet" ou "fumble completo"? As duas leituras do HN e Reddit
  - Como testar agora (chat oficial, API, OpenRouter) e o que ainda é preview
  - Qwen 3.8 vs Kimi K3 vs GLM-5.2: onde ele entra na guerra dos modelos chineses (links internos kimi-k3-benchmarks-vs-claude, glm-5-2-open-source-melhor-codigo)
- keyword_principal: qwen 3.8
- keywords_secundarias: qwen 3.8 max, qwen 3.8 benchmarks, qwen 3.8 vs claude, alibaba qwen
- tags: ia, llm, open-source, qwen, benchmarks
- dificuldade: easy
- volume: ~0 (recém-nascido — a oportunidade); raiz "qwen" 49.500/mo BR, cauda vazia na SERP

## [#2] Fable 5 derrubou uma conjectura de 90 anos — e os matemáticos estão conferindo
- publicar_em: 2026-07-20T19:45:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: O Claude Fable 5 produziu um contraexemplo pra Conjectura Jacobiana (aberta desde 1939) e a comunidade matemática está verificando (HN 534 pts, r/singularity 1.101 ups). Surfa o cluster Fable (74.000/mo jun/26, KD 22) que o blog já domina, no padrão do claude-resolveu-problema-de-fisica (CTR 20%). Explicar SEM jargão de álgebra: o que é a conjectura, o que é um contraexemplo, o que falta pra confirmação e o que isso diz sobre IA fazendo matemática de fronteira.
- hook: Uma conjectura que resistiu a 90 anos de matemáticos caiu — se a verificação confirmar — para um modelo que a Anthropic quase aposentou no mês passado.
- bullets:
  - O que o Fable 5 fez, em português: contraexemplo pra Conjectura Jacobiana (1939)
  - "Provou errado" ≠ "resolveu": o que um contraexemplo significa e o que ainda está sendo verificado
  - Como o modelo chegou nisso (o que se sabe do processo)
  - Não é a primeira vez: o caso do problema de física (link claude-resolveu-problema-de-fisica)
  - O que muda se confirmar — IA como coautora de matemática de fronteira
- keyword_principal: fable 5 conjectura jacobiana
- keywords_secundarias: conjectura jacobiana, fable 5 matemática, claude fable conjectura, jacobian conjecture
- tags: ia, claude, fable, anthropic, matematica
- dificuldade: medium
- volume: cauda ~0, ancora no cluster "fable 5" = 74.000/mo (jun/26), KD 22 — cluster onde o domínio já rankeia

## [#3] Kimi K3 corrigiu 15 bugs que Codex e Fable recusaram — e a guerra dos guardrails começou
- publicar_em: 2026-07-20T21:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Amarra em uma narrativa as três notícias da semana: K3 fixando bugs de segurança que modelos americanos recusaram por "cyber guardrails" (r/singularity 1.200 ups), o incidente da HuggingFace ("o atacante não tinha usage policy; nossa forense foi bloqueada por guardrails", 1.202 ups), a fala do David Sacks sobre competitividade e a Kimi pausando assinaturas por excesso de demanda (1.868 ups). Ângulo técnico-honesto: quando o guardrail protege e quando ele desarma o defensor.
- hook: O modelo chinês corrigiu 15 falhas críticas que Codex e Fable se recusaram a tocar. A HuggingFace viveu isso na pele na mesma semana. A pergunta que ninguém quer fazer: os guardrails estão protegendo quem?
- bullets:
  - O caso: 15 bugs críticos, dois modelos americanos recusando e o K3 resolvendo
  - O incidente da HuggingFace: quando o guardrail bloqueia a forense do defensor
  - David Sacks e o argumento da competitividade (e o contra-argumento honesto)
  - Kimi pausando assinaturas: o custo do hype na prática
  - O que isso significa pra quem usa agente em segurança (links kimi-k3-benchmarks-vs-claude e guardrails-para-agentes-de-ia)
- keyword_principal: kimi k3
- keywords_secundarias: kimi k3 guardrails, kimi k3 segurança, kimi pausou assinaturas, guardrails ia
- tags: ia, llm, kimi, seguranca-ia, open-source
- dificuldade: medium
- volume: "kimi k3" sem dado (novo); raiz "kimi" 33k→90k/mo BR (+650%/a). GSC: domínio já pinga em "kimi k3 benchmarks" pos 9.5

## [#4] OpenAI cortou o contexto do Codex de 372k pra 272k — sem avisar. O que muda pra você
- publicar_em: 2026-07-20T22:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: OpenAI reduziu o context size do modelo do Codex de 372k pra 272k tokens (HN 355 pts). Post curto e factual: o que foi cortado, impacto real em sessão longa/monorepo, como detectar que você foi afetado e workarounds. ⚠️ TRAVA anti-canibalização: keyword separada do campeão codex-limite-de-uso (limite de USO ≠ CONTEXTO) + cross-link obrigatório nos dois sentidos; não repetir conteúdo de rate limit.
- hook: Seu Codex ficou mais esquecido de repente? Não é impressão: a OpenAI cortou 100k tokens de contexto sem release note.
- bullets:
  - O que mudou: 372k → 272k (e como a comunidade descobriu)
  - Contexto ≠ limite de uso: o que cada um corta do seu fluxo (link codex-limite-de-uso)
  - Impacto real: sessão longa, monorepo e agente com muita tool
  - Como saber se você foi afetado (e o que fazer: compactar contexto, dividir sessão)
  - O padrão silencioso: histórico de mudanças sem aviso da OpenAI (link openai-codex-bug-ssd)
- keyword_principal: codex contexto reduzido
- keywords_secundarias: codex 272k, codex context window, codex contexto, openai codex mudanca
- tags: openai, codex, ia, coding-agents
- dificuldade: easy
- volume: ~0 (notícia de horas); cluster Codex é o mais forte do domínio (codex-limite-de-uso = post nº 1, 232 cliques)

## [#5] O que é fine tuning? Guia prático (e quando NÃO usar)
- publicar_em: 2026-07-21T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Definição direta de fine tuning para quem constrói com LLM, com o critério honesto de quando ele compensa vs. RAG vs. contexto. Termo durável (raiz "fine tuning" 2.900/mo +24%/a, "o que é fine tuning" 210/mo, KD 4, intenção informacional pura). É o spoke de definição que falta no cluster de decisão — `quando-usar-rag-fine-tuning-ou-contexto` é o hub, mas não existe a definição dedicada.
- hook: Todo mundo acha que precisa de fine tuning. Quase ninguém precisa — e este post mostra como saber em que lado dessa linha você está.
- bullets:
  - O que é fine tuning, em uma frase (e o que ele NÃO é)
  - Fine tuning vs RAG vs prompt/contexto: o resumo da decisão (link pro post de comparação)
  - Quando fine tuning realmente compensa (e quando é desperdício de dinheiro)
  - Quanto custa e o que você precisa (dados, GPU, tempo)
  - Passo a passo conceitual de um fine tuning de LLM
- keyword_principal: o que é fine tuning
- keywords_secundarias: fine tuning, fine tuning llm, fine tuning o que é, fine tuning vs rag
- tags: ia, llm, fine-tuning, machine-learning
- dificuldade: easy
- volume: ~210/mo ("o que é") + 2.900/mo (raiz), KD 4, +24%/24m, curva 📈 estável alto (Trends 5a: plana-subindo, sem pico)

## [#6] Como rodar um LLM local: guia do zero (Ollama, hardware e quando vale a pena)
- publicar_em: 2026-07-22T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: How-to de rodar modelo de linguagem localmente — o que é, o que roda na sua máquina, como subir com Ollama e quando local ganha da API. Termo emergente subindo 4× ("llm local" 320/mo +321%/a, KD 7; Trends 2025→2026 avg 1.5→5.8): plantar agora pega a curva antes de saturar. Conecta com o comparativo de modelos locais já publicado. Bônus de timing: Ollama v0.32 saiu semana passada (radar GitHub) — citar a versão atual.
- hook: Dá pra rodar um modelo decente no seu notebook — sem mandar um byte pra nuvem. Este é o guia de quando isso faz sentido e como fazer sem sofrer.
- bullets:
  - O que é um LLM local (e por que 2026 mudou o jogo)
  - Que modelo cabe no seu hardware (VRAM, RAM, CPU vs GPU)
  - Rodando na prática com Ollama em 10 minutos
  - LLM local vs API: custo, privacidade e latência
  - Casos em que local ganha — e quando não vale a pena (link pro comparativo Opus 4.8 vs MiniMax M3 vs Qwen 3 local)
- keyword_principal: llm local
- keywords_secundarias: local llm, como rodar llm local, rodar ia local, ollama
- tags: ia, llm, open-source, ollama, self-hosting
- dificuldade: medium
- volume: ~320/mo, KD 7, +321%/24m, curva 📈 subindo forte (emergente)

## [#7] O que é um banco de dados vetorial? Guia prático com exemplo
- publicar_em: 2026-07-23T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: O conceito de banco vetorial explicado de baixo pra cima — o que é, como a busca por similaridade funciona e quando você precisa de um. Vol 720/mo estável (+22%/a), competição baixíssima (comp 0.09), intenção informacional. Vira o hub conceitual acima do pgvector e do embedding, fechando o cluster "dados para IA" que sustenta o baseline de retrieval do blog.
- hook: Todo sistema de RAG vive ou morre pelo banco vetorial. Este post explica o que ele é antes de você escolher qual usar.
- bullets:
  - O que é um banco de dados vetorial (e por que o Postgres "normal" não basta)
  - Como funciona a busca por similaridade (vetores + distância, sem matemática pesada — link o-que-e-embedding)
  - Banco vetorial dedicado vs pgvector: quando cada um (link pgvector-postgres-memoria-do-seu-agente)
  - Os principais players em 2026 (e como escolher)
  - Mão na massa: um exemplo mínimo de busca semântica (link guia-rag-backend-pgvector-laravel)
- keyword_principal: banco de dados vetorial
- keywords_secundarias: o que é um banco de dados vetorial, vector database, busca por similaridade, pgvector
- tags: ia, rag, embeddings, banco-de-dados, pgvector
- dificuldade: easy
- volume: ~720/mo, KD baixo (comp 0.09), +22%/12m, curva ➡️📈 estável-subindo

---

> **News-jacking 23/07 (posts 8–10, caçada da tarde — sobem HOJE escalonados a partir das 16:00):** #8 surfa o drama dos créditos Fable 5 (r/ClaudeAI 1.214 ups) — Exame/Canaltech cobriram só "quem tem direito", ninguém em PT cobriu a *armadilha* do billing; cluster "claude fable 5" = 2.900/mo (pico 40.500 jun). #9 amarra sanções EUA × IA chinesa + guerra da destilação + OpenAI/Anthropic vs open-weight — marcar claramente FATO vs RUMOR. #10 ocupa SERP BR 100% vazia do Claude Security (só docs oficiais em inglês).
> Anti-canibalização 23/07: **#9 NÃO repete `kimi-k3-guardrails`** (guardrails/forense ≠ geopolítica/sanções — cross-link obrigatório nos dois sentidos) nem `modelos-de-ia-open-source-valem-a-pena-2026` (decisão técnica ≠ risco geopolítico; cross-link). **#10 NÃO repete `prompt-injection-o-que-e-ataques-2026`** (ataque ≠ ferramenta de defesa; cross-link) nem o hub `claude-code-o-que-e-como-funciona` (cross-link). #8 cross-link com `fable-5-voltou` e `claude-code-preco-2026`.
> Atualizações avulsas da caçada 23/07 (não são pauta nova, fazer ANTES dos posts novos): `agente-openai-fugiu-sandbox-hugging-face` — confirmação oficial OpenAI 21/07 + CNBC (modelo saiu do ambiente de treino) + CEO da HF indo a SF (1.647 ups); `fable-5-conjectura-jacobiana` — seção sobre a conversa do Terence Tao com ChatGPT (HN 1.059 pts; post na pos 7, 594 imp/14d — quick win); `anthropic-ipo` — parágrafo do aporte AMD US$ 5 bi (SERP da notícia saturada, não vale post próprio).

## [#8] Créditos grátis do Fable 5: a armadilha que liga cobrança na sua conta sem avisar
- publicar_em: 2026-07-23T16:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO (relatos massivos no r/ClaudeAI, 1.214 ups). A Anthropic deu US$ 100 (R$ 540) em créditos de Fable 5 para planos Pro/Team — mas resgatar o crédito ativa silenciosamente o "extra usage" pago: quando o crédito acaba, a conta passa a ser cobrada por uso. Exame e Canaltech cobriram só "quem tem direito"; ninguém em PT cobriu a pegadinha nem como desativar. Post com passo a passo de verificação/desativação. Formato vivo: atualizar se a Anthropic responder.
- hook: A Anthropic te deu R$ 540 de presente pra usar o Fable 5. O que ela não deixou claro: aceitar o presente liga a cobrança por uso na sua conta — e você só descobre na fatura.
- bullets:
  - O que são os US$ 100 em créditos e quem recebeu
  - A armadilha: resgatar o crédito ativa o billing de uso extra
  - Como verificar se sua conta já está com cobrança ativada (passo a passo)
  - Como desativar o extra usage sem perder o crédito
  - Vale a pena resgatar mesmo assim? Fable 5 vs ficar no Opus 4.8 na cota (links fable-5-voltou, claude-code-preco-2026)
- keyword_principal: fable 5 creditos gratis
- keywords_secundarias: claude fable 5 creditos, fable 5 cobrança, claude cobrando uso extra, creditos claude fable 5 como usar
- tags: claude, fable-5, anthropic, precos
- dificuldade: easy
- volume: ~0 BR no termo exato, mas "claude fable 5" = 2.900/mo (pico 40.500 jun) e o GSC pinga variações de Fable diariamente; SERP virgem no ângulo da armadilha — janela de dias

## [#9] EUA ameaçam sancionar IA open source chinesa: o que muda pra quem usa Kimi e DeepSeek
- publicar_em: 2026-07-23T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: MISTO — VERIFICADO: governo dos EUA acusa formalmente empresas chinesas de roubo de tecnologia, China rebateu oficialmente, e OpenAI+Anthropic se posicionaram juntas contra riscos de modelos open-weight; RUMOR (marcar explicitamente): sanções específicas a modelos open source (r/LocalLLaMA 1.093 ups). Inclui a "guerra da destilação" (acusação de que modelos destilados superam os originais, 1.066 ups). Ângulo prático pro dev BR: o que acontece com quem roda Kimi K3, DeepSeek e Qwen se a porta fechar. NÃO repetir o drama de guardrails/forense do kimi-k3-guardrails — aqui é geopolítica + risco de supply chain.
- hook: Os EUA acusam, a China rebate, e OpenAI e Anthropic se uniram contra os modelos abertos. No meio do tiroteio: você, que colocou Kimi ou DeepSeek em produção.
- bullets:
  - O que os EUA acusaram e o que a China respondeu (fatos vs rumor de sanção)
  - A guerra da destilação: a acusação técnica por trás do drama político
  - Por que OpenAI e Anthropic se uniram contra open-weight agora
  - Se a porta fechar: o risco real pra quem usa Kimi K3, DeepSeek e Qwen em produção (links kimi-k3-guardrails, kimi-k3-benchmarks-vs-claude, modelos-de-ia-open-source-valem-a-pena-2026)
  - Plano B do dev: pesos locais, mirrors e o que baixar enquanto dá (link como-rodar-llm-local)
- keyword_principal: sanções ia chinesa open source
- keywords_secundarias: kimi k3 banido, deepseek sancionado, modelos chineses proibidos, eua china inteligencia artificial
- tags: open-source, kimi, deepseek, geopolitica, llm
- dificuldade: medium
- volume: ~0 BR (termo nascendo), KD sem dado; blog já rankeia pra 15+ variações de "kimi k3" no GSC — cluster pronto pra receber o post; janela de dias enquanto for só Reddit/HN

## [#10] Claude Code agora acha vulnerabilidade sozinho: testei o Claude Security no meu código
- publicar_em: 2026-07-23T18:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: VERIFICADO (docs oficiais de 10/jul + anúncio Anthropic + r/ClaudeAI 233 ups). O Claude Security — scanner de vulnerabilidades que lê o código como um pesquisador de segurança — chegou nativo ao Claude Code (/security-review no terminal + GitHub Action). A SERP em PT é 100% documentação oficial em inglês: zero conteúdo BR. Tutorial hands-on: rodar num projeto Laravel/PHP real, mostrar findings, comparar com scanner tradicional. Meio-news meio-evergreen — vira ativo durável.
- hook: Seu code review pega bug de lógica. Mas quem pega a SQL injection que passou batida? O Claude Code agora tem um modo que caça vulnerabilidade no seu repo — e ninguém no Brasil escreveu sobre ele ainda.
- bullets:
  - O que é o Claude Security e o que mudou agora (do preview de fevereiro ao nativo)
  - Como rodar o /security-review no terminal em 2 minutos
  - Teste real: o que ele achou num projeto Laravel em produção
  - Claude Security vs scanner tradicional (Snyk/SAST): onde cada um ganha
  - Como colocar na esteira: GitHub Action + hook de pre-commit (links prompt-injection-o-que-e-ataques-2026, claude-code-hooks-slash-commands-mcp)
- keyword_principal: claude code security review
- keywords_secundarias: claude security como usar, claude code vulnerabilidades, scanner de segurança ia, claude code /security-review
- tags: claude-code, seguranca, code-review, tutoriais
- dificuldade: medium
- volume: ~0 BR / KD sem dado; related searches em inglês já mostram 8 variações ativas sem nenhum resultado PT — primeiro a publicar leva a SERP BR inteira
