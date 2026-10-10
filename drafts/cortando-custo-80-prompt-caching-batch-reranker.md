# Cortando custo em 80%: prompt caching, batch e quando NÃO usar reranker

A maioria dos agentes em produção sangra dinheiro. Não em treinamento. Não em GPU. Em chamada repetida pra LLM.

Você tem um system prompt de 8 mil tokens com regras, ferramentas, exemplos de few-shot. Reenvia ele a cada turno. Soma uma camada de RAG que faz busca vetorial e ainda joga um reranker em cima por reflexo. No fim do mês a fatura assusta — e o feature funcionava igual com metade do bolt-on.

Este post é sobre três alavancas que mexem o ponteiro: [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) pra zerar o custo do system prompt repetido, [Batch API](https://platform.claude.com/docs/en/build-with-claude/batch-processing) pra todo workload assíncrono, e a decisão fria de quando o reranker é só caro e lento.

## TL;DR

- **O que é:** combinação de cache de prompt, processamento em lote e enxugamento de pipeline RAG pra reduzir custo de LLM em produção.
- **Stack/Modelos:** Claude (Sonnet 4.6, Opus 4.7, Haiku 4.5), OpenAI GPT-4o, Cohere Rerank 3.5.
- **Custo/Acesso:** todas as features cobertas estão disponíveis no plano padrão da API.
- **Links úteis:** [docs Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [docs Batch API](https://platform.claude.com/docs/en/build-with-claude/batch-processing), [OpenAI prompt caching](https://openai.com/index/api-prompt-caching/), [Pinecone reranker guide](https://www.pinecone.io/learn/series/rag/rerankers/).

## Onde o dinheiro vaza

Antes de otimizar, mapeia o vazamento.

Um agente de produção típico tem três pontos onde o token queima fora de proporção:

1. **System prompt fixo.** Regras do agente, descrição de ferramentas, exemplos. 4 a 12 mil tokens. Vai inteiro a cada turno do usuário.
2. **Workload assíncrono em lote.** Análise de reviews, classificação de tickets, enrichment de catálogo. Mil documentos por dia, cada um virando uma chamada síncrona.
3. **Pipeline RAG empilhado.** Busca vetorial → reranker → LLM. O reranker entra por reflexo, não por medida.

Os três têm tratamento diferente. Vamos um a um.

## Pré-requisitos

- Conta na Anthropic, OpenAI ou ambas.
- Familiaridade com `messages.create` (Claude) ou `chat.completions` (OpenAI).
- Saber medir custo: log de `input_tokens`, `output_tokens` e, se for Claude, `cache_read_input_tokens` e `cache_creation_input_tokens`.

Se você não loga isso, pare aqui. Otimizar sem medição é fé.

## Alavanca 1: prompt caching no system prompt do harness

O system prompt do seu agente muda raramente. As mensagens do usuário mudam o tempo todo. É a definição perfeita de cache.

### Como funciona na Anthropic

Você marca os blocos estáveis com `cache_control`. Anthropic armazena. Da próxima chamada até 5 minutos depois (ou 1 hora, se você pagar a mais no write), o cache hit custa **0.10× o preço do input base**. É 90% de desconto na leitura.

A conta do write não é grátis: 5min TTL custa **1.25×** o input e 1h TTL custa **2.0×**. Mas isso é cobrado uma vez. Toda chamada subsequente que bate no cache lê barato.

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": SYSTEM_PROMPT_GIGANTE,  # 8k tokens, estável
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": pergunta_do_usuario}]
)

print(response.usage.cache_read_input_tokens)
print(response.usage.cache_creation_input_tokens)
```

Detalhes que doem se você ignorar:

- **Mínimo de tokens cacheáveis varia por modelo.** Opus 4.7, 4.6, 4.5 e Haiku 4.5 exigem **4.096 tokens** por breakpoint. Sonnet 4.6 exige **2.048**. Modelos mais antigos, **1.024**. Abaixo do mínimo, o `cache_control` é silenciosamente ignorado — sem erro, sem aviso.
- **No máximo 4 cache breakpoints** distribuídos entre tools, system e messages. Use cada um com critério.
- **Hierarquia do cache: tools → system → messages.** Mude um item no topo e invalida tudo abaixo.

A primeira chamada vai custar 1.25× pro pedaço cacheado. Da segunda em diante, 0.10×. Se seu agente faz 20 turnos numa sessão, você paga 1.25× uma vez e 0.10× nas outras 19. Faz a conta.

### Como funciona na OpenAI

Aqui é mais simples e mais limitado. O [prompt caching da OpenAI](https://openai.com/index/api-prompt-caching/) é **automático**: prefixos repetidos com 1.024+ tokens entram em cache, com granularidade de 128 tokens. O hit custa **50% do input normal**. Sem `cache_control`, sem decisão sua. Pague sempre menos no que se repetir.

A consequência prática: estruture seu prompt com o que é estável **no começo**. System primeiro, contexto fixo depois, mensagem do usuário no fim. Inverter isso é deixar dinheiro na mesa.

### Quanto isso vale na prática

Suponha um agente em Sonnet 4.6 com system prompt de 6k tokens e o usuário mandando 500 tokens por turno. Em 100 turnos:

- **Sem cache:** 100 × 6.500 tokens de input = 650k tokens × $3/MTok = **$1,95**.
- **Com cache (5min TTL):** 1 write de 6k a 1.25× ($0,0225) + 99 reads a 0.10× ($0,18) + 100 × 500 tokens fora do cache ($0,15) = **$0,35**.

Reduziu **82% só no system prompt repetido**. E sem mexer em código de produto.

## Alavanca 2: Batch API para tudo que não precisa de resposta agora

Toda análise em massa que você faz de forma síncrona está pagando preço de varejo.

A [Message Batches API](https://platform.claude.com/docs/en/build-with-claude/batch-processing) da Anthropic processa lotes assíncronos com **50% de desconto em input e output**. SLA de 24h. Na prática, a maioria termina em menos de 1 hora.

Casos de uso óbvios:

- Análise de sentimento de 10 mil reviews que vão pra dashboard de produto.
- Classificação de tickets de suporte do dia anterior.
- Enrichment de catálogo (gerar título, descrição, tags) pra produtos novos.
- Avaliações em massa (LLM-as-a-judge) sobre dump de logs.

Se a feature pode esperar uma hora, ela tem que rodar em batch. Não é otimização, é o default certo.

```python
batch_response = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"review-{review.id}",
            "params": {
                "model": "claude-haiku-4-5",
                "max_tokens": 256,
                "system": [
                    {
                        "type": "text",
                        "text": PROMPT_CLASSIFICACAO,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                "messages": [{"role": "user", "content": review.texto}]
            }
        }
        for review in reviews_do_dia
    ]
)
```

E o melhor: **batch e prompt caching empilham**. O system prompt cacheado dentro do batch também ganha o desconto de leitura. Em lote de 10 mil itens com system prompt comum, você combina 50% (batch) com 90% (cache read) — o desconto efetivo no input se aproxima de 95%.

Na OpenAI vale o mesmo princípio. A combinação de Batch (50%) com cache automático produz, segundo a própria OpenAI, **até 75% off no agregado**.

Limites a respeitar:

- 24h é o teto, não o esperado. Se sua feature precisa de SLA de minutos, batch não serve.
- Resultado vem todo de uma vez. Você não consegue stream parcial.
- Não é elegível pra Zero Data Retention. Se compliance exige ZDR, batch sai do menu.

## Alavanca 3: quando o reranker é desperdício puro

Aqui é onde a maioria dos pipelines RAG queima dinheiro por reflexo.

Reranker é um cross-encoder que pega top-N da busca vetorial e reordena por relevância. [Cohere Rerank 3.5](https://cohere.com/pricing) custa **$2 por 1.000 buscas** (cada busca = 1 query com até 100 documentos). Latência adicional de **100 a 300ms** por chamada. Documentos com mais de 500 tokens são chunked, e cada chunk conta como documento separado.

Em pipeline grande, isso vira número sério. Servir 1 milhão de queries reordenando top-10 num corpus de 10 milhões é, em compute, equivalente a indexar o corpus inteiro de novo.

A pergunta certa não é "devo usar reranker?". É "minha busca já é cirúrgica?".

### Quando reranker NÃO faz sentido

- **Corpus pequeno e bem estruturado.** Algo como 5 mil documentos, vocabulário consistente, busca híbrida (BM25 + vetorial) já calibrada. O reranker entra pra ajustar a 5ª casa decimal.
- **Retrieval já acerta no top-1.** Se a métrica de avaliação mostra que a resposta certa aparece em primeiro lugar na maioria das queries, reranking só adiciona latência.
- **Latency budget apertado.** Agente conversacional com SLA de 800ms total não pode pagar 200ms só pra reordenar.
- **Domínio com query expansion agressivo.** Se você reescreve a query antes da busca, o trabalho do reranker já foi feito upstream.

### Quando reranker SALVA o pipeline

- **Corpus heterogêneo de centenas de milhares de docs.** Embedding generalista perde nuance.
- **Recall alto, precisão baixa.** Você puxa top-100 com confiança, mas top-10 mistura ruído.
- **Domínio com vocabulário ambíguo.** Termo técnico que tem sentidos diferentes por contexto.

A regra de bolso: **mede antes**. Avalia o pipeline sem reranker. Se NDCG@5 ou MRR já estão em níveis aceitáveis pro seu produto, o reranker é gordura.

> O default da indústria virou empilhar reranker. O default certo é medir. Reranker que não move métrica é só latência cara.

## Limitações e pontos de atenção

Três armadilhas comuns:

1. **Cache TTL e variabilidade.** Se seu agente tem rajadas de tráfego com gap de 7 minutos, o cache de 5min expira sempre. Avalie 1h TTL — paga 2× no write, mas se sua densidade de hits compensa, vale.
2. **Mudanças no system prompt invalidam o cache inteiro.** A/B testes em prompt destroem economia. Estabilize antes de cachear, não cacheia em ambiente de experimentação.
3. **Batch não é ZDR.** Se você processa dado regulado (saúde, financeiro), confirma com o jurídico antes de jogar em batch.

E sobre reranker: nunca tire reranker de produção sem rodar avaliação offline antes. Custo cai, mas se a precisão despencar, sua feature pode quebrar de um jeito difícil de detectar (resposta plausível, mas baseada no contexto errado).

## Quer mergulhar mais fundo nisso

Custo de LLM em produção é arquitetura, não billing. Quem trata como billing fica preso em planilha. Quem trata como arquitetura constrói feature real com IA, mede impacto, e escala sem queimar margem.

É exatamente esse o nível de prática que rola dentro do **[Clã Beer & Code](https://beerandcode.com.br)**. Discussão técnica de verdade, projetos com dado real, e mentoria sobre construir produto com IA — não brincar de prompt.

Se isso ressoa, [entra no Clã](https://beerandcode.com.br) e vem trocar com a galera.

## FAQ

**Por que meu cache_control não está funcionando?**

Provavelmente o bloco que você marcou tem menos tokens que o mínimo do modelo. Opus 4.7 e Haiku 4.5 exigem 4.096 tokens. Sonnet 4.6 exige 2.048. Cheque `cache_creation_input_tokens` na resposta — se vier zero, o marker foi ignorado.

**Posso combinar Anthropic cache com OpenAI cache no mesmo agente?**

Sim, tratando cada provider isoladamente. Cada um tem mecânica própria. Anthropic é explícita (cache_control), OpenAI é automática. Não há cache cross-provider.

**Batch e streaming são compatíveis?**

Não. Batch é assíncrono por definição. Se você precisa de stream de tokens em tempo real, use a API síncrona normal — e cacheia o system prompt pra não pagar full price.

**Reranker grátis (open-source) muda a equação?**

Muda parcialmente. Modelos como [FlashRank](https://github.com/PrithivirajDamodaran/FlashRank) eliminam o custo financeiro, mas a latência continua. E a pergunta segue: o reranker está movendo sua métrica? Se não, ainda é desperdício, agora só de tempo.

## Conclusão

Três alavancas, três decisões.

Cache no system prompt: 80% a 90% de desconto no input repetido, com pouco código.

Batch API: 50% de desconto em tudo que aceita esperar 1 hora — e empilha com cache.

Reranker: só com medição. Sem evidência de ganho, sai do pipeline.

Custo de LLM em produção não é problema de planilha. É problema de arquitetura. Quem mede, decide. Quem só copia padrão da indústria, paga conta de hype.
