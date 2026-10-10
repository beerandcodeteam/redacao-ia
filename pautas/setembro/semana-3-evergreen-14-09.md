# Pauta evergreen — setembro, semana 3 (15/09 a 19/09) — versão 2, lente de DOR de topo de funil

Origem: `minerar-evergreen` em 13/09/2026, refeita depois do feedback do Lucas: a v1 (o que é Codex, instalar Claude Code, preço do Claude)
era pauta de produto. O que cresce no blog é **dor de quem ainda não escolheu produto**: "como economizar tokens" (+340%),
"qual a melhor IA para programar" (+278%). Critério desta versão: consciência baixa + problema concreto + demanda estável.
Todos passaram no gate de durabilidade (curva 12m plana ou subindo, sem pico-e-morte). Produto só aparece como resposta, nunca como título.

Cluster: hub **"Qual IA usar e como não gastar à toa"**. Os 5 posts novos se linkam entre si e com os refreshes no fim.

---

## Por que o Claude gasta tanto token (e como fazer o limite do Pro e do Max durar)
- publicar_em: 2026-09-15T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: A mesma dor do post que mais cresceu no blog (economizar tokens), um nível mais específico: quem usa Claude e Claude Code e vê o limite de sessão acabar na terça de manhã. Explica os dois limites (janela de contexto vs cota de 5h e teto semanal), por que uma pergunta de uma linha consome o dia inteiro (cache quebrado, contexto inchado, MCP demais, Auto Mode), qual modelo gasta menos, como medir o próprio consumo e as alavancas que fazem a sessão durar. Validado pela planejar-pauta em 13/09: o post genérico do blog já está em **posição 6 orgânica** para "como economizar tokens no claude", então a keyword principal deste post é a dor do LIMITE ("quantos tokens tem o claude pro", 590/mo e 1.600 nos últimos 3 meses, rd 2, sem post dedicado) e as variações de "economizar no claude" entram como secundárias, com link explícito do hub pra cá e daqui pro hub. SERP do limite: Reddit, suporte da Anthropic, Truefoundry traduzido, Balta; AI Overview presente, citando Reddit e YouTube, nenhum post BR de dev. Abrir com a definição dos dois limites na primeira frase.
- hook: Você mandou uma pergunta de uma linha e o /usage acusou 40% da sessão. Não foi a pergunta. Foi tudo que veio junto com ela.
- bullets:
  - O Claude Pro tem limite de uso? Os dois limites que existem (contexto vs cota de 5 horas e semanal) e por que ninguém publica um número fixo
  - Por que o Claude Code está consumindo muitos tokens: o que entra na conta a cada mensagem e por que a sessão longa custa mais que a curta
  - Como saber quantos tokens você gastou: /usage, /cost e o painel, com o que cada número significa
  - Qual modelo do Claude gasta menos tokens: Haiku, Sonnet e Opus na mesma tarefa, com a conta
  - Como configurar o Claude para gastar menos tokens: cache de prefixo, CLAUDE.md enxuto, /clear na hora certa, menos MCP, subagentes e Auto Mode
  - "Você usou 90% do seu limite de sessão": o que fazer na hora sem perder o trabalho, e Pro, Max 5x ou Max 20x: quando subir de plano e quando o problema é o fluxo
- perguntas_paa:
  - O Claude Pro tem limite de uso?
  - Como saber a quantidade de tokens do Claude?
  - Como funciona o gasto de tokens no Claude?
  - Por que o Claude Code está consumindo muitos tokens?
  - Qual modelo do Claude gasta menos tokens?
- keyword_principal: quantos tokens tem o claude pro
- keywords_secundarias: como economizar tokens no claude; como gastar menos tokens no claude; consumo de tokens claude; limite de uso claude pro; claude code gastando muito token; quantos tokens tem o claude max; claude pro vale a pena
- tags: claude, claude-code, tokens, custos, cache, engenharia-de-contexto, produtividade
- dificuldade: easy
- volume: "quantos tokens tem o claude pro" ~590/mo (1.600 nos últimos 3 meses), rd 2, subindo desde fev; cluster "economizar/gastar menos tokens no claude" no GSC: ~700 impressões em 90d, pos 7 a 10, 0 cliques, blog em pos 6 orgânica com o post genérico; "claude tokens" ~390/mo (KD 20, rd 110, transacional: não mirar); "claude pro vale a pena" ~320/mo, rd 0.3

