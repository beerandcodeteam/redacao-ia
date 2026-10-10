Hoje, 3 de setembro, o Claude ficou fora do ar das 13:26 às 16:23 UTC. Mythos, Fable, Opus, tudo junto, em claude.ai, API, Claude Code e Cowork ([status oficial](https://status.claude.com/incidents/461yvfrzpwtt)). O Codex caiu no mesmo horário ([HN](https://news.ycombinator.com/item?id=49549676)). Se você usa agente de código pra trabalhar, sabe exatamente o que aconteceu com a sua tarde.

Agora inverte a câmera. Em Londres, em Dublin, em San Francisco, tem engenheiro da Anthropic com o mesmo terminal travado que o seu. Só que o incidente é deles. O pager tocou pra eles.

Em 24 de agosto alguém fez a pergunta óbvia no Hacker News: *"When Claude is down, do they have a backup Claude to investigate the root cause?"* ([HN](https://news.ycombinator.com/item?id=49415517)). Zero respostas.

Este post é a resposta que ninguém deu. Cruzei o que a Anthropic publicou, o que engenheiros nomeados disseram em palestra e podcast, o código do Claude Code que vazou em março, o status page inteiro de 2025 e 2026 e as vagas abertas do time de confiabilidade. Três perguntas: eles têm servidor privado? Trocam pra outro modelo? Ou voltam a trabalhar na mão?

## TL;DR

- **Servidor privado:** sem evidência. O que existe é staging interno vazado no código e um pool isolado do governo americano que fica de pé quando o resto cai. A Anthropic nunca explicou nenhum dos dois.
- **Outro modelo:** não. Todo fallback documentado é Claude-para-Claude. O "outro modelo" dos funcionários é um Claude que ainda não saiu.
- **Moda antiga:** parcialmente sim. Existe um time humano de confiabilidade contratando em três países, e o engenheiro mais público dele admite que ainda lê log na mão. E diz estar preocupado com quem não sabe mais fazer isso.
- **Resposta oficial:** silêncio. Nenhum blog, postmortem ou página de suporte da Anthropic diz o que os funcionários fazem numa queda.
- **Frequência:** 358 entradas de incidente no status oficial entre 1 de janeiro e 3 de setembro de 2026, contra 335 em todo 2025.

## Claude fora do ar: com que frequência isso acontece

Antes das três perguntas, o tamanho do problema. Contei o [histórico do status page](https://status.claude.com/history) até hoje:

| período | entradas de incidente | críticas |
|---|---|---|
| 2024 inteiro | 191 | 5 |
| 2025 inteiro | 335 | 22 |
| 2026 (1/jan a 3/set) | 358 | 17 |

Na janela comparável, janeiro a agosto, foram 234 entradas em 2025 e 352 em 2026. Metade a mais. O crescimento é quase todo em incidente "minor" (107 pra 221); os críticos ficaram praticamente iguais. Uptime de 90 dias hoje: 99,41% no claude.ai, 99,45% no Claude Code ([status.claude.com](https://status.claude.com/)).

Cuidado com a leitura. Entrada de incidente não é queda. Vinte e duas são informativas, uma das "críticas" é a suspensão regulatória do Fable 5 e do Mythos 5 em junho, e muita coisa é degradação de dez minutos num modelo só. Mas a tendência é real, e a Anthropic não nega.

A explicação oficial, em nível de empresa, é uma só: demanda. Dario Amodei, em maio: *"We tried to plan very well for a world of 10x growth per year. And yet we saw 80x. And so that is the reason we have had difficulties with compute"* ([CNBC](https://www.cnbc.com/2026/05/06/anthropic-ceo-dario-amodei-says-company-crew-80-fold-in-first-quarter.html)). À Fortune, um mês antes: *"Demand for Claude has grown at an unprecedented rate, and our infrastructure has been stretched to meet it, particularly at peak hours"* ([Fortune](https://fortune.com/2026/04/24/anthropic-engineering-missteps-claude-code-performance-decline-user-backlash/)).

E tem a versão do chão de fábrica. Em março, num thread do HN sobre o Claude perder os 99% de uptime no trimestre, um usuário chamado "palcu" se apresentou como *"Alex from the reliability engineering team at Anthropic"* e escreveu: *"we're dealing with very compressed timelines and while most of the time we're able to fix the issues beforehand, sometimes we have to do them in production. Sorry for that."* ([HN](https://news.ycombinator.com/item?id=47543189)).

Guarda esse nome. Alex Palcuie é o personagem central desta história.

## Uma empresa que não escreve mais código à mão

Pra entender por que a pergunta importa, precisa entender o quanto a Anthropic depende do próprio produto.

Boris Cherny, criador do Claude Code, em junho: *"I haven't written a line of code by hand in, I think, eight months now"* ([Fortune](https://fortune.com/2026/06/11/anthropic-claude-boris-cherny-doesnt-write-code-by-hand-anymore/)). Não é só ele. O ensaio "When AI builds itself", do Anthropic Institute, afirma: *"As of May 2026, more than 80% of the code we merge into Anthropic's codebase was authored by Claude"*, contra dígitos baixos antes de fevereiro de 2025 ([Anthropic Institute](https://www.anthropic.com/institute/recursive-self-improvement)).

O [estudo interno de dezembro](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic), com 132 engenheiros e pesquisadores, mediu 59% do trabalho feito com Claude e 50% de ganho de produtividade auto-relatado. E registrou o medo: *"When producing output is so easy and fast, it gets harder and harder to actually take the time to learn something."* As palavras outage, downtime e unavailable não aparecem no texto.

Tem mais. O time de engenharia publicou em maio que *"Twelve months ago, we'd have rejected out of hand the idea of granting Claude access sufficient to take down an internal Anthropic service. Today that level of access is routine"* ([How we contain Claude](https://www.anthropic.com/engineering/how-we-contain-claude)). E desde agosto o primeiro relatório de situação de todo incidente de CI da empresa é escrito pelo Claude Tag, o Claude do Slack, com mediana de 14 minutos ([claude.com](https://claude.com/blog/ai-ci-cd-on-call)).

Ou seja: a ferramenta de resposta a incidente da Anthropic é o Claude. Quando o Claude é o que cai, essa camada cai junto. É exatamente esse cenário que a gente treina toda semana no [Clã Beer and Code](https://beerandcode.com.br?utm_source=blog&utm_medium=post&utm_campaign=claude-fora-do-ar-quem-conserta-o-claude&utm_content=g-n1): é pago, é assinatura, e a régua lá é o que você consegue construir e sustentar quando a ferramenta trava, não o que você consegue pedir pra ela.

Com esse pano de fundo, as três perguntas.

## Pergunta 1: eles têm servidores privados?

**Resposta curta: sem evidência de que exista um Claude reserva pra funcionário.** O que existe é mais interessante que isso.

**Existe staging, e ele vazou.** Em 31 de março de 2026 o pacote npm do Claude Code saiu com source map, e o código-fonte inteiro ficou público por algumas horas ([análise de Alex Kim](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/); [espelho](https://github.com/davccavalcante/claude-code-leaked)). Dentro dele, um caminho gated por `process.env.USER_TYPE === 'ant'`, constante de build presente só na versão interna, em que a função que valida a URL da API aceita `api-staging.anthropic.com` além de `api.anthropic.com`. Tem config de OAuth apontando pra `platform.staging.ant.dev`. É ambiente de teste de funcionário. Nada no código descreve isso como fallback de queda: busca por *fallback*, *outage* ou *failover* perto desses hosts retorna zero. E os hosts de staging resolvem pro mesmo IP público da API.

**Existe um pool isolado que sobrevive às quedas. Não é dos funcionários. É do governo.** "Claude for Government" é uma componente separada no [status page](https://status.claude.com/api/v2/components.json), criada em fevereiro. Nas quedas de 23 de junho, 29 e 30 de julho e hoje, ela não aparece como afetada. Marca 100% de uptime em 90 dias enquanto o resto fica em 99,4% ([TechTimes](https://www.techtimes.com/articles/325344/20260824/commercial-claude-has-gone-down-28-times-30-days-its-government-tier-has-never-gone-down-once.htm)). A imprensa atribui isso a rodar isolado via Palantir com FedRAMP High. A Anthropic nunca descreveu a arquitetura. E o "100%" é janela rolante: entre março e maio essa componente foi marcada em pelo menos 13 incidentes.

**O tráfego interno parece passar pelo mesmo stack, com flag diferente.** O [postmortem de 23 de abril](https://www.anthropic.com/engineering/april-23-postmortem), sobre a degradação de qualidade do Claude Code, diz que *"neither our internal usage nor evals initially reproduced the issues"*, que *"an internal-only server-side experiment related to message queuing"* atrapalhou a reprodução, e promete que *"a larger share of internal staff use the exact public build of Claude Code (as opposed to the version we use to test new features)"*. Um experimento server-side só pra funcionário é forte indício de mesmo serving com comportamento diferente, não de cluster à parte. Isso é leitura minha; o postmortem não usa a palavra "mesmo stack".

**O CFO fala em compute fungível, não em reserva.** Krishna Rao, no Invest Like the Best em maio: a Anthropic usa Trainium, TPU e GPU *"fungibly"* pra treinar, pra uso interno e pra cliente, *"we meet a lot about compute allocation"*, e existe *"a level of compute for model development that we will not go below"* ([YouTube](https://www.youtube.com/watch?v=wEEZPpx8qow)). Piso pra pesquisa. Nada sobre serving de emergência.

O que dá pra afirmar: se a Anthropic consegue manter o governo isolado, tecnicamente poderia fazer o mesmo pra funcionário. Não há um único indício de que faça.

## Pergunta 2: usam outro modelo?

**Resposta curta: nenhuma evidência de GPT, Gemini ou qualquer coisa que não seja Claude.**

**Todo fallback documentado é Claude-para-Claude.** A flag `--fallback-model` do Claude Code troca pra outro modelo Claude quando o primário está *"overloaded, unavailable, or returns another non-retryable server error"* ([CLI reference](https://code.claude.com/docs/en/cli-reference)). A doc de gateway é explícita: a Anthropic *"doesn't support routing Claude Code to non-Claude models through any gateway"* ([LLM gateway](https://code.claude.com/docs/en/llm-gateway)). E o modo watchdog público, `CLAUDE_CODE_RETRY_WATCHDOG`, espera indefinidamente por 429 e 529 em vez de trocar de fornecedor ([env vars](https://code.claude.com/docs/en/env-vars.md)). No código vazado ele aparecia antes como `CLAUDE_CODE_UNATTENDED_RETRY`, só pra "ants". A estratégia interna pra sobrecarga é esperar passar.

**O "outro modelo" interno é um Claude que você ainda não viu.** O vazamento mostra aliases só pra funcionário, tipo `capybara-fast`, resolvidos por uma flag chamada `tengu_ant_model_override`, e um "Undercover mode" que proíbe citar codinomes e versões não lançadas em commit público. Oficialmente, a Anthropic confirma que em março de 2026, 130 pesquisadores já usavam o Mythos Preview internamente, um mês antes do anúncio, e a mediana estimava uns 4x de output ([Anthropic Institute](https://www.anthropic.com/institute/recursive-self-improvement)).

**Perguntado sobre o Codex, o chefe do Claude Code disse que não usa.** Boris Cherny no Lenny's Podcast, em fevereiro: *"I actually haven't really used it. But I think I did use it maybe when it came out. It looked a lot like Claude Code to me, so that was kind of flattering. [...] We don't really try the other products"* ([YouTube](https://www.youtube.com/watch?v=We7BZVKbCVw)). No mesmo episódio ele conta que até maio de 2025 usava Cursor pra maior parte do código, e que só chegou a 100% Claude Code em novembro.

**A Anthropic acessa concorrente, mas pra avaliar.** Quando cortou o acesso da OpenAI ao Claude, em agosto de 2025, disse que manteria acesso *"for the purposes of benchmarking and safety evaluations as is standard practice across the industry"* ([TechCrunch](https://techcrunch.com/2025/08/02/anthropic-cuts-off-openais-access-to-its-claude-models/)). Trabalho do dia a dia com GPT? Nenhuma fonte.

Tem um caso-limite curioso. Entre 13 de junho e 1 de julho o governo americano suspendeu o acesso ao Fable 5 e ao Mythos 5, e o comunicado da Anthropic inclui *"foreign national Anthropic employees"* na restrição ([Anthropic](https://www.anthropic.com/news/fable-mythos-access)). O que funcionário americano usou nessas duas semanas? A leitura mais provável é Opus 4.8 e Sonnet. Ninguém disse.

## Pergunta 3: trabalham à moda antiga?

**Resposta curta: em parte sim. E a Anthropic tem medo de perder essa parte.**

**Existe um time humano cuja função oficial é responder a incidente do Claude.** Chama AIRE, AI Reliability Engineering. As vagas abertas em [Londres](https://job-boards.greenhouse.io/anthropic/jobs/5101173008), [Dublin](https://job-boards.greenhouse.io/anthropic/jobs/5101169008) e [EUA](https://job-boards.greenhouse.io/anthropic/jobs/5113224008) dizem: *"Lead incident response for critical AI services"*. E o slogan: *"Claude has your back. AIRE has Claude's."*

Alex Palcuie, aquele do HN, é Member of Technical Staff no AIRE. A bio pessoal dele é a frase que resume este post inteiro: *"I keep Claude reliable on the AI Reliability Engineering (AIRE) team, which means the unenviable job of fixing Claude without Claude when it goes down"* ([palcu.net](https://palcu.net/)). Piada pessoal, não missão do time. Mas é a coisa mais próxima de uma resposta oficial que existe.

Em março ele deu uma palestra no QCon London chamada "Can Claude Fix Itself? Using LLMs for Incident Response". A [transcrição saiu na InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/) em 26 de agosto, e é a melhor fonte primária sobre o assunto. Ele começa se colocando na posição ideal pra responder:

> "If anyone has this working, it's the company that makes the model. We have unlimited tokens. Researchers sit a desk away from me. I get involved in training the models. Surely, if it's anyone, it's us. Let me get the answer out of the way. It's a no."

E dá a prova por contradição:

> "If an LLM could carry a pager, we might not need to hire so much. The fact that my team exists, the fact that we're hiring for many positions, in London, in Dublin, and the U.S., and we have staff positions, this should show to you that, no, it doesn't work."

Isso não quer dizer que ele responde a incidente sem o modelo. Pelo contrário: *"since about January this year, I've started doing something that feels slightly transgressive to admit, which is, I start reaching out for Claude before I reach out to my monitoring dashboards."* Ele conta o incidente da véspera de Ano Novo, 500s no Opus 4.5 com equipe reduzida: abriu o Claude Code com um SKILL.md próprio, o modelo escreveu SQL contra os logs, achou uma exceção no caminho de imagens disparada por requisições com exatamente 22 imagens, cruzou com 200 contas mandando o mesmo payload e 4 mil cadastros com o mesmo template de e-mail, e concluiu: *"stop looking at the 500s, this is fraud."*

Quando o Claude está de pé, o Claude é a primeira ferramenta. A pergunta é o que sobra quando não está. E aqui vem a parte que vale o post:

> "While I was going through the logs manually, because this is something that I still do, I don't know why, one of my newer teammates, not even on-call trained, two to three months in the team, just pointed Claude Code at the logs. It instantly found the root cause."

Ele ainda lê log na mão. Não sabe explicar por quê. O colega novo não lê. E na seção que ele chama de "The Learning Problem":

> "When the big thing happens that the model can't fix, you might be miscalibrated on how to respond to such an incident. I'm genuinely worried about this."

É isso. A resposta pra "trabalham à moda antiga?" é: os que ainda sabem, sim. E o time que mantém o Claude de pé tem consciência de que essa habilidade está evaporando por dentro da própria empresa.

Um detalhe pra não distorcer: a maioria das quedas é parcial. Em 11 de março caiu o claude.ai e o login, mas a API ficou de pé ([status](https://status.claude.com/incidents/jm3b4jjy2jrt)). Em 26 e 27 de março caíram só Opus 4.6 e Sonnet 4.6 ([status](https://status.claude.com/incidents/b9802k1zb5l2)). Na maior parte dos incidentes, algum Claude continua alcançável por outro modelo ou outra superfície. A piada do Palcuie descreve o caso extremo. Hoje foi um desses.

## O que a Anthropic não diz

Tudo acima é soma de evidência indireta. Pra manter a honestidade, o que **não** existe:

- Nenhuma declaração oficial sobre o que funcionários fazem durante uma queda. Li o estudo interno e os dois postmortems de engenharia de ponta a ponta. Zero menções.
- Nenhum funcionário nomeado dizendo em público que perdeu acesso, trocou de modelo ou trabalhou na mão numa queda específica.
- Nenhum postmortem de disponibilidade em 2026. Das 358 entradas do status page, 8 têm um parágrafo de causa, todas entre janeiro e março. A queda de 29 e 30 de julho foi explicada só num tweet do @ClaudeDevs, sobre falhas de rede.
- Nenhum SLA no tier padrão. A doc fala em *"best-effort availability"*; o Priority Tier mirava 99,5% e não é mais vendido ([service tiers](https://platform.claude.com/docs/en/api/service-tiers)). Os termos comerciais entregam o serviço *"AS IS"* e *"AS AVAILABLE"* ([Commercial Terms](https://www.anthropic.com/legal/commercial-terms)).

Se alguém da Anthropic quiser responder ao thread do HN, o post é atualizado.

## O que isso muda pra você

Três coisas práticas.

**Domínio de falha é real, aproveita.** No bug de roteamento de 2025, o pico foi 16% das requisições de Sonnet 4 erradas na API própria, contra 0,18% no Bedrock e menos de 0,0004% no Vertex ([postmortem](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues)). São três caminhos de serving e três famílias de hardware. Se você roda agente em produção, o [Bedrock](https://blog.beerandcode.com.br/tutoriais/aws-bedrock-o-que-e-claude-producao-governanca) como segunda rota é a alavanca que a própria Anthropic não usa em público, mas que você pode usar. O [playbook de retry, circuit breaker e cascata](https://blog.beerandcode.com.br/noticias/claude-opus-5-fora-do-ar) já está escrito.

**Fallback pra outro fornecedor é decisão sua, não da ferramenta.** O Claude Code nunca vai te mandar pro GPT. Se o seu produto precisa disso, a camada é o seu código: um roteador que decide por 529 e latência, com a mesma disciplina de contrato que a gente cobra de [structured output](https://blog.beerandcode.com.br/tutoriais/json-que-nao-quebra-structured-output-llm). E lembra do dia de hoje: Claude e Codex caíram juntos. Multi-vendor não é garantia, é redução de probabilidade.

**A lição do Palcuie serve pra você.** Ele lê log na mão "e não sabe por quê". Sabe sim. É a única forma de continuar calibrado pro dia em que o modelo não resolve. Se você passou a semana sem entender um stack trace porque o agente resolveu antes, você está no mesmo lugar do colega novo dele. Reserva um incidente por mês pra resolver sem IA. É barato, e é a diferença entre saber usar a ferramenta e depender dela.

## FAQ rápido

**O Claude caiu agora?**
Confere em [status.claude.com](https://status.claude.com/), que é o feed oficial, componente por componente. Downdetector e StatusGator agregam relato de usuário e costumam acusar antes, mas com falso positivo. Erro 529 na API significa sobrecarga, não queda total: retry com backoff resolve na maioria dos casos.

**A Anthropic tem SLA de uptime?**
Não no plano padrão. A documentação de service tiers fala em disponibilidade best-effort. O Priority Tier tinha alvo de 99,5% e foi descontinuado. Contrato enterprise pode ter termos próprios, mas nada disso é público.

**Bedrock e Vertex caem junto com a API da Anthropic?**
Não necessariamente. São deployments separados, geridos pela AWS e pelo Google, em hardware diferente. No postmortem de 2025 as taxas de erro divergiram em ordens de grandeza. Mas não é imunidade: em agosto houve relatos de instabilidade no Vertex por dois dias. Trata como segunda rota, não como garantia.

**Funcionário da Anthropic usa ChatGPT quando o Claude cai?**
Nenhuma evidência. O único depoimento direto é o do Boris Cherny dizendo que não experimenta produto concorrente. Não existe política interna publicada. É a pergunta mais fácil de fazer e a que ninguém respondeu.

## Conclusão

Servidor privado? Provavelmente não. Outro modelo? Provavelmente não. Moda antiga? Provavelmente sim, pelos que ainda lembram como.

E a resposta oficial da Anthropic pra tudo isso é silêncio. O que existe é uma bio de engenheiro com uma piada boa, uma palestra honesta, um código vazado com hosts de staging, um status page com 358 entradas e um postmortem que promete que funcionário vai usar a mesma build que você.

A parte que fica não é sobre a Anthropic. É sobre o time do Palcuie ser o espelho do seu. Eles têm token ilimitado, pesquisador na mesa ao lado e acesso ao modelo antes de todo mundo. E mesmo assim mantêm gente lendo log na mão, porque sabem que o dia em que o modelo não resolve chega.

Hoje chegou, das 13:26 às 16:23 UTC. Quantos incidentes você resolveu sem IA nos últimos três meses?
