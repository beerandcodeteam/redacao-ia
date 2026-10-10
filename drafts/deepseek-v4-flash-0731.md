A DeepSeek trocou o motor do carro sem trocar a placa. O DeepSeek V4 Flash ganhou pesos novos hoje, e se o seu agente aponta pra `deepseek-v4-flash`, ele acordou rodando outro modelo — sem changelog nenhum.

Em 31 de julho de 2026, a DeepSeek colocou o V4-Flash em beta público como build `0731`. Mesma arquitetura, mesmo tamanho, mesmo nome de modelo na API. O que mudou foi o pós-treino: os pesos são outros, e os benchmarks de agente pularam de forma que não dá pra ignorar — DeepSWE saiu de 7,3 para 54,4.

Neste post: o que exatamente mudou, os números que a DeepSeek publicou versus os que uma casa independente mediu, quanto isso custa de verdade contra o GPT-5.6 Luna depois do corte de 80% da OpenAI, e o que fazer se você tem agente em produção apontando pra um nome de modelo que virou alvo móvel.

## TL;DR

- **O que é:** DeepSeek-V4-Flash-0731, release oficial (beta público) do V4-Flash. [Mesma arquitetura e tamanho do Preview, só re-pós-treinado](https://api-docs.deepseek.com/updates).
- **Specs:** 284B de parâmetros totais, 13B ativos, MoE, 1M de contexto, 384K de saída máxima, licença MIT.
- **Benchmark de destaque:** 82,7 no Terminal Bench 2.1 (número da DeepSeek). Artificial Analysis mediu 79% no teste próprio.
- **Preço:** US$ 0,0028 input com cache hit, US$ 0,14 input com cache miss, US$ 0,28 output por 1M de tokens.
- **A pegadinha:** o nome do modelo na API não mudou. Quem chamava `deepseek-v4-flash` ontem está chamando outro conjunto de pesos hoje.
- **Rodar local:** o quant Q8 do Unsloth tem 161,9 GB e pede 169 GB de RAM+VRAM somados.

## O que a DeepSeek mudou no V4 Flash 0731 (e o que não mudou)

Começa pelo que não mudou, porque é a parte que confunde.

A arquitetura é a mesma: 284B de parâmetros totais com 13B ativos por token, um backbone MoE de 43 camadas com 256 experts roteados mais um compartilhado por bloco, roteamento top-6, 1M de contexto. A [documentação da DeepSeek é explícita](https://api-docs.deepseek.com/updates): o 0731 "mantém a mesma arquitetura e tamanho do DeepSeek-V4-Flash-Preview, e foi apenas re-pós-treinado".

E o nome na API também não mudou. Você continua mandando `model: "deepseek-v4-flash"`. Mesma string, pesos diferentes.

O que mudou foi o pós-treino, e mudou muito. Olhando a [tabela do próprio card no Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731), o salto em tarefas de agente é o tipo de coisa que normalmente exige geração nova de modelo:

| Benchmark | V4-Flash-0731 | V4-Flash (Preview) | V4-Pro (Preview) |
|---|---|---|---|
| Terminal Bench 2.1 | 82,7 | 61,8 | 72,1 |
| DeepSWE | 54,4 | 7,3 | 12,8 |
| Cybergym | 76,7 | 38,7 | 52,7 |
| Toolathlon-Verified | 70,3 | 49,7 | 55,9 |
| DSBench-FullStack | 68,7 | 37,0 | 41,8 |

Repare na coluna do V4-Pro. O Flash, que é o modelo pequeno e barato, passou o irmão grande — o Pro Preview tem 1,6 trilhão de parâmetros totais e 49B ativos. Um modelo com 13B ativos batendo um de 49B ativos em nove benchmarks de agente diz menos sobre tamanho e mais sobre o quanto pós-treino específico pra ferramenta ainda tem gordura pra queimar.

Aqui está o detalhe operacional que o card não grita: sem versionamento no nome do modelo, essa troca chegou na sua produção sem aviso. Acompanhar isso sozinho, toda semana, é o que cansa — e não é falta de disciplina sua, é falta de ambiente. No [Clã Beer and Code](https://beerandcode.com.br?utm_source=blog&utm_medium=post&utm_campaign=deepseek-v4-flash-0731&utm_content=b-n1) essa leitura é rotina: execução ao vivo toda semana, com gente testando modelo novo em produto real antes de trocar o que está rodando em produção.

## Benchmarks do DeepSeek V4 Flash: ganha no terminal, perde no resto

Agora a parte que a manchete não conta.

O 82,7 no Terminal Bench é real e está publicado. Mas ele não é primeiro lugar. Na **própria tabela da DeepSeek**, o Opus 4.8 marca 85,0 no mesmo teste. O GLM-5.2 marca 81,0. Ou seja: o V4-Flash-0731 entra na briga de topo no terminal, fica na frente do GLM por pouco e continua atrás do Opus.

E quando você sai do terminal, o desenho piora:

| Benchmark | V4-Flash-0731 | GLM-5.2 | Opus-4.8 |
|---|---|---|---|
| Terminal Bench 2.1 | 82,7 | 81,0 | 85,0 |
| DeepSWE | 54,4 | 46,2 | 58,0 |
| NL2Repo | 54,2 | 48,9 | 69,7 |
| DSBench-Hard | 59,6 | 54,5 | 71,7 |
| Cybergym | 76,7 | — | 83,1 |

NL2Repo com 15 pontos de diferença e DSBench-Hard com 12 não são detalhe. Traduzindo pro seu dia: o modelo virou muito bom em operar terminal e encadear ferramenta, e continua mediano em tarefa de engenharia de repositório inteiro e análise de dados difícil.

Tem ainda o dado de fora da casa. A [Artificial Analysis colocou o V4 Flash 0731 em 50 no Intelligence Index](https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash) — 10 pontos acima do Flash anterior, 6 pontos acima do V4 Pro (44), e **um ponto atrás** do GPT-5.6 Luna (max) e do GLM-5.2 (max), ambos em 51. No teste próprio de terminal, eles mediram 79%, não 82,7. Não é contradição: benchmark rodado pelo lab e benchmark rodado por terceiro quase nunca batem, porque scaffold, número de tentativas e harness mudam. É por isso que o número do vendor serve de sinal, não de contrato.

E tem o custo escondido em token. A Artificial Analysis registrou ~206M de tokens de saída só pra rodar o índice, e a [discussão no Hacker News](https://news.ycombinator.com/item?id=49120299) (467 pontos, 254 comentários) bateu justamente nisso: comentaristas relataram que o modelo precisa de bem mais token que um Gemini 3.6 Flash pra fechar a mesma tarefa. Preço por token baixo com verbosidade alta não é o mesmo que conta baixa.

Resumo honesto: não é vitória limpa. É um modelo barato que virou competitivo em agente de terminal, empatou tecnicamente no índice geral e continua atrás em SWE de repositório.

## Preço do DeepSeek V4 Flash: onde dói na OpenAI

A tabela da DeepSeek, [publicada na doc oficial](https://api-docs.deepseek.com/quick_start/pricing), por 1M de tokens:

| | Preço |
|---|---|
| Input (cache hit) | US$ 0,0028 |
| Input (cache miss) | US$ 0,14 |
| Output | US$ 0,28 |

O cache hit a US$ 0,0028 é o número que muda arquitetura, não planilha. É 50x mais barato que o cache miss. Se o seu agente tem system prompt grande e estável — e agente de terminal sempre tem — a diferença entre estruturar o prompt pra bater cache e não estruturar é a diferença entre uma conta e cinquenta.

Contra a OpenAI: a Artificial Analysis calculou que o custo por tarefa do V4 Flash 0731 na API de primeira mão da DeepSeek sai **~60% mais barato que o GPT-5.6 Luna (max)** — e isso já contando [o corte de 80% que a OpenAI aplicou no Luna](https://blog.beerandcode.com.br/noticias/gpt-5-6-luna-preco-corte-80). É esse o ponto que dói: a OpenAI cortou 80% e continua mais cara, contra um modelo que empata em índice geral por um ponto.

Só que "mais barato por tarefa" carrega a ressalva do bloco anterior. Se o seu caso de uso é daqueles em que o modelo fica verboso, parte da economia volta pela porta dos fundos em token de saída. A conta que vale é a sua, com o seu prompt — não a média do índice. Vale lembrar também que a DeepSeek já experimentou [preço variável por horário de pico](https://blog.beerandcode.com.br/noticias/deepseek-v4-preco), então tabela de preço dessa casa é coisa que se confere, não que se decora.

## Rodar local: os pesos estão no Hugging Face, mas pedem 169 GB

Peso MIT no Hugging Face não significa que roda na sua máquina.

Os quants do Unsloth, [documentados no guia deles](https://unsloth.ai/docs/models/deepseek-v4):

- **UD-Q8_K_XL** (lossless): arquivo de 161,9 GB, recomendação de **169 GB** de RAM + VRAM somados.
- **UD-Q4_K_XL** (quase lossless): 155,1 GB de arquivo, 162 GB recomendados.
- **UD-IQ3_XXS**: 110–135 GB, a opção mais realista pra máquina de gente.

Note que Q4 e Q8 diferem em só 7 GB — a arquitetura MoE fina não comprime linearmente como um denso, então descer de bit rende menos do que você espera. No Hacker News, usuário com MacBook Pro de 128 GB relatou 20–25 tokens/s de geração com prefill em 400–450 tps. Utilizável pra tarefa assíncrona, sofrido pra loop de agente interativo.

Se o seu plano era GPU única, a gente já fez essa conta em detalhe no post sobre [rodar o V4 Flash local num RTX 5090](https://blog.beerandcode.com.br/noticias/deepseek-v4-flash-local-5090), e o padrão se repete aqui: o gargalo nunca é o modelo caber, é a memória total do sistema. Mesmo enredo do [Kimi K3 quando liberou os pesos](https://blog.beerandcode.com.br/noticias/kimi-k3-pesos-abertos) — peso aberto é liberdade de licença, não de hardware.

Uma limitação que economiza seu tempo antes de baixar 162 GB: o V4 Flash **não é multimodal**. Se o seu pipeline lê screenshot, PDF escaneado ou imagem, ele está fora dessa etapa.

## Rastreador: o DeepSeek V4 Pro oficial

Etiqueta clara: **RUMOR**.

O que é **fato**: o [DeepSeek-V4-Pro existe desde abril de 2026](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro), com 1,6 trilhão de parâmetros totais e 49B ativos — e está publicado como **preview**, não como release oficial. Nunca saiu do rótulo de prévia.

O que é **rumor**: que a versão oficial do V4-Pro sai "em breve". Isso circula em thread de r/LocalLLaMA e não tem anúncio, data nem changelog oficial. Não planeje migração em cima disso.

O que dá pra ler com segurança do movimento de hoje: a DeepSeek acabou de mostrar que consegue tirar um salto de agente enorme só com pós-treino, sem tocar em arquitetura. Aplicar a mesma receita no Pro é o próximo passo natural — e a situação atual, com o Flash barato passando o Pro caro em nove benchmarks de agente, é constrangedora o suficiente pra forçar a mão. Mas "natural" e "anunciado" são coisas diferentes.

Atualizo esta seção quando sair anúncio formal.

## O que fazer se seu agente aponta pra `deepseek-v4-flash`

A parte acionável. Nome de modelo sem versão é alvo móvel, e você tem três problemas concretos.

**1. Você não sabe qual versão respondeu.** Logue a resposta inteira, não só o conteúdo. O campo `model` do retorno é a única testemunha que você vai ter quando o comportamento mudar:

```python
resp = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=msgs,
)

logger.info("llm_call", extra={
    "model_requested": "deepseek-v4-flash",
    "model_returned": resp.model,          # guarde SEMPRE
    "prompt_tokens": resp.usage.prompt_tokens,
    "cached_tokens": resp.usage.prompt_tokens_details.cached_tokens,
    "completion_tokens": resp.usage.completion_tokens,
})
```

O `cached_tokens` está aí de propósito: é ele que diz se você está pagando US$ 0,0028 ou US$ 0,14. Cache hit baixo é o bug de custo mais comum e o mais silencioso.

**2. Você não tem como fixar a versão na API de primeira mão.** A DeepSeek não expõe slug datado — `deepseek-v4-flash` é o que tem. Se pin de versão é requisito do seu produto, o caminho é provider terceiro: o OpenRouter publica o build como slug datado (`deepseek/deepseek-v4-flash-0731`), o que te dá reprodutibilidade em troca de uma camada a mais e de preço um pouco pior. É trade-off, não solução mágica.

**3. Você não sabe se melhorou pro seu caso.** Benchmark de agente subir 47 pontos não garante que o seu fluxo específico melhorou — pós-treino pesado em ferramenta costuma mexer em formato de saída, verbosidade e obediência a instrução. Rode a sua suíte de evals contra o modelo hoje e compare com o baseline. Se você não tem baseline salvo, essa é a lição da semana: sem eval própria versionada, atualização silenciosa de peso é indetectável até o cliente reclamar.

## FAQ rápido

**Preciso mudar meu código pra usar o 0731?**
Não. O nome do modelo continua `deepseek-v4-flash` e o formato de chamada é o mesmo. O 0731 já está respondendo. O trabalho não é de integração, é de validação — rodar eval e conferir se o comportamento novo serve pro seu caso.

**Ele é melhor que o GPT-5.6 Luna?**
Depende da tarefa. No Intelligence Index da Artificial Analysis ficam praticamente empatados (50 contra 51). Em agente de terminal o DeepSeek está forte. Em custo por tarefa sai ~60% mais barato mesmo após o corte da OpenAI. Em tarefa de repositório grande e em multimodal, o Luna leva.

**Posso usar comercialmente?**
Sim. Os pesos estão sob licença MIT no Hugging Face, o que permite uso comercial, modificação e redistribuição. A ressalva relevante não é de licença, é de compliance de cliente e do risco geopolítico que a gente destrinchou no post sobre [sanções à IA chinesa open source](https://blog.beerandcode.com.br/noticias/sancoes-ia-chinesa-open-source).

**Dá pra rodar num setup de 64 GB?**
Não nos quants bons. O piso realista é o IQ3_XXS em 110–135 GB. Abaixo disso você entra em quantização agressiva que degrada exatamente a capacidade de agente que faz esse modelo valer a pena.

## Conclusão

O fato de 31 de julho é pequeno e a implicação é grande. A DeepSeek re-pós-treinou o V4-Flash, publicou pesos novos sob o mesmo nome de API, e entregou um modelo que ganha em terminal, empata no índice geral por um ponto e perde em SWE de repositório. Barato de verdade, competitivo de verdade, e longe da vitória limpa que a manchete sugere.

A lição que sobrevive ao ciclo de notícia é outra, e não é sobre a DeepSeek: você está construindo produto em cima de dependência que se atualiza sozinha, sem versão e sem aviso. Isso não é defeito de lab chinês — é a natureza de consumir modelo como serviço. Quem tem eval versionada e log do `model` retornado descobre a mudança no gráfico. Quem não tem descobre no ticket de suporte.

O próximo capítulo provável é o V4-Pro recebendo o mesmo tratamento de pós-treino. Quando sair, a pergunta que vai importar não é quanto ele marcou no Terminal Bench. É se você tem como medir o que ele fez com o seu produto.