## Claude ou ChatGPT: qual usar em 2026 (e qual é melhor para programar)
- publicar_em: 2026-09-16T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A dor "qual escolher" no nível mais baixo de consciência: a pessoa ainda compara os dois chats, não sabe que existe Claude Code nem Codex. O post responde por tarefa (escrever, analisar documento, programar, agente), mostra onde cada um ganha com critério e número, e leva o dev para o próximo passo (o comparativo Claude Code vs Codex do blog). Validado pela planejar-pauta em 13/09: cluster de ~5.000 buscas/mês somando as grafias (ou, vs, versus, x, é melhor que), todas subindo em 2026 e estáveis desde março; 0 a 6 domínios de referência no top 10; SERP inteira generalista (Reddit, Alura pos 2, Exame, Conta Azul, Serasa, Pluga), nenhuma com benchmark ou ângulo de dev, e "claude ou chatgpt para programação" aparece nas pesquisas relacionadas. Sem post no blog e sem impressão no GSC ainda. Cuidado: "claude é gratuito" (880/mo) tem 620 domínios de referência no top 10 e fica só como H2, não como alvo.
- hook: Todo mundo responde "depende". Aqui tem a tabela do depende: tarefa por tarefa, com número, e o que muda quando você é dev.
- bullets:
  - Claude ou ChatGPT: a resposta curta por tarefa (texto, documento longo, código, imagem, voz, pesquisa, agente)
  - Qual é melhor para programar: o que os benchmarks dizem e o que muda quando sai do chat e vai pro terminal (link pro Claude Code vs Codex)
  - Devo assinar Claude ou ChatGPT? Pro vs Plus: o que cada assinatura libera de verdade e os limites que ninguém conta
  - Claude é gratuito? O que dá pra usar sem pagar em cada um, e onde o Claude é mais restritivo
  - Qual a diferença do Claude para o ChatGPT no dia a dia: instrução literal, contexto longo, ecossistema e voz
  - Claude ou ChatGPT ou Gemini: quando o terceiro entra na conta, e o teste de 5 minutos pra decidir com a sua tarefa
- perguntas_paa:
  - Qual IA é melhor que o ChatGPT?
  - Qual IA é melhor que o Claude?
  - Devo assinar Claude ou ChatGPT?
  - Qual é a melhor IA atualmente?
  - A IA Claude é boa?
- keyword_principal: claude ou chatgpt
- keywords_secundarias: claude vs chatgpt; claude é melhor que chatgpt; qual é melhor claude ou chatgpt; claude ou chatgpt para programação; claude pro ou chatgpt plus; qual a diferença do claude para o chatgpt; claude ou gemini
- tags: claude, chatgpt, openai, anthropic, ferramentas-de-ia, modelos-de-ia
- dificuldade: easy
- volume: "claude ou chatgpt" ~1.000/mo (1.900 a 2.400 recentes), rd 6, +805%/ano; "claude versus chatgpt" ~720/mo, rd 0; "claude vs chatgpt" ~720/mo, rd 4; "claude é melhor que chatgpt" ~590/mo (1.300 recentes), rd 5; "claude x chatgpt" ~390/mo, rd 45; "claude ou gemini" ~260/mo, rd 5, +1.200%/ano; cluster ~5.000/mo, tudo informacional

