A AWS escreve uma documentação ótima sobre como ligar o AWS Bedrock. Console, "Enable model access", três cliques, primeira chamada respondendo. Bonito.

Ninguém escreve sobre o resto.

Ninguém escreve sobre a diferença entre CloudTrail e model invocation logging — e por que a primeira não te salva numa auditoria. Ninguém escreve que a região de São Paulo existe no Bedrock mas não te dá residência de dados. E ninguém escreve o que aparece na fatura no fim do mês, convertido pra real, com IOF em cima.

Este post é sobre isso. Vamos ver o que é o AWS Bedrock na prática, ligar o Claude nele, fechar as quatro camadas de governança que uma empresa séria vai te cobrar, e fazer a conta em real de um agente interno rodando de verdade.

## TL;DR

- **O que é:** o AWS Bedrock é o serviço gerenciado da AWS que serve modelos de fundação (incluindo o Claude, da Anthropic) por API, dentro da sua conta AWS, com IAM, VPC, CloudTrail e billing nativos.
- **Stack:** Python + `anthropic[bedrock]`, IAM, CloudWatch/S3, Bedrock Guardrails.
- **Custo/acesso:** mesmo preço por token da API direta da Anthropic. Endpoint regional custa 10% a mais. Batch é 50% mais barato.
- **Link útil:** [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock) e [Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/).

## AWS Bedrock: o que é, na prática

AWS Bedrock é um serviço gerenciado que expõe modelos de fundação de vários fornecedores — Anthropic, Meta, Mistral, Amazon, Cohere — atrás de uma API única, dentro da sua conta AWS.

Isso é a definição. O que ela significa na prática é mais interessante: **quando você chama o Claude pelo Bedrock, a chamada não sai do seu perímetro AWS.** Autenticação é SigV4 com IAM. O tráfego pode ir por PrivateLink. A cobrança cai na mesma fatura do RDS e do S3. E, segundo a documentação da Anthropic, a infraestrutura de inferência roda com *zero operator access* — ninguém da Anthropic tem acesso a ela.

O que o Bedrock **não** é: um proxy transparente pra API da Anthropic. Ele é um produto operado pela AWS, com o próprio ciclo de release, o próprio subconjunto de features e os próprios IDs de modelo. Tratar os dois como intercambiáveis é o erro que mais custa caro na migração — e vamos ver exatamente onde ele dói.

Uma coisa mudou e vale registrar: a integração atual do Claude no Bedrock serve a **Messages API** no endpoint `https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages`. É o mesmo formato de request da API de primeira parte. A integração antiga (`InvokeModel` e `Converse`, com aqueles IDs versionados em ARN tipo `anthropic.claude-sonnet-4-5-20250929-v1:0`) continua existindo, mas é caminho legado. Código novo vai no Mantle.

## O contexto: por que passar o Claude pelo Bedrock

