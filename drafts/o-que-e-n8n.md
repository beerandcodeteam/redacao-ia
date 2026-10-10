# O que é n8n: guia pra dev — e quando desenvolver do zero

Você já viu o n8n em todo lugar. No vídeo de automação, no post do LinkedIn, na vaga que pede "experiência com n8n" como se fosse stack. E a pergunta que fica não é "o que é" — é se você, dev, deveria se importar.

O n8n é uma ferramenta de automação de workflows: você conecta gatilhos, dados e ações num editor visual e a máquina executa sozinha. Simples assim. O problema é que quase todo conteúdo sobre ele foi escrito pra quem não programa — e trata a caixinha como destino final, não como ferramenta com limite.

Este guia é o contrário. Vou te mostrar o que o n8n é de verdade, como ele funciona por baixo, onde ele brilha pra quem escreve código — e os sinais objetivos de que chegou a hora de largar o editor visual e desenvolver do zero. No fim, uma régua de decisão pra você nunca mais escolher no chute.

## TL;DR

- **O que é:** ferramenta de automação de workflows fair-code — editor visual onde triggers, nodes e ações formam fluxos que rodam sozinhos, com nodes nativos de IA e agentes.
- **Stack:** Node.js/TypeScript por baixo; 400+ integrações; nodes de IA construídos sobre LangChain.
- **Custo/Acesso:** self-host gratuito pra uso interno (Sustainable Use License); cloud pago; embutir no seu produto comercial exige licença.
- **Link útil:** [docs.n8n.io](https://docs.n8n.io/)

## O que é o n8n (e por que todo mundo fala dele)

O n8n se define como uma ferramenta de automação de workflows com licença fair-code que combina IA com automação de processos ([docs oficiais](https://docs.n8n.io/)). Traduzindo: é um canvas onde você desenha fluxos — "quando chegar mensagem no WhatsApp, consulta a planilha, chama o modelo, responde" — e o motor executa cada passo, com retry, log e histórico de execução.

E o hype tem lastro. Em outubro de 2025 a empresa levantou uma Series C de US$ 180 milhões liderada pela Accel, com a NVentures (braço de venture da NVIDIA) no meio, avaliada em US$ 2,5 bilhões — citando crescimento de 6x em usuários e 10x em receita no ano ([anúncio oficial](https://blog.n8n.io/series-c/)). No Brasil, o Google Trends conta a mesma história: o n8n abriu uma distância enorme dos concorrentes visuais e virou sinônimo da categoria.

A licença merece um parágrafo, porque "fair-code" confunde. O código é aberto e você pode rodar o n8n no seu servidor de graça, sem limite de workflows, pra uso interno. O que a [Sustainable Use License](https://docs.n8n.io/sustainable-use-license/) proíbe é revender o n8n como serviço ou embuti-lo no seu produto comercial sem pagar. Pra maioria dos cenários de agência e produto interno, o self-host gratuito resolve.

## Como funciona na prática: trigger, nodes e ações

Todo workflow do n8n tem a mesma anatomia de três peças ([docs](https://docs.n8n.io/workflows/components/nodes/)):

1. **Trigger** — o evento que acorda o fluxo: um webhook, um cron, uma mensagem nova, uma linha criada na planilha.
2. **Nodes** — os blocos que processam: buscam dado, transformam, filtram, decidem caminho.
3. **Ações** — o efeito no mundo: manda o e-mail, grava no banco, responde a API.

Os dados atravessam o fluxo como uma lista de itens JSON, e cada node opera sobre essa lista. É aqui que o n8n para de ser brinquedo de no-code pra quem é dev: quando a caixinha pronta não resolve, você abre um **Code node** e escreve JavaScript de verdade sobre os itens:

```javascript
// Code node: enriquece cada pedido com o total em reais
return items.map((item) => {
  const { valor_centavos, qtd } = item.json;
  return {
    json: {
      ...item.json,
      total_brl: (valor_centavos * qtd) / 100,
      processado_em: new Date().toISOString(),
    },
  };
});
```

Na prática, o fluxo de trabalho do dev no n8n é: caixinha pronta pra integração chata (OAuth do Google, paginação de API, retry), código só onde existe lógica sua. Essa divisão é o superpoder da ferramenta — e, como a gente vai ver adiante, também é onde mora a armadilha.

## n8n + agentes de IA na prática

O motivo do n8n ter explodido de vez foi a camada de IA. O [AI Agent node](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent) implementa um agente completo em cima do LangChain: você pluga um chat model (Claude, GPT, Gemini), conecta tools e uma memória como sub-nodes, e o agente decide sozinho qual ferramenta chamar pra cumprir a tarefa.

O detalhe poderoso: **qualquer workflow do n8n pode virar tool do agente**. Aquelas 400+ integrações deixam de ser passos fixos de um fluxo e viram ferramentas que o modelo chama sob demanda — consultar o CRM, gravar na planilha, disparar o e-mail. É tool use visual, sem você escrever o loop.

A gente já provou esse caminho na prática aqui no blog: construímos um [agente de bolão da Copa no WhatsApp com Evolution API e n8n](https://blog.beerandcode.com.br/tutoriais/agente-bolao-copa-whatsapp-evolution-api-n8n) — com guardrails, engenharia de prompt e o flow real na mesa. Pra colocar um agente conversando com um grupo de WhatsApp em dias, não semanas, o n8n é imbatível.

Mas repara no que o node esconde: o loop de raciocínio, a serialização das tools, o corte de contexto, o tratamento de erro do modelo. Enquanto o agente funciona, isso é conveniência. Quando ele quebra — e agente em produção quebra —, você vai debugar uma abstração que não escreveu, num canvas que não tem stack trace.

## Quando desenvolver do zero: os sinais de que a caixinha virou dívida técnica

Aqui está a parte que a primeira página do Google não te conta. O n8n não falha por ser ruim — ele falha quando é usado além da fronteira pra qual foi desenhado. Os sinais são objetivos:

- **Seu workflow vive no banco, não no Git.** Os fluxos ficam armazenados no banco de dados do n8n. O [source control com Git e ambientes dev/prod existe, mas é feature Enterprise](https://docs.n8n.io/source-control-environments/) — e mesmo ele não suporta review estilo pull request dentro da ferramenta. Sem plano pago: sem histórico, sem rollback, sem code review. Pra automação interna, tolerável. Pra lógica de negócio central, inaceitável.
- **Você não consegue escrever um teste.** Como você roda um teste automatizado num grafo de 40 caixinhas? Não roda. Você clica em "execute" e olha. Quando a lógica importa, "testei clicando" é o mesmo que não testar — o argumento inteiro está em [como montar evals honestos](https://blog.beerandcode.com.br/tutoriais/avaliacao-de-agentes-de-ia-evals-honestos).
- **O grafo virou espaguete.** 10 nodes se leem num relance. 40 nodes com três ramificações e dois sub-workflows são um sistema distribuído sem tipos, sem contrato e sem IDE. A tela que era clareza virou névoa.
- **Você precisa de comportamento que o node não expõe.** Streaming de resposta, controle fino de contexto, fallback entre modelos, observabilidade por token. Cada gambiarra pra contornar o node é um empréstimo — e essa dívida cobra juros a cada mudança.

Quando dois ou mais desses sinais aparecem juntos, a resposta não é otimizar o workflow. É reescrever aquilo como software: um repositório, um loop de agente que você entende linha a linha, testes que rodam no CI. Se você nunca fez isso, o caminho está mapeado em [como criar um agente de IA do zero — com código, não no-code](https://blog.beerandcode.com.br/tutoriais/como-criar-um-agente-de-ia-do-zero).

## A régua de decisão: n8n ou código do zero

Sem mistério e sem torcida. A escolha se resolve com quatro perguntas:

| Pergunta | Resposta "n8n" | Resposta "código" |
|---|---|---|
| Isso é protótipo ou produto? | Validar ideia em dias | Produto com SLA e usuário pagante |
| A lógica é sua ou é cola? | Integração entre sistemas prontos | Regra de negócio que diferencia seu produto |
| Quem mantém? | Você ou um time pequeno de ops | Time de engenharia com CI/CD |
| O que acontece se falhar às 3h? | Reprocessa de manhã | Alguém é acordado — precisa de teste, log e rollback |

A régua resumida: **protótipo, integração e automação interna → n8n. Produto com SLA, lógica de negócio central e necessidade de teste → código.** E os dois convivem: tem time maduro usando n8n pra colar sistemas na borda enquanto o núcleo do produto é código versionado, testado e observável. O erro não é usar a caixinha — é não perceber a hora em que ela virou o gargalo.

## FAQ rápido

**O n8n é gratuito?**
Self-hosted, sim — uso interno sem limite de workflows, sob a [Sustainable Use License](https://docs.n8n.io/sustainable-use-license/). O n8n Cloud é pago por execução de workflow. O que não pode, sem licença comercial: revender o n8n como serviço ou embuti-lo no seu produto.

**Preciso saber programar pra usar o n8n?**
Pra fluxos simples, não. Mas o teto de quem programa é muito mais alto: Code node em JavaScript, expressões pra transformar dados, chamadas HTTP cruas. O n8n é uma ferramenta melhor nas mãos de um dev — só não deixa de ser uma ferramenta.

**n8n substitui um dev ou um agente feito em código?**
Não. Ele acelera absurdamente a montagem de automações e protótipos de agente. Mas produto com IA em produção continua exigindo [arquitetura, guardrails, avaliação e observabilidade](https://blog.beerandcode.com.br/noticias/arquitetura-de-agentes-de-ia) — e boa parte disso o canvas não entrega.

**Posso rodar os nodes de IA com qualquer modelo?**
Sim. O AI Agent node aceita os principais provedores (Anthropic, OpenAI, Google) e modelos locais via Ollama. Os sub-nodes de memória e tools são plugáveis — por baixo, é o stack do LangChain ([docs](https://docs.n8n.io/advanced-ai/langchain/overview/)).

## Conclusão

O n8n merece o barulho que faz: é a forma mais rápida de transformar "quando acontecer X, faça Y" em coisa rodando — inclusive com agente de IA no meio. A régua é clara: cola entre sistemas, protótipo e automação interna são território dele; lógica de negócio central, produto com SLA e código que precisa de teste são território seu.

O próximo salto, pra dev, não é dominar mais caixinhas. É saber o que existe dentro delas — o loop, as tools, o contexto — pra decidir com critério quando usar e quando construir. Usar IA qualquer um já usa; construir software com IA é outra profissão, e é ela que a gente treina toda semana, ao vivo, no [Clã Beer and Code](https://beerandcode.com.br/cla?utm_source=blog&utm_medium=post&utm_campaign=o-que-e-n8n&utm_content=a-n1). É pago, é assinatura, e é exatamente o ambiente que a segunda metade deste post descreve.

Comece pela caixinha, sem culpa. Só não more nela.