## Qual a melhor IA gratuita para programar em 2026 (o que é de graça de verdade)
- publicar_em: 2026-09-17T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A dor "não quero ou não posso pagar" de quem quer programar com IA. A SERP de "qual a melhor ia gratuita" é generalista (TechTudo, Exame, DataCamp), mas o Reddit r/brdev está em pos 2, prova de que a busca vem de dev. O post responde o que cada tier grátis entrega hoje (ChatGPT, Claude, Gemini, Copilot, Gemini CLI, Codex no Plus, Claude Code via OpenRouter, modelos locais com Ollama), onde o "grátis" acaba (limites, janela, modelo rebaixado) e qual combinação zero-custo aguenta o dia de trabalho. Demanda plana há 12 meses com KD 1. Sem post no blog com a palavra "gratuito".
- hook: "Grátis" em IA quer dizer três coisas diferentes: sem cartão, sem limite ou sem modelo bom. Nunca as três ao mesmo tempo. A tabela de qual é qual.
- bullets:
  - Qual IA é realmente gratuita: o que cada plano free libera (modelo, mensagens, contexto) em setembro de 2026
  - Qual IA gratuita oferece uso ilimitado: as que não têm teto e o preço escondido disso (modelo fraco, dados de treino)
  - Melhor IA gratuita para programar: chat, extensão de IDE e agente de terminal, o que dá pra ter sem pagar em cada camada
  - Como usar o Claude Code de graça (OpenRouter, modelos alternativos) e o que você perde no caminho
  - Modelo local é a IA grátis de verdade: quando o Ollama no seu notebook resolve e quando não resolve
  - A combinação zero-custo que aguenta um dia de trabalho de dev, e o primeiro real que vale a pena gastar
- keyword_principal: qual a melhor ia gratuita
- keywords_secundarias: melhor ia gratuita para programar; ia para programar gratuito; agente de ia gratuito; ia gratuita sem limite; como usar o claude code gratuito; qual ia é realmente gratuita
- tags: ferramentas-de-ia, custos, claude-code, ollama, open-source, produtividade
- dificuldade: medium
- volume: "qual a melhor ia gratuita" ~720/mo, KD 1, rd 54, plana há 12 meses; "agente de ia gratuito" ~390/mo, KD 1; "como usar o chatgpt gratuitamente" ~1.000/mo (em queda, -38%/ano, não mirar)

## Qual a melhor IA em 2026? Como escolher por tarefa sem cair em hype
- publicar_em: 2026-09-18T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: O hub do cluster. A query mais genérica e de menor consciência possível ("qual a melhor ia", 2.900/mês e dobrando no ano) respondida com o método da casa: não existe melhor, existe melhor pra tarefa, e aqui está o critério, a tabela por tarefa e o teste de 5 minutos pra decidir. Encaminha para os spokes: Claude ou ChatGPT, melhor IA gratuita, melhor IA para programar, tokens. Cuidado com canibalização: este post NÃO mira "melhor ia para programar" (fica com o post existente, ver refreshes) nem "claude ou chatgpt" (post 2). Só 13 domínios de referência no top 10 e a SERP é de portal generalista.
- hook: "Qual a melhor IA" é a pergunta errada, e todo mundo sabe. O que ninguém entrega é o jeito de fazer a pergunta certa em 5 minutos.
- bullets:
  - Qual a melhor IA: por que a pergunta não tem resposta única e o critério que substitui ela (tarefa, contexto, custo, controle)
  - A tabela por tarefa: texto, código, documento longo, pesquisa, imagem, agente, com o modelo que lidera cada uma hoje
  - Qual IA é melhor que o ChatGPT: onde Claude e Gemini ganham de fato, com número, não com opinião
  - ChatGPT ou Gemini: o duelo que mais gente busca e o critério de desempate
  - Qual a IA mais usada e por que isso não deveria decidir a sua escolha
  - O teste de 5 minutos: como rodar a mesma tarefa em três IAs e decidir com evidência
- keyword_principal: qual a melhor ia
- keywords_secundarias: ia melhor que chatgpt; qual ia é melhor chatgpt ou gemini; chatgpt ou gemini; qual ia usar; qual a ia mais usada
- tags: ferramentas-de-ia, modelos-de-ia, benchmark, produtividade
- dificuldade: medium
- volume: "qual a melhor ia" ~2.900/mo (3.600 a 4.400 recentes), rd 13, +125%/ano; "ia melhor que chatgpt" ~880/mo (em queda, -41%); "qual ia é melhor chatgpt ou gemini" ~480/mo, KD 3, +324%/ano

