A Moonshot AI botou um countdown no ar prometendo os pesos abertos do Kimi K3 para 27 de julho. Soltou no dia 26, por volta das 19h30 (horário de Nova York) — um dia antes do próprio prazo. Não é todo dia que um lab entrega adiantado.

O arquivo está lá: 2,8 trilhões de parâmetros, o maior modelo de pesos abertos já publicado, livre para baixar. E aí começa a parte que o hype não conta. Porque "de graça" e "roda na sua máquina" são duas afirmações completamente diferentes, e a distância entre elas, nesse caso, é de aproximadamente 1,4 terabyte de VRAM.

Neste post: o que exatamente a Moonshot liberou (licença, formato, onde baixar), o hardware que um MoE dessa escala exige de verdade, a conta honesta de rodar local contra pagar a API a US$ 3 / US$ 15 por milhão de tokens, e o que as sanções americanas alcançam — ou não — de quem baixa peso no Brasil.

## TL;DR

- **O que é:** [Kimi K3](https://huggingface.co/moonshotai/Kimi-K3), MoE de 2,8T de parâmetros totais e 104B ativados, contexto de 1.048.576 tokens, visão nativa. Pesos publicados em 26/07/2026.
- **Licença:** MIT modificada. Uso interno e comercial liberado; operar K3 como Model-as-a-Service com receita acima de US$ 20 milhões em 12 meses exige acordo separado com a Moonshot.
- **Formato:** safetensors com quantização MXFP4 nativa (pesos) e MXFP8 nas ativações, aplicada via quantization-aware training. Não é uma quantização feita depois por terceiro.
- **Custo real de rodar:** ~1,4 TB só para carregar os pesos. Não cabe em nó nenhum de 8 GPUs da geração H200, e nem num DGX B200.
- **API:** US$ 3 por milhão de tokens de entrada (cache miss), US$ 0,30 em cache hit, US$ 15 na saída. Sem sobretaxa de contexto longo.

## O que a Moonshot liberou de verdade nos pesos abertos do Kimi K3

Vamos ao que está no card do Hugging Face, porque é onde mora a diferença entre notícia e boato.

**Arquitetura.** 2,8 trilhões de parâmetros totais, 104 bilhões ativados por token. São 896 experts, sendo 2 compartilhados, e o roteador ativa 16 por token. 93 camadas, das quais 69 usam Kimi Delta Attention (a atenção linear híbrida da casa) e 24 usam Gated MLA. Encoder de visão MoonViT-V2 com 401M de parâmetros. Contexto de 1.048.576 tokens.

**Formato.** Safetensors com MXFP4 nativo nos pesos e MXFP8 nas ativações. E aqui tem um detalhe de engenharia que importa: a quantização foi aplicada com *quantization-aware training*, não empurrada depois num modelo FP16 pronto. Ou seja, o MXFP4 não é uma versão degradada do "modelo de verdade" — é o modelo de verdade. Você não está baixando o GGUF que alguém fez no fim de semana.

**Licença.** É uma MIT modificada, e a modificação é o que você precisa ler. Duas cláusulas somem com o "MIT" da conversa se o seu produto crescer:

1. Se você (ou uma afiliada) opera um negócio de Model-as-a-Service e a receita agregada passa de **US$ 20 milhões em quaisquer 12 meses consecutivos**, precisa fechar um acordo separado com a Moonshot antes de usar.
2. Produto comercial com mais de **100 milhões de usuários ativos mensais** ou mais de **US$ 20 milhões de receita mensal** tem que exibir "Kimi K3" de forma proeminente na interface.

Os limites **não valem para uso interno** — definido como qualquer uso que não disponibilize o modelo, suas saídas ou suas capacidades a terceiros. Traduzindo para o seu caso: se você vai rodar o K3 dentro da empresa, num pipeline interno, num produto seu que não revende inferência, nada disso te alcança. Se o seu negócio *é* vender token, leia a licença com o jurídico.

Para dimensionar o que isso significa competitivamente, vale a leitura do Nathan Lambert, que chamou o lançamento de [um "watershed moment"](https://www.interconnects.ai/p/kimi-k3-the-open-weights-escalation) e estima que a distância entre modelos abertos e fechados caiu de 6 a 9 meses para algo entre 3 e 5. A frase dele que resume o incômodo em Washington e em São Francisco: "a Moonshot AI está indo de igual pra igual com Anthropic e OpenAI com muito, muito menos recursos".

Só que peso publicado não é produto. Entre baixar um safetensors e ter inferência servindo requisição com latência aceitável existe uma camada inteira de engenharia — e é exatamente essa camada que separa quem *usa* IA de quem *constrói* com IA. É o assunto do [Clã Beer and Code](https://beerandcode.com.br?utm_source=blog&utm_medium=post&utm_campaign=kimi-k3-pesos-abertos&utm_content=a-n1), a maior comunidade de engenharia de IA do Brasil: é pago, é assinatura, e é onde essa conta aparece com número na mesa em vez de thread de entusiasmo.

Se você quer o recorte de capacidade — quanto o K3 realmente entrega contra Claude e GPT nos benchmarks —, isso a gente já destrinchou [quando o modelo foi lançado via API](https://blog.beerandcode.com.br/noticias/kimi-k3-benchmarks-vs-claude). Este post aqui é sobre a outra metade da história: o que custa colocar isso pra rodar.

## Requisitos do Kimi K3: a conta de 1,4 TB de VRAM que não cabe no título

Aqui está o número que decide tudo: **os pesos em MXFP4 ocupam cerca de 1,4 TB**. Em FP16 seriam algo perto de 5,6 TB — a quantização nativa já te deu um desconto de 4x, e ainda assim sobra 1,4 TB para carregar antes de processar um único token.

Faça a conta com o hardware que existe:

| Configuração | VRAM agregada | Cabe? |
|---|---|---|
| 1× RTX 5090 (32 GB) | 0,032 TB | Não, e nem perto |
| 8× H100 (80 GB) | 0,64 TB | Não |
| 8× H200 (141 GB) | 1,128 TB | **Não** |
| 8× B200 (180 GB) | 1,44 TB | Tecnicamente sim, na prática não |
| 8× B300 / MI355X (288 GB) | 2,304 TB | Sim |
| GB300 NVL72 | ~20,7 TB | Sim, com folga |

Repare na linha do H200. Circula bastante que "um nó de 8× H200 resolve se você aceitar MXFP4". Não resolve: 8 × 141 GB dá 1,128 TB, e os pesos pedem 1,4 TB. Falta antes de começar.

A linha do B200 é mais sutil e mais interessante. 8 × 180 GB dá 1,44 TB — cabem os pesos, sobram uns 40 GB no nó inteiro. Aí você lembra que ainda precisa de espaço para KV cache, ativações e overhead do runtime, e que o modelo anuncia 1M de contexto. Por isso a [SemiAnalysis foi direta](https://x.com/SemiAnalysis_/status/2077966560447074689): o K3 não cabe num DGX B200 nem em FP4, e o caminho é GB300 NVL72, B300 ou MI355X, onde cada GPU tem 288 GB.

A Kimi Delta Attention ajuda bastante nessa parte — atenção linear híbrida gasta muito menos KV cache que atenção cheia no mesmo comprimento, e é por isso que 1M de contexto é viável aqui. Ajuda. Não faz milagre em 40 GB.

Dá para ir de dois nós de 8× H200 (16 GPUs, 2,256 TB) e distribuir? Dá. Mas aí você bate no outro muro, que a própria SemiAnalysis aponta: o B200 tem 400 Gbit/s de banda entre nós, contra um NVL72 com banda inter-nó cerca de 18x maior. Num MoE com 896 experts, roteamento de token atravessando a rede a cada camada não é detalhe — é o gargalo. Modelo esparso pune interconnect ruim de um jeito que modelo denso não pune.

E o runtime? vLLM, SGLang e TensorRT-LLM são os caminhos suportados, com a ressalva de que o roteamento de 896 experts exige scheduling ciente de MoE — engine desatualizada pode precisar de patch. Não é `docker run` e pronto.

## Rodar Kimi K3 local vs API a US$ 3 / US$ 15: onde fica o break-even

Agora a conta que interessa pra quem decide orçamento.

**Lado do aluguel.** Preços de mercado em julho de 2026: H200 sai entre US$ 3,72 e US$ 10,60 por GPU-hora, com mediana perto de US$ 3,95. A CoreWeave lista o nó HGX H200 de 8 GPUs a US$ 50,44/hora sob demanda, e cerca de US$ 20,93/hora em spot. B200 fica na faixa de US$ 6 a US$ 8,60 por GPU-hora. GB200 NVL72 vai de US$ 10,50 a US$ 27 por GPU-hora.

Pegue a configuração mínima que fecha a conta de memória com dois nós H200:

- **Sob demanda:** 2 × US$ 50,44 = US$ 100,88/hora → US$ 2.421/dia → **~US$ 72.600/mês** rodando 24/7.
- **Spot:** 2 × US$ 20,93 = US$ 41,86/hora → **~US$ 30.100/mês**, com o risco de preempção que spot traz.

**Lado da API.** US$ 3 por milhão de entrada, US$ 15 por milhão de saída, US$ 0,30 em cache hit. Sem sobretaxa de contexto longo — o que, num modelo de 1M, não é pouca coisa.

Vamos usar um blend realista de carga agentica, que é entrada-pesada: para cada 1M de tokens de entrada, uns 100k de saída. Custo por 1M de entrada-equivalente = US$ 3 + (0,1 × US$ 15) = **US$ 4,50**.

Agora o break-even:

```
US$ 72.600 / US$ 4,50 por 1M tokens = ~16,1 bilhões de tokens/mês
16,1e9 tokens / (30 dias × 86.400 s) = ~6.200 tokens/segundo, 24 horas por dia, 30 dias
```

Seis mil e duzentos tokens por segundo. Sustentados. Sem parar. É esse o volume que você precisa manter para o aluguel sob demanda empatar com a API. Na versão spot, o número cai para ~2.600 tokens/s sustentados — ainda é uma carga de empresa, não de time.

E tem um detalhe que piora ainda mais o lado local: o cache hit a US$ 0,30/M. Se a sua carga tem prefixo repetido — system prompt grande, base de código, documento fixo, que é exatamente o perfil de agente —, a API fica **10x mais barata** naquela fatia. O break-even sobe junto.

A conclusão desconfortável é simples: **rodar Kimi K3 local não é decisão de custo.** Nessa escala, a API ganha de lavada para quase todo mundo. Local ganha por outros motivos, e eles são legítimos: soberania de dado, requisito regulatório que proíbe a inferência sair do perímetro, fine-tuning e pré-treino continuado sobre os pesos, ou pesquisa. Se o seu argumento para self-host é "vou economizar", refaça a planilha.

Isso é diferente do que rola um degrau abaixo. Modelo menor no seu hardware é outra conversa — a gente mostrou [DeepSeek V4 Flash rodando 1M de contexto num RTX 5090](https://blog.beerandcode.com.br/noticias/deepseek-v4-flash-local-5090), com os asteriscos do caso, e comparou [pago caro, pago barato e local de graça construindo o mesmo produto três vezes](https://blog.beerandcode.com.br/noticias/claude-opus-4-8-vs-minimax-m3-vs-qwen-3-local). Ali "rodar local" é uma frase com sentido. Com 2,8T, "local" virou sinônimo de "datacenter".

Quem quiser testar sem montar cluster: Together AI e Modal anunciaram hospedagem no dia zero, junto com a API da própria Moonshot.

## O que as sanções alcançam de quem baixa peso no Brasil

Pergunta que apareceu em toda thread desde o dia 21, quando o secretário do Tesouro Scott Bessent [ameaçou sancionar labs chineses por suposto roubo de propriedade intelectual](https://techcrunch.com/2026/07/21/us-threatens-sanctions-against-chinese-ai-models-over-ip-theft/): baixar isso me coloca em risco?

Resposta curta: hoje, não. Não existe sanção formal publicada contra modelos chineses de pesos abertos — existe ameaça pública, que é outra coisa. E mesmo se vier, tem uma característica do formato que muda tudo: **peso publicado é irreversível**. A licença é uma concessão irrevogável, o arquivo está no seu disco, e não há kill switch. Sanção americana não apaga safetensors do seu storage nem transforma inferência local em ilícito no Brasil.

O risco real é indireto, e vale mapear:

- **Distribuição.** Hugging Face é empresa americana. Takedown ou geo-block de repositório é o cenário plausível. Se o K3 está no seu roadmap, baixe e versione agora — storage é barato, re-download depois de takedown não existe.
- **Providers.** Together, Modal, Fireworks, OpenRouter: empresas americanas cumprem sanção americana. Seu acesso via API de terceiro é o ponto de falha mais frágil da cadeia.
- **Compliance de cliente.** Você tem CNPJ brasileiro, mas se vende para multinacional com capital americano, o jurídico do cliente pode vetar modelo sancionado na cadeia de fornecedores. O contrato alcança onde a sanção não alcança.

A gente destrinchou o cenário completo — o que é fato, o que é rumor e o playbook mínimo — no post sobre [as sanções à IA chinesa open source](https://blog.beerandcode.com.br/noticias/sancoes-ia-chinesa-open-source). O resumo operacional continua valendo: peso versionado, provider abstraído, evals próprias, fallback definido a frio.

E não confunda as duas coisas: o limite de US$ 20 milhões da licença da Moonshot é cláusula contratual, não sanção geopolítica. Uma você resolve com advogado e um acordo; a outra não depende de você.

## Limitações e pontos de atenção

**A quantização não é uma escada.** Como o MXFP4 é nativo e treinado, não existe o caminho confortável de "pego o FP16 e quantizo mais". Você já está no formato de origem. Quantizações mais agressivas por terceiros vão aparecer, mas partem de um modelo que já foi otimizado para 4 bits — a margem para cortar sem estragar é bem menor do que a que existia em modelos FP16.

**Contexto de 1M é teto, não default.** Anunciar 1.048.576 tokens não significa que você vai servir todo mundo com janela cheia. Cada token de contexto ocupa memória que compete com o peso do modelo no mesmo nó. Em produção, você vai definir um limite bem menor por request e vai gostar do resultado.

**Suporte de engine ainda está amadurecendo.** 896 experts com 2 compartilhados e roteamento de 16 por token é uma topologia nova. Espere versões de vLLM/SGLang com correções específicas nas próximas semanas, e não planeje deploy crítico em cima da primeira release que funcionar.

**Benchmark não é o seu caso de uso.** Vale para todo modelo, vale em dobro aqui: terceiro lugar num ranking geral não diz nada sobre o seu domínio. Sem suite de evals própria, "o K3 é melhor" é opinião.

## FAQ rápido

**Consigo rodar o Kimi K3 na minha RTX 5090 com alguma quantização?**
Não. Os pesos MXFP4 nativos ocupam ~1,4 TB; uma 5090 tem 32 GB. Nem com offload agressivo para RAM e disco isso vira algo utilizável — você trocaria latência de milissegundos por minutos. Para local de verdade, olhe modelos de 30B a 200B.

**Posso usar comercialmente?**
Sim, na maioria dos casos. A MIT modificada libera uso interno e comercial. As restrições só ligam se você opera Model-as-a-Service com receita acima de US$ 20M/12 meses, ou tem produto com 100M+ de usuários mensais (aí precisa creditar "Kimi K3" na interface). Uso interno está explicitamente isento.

**Onde baixar o Kimi K3 e qual o tamanho real do download?**
No repositório [moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3), em safetensors MXFP4, na casa de 1,4 TB. Planeje banda e storage antes de dar `git clone` — e use `hf download` com retomada, não o navegador.

**Vale a pena montar infra própria para isso?**
Só se o motivo não for custo. Pelo break-even acima, você precisa de ~6.200 tokens/s sustentados 24/7 para empatar com a API sob demanda. Se o motivo é soberania de dado, requisito regulatório ou fine-tuning sobre os pesos, aí sim a conta muda de natureza — deixa de ser economia e vira capacidade que a API não vende.

## Conclusão

O Kimi K3 de pesos abertos é o maior modelo já publicado livremente, saiu um dia antes do prometido, com licença que a maioria dos times pode usar sem falar com advogado, e num formato que não é gambiarra de quantização. Isso é real e é grande.

O que não é real é a ideia de que "aberto" resolveu o problema de acesso. Resolveu o problema de *permissão*. O problema de *capacidade* continua exatamente onde estava: 1,4 TB de VRAM, interconnect de datacenter e um break-even que só fecha em escala de empresa. O modelo ficou de graça; a infra para rodar ele ficou igualzinha.

E é aí que está a provocação que sobra desse lançamento. Quando um modelo de fronteira é livre para baixar mas exige um rack de US$ 3 milhões para servir, o gargalo do mercado deixa de ser "quem tem o melhor modelo" e passa a ser "quem consegue operar o modelo que já é de todo mundo". Isso não é problema de pesquisa. É problema de engenharia — e essa parte ninguém vai publicar no Hugging Face pra você.