A pergunta certa não é "qual é mais barato". Por token, é o mesmo preço: Haiku 4.5 a US$ 1/US$ 5, Sonnet a US$ 3/US$ 15, Opus a US$ 5/US$ 25 por milhão de tokens de entrada/saída — [idêntico nos dois caminhos](https://www.cloudzero.com/blog/claude-on-aws-bedrock/).

A pergunta certa é: **quem precisa assinar embaixo?**

Se a resposta for "eu", use a API direta da Anthropic. Você ganha structured outputs, Files API, server-side tools, Managed Agents e acesso a feature nova no dia do lançamento.

Se a resposta envolver um time de segurança, um DPO, um auditor ou um contrato com cláusula de residência de dados, o Bedrock ganha por um motivo só: ele fala a língua que essas pessoas já falam. Não existe "processo de aprovação de fornecedor de IA" — existe uma policy de IAM, um log no CloudTrail e uma linha na fatura da AWS que o financeiro já reconcilia todo mês.

Esse é o tipo de decisão que separa protótipo de produto: não é sobre o modelo ser bom, é sobre a arquitetura passar no comitê. É exatamente esse recorte que a gente destrincha ao vivo no [Clã Beer and Code](https://beerandcode.com.br) — sistemas com IA construídos na frente de todo mundo, com código rodando e a conta aberta na tela.

## Pré-requisitos

- Conta AWS com **model access** habilitado para o modelo que você vai usar (console do Bedrock → Model access). Claude Fable 5, Opus 4.8, Sonnet 5, Opus 4.7 e Haiku 4.5 são abertos pra qualquer cliente Bedrock.
- Credenciais AWS resolvidas pela cadeia padrão (env vars, `~/.aws/config`, SSO, role de task no ECS, IMDS).
- Python 3.11+ com `pip install -U "anthropic[bedrock]"`.
- Permissão IAM de `bedrock-mantle:CreateInference` nos ARNs dos modelos liberados.

## Como usar o AWS Bedrock: a primeira chamada

### Passo 1: o client e o ID do modelo

O SDK da Anthropic tem um client dedicado pro Bedrock. Ele resolve credenciais e região pela precedência padrão da AWS e assina em SigV4.

```python
from anthropic import AnthropicBedrockMantle

client = AnthropicBedrockMantle(aws_region="us-east-1")

message = client.messages.create(
    model="anthropic.claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)

print(next(b.text for b in message.content if b.type == "text"))
```

Repare no `anthropic.` na frente do ID do modelo. **Esse prefixo é obrigatório no Bedrock e não existe na API direta.** Se você copiou um trecho de código da doc de primeira parte e mandou `model="claude-opus-5"`, toma 404. É a primeira pedra do caminho e a que mais consome tempo de gente que "já sabe usar o Claude".

Se preferir cURL, o shape é o mesmo — só muda a assinatura:

```bash
curl https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages \
  --aws-sigv4 "aws:amz:us-east-1:bedrock-mantle" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "anthropic.claude-opus-5",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello, Claude"}]
  }'
```

### Passo 2: escolher o endpoint (e descobrir que São Paulo não resolve residência)

Aqui mora a armadilha que ninguém conta.

O Bedrock oferece dois tipos de endpoint: **Global**, que roteia dinamicamente entre todas as regiões disponíveis, e **Regional**, que resolve pra uma região só — o caminho pra quem tem exigência de residência de dados. O endpoint regional custa **10% a mais** que o global.

Agora olhe a tabela de regiões da documentação: `sa-east-1` (South America, São Paulo) aparece com **um único tipo de endpoint suportado: Global.**

Ou seja: você *pode* chamar o Claude a partir de São Paulo, mas a inferência vai ser roteada globalmente. Não existe perfil geográfico "SA" como existe US, EU, JP e AU. Se o contrato do seu cliente diz "os dados não saem do Brasil", o Claude no Bedrock não atende esse requisito hoje — e descobrir isso depois de o time jurídico ter aprovado a arquitetura é um problema caro.

Para quem tem residência regional (EU, US, JP, AU), o caminho é o **inference profile geográfico** — aqueles IDs com prefixo `us.`, `eu.`, `apac.`. A [documentação da AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/geographic-cross-region-inference.html) é explícita sobre a nuance: a requisição fica dentro da geografia, mas "seus prompts de entrada e resultados de saída podem se mover para fora da sua região de origem" durante o roteamento cross-region.

### Passo 3: o erro 403 que parece problema de permissão e não é

Se sua organização usa SCP pra bloquear regiões não utilizadas — e a maioria das empresas grandes usa — o inference profile geográfico vai quebrar.

Motivo: um profile `us.` roteia entre `us-east-1`, `us-east-2` e `us-west-2`. Se a SCP libera só `us-east-1`, a chamada falha quando o roteador escolhe outra região. O erro chega como 403 e parece falta de permissão no modelo. Não é: é a SCP barrando a região de destino.

A policy correta libera o profile **e** o foundation model em todas as regiões de destino:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "GrantInferenceProfileAccess",
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": [
        "arn:aws:bedrock:us-east-1:<ACCOUNT_ID>:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
      ]
    },
    {
      "Sid": "GrantModelAccessInAllDestinations",
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0",
        "arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0",
        "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-sonnet-4-5-20250929-v1:0"
      ],
      "Condition": {
        "StringEquals": {
          "bedrock:InferenceProfileArn": "arn:aws:bedrock:us-east-1:<ACCOUNT_ID>:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
        }
      }
    }
  ]
}
```

A condition `bedrock:InferenceProfileArn` é o detalhe que vale ouro: ela libera as regiões de destino **só** quando a chamada vem pelo profile aprovado. Sem ela, você abriu três regiões pra qualquer invocação.

## Governança: as quatro camadas

Governança no Bedrock não é uma feature, é a composição de quatro controles independentes. Falhar em qualquer um deles invalida os outros.

### 1. Quem pode chamar o quê (IAM + SCP)

O básico: policy de identidade limitando `bedrock-mantle:CreateInference` aos ARNs dos modelos homologados. O menos básico: usar IAM para **forçar** o guardrail. Você pode negar qualquer requisição de inferência que não venha com um identificador de guardrail aprovado. Sem isso, o guardrail é opcional na prática — e o que é opcional é ignorado sob prazo.

### 2. O que o modelo pode dizer (Guardrails)

Bedrock Guardrails aplica filtros consistentes em entrada e saída: tópicos negados, filtros de conteúdo, redação de PII, checagem de fundamentação contra fonte. É a camada que faz sentido quando o output vai pro cliente final, não pro seu terminal.

O ponto de arquitetura: guardrail não é substituto de prompt bem escrito, é rede de segurança pra quando o prompt falhar. Trate como circuit breaker, não como lógica de negócio.

### 3. Por onde o tráfego passa (VPC + PrivateLink)

Endpoint de VPC pro Bedrock, policy no endpoint restringindo modelos, e a chamada nunca toca a internet pública. Combinado com a camada 1, você tem o caminho de rede fechado.

### 4. O que ficou registrado (e a pegadinha do CloudTrail)

Esta é a que mais gera falso senso de segurança.

**CloudTrail registra a chamada como management event: quem chamou, quando, de onde, qual modelo. Metadata, não conteúdo.** Ele é ligado por padrão. E ele *não* mostra o que foi perguntado ao modelo nem o que o modelo respondeu.

Quem guarda prompt e completion é o **model invocation logging**, que grava em S3, CloudWatch Logs ou nos dois. E ele é **opt-in** — vem desligado.

O resultado prático: um monte de empresa está em produção achando que tem trilha de auditoria de IA porque "o CloudTrail está ligado". Não tem. Tem log de acesso. No dia em que alguém perguntar "que dado de cliente esse agente viu em março?", a resposta vai ser silêncio.

Ligar é uma chamada:

```bash
aws bedrock put-model-invocation-logging-configuration \
  --logging-config '{
    "cloudWatchConfig": {
      "logGroupName": "/aws/bedrock/invocations",
      "roleArn": "arn:aws:iam::<ACCOUNT_ID>:role/BedrockLoggingRole"
    },
    "s3Config": {
      "bucketName": "meu-bucket-bedrock-logs",
      "keyPrefix": "invocations/"
    },
    "textDataDeliveryEnabled": true
  }'
