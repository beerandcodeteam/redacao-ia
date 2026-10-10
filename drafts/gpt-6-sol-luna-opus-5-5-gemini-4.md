O GPT-6 Sol e o GPT-6 Luna, da OpenAI, e o Claude Opus 5.5, da Anthropic, saíram no mesmo dia: 22 de setembro, com noventa minutos de diferença. E dois dias depois, o chefe do Google DeepMind subiu num palco pra dizer que o Gemini 4 já está em pós-treino.

Três labs, uma semana. A timeline inteira gritando "modelo novo".

Só que, se você olhar os números com calma, essa rodada tem uma característica que as anteriores não tinham: **quase nada aqui é sobre o modelo ficar mais inteligente. É sobre a mesma inteligência ficar mais barata.** E isso muda a conta de quem roda agente em produção muito mais do que qualquer ponto a mais em benchmark.

Neste post você vai ver o que cada lançamento traz de diferente de verdade, onde está a pegadinha de cada um, o que já se sabe sobre o Gemini 4 e qual modelo faz sentido pra cada tipo de carga.

## TL;DR

- **GPT-6 Sol:** mesma inteligência do GPT-5.6 Sol pela metade do preço ($2/$10 por milhão de tokens), alucinando bem menos.
- **GPT-6 Luna:** o modelo de volume. $0,10/$0,50, mas cai um pouco em código agentic e gasta mais tokens por tarefa.
- **Claude Opus 5.5:** entrega no nível do Fable 5.1 a $4/$20, 30% mais rápido que o Opus 5, com cache read 60% mais barato. Vem com 4 breaking changes na API.
- **Gemini 4:** ainda não saiu. Pré-treino confirmado em julho, pós-treino agora, mercado de previsão apostando em outubro.

## O padrão da rodada: o preço cai, a inteligência fica

Comece pelo dado mais honesto que existe sobre o GPT-6 Sol. Não é o da OpenAI. É o da [Artificial Analysis](https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier), que roda os mesmos testes em todo mundo.

O veredito deles: o Intelligence Index do GPT-6 Sol ficou **no mesmo nível** do GPT-5.6 Sol. O do Luna, no mesmo nível do GPT-5.6 Luna. Com ganhos em algumas avaliações e regressões em outras.

O que mudou foi o custo por tarefa:

| Modelo | Custo por tarefa (Intelligence Index, esforço max) |
|---|---|
| GPT-5.6 Sol | $1,99 |
| **GPT-6 Sol** | **$1,06** |
| GPT-5.6 Luna | $0,18 |
| **GPT-6 Luna** | **$0,07** |

