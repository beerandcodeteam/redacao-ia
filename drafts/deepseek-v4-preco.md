O [open source já chegou no topo em código](https://blog.beerandcode.com.br/noticias/glm-5-2-open-source-melhor-codigo). A DeepSeek V4-Pro empata com modelo de fronteira em benchmark de engenharia, roda com 1 milhão de tokens de contexto e custa centavos por milhão de tokens. Esse jogo já estava ganho.

A novidade não é o modelo. É a conta de luz.

A DeepSeek anunciou que a versão oficial da V4 vai cobrar com **preço dinâmico por horário** — barato fora do pico, caro no pico. Igual tarifa de energia: madrugada é vale, horário comercial é ponta. É a primeira vez que um lab grande de IA leva o modelo peak/valley pra API de um modelo open source de ponta.

E pra dev brasileiro tem uma pegadinha de fuso que muda tudo. Vou chegar nela.

## O que já está confirmado (e o que ainda é rumor)

Antes de te vender certeza, deixa eu separar o que dá pra checar do que é boato de timeline.

**Confirmado** — a V4 já existe. Ela saiu em preview no fim de abril de 2026, com pesos abertos sob licença MIT no Hugging Face e disponível via API e em provedores como o OpenRouter. A configuração é absurda:

- **DeepSeek V4-Pro**: arquitetura MoE (Mixture-of-Experts) com **1,6 trilhão de parâmetros totais** e ~49 bilhões ativos por token.
- **Contexto de 1 milhão de tokens**, saída máxima de 384K.
- **80,6% no SWE-bench Verified** na configuração mais forte — empatando com o topo dos modelos de pesos abertos e brigando com Gemini 3.1 Pro.
- Preço de tabela hoje: ~US$ 0,44 por milhão de tokens de entrada e **US$ 0,87 por milhão de saída**.

Isso não é hype. É um modelo que você baixa, roda e mede.

**Rumor** — a data. A versão "oficial" (estável) com o esquema peak/valley está prevista pra **meados de julho de 2026**, segundo flashes de mercado e relatos de usuários da API que receberam e-mail de ajuste de preço. Isso ainda não tem changelog oficial fechado. Então trate a data como provável, não como cravada.

Esse post é vivo: quando o anúncio oficial sair, a tabela de preço e a data entram aqui confirmadas.

## Como funciona o preço peak/valley

A ideia é a mesma da sua conta de energia. Demanda concentrada num horário deixa o serviço caro e instável. Então você cobra mais nesse horário pra empurrar a carga que não tem pressa pra fora do pico.

No anúncio da DeepSeek, o desenho é:

- **Horário de pico**: 9h–12h e 14h–18h no horário de Pequim. Nesses blocos, o preço **dobra**.
- **Fora do pico (vale)**: o preço atual, sem alteração.

Em números, pra V4-Pro no pico:

```text
                       fora do pico (vale)   →   pico (2x)
input cache-hit        ~US$ 0,004 / 1M           ~US$ 0,007 / 1M
input cache-miss       ~US$ 0,44  / 1M           ~US$ 0,85  / 1M
output                 ~US$ 0,87  / 1M           ~US$ 1,70  / 1M
```

A V4-Flash, mais barata e rápida, segue a mesma lógica de dobrar no pico. Ou seja: rodar um agente pesado às 10h da manhã em Pequim sai literalmente o dobro de rodar o mesmo job às 3h da manhã.

Faz sentido pra DeepSeek? Faz. Inferência de modelo de 1,6T não é de graça — alguém paga GPU, energia e refrigeração. Espalhar a demanda no relógio é engenharia de capacidade, não maldade. O que muda pra você é que **o relógio agora entra na sua conta de custo**.

## A pegadinha de fuso que joga a favor do dev BR

Aqui está a parte que ninguém te conta.

O pico é ancorado em **horário de Pequim**. Pequim está em UTC+8. Brasília está em UTC−3. São 11 horas de diferença.

Faz a conta do que acontece com o relógio:

- Pico chinês 9h–12h  →  **22h–01h** em Brasília (da noite anterior).
- Pico chinês 14h–18h  →  **03h–07h** em Brasília.

Ou seja: **o horário caro da DeepSeek cai exatamente na madrugada brasileira.** E o seu dia útil — 8h às 21h no Brasil — corresponde à noite e madrugada chinesa, que é tudo **vale**.

Deixa isso assentar. Enquanto o dev de Pequim paga o dobro no meio do expediente dele, você, codando das 9h às 18h de Brasília, está rodando no preço de vale o tempo inteiro. De graça, sem mexer em nada.

O gancho "barato de madrugada, caro no pico" é verdade pra quem mora na China. No Brasil, a relação **inverte**: a sua madrugada é que é o horário caro. Se você tem batch noturno, job agendado, pipeline de embeddings rodando às 3h da manhã — é justo aí que o preço dobra pra você. Vale conferir o cron.

## A conta de verdade: V4-Pro vs Claude Opus 4.8

Peak/valley é uma variação de 2x dentro da DeepSeek. Parece muito até você comparar com um modelo de fronteira.

O Claude Opus 4.8 — o Opus mais capaz da Anthropic, com 1M de contexto a preço padrão — custa **US$ 5 por milhão de tokens de entrada e US$ 25 por milhão de saída**. É um modelo excelente, provavelmente mais forte em raciocínio longo e trabalho agêntico de horizonte longo. Mas o preço é outro planeta.

Coloca lado a lado, por milhão de tokens de saída:

```text
V4-Pro (vale)     ~US$ 0,87
V4-Pro (pico)     ~US$ 1,70
Opus 4.8          ~US$ 25,00
```

Mesmo no pico, a V4-Pro sai cerca de **14x mais barata** que o Opus 4.8 na saída. No vale, passa de **28x**. Na entrada a distância é parecida: ~US$ 0,85 no pico da V4 contra US$ 5 do Opus.

Sacou a ironia? A oscilação peak/valley que a DeepSeek introduziu — esse "muda a conta do open source" — é ruído perto do abismo que separa open source barato de frontier caro. O horário do dia faz seu custo variar 2x. A escolha entre V4-Pro e Opus 4.8 faz variar 15 a 30x.

Isso não quer dizer "troca tudo pra DeepSeek e pronto". Quer dizer que a decisão real continua sendo a de sempre: **[qual modelo pra qual tarefa](https://blog.beerandcode.com.br/noticias/claude-opus-4-8-vs-minimax-m3-vs-qwen-3-local).** Tarefa de raciocínio pesado, agente autônomo de horizonte longo, código onde errar custa caro? Talvez valha o Opus. Volume alto, classificação, extração, sumarização, draft de código que você revisa? A V4-Pro derruba seu custo em uma ordem de grandeza e ainda te dá 1M de contexto.

Peak/valley só adiciona uma terceira pergunta no fim: **quando** o job roda. E pro dev BR, essa terceira pergunta já vem quase resolvida pelo fuso.

## O que fazer com isso na prática

Três movimentos concretos, sem firula:

1. **Mapeie suas tarefas por criticidade, não por moda.** Faça uma tabelinha: tarefa → modelo → custo estimado. Onde a V4-Pro entrega resultado bom o suficiente, o ganho de custo é absurdo. Onde você precisa do teto de raciocínio, paga o Opus e segue a vida.

2. **Olhe o seu cron antes de julho.** Se você tem batch noturno rodando entre 22h e 7h de Brasília contra a API da DeepSeek, esse é o horário que vai ficar caro quando o peak/valley entrar. Mover o job pro horário comercial brasileiro — que é vale chinês — pode cortar custo sem trocar uma linha de modelo.

3. **Trate o preço como variável de arquitetura, não detalhe de billing.** Custo por token agora tem dimensão de tempo. Isso muda como você projeta fila, retry e agendamento de inferência. Não é nota de rodapé da fatura — é decisão de engenharia.

A verdade incômoda é que escolher modelo virou um problema de otimização com três eixos: capacidade, custo e agora horário. Quem trata isso como engenharia — medindo, comparando, projetando o fluxo — paga uma fração do que paga quem joga tudo no modelo mais caro "por garantia".

E é exatamente esse tipo de decisão — qual modelo, qual custo, como o fluxo se encaixa num produto que precisa funcionar e fechar a conta — que a gente vai construir do zero, ao vivo, no [Do prompt ao harness: construindo um agent de vendas](https://beerandcode.com.br/landing-pages/do-prompt-ao-harness-construindo-um-agent-de-vendas), dois dias montando um agente de vendas plugado num e-commerce de ponta a ponta.

O open source ganhou o jogo do preço. A DeepSeek agora quer que você jogue contra o relógio também. Pra quem codifica no Brasil, o relógio já está do seu lado — desde que você saiba que ele está lá.