```

CloudWatch pra alarme e métrica em tempo real; S3 pra retenção longa e replicação. A Anthropic recomenda manter no mínimo 30 dias de log rotativo. E lembre: agora você tem prompts de usuário parados num bucket. Criptografia com KMS, policy de acesso restrita e lifecycle de expiração deixam de ser opcionais.

## Preço do Bedrock: a conta em real

Vamos fazer a conta de um caso concreto, não de um "hello world".

Cenário: agente interno de suporte. 10.000 requisições por mês. Cada uma manda 8.000 tokens de entrada (system prompt + 6 documentos recuperados via RAG) e devolve 600 tokens. Modelo classe Sonnet, a US$ 3 / US$ 15 por milhão.

**Sem otimização nenhuma:**

- Entrada: 10.000 × 8.000 = 80M tokens → 80 × US$ 3 = **US$ 240**
- Saída: 10.000 × 600 = 6M tokens → 6 × US$ 15 = **US$ 90**
- Total: **US$ 330/mês**

A US$ 5,22 por dólar (cotação de agosto de 2026), isso é **R$ 1.722** por mês. Antes de IOF, antes de spread de câmbio do cartão.

**Com prompt caching:** o system prompt e os documentos base somam ~7.000 dos 8.000 tokens de entrada, e são estáveis entre requisições. O Bedrock suporta prompt caching pro Claude com dois TTLs: 5 minutos (escrita a 1,25x, leitura a 0,1x) e 1 hora (escrita a 2,0x, leitura a 0,1x).

- Leitura de cache: 70M × US$ 3 × 0,1 = **US$ 21**
- Entrada variável: 10M × US$ 3 = **US$ 30**
- Escritas de cache (~300 no mês): 2,1M × US$ 3 × 1,25 ≈ **US$ 8**
- Saída: **US$ 90**
- Total: **≈ US$ 149/mês** → **R$ 778**

Corte de 55% mexendo em onde você coloca o cache breakpoint. Nenhuma linha de lógica de negócio mudou.

E lembre que token é só um item de linha. A fatura real de um agente em produção tem mais cinco baldes além da inferência, e eu abri o balancete completo em [quanto custa um agente em produção em 2026](https://blog.beerandcode.com.br/noticias/custo-agente-ia-producao-2026-planilha-tco).

Três avisos sobre essa conta:

**O cache tem ponto de equilíbrio.** A escrita custa mais caro que a entrada normal. Abaixo de ~30% de taxa de acerto, cada escrita custa mais do que as leituras economizam. Se seu prefixo muda a cada requisição, você está pagando 1,25x pra não usar nada. Meça `cache_read_input_tokens` na resposta — se vier zero em requisições consecutivas com o mesmo prefixo, tem invalidador silencioso no seu prompt (timestamp, UUID, JSON sem ordenação estável).

**Endpoint regional custa 10% a mais.** Se residência de dados te obriga ao regional, some 10% em cima de tudo. No exemplo, US$ 149 vira US$ 164.

**Batch corta 50% — mas não é o batch da Anthropic.** O Bedrock tem inferência em batch própria (`CreateModelInvocationJob`): você joga um JSONL no S3, ele processa assíncrono em até 24h e devolve no S3, a metade do preço on-demand. A Message Batches API da Anthropic **não** está disponível no Bedrock. São APIs diferentes, com integrações diferentes. Se o seu pipeline tolera latência de horas — classificação de tickets, enriquecimento de base, geração de resumo noturno — metade da fatura está na mesa.

## Limitações e pontos de atenção

O que você perde ao escolher o Bedrock em vez da API direta, segundo a [documentação oficial](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock):

- **Structured outputs** não é suportado. Se seu código depende de `output_config.format` pra garantir JSON válido, você vai voltar pra tool use com `strict: true` ou pra validação com retry.
- **Server-side tools** não rodam: web search, web fetch, code execution, advisor. Tudo que dependia da Anthropic executar a ferramenta vira responsabilidade sua.
- **Files API e URL sources** fora. Anexo vai como base64 no request.
- **MCP connector, Agent Skills e Managed Agents** fora. Agente no Bedrock é loop que você escreve e hospeda.
- **Server-side fallback** (o parâmetro `fallbacks`) não existe. Use o padrão client-side.

O que continua: Messages API completa, prompt caching, thinking, tool use (incluindo bash, computer use, memory, text editor) e citations.

Sobre quota: o padrão são **2 milhões de tokens de entrada por minuto**, e dá pra pedir até 4 milhões sem aprovação adicional da Anthropic. Limites de requisições por minuto são impostos pela AWS — esse teto se ajusta com o suporte da AWS, não com a Anthropic.

## FAQ

**Por que recebo 404 no ID do modelo?**
Provavelmente faltou o prefixo `anthropic.`. No Bedrock é `anthropic.claude-opus-5`, não `claude-opus-5`. Se o prefixo está certo, confira se o model access está habilitado para esse modelo na sua conta, no console do Bedrock.

**403 mesmo com a policy IAM correta. E agora?**
Se você usa inference profile geográfico, verifique as SCPs da organização. O profile roteia entre várias regiões e a SCP precisa liberar **todas** as regiões de destino, não só a de origem. Bloquear qualquer região de destino quebra o cross-region inference inteiro.

**O CloudTrail me dá trilha de auditoria de IA?**
Não. CloudTrail registra metadata da chamada. Para guardar prompt e resposta você precisa habilitar model invocation logging, que vem desligado por padrão.

**Consigo manter os dados no Brasil?**
Hoje, não pelo Bedrock. A região `sa-east-1` só oferece endpoint Global para o Claude, e não existe perfil geográfico para América do Sul. Se residência no Brasil é requisito contratual, essa arquitetura não fecha.

**Vale migrar da API direta para o Bedrock?**
Só se você precisa do perímetro AWS ou de billing consolidado. O preço por token é o mesmo, e você perde um conjunto relevante de features. Migre por razão de governança, nunca por custo. Se a sua dúvida é custo mesmo, a comparação que interessa é outra: [LLM local vs API, com planilha de 90 dias](https://blog.beerandcode.com.br/noticias/llm-local-vs-api-2026-planilha-90-dias).

## Fechando

O Bedrock não deixa o Claude mais barato nem mais inteligente. Ele muda quem responde pelas perguntas difíceis: onde o dado passou, quem autorizou, o que ficou registrado e quanto custou.

Se o seu contexto tem essas perguntas, o trabalho não é ligar o serviço — é fechar as quatro camadas. IAM que limita e força o guardrail. Guardrail como circuit breaker. Rede privada. E model invocation logging **ligado**, porque a camada que todo mundo esquece é justamente a que o auditor vai pedir primeiro.

O próximo passo natural é evals: você agora tem os logs de invocação em S3. Isso é um dataset de casos reais esperando pra virar suíte de avaliação. Modelo em produção sem eval é fé, não engenharia.
