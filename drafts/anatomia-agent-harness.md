## Introdução

Você cola a chave da OpenAI no script, encaixa um while-loop em volta de uma chamada de tool, abre uma garrafa e chama de "agente em produção". Aí na sessão três o bicho perde contexto, executa um shell que ninguém autorizou, entra em loop infinito por uma alucinação e queima o orçamento da API por uma noite inteira. O que faltou ali não foi prompt melhor. Foi harness.

Harness é a camada de software que envolve o modelo. É o que transforma um LLM, que sozinho só sabe responder texto, em um agente que aguenta produção. A Anthropic é explícita sobre isso na documentação oficial: "Claude Code serves as the agentic harness around Claude: it provides the tools, context management, and execution environment that turn a language model into a capable coding agent" ([How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)).

Esse post é o mapa mental. Vou quebrar o harness em cinco componentes obrigatórios. Estado persistente, roteador de ferramentas, validação de I/O, loop de raciocínio e limites de segurança. Cada um vai virar post próprio depois. Esse aqui é o esqueleto que você vai revisitar em todos.

## TL;DR

- **O que é:** harness é a infraestrutura de software que envolve um LLM e o transforma em um agente confiável.
- **Stack/Modelos:** independente de modelo (Claude, GPT, Gemini, Llama). Padrão referenciado: [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) e Claude Code.
- **Custo/Acesso:** SDK aberto, gratuito. O harness próprio é decisão de engenharia.
- **Repositório útil:** [claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos).

## O contexto: por que harness virou a palavra do ano em IA aplicada

Em 2024 a discussão era prompt. Em 2025 era contexto. Em 2026, harness.

