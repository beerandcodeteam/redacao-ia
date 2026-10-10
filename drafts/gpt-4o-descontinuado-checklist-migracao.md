O modelo que virou sinônimo de ChatGPT tem data marcada pra desligar. Se você tem `gpt-4o` hardcoded em algum lugar, o prazo é 23 de outubro — e a migração não é só trocar uma string no `.env`.

GPT-4o descontinuado não é boato. A [página oficial de deprecações da OpenAI](https://developers.openai.com/api/docs/deprecations) confirma que o `gpt-4o-2024-05-13` é desligado em **23 de outubro de 2026**, junto com mais onze model IDs. Substituto recomendado: `gpt-5.6-sol`.

Só que a manchete que circulou nos portais gringos está errada em dois pontos importantes. E se você migrar acreditando nela, vai quebrar coisa que não precisava quebrar — ou vai deixar passar o que realmente ia te derrubar. Vamos aos fatos, com a fonte primária aberta, e depois ao checklist técnico.

## TL;DR

- **O que morre em 23/10/2026:** `gpt-4o-2024-05-13`, `gpt-4-turbo`, `gpt-4-0613`, `gpt-3.5-turbo-0125`, `gpt-4.1-nano`, `o1`, `o1-pro`, `o3-mini`, `o4-mini`, `gpt-image-1` e os fine-tunes de `o4-mini`.
- **O que NÃO morre:** `gpt-4o-mini`. Ele continua listado como modelo padrão, sem aviso de deprecação. Quem morreu foi outra coisa (explico abaixo).
- **A bomba seguinte:** toda a família legada de áudio e realtime desliga em **20/01/2027**.
- **A bomba mais próxima:** a Assistants API desliga em **26/08/2026**. Daqui a um mês.
- **Custo:** o substituto recomendado (`gpt-5.6-sol`) é 2x mais caro no input e 3x no output que o `gpt-4o`.
- **Fonte primária** da tabela de shutdown do GPT-4o: [developers.openai.com/api/docs/deprecations](https://developers.openai.com/api/docs/deprecations)

## GPT-4o descontinuado: o que a OpenAI realmente anunciou

A tabela do dia 23 de outubro, anunciada em 22 de abril de 2026, tem doze linhas. Transcrevendo o que interessa:

| Modelo desligado | Substituto recomendado |
|---|---|
| `gpt-4o-2024-05-13` | `gpt-5.6-sol` |
| `gpt-4-turbo` | `gpt-5.6-sol` |
| `gpt-4-0613` | `gpt-5.6-sol` |
| `gpt-4-1106-preview` | `gpt-5.6-sol` |
| `gpt-3.5-turbo-0125` | `gpt-5.6-terra` |
| `gpt-4.1-nano` | `gpt-5.6-luna` |
| `o1-2024-12-17` | `gpt-5.6-sol` |
| `o1-pro-2025-03-19` | `gpt-5.6-sol` |
| `o3-mini-2025-01-31` | `gpt-5.6-sol` |
| `o4-mini-2025-04-16` | `gpt-5.6-terra` |
| `ft-o4-mini-2025-04-16` | `gpt-5.6-terra` |
| `gpt-image-1` | `gpt-image-2` |

Repara numa coisa: o que está na lista é `gpt-4o-2024-05-13`. O snapshot de maio de 2024. O primeiro.

O alias `gpt-4o` — aquele sem data, o que 90% dos projetos usam — hoje resolve para `gpt-4o-2024-11-20`, e esse snapshot **não está na tabela**. A página de modelos ainda lista `gpt-4o` como disponível, a US$ 2,50 por milhão de tokens de input e US$ 10,00 de output, com apenas o `gpt-4o-2024-08-06` marcado como "Deprecated".

Isso muda completamente o seu plano de ação. Quem pinou `gpt-4o-2024-05-13` no código tem uma data dura e um erro 404 esperando em outubro. Quem usa o alias tem um problema diferente e mais traiçoeiro: o modelo por baixo vai continuar mudando sem você fazer deploy nenhum. Diagnosticar qual dos dois é o seu caso é o primeiro item do checklist — e é o tipo de decisão de arquitetura que a gente destrincha toda semana no [Clã Beer and Code](https://beerandcode.com.br), com código rodando e conta de API na mesa.

## Não, não foi "abrupto e sem caminho de migração"

Essa foi a manchete que rodou. É falsa, e dá pra provar com a própria página.

A política de deprecação da OpenAI, publicada no topo do documento, promete **no mínimo 6 meses** de aviso para modelos em disponibilidade geral, no mínimo 3 meses para variantes especializadas, e admite que modelos `preview` podem sair com prazo bem mais curto — "such as 2 weeks", nas palavras deles.

Faz a conta: anúncio em 22 de abril, desligamento em 23 de outubro. Seis meses e um dia. A política foi cumprida à risca. E cada linha da tabela tem um substituto recomendado explícito — o "caminho de migração" que os portais disseram não existir está literalmente na coluna da direita.

A crítica legítima é outra, e é mais interessante. Até o [TheRouter](https://therouter.ai/news/openai-legacy-model-deprecation-wave-july-october-2026/), que tratou o caso como "o evento de ciclo de vida de modelo mais relevante de 2026", não reclama de falta de aviso. Reclama que "the replacement mappings are not always cost-equivalent" — os mapeamentos não são equivalentes em custo.

Nisso eles têm toda razão:

| Modelo | Input / 1M | Cached input / 1M | Output / 1M |
|---|---|---|---|
| `gpt-4o` | $2.50 | $1.25 | $10.00 |
| `gpt-4o-mini` | $0.15 | — | $0.60 |
| `gpt-5.6-sol` | $5.00 | $0.50 | $30.00 |
| `gpt-5.6-terra` | $2.50 | $0.25 | $15.00 |
| `gpt-5.6-luna` | $1.00 | $0.10 | $6.00 |

Seguir a recomendação da OpenAI ao pé da letra — `gpt-4o-2024-05-13` para `gpt-5.6-sol` — dobra seu custo de input e triplica o de output. Numa aplicação que gera muito texto, isso é a diferença entre uma feature que se paga e uma que some no próximo corte de custo.

Tem um detalhe que quase ninguém comentou, e ele inverte a conta: o **cached input** do `gpt-5.6-sol` custa US$ 0,50, contra US$ 1,25 do `gpt-4o`. Se sua carga é de prompt longo e repetido — RAG com contexto fixo, system prompt gordo, agente com histórico — o cache hit sai 60% mais barato no modelo novo. A migração pode até reduzir sua fatura. Depende inteiramente do seu perfil de tokens, não da tabela de preço base.

E se você olhar a coluna toda, o `gpt-5.6-luna` é mais barato que o `gpt-4o` nos dois lados: US$ 1,00 contra US$ 2,50 no input, US$ 6,00 contra US$ 10,00 no output. Para tarefa de classificação, extração e roteamento, o substituto "oficial" provavelmente não é o que você quer.

## O que já morreu em 23 de julho (e o sinal do OpenRouter)

Aqui está a correção mais importante, porque é a que mais gente errou.

`gpt-4o-mini` **não está deprecado**. A página de modelos ainda o lista como padrão, com janela de 128k tokens, cutoff de outubro de 2023 e preço de US$ 0,15 / US$ 0,60. Nenhum banner, nenhuma data.

O que morreu — quatro dias atrás, em **23 de julho de 2026** — foi o `gpt-4o-mini-search-preview-2025-03-11`. Um modelo `preview`, especializado em busca, com substituto recomendado `gpt-5.6-terra`. É exatamente por isso que o `openai/gpt-4o-mini-search-preview` sumiu do catálogo do OpenRouter nas últimas 48 horas: o upstream desligou, o agregador tirou do ar. Não é o `gpt-4o-mini` indo embora. É um primo `preview` dele.

Essa mesma onda de 23 de julho levou junto:

- `gpt-4o-search-preview-2025-03-11` → `gpt-5.6-terra`
- `computer-use-preview-2025-03-11` → `gpt-5.6-terra`
- `gpt-5-codex`, `gpt-5.1-codex`, `gpt-5.1-codex-max`, `gpt-5.2-codex` → `gpt-5.6-sol`
- `gpt-5.1-codex-mini` → `gpt-5.6-terra`
- `gpt-5-chat-latest` e `gpt-5.1-chat-latest` → `gpt-5.6-sol`
- `o3-deep-research-2025-06-26` e `o4-mini-deep-research-2025-06-26` → `gpt-5.6-sol`
- `gpt-4o-mini-tts-2025-03-20` → `gpt-4o-mini-tts-2025-12-15`

Presta atenção nessa cadeia, porque ela é a moral da história toda: o `chatgpt-4o-latest` foi desligado em 17 de fevereiro de 2026, com migração recomendada para `gpt-5.1-chat-latest`. E o `gpt-5.1-chat-latest` morreu em 23 de julho. Quem seguiu a recomendação oficial em fevereiro migrou para um modelo que durou cinco meses.

Alias com `-latest` no nome não é estabilidade. É uma assinatura de mudança contínua.

Se você quer o quadro maior de para onde essa família está indo, vale ler o [comparativo de Sol, Terra e Luna](https://blog.beerandcode.com.br/noticias/gpt-5-6-sol-terra-luna-qual-usar) antes de escolher o destino da sua migração.

## A bomba de janeiro: áudio e realtime

Anunciada em **20 de julho de 2026** — há uma semana — e com desligamento em **20 de janeiro de 2027**, essa é a onda que vai pegar quem construiu produto de voz.

| Modelo desligado | Substituto recomendado |
|---|---|
| `gpt-realtime` | `gpt-realtime-2.1` |
| `gpt-4o-realtime` | `gpt-realtime-2.1` |
| `gpt-realtime-mini` | `gpt-realtime-2.1-mini` |
| `gpt-4o-mini-realtime` | `gpt-realtime-2.1-mini` |
| `gpt-audio` | `gpt-audio-1.5` |
| `gpt-audio-mini` | `gpt-audio-1.5` |
| `gpt-4o-audio` | `gpt-audio-1.5` |
| `gpt-4o-mini-audio` | `gpt-audio-1.5` |
| `gpt-4o-mini-transcribe-2025-03-20` | `gpt-4o-mini-transcribe-2025-12-15` |

Repara que aqui os IDs sem data — `gpt-realtime`, `gpt-audio` — estão na lista. Não é só o snapshot antigo. É a família inteira.

Migração de realtime não é troca de string. É protocolo de WebSocket, formato de evento, tratamento de interrupção, latência de primeiro token e comportamento de voz que o seu usuário já reconhece. Seis meses é prazo justo, mas só se você começar a olhar agora.

## O checklist pra migrar sem quebrar produção

Cinco passos para migrar do GPT-4o sem susto. Nessa ordem.

### 1. Descubra o que você realmente está chamando

Antes de qualquer decisão, inventário. Model ID não vive só no `.env` — ele se esconde em migration de banco, seed, fixture de teste, config de fila, prompt salvo no CMS e naquele script Python de 2024 que ninguém abre.

```bash
grep -rniE 'gpt-4o|gpt-4-turbo|gpt-3\.5-turbo|o1-|o3-mini|o4-mini|gpt-image-1|realtime|audio-preview' \
  --include='*.php' --include='*.py' --include='*.js' --include='*.ts' \
  --include='*.env*' --include='*.json' --include='*.yml' --include='*.yaml' \
  --exclude-dir={vendor,node_modules,.git,storage} .
```

Depois cruza com a realidade: o que o código diz e o que a API registra podem divergir. Puxe os últimos 30 dias de uso no dashboard da OpenAI agrupado por modelo. Se aparecer um ID que não estava no grep, você tem código que não sabia que tinha.

### 2. Decida entre alias e snapshot — e assuma a escolha

Essa é a decisão de arquitetura do checklist, e ela não tem resposta única.

**Snapshot pinado** (`gpt-4o-2024-11-20`) te dá comportamento estável e uma data de morte conhecida. Você quebra num dia que a OpenAI anuncia com seis meses de antecedência.

**Alias** (`gpt-4o`) te dá continuidade de serviço e comportamento instável. Você nunca toma 404, mas o modelo por baixo pode mudar numa terça-feira e derrubar a acurácia do seu classificador sem um único commit no seu repositório.

Para produto sério, a resposta quase sempre é: pina o snapshot, centraliza num único lugar e trata a data de deprecação como um item de backlog com dono.

```php
// config/ai.php — um lugar só. Nunca um model ID solto no meio do serviço.
return [
    'models' => [
        // sunset: 2026-10-23 — https://developers.openai.com/api/docs/deprecations
        'chat'       => env('AI_MODEL_CHAT', 'gpt-5.6-terra'),
        'reasoning'  => env('AI_MODEL_REASONING', 'gpt-5.6-sol'),
        'classifier' => env('AI_MODEL_CLASSIFIER', 'gpt-5.6-luna'),
    ],
];
```

O ganho aqui não é elegância. É que no dia da migração você troca três linhas e roda a suíte, em vez de caçar string em quarenta arquivos.

### 3. Refaça a conta de custo com os SEUS tokens

Não use a tabela de preço base para decidir. Use seu consumo real.

```python
# Custo mensal estimado, por modelo. Preços em USD por 1M tokens.
PRICES = {                # input, cached_input, output
    "gpt-4o":        (2.50, 1.25, 10.00),
    "gpt-5.6-sol":   (5.00, 0.50, 30.00),
    "gpt-5.6-terra": (2.50, 0.25, 15.00),
    "gpt-5.6-luna":  (1.00, 0.10,  6.00),
}

# Puxe estes três números do seu dashboard de usage (mensal).
IN_TOKENS, CACHED_TOKENS, OUT_TOKENS = 180_000_000, 120_000_000, 25_000_000

for model, (pin, pcached, pout) in PRICES.items():
    fresh = IN_TOKENS - CACHED_TOKENS
    total = (fresh * pin + CACHED_TOKENS * pcached + OUT_TOKENS * pout) / 1_000_000
    print(f"{model:<14} US$ {total:>9,.2f}/mes")
```

Rode com os seus números. Em carga com muito cache hit, o `gpt-5.6-sol` costuma sair mais barato que o `gpt-4o` apesar do preço base ser o dobro. Em carga de output pesado, ele explode. Essa conta é sua, não da OpenAI.

### 4. Não troque a string sem eval

Esse é o passo que separa migração de acidente.

Modelo novo não é modelo melhor para o **seu** caso. Ele tem outro estilo de resposta, outro comportamento de recusa, outro formato preferido de saída, outra tendência a verbosidade. Se você tem parser de JSON no fim do pipeline, prompt afinado no cotovelo ou classificador calibrado em cima do comportamento do `gpt-4o`, trocar a string em produção é apostar.

O mínimo viável:

1. Congele 50 a 100 casos reais do seu log de produção, com a saída atual que você considera correta.
2. Rode os mesmos casos nos candidatos (`sol`, `terra`, `luna`) com o prompt inalterado.
3. Meça o que importa no seu domínio: taxa de JSON válido, acerto de classificação, chamada de tool correta, tokens de saída, latência p95.
4. Só então mexa no prompt — e re-rode.

Cinquenta casos e uma planilha resolvem. Não precisa de framework de eval para começar; precisa começar.

### 5. Cheque a Assistants API antes de tudo isso

Se o seu projeto usa a Assistants API, ela é sua urgência real: o desligamento é **26 de agosto de 2026**, anunciado um ano antes, em 26 de agosto de 2025.

São trinta dias. Muito menos que os oitenta e oito que você tem até o 23 de outubro, e a migração é mais pesada — sai de threads e assistants gerenciados pela OpenAI e passa a gerenciar estado de conversa você mesmo. Resolve isso primeiro.

## Limitações e pontos de atenção

Três coisas que o checklist não cobre e que costumam morder.

**Fine-tunes não migram.** Um `ft-o4-mini-2025-04-16` sai do ar em 23 de outubro e você não "aponta" ele para o `gpt-5.6-terra` — você retreina do zero, com o dataset que espero que você ainda tenha versionado. Se o dataset se perdeu, o prazo real não é outubro: é o tempo de reconstruir o dataset mais o treino mais a validação.

**Provider agregador não te protege.** OpenRouter, LiteLLM, gateway próprio — todos repassam o desligamento do upstream. O `gpt-4o-mini-search-preview` sumindo do catálogo do OpenRouter é a prova: o agregador não segura um modelo que a OpenAI apagou. Ele só te avisa depois.

**Preview é preview.** Qualquer ID com `preview` no nome pode sair com duas semanas de aviso, segundo a própria política. Se tem `preview` rodando em caminho crítico de produção, isso não é dívida técnica — é uma escolha de risco que alguém precisa aprovar conscientemente.

## FAQ rápido

**O `gpt-4o-mini` vai ser desligado em outubro?**
Não. Ele segue listado como modelo padrão na documentação, sem data de shutdown. Quem foi desligado em 23 de julho foi o `gpt-4o-mini-search-preview-2025-03-11`, um modelo `preview` de busca — e é isso que sumiu dos catálogos de agregadores.

**Se eu uso o alias `gpt-4o` sem data, quebro em 23 de outubro?**
Provavelmente não, porque o alias resolve hoje para `gpt-4o-2024-11-20`, que não está na lista. Mas você fica exposto a remapeamento silencioso do alias. Pinar snapshot e monitorar a [página de deprecações](https://developers.openai.com/api/docs/deprecations) é a postura defensável.

**Preciso ir para o `gpt-5.6-sol` como a OpenAI recomenda?**
Não. A coluna de substituto é sugestão, não regra. Para classificação, extração e roteamento, o `gpt-5.6-luna` é mais barato que o próprio `gpt-4o` nos dois lados da conta. Decida por eval e por custo real, não pela tabela.

**Como eu fico sabendo da próxima onda antes do portal de notícia?**
A página de deprecações é a fonte primária e é atualizada antes de qualquer cobertura. Coloca ela no seu monitoramento de mudança de página. O anúncio de 20 de julho sobre áudio e realtime esteve lá dias antes de virar manchete.

## Fecha assim

O fim do GPT-4o na versão `2024-05-13` é real, a data é 23 de outubro de 2026, e a lista tem doze model IDs — dos quais o do GPT-4o é só o mais famoso. O que não é real é a versão de que a OpenAI puxou o tapete sem aviso: houve seis meses de antecedência e uma tabela de substituição publicada. A dor verdadeira não é a data. É que o substituto oficial custa 2x no input e 3x no output, é que fine-tune não migra, e é que ninguém tem eval o suficiente para saber se o modelo novo vai se comportar igual no caso específico que paga a conta.

Faz o inventário essa semana. Roda a conta de custo com os seus tokens. Congela cinquenta casos de eval. Oitenta e oito dias é prazo confortável para quem começa agora e prazo apertado para quem começa em outubro.

E se você quer acompanhar o próximo capítulo dessa história — porque vai ter próximo capítulo —, o [rastreador do GPT-6](https://blog.beerandcode.com.br/noticias/gpt-6-lancamento-rastreador) separa o que é fato do que é boato, com data e fonte em cada linha. Vale também [o que os primeiros testes reais do Sol Ultra no Codex](https://blog.beerandcode.com.br/noticias/gpt-5-6-sol-ultra-codex) mostraram, se o seu destino de migração for o Sol.