## Qual modelo do Claude usar: Haiku, Sonnet, Opus ou Fable (e qual gasta menos token)
- publicar_em: 2026-09-19T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A dor de quem já está dentro do Claude e não sabe qual modelo escolher no seletor: "deixo no Opus e o limite acaba em dois prompts" é a frase mais votada do Reddit que lidera a SERP. O post dá o critério por tarefa (planejar, codar, refatorar, revisar, tarefa em lote), a conta de custo e de consumo de cota de cada modelo, e o padrão Opus pra planejar e Sonnet pra executar. Liga direto com o post 1 (é a resposta à pergunta do PAA "qual modelo do Claude gasta menos tokens?"). Validado pela planejar-pauta em 13/09: cluster de ~900 buscas/mês entre "opus vs sonnet", "sonnet vs opus", "sonnet ou opus", "haiku vs sonnet", todas subindo (190% a 1.200% no ano) com 0 a 2 domínios de referência no top 10. Sem post no blog (só a notícia do Sonnet 5). SERP: Reddit em pos 1, 4 e 7, o resto é inglês (Cosmic JS, Claude Academy, Towards AI, Verdent); AI Overview cita Emergent e Claude Academy via Google Tradutor. Nenhum conteúdo pt-BR de dev. Abrir com o critério de escolha na primeira frase pra ser citado.
- hook: O seletor de modelo do Claude Code vem no Opus por padrão. É por isso que seu limite acaba na segunda tarefa do dia.
- bullets:
  - Qual é melhor, Claude Opus ou Sonnet: a resposta em uma tabela, por tarefa, com o benchmark que importa e o que não importa
  - Quando usar o Sonnet e quando usar o Opus: o padrão "Opus planeja, Sonnet executa" na prática do Claude Code
  - Qual modelo do Claude gasta menos tokens e cota: Haiku, Sonnet, Opus e Fable na mesma tarefa, com a conta de custo e de limite de sessão
  - Qual é mais caro, Sonnet ou Opus: preço por milhão, preço por tarefa e por que os dois números discordam
  - Claude Sonnet ou Opus para programação: onde o Sonnet empata, onde o Opus abre vantagem e quando o Fable é a única saída
  - Como trocar de modelo no meio da sessão (/model) sem perder contexto, e o CLAUDE.md que fixa o modelo certo por tipo de tarefa
- perguntas_paa:
  - Qual é melhor, Claude Opus ou Claude Sonnet?
  - Quando usar o Sonnet e quando usar o Opus?
  - Qual o melhor modelo do Claude?
  - Qual é mais caro, Sonnet ou Opus?
  - Qual modelo do Claude gasta menos tokens?
- keyword_principal: claude opus vs sonnet
- keywords_secundarias: claude sonnet vs opus; claude sonnet ou opus; claude haiku vs sonnet; claude opus vs sonnet vs haiku; claude sonnet ou opus para programação; qual o melhor modelo do claude
- tags: claude, anthropic, claude-code, modelos-de-ia, tokens, custos, benchmark
- dificuldade: easy
- volume: "claude opus vs sonnet" ~320/mo, rd 1, +191%/ano; "claude sonnet vs opus" ~320/mo, rd 2, +333%/ano; "claude sonnet ou opus" ~140/mo, rd 0, +1.200%/ano; "claude haiku vs sonnet" ~140/mo, rd 0, +1.000%/ano; cluster ~900/mo, tudo informacional

---

## Refreshes de posts de DOR que já existem e não estão rankeando

O dedup mostrou que o blog já tem a maior parte das dores cobertas, mas nenhuma aparece no GSC. O problema é título/intenção e canibalização, não falta de conteúdo. Em ordem de retorno:

