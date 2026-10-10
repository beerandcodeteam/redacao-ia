O **Muse Code** da Meta entrou na briga de agente de terminal. E entrou pelo preço.

No dia 5 de agosto de 2026, o Meta Superintelligence Labs soltou o Muse Code em beta: o agente de terminal da Meta rodando o modelo **Muse Spark 1.2**, feito pra atacar exatamente o território do Claude Code e do Codex. Instala com um `curl`, roda em macOS e Linux, e não tem GUI nem extensão de IDE. É terminal puro.

O número que rodou o Twitter foi o Terminal-Bench: 82,9%. Acima do GPT-5.6 Terra. E o preço do tier "contributor" — US$ 0,10 por milhão de tokens de entrada e US$ 0,20 de saída — que deixa o Muse Spark 1.2 até 20x mais barato que a concorrência.

Só que essas duas frases escondem coisa. Vamos abrir as duas.

## TL;DR

- **O que é:** Muse Code, agente de terminal da Meta em beta, rodando o modelo proprietário Muse Spark 1.2.
- **Stack/Modelos:** Muse Spark 1.2 (closed-weight), 1 milhão de tokens de contexto, sub-agentes em git worktrees isolados, event log append-only.
- **Custo/Acesso:** Tier padrão US$ 1,25/M entrada e US$ 4,25/M saída. Tier contributor US$ 0,10/M entrada e US$ 0,20/M saída — com a Meta treinando modelo em cima do seu código.
- **O benchmark:** 82,9% no Terminal-Bench 2.1. Ganhou do GPT-5.6 Terra (81,8%). Perdeu do Claude Opus 5 (86,7%) nos três benchmarks que a própria Meta escolheu mostrar.
- **Link útil:** [dev.meta.ai](https://dev.meta.ai)

## O contexto: por que a Meta precisava do Muse Code

Até essa semana, a disputa de agente de terminal era Anthropic contra OpenAI. Claude Code de um lado, Codex do outro. A Meta estava fora — e não por falta de dinheiro.

O Muse Code é a primeira tentativa séria de mudar isso, e vem com uma mudança de postura que merece atenção: **o Muse Spark é closed-weight**. Não tem peso no Hugging Face, não tem licença permissiva, não tem "abra e rode local". Depois de anos construindo reputação em cima do Llama aberto, a Meta lançou o modelo de código dela fechado. O Zuckerberg deixou a porta aberta pra abrir depois, mas hoje não é aberto.

A escolha faz sentido quando você olha o produto. O Muse Code não é um chat que cospe função. Ele foi desenhado pro tipo de tarefa que quebra a maioria das ferramentas: repositório grande, mudança em vários arquivos, trabalho que leva horas em vez de segundos. A Meta mostrou um caso de otimização de kernel em GPU Hopper da NVIDIA com mais de mil chamadas de ferramenta ao longo de até 24 horas.

Esse é o ponto que interessa pra quem constrói: a briga saiu de "qual modelo escreve a função mais bonita" e virou "qual harness aguenta rodar 24 horas sem se perder". É problema de engenharia, não de modelo.

E aí mora a parte chata. Toda semana aparece um agente novo prometendo substituir o anterior, e testar cada um em repositório de verdade é o trabalho que ninguém tem tempo de fazer sozinho — é exatamente o que a gente faz junto, ao vivo, toda semana no [Clã Beer and Code](https://beerandcode.com.br?utm_source=blog&utm_medium=post&utm_campaign=muse-code-meta-terminal-bench&utm_content=c-n1). É pago, é assinatura, e é o ambiente que este post descreve.

## O benchmark do Muse Code: a Meta bateu o Codex, mas qual Codex?

Aqui a manchete precisa de cirurgia.

O gráfico que a Meta apresentou no lançamento tem estes números no **Terminal-Bench 2.1** (89 tarefas, pass@1 sobre cinco tentativas):

| Modelo | Terminal-Bench 2.1 |
|---|---|
| Claude Opus 5 | 86,7% |
| **Muse Spark 1.2** | **82,9%** |
| GPT-5.6 Terra | 81,8% |
| Grok 4.5 | 81,6% |

Sim, o Muse Spark 1.2 ficou acima de um modelo da OpenAI. Ficou 1,1 ponto acima do **GPT-5.6 Terra**.

O problema: **o Codex não roda o Terra.** Desde que o GPT-5.6 ficou disponível de forma geral, em 9 de julho de 2026, o Codex tem como padrão o **GPT-5.6 Sol** — que no [leaderboard independente da Artificial Analysis](https://artificialanalysis.ai/evaluations/terminalbench-v2-1) marca 89,5% no mesmo Terminal-Bench v2.1, o topo da tabela. O Claude Opus 5 em esforço máximo aparece logo atrás, com 89,1%.

Ou seja: a Meta escolheu comparar com o modelo do meio da linha da OpenAI, não com o que o produto concorrente realmente usa. O [The Register notou a mesma coisa](https://www.theregister.com/ai-and-ml/2026/08/06/meta-wants-to-get-inside-your-terminal-with-its-new-coding-agent/5283717) e descreveu o gráfico do Zuckerberg como "vago", com pontuações apertadas onde o Muse Spark aparece competitivo mas nunca em primeiro.

E não para no Terminal-Bench. Nos outros dois benchmarks do próprio anúncio:

| Benchmark | Muse Spark 1.2 | Claude Opus 5 |
|---|---|---|
| DeepSWE 1.1 | 59,3% | 65,0% |
| Meta Internal Coding Bench | 70,6% | 79,4% |

Leia de novo a segunda linha. **No benchmark interno da Meta — 440 tarefas tiradas de pull requests reais, construído pela Meta, escolhido pela Meta pra entrar no slide — o Claude Opus 5 ganhou por quase 9 pontos.**

Isso é honestidade ou é falta de opção? Provavelmente as duas. Mas é um dado que a maioria das manchetes não carregou.

Vale registrar também a divergência entre as medições: a Meta coloca o Opus 5 em 86,7% no Terminal-Bench, a Artificial Analysis coloca em 89,1%. Configuração de esforço, harness, número de tentativas — tudo isso muda o número. É o mesmo padrão que a gente já viu no [DeepSeek V4 Flash 0731, que marcou 82,7 no gráfico do vendor e 79% na medição independente](https://blog.beerandcode.com.br/noticias/deepseek-v4-flash-0731). Benchmark de vendor é material de marketing com metodologia anexa. Trate como tal.

O que sobra de verdade: o Muse Spark 1.2 subiu 6,7 pontos sobre o 1.1 (que marcava 76,2%) no Terminal-Bench e 6,3 no DeepSWE. **Esse salto entre versões é real e é rápido.** A Meta chegou atrasada, mas não chegou perdida.

## A arquitetura: onde o Muse Code é genuinamente diferente

Se o modelo é o segundo ou terceiro melhor, por que olhar? Porque o harness tem decisões de engenharia que valem estudo mesmo que você nunca instale a ferramenta.

**Sub-agentes em worktrees isolados.** Quando a tarefa é grande, o Muse Code abre sub-agentes em git worktrees separados. Nas palavras do Zuckerberg: *"When a job is big enough, it fans out to separate sub-agents working in parallel in isolated worktrees."* Na demonstração, seis features de um jogo construídas ao mesmo tempo, sem colisão e sem tocar na sua working copy. Quem já tentou rodar dois agentes no mesmo checkout sabe exatamente que dor isso resolve.

**Background agents persistentes.** Em vez de nascer e morrer por tarefa, os sub-agentes ficam vivos durante a sessão inteira. Isso muda o custo de coordenação: o agente não reconstrói contexto do zero a cada delegação.

**Event log append-only.** Essa é a melhor parte. O Muse Code grava localmente um log append-only de tudo: chamada de modelo, execução de ferramenta, aprovação, edição. O runtime é descrito como *replay-exact* e *restart-safe* — se o processo morrer no meio de uma tarefa de 24 horas, ele retoma de onde parou em vez de recomeçar.

Isso não é firula. É a diferença entre um agente de demo e um agente que você deixa rodando de verdade. Se você constrói agente próprio e ainda não tem event log, esse é o item pra copiar do Muse Code — independente de qual modelo você usa por baixo. Já falamos aqui sobre [agentes que deixam estado entre execuções](https://blog.beerandcode.com.br/noticias/agente-ia-estado-entre-execucoes); o event log é a versão disciplinada disso.

Além disso, o Muse Code vem com skills padrão — `/plan`, `/grill` e `/goal` — no mesmo espírito de slash command que o Claude Code popularizou.

## US$ 0,30 por milhão: o que você está pagando de verdade

Agora o preço, que é a real arma do lançamento.

```
Tier padrão
  entrada:         US$ 1,25 / 1M tokens
  entrada cacheada: US$ 0,15 / 1M tokens
  saída:           US$ 4,25 / 1M tokens

Tier contributor
  entrada:         US$ 0,10 / 1M tokens
  entrada cacheada: US$ 0,002 / 1M tokens
  saída:           US$ 0,20 / 1M tokens
```

Some entrada e saída do contributor e você chega nos famosos **US$ 0,30 por milhão de tokens**. É 12,5x mais barato na entrada e 21x mais barato na saída que o tier padrão. Na entrada cacheada a diferença é de 75x.

O Alexandr Wang, chefe de IA da Meta, vendeu exatamente isso: a ferramenta "pode ser uma opção incrivelmente boa, especialmente do ponto de vista de custo".

E o que a Meta pede em troca? Que ela possa usar seus prompts e completions pra treinar os modelos dela.

Pausa aqui, porque isso merece mais do que um encolher de ombros.

Um agente de terminal não lê "prompts". Ele lê **repositório**. Pra funcionar, o Muse Code precisa carregar seu código-fonte, sua estrutura de pastas, seus schemas de banco, suas regras de negócio, seus comentários internos, suas mensagens de commit — e, se você for descuidado, seus `.env` e suas chaves. Com 1 milhão de tokens de contexto, cabe muita coisa.

Então o cálculo do tier contributor não é "quanto eu economizo por mês". É **"quanto vale a propriedade intelectual do meu código como material de treino"**. E essa conta não é do time financeiro. É do time de segurança, do jurídico e — se você presta serviço — do seu cliente, que provavelmente tem cláusula de confidencialidade dizendo algo sobre isso.

Pra projeto pessoal, código open-source ou protótipo descartável? US$ 0,30 por milhão é um preço absurdamente bom e eu rodaria sem pensar duas vezes. Pra o monólito da empresa que paga seu salário? Você não tem autoridade pra aceitar esses termos sozinho.

O desconto não é generosidade. É o valor que a Meta atribui ao dado — e ela provavelmente está pagando barato.

## Limitações e pontos de atenção

**Beta, e beta de verdade.** Só macOS e Linux. Sem Windows, sem GUI, sem integração com IDE. Se seu fluxo depende de VS Code ou JetBrains, não existe caminho hoje.

**Modelo fechado.** Sem pesos, sem rodar local, sem auditar. Você depende da API da Meta e do uptime dela. Quem escolheu Llama justamente pela abertura não ganha nada aqui.

**Instalação por `curl | bash`.** O comando divulgado é `curl -fsSL https://dev.meta.ai/install.sh | bash`. Funciona, mas é um script remoto com execução direta no seu shell. Baixe, leia, depois rode. Vale pra qualquer instalador, não só o da Meta.

**Preço do contributor ainda é reportado de segunda mão.** Os valores circularam via comentário público e cobertura de imprensa; a página oficial de pricing é a fonte que vale pra decisão de compra. Confira em `dev.meta.ai` antes de fechar orçamento.

**Demonstração é demonstração.** As mil chamadas de ferramenta em 24 horas otimizando kernel são número do fornecedor, em hardware do fornecedor, em tarefa escolhida pelo fornecedor. Não é validação independente.

## FAQ rápido

**O Muse Code substitui o Claude Code ou o Codex hoje?**
Pelos números, não. O Muse Spark 1.2 perde pro Claude Opus 5 nos três benchmarks do próprio anúncio da Meta, e o Codex roda o GPT-5.6 Sol, que lidera o Terminal-Bench independente. O argumento do Muse Code hoje é custo e arquitetura de longa duração, não capacidade bruta.

**Posso usar o tier contributor em código de cliente?**
Assuma que não até que alguém com autoridade contratual diga que sim. O tier troca desconto por permissão de treinar modelos com o que você enviar, e um agente de terminal envia repositório inteiro. Contrato com cláusula de confidencialidade normalmente proíbe isso.

**Roda local ou offline?**
Não. O Muse Spark é closed-weight e servido por API. Sem pesos públicos, não existe execução local.

**Muse Code vs Claude Code: qual escolher pra repositório grande?**
Se o critério é qualidade de saída, Claude Code — o Opus 5 ganha nos três benchmarks. Se o critério é custo de tarefa longa em código que você pode compartilhar, o Muse Code fica competitivo. E o desempate raramente é o modelo: é o harness que você monta em volta dele.

**Vale a pena testar mesmo assim?**
Vale — em repositório que você não se importa em compartilhar, no tier padrão se o código for sensível. O que vale mais é estudar o desenho: worktrees isolados por sub-agente e event log append-only são padrões que você pode implementar no seu próprio harness hoje.

## O que fica

A Meta não bateu o estado da arte. Ela bateu o GPT-5.6 Terra por 1,1 ponto, perdeu pro Opus 5 em tudo — inclusive no benchmark que ela mesma construiu — e escolheu não comparar com o modelo que o Codex realmente usa. Manchete de "a Meta ganhou" não sobrevive a cinco minutos lendo o gráfico.

Mas duas coisas são reais e importam. O salto de 6,7 pontos entre Muse Spark 1.1 e 1.2 mostra velocidade de iteração. E o tier de US$ 0,30 por milhão coloca uma pressão de preço que Anthropic e OpenAI vão ter que responder de alguma forma.

O próximo movimento previsível é a guerra de preço descer pro tier pago sem troca de dados. Enquanto isso não acontece, o custo real do Muse Code barato continua sendo pago na moeda que a Meta quer: o seu código.

Lê o gráfico antes de trocar de ferramenta. E lê os termos antes de trocar de tier.
