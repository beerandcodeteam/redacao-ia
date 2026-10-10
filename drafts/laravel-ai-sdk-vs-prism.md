Digita "laravel ai sdk vs prism" no Google e você vai encontrar duas afirmações confiantes e contraditórias. Metade dos posts diz que o SDK oficial matou o Prism. A outra metade jura que o SDK **usa** o Prism por baixo dos panos — alguns até citam a linha `prism-php/prism: ^0.99.0` no `composer.json`.

A segunda é falsa. Dá pra checar em dez segundos.

O `composer.json` do `laravel/ai` não tem `prism-php/prism` em lugar nenhum. Nem em `require`, nem em `require-dev`, nem em `suggest`. São dois pacotes independentes, escritos por gente diferente, que se sobrepõem em boa parte do escopo e divergem justamente onde a sua decisão de arquitetura acontece.

Neste post: o que cada um faz de fato, o código lado a lado, a tabela do que só existe em um deles, um dado de manutenção que quase ninguém olha antes de escolher, e um guia de decisão por caso concreto — não por "depende".

## TL;DR

- **O que é:** dois pacotes de IA para Laravel com escopos diferentes. Prism é uma camada de integração com LLM; o Laravel AI SDK é uma plataforma de IA dentro do framework.
- **Stack:** Prism roda em PHP 8.2+ e Laravel 11, 12 ou 13. O AI SDK exige PHP 8.3+ e Laravel 12 ou 13.
- **Custo/Acesso:** os dois são MIT e gratuitos. Você paga o token do provedor.
- **Links úteis:** [documentação do Prism](https://prismphp.com/getting-started/introduction/) e [documentação do Laravel AI SDK](https://laravel.com/docs/13.x/ai-sdk).

## Prism PHP e Laravel AI SDK: por que a comparação está mal formulada

O Prism nasceu em fevereiro de 2024, feito pelo TJ Miller. Ele resolve um problema específico e resolve bem: dar uma interface fluente e única para falar com vários provedores de LLM sem reescrever código quando você troca de modelo. É uma camada de roteamento. A [própria Laravel descreveu assim](https://laravel.com/blog/prism-makes-ai-feel-laravel-native-the-artisan-of-the-day-is-tj-miller) quando destacou o TJ na comunidade: "uma camada de roteamento Laravel-native para modelos de IA".

O Laravel AI SDK [foi anunciado em 5 de fevereiro de 2026](https://laravel-news.com/laravel-announces-official-ai-sdk-for-building-ai-powered-apps), junto com o Boost e o Laravel MCP. O escopo é outro. Ele também faz roteamento de provedor, mas empacota junto agente como classe PHP, persistência de conversa em tabela, vector store, reranking, geração de imagem, transcrição de áudio, tools de sistema de arquivos e fakes de teste para tudo isso.

Um é um cabo. O outro é uma tomada com quadro de distribuição. Chamar de concorrente esconde a única pergunta que importa: **você precisa de quanto disso?**

E aqui vale o aviso que ninguém dá: escolher o pacote é a parte fácil. Trocar de pacote é refactor de uma tarde — o que não se troca depois é o critério de arquitetura em volta dele, que é onde os projetos de IA realmente quebram. Esse critério é o que a gente constrói ao vivo toda semana no [Clã Beer and Code](https://beerandcode.com.br?utm_source=blog&utm_medium=post&utm_campaign=laravel-ai-sdk-vs-prism&utm_content=g-n1), com sistema rodando e decisão sendo discutida na hora. Se a sua praia é colecionar tutorial, lá vai te frustrar: a régua é o que você coloca de pé.

## O mesmo "hello world" nos dois

Nada explica escopo melhor que código. Geração de texto simples, primeiro no Prism:

```php
use Prism\Prism\Facades\Prism;
use Prism\Prism\Enums\Provider;

$response = Prism::text()
    ->using(Provider::Anthropic, 'claude-3-7-sonnet-latest')
    ->withSystemPrompt(view('prompts.system'))
    ->withPrompt('Explique idempotência em uma API REST.')
    ->asText();

echo $response->text;
```

Repare no `view('prompts.system')`. Prompt como Blade view é um idioma que o Prism inventou e que continua sendo um dos jeitos mais limpos de versionar prompt com variável dentro. Você ganha `@if`, `@foreach` e partial reaproveitável de graça.

Agora o mesmo no AI SDK:

```php
use function Laravel\Ai\agent;
use Laravel\Ai\Enums\Lab;

$response = agent(
    instructions: 'Você é um assistente técnico. Responda direto.',
)->prompt('Explique idempotência em uma API REST.', provider: Lab::Anthropic);

echo (string) $response;
```

Empatou. Nesse nível de uso — mandar texto, receber texto — a diferença entre os dois é estética. Quem te disser que um é "muito melhor" para isso está vendendo alguma coisa.

A divergência começa quando a feature cresce. No AI SDK, agente é classe:

```php
<?php

namespace App\Ai\Agents;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Concerns\RemembersConversations;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;
use Stringable;

#[Provider(Lab::OpenAI, Lab::Anthropic)]
class AnalistaDeChamado implements Agent, HasStructuredOutput
{
    use Promptable, RemembersConversations;

    public function instructions(): Stringable|string
    {
        return 'Analise o chamado de suporte e devolva a classificação.';
    }

    public function schema(JsonSchema $schema): array
    {
        return [
            'categoria' => $schema->string()->enum(['bug', 'duvida', 'billing'])->required(),
            'urgencia'  => $schema->integer()->min(1)->max(5)->required(),
        ];
    }
}
```

Aquele `#[Provider(Lab::OpenAI, Lab::Anthropic)]` é failover declarativo: OpenAI cai ou estoura rate limit, ele tenta Anthropic. O `RemembersConversations` persiste o histórico nas tabelas que a migration do pacote cria. Duas linhas para dois problemas que, no Prism, você resolve escrevendo código.

Não é magia — é escopo. O Prism tomou a decisão consciente de não entrar nessa camada.

## Onde os escopos divergem de verdade

Este é o quadro que resolve a discussão. Só o que é assimétrico:

| Recurso | Prism | Laravel AI SDK |
|---|---|---|
| Geração de texto, streaming, tools | sim | sim |
| Structured output com schema | sim | sim |
| Multimodal (imagem, documento, áudio, vídeo) | sim | sim |
| Fakes para teste | sim | sim |
| **Prompt como Blade view** | **sim** | não (string ou `Stringable`) |
| **Prism Server (expõe seus modelos numa API OpenAI-compatible)** | **sim** | não |
| **Provedor Perplexity** | **sim** | não |
| **Moderação de conteúdo** | **sim** | não |
| **Laravel 11 / PHP 8.2** | **sim** | não (exige Laravel 12+ e PHP 8.3+) |
| **Agente como classe com atributos** | não | **sim** |
| **Persistência de conversa (migrations prontas)** | não | **sim** |
| **Failover automático entre provedores** | não | **sim** |
| **Vector store + `whereVectorSimilarTo` no Eloquent** | não | **sim** |
| **Reranking (Cohere, Jina, VoyageAI)** | não | **sim** |
| **Human-in-the-loop: aprovar tool antes de executar** | não | **sim** |
| **Tools de filesystem prontas** | não | **sim** |
| **`Str::summarize()`** | não | **sim** |
| **Embeddings multimodais (imagem e áudio)** | não | **sim** |

As quatro últimas linhas do lado do SDK são recentes: saíram [no Laracon US 2026, em 29 de julho](https://laravel.com/blog/everything-we-announced-at-laracon-us-2026). É a melhor evidência de que a comparação não é entre iguais — o SDK está expandindo escopo para lugares que o Prism nunca prometeu ocupar.

Do outro lado, o **Prism Server** é o recurso mais subestimado dessa tabela. Ele [expõe seus modelos configurados numa API compatível com a da OpenAI](https://prismphp.com/core-concepts/prism-server/), o que significa que qualquer UI de chat ou SDK que fale o protocolo da OpenAI conversa com o seu Laravel sem adaptador. Se o seu caso é "quero plugar um front pronto na minha camada de IA", isso sozinho decide a escolha.

## O dado de manutenção que quase ninguém olha

Antes de casar com um pacote, olhe a cadência de release. Os números públicos, em agosto de 2026:

| | Prism | Laravel AI SDK |
|---|---|---|
| Versão atual | v0.100.1 | v0.10.3 |
| Data do último release | 20/03/2026 | 06/08/2026 |
| Instalações (Packagist) | ~5,9 milhões | ~5,5 milhões |
| Issues abertas | 117 | — |

Leia isso com honestidade, porque dá pra distorcer para os dois lados.

O [Prism está há cerca de cinco meses sem release](https://packagist.org/packages/prism-php/prism) e o repositório não recebe push desde 20 de março. Isso não quer dizer "abandonado" — quer dizer que o pacote está estável e que o autor foi fazer outras coisas. Código que funciona não some. Mas com 117 issues abertas e uma área que muda a cada seis semanas, é um risco que você precisa precificar: modelo novo do provedor, mudança de contrato de API, correção de segurança. Quem responde?

O [`laravel/ai` está em v0.10.3, lançado em 6 de agosto](https://packagist.org/packages/laravel/ai), com release praticamente mensal. Cadência é bom sinal de vida e péssimo sinal de estabilidade. Repare no número: **nenhum dos dois chegou em 1.0.** Major zero significa que semver não te protege de nada. Pinne a versão exata no `composer.json` e leia o CHANGELOG antes de subir minor em produção. Vale para os dois.

## Laravel AI SDK vs Prism: qual usar em cada caso

Sem "depende". Ache o seu caso na lista.

**Você está em Laravel 11 ou PHP 8.2.** Prism. Não é preferência, é constraint: o `laravel/ai` exige `php: ^8.3` e `illuminate/*` em `^12.0|^13.0`. Ou você atualiza o runtime primeiro, ou a decisão já foi tomada por você.

**Projeto novo, feature simples de texto** (resumir, classificar, extrair, gerar copy). AI SDK. Não porque o Prism não dá conta — dá — mas porque em projeto novo você vai querer o resto do ecossistema oficial depois, e começar já dentro dele evita uma migração daqui a seis meses.

**Agente com memória de conversa entre requisições.** AI SDK, sem discussão. O `RemembersConversations` mais as migrations prontas resolvem em duas linhas o que é um schema, um repositório e uma política de truncamento de histórico escritos à mão.

**RAG com busca vetorial e reranking.** AI SDK. O `whereVectorSimilarTo` no Eloquent e o rerank first-party com Cohere, Jina ou VoyageAI economizam a camada que todo mundo escreve errado na primeira vez.

**Você precisa expor sua camada de IA como API OpenAI-compatible.** Prism, pelo Prism Server. O SDK aceita consumir qualquer provedor OpenAI-compatible, mas não faz o caminho inverso.

**Perplexity é obrigatório na sua stack.** Prism. Ele é o único dos dois com suporte first-party.

**Seus prompts são longos, com variável, e mudam toda semana.** Prism, pelo prompt em Blade view. Dá pra reproduzir isso no SDK passando um `Stringable` que renderiza uma view, mas no Prism é o caminho oficial e documentado.

**Sua tool escreve no banco, apaga arquivo ou dispara e-mail.** AI SDK, pela API de human-in-the-loop. Poder interceptar a chamada de tool e exigir aprovação humana antes da execução não é conforto: em agente com permissão de escrita, é controle de risco.

**Você já roda Prism em produção e está funcionando.** Fica. Migração sem dor não é motivo, é hobby caro. Migre quando bater numa das linhas de cima — aí a conta fecha. Se for esse o caso, [já abrimos o diff de uma migração real de Prism para o SDK](https://blog.beerandcode.com.br/noticias/laravel-ai-sdk-vale-migrar-do-prism) num projeto de verdade.

## Se você for migrar, três coisas quebram

Quem já fez o caminho [documentou os tropeços](https://notesonlaravel.com/laravel-ai-sdk-migration/), e os três valem o preço da leitura:

1. **`#[Temperature]` derruba modelos novos.** Modelos como `gpt-5-mini` e `gpt-5-nano` não aceitam o parâmetro `temperature` e devolvem HTTP 400. Se você trouxe a temperatura do Prism por reflexo, remova o atributo.
2. **`withoutAdditionalProperties()` não desce sozinho.** O modo estrito da OpenAI exige a flag em objetos aninhados do schema, e o SDK só aplica automaticamente na raiz. Schema com objeto dentro de objeto falha em silêncio até você descer manualmente.
3. **`catch (Exception $e)` não pega tudo.** Use `catch (Throwable $e)`. É a convenção do próprio Laravel e é o que captura os erros mais profundos de PHP que aparecem em chamada de LLM.

Além disso, a mudança conceitual: você sai de **um service genérico** que toda feature de IA chamava, e entra em **uma classe de agente por tarefa**. Não tente traduzir o service linha a linha. É reescrita de arquitetura, não find-and-replace.

## Limitações e pontos de atenção

**Os dois são 0.x.** Já falei acima e repito porque é o item que mais dói: em major zero, um minor pode quebrar sua build. Pin exato, CHANGELOG lido, e uma suíte de teste com os fakes de cada pacote.

**Nenhum dos dois é engenharia de IA.** Os dois te dão cliente HTTP, retry, schema e mock. Nenhum decide qual contexto o modelo recebe, como você mede se a resposta presta, quanto aquilo custa por requisição ou o que fazer quando o provedor cai. Trocar de pacote não conserta um sistema de IA ruim — só troca a sintaxe do erro.

**Custo é invisível até chegar a fatura.** Nos dois casos, logue o `usage` da resposta desde o primeiro dia. Um agente com múltiplos passos pode fazer dez chamadas ao modelo dentro de um único `prompt()`, e essa conta não aparece em lugar nenhum se você não gravar.

**Prompt injection é seu problema, não do pacote.** Nenhum dos dois sanitiza entrada. Se a tool tem permissão de escrita, trate como endpoint público: valide argumento, escope por usuário autenticado e considere aprovação humana antes de executar.

**Não jogue dado de cliente no prompt sem pensar.** Provedor de LLM é terceiro. Máscara em PII, ou modelo local via Ollama — suportado pelos dois.

## FAQ rápido

**O Laravel AI SDK usa o Prism por baixo dos panos?**
Não. O `composer.json` do `laravel/ai` requer `php ^8.3`, `aws/aws-sdk-php`, os componentes `illuminate/*`, `laravel/prompts` e `laravel/serializable-closure`. `prism-php/prism` não aparece. A confusão provavelmente vem de conteúdo gerado sem checar a fonte — e virou fato repetido.

**Dá pra usar os dois no mesmo projeto?**
Dá. São namespaces distintos e não conflitam. Mas escolha um por feature: dois caminhos de chamada de LLM no mesmo repositório é exatamente a bagunça que esses pacotes existem para acabar.

**O Prism está morto?**
Não. Está estável e sem release desde março de 2026, o que é diferente. Continua com quase 6 milhões de instalações e roda em produção em muito lugar. O que você precisa avaliar é o tempo de resposta a uma mudança de API de provedor, não se o código funciona hoje.

**Qual tem mais provedor?**
Depende da capacidade. Para texto, empatam na prática. Para embeddings e reranking, o AI SDK tem mais (Cohere, Jina, VoyageAI). Para o resto, o Prism tem Perplexity e o SDK não. Conte por capacidade, não por marca no site.

**Preciso do Laravel 13 para o AI SDK?**
Não. Laravel 12 roda — os `illuminate/*` são pinados em `^12.0|^13.0`. O requisito duro é PHP 8.3. Se você quer o panorama completo do pacote antes de escolher, tem o [guia prático do Laravel AI SDK](https://blog.beerandcode.com.br/tutoriais/o-que-e-laravel-ai-sdk) do `composer require` ao primeiro agente rodando.

## O que fazer com isso

A comparação certa não é "qual é melhor". É "qual escopo eu preciso". Prism entrega uma camada de integração enxuta, com dois recursos que o oficial não tem — Prism Server e prompt em Blade — e a vantagem de rodar em stack mais antiga. O AI SDK entrega uma plataforma: agentes, memória, vector store, rerank, aprovação humana, e a cadência de quem tem time pago para manter.

Se você está começando hoje em Laravel 12 ou 13, o SDK oficial é a escolha padrão. Se você tem constraint de runtime, precisa de Prism Server, ou já tem Prism em produção funcionando — fica onde está, com a versão pinada.

E depois que a escolha estiver feita, o trabalho de verdade começa: decidir o que entra no contexto, como medir a resposta, e o que acontece às três da manhã quando o provedor devolve 503. Nenhum dos dois pacotes resolve isso por você. Essa parte continua sendo engenharia.