A mudança não é cosmética. A Anthropic publicou em março/2026 dois posts no [engineering blog](https://www.anthropic.com/engineering) só sobre design de harness. O argumento central: "task execution reliability increasingly depends not on the underlying model's capabilities, but on the infrastructure layer that wraps around it".

Traduzindo: o gargalo do agente em produção não é mais o modelo. É o software ao redor do modelo.

Faz sentido. Opus 4.7 é absurdamente capaz. Mas se você não tem como ele lembrar do que fez, validar o que ele fez, parar quando deveria parar e proteger o sistema do que ele decidiu fazer, o modelo bom não te salva. A diferença entre um demo bonito no Twitter e um agente que roda em cliente real está toda dentro do harness.

A tese desse post é simples. Harness não é um detalhe de implementação. Harness é o produto.

## Pré-requisitos para acompanhar a série

Esse post é a porta de entrada. Você não precisa codar nada agora. Mas para a série inteira faz sentido ter:

- [ ] Conhecimento básico de chamadas a APIs LLM (qualquer provedor).
- [ ] Familiaridade com o conceito de tool use / function calling.
- [ ] Stack escolhida: Python (LangGraph, Claude Agent SDK), TypeScript (Agent SDK), ou PHP (prism-php).
- [ ] Vontade de ir além do "cole o prompt e reza".

Se algum desses pontos é novo, segue normal. A gente vai descer no detalhe técnico de cada peça nos próximos posts.

## Os 5 componentes obrigatórios

Esses cinco são o esqueleto. Tira qualquer um e o agente quebra. Pode ser que você não chame pelo mesmo nome que eu, mas a função tem que estar lá.

### 1. Estado persistente

Estado é o que sobrevive ao final de um turno do modelo.

Parece simples. Não é.

Cada chamada à API começa do zero. O modelo não lembra de nada que não esteja no payload daquela request. Tudo que você quer que persista, você precisa armazenar e re-injetar. Existem três escalas que importam:

- **Working memory:** o que está dentro da janela de contexto agora. Histórico de mensagens, system prompt, output das tools.
- **Session memory:** o que sobrevive entre turns dentro da mesma sessão. O Claude Agent SDK persiste isso em arquivos JSONL no disco.
- **Long-term memory:** o que sobrevive entre sessões. Banco vetorial, arquivo de progresso, banco relacional, índice no disco.

A ingenuidade clássica é "salvar tudo no histórico de mensagens". Funciona até o terceiro turno. Depois explode em context overflow.

A Anthropic resolve isso de duas formas. Dentro da sessão, com auto-compaction: "Claude Code manages context automatically as you approach the limit. It clears older tool outputs first, then summarizes the conversation if needed" ([docs](https://code.claude.com/docs/en/how-claude-code-works#when-context-fills-up)). Entre sessões, com artefatos estruturados. No post [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) eles descrevem o uso de um arquivo `claude-progress.txt` somado ao histórico do git para que um novo agente, começando com contexto vazio, consiga reconstruir o que foi feito antes.

Esse é o ponto que ninguém vê em demo. Mas é o que separa um agente que faz uma tarefa de um agente que continua uma tarefa amanhã.

### 2. Roteador de ferramentas

Roteador de ferramentas é a parte do harness que registra schemas, valida argumentos, executa o efeito colateral e devolve uma observation legível para o modelo.

A definição de uma tool é minimalista: nome, descrição, schema dos parâmetros. É essa tripla que o modelo vê no contexto e usa para decidir quando chamar. A documentação do Claude Code agrupa as tools nativas em cinco categorias: file operations, search, execution, web e code intelligence. Esse conjunto cobre a maior parte dos casos de uso de agente de código.

O detalhe que muita gente perde está no diff entre o Client SDK e o Agent SDK da Anthropic:

```python
# Client SDK: você implementa o tool loop
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    result = your_tool_executor(response.tool_use)
    response = client.messages.create(tool_result=result, **params)

# Agent SDK: o harness gerencia
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

No Client SDK você escreve o while-loop. No Agent SDK o harness escreve por você. Não é syntactic sugar. É a diferença entre reimplementar tool execution toda vez ou ter um roteador testado em produção.

A frase da Anthropic resume: "Tools are what make Claude Code agentic. Without tools, Claude can only respond with text". Sem roteador, o modelo é um chatbot caro.

### 3. Validação de I/O

O modelo não devolve sempre o que você espera. Tool calls nativos ajudam muito porque o schema vai pré-validado pelo provedor. Mas argumento inválido ainda chega. Tool result vem em formato que não é o esperado. Resposta final tem alucinação que precisa ser filtrada.

Validação de I/O é a peça que captura tudo isso antes de afetar o resto do sistema.

A taxonomia de erros mais útil que vi vem do post [Anatomia de um Agent Harness](https://blog.dailydoseofds.com/p/the-anatomy-of-an-agent-harness) do Avi Chawla. Quatro categorias:

- **Transient:** rede caiu, rate limit, timeout. Retry com backoff.
- **LLM-recoverable:** argumento inválido, tool não encontrada. Devolve o erro como `ToolMessage` para o modelo se corrigir.
- **User-fixable:** falta credencial, falta permissão, ambiguidade de intenção. Interrompe e pergunta.
- **Unexpected:** algo realmente quebrou. Loga, alerta, encerra.

A regra prática da Anthropic é "catches failures within tool handlers and returns them as error results to keep the loop running". Em outras palavras, erro de uma tool não é exceção fatal. É observation. O modelo lê, entende e tenta de outro jeito.

E tem mais um lado: verificação ativa. Avi Chawla cita que loops de verificação "improve quality by 2 to 3x through rules-based feedback, visual feedback, or LLM-as-judge". É exatamente o que a Anthropic fez no [harness design para long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps): separou um agente "evaluator" do "generator", porque agentes que avaliam o próprio trabalho enviesam positivo, "agents tend to respond by confidently praising the work, even when the quality is obviously mediocre".

Validação não é só rejeitar entrada errada. É arquitetar feedback de qualidade.

### 4. Loop de raciocínio

Aqui mora o orchestration loop. A peça que decide se o agente continua ou para.

A Anthropic descreve o loop em três fases que se misturam: "When you give Claude a task, it works through three phases: gather context, take action, and verify results. These phases blend together" ([docs](https://code.claude.com/docs/en/how-claude-code-works#the-agentic-loop)). É o ciclo TAO clássico — thought, action, observation — em outra roupa.

Mecanicamente, é um while-loop. A complexidade não vive no loop. Vive no que o loop gerencia: quando ele para?

As condições de parada de um loop bem feito:

- O modelo respondeu sem tool calls (resposta final).
- Atingiu o limite máximo de turns.
- Estourou o orçamento de tokens.
- Um guardrail disparou um tripwire.
- O usuário interrompeu.
- O modelo retornou refusal de segurança.

Sem essas guards, o loop vira loop infinito. Com elas, vira agente.

E para tarefas que duram horas ou dias, single-loop não basta. A Anthropic decompõe em múltiplos agentes especializados, cada um com seu próprio loop e contexto fresco: planner expande o pedido em spec, generator implementa, evaluator testa via Playwright MCP. O princípio que eles enfatizam é "find the simplest solution possible, and only increase complexity when needed". Você não começa com três agentes. Você chega neles quando o single-loop não dá conta.

### 5. Limites de segurança

Sem essa quinta peça, tudo que veio antes é uma bomba.

Guardrails operam em três níveis:

- **Input:** sanitiza prompt antes de mandar pro modelo (prompt injection, dados sensíveis).
- **Output:** filtra a resposta antes de devolver pro usuário ou pro próximo turno.
- **Tool:** valida cada chamada de tool antes de executar. É o ponto crítico, porque tool é onde o agente toca o mundo real.

O Claude Agent SDK expõe esse controle via dois mecanismos. **Permission modes** definem o nível de autonomia: `default` (pergunta antes de cada edit), `acceptEdits` (auto-aprova edits, ainda pergunta para shell), `plan` (read-only), `auto` (avalia tudo com checagem de segurança em background, ainda em research preview). E **hooks**, callbacks que rodam em pontos do ciclo de vida: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`.

Exemplo de hook que audita toda edição de arquivo:

```python
from datetime import datetime
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
    with open("./audit.log", "a") as f:
        f.write(f"{datetime.now()}: modified {file_path}\n")
    return {}

async for message in query(
    prompt="Refactor utils.py",
    options=ClaudeAgentOptions(
        permission_mode="acceptEdits",
        hooks={"PostToolUse": [HookMatcher(matcher="Edit|Write", hooks=[log_file_change])]},
    ),
):
    print(message)
```

Em paralelo, checkpoints. Antes de cada edit, o Claude Code tira snapshot do arquivo. Esc duas vezes reverte. Mas atenção: checkpoint é local, não cobre side effect externo. "Actions that affect remote systems (databases, APIs, deployments) can't be checkpointed". É por isso que harness sério bloqueia destrutivo, audita tool calls e exige aprovação para ação sensível.

Se seu agente pode rodar `rm -rf` ou apagar uma tabela do Postgres sem revisão, você não tem agente. Tem incidente esperando pra acontecer.

## Como esses 5 conversam

O fluxo, em uma frase: prompt entra, loop puxa o estado persistente, monta contexto, modelo decide tool, roteador valida e executa, observation volta, validação de I/O processa, guardrail audita, estado atualiza, loop decide se segue ou para.

Cinco peças. Um único laço. Cada turno passa por todas.

Se desenhar isso num quadro branco, é uma versão expandida da figura que a Anthropic publica como agentic loop. A diferença é que cada uma das cinco etapas é um sistema com responsabilidade própria, testes próprios e modos de falha próprios.

## Erros que aparecem quando algum componente falta

Mapa rápido pra te ajudar a debugar quando o agente está se comportando mal:

- **Sem estado persistente:** agente "esquece" tudo no segundo turn. Você tem chatbot, não agente.
- **Sem roteador de ferramentas:** você reescreve tool execution em cada projeto. Bugs sutis se multiplicam.
- **Sem validação de I/O:** um erro de tool quebra a sessão inteira. Alucinação passa direto pro usuário.
- **Sem loop de raciocínio robusto:** o agente para no primeiro tool call ou roda infinito até o budget acabar.
- **Sem limites de segurança:** um dia desses tem `rm -rf` na pasta errada, segredo vazado em log público, billing alert de madrugada.

Cada um desses erros tem um sintoma diferente. Mas o tratamento é sempre o mesmo: encaixar a peça que faltava.

## Limitações e pontos de atenção

Essa anatomia de cinco peças é mapa, não receita pronta. Algumas armadilhas:

- **Não é universal.** LangGraph organiza diferente (state graph), OpenAI Agents SDK organiza diferente (handoffs), CrewAI organiza diferente (crews + tasks). Os nomes mudam. As funções precisam estar.
- **Não é estático.** Conforme o modelo melhora, partes do harness simplificam. A Anthropic explicitamente recomenda subtrair: "find the simplest solution possible, and only increase complexity when needed". Sprint-based decomposition que era essencial em Sonnet 4.5 ficou desnecessária em Opus 4.6.
- **Não é grátis.** Cada peça tem custo de manutenção. Se seu caso de uso é "responder pergunta simples sobre PDF", você não precisa de harness. Precisa de RAG.
- **Não substitui produto.** Harness perfeito com produto mal pensado é caro e inútil. A pergunta primeiro é "que problema isso resolve no mundo real". Depois, "que harness aguenta isso".

Se você está pensando em construir, comece pelo SDK pronto (Agent SDK, LangGraph, OpenAI Agents). Customize quando bater no limite. Reescrever do zero é projeto de doutorado, não de produto.

## Entra no Clã

A próxima fase do mercado de IA não é prompt engineering. É harness engineering. Quem domina os cinco componentes acima sai na frente de quem ainda está colando key no script e chamando de agente.

No Clã Beer & Code a gente está construindo isso na prática: agentes Laravel com PHP, RAG em produção, ferramentas internas que aguentam volume real de cliente. Se quer estar nessa direção, entra no [Clã](https://beerandcode.com.br) e recebe os próximos posts dessa série antes de todo mundo, com código, exemplos e revisão de arquitetura.

## FAQ

**Preciso construir um harness do zero?**

Não. Agent SDK (Anthropic), LangGraph, OpenAI Agents e CrewAI já entregam o esqueleto. O que você precisa é entender o que cada um faz e onde customizar para o seu caso. Reinventar a roda só tem sentido quando o limite do framework atrapalha o produto.

**Funciona pra Laravel/PHP?**

Funciona. Mesma anatomia. Use [prism-php](https://prismphp.com) ou um cliente HTTP direto, monte sua orquestração, persista estado em banco/cache. Os conceitos são portáveis. PHP não tem um "Agent SDK" oficial dos labs, mas o ecossistema está crescendo rápido.

**Quando passa do while-loop simples pra harness completo?**

Quando bate uma dessas três: o agente vai rodar em produção atendendo mais de um usuário, vai trabalhar por mais de cinco minutos sem supervisão, ou tem ação destrutiva no escopo. Qualquer uma das três e você precisa dos cinco componentes. Não dá pra atalhar.

**Qual a diferença entre harness e framework?**

Framework é o conjunto de ferramentas que te ajuda a construir o harness. Harness é a instância concreta que envolve o seu agente. LangGraph é framework. O harness do seu agente de suporte construído em LangGraph é harness.

## Conclusão

Cinco peças. Estado persistente, roteador de ferramentas, validação de I/O, loop de raciocínio e limites de segurança. Tira qualquer uma e o agente não aguenta produção.

Esse é o mapa. Os próximos posts dessa série vão descer em cada peça, começando pela mais traiçoeira: estado persistente. Tem três escalas de memória, padrões de compaction e o problema de sessões que começam do zero. É lá que a maior parte dos agentes morre antes de chegar ao cliente.

Engenharia de IA não começa no prompt. Começa no harness.
