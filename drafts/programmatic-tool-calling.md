Function calling clássico parece sólido até você botar um agente com 30 tools em produção.

Daí o tool definitions sozinho consome [134 mil tokens antes da conversa começar](https://www.anthropic.com/engineering/advanced-tool-use). Cada chamada vira um round-trip novo no modelo. Cada resultado bruto de tool entra no contexto. E quando o agente precisa cruzar 20 lookups, você paga 20 vezes a inferência.

Em 24 de novembro de 2025 a Anthropic anunciou o [programmatic tool calling](https://www.anthropic.com/engineering/advanced-tool-use). A ideia é simples e provocadora: em vez de Claude pedir uma tool por vez, ele escreve **código Python** que chama suas tools, roda esse código em sandbox, processa o resultado ali e só devolve a conclusão pro contexto.

Neste post a gente compara lado a lado, lê o código que o modelo gera e fecha com um agente real orquestrando as próprias tools.

## TL;DR

- **O que é:** Claude escreve Python que invoca suas tools dentro de um container de code execution. Resultados intermediários não entram no contexto do modelo.
- **Stack/Modelos:** Claude API, `code_execution_20260120`, Opus 4.5+ ou Sonnet 4.5+.
- **Custo/Acesso:** GA na Claude API, mesma cobrança do code execution. Sem beta header na first-party API.
- **Repositório/Link útil:** [Docs oficiais](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) e [cookbook PTC](https://platform.claude.com/cookbook/tool-use-programmatic-tool-calling-ptc).

## Por que function calling clássico está virando legado

O loop tradicional você já conhece de cor.

Você manda system prompt + definições de tool + mensagem do user. O modelo decide chamar `query_database`. Você executa. Devolve o resultado pro modelo. Ele decide chamar de novo. Devolve. Repete até `stop_reason: end_turn`.

Funciona perfeitamente para um agente com 3 tools e 2 chamadas. Quebra em três frentes assim que a coisa cresce:

**Tokens.** Cada round-trip carrega o histórico inteiro: system prompt, todas as definições de tool, todos os resultados anteriores. A própria Anthropic documenta o caso de um agente com cinco MCPs gastando [~55 mil tokens antes de qualquer mensagem](https://www.anthropic.com/engineering/advanced-tool-use). E setups internos chegando a 134K só de definição de ferramentas.

**Latência.** Cada chamada é uma inferência nova. Para um agente que cruza 20 endpoints, são 20 amostragens do modelo, sequenciais, cada uma na casa das centenas de milissegundos. Multiplica.

**Composabilidade.** Você não compõe nada. Filtrar resultado, paralelizar lookups, fazer early termination, decidir condicionalmente qual tool chamar a seguir, tudo isso o modelo simula uma chamada por vez, com round-trip no meio. É código orquestrado por amostragem, e amostragem é cara.

O ponto não é que function calling clássico esteja errado. É que ele força o modelo a operar como se cada decisão fosse uma frase isolada, quando o que você quer mesmo é que ele opere como um programador escrevendo um script.

## O que muda quando o agente escreve o próprio código

Programmatic tool calling inverte o fluxo.

Claude continua tendo as tools declaradas no payload. Mas você marca cada tool com `allowed_callers: ["code_execution_20260120"]`. Isso diz ao modelo: essa função existe dentro do sandbox de code execution, você pode chamá-la como Python normal.

Aí, em vez de retornar um `tool_use` por turno, o modelo gera um bloco de código que chama várias tools, processa os resultados, faz `if`, faz `for`, faz `asyncio.gather`. Cada vez que esse código chama uma tool, o container pausa, a API devolve um `tool_use` com `caller.type = "code_execution_20260120"`, você executa a tool no seu lado e responde com o `tool_result`. O container retoma a execução.

O resultado intermediário **não entra no contexto do modelo**. Só o `stdout` final do script chega de volta na próxima inferência. É isso que destrava os ganhos.

A própria documentação resume bem:

> Programmatic tool calling allows Claude to write code that calls your tools programmatically within a code execution container, rather than requiring round trips through the model for each tool invocation.
> — [docs Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)

E em benchmarks de pesquisa multistep como [BrowseComp](https://arxiv.org/abs/2504.12516) e [DeepSearchQA](https://github.com/google-deepmind/deepsearchqa), a Anthropic afirma que adicionar PTC em cima das tools básicas de busca foi o "fator-chave que destravou de vez a performance do agente".

## Comparação lado a lado

| Dimensão | Function calling clássico | Programmatic tool calling |
|---|---|---|
| Quem orquestra | O modelo, uma chamada por turno | Código Python no sandbox |
| Tokens (research multistep) | ~43.588 | ~27.297 ([-37%](https://www.anthropic.com/engineering/advanced-tool-use)) |
| Round-trips para 20 lookups | 20 inferências | 1 inferência + N tool results |
| Resultados brutos no contexto | Sim, todos | Não, só o output final |
| Composição (filtrar, paralelizar) | Simulada turno a turno | Nativa em Python (`asyncio.gather`, `for`, `if`) |
| Estado entre chamadas | Histórico de mensagens | REPL persistente no container |
| Debug | Inspecionar JSON de cada turno | Inspecionar o código gerado e o stdout |
| Onde não cabe | Pipelines de dados grandes | Single tool call rápido |

A linha de tokens vem do anúncio oficial: tarefas complexas de pesquisa caíram de **43.588 para 27.297 tokens em média, queda de 37%**. Combinada com o [tool search tool](https://www.anthropic.com/engineering/advanced-tool-use) (de 77K para 8.7K tokens em definições, queda de 85%), dá pra atacar os dois lados do gargalo.

## Mão na massa: um agente que escreve seu próprio Python

Vou mostrar o caso clássico do anúncio: descobrir quais engenheiros estouraram orçamento de viagem em Q3.

Você tem duas tools: uma para listar membros do time, outra para puxar despesas por funcionário e trimestre. No fluxo tradicional, isso vira N+1 round-trips. Aqui vai virar um único script.

### Passo 1: declarar as tools com `allowed_callers`

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "type": "code_execution_20260120",
        "name": "code_execution",
    },
    {
        "name": "get_team_members",
        "description": "Retorna lista de membros do time. Output: JSON array com {id, name, department}.",
        "input_schema": {
            "type": "object",
            "properties": {
                "department": {"type": "string"}
            },
            "required": ["department"],
        },
        "allowed_callers": ["code_execution_20260120"],
    },
    {
        "name": "get_expenses",
        "description": "Retorna despesas de um funcionário em um trimestre. Output: JSON array com {amount, category, status}.",
        "input_schema": {
            "type": "object",
            "properties": {
                "employee_id": {"type": "string"},
                "quarter": {"type": "string"},
            },
            "required": ["employee_id", "quarter"],
        },
        "allowed_callers": ["code_execution_20260120"],
    },
]
```

Note o detalhe que a doc bate na tecla: descreva bem o **formato de saída** de cada tool. Como Claude vai desserializar o resultado em código, ele precisa saber se é JSON, se é string, qual o schema. Quanto mais explícito, menos parse defensivo no script gerado.

### Passo 2: rodar o agente

```python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": "Quais engenheiros estouraram orçamento de viagem em Q3?",
    }],
    tools=tools,
)
```

A primeira resposta vem com `stop_reason: tool_use` e dois blocos: um `server_tool_use` com o código que Claude gerou, e um `tool_use` com a primeira chamada de função. Note o campo novo:

```json
{
  "type": "tool_use",
  "name": "get_team_members",
  "input": {"department": "engineering"},
  "caller": {
    "type": "code_execution_20260120",
    "tool_id": "srvtoolu_abc123"
  }
}
```

O `caller.type` te diz que aquela invocação veio do código, não do modelo direto. Você executa sua tool normal no servidor e responde com o `tool_result`. O container retoma o script.

### Passo 3: o código que Claude gera

Esse é o pulo do gato. Veja o que o modelo escreve sem você pedir:

```python
import asyncio
import json

async def main():
    members_raw = await get_team_members(department="engineering")
    members = json.loads(members_raw)

    expense_calls = [
        get_expenses(employee_id=m["id"], quarter="Q3")
        for m in members
    ]
    expenses_per_member = await asyncio.gather(*expense_calls)

    over_budget = []
    for member, raw in zip(members, expenses_per_member):
        expenses = json.loads(raw)
        travel_total = sum(
            e["amount"] for e in expenses
            if e["category"] == "travel" and e["status"] == "approved"
        )
        if travel_total > 5000:
            over_budget.append({"name": member["name"], "total": travel_total})

    print(json.dumps(over_budget, indent=2))

await main()
```

Repare nos quatro padrões que aparecem de graça:

1. **Paralelização** com `asyncio.gather`. Vinte funcionários viram vinte chamadas concorrentes, não vinte round-trips.
2. **Filtragem em código.** A lista bruta de despesas nunca volta pro modelo. Só os funcionários que estouraram.
3. **Agregação local.** A soma do `travel_total` é Python puro, custa zero token.
4. **Output controlado.** O `print` no final é o único dado que retorna pro contexto do modelo na próxima inferência.

### Passo 4: o output final

Quando o script termina, a API devolve um `code_execution_tool_result` com o `stdout`. Claude vê só:

```json
[
  {"name": "Ana Souza", "total": 6800},
  {"name": "Renato Lima", "total": 5400}
]
```

E gera a resposta em texto pra você. Ele nunca leu as 47 linhas de despesa por funcionário. Você economizou contexto, latência, dinheiro.

## Limitações e pontos de atenção

PTC não é varinha mágica. Lugares onde você vai se queimar:

**Container expira.** São 4,5 minutos de idle e 30 dias de teto duro. Se sua tool externa demora pra responder, o container morre e o script recebe `TimeoutError`. Trate timeout no seu lado e monitore o `expires_at` na resposta.

**MCP connector ainda não vai.** Tools expostas via [MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector) não são chamáveis programaticamente hoje. A doc indica que pode mudar; por enquanto, se você roda agente em cima de servidores MCP remotos, esses tools ficam no caminho clássico.

**Tool result é string.** Se sua tool devolve dado externo bruto, validar e sanitizar virou prioridade. O `tool_result` vai parar dentro de um runtime Python. Code injection deixa de ser hipótese e vira vetor.

**Algumas flags não combinam.** `strict: true`, `tool_choice` forçando uma tool específica e `disable_parallel_tool_use` não funcionam com PTC. Se sua arquitetura depende delas, repensa antes de migrar.

**Não force o pattern em call simples.** Para uma tool só, com uma chamada e uma resposta, o overhead do container come o ganho. Use PTC quando há composição: 3+ chamadas dependentes, agregação, filtragem, batch. Pra `get_user_by_id`, mantém o clássico.

## FAQ

**Funciona em qual modelo?**
Hoje, Claude Opus 4.7, Opus 4.6, Sonnet 4.6, Opus 4.5 e Sonnet 4.5. A versão da tool é `code_execution_20260120`. Modelos anteriores não suportam.

**Precisa de beta header?**
Não na first-party Claude API: é GA. Em Bedrock e Vertex AI ainda há header beta requerido. A [doc de erro](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) lista `missing_beta_header` como erro comum nessas plataformas.

**Como cobra?**
Mesmo pricing do code execution. E o detalhe importante: tool results de chamadas programáticas **não contam** no input/output token usage do modelo. Só a saída final do script é cobrada como contexto. É exatamente daí que sai a economia.

**E se eu já uso LangChain ou similar?**
Provedores como [LiteLLM já expõem PTC](https://docs.litellm.ai/docs/providers/anthropic_programmatic_tool_calling). Mas a essência do padrão é genérica: um agente que escreve código que chama tools. Você pode implementar manualmente com sandbox próprio se não quiser depender do container gerenciado da Anthropic.

## O agente que escreve scripts é o mesmo que escreve produto

A tese aqui é incômoda de propósito. Function calling clássico não some amanhã. Mas ele vira o caso especial, não o padrão. O padrão passa a ser: dou ao modelo um conjunto de funções e deixo ele compor.

Isso muda como você desenha agente. Em vez de catedral de prompt orquestrando turnos, você escreve tools bem documentadas, com schema de output explícito, e confia na capacidade do modelo de programar contra elas. É menos engenharia de prompt e mais engenharia de **harness** — o ambiente em volta do modelo, com sandbox, tools e feedback loop.

Se essa parte de harness aplicado em produto real é o que te interessa, é exatamente o foco do workshop [Harness Engineering com Claude Code](https://beerandcode.com.br/landing-pages/harness-engineering-com-claude-code) que rola dia 16 e 17 de maio: dois dias construindo do zero um app que recebe link de produto, pesquisa alternativas em e-commerces, compara preço e devolve recomendação estruturada, em Claude Code com Laravel e NativePHP. Sem chatbot, sem demo de slide. Produto.

E se você quer ver PTC aplicado em outros padrões de agente, vale revisitar o post sobre [anatomia de um agent harness](https://blog.beerandcode.com.br/anatomia-agent-harness): a peça do code execution se encaixa exatamente na camada de execução de tools.
