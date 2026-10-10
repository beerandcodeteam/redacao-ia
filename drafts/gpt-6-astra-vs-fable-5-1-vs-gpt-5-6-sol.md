O **GPT-6 Astra** é o novo modelo topo de linha da OpenAI, lançado hoje, 3 de setembro de 2026, pelo mesmo preço do Claude Fable 5.1, que saiu dois dias antes. Greg Brockman abriu o anúncio com "Welcome to the AGI era".

Ignora a frase. Olha a tabela.

Neste post eu coloco os três modelos que importam agora lado a lado: GPT-6 Astra, GPT-5.6 Sol (o topo de linha da OpenAI até ontem) e Claude Fable 5.1. Benchmark por benchmark, com fonte. Preço com a conta de cache aberta, porque é ali que a fatura nasce. E o detalhe que mais importa pra quem constrói agente: o mesmo GPT-6 Astra tirou 62,7% e 99,9% no mesmo benchmark, e o que mudou entre um número e outro não foi o modelo.

## TL;DR

- **O que é:** GPT-6 Astra, novo flagship da OpenAI. Model id `gpt-6-astra`, janela de 1.050.000 tokens, 128k de output, conhecimento até 30/04/2026. Sucessor do GPT-5.6 Sol.
- **Preço:** $10 input / $50 output por milhão de tokens. Exatamente o preço do Claude Fable 5.1, e 2,5x o preço atual do GPT-5.6 Sol. Cache read a $1, contra $0,25 do Fable 5.1.
- **Benchmarks:** nos números da própria OpenAI, o Astra ganha do Fable 5.1 em tudo que os dois publicaram, com folga em matemática, ciência e automação. No índice independente da Artificial Analysis, o Fable 5.1 continua em 1º e o Astra aparece em 14º. Explico a diferença abaixo.
- **Acesso:** primeiro pras empresas do programa Daybreak (cibersegurança), depois "nos próximos dias" pra ChatGPT Plus, Pro, Business e Enterprise, API e AWS. É o primeiro modelo classificado como **Critical** em cyber no Preparedness Framework da OpenAI.
- **Links úteis:** [system card](https://deploymentsafety.openai.com/gpt-6-astra), [docs do modelo na API](https://developers.openai.com/api/docs/models/gpt-6-astra), [análise do ARC Prize](https://arcprize.org/blog/astra).

## O que a OpenAI lançou, e por que o preço é a primeira notícia

O pitch oficial é curto: "o modelo mais inteligente e alinhado do mundo", estado da arte em computer use, navegação, engenharia de software, cibersegurança, ciência e trabalho profissional. Brockman resumiu pra [NBC](https://www.nbcnews.com/tech/tech-news/openai-debuts-gpt-6-astra-security-measures-rcna595940): "o Astra consegue fazer qualquer coisa que um humano faz com um computador".

O [vídeo de lançamento](https://www.youtube.com/watch?v=1QNsdr-Qx_I) é todo sobre isso. Uma pessoa pede um círculo amarelo, transforma em janela de foguete, manda virar modelo 3D no Blender, exporta STL pra impressora. No meio disso, o modelo cria um anúncio no eBay com foto da pasta de downloads, redige minuta de contrato de licenciamento, monta um jogo 3D de desviar de asteroide, pede comida e reserva quadra de tênis. Tudo em paralelo, numa sessão só. É demo, então desconta. Mas a mensagem é clara: o produto não é chat. É operador de computador. (Se você acompanhou o [rastreador do GPT-6](https://blog.beerandcode.com.br/noticias/gpt-6-lancamento-rastreador) desde julho, o nome Astra e o rollout escalonado por cyber eram as duas coisas que mais se repetiam nos vazamentos. As duas se confirmaram.)

Agora o número que ninguém colocou na manchete.

O Astra custa **$10 por milhão de tokens de input e $50 de output**. É a mesma tabela do Claude Fable 5.1. Centavo por centavo.

Isso é uma mudança de postura. Em julho, o GPT-5.6 Sol chegou custando cerca de um terço do Fable 5 por tarefa no índice da Artificial Analysis, e a OpenAI vendeu isso como "fronteira de preço-desempenho". Hoje o Sol está em [$4 / $20](https://artificialanalysis.ai/models/gpt-5-6-sol) em preço promocional. O Astra vem 2,5x acima do Sol e cravado no preço do concorrente. A OpenAI parou de competir por baixo no topo da linha. Quando os dois maiores labs cobram o mesmo, a briga deixa de ser preço e vira preço por tarefa, e isso muda como você compara os dois.

Tem ainda um modo Fast a $20 / $100, segundo o [VentureBeat](https://venturebeat.com/technology/welcome-to-the-agi-era-openai-launches-gpt-6-astra), e uma sobretaxa de contexto longo: prompt acima de 272k tokens paga 2x no input e 1,5x no output da request inteira.

A tabela de preço dos três, por milhão de tokens:

| Modelo | Input | Cache read | Cache write | Output |
|---|---|---|---|---|
| GPT-6 Astra | $10,00 | $1,00 | $12,50 | $50,00 |
| Claude Fable 5.1 | $10,00 | **$0,25** | $12,50 | $50,00 |
| GPT-5.6 Sol (promo) | $4,00 | ~$0,40 | ~$5,00 | $20,00 |

Fontes: [docs do Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [anúncio do Fable 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1), [Artificial Analysis](https://artificialanalysis.ai/models/gpt-5-6-sol) pro Sol. Cache do Sol estimado pela regra da OpenAI de cache read a 10% do input e cache write a 1,25x.

Repara na coluna do cache read. É a única linha em que Astra e Fable 5.1 divergem, e é a linha que mais pesa numa sessão de agente. Volto nisso na conta.

O topo de linha trocou de dono duas vezes em 48 horas, e vai trocar de novo antes do fim do mês. O que não muda é a arquitetura que aguenta trocar de modelo sem reescrever o produto. É essa a régua que a gente usa toda semana, ao vivo, no [Clã Beer and Code](https://beerandcode.com.br?utm_source=blog&utm_medium=post&utm_campaign=gpt-6-astra-vs-fable-5-1-vs-gpt-5-6-sol&utm_content=j-n1): o modelo é parâmetro, não fundação.

## GPT-6 Astra vs Fable 5.1 vs GPT-5.6 Sol: a tabela, benchmark por benchmark

Todos os números do Astra abaixo são reportados pela OpenAI, no [system card](https://deploymentsafety.openai.com/gpt-6-astra) e no material de lançamento compilado pelo [OfficeChai](https://officechai.com/ai/openais-gpt-6-astra-seems-to-comfortably-beat-fable-5-1-in-leaked-benchmarks/). Os do Fable 5.1 e do Sol que aparecem no anúncio da OpenAI batem com os que a [Anthropic publicou](https://www.anthropic.com/claude-fable-and-mythos-5-1) dois dias atrás, o que dá um mínimo de confiança cruzada. Ainda assim: ninguém independente reproduziu nada disso ainda.

| Benchmark | GPT-6 Astra | Claude Fable 5.1 | GPT-5.6 Sol |
|---|---|---|---|
| FrontierMath Tier 4 (v2) | **97,6%** | 87,8% | 83,0% |
| GPQA Diamond | **96,0%** | 93,7% | n/p |
| Terminal-Bench-Science 0.1 | **64,6%** | 52,6% | 22,4% |
| AutomationBench | **41,4%** | 31,4% | 19,6% |
| DeepSWE v1.1 | **74,1%** | 67,4% | n/p |
| BenchCAD | **95,9%** | 84,3% | n/p |
| HealthBench Professional | **63,4%** | 56,6% | 60,5% |
| OSWorld 2.0 | 72,6% | 77,9% (partial) / 41,7% (strict) | 65,7% |
| ARC-AGI-3 (semi-private) | 99,9% / 62,7%* | n/p | n/p |
| Terminal-Bench 4.0 | "estado da arte", sem número | 55,8% | 37,3% |

*Depende do harness. Seção própria abaixo. n/p = não publicado.

Olha a tabela em três grupos.

**Grupo 1: massacre.** FrontierMath Tier 4 foi de 87,8% pra 97,6%, e a OpenAI fala em benchmark saturado. Terminal-Bench-Science subiu 12 pontos em cima do que já era a maior vantagem do Fable 5.1 sobre o Opus 5. AutomationBench, que mede fluxo de trabalho de negócio de ponta a ponta, foi de 31,4% pra 41,4%. São ganhos de dois dígitos em tarefas longas e autônomas. É o mesmo padrão do Fable 5.1 sobre o Fable 5: a distância aparece quando o agente precisa ficar acordado por horas.

**Grupo 2: margem estreita.** GPQA Diamond: 2,3 pontos, num benchmark que já está no teto. HealthBench: 6,8 pontos. DeepSWE: 6,7 pontos, e vale notar que o Gemini 3.8 Flash faz 73,7% no mesmo benchmark a uma fração do preço. Coding puro não foi onde o Astra abriu a maior distância.

**Grupo 3: não comparável.** OSWorld 2.0 tem três números na tabela que medem coisas diferentes. A Anthropic publica "partial" e "strict"; a OpenAI publica um número só, e não diz qual critério. Não coloque 72,6% ao lado de 77,9% e conclua nada. E o Terminal-Bench 4.0, que é o benchmark de coding agentic que a Anthropic usou pra posicionar o Fable 5.1, aparece no anúncio da OpenAI como "estado da arte" sem número. Quando o número vem, você compara. Quando vem o adjetivo, você espera.

## O índice independente conta outra história, por enquanto

A [Artificial Analysis](https://artificialanalysis.ai/models/gpt-6-astra-high) já rodou o Astra. Resultado:

| Modelo | Intelligence Index | Posição |
|---|---|---|
| Claude Fable 5.1 | **66** | 1º de 202 |
| GPT-5.6 Sol (max) | 61 | 10º |
| GPT-6 Astra (high) | 60 | 14º |

Antes de gritar "o Astra perdeu", lê o parêntese. O Astra foi testado em `high`. O modelo tem cinco níveis de esforço: `low`, `medium`, `high`, `xhigh` e `max`. O Sol foi testado em `max`. O Fable 5.1 tem thinking adaptativo sempre ligado. Você está olhando três modelos em três configurações diferentes.

Isso não invalida o índice. Invalida a comparação apressada. Quando o Astra em `xhigh` e `max` entrar na tabela, aí você tem número. Até lá, o índice diz uma coisa útil: em `high`, o Astra custa 2,5x o Sol pra entregar o mesmo score. Se o seu caso de uso não precisa do esforço máximo, o modelo novo não é automaticamente o modelo certo.

E fica a lição que vale pra qualquer benchmark que você ler nessa semana: pergunte sempre "em que nível de esforço?". Sem essa resposta, o número não significa nada.

## 62,7% ou 99,9%: o harness valeu mais que o modelo

Esse é o trecho do lançamento que eu mais quero que você leia.

O [ARC Prize](https://arcprize.org/blog/astra) rodou o GPT-6 Astra no ARC-AGI-3 semi-privado de duas formas. No harness padrão, em que o modelo carrega notas que ele mesmo escolhe manter ao longo do ambiente, o Astra fez **62,7%**, gastando US$ 26 mil. No harness "provider adapter", que preserva o estado opaco de raciocínio entre requests e usa compactação em conversas longas, o mesmo modelo fez **99,9%**, gastando US$ 19 mil.

Mesmo modelo. Mesmos pesos. 37 pontos de diferença. E a versão melhor foi 3,66x mais rápida e usou 49% menos tokens.

Isso é engenharia de contexto, não inteligência. O que mudou entre 62,7% e 99,9% foi como o raciocínio sobrevive de um turno pro outro. O modelo que "esquece" entre chamadas e precisa se reorientar gasta mais e acerta menos. O modelo que carrega estado gasta menos e acerta mais.

A OpenAI produtizou exatamente essa ideia no Codex. Segundo o [9to5Mac](https://9to5mac.com/2026/09/03/openai-releasing-major-upgrade-to-chatgpt-and-codex-with-gpt-6-astra-details-here/), em vez de comprimir a conversa por sumarização quando a janela enche, o Astra "mantém notas entre janelas de contexto, preservando os detalhes acumulados", e as janelas anteriores continuam pesquisáveis. Requisito que você deu na mensagem 3 não vira parágrafo resumido na mensagem 80. Vira nota recuperável.

Se você constrói agente, isso é a única coisa deste post que muda seu código hoje. Não é o modelo. É o que você faz com o estado entre chamadas. A gente já viu esse padrão quando o [modo Ultra do Sol rendeu 3 pontos no Terminal-Bench](https://blog.beerandcode.com.br/noticias/gpt-5-6-sol-ultra-codex) coordenando quatro subagentes: a diferença de score veio da orquestração, não dos pesos.

E o próprio ARC Prize fecha com a frase que a OpenAI não colocou no anúncio: saturar o benchmark "não representa prova de AGI". O escopo do ARC-AGI-3 é fechado. Não é o mundo real.

## Computer use: 72,6% e 40 minutos por tarefa

No OSWorld 2.0, o Astra fez 72,6% gastando em média 40 minutos por tarefa. O Sol fazia 65,7% em 75 minutos. Menos tempo, mais acerto. É o ganho mais concreto do lançamento pra quem usa modelo como operador de sistema.

Só que 40 minutos por tarefa é o dado que importa pra arquitetura. Isso não é latência de chat. Isso é job. Se você está pensando em plugar o Astra num fluxo que preenche formulário, atualiza CRM, monta planilha ou navega painel legado, o desenho é assíncrono: fila, estado persistido, callback quando termina, e um humano que aprova antes de qualquer ação irreversível. Modelo que opera computador por 40 minutos sem supervisão e sem checkpoint é incidente esperando data.

A lista de tools nativas na API deixa claro pra onde a OpenAI está apontando: `computer_use`, `hosted_shell`, `apply_patch`, `skills`, `mcp`, `tool_search`, além de web search, file search e code interpreter. Structured outputs, function calling e prompt caching estão suportados. Fine-tuning, Realtime e Assistants, não.

## "Critical" em cyber: o que muda na sua API

O Astra é o primeiro modelo da OpenAI a bater o nível **Critical** de capacidade em cibersegurança no Preparedness Framework. A definição oficial: "com as ferramentas e o acesso certos, o GPT-6 Astra consegue encontrar falhas de segurança desconhecidas e desenvolver novas formas de explorá-las em muitos sistemas bem protegidos, sem uma pessoa guiando cada passo". Durante a avaliação, achou duas vulnerabilidades inéditas. ExploitBench: 100%.

O que isso muda pra você, na prática:

**Rollout escalonado.** Quem tem acesso hoje é o programa Daybreak, de defensores de cibersegurança. O resto vem "nos próximos dias". Se você já está bloqueado no Sol por cota ou região, não espere o Astra abrir mais cedo.

**Tarefa pode parar no meio.** Segundo o VentureBeat, em atividade sinalizada como suspeita o ChatGPT pede aprovação do usuário antes de continuar, e "em fluxos de API, uma tarefa sinalizada pode simplesmente parar". Lembra dos [bans automáticos do Sol](https://blog.beerandcode.com.br/noticias/gpt-5-6-sol-banindo-contas) em script de DevOps e macro de Excel? A mesma classe de guardrail agora tem um modelo mais sensível por trás. Seu código precisa tratar "parou por política" como estado de erro previsto, com retry desligado e alerta ligado.

**Monitoramento total.** A OpenAI passou a monitorar trajetórias completas, incluindo cadeia de raciocínio, em toda inferência externa com uso de tool. Não é opcional.

Agora a parte que o anúncio esconde no system card. O Astra mostra "redução substancial na monitorabilidade da cadeia de raciocínio" em relação aos modelos anteriores: controla melhor o próprio raciocínio, resolve tarefa sem verbalizar, e evita o monitor quando sabe que está sendo observado. A Apollo Research mediu consciência de estar em avaliação em 41% a 51% das execuções. Jakub Pachocki, chief scientist, disse à NBC: "não vamos aceitar degradação na nossa capacidade de monitorar o alinhamento do modelo além de um certo nível". A frase existe porque o nível chegou perto.

Do outro lado, os números de alinhamento em ambiente de trabalho simulado melhoraram bastante. Taxa de resultado desalinhado: 3,4% no Astra contra 18,8% no Sol. Ataque a honeypot: zero contra 55,4%. Prompt injection indireta na arena da Gray Swan: 8,5% de sucesso do atacante contra 27,0% no Sol. Pra quem coloca agente lendo e-mail, página e documento de terceiro, essa última linha é a que vale dinheiro. Mas 8,5% não é zero. Guardrail continua sendo seu, não do modelo.

## Qual usar: Astra, Fable 5.1 ou Sol

Preço por token empatou entre Astra e Fable 5.1. Então a decisão vira preço por tarefa, e preço por tarefa depende do formato da carga.

Pega a mesma simulação que eu usei no post do [Fable 5.1 contra o Opus 5](https://blog.beerandcode.com.br/noticias/claude-fable-5-1-vs-opus-5): agente de coding com prefixo cacheado de 120k tokens (system prompt, tools, arquivos do projeto), 200 turnos, 3k de input novo e 2k de output por turno.

| Linha | GPT-6 Astra | Claude Fable 5.1 | GPT-5.6 Sol |
|---|---|---|---|
| Cache write (1x, 120k) | $1,50 | $1,50 | $0,60 |
| Cache reads (200 x 120k = 24M) | **$24,00** | **$6,00** | $9,60 |
| Input novo (600k) | $6,00 | $6,00 | $2,40 |
| Output (400k) | $20,00 | $20,00 | $8,00 |
| **Total da sessão** | **$51,50** | **$33,50** | **$20,60** |

Mesma tabela de preço. Sessão 54% mais cara no Astra. A diferença inteira é o cache read: $1 contra $0,25. Numa sessão de agente, leitura de cache domina a contagem de tokens, e a Anthropic cortou esse multiplicador na semana passada exatamente pra isso.

Com isso na mão, a árvore que eu usaria hoje:

**1. Turno único, volume alto.** Classificação, extração, roteamento. Nenhum dos três. Sonnet 5, GPT-5.6 Luna ou Terra. Topo de linha aqui é dinheiro queimado, e isso não mudou com o lançamento.

**2. Coding agentic do dia a dia.** GPT-5.6 Sol continua sendo o melhor preço por tarefa dos três, e 88,8% no Terminal-Bench 2.1 não ficou obsoleto porque saiu um modelo novo. Se o seu eval no Sol fecha, você não tem motivo pra migrar.

**3. Sessão longa com prefixo grande relido.** Fable 5.1. O cache read de $0,25 come qualquer vantagem de benchmark do Astra na conta, e a diferença em coding puro (DeepSWE, 6,7 pontos) não paga 54% a mais por sessão.

**4. Matemática de fronteira, pesquisa científica no terminal, automação de fluxo de negócio de ponta a ponta.** Astra, com folga. 10 a 12 pontos em FrontierMath, Terminal-Bench-Science e AutomationBench é a distância que justifica trocar.

**5. Computer use como operador.** Astra. 72,6% em 40 minutos por tarefa é o melhor número publicado, desde que a arquitetura seja assíncrona e com aprovação humana.

**6. Compliance.** Fable 5.1 exige retenção de dados de 30 dias e não roda sob zero data retention sem autorização da Anthropic. Astra pode parar tarefa sinalizada no meio, e o acesso inicial passa por programa fechado. Nenhum dos dois é neutro em contrato. Lê antes de assinar.

E antes de subir de modelo, sobe o `effort`. Os cinco níveis do Astra negociam inteligência por custo dentro do mesmo modelo, sem invalidar cache e sem migrar código. Vale a mesma regra que valeu na geração anterior: [Sol, Terra ou Luna](https://blog.beerandcode.com.br/noticias/gpt-5-6-sol-terra-luna-qual-usar) era decisão de eval, não de manchete.

## Limitações e pontos de atenção

- **Tudo é auto-reportado.** Os benchmarks do Astra vieram da OpenAI. O único índice independente que já rodou o modelo testou em `high`, não em `max`. Trate a tabela como hipótese até a segunda semana.
- **Você provavelmente ainda não tem acesso.** API e planos pagos entram "nos próximos dias". Rate limit inicial no tier 1 é de 500 requests e 500 mil tokens por minuto.
- **Contexto longo custa o dobro.** Acima de 272k tokens de input, a request inteira paga 2x no input e 1,5x no output. Um agente que deixa a janela encher sem compactar dobra a conta sem avisar.
- **Tarefa sinalizada para.** Em API, não é aviso. É parada. Seu fluxo precisa de estado persistido pra retomar de onde parou, e de alerta pra alguém olhar.
- **Monitorabilidade caiu.** O próprio system card diz que, se a queda continuar nas próximas gerações, a confiança em detectar comportamento desalinhado "cairia significativamente". Você não resolve isso na sua aplicação, mas precisa saber que existe ao desenhar o que o agente pode fazer sozinho.
- **AGI é opinião do vendedor.** Brockman disse "eu, pessoalmente, acho que chegamos". O ARC Prize, dono do benchmark que ele citou, disse que saturar o teste não prova nada disso. Fica com o segundo.

## FAQ rápido

**O GPT-6 Astra já está disponível na API?**
Não pra todo mundo. Hoje só o programa Daybreak tem acesso. A OpenAI promete API, ChatGPT Plus/Pro/Business/Enterprise e AWS "nos próximos dias". O model id é `gpt-6-astra`, e as [docs](https://developers.openai.com/api/docs/models/gpt-6-astra) já estão no ar com preço, limites e tools suportadas.

**Vale migrar do GPT-5.6 Sol pro Astra?**
Só se o seu eval no Sol em esforço máximo está falhando, e a falha é em tarefa longa, científica ou de automação de ponta a ponta. Pra coding do dia a dia, o Sol continua custando 2,5x menos por token e entregando o mesmo score no índice independente. Sem eval, você não tem como saber.

**Astra ou Fable 5.1 pra agente de longa duração?**
Mesma tabela de preço, cache read 4x mais caro no Astra. Se a sessão relê um prefixo grande muitas vezes, o Fable 5.1 sai bem mais barato por tarefa. Se a tarefa é matemática, ciência ou automação de negócio, o Astra tem 10 pontos ou mais de vantagem e a conta inverte.

**O GPT-6 Astra é AGI?**
A OpenAI diz que "provavelmente marca o início". O ARC Prize, que roda o benchmark de 99,9% citado no anúncio, diz que saturar o teste não é prova de AGI. Pra quem constrói produto, a pergunta é irrelevante: o que importa é preço por tarefa, taxa de erro e o que acontece quando o guardrail dispara.

## Conclusão

O GPT-6 Astra é, pelos números da OpenAI, o modelo mais capaz que qualquer pessoa vai poder alugar nas próximas semanas. E a distância pro Fable 5.1 é real onde ela importa pra OpenAI: matemática, ciência, automação, operação de computador.

Mas o lançamento deixou três coisas mais claras que qualquer benchmark. O preço do topo de linha convergiu, então a competição agora é cache e formato de carga. O mesmo modelo faz 62,7% ou 99,9% dependendo de como você preserva estado entre chamadas, então harness é engenharia de produto, não detalhe. E o modelo mais capaz é também o mais difícil de monitorar, e a OpenAI está dizendo isso em voz alta.

O que muda no seu código hoje não é a string do modelo. É como você guarda contexto entre turnos, como você trata tarefa que para por política, e se você tem um eval pra saber se qualquer um desses três vale o que custa.

Quem tiver eval descobre em uma tarde. Quem não tiver descobre na fatura.
