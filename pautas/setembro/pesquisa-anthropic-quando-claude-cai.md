# Dossiê: o que a Anthropic faz quando o Claude cai?

**Para:** Lucas / Beer & Code
**Data:** 2026-09-03
**Pergunta de pesquisa:** Quando o Claude está fora do ar, o time da Anthropic (1) tem servidores privados/internos para continuar usando o modelo? (2) Troca para outro modelo? (3) Ou trabalha "à moda antiga", na mão?

**Regra de uso deste dossiê:** só entram aqui afirmações com status *confirmado* ou *parcial* (para as parciais, uso a redação corrigida e sinalizo a nuance). Afirmações refutadas aparecem apenas na subseção "Mitos" para serem desmontadas. Toda frase factual tem link inline para a fonte.

---

## 1. Resumo executivo

1. **Não existe resposta oficial.** A Anthropic nunca publicou nada — blog, help center, status page, postmortem — dizendo o que seus funcionários fazem durante uma queda do Claude. Isso foi checado por nove agentes, em inglês e português, incluindo o [estudo interno de dez/2025](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic) e os dois postmortems de engenharia ([set/2025](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues), [abr/2026](https://www.anthropic.com/engineering/april-23-postmortem)).
2. **Servidores privados: sem evidência de que existam para uso geral.** O que existe é um ambiente de *staging* interno vazado no código do Claude Code (`api-staging.anthropic.com`), que não é documentado como fallback de queda; e uma componente isolada "Claude for Government" que fica no ar quando o resto cai — mas a Anthropic nunca explicou a separação.
3. **Outro modelo: nenhuma evidência de que troquem para GPT/Gemini.** Toda a lógica de fallback pública da Anthropic é Claude-para-Claude. O "outro modelo" que os funcionários usam é um Claude *não lançado* (aliases internos como `capybara-fast`, Mythos Preview usado internamente meses antes do anúncio).
4. **À moda antiga: parcialmente sim, e a Anthropic tem medo disso.** O time de confiabilidade (AIRE) é humano, está contratando em Londres, Dublin e EUA, e um engenheiro do time admite que ainda lê logs manualmente — enquanto colegas novos apontam o Claude Code para os mesmos logs. O próprio engenheiro diz estar "genuinamente preocupado" com a atrofia da habilidade de responder sem o modelo.
5. **O mais próximo de uma resposta oficial** é a piada do engenheiro Alex Palcuie (AIRE): "fixing Claude without Claude when it goes down" — piada pessoal, não missão do time, e o mesmo engenheiro diz que "reaches for Claude before a dashboard" quando o Claude está acessível.
6. **A dependência interna é enorme:** >80% do código mergeado na Anthropic é escrito pelo Claude (maio/2026); o criador do Claude Code não edita uma linha à mão desde nov/2025; acesso suficiente para derrubar um serviço interno é "rotina".
7. **Frequência:** 358 entradas de incidente no status oficial entre 1/jan e 3/set de 2026 (17 críticas), contra 335 em todo 2025; uptime de 90 dias em ~99,4% para claude.ai e Claude Code em 3/set.
8. **Causa oficial genérica:** demanda acima da infraestrutura em horário de pico (declaração à Fortune) e crescimento de 80x anualizado no Q1 contra planejamento de 10x (Dario Amodei).
9. **A ironia central do post:** a ferramenta de resposta a incidentes da Anthropic *é* o Claude (SITREPs de CI escritos pelo Claude Tag em ~14 min). Quando é o próprio Claude que cai, essa camada cai junto.
10. **Postura honesta para o texto:** o post pode responder "provavelmente não, provavelmente não, e provavelmente sim — mas ninguém na Anthropic disse isso em público". O que dá sustentação é a soma de evidências indiretas, não uma fonte única.

---

## 2. As três perguntas

### 2.1 Eles têm servidores privados?

#### O que a evidência diz

**Existe um caminho de serving separado para funcionários, mas é staging, não fallback.** O código-fonte do Claude Code vazado em 31/03/2026 (npm `@anthropic-ai/claude-code` v2.1.88, via source map; pacote retirado depois) contém um caminho gated por `process.env.USER_TYPE === 'ant'` — uma constante de *build* presente só em builds internos, não uma variável que usuários externos possam setar — em que `isFirstPartyAnthropicBaseUrl()` aceita `api-staging.anthropic.com` além de `api.anthropic.com`, e um `STAGING_OAUTH_CONFIG` aponta para `platform.staging.ant.dev` e `claude-ai.staging.ant.dev`, ativado só com `USE_STAGING_OAUTH` ([espelho do vazamento](https://github.com/davccavalcante/claude-code-leaked); [análise de Alex Kim](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/)). Hosts internos sob `infra.ant.dev` aparecem para artefatos (Artifactory) e upload de relatórios, não para inferência. Nada no código descreve esse ambiente como fallback de queda: grep por *fallback/outage/failover* perto desses hosts retorna zero.

**Existe pool isolado que sobrevive às quedas públicas — mas é o governo, não os funcionários.** "Claude for Government" é uma componente separada em [status.claude.com](https://status.claude.com/api/v2/components.json) (criada em 17/02/2026) que não aparece nos incidentes de 23/jun, 29–30/jul e 3/set de 2026 e marca 100,0% de uptime em 90 dias contra ~99,4–99,5% de claude.ai, API, Claude Code e Cowork ([TechTimes, 24/08/2026](https://www.techtimes.com/articles/325344/20260824/commercial-claude-has-gone-down-28-times-30-days-its-government-tier-has-never-gone-down-once.htm)). Nuance: snapshots do Wayback mostram a componente em 99,93% em jun/jul e ela foi marcada como afetada em pelo menos 13 incidentes entre 27/mar e 8/mai — o "100%" é janela rolante de 90 dias, não histórico perfeito. A explicação "roda isolado via Palantir FedRAMP High" vem da imprensa ([BeInCrypto via Yahoo](https://tech.yahoo.com/ai/claude/articles/claude-outage-hits-public-users-200000867.html)), não da Anthropic; o TechTimes registra que "Anthropic has not publicly described the architectural details of this separation".

**A infraestrutura de serving é multi-cloud e multi-chip.** A Anthropic serve o Claude via API própria, Amazon Bedrock e Google Vertex AI, em AWS Trainium, GPUs NVIDIA e TPUs Google ([postmortem set/2025](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues)); desde nov/2025 também via Microsoft Foundry. No bug de roteamento de 2025, o pico foi de 16% das requisições de Sonnet 4 na API própria (pior hora, 31/ago) contra 0,18% no Bedrock e <0,0004% no Vertex — ou seja, são domínios de falha genuinamente distintos. Um funcionário da Anthropic comentou no HN, em caráter pessoal, que os deployments no Bedrock são geridos pela AWS ([HN 45281139](https://news.ycombinator.com/item?id=45281139)).

**O CFO fala em compute "fungível" e em piso para pesquisa — não em fallback.** No podcast Invest Like the Best (13/05/2026), Krishna Rao disse que a Anthropic usa Trainium, TPUs e GPUs "fungibly" para desenvolvimento de modelo, uso interno e clientes, que "we meet a lot about compute allocation", e que "there's a level of compute for model development that we will not go below" — um piso, não uma fatia maior ([transcrição, teahose](https://www.teahose.com/podcast/Invest%20like%20the%20best/Krishna%20Rao%20-%20Anthropic's%20CFO%20on%20Compute,%20Scaling%20to%20$30B%20ARR,%20and%20the%20Returns%20to%20Frontier%20Intelligence%20-%20[Invest%20Like%20the%20Best,%20EP.471]); [YouTube](https://www.youtube.com/watch?v=wEEZPpx8qow)). Ele também disse que o compute alocado a funcionários "could serve billions of dollars of revenue".

**Funcionários usam um build diferente do cliente, e um experimento server-side "internal-only" mascarou um bug.** O postmortem de 23/04/2026 diz que "neither our internal usage nor evals initially reproduced the issues", que "an internal-only server-side experiment related to message queuing" dificultou reproduzir o bug, e que a empresa vai garantir "a larger share of internal staff use the exact public build of Claude Code (as opposed to the version we use to test new features)" ([postmortem](https://www.anthropic.com/engineering/april-23-postmortem)).

#### O que é inferência

- Um "experimento server-side só para uso interno" que muda o comportamento do tráfego de funcionários é forte indício de que esse tráfego passa **pelo mesmo stack de serving** com uma flag diferente — não por um cluster à parte. O postmortem não usa as palavras "mesmo stack"; é leitura minha.
- Se a Anthropic consegue manter o Claude for Government isolado, tecnicamente *poderia* fazer o mesmo para staff. Não há nenhuma evidência de que faça.
- Especulação comunitária (HN, não Anthropic): "They probably use every ounce of compute available, all at once, because demand > supply. So, there's no fallback mechanism" ([dconsorte, 13/03/2026](https://news.ycombinator.com/item?id=47368939)) e "Demand is actually shared between users and internal. Anthropic uses their own compute for training and building" ([hmokiguess, 03/09/2026](https://news.ycombinator.com/item?id=49550274)). Ambos hedgeados ("probably"), contestados no mesmo thread, e parcialmente contraditos pela Anthropic, que diz que a diversidade de plataformas dá "greater resilience".

#### O que não se sabe

- Se o tráfego de funcionários no claude.ai/Claude Code passa pela mesma API pública dos clientes (nenhuma frase oficial diz "employees use the same production API").
- Se `api-staging.anthropic.com` fica no ar durante quedas de produção (todos os hosts de staging resolvem para o mesmo IP público de `api.anthropic.com`).
- Como a capacidade é priorizada entre API, planos consumer, Claude Code e pesquisa interna durante um incidente.

#### Mitos

- **"A Anthropic tem um Claude de backup para consertar o Claude."** Não há evidência. A pergunta literal foi feita no HN em 24/08/2026 ("When Claude is down, do they have a backup Claude to investigate the root cause?") e recebeu zero respostas ([HN 49415517](https://news.ycombinator.com/item?id=49415517)). A única versão "verdadeira" da piada foi dada por outro usuário: "Opus and Sonnet are still working fine in AWS Bedrock ... so they genuinely do have an emergency backup Claude they can use" ([HN 47228241](https://news.ycombinator.com/item?id=47228198)) — mas isso é sobre clientes usando Bedrock, não sobre a Anthropic.
- **"Pesquisa interna fica com a maior fatia do compute, na frente dos clientes."** É paráfrase do Crypto Briefing (13/07/2026) que a transcrição do podcast não sustenta; Rao falou em *piso*, não em fatia maior, e não deu proporções.

---

### 2.2 Usam outro modelo?

#### O que a evidência diz

**Todo fallback documentado é Claude-para-Claude.** A flag `--fallback-model` do Claude Code (e o setting `fallbackModel`) troca para outro modelo Claude quando o primário está "overloaded, unavailable, or returns another non-retryable server error"; erros de autenticação, cobrança, rate limit e transporte "never trigger a switch" ([CLI reference](https://code.claude.com/docs/en/cli-reference); [model config](https://code.claude.com/docs/en/model-config)). Há também um fallback de classificador de segurança (Fable 5.x → Opus 5 / Opus 4.8) e um fallback de startup em Bedrock/Vertex — todos Claude. A doc de gateways diz textualmente que a Anthropic "doesn't support routing Claude Code to non-Claude models through any gateway" ([LLM gateway docs](https://code.claude.com/docs/en/llm-gateway)).

**O "outro modelo" interno é um Claude que ainda não saiu.** O vazamento mostra aliases de modelo só para "ants" (ex.: `capybara-fast`) resolvidos via flag GrowthBook `tengu_ant_model_override`, e um "Undercover mode" que proíbe citar codinomes internos (Capybara, Tengu) e versões não lançadas (ex.: `opus-4-7`, `sonnet-4-8`) em commits públicos ([espelho do vazamento](https://github.com/davccavalcante/claude-code-leaked); [Alex Kim](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/)). Oficialmente, o ensaio "When AI builds itself" diz que numa pesquisa de março/2026 com 130 funcionários de pesquisa, a mediana estimou ~4x de output com o Mythos Preview — antes do anúncio público de 7/abr — e a Anthropic acrescenta que espera que o uplift real fosse "somewhat lower" ([Anthropic Institute](https://www.anthropic.com/institute/recursive-self-improvement)). O Mythos Preview não foi liberado ao público geral, apenas a parceiros do Project Glasswing ([Anthropic](https://www.anthropic.com/research/mythos-preview)).

**A Anthropic acessa modelos concorrentes — para avaliação, não para trabalho.** Quando cortou o acesso da OpenAI ao Claude (jul/ago 2025), disse que manteria acesso "for the purposes of benchmarking and safety evaluations as is standard practice across the industry"; a OpenAI respondeu que "our API remains available to them" ([TechCrunch](https://techcrunch.com/2025/08/02/anthropic-cuts-off-openais-access-to-its-claude-models/)). O exercício conjunto de alinhamento (ago/2025) confirma que a Anthropic avaliou GPT-4o, GPT-4.1, o3 e o4-mini "over a public developer API" ([Anthropic Alignment](https://alignment.anthropic.com/2025/openai-findings/)). Os termos comerciais da Anthropic proíbem clientes de usar o Claude "to build a competing product or service" ([Commercial Terms, D.4](https://www.anthropic.com/legal/commercial-terms)).

**Perguntado diretamente sobre o Codex, o chefe do Claude Code disse que não usa.** No Lenny's Podcast (19/02/2026), Boris Cherny: "Yeah, I actually haven't really used it. But I think I did use it maybe when it came out. It looked a lot like Claude Code to me, so that was kind of flattering. [...] we don't spend a lot of time looking at competing products. We don't really try the other products" ([YouTube, ~71:15](https://www.youtube.com/watch?v=We7BZVKbCVw)). No mesmo episódio ele conta que usava Cursor para a maior parte do código até meados de 2025 ("even in May, it was writing maybe 30%. I was still using, you know, Cursor for most of my code. And it only crossed 100% in November") e que saiu para a Cursor em jul/2025 e voltou em duas semanas porque "what I really missed about Anthropic was the mission" ([mesmo episódio](https://www.youtube.com/watch?v=We7BZVKbCVw); [The Verge, 16/07/2025](https://www.theverge.com/ai-artificial-intelligence/708521/anthropic-hired-back-two-of-its-employees-just-two-weeks-after-they-left-for-a-competitor)).

**A suspensão de Fable 5 / Mythos 5 (13/jun–1/jul de 2026) valeu para funcionários estrangeiros da própria Anthropic.** A diretriz de export control do governo americano suspendeu acesso "by any foreign national, whether inside or outside the United States, including foreign national Anthropic employees" ([comunicado da Anthropic, 12/06/2026](https://www.anthropic.com/news/fable-mythos-access)). A Anthropic desligou os dois modelos para todos os clientes, disse que "Access to all other Anthropic models will not be affected", e é silenciosa sobre se funcionários americanos mantiveram acesso interno. A componente ficou como incidente "critical" único no status page, com 450 horas ([incidente s9w82lp9dcn9](https://status.claude.com/api/v2/incidents/s9w82lp9dcn9.json)). Acesso restaurado em 1/jul ([Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5)).

#### O que é inferência

- "Não usam GPT/Gemini para trabalhar" é inferência a partir de (a) Cherny dizendo que não experimenta concorrentes, (b) ausência total de declarações em contrário, (c) fallback Claude-only na ferramenta. Não há política interna publicada sobre uso de ferramentas concorrentes por funcionários.
- Durante a suspensão de Fable/Mythos, a leitura mais plausível é que funcionários caíram para Opus 4.8 / Sonnet — mas ninguém disse isso.

#### O que não se sabe

- Se algum funcionário da Anthropic usa ChatGPT/Codex/Gemini no dia a dia, e se existe política interna sobre isso.
- O que funcionários americanos usaram entre 13/jun e 1/jul de 2026.
- Se funcionários usam Bedrock/Vertex como fallback interno (nenhuma fonte; e há relatos contraditórios de usuários sobre o Vertex ter ficado dois dias fora em ago/2026).

#### Mitos

- **"Eles usam ChatGPT, óbvio."** Só piada de comunidade. Nenhuma evidência.
- **"O Claude Code cai para GPT via gateway."** A documentação diz o oposto; o vazamento não tem nenhum caminho para modelo não-Anthropic; o modo watchdog público (`CLAUDE_CODE_RETRY_WATCHDOG`) espera indefinidamente por 429/529 em vez de trocar de provedor ([env vars](https://code.claude.com/docs/en/env-vars.md)).

---

### 2.3 Trabalham à moda antiga?

#### O que a evidência diz

**Existe um time humano cuja função oficial é responder a incidentes do Claude.** AIRE (AI Reliability Engineering) é um time nomeado em vagas oficiais da Anthropic: "Claude has your back. AIRE has Claude's." e "Lead incident response for critical AI services" ([vaga Londres](https://job-boards.greenhouse.io/anthropic/jobs/5101173008); [Dublin](https://job-boards.greenhouse.io/anthropic/jobs/5101169008); [EUA](https://job-boards.greenhouse.io/anthropic/jobs/5113224008)). A frase "fixing Claude without Claude when it goes down" é bio pessoal de Alex Palcuie, MTS no AIRE ([palcu.net](https://palcu.net/); [QCon London](https://qconlondon.com/speakers/alexpalcuie)) — não é missão do time, e não deve ser lida como "humanos respondem sem o modelo".

**A resposta a "o Claude conserta os próprios incidentes?" é não — com asterisco.** Na palestra do QCon London (17/03/2026; transcrição no InfoQ em 26/08/2026), Palcuie: "If anyone has this working, it's the company that makes the model. We have unlimited tokens. Researchers sit a desk away from me. I get involved in training the models. Surely, if it's anyone, it's us. Let me get the answer out of the way. It's a no." E: "If an LLM could carry a pager, we might not need to hire so much. The fact that my team exists, the fact that we're hiring for many positions, in London, in Dublin, and the U.S. ... this should show to you that, no, it doesn't work." Asterisco: "many of us would not be surprised if somewhere in the future we would be able to do such a thing" ([InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)). Nota: foi pergunta retórica dele mesmo, não do público.

**Mas o Claude é a primeira ferramenta que ele pega quando está disponível.** "Since about January this year, I've started doing something that feels slightly transgressive to admit, which is, I start reaching out for Claude before I reach out to my monitoring dashboards" ([InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)). A palestra foi coberta pelo The Register como "Fixing Claude *with* Claude" ([The Register, 19/03/2026](https://www.theregister.com/software/2026/03/19/fixing-claude-with-claude-anthropic-reports-on-ai-sre/5224819)).

**Parte do trabalho ainda é manual — e a Anthropic teme perder essa habilidade.** Palcuie: "While I was going through the logs manually, because this is something that I still do, I don't know why, one of my newer teammates, not even on-call trained, two to three months in the team, just pointed Claude Code at the logs. It instantly found the root cause". E, na seção "The Learning Problem": "When the big thing happens that the model can't fix, you might be miscalibrated on how to respond to such an incident. I'm genuinely worried about this" ([InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)). Ele ressalva que o Claude "is not reasoning about the cause yet. It's just gathering signals way faster".

**O Claude está dentro do loop de incidentes da Anthropic — o que cai junto quando o Claude cai.** Post oficial de 18/08/2026: "For the last several months Claude Tag has been the on-call first responder for CI/CD failures at Anthropic ... Claude authored the first situation report in every recent incident that had one, typically publishing its first analysis within 15 minutes" (mediana 14 min), com subagentes investigando Grafana, logs, PagerDuty, GitHub, Kubernetes e Slack via MCP ([claude.com/blog](https://claude.com/blog/ai-ci-cd-on-call)). Nuance: é a rotação do time de CI, construída por um engenheiro, sobre o produto público Claude Tag (Slack); o kit open-source é read-only e "All fixes are deployed by humans" ([anthropics/oncall-kit](https://github.com/anthropics/oncall-kit)). Nem o post nem o kit dizem o que acontece quando a API do Claude está indisponível.

**Exemplos de incidentes reais debugados com Claude (quando o Claude estava de pé):** na véspera de Ano Novo (31/12/2025), 500s no Opus 4.5 — Palcuie abriu o Claude Code com um SKILL.md próprio, o modelo escreveu SQL, achou uma exceção no caminho de imagens disparada por requisições com exatamente 22 imagens, e concluiu "stop looking at the 500s, this is fraud" (~200 contas, ~4.000 cadastros no mesmo template) ([InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)). O time de Data Infrastructure usou o Claude Code para diagnosticar exaustão de IPs de pods em Kubernetes durante uma queda, e Security Engineering alimenta o Claude Code com stack traces em incidentes ([How Anthropic teams use Claude Code, 24/07/2025](https://claude.com/blog/how-anthropic-teams-use-claude-code)).

**Quanto código humano ainda existe:** Boris Cherny, na Fortune Brainstorm Tech (11/06/2026): "I haven't written a line of code by hand in, I think, eight months now" ([Fortune](https://fortune.com/2026/06/11/anthropic-claude-boris-cherny-doesnt-write-code-by-hand-anymore/)); em X, 27/12/2025: "In the last thirty days, 100% of my contributions to Claude Code were written by Claude Code" ([X](https://x.com/bcherny/status/2004897269674639461)). A Anthropic afirma que "As of May 2026, more than 80% of the code we merge into Anthropic's codebase was authored by Claude" e cita um funcionário anônimo: "it's now been ~5 months since I last wrote any code myself" ([Anthropic Institute](https://www.anthropic.com/institute/recursive-self-improvement)); o Deputy CISO repete "about 80%" ([claude.com, 21/07/2026](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle)). Um porta-voz deu faixa de 70–90% em jan/2026 ([Fortune, 29/01/2026](https://fortune.com/2026/01/29/100-percent-of-code-at-anthropic-and-openai-is-now-ai-written-boris-cherny-roon/)).

**O estudo interno da Anthropic também registra o medo de atrofia — e ignora quedas.** Em ago/2025, 132 engenheiros/pesquisadores responderam usar o Claude em 59% do trabalho (28% um ano antes), com +50% de produtividade auto-relatada; mais da metade disse conseguir "fully delegate" só 0–20% das tarefas; e alguns relataram "When producing output is so easy and fast, it gets harder and harder to actually take the time to learn something". As palavras outage, unavailable, downtime não aparecem no texto ([How AI is transforming work at Anthropic, 02/12/2025](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic)).

**"Antfooding" agressivo.** Cerca de 60–100 releases internos por dia (set/2025), "Everyone at Anthropic uses the internal version" ([Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-claude-code-is-built)); "over I think 70 or 80 percent of ants — technical Anthropic employees — use Claude Code every day" (Cat Wu, out/2025, [Every](https://every.to/podcast/transcript-how-to-use-claude-code-like-the-people-who-built-it)); features saem primeiro para todo mundo dentro da Anthropic, e a versão interna do Claude Tag "lands 65% of our product eng PRs" — só do time de produto do Claude Code ([Simon Willison, 21/07/2026](https://simonwillison.net/2026/Jul/21/cat-and-thariq/)).

#### O que é inferência

- "Humanos lideram a resposta, usando Claude Code como ferramenta de primeira linha quando acessível; quando o próprio Claude está fora, o que resta é a habilidade manual que Palcuie diz ainda praticar" — é a síntese mais defensável, mas Palcuie fala por si, não pelo time.
- A piada "fixing Claude without Claude" descreve o *edge case* em que a ferramenta indisponível é o Claude; a maioria dos incidentes é parcial (ex.: 11/03/2026 API não afetada; 26–27/03 só Opus/Sonnet 4.6), então o Claude geralmente continua alcançável por outro modelo ou outra superfície.

#### O que não se sabe

- Nenhum funcionário nomeado descreveu, em público, ter perdido acesso, trocado de modelo ou trabalhado na mão durante uma queda. O único comentário "in-incident" encontrado de um engenheiro nomeado é um tweet de Cherny em 21/08/2026 ("Coding is solved, bugs are not yet solved. Fix incoming") — e ele responde a um bug de relaunch do app desktop, não a uma queda ([X](https://x.com/bcherny/status/2090649326032945591)).
- Se existe runbook/procedimento formal "Claude API indisponível" no AIRE ou no oncall-kit (o kit só cobre GitHub e Slack fora do ar).

#### Mitos

- **"Palcuie foi puxado para um incidente no meio da palestra."** Ele disse "Earlier, I was involved in an incident, even if I'm at a conference" — mais cedo no dia, não durante o talk.
- **"Ninguém na Anthropic escreve código."** Humanos ainda são ~20% das linhas mergeadas, dirigem, revisam e aprovam; a Anthropic diz que "agents aren't merging code to production unchecked".

---

## 3. Contexto

### 3.1 Linha do tempo de quedas e incidentes relevantes (2025–2026)

Fonte primária de todas as linhas do status page: [status.claude.com/history](https://status.claude.com/history) e [incidents.json](https://status.claude.com/api/v2/incidents.json). Causas declaradas só quando a Anthropic as publicou.

| Data | Duração | Produtos afetados | Causa declarada | Fonte |
|---|---|---|---|---|
| 05/08–18/09/2025 | ~6 semanas (degradação) | Sonnet 4 (API 1P: pico 16% em 31/08; Bedrock 0,18%; Vertex <0,0004%) | Bug de roteamento para servidores de contexto 1M + dois bugs de inferência | [Postmortem set/2025](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) |
| 10/09/2025 | horas | API, claude.ai, Console | Não declarada | [HN 45200398](https://news.ycombinator.com/item?id=45200398); [Slashdot/Ars](https://developers.slashdot.org/story/25/09/10/2039218/developers-joke-about-coding-like-cavemen-as-ai-service-suffers-major-outage) |
| 31/12/2025 | não divulgada | Opus 4.5 (500s) | Fraude / abuso de contas (relato interno) | [Palcuie, InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/) |
| 13/01/2026 | — | serving | "configuration mismatch between our inference servers that caused our load balancing system to route traffic unevenly" | status page (postmortem curto) |
| 14/01/2026 | — | Opus 4.5, Sonnet 4.5 | "service deployment that temporarily reduced our serving capacity" | [status tgzm3mf45wzc](https://status.claude.com/incidents/tgzm3mf45wzc) |
| 21/01/2026 | — | modelos | "insufficient compute capacity allocated to meet demand" | status page (postmortem curto) |
| 03/02/2026 | 3 min (critical) | API, todos os modelos | "internal configuration update" | status page |
| 02/03/2026 | horas | claude.ai, apps | Anthropic: "match the incredible demand we've seen for Claude in recent days" | [CNBC](https://www.cnbc.com/2026/03/02/anthropic-claude-ai-outage-apple-pentagon.html); [HN 47216795](https://news.ycombinator.com/item?id=47217594) |
| 11/03/2026 | 14:17–17:11 UTC | claude.ai, login Claude Code/Console (API não afetada) | "primary application database experienced severely degraded I/O performance following a routine maintenance operation" | [status jm3b4jjy2jrt](https://status.claude.com/incidents/jm3b4jjy2jrt) |
| 22/03/2026 | — (critical) | claude.ai e login | Não declarada | status page |
| 26–27/03/2026 | ~1 dia | Opus 4.6, Sonnet 4.6 | "networking performance degradation within our infrastructure that disrupted communication between components of our serving stack" | [status b9802k1zb5l2](https://status.claude.com/incidents/b9802k1zb5l2) |
| 13/04, 28/04, 30/04/2026 | — (critical/major) | claude.ai; claude.ai + API | Não declarada | status page |
| 23/04/2026 | 4/mar–20/abr (qualidade, não disponibilidade) | Claude Code, Agent SDK, Cowork | Três mudanças de engenharia (esforço padrão, bug de cache de thinking, prompt de verbosidade) | [Postmortem abr/2026](https://www.anthropic.com/engineering/april-23-postmortem) |
| 08/05/2026 | — (major) | vários modelos | Não declarada | status page |
| 13/06–01/07/2026 | ~450 h (critical) | Fable 5, Mythos 5 em claude.ai, API, Claude Code, Cowork | Diretriz de export control do governo dos EUA | [status s9w82lp9dcn9](https://status.claude.com/api/v2/incidents/s9w82lp9dcn9.json); [Anthropic](https://www.anthropic.com/news/fable-mythos-access) |
| 16/06/2026 | — (critical) | vários modelos | Não declarada; 10ª interrupção em 12 dias | [TechTimes](https://www.techtimes.com/articles/318514/20260616/claude-outage-tenth-disruption-12-days-exposes-anthropic-infrastructure-strain.htm) |
| 23/06/2026 | 14:08–15:33 UTC (critical) | claude.ai, Console, API, Claude Code, Cowork (Gov não) | Não declarada | [Yahoo/BeInCrypto](https://tech.yahoo.com/ai/claude/articles/claude-outage-hits-public-users-200000867.html) |
| 21/07/2026 | 15:28–16:26 UTC (critical) | vários modelos | Não declarada | status page |
| 29–30/07/2026 | 19:45–21:26 UTC (critical) + 291 min (major) | claude.ai, API, Claude Code, Cowork | @ClaudeDevs no X: "Multiple separate network failures cut into our capacity to serve Claude" (não no status page) | [status q2kg8n613kr3](https://status.claude.com/incidents/q2kg8n613kr3); [explainx](https://explainx.ai/blog/claude-outage-network-failures-recovery-july-2026) |
| 05/08/2026 | 07:05–14:14 UTC | Mythos 5, Fable 5, Opus 5, Sonnet 5 (claude.ai, API, Claude Code, Cowork) | Não declarada | [Exame](https://exame.com/inteligencia-artificial/o-claude-caiu-anthropic-confirma-falha-nesta-quarta-feira-5/) |
| 16/08/2026 | ~36 min (critical) | claude.ai, Console, API, Claude Code, Cowork; sessões OAuth derrubadas | Não declarada | [HN 49324078](https://news.ycombinator.com/item?id=49324078) |
| 24/08/2026 | 04:50–07:36 UTC (major) | Mythos 5, Fable 5, Opus 5, Opus 4.8 | Não declarada | [status vgz5psbjmt1h](https://status.claude.com/incidents/vgz5psbjmt1h); [TechTimes](https://www.techtimes.com/articles/325344/20260824/commercial-claude-has-gone-down-28-times-30-days-its-government-tier-has-never-gone-down-once.htm) |
| 28/08/2026 | 17:22–20:21 UTC | Claude Code web, Cowork | "an issue with an upstream cloud provider" | [status vr9tpk8w7zr8](https://status.claude.com/incidents/vr9tpk8w7zr8) |
| 03/09/2026 | 13:26–16:23 UTC (major) | Mythos/Fable 5.1, 5, Opus 5, 4.8, 4.6 (claude.ai, API, Claude Code, Cowork) | Não declarada; Codex caiu simultaneamente | [status 461yvfrzpwtt](https://status.claude.com/incidents/461yvfrzpwtt); [HN 49549676](https://news.ycombinator.com/item?id=49549676) |

**Frequência agregada (status oficial, contagem própria em 03/09/2026):**
- 2026 (1/jan–3/set): 358 entradas — Jan 26, Fev 58, Mar 51, Abr 49, Mai 41, Jun 47, Jul 55, Ago 25, Set 6; 17 críticas, 95 major, 224 minor, 22 informativas ([history.json](https://status.claude.com/history.json?page=1)).
- 2025 inteiro: 335 (22 críticas); 2024 inteiro: 191 (5 críticas).
- Janela comparável jan–ago: 234 em 2025 vs 352 em 2026 (+50%), crescimento quase todo em "minor" (107→221); críticas praticamente iguais (16→17).
- Uptime de 90 dias em 3/set/2026: claude.ai 99,41%, API 99,51%, Claude Code 99,45%, Cowork 99,44%, Console 99,93%, Government 100,0% ([status.claude.com](https://status.claude.com/)).
- StatusGator (metodologia própria): "194 Claude outages since January 2026" ([StatusGator](https://statusgator.com/services/claude/outage-history)).
- Sem SLA no tier padrão ("best-effort availability"); Priority Tier "targets 99.5% uptime" mas não é mais vendido ([Service tiers](https://platform.claude.com/docs/en/api/service-tiers)); termos comerciais entregam o serviço "AS IS" e "AS AVAILABLE" ([Commercial Terms](https://www.anthropic.com/legal/commercial-terms)).
- Cuidado editorial: "entrada de incidente" não é "queda". 22 entradas são informativas, uma "critical" é a suspensão regulatória de Fable/Mythos, e muitas são degradações de 5–30 min em um único modelo. Falta comparador com OpenAI/Google no mesmo período (não foi possível contar de forma confiável).

**Causas oficiais em nível de empresa:**
- À Fortune (24/04/2026): "Demand for Claude has grown at an unprecedented rate, and our infrastructure has been stretched to meet it, particularly at peak hours" e "compute is a constraint across the entire industry" ([Fortune](https://fortune.com/2026/04/24/anthropic-engineering-missteps-claude-code-performance-decline-user-backlash/)). Era sobre a pressão geral e os limites de pico, não root cause de quedas específicas.
- Dario Amodei, Code with Claude (06/05/2026): "We tried to plan very well for a world of 10x growth per year. And yet we saw 80x. And so that is the reason we have had difficulties with compute" ([CNBC](https://www.cnbc.com/2026/05/06/anthropic-ceo-dario-amodei-says-company-crew-80-fold-in-first-quarter.html); [VentureBeat](https://venturebeat.com/technology/anthropic-says-it-hit-a-30-billion-revenue-run-rate-after-crazy-80x-growth)).
- Palcuie no HN (28/03/2026): "the general trend is the unprecedented growth ... we're dealing with very compressed timelines and while most of the time we're able to fix the issues beforehand, sometimes we have to do them in production. Sorry for that." ([HN 47552876](https://news.ycombinator.com/item?id=47543189)).
- Compute novo: acordo com a SpaceX pelo Colossus 1 (>300 MW, >220 mil GPUs NVIDIA), removendo a redução de limites em horário de pico ([Anthropic, 06/05/2026](https://www.anthropic.com/news/higher-limits-spacex)).

**Comunicação sobre quedas:** nenhum postmortem em nível de blog para queda de disponibilidade em 2026. No status page, só 8 das 358 entradas (~2%) trazem um parágrafo "Postmortem" com causa, todas entre 13/jan e 27/mar; desde abril, a única causa declarada foi a de 28/ago ("upstream cloud provider"). Nenhuma menciona impacto interno. ([status history](https://status.claude.com/history); [engineering index](https://www.anthropic.com/engineering)).

### 3.2 Dependência interna (números)

| Métrica | Valor | Fonte |
|---|---|---|
| Código mergeado autorado pelo Claude | >80% (maio/2026); "about 80%" (jul/2026); dígitos baixos antes de fev/2025 | [Anthropic Institute](https://www.anthropic.com/institute/recursive-self-improvement); [claude.com](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle) |
| Cherny sem escrever código à mão | desde nov/2025; "eight months" em jun/2026 | [Fortune](https://fortune.com/2026/06/11/anthropic-claude-boris-cherny-doesnt-write-code-by-hand-anymore/); [Lenny's](https://www.youtube.com/watch?v=We7BZVKbCVw) |
| Uso do Claude no trabalho (auto-relato, 132 eng.) | 59% (ago/2025), 28% um ano antes | [Anthropic Research](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic) |
| Produtividade auto-relatada | +50% (ago/2025), +20% um ano antes; +67% em PRs mergeados/eng/dia (objetivo) | idem |
| Delegação total | >50% conseguem delegar totalmente só 0–20% | idem |
| Uplift estimado com Mythos Preview (130 pesquisadores, mar/2026) | mediana ~4x (Anthropic: real "somewhat lower") | [Anthropic Institute](https://www.anthropic.com/institute/recursive-self-improvement) |
| Funcionários técnicos usando Claude Code diariamente | "70 or 80 percent" (out/2025); ">80% of engineers who write code" (set/2025) | [Every](https://every.to/podcast/transcript-how-to-use-claude-code-like-the-people-who-built-it); [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-claude-code-is-built) |
| Releases internos do Claude Code | ~60–100/dia (set/2025, time de ~12) | [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-claude-code-is-built) |
| PRs de produto do Claude Code via Claude Tag interno | 65% (jul/2026) | [Simon Willison](https://simonwillison.net/2026/Jul/21/cat-and-thariq/) |
| Acesso de agentes a serviços internos | "access sufficient to take down an internal Anthropic service ... today that level of access is routine" | [How we contain Claude, 25/05/2026](https://www.anthropic.com/engineering/how-we-contain-claude) |
| Primeiro SITREP de incidentes de CI | escrito pelo Claude, mediana 14 min, root cause em 4 min nos melhores casos | [claude.com/blog](https://claude.com/blog/ai-ci-cd-on-call) |

### 3.3 Infraestrutura de serving

- Três caminhos de serving declarados em set/2025 (API própria, Bedrock, Vertex) e três plataformas de hardware (Trainium, GPUs NVIDIA, TPUs); "greater resilience" é a justificativa oficial da diversidade ([postmortem 2025](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues); [Google/Broadcom, 06/04/2026](https://www.anthropic.com/news/google-broadcom-partnership-compute)). Docs atuais listam cinco rótulos de plataforma, incluindo Microsoft Foundry ([docs](https://platform.claude.com/docs/en/build-with-claude/overview)).
- "We never reduce model quality due to demand, time of day, or server load" (2025) e "We never intentionally degrade our models" (2026) — declarações de intenção, com o próprio postmortem admitindo semanas de degradação não intencional.
- Controles de privacidade internos "limit how and when engineers can access user interactions", o que atrasou o debug em 2025 — outro motivo pelo qual a Anthropic depende de reproduções internas.
- Compute: até 1 milhão de TPUs (out/2025), US$ 30 bi em Azure/NVIDIA (nov/2025), Colossus 1 da SpaceX (mai/2026). CFO: uso "fungible" das três famílias de chip; reuniões frequentes de alocação com discussão de ROI; piso de compute para desenvolvimento de modelo.
- Vazamento: tooling interno de incidentes só para "ants": `CLAUDE_CODE_UNATTENDED_RETRY` (retry indefinido de 429/529, depois publicado como `CLAUDE_CODE_RETRY_WATCHDOG` em jun/2026) e `claude rollback --safe` ("Roll back to the server-pinned safe version (set by oncall during incidents)") — confirma rotação de oncall para o Claude Code e uma estratégia de "esperar passar" para sobrecarga ([espelho do vazamento](https://github.com/davccavalcante/claude-code-leaked); [env vars](https://code.claude.com/docs/en/env-vars.md)).

---

## 4. Citações matadoras (verbatim, idioma original)

1. **"I keep Claude reliable on the AI Reliability Engineering (AIRE) team, which means the unenviable job of fixing Claude without Claude when it goes down."** — Alex Palcuie, Member of Technical Staff, AIRE, Anthropic; bio pessoal (redação atual desde abr/2026; versão de mar/2026 ligeiramente diferente). [palcu.net](https://palcu.net/)

2. **"Claude has your back. AIRE has Claude's. Help us keep Claude reliable for everyone who depends on it."** — Anthropic, vaga oficial "Staff Software Engineer, AI Reliability Engineering", Londres, atualizada 28/08/2026. [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5101173008)

3. **"If anyone has this working, it's the company that makes the model. We have unlimited tokens. Researchers sit a desk away from me. I get involved in training the models. Surely, if it's anyone, it's us. Let me get the answer out of the way. It's a no."** — Alex Palcuie, QCon London, 17/03/2026 (transcrição InfoQ 26/08/2026). [InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)

4. **"If an LLM could carry a pager, we might not need to hire so much. The fact that my team exists, the fact that we're hiring for many positions, in London, in Dublin, and the U.S., and we have staff positions, this should show to you that, no, it doesn't work."** — Palcuie, mesmo talk. [InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)

5. **"Claude is down more often than any of us would like. Earlier, I was involved in an incident, even if I'm at a conference."** — Palcuie, mesmo talk. [InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)

6. **"on-call is a tax we levy on humans because our systems are not good enough to look after themselves"** — Palcuie, mesmo talk. [InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)

7. **"since about January this year, I've started doing something that feels slightly transgressive to admit, which is, I start reaching out for Claude before I reach out to my monitoring dashboards."** — Palcuie, mesmo talk. [InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)

8. **"While I was going through the logs manually, because this is something that I still do, I don't know why, one of my newer teammates, not even on-call trained, two to three months in the team, just pointed Claude Code at the logs. It instantly found the root cause"** — Palcuie, mesmo talk. [InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)

9. **"When the big thing happens that the model can't fix, you might be miscalibrated on how to respond to such an incident. I'm genuinely worried about this."** — Palcuie, mesmo talk. [InfoQ](https://www.infoq.com/presentations/claude-sre-incidents/)

10. **"Yes, the general trend is the unprecedented growth that we've seen. Typically one would have some time in advance to re-engineer the systems to support the increased in traffic and users. But we're dealing with very compressed timelines and while most of the time we're able to fix the issues beforehand, sometimes we have to do them in production. Sorry for that."** — Alex Palcuie ("palcu"), Hacker News, 28/03/2026. [HN 47552876](https://news.ycombinator.com/item?id=47543189)

11. **"Twelve months ago, we'd have rejected out of hand the idea of granting Claude access sufficient to take down an internal Anthropic service. Today that level of access is routine, and Anthropic developers are more productive for it."** — Anthropic Engineering (McGuinness, Grace, De Jonghe, Eaton, Ribbink), 25/05/2026. [How we contain Claude](https://www.anthropic.com/engineering/how-we-contain-claude)

12. **"I haven't written a line of code by hand in, I think, eight months now."** — Boris Cherny, head do Claude Code, Fortune Brainstorm Tech, 11/06/2026. [Fortune](https://fortune.com/2026/06/11/anthropic-claude-boris-cherny-doesnt-write-code-by-hand-anymore/)

13. **"We tried to plan very well for a world of 10x growth per year. And yet we saw 80x. And so that is the reason we have had difficulties with compute."** — Dario Amodei, CEO, Code with Claude, San Francisco, 06/05/2026. [VentureBeat](https://venturebeat.com/technology/anthropic-says-it-hit-a-30-billion-revenue-run-rate-after-crazy-80x-growth); [CNBC](https://www.cnbc.com/2026/05/06/anthropic-ceo-dario-amodei-says-company-crew-80-fold-in-first-quarter.html)

14. **"we'll ensure that a larger share of internal staff use the exact public build of Claude Code (as opposed to the version we use to test new features)"** — Anthropic Engineering, postmortem de 23/04/2026. [april-23-postmortem](https://www.anthropic.com/engineering/april-23-postmortem)

15. **"Yeah, I actually haven't really used it. But I think I did use it maybe when it came out. It looked a lot like Claude Code to me, so that was kind of flattering. [...] we don't spend a lot of time looking at competing products. We don't really try the other products."** — Boris Cherny sobre o Codex, Lenny's Podcast, 19/02/2026. [YouTube](https://www.youtube.com/watch?v=We7BZVKbCVw)

**Cor de comunidade (usar como piada, não como fato):**
- "When Claude is down, do they have a backup Claude to investigate the root cause? Investigating without AI sounds so 2024." — pykul, HN, 24/08/2026, zero respostas. [HN](https://news.ycombinator.com/item?id=49415517)
- "more importantly how is Anthropric [sic] going to fix Claude if Claude can't help them :-D" — abirch, HN, 02/03/2026. [HN](https://news.ycombinator.com/item?id=47217594)
- "Nooooo I'm going to have to use my brain again and write 100% of my code like a caveman from December 2024." — atonse, HN, 12/06/2025 (queda do GCP; repostado em quedas do Claude em set/2025 e ago/2026). [Slashdot/Ars](https://developers.slashdot.org/story/25/09/10/2039218/developers-joke-about-coding-like-cavemen-as-ai-service-suffers-major-outage)
- "The C-suite doesn't want us to write code by hand anymore, so I think I'm supposed to just drink tea and collect salary whenever Claude is down." — Hamuko, HN, 11/03/2026. [HN](https://news.ycombinator.com/item?id=47336999)
- "Como que trabalha? Claude caiu… nem lembro como clicar no mouse sem ele 😭" — @rafagallopeu, X, 18/08/2026, via Olhar Digital. [Olhar Digital](https://olhardigital.com.br/2026/08/18/inteligencia-artificial/claude-fica-fora-do-ar-nesta-terca-feira-18/)
- Atenção: "todo mundo virou engenheiro de software de novo" (Tecnoblog, 05/08/2026) é **tradução** de um tweet em inglês de @Ai_Engineer__ ("Claude is down. I guess everyone is a software engineer again."), não fala de brasileiro. [Tecnoblog](https://tecnoblog.net/noticias/claude-fora-do-ar-instabilidade-derruba-modelos-da-anthropic/)

---

## 5. O que NÃO se sabe (ausências documentadas)

1. **Nenhuma declaração oficial** da Anthropic (blog, help center, status page, postmortem) sobre o que funcionários fazem durante uma queda. Estudo interno de dez/2025 e os dois postmortems foram lidos por inteiro: zero menções a indisponibilidade.
2. **Nenhum post público de funcionário nomeado** (Cherny, Wu, Shihipar, Albert, Krieger, Amodei, Askell, Kaplan, Palcuie) dizendo que perdeu acesso, trocou de modelo ou trabalhou na mão numa queda. Os 71 comentários de "palcu" no HN e os retros de incidente foram varridos.
3. **Nenhuma evidência de cluster de inferência privado** para staff. Só staging vazado (não documentado como fallback), Gov isolado (sem explicação oficial) e o piso de compute para pesquisa citado pelo CFO (treinamento, não serving de emergência).
4. **Nenhuma evidência de uso de GPT/Codex/Gemini** por funcionários em quedas ou no dia a dia; nenhuma política interna publicada; nenhuma entrevista onde pesquisador da Anthropic é perguntado se usa ChatGPT (Cherny sobre Codex é o mais perto).
5. **Nenhum fallback para modelo não-Anthropic** no código vazado, na doc ou nas ferramentas; nenhuma frase oficial "employees use the same production API as customers".
6. **O que funcionários americanos usaram entre 13/jun e 1/jul de 2026**, quando Fable 5/Mythos 5 foram suspensos e o comunicado só fala de funcionários estrangeiros.
7. **Nenhum postmortem oficial** para quedas de disponibilidade de 2026; @ClaudeDevs explicou 29–30/jul só no X; status page desde abril não traz causa exceto 28/ago.
8. **Nenhum procedimento "Claude API down"** no oncall-kit, no post do Claude Tag on-call, no blog de Palcuie ou no abstract do SREcon26 EMEA (15/10/2026).
9. **Sem SLA público** além do alvo de 99,5% do Priority Tier (que não é mais vendido); sem comparador confiável de frequência com OpenAI/Google no mesmo período.
10. **Sem cobertura em português** do tema interno: Exame, TechTudo, Tecnoblog, Canaltech, Olhar Digital, CNN Brasil cobrem "o Claude caiu?" e reações de usuários; TabNews (1.909 posts jun–set/2026) e a newsletter do Filipe Deschamps (700 itens) não têm thread sobre queda do Claude nem sobre a Anthropic sem Claude. Hipsters Ponto Tech: nada relevante.
11. **Não usar como fato:** "queda de 48h em 2/mar/2026" (dev.to), "loop infinito de sub-agente" como causa de 2/jun (TechTimes), "20 h/semana de Claude Code" interno, "uptime 98,2% em março" (techmaniacs), "queda mundial em maio", e a leitura de "pesquisa fica com a maior fatia do compute" (Crypto Briefing).

---

## 6. Ângulos de post para o Beer & Code

1. **"Quem conserta o Claude quando o Claude cai? A resposta oficial da Anthropic é o silêncio"**
   *Gancho:* a pergunta que o HN fez e ninguém respondeu, respondida com a soma de evidências indiretas.
   *Por que funciona:* dá o conflito logo no título e entrega a apuração honesta (seções 2 e 5). Apoia-se em C01–C04, C24, C25.

2. **"'Fixing Claude without Claude': o time humano que segura o pager na Anthropic"**
   *Gancho:* perfil do AIRE a partir das vagas oficiais e da palestra do Palcuie, incluindo "It's a no" e "if an LLM could carry a pager".
   *Por que funciona:* história com personagem, citações fortes e verificadas, e um recado para SRE brasileiro (atrofia de habilidade). Apoia-se em C01–C05.

3. **"O código vazado do Claude Code mostra o que os 'ants' têm que você não tem"**
   *Gancho:* `USER_TYPE === 'ant'`, `api-staging.anthropic.com`, `capybara-fast`, `claude rollback --safe`, Undercover mode.
   *Por que funciona:* público dev adora ler código; enquadra o vazamento como staging e modelos não lançados, não como "servidor secreto". Apoia-se em C10–C12, com o disclaimer de espelho de vazamento.

4. **"80% do código da Anthropic é escrito pelo Claude. O que acontece nos 99,4% de uptime?"**
   *Gancho:* cruza os números de dependência (Cherny, >80%, 59%, "routine access") com os 358 incidentes e a inexistência de SLA.
   *Por que funciona:* números duros, todos oficiais ou de primeira mão; permite discutir risco de dependência sem sensacionalismo. Apoia-se em C07–C09, C22–C23.

5. **"A Anthropic tem um Claude de backup? Não — mas o governo americano tem"**
   *Gancho:* o meme "down for everyone except the government" e a componente Claude for Government em 100% enquanto o resto fica em 99,4%.
   *Por que funciona:* curiosidade + dado verificável no status page; obriga a explicar que a Anthropic nunca descreveu a separação. Apoia-se em C14, com as nuances do Wayback.

6. **"Trocar pra GPT quando o Claude cai? Nem a Anthropic faz isso (e o Codex caiu junto em 3/set)"**
   *Gancho:* fallback Claude-para-Claude na ferramenta, Cherny dizendo que não usa Codex, e o dia em que Claude, Codex e Grok caíram juntos.
   *Por que funciona:* playbook prático para o leitor (Bedrock/Vertex, `--fallback-model`, OpenRouter) contrastado com a ausência de fallback multi-vendor na própria Anthropic. Apoia-se em C19–C21, gap de podcasts.

**Recomendação:** o ângulo 1 ou 2 como texto principal; 3 e 5 como caixas/seções; 6 como fecho prático. Evitar sugerir que o Claude é "unicamente instável" — falta comparador; usar a comparação 2025 vs 2026 do próprio status page (234 → 352 na janela jan–ago, críticas estáveis).

---

## 7. Fontes

### Anthropic oficial
- https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues
- https://www.anthropic.com/engineering/april-23-postmortem
- https://www.anthropic.com/engineering/how-we-contain-claude
- https://www.anthropic.com/engineering
- https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic
- https://www.anthropic.com/institute/recursive-self-improvement
- https://www.anthropic.com/research/mythos-preview
- https://www.anthropic.com/glasswing
- https://www.anthropic.com/news/fable-mythos-access
- https://www.anthropic.com/news/redeploying-fable-5
- https://www.anthropic.com/news/higher-limits-spacex
- https://www.anthropic.com/news/google-broadcom-partnership-compute
- https://www.anthropic.com/news/introducing-claude-tag
- https://www.anthropic.com/legal/commercial-terms
- https://alignment.anthropic.com/2025/openai-findings/
- https://claude.com/blog/ai-ci-cd-on-call
- https://claude.com/blog/how-anthropic-teams-use-claude-code
- https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle
- https://claude.com/blog/how-anthropic-employees-use-claude-tag
- https://code.claude.com/docs/en/cli-reference
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/llm-gateway
- https://code.claude.com/docs/en/env-vars.md
- https://platform.claude.com/docs/en/api/service-tiers
- https://platform.claude.com/docs/en/build-with-claude/overview
- https://job-boards.greenhouse.io/anthropic/jobs/5101173008
- https://job-boards.greenhouse.io/anthropic/jobs/5101169008
- https://job-boards.greenhouse.io/anthropic/jobs/5113224008
- https://github.com/anthropics/oncall-kit

### Status page
- https://status.claude.com/
- https://status.claude.com/history
- https://status.claude.com/history.json?page=1
- https://status.claude.com/api/v2/incidents.json
- https://status.claude.com/api/v2/components.json
- https://status.claude.com/incidents/b9802k1zb5l2
- https://status.claude.com/incidents/vr9tpk8w7zr8
- https://status.claude.com/incidents/jm3b4jjy2jrt
- https://status.claude.com/incidents/tgzm3mf45wzc
- https://status.claude.com/incidents/q2kg8n613kr3
- https://status.claude.com/incidents/vgz5psbjmt1h
- https://status.claude.com/incidents/461yvfrzpwtt
- https://status.claude.com/api/v2/incidents/s9w82lp9dcn9.json
- https://statusgator.com/services/claude/outage-history

### Funcionários da Anthropic (posts, palestras)
- https://palcu.net/
- https://qconlondon.com/speakers/alexpalcuie
- https://qconlondon.com/presentation/mar2026/can-claude-fix-itself-using-llms-incident-response
- https://www.infoq.com/presentations/claude-sre-incidents/
- https://news.ycombinator.com/item?id=47543189 (thread com comentários de "palcu")
- https://news.ycombinator.com/item?id=45281139 (comentário de "l1n" sobre Bedrock)
- https://x.com/bcherny/status/2004897269674639461
- https://x.com/bcherny/status/2090649326032945591
- https://www.youtube.com/watch?v=We7BZVKbCVw (Lenny's Podcast, Boris Cherny)
- https://www.youtube.com/watch?v=wEEZPpx8qow (Invest Like the Best, Krishna Rao)
- https://www.teahose.com/podcast/Invest%20like%20the%20best/Krishna%20Rao%20-%20Anthropic's%20CFO%20on%20Compute,%20Scaling%20to%20$30B%20ARR,%20and%20the%20Returns%20to%20Frontier%20Intelligence%20-%20[Invest%20Like%20the%20Best,%20EP.471]
- https://every.to/podcast/transcript-how-to-use-claude-code-like-the-people-who-built-it
- https://simonwillison.net/2026/Jul/21/cat-and-thariq/

### Imprensa
- https://www.theregister.com/software/2026/03/19/fixing-claude-with-claude-anthropic-reports-on-ai-sre/5224819
- https://www.devclass.com/ai-ml/2026/03/23/fixing-claude-with-claude-anthropic-reports-on-ai-site-reliability-engineering/5209470
- https://fortune.com/2026/06/11/anthropic-claude-boris-cherny-doesnt-write-code-by-hand-anymore/
- https://fortune.com/2026/01/29/100-percent-of-code-at-anthropic-and-openai-is-now-ai-written-boris-cherny-roon/
- https://fortune.com/2026/04/24/anthropic-engineering-missteps-claude-code-performance-decline-user-backlash/
- https://www.cnbc.com/2026/05/06/anthropic-ceo-dario-amodei-says-company-crew-80-fold-in-first-quarter.html
- https://www.cnbc.com/2026/03/02/anthropic-claude-ai-outage-apple-pentagon.html
- https://venturebeat.com/technology/anthropic-says-it-hit-a-30-billion-revenue-run-rate-after-crazy-80x-growth
- https://newsletter.pragmaticengineer.com/p/how-claude-code-is-built
- https://techcrunch.com/2025/08/02/anthropic-cuts-off-openais-access-to-its-claude-models/
- https://www.theverge.com/ai-artificial-intelligence/708521/anthropic-hired-back-two-of-its-employees-just-two-weeks-after-they-left-for-a-competitor
- https://www.techtimes.com/articles/325344/20260824/commercial-claude-has-gone-down-28-times-30-days-its-government-tier-has-never-gone-down-once.htm
- https://www.techtimes.com/articles/318514/20260616/claude-outage-tenth-disruption-12-days-exposes-anthropic-infrastructure-strain.htm
- https://tech.yahoo.com/ai/claude/articles/claude-outage-hits-public-users-200000867.html
- https://www.latestly.com/social-viral/claude-down-funny-memes-and-videos-shared-on-social-media-as-anthropics-ai-chatbot-suffers-outage-7486966.html
- https://explainx.ai/blog/claude-outage-network-failures-recovery-july-2026
- https://developers.slashdot.org/story/25/09/10/2039218/developers-joke-about-coding-like-cavemen-as-ai-service-suffers-major-outage
- https://www.nextgov.com/artificial-intelligence/2026/06/anthropic-suspends-top-ai-models-after-us-export-control-order/414173/

### Imprensa brasileira
- https://exame.com/inteligencia-artificial/o-claude-caiu-anthropic-confirma-falha-nesta-quarta-feira-5/
- https://tecnoblog.net/noticias/claude-fora-do-ar-instabilidade-derruba-modelos-da-anthropic/
- https://olhardigital.com.br/2026/08/18/inteligencia-artificial/claude-fica-fora-do-ar-nesta-terca-feira-18/
- https://www.techtudo.com.br/noticias/2026/08/claude-fora-do-ar-instabilidade-afeta-chatbot-e-claude-code-nesta-quarta-5-edsoftwares.ghtml
- https://www.tabnews.com.br/api/v1/contents?strategy=relevant&page=1&per_page=100 (ausência verificada)

### Vazamento / engenharia reversa
- https://github.com/davccavalcante/claude-code-leaked
- https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/
- https://www.theregister.com/2026/04/01/claude_code_source_leak_privacy_nightmare/

### Comunidade (HN)
- https://news.ycombinator.com/item?id=49415517
- https://news.ycombinator.com/item?id=47217594
- https://news.ycombinator.com/item?id=47336999
- https://news.ycombinator.com/item?id=47368939
- https://news.ycombinator.com/item?id=49550274
- https://news.ycombinator.com/item?id=49549676
- https://news.ycombinator.com/item?id=49415907
- https://news.ycombinator.com/item?id=49324078
- https://news.ycombinator.com/item?id=47228198
- https://news.ycombinator.com/item?id=45200398