Do lado da Anthropic, a mesma história com outra embalagem. O [Opus 5.5](https://www.anthropic.com/claude-opus-5-5) "performa no nível do Claude Fable 5.1 na maior parte do trabalho" e custa 40% menos que o Opus 5 em cargas típicas.

Ou seja: nenhum dos dois labs te vendeu um salto de capacidade essa semana. Os dois te venderam **a capacidade de ponta de um mês atrás pela metade do preço**.

Parece menos empolgante. Não é.

Agente em produção não morre por falta de inteligência. Morre de custo. Um loop de agente que faz 40 chamadas por tarefa e custava R$ 2 por execução agora pode custar R$ 1. Isso é a diferença entre uma feature que fecha a conta e uma que fica no protótipo.

E o ritmo é esse: toda semana algum lab mexe na tabela de preço, no default de um parâmetro ou num comportamento da API. Acompanhar isso sozinho, com o código de produção na mão, é o que mais cansa. É por isso que no [Clã Beer and Code](https://beerandcode.com.br?utm_source=blog&utm_medium=post&utm_campaign=gpt-6-sol-luna-opus-5-5-gemini-4&utm_content=c-n1) a gente pega lançamento como esse e testa junto, toda semana, ao vivo, em projeto real.

## GPT-6 Sol e Luna: a mudança que importa é a alucinação

A [OpenAI](https://openai.com/index/introducing-gpt-6-sol-and-luna/) posiciona os dois assim: o Sol é o modelo do dia a dia, com mais raciocínio, e o Luna é o barato, otimizado pra resposta rápida e volume alto. Segundo a [TechCrunch](https://techcrunch.com/2026/09/22/openai-launches-gpt-6-sol-and-luna/), o Luna mira "tarefas de alto volume com objetivo claro, como resumir documentos, extrair informação ou responder perguntas rápidas".

Os preços, com o antes e depois ([MacRumors](https://www.macrumors.com/2026/09/22/openai-gpt-6-sol-luna/)):

| Modelo | Input (1M tokens) | Output (1M tokens) |
|---|---|---|
| GPT-5.6 Sol | $4 | $20 |
| **GPT-6 Sol** | **$2** | **$10** |
| GPT-5.6 Luna | $0,20 | $1,20 |
| **GPT-6 Luna** | **$0,10** | **$0,50** |

A OpenAI atribui o corte a "melhorias em caching e inferência". Não é promoção. É eficiência de infraestrutura.

Agora, o dado que eu mais gostei dessa rodada: **alucinação**.

No AA-Omniscience, teste que mede quanto o modelo inventa resposta em vez de admitir que não sabe, a taxa de alucinação do Sol caiu de **92% para 60%**. A do Luna, de **93% para 77%** ([Artificial Analysis](https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier)). A própria OpenAI diz que o Sol comete "cerca de metade dos erros" do GPT-5.6 Sol, chegando na confiabilidade do Astra.

60% ainda é alto. Mas a queda é enorme, e ela bate direto em RAG, extração e qualquer fluxo onde o modelo responde sobre dado que ele não tem.

Tem também uma mudança de estilo herdada do Astra: respostas um pouco mais curtas, menos jargão e, segundo a OpenAI, "menos afirmações enganosas sobre o próprio trabalho de código". Quem já pegou agente dizendo "todos os testes passaram" sem ter rodado nada sabe o valor disso.

### A pegadinha do Luna

O Luna é barato por token. Mas olha o que a Artificial Analysis mediu:

- No **Coding Agent Index**, o Luna **caiu 2 pontos** (41). O Sol subiu 2 (57).
- O Luna gastou **51 mil tokens** de output nas tarefas do índice, contra 41 mil do GPT-5.6 Luna.
- Os dois modelos **regrediram no GDPval-AA v2.1** no esforço máximo, porque entregam documentos mais curtos que "com mais frequência omitem elementos obrigatórios".

Tradução: se o seu fluxo com Luna é código agentic ou geração de documento com checklist de conteúdo, não troque no escuro. Rode o seu eval antes. Pra resumo e extração, a troca é quase óbvia.

## Claude Opus 5.5: nível Fable pelo preço de Opus, com quatro breaking changes

O [Opus 5.5](https://www.anthropic.com/claude-opus-5-5) é o primeiro modelo da família 5.5. Model id: `claude-opus-5-5`.

Os números contra o Opus 5, todos do anúncio oficial:

| Benchmark | Opus 5 | Opus 5.5 |
|---|---|---|
| Terminal-Bench 4.0 | 52,3% | **66,4%** |
| CursorBench 4.0 | 46,6% | **57,8%** |
| FrontierCode v1.1 | 48,0% | **54,4%** |
| OSWorld 2.0 | 74,0% | **81,8%** |
| Humanity's Last Exam | 63,6% | **67,7%** |
| GDPval-AA v2.1 (Elo) | 1708 | **1846** |

Catorze pontos no Terminal-Bench numa versão ponto-cinco não é pouca coisa. E a Artificial Analysis colocou o Opus 5.5 no topo do Intelligence Index, com 58 pontos.

Mas o que eu quero que você olhe é o preço:

| | Opus 5 | Opus 5.5 |
|---|---|---|
| Input | $5 | **$4** |
| Output | $25 | **$20** |
| Cache write | $6,25 | **$5** |
| Cache read | $0,50 | **$0,20** |

O cache read caiu 60%. Em sessão agentic, onde o contexto inteiro é relido a cada turno, é essa linha que manda na fatura, não a de input. A gente já fez essa conta no [comparativo do Fable 5.1 com o Opus 5](https://blog.beerandcode.com.br/noticias/claude-fable-5-1-vs-opus-5): com cache quente, a razão de custo entre modelos muda completamente. No Opus 5.5 ela pende forte a favor dele.

A Anthropic ainda compara com o GPT-6 Astra: mesmo nível no FrontierCode a "cerca de 20% do custo por tarefa", e no Terminal-Bench 4.0 a "cerca de 40%". É número do próprio lab, então leia com o desconto de sempre.

E mais: gera output mais de 30% mais rápido que o Opus 5, e na auditoria comportamental tentou contornar limites "cerca de 85% menos vezes" que o Opus 5.

### O que quebra se você só trocar o model id

Aqui mora o problema. O [guia de migração](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide) lista quatro breaking changes:

1. **Thinking não pode ser desligado.** `thinking: {"type": "disabled"}` e `thinking: {"type": "enabled", "budget_tokens": N}` devolvem erro 400. Adaptive thinking roda em toda requisição. O controle agora é só o `effort`.
2. **Forced tool use foi removido.** `tool_choice` com `{"type": "any"}` ou `{"type": "tool", ...}` devolve 400. Use `auto` com strict tool use ou structured outputs.
3. **Thinking blocks ficam presos à conversa.** O API só aceita um thinking block reenviado se tudo que veio antes dele continuar idêntico. Editou um turno anterior, removeu um reminder injetado, reconstruiu o system prompt ou fez compactação no cliente? Erro. Pra contas criadas a partir de 31/08/2026, esse é o comportamento padrão.
4. **Computer use mudou.** Na API e no Google Cloud, o antigo `computer_20251124` é rejeitado. O novo é `computer_toolset_20260801`.

E tem uma mudança silenciosa que não dá erro nenhum, só muda o resultado: **o effort padrão agora é `medium`. No Opus 5 era `high`.** Se você migrar sem setar, vai rodar com menos raciocínio e achar que o modelo piorou.

Antes, no Opus 5, desligando thinking pra economizar:

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=4096,
    thinking={"type": "disabled"},
    messages=[{"role": "user", "content": prompt}],
)
```

Depois, no Opus 5.5:

```python
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,  # agora cobre thinking + texto
    output_config={"effort": "low"},  # thinking sempre ligado; effort é o controle
    messages=[{"role": "user", "content": prompt}],
)

# a resposta começa com blocos de thinking: filtre por tipo
text = "".join(b.text for b in response.content if b.type == "text")
```

Dois detalhes que pegam gente. Primeiro: `max_tokens` agora é o teto de thinking **mais** texto. Se você usava 4096 sem thinking, pode começar a receber resposta cortada. A doc sugere começar em 64k pra `xhigh` e `max`. Segundo: thinking é cobrado como output mesmo quando você não vê o texto dele. Fluxo que rodava sem thinking vai gastar mais output por requisição.

Se você usa Claude Code, dá pra deixar o próprio Claude fazer a migração com `/claude-api migrate this project to claude-opus-5-5`.

Sonnet 5.5 e Haiku 5.5 vêm "nas próximas semanas", segundo a Anthropic.

## Gemini 4: o que já se sabe e a previsão

O Google é o único dos três que não lançou nada essa semana. E ele sabe disso: o último flagship da empresa foi a série Gemini 3, em novembro de 2025.

O que está confirmado, em ordem:

- **21/07/2026:** o Google confirmou publicamente que começou o "pré-treino mais ambicioso até hoje" do Gemini 4, uma confirmação rara feita no meio do treino ([MindStudio](https://www.mindstudio.ai/blog/gemini-4-release-date-rumors)).
- **23/07/2026:** na call de resultados, Sundar Pichai disse que o Gemini 4 vai usar um modelo base "significativamente maior", com código e agentes autônomos como prioridades.
- **Esta semana:** Koray Kavukcuoglu, na primeira aparição pública como chefe do Google DeepMind (AI Agenda Live, da The Information), disse que o Gemini 4 está no começo do pós-treino e que a meta é lançar "muito antes" do fim do ano. Nas palavras dele: "Nossa intenção é soltar uma versão inicial do pós-treino o quanto antes, porque já vimos resultados promissores" ([AI Weekly](https://aiweekly.co/alerts/deepminds-kavukcuoglu-targets-pre-year-end-gemini-4-ship)).

E o que o mercado aposta. No [Polymarket](https://polymarket.com/event/gemini-4pt0-released-by-june-30-2026), a chance do Gemini 4.0 sair até cada data, hoje:

| Até | Probabilidade |
|---|---|
| 30/09/2026 | 2% |
| 31/10/2026 | 75% |
| 30/11/2026 | 92% |

Detalhe importante: esse mercado resolve com o **Gemini 4.0 Flash** disponível ao público, não o Pro.

**Minha leitura.** "Versão inicial do pós-treino o quanto antes" soa como preview, provavelmente um Flash ou um Pro com rótulo experimental, em outubro. Pelas prioridades que o Pichai declarou, o foco vai ser código e agente. É exatamente onde o Opus 5.5 e o GPT-6 Sol acabaram de subir a régua de preço-por-desempenho. Então a pergunta que importa pro Gemini 4 não é "vai ser mais inteligente?". É **"vai ser mais barato por tarefa resolvida que o Opus 5.5?"**. Se não for, chega atrasado.

Isso é previsão, não fato. Trate como tal.

## Qual usar agora

| Carga | Escolha | Por quê |
|---|---|---|
| Agente de código, tarefa longa | **Opus 5.5** | Melhor Terminal-Bench e CursorBench da rodada, cache read barato |
| Resumo, extração, classificação em volume | **GPT-6 Luna** | $0,10/$0,50, alucinação menor que o antecessor |
| Assistente de uso geral, RAG | **GPT-6 Sol** | Metade do preço do 5.6, queda forte de alucinação |
| Já está no GPT-5.6 Sol | **GPT-6 Sol** | Mesmo nível, metade do custo, troca de baixo risco |
| Já está no Opus 5 | **Opus 5.5**, com migração | Mais barato e melhor, mas leia os breaking changes antes |
| Esperando o Gemini 4 | Não espere | Sem data oficial; migre o que der e reavalie em outubro |

## Limitações e pontos de atenção

**Benchmark de lab é benchmark de lab.** Os números do Opus 5.5 são da Anthropic. A frase "supera os modelos da Anthropic" é da OpenAI. Os números independentes que eu usei são da Artificial Analysis, e mesmo eles medem com harness próprio. Terminal-Bench no anúncio da Anthropic e Terminal-Bench na Artificial Analysis não são comparáveis diretamente.

**Mesma inteligência não significa mesmo comportamento.** O Sol e o Luna ficaram mais concisos. Se o seu produto depende de resposta longa e completa, a regressão no GDPval mostra que você pode perder conteúdo. Eval próprio, sempre.

**Nem tudo está em todo lugar.** Na data do lançamento, o GPT-6 Sol e o Luna estavam no ChatGPT Work, no Codex e na API, mas ainda não no Chat mode.

**Previsão do Gemini é aposta.** Kavukcuoglu falou em "intenção", não em data.

## FAQ rápido

**O GPT-6 Sol é melhor que o GPT-6 Astra?**
Não. O Astra continua sendo o topo da OpenAI. O Sol traz as melhorias do Astra pra um preço menor, com confiabilidade parecida em factualidade, mas não é um substituto em capacidade bruta. A comparação completa do Astra está no [nosso comparativo](https://blog.beerandcode.com.br/noticias/gpt-6-astra-vs-fable-5-1-vs-gpt-5-6-sol).

**Posso trocar `claude-opus-5` por `claude-opus-5-5` e pronto?**
Só se você não desliga thinking, não força tool use, não edita o histórico da conversa e não usa computer use. Senão, vai tomar 400. E sete o `effort` explicitamente: o padrão caiu de `high` para `medium`.

**O Opus 5.5 substitui o Fable 5.1?**
Na maior parte do trabalho, segundo a Anthropic, sim, e custando bem menos. Pra tarefa realmente de fronteira, o Fable 5.1 continua sendo o teto. Teste nos seus casos mais difíceis antes de desligar o Fable.

**Quando sai o Gemini 4?**
Não tem data oficial. O Google diz "muito antes do fim do ano", e o Polymarket dá 75% de chance de um Gemini 4.0 Flash público até 31/10.

## Conclusão

Essa rodada não trouxe o modelo que muda tudo. Trouxe algo mais útil: a capacidade de ponta ficou mais barata e mais confiável. O GPT-6 Sol alucina bem menos pela metade do preço. O Opus 5.5 entrega nível Fable a preço de Opus, com um cache que faz agente longo fechar a conta.

O próximo passo dessa corrida não é quem tem o maior número no benchmark. É quem resolve a tarefa pelo menor custo total. O Gemini 4 vai ser julgado por essa régua.

Se você ainda está decidindo entre os modelos de topo, vale ler [a comparação do GPT-6 Astra com o Fable 5.1](https://blog.beerandcode.com.br/noticias/gpt-6-astra-vs-fable-5-1-vs-gpt-5-6-sol) pra ver como o cache muda a conta de uma sessão inteira.