| post existente | dor / keyword | vol BR | o que está errado | ação |
|---|---|---|---|---|
| `noticias/melhor-ia-para-programar-2026-claude-code-vs-codex` | melhor ia para programar + qual a melhor ia para programação | 2.900 + 1.000 + 720/mo, tudo plano | CORRIGIDO 14/09: a varredura de canibalização mostrou que o post NUNCA rankeou pra essa keyword (9 impressões); os 52 cliques vêm de "codex ou claude code". Não retitular. | manter como está (duelo Claude Code vs Codex) e escrever um HUB novo "Melhor IA para programar em 2026" com 6 a 7 ferramentas, linkando o duelo como spoke; remover o duplicado `melhor-ia-para-programacao-2026` com 301 |
| `noticias/o-que-e-um-agente-de-ia` | o que é um agente de ia | 1.300/mo (1.600 recentes), KD 3, +82% | post de junho, não aparece no GSC | refresh + definição fechada na 1ª frase (AI Overview) + reindexar |
| `tutoriais/como-criar-um-agente-de-ia-do-zero` | como criar um agente de ia | 1.300/mo, +48%, SERP com só 20 resultados | só rankeia pra "para whatsapp" em pos 25 | retitular casando a query, adicionar H2 "no ChatGPT / no Gemini / no Claude" (320 + 170 + 110/mo) e "como fazer um agente de ia" (+191%) |
| `noticias/engenharia-de-prompt-guia-honesto` | como criar um prompt + o que é engenharia de prompt | 320 (+88%) + 210 (+52%) + 480 (KD 3) | título não casa "como criar"; o post "engenharia de prompt acabou" (31/08) disputa a mesma keyword | retitular pra "Como criar um prompt que funciona: engenharia de prompt sem fórmula mágica"; o post de 31/08 vira opinião e aponta pra este |
| `noticias/por-que-a-ia-alucina...` + `noticias/alucinacao-de-ia-grounding` | alucinação ia / por que a ia alucina | 260 + 210 + 90/mo | dois posts pra mesma dor = canibalização | consolidar: o de 01/09 vira canonical, o de junho redireciona ou vira spoke de e-commerce |
| `noticias/o-que-e-um-llm-explicacao-para-quem-vai-construir` | llm o que é | 9.900/mo, KD 23, +22% | publicado 31/08, título começa com "O que é um LLM" (ok) | monitorar 30 dias; se não pingar, encurtar title e reforçar links internos |
| `noticias/o-que-e-mcp` | o que é mcp | 2.900/mo (4.400 recentes), rd 1.6 | pos 38 a 61 | refresh completo com H2 por variação |
| `noticias/vibe-coding-o-que-e-onde-quebra` | vibe coding o que é | 4.400/mo, rd 2.7 | título não abre com a definição | retitular e abrir com "Vibe coding é..." |
| `tutoriais/como-economizar-tokens-claude-code-codex-cursor` | como economizar tokens (hub) | vencedor atual | vai receber o spoke do Claude (post 1) | adicionar bloco "por ferramenta" com link pro post 1; manter como hub |

## Adjacente (fora da pauta, decidir depois)
- "qual a melhor ia para estudar" (2.400/mo, +177%, rd 34): mesma dor de escolha, mas público de concurso/faculdade. Só entra se houver ângulo "para estudar programação" (50/mo hoje).
- "prompt o que é" (8.100/mo, KD 4): gigante e genérica; entraria como definição curta dentro do refresh de engenharia de prompt, não como post.

## Descartados no gate
- Toda a v1 (o que é Codex, instalar Codex CLI, instalar Claude Code, preço do Claude): pauta de produto, consciência alta, vira news-jacking disfarçado.
- "chatgpt lento", "chatgpt tem limite de uso", "chatgpt sem limite": dor real mas de usuário de chat, não de dev, e em queda (-46%/ano).
- "ia vai substituir programadores", "como revisar código gerado por ia", "ia erra muito": sem registro de volume no DataForSEO; sem demanda medida não entra.
- "tokens o que é" (2.900/mo): ambíguo (cripto, banco).
