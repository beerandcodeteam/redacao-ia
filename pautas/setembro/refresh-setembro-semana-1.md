# Refresh — semana de 03/09 a 06/09/2026

> **STATUS: EXECUTADO em 31/08/2026.** Os 12 refreshes foram aplicados nos 18 posts via MCP
> (14 agentes, 0 falhas), e verificados no ar: os 12 URLs respondem 200, com title novo e o
> CTA do evento presente. **Não rodar de novo** — reexecutar duplicaria seções e CTAs.
> Pendências que sobraram estão em "Pós-execução", no fim do arquivo.

Origem: auditoria de canibalização da rodada `planejar-pauta` de 31/08/2026. Estes 12
temas estavam na pauta como post novo e **já existiam no blog com o mesmo ângulo**. Em vez
de canibalizar, o trabalho é refresh: atualizar conteúdo, reescrever title/meta, cruzar
links internos e plugar o CTA do AI Engineering Lab 3ª Edição
(`https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao`).

**Por que refresh rende mais que post novo aqui:** o evento é 19/09. URL já indexado, com
histórico e posição média, reage em dias — post novo leva semanas. E os posts abaixo estão
todos abaixo do potencial: metade sequer aparece no top 130 de páginas do GSC, apesar de
mirar keywords de 1.600 a 33.100 buscas/mês.

Janela de dados: GSC 02/06 a 30/08/2026 (90d). "Fora do top 130" = menos de ~86
impressões no período.

Pauta de posts novos da mesma rodada: [`semana-1.md`](semana-1.md).

---

## CTA — destino

**URL única de todos os CTAs desta rodada:**
`https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao`

É a página de evento **no próprio blog**, não a landing page. Três razões:

1. **Link interno.** Passa autoridade dentro do domínio em vez de vazar para
   `beerandcode.com.br`, e ajuda a página de evento a ranquear sozinha — as edições
   anteriores já pingam no GSC (`/eventos/ai-engineering-lab-do-prompt-ao-harness`, pos 7,0,
   CTR 4,6%).
2. **Rastreável.** Cliques em `/eventos/*` aparecem no GA4 e no GSC do blog; saída direta
   para a LP não aparece.
3. **Um lugar só pra corrigir.** Se lote, data ou link de checkout mudarem, muda o evento no
   MCP e os 12 posts continuam certos. A página de evento é quem leva para a LP e o checkout.

**Intensidade:** `leve` = uma linha + link no fechamento. `forte` = bloco de pitch (usar a
skill `montar-cta-pitch`). Cada entrada abaixo traz `onde` inserir e a `âncora` sugerida —
âncora variada, não repetir "clique aqui" nos 12.

---

## vibe-coding-o-que-e-onde-quebra
- publicar_em: 2026-09-03T09:00:00-03:00
- url: https://blog.beerandcode.com.br/noticias/vibe-coding-o-que-e-onde-quebra
- estado: fora do top 130 de páginas (< 86 impressões/90d)
- keyword_alvo: vibe coding — 33.100/mo (KD 22, +50%/ano)
- diagnostico: maior descompasso do acervo. Post publicado em 06/2026 mirando a keyword de
  maior volume viável do blog, e invisível na busca. Título genérico demais para uma SERP
  onde todo mundo escreveu "o que é vibe coding".
- acoes:
  - Reescrever title/meta com o ângulo que diferencia: onde quebra e o que fazer depois
  - Adicionar seção nova "protótipo vs. produto: a lista do que falta" (estado, custo,
    avaliação, debug) — era o post novo cortado
  - Atualizar exemplos e ferramentas para 08/2026
  - Cruzar link com `agentic-code-vs-vibe-coding-vs-sdd-tabela-decisao` e
    `agentic-code-quando-agente-escreve-executa-testa-proprio-codigo`
- cta: leve — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: no fim da seção nova "protótipo vs. produto", logo depois da lista do que falta
  - âncora: "essa lista do que falta é a ementa dos dois dias do AI Engineering Lab"

## Consolidação do cluster SDD (6 posts)
- publicar_em: 2026-09-03T13:00:00-03:00
- url: `sdd-em-laravel-pdf-vendas-specification-executavel` (633 impr, 36 cliques, pos 8,5)
  · `do-legado-ao-sdd-spec-reversa-em-modulo-legado` (282 impr, 24 cliques, pos 5,5)
  · `bmad-method-para-quem-ja-usa-sdd` (152 impr, 4 cliques, pos 6,0)
  · `paradoxo-da-especificacao-quando-sdd-vira-overengineering` (fora do top 130)
  · `5-sinais-de-que-sua-especificacao-virou-burocracia...` (fora do top 130)
  · `agentic-code-vs-vibe-coding-vs-sdd-tabela-decisao` (fora do top 130)
- keyword_alvo: spec driven development — 6.600/mo (KD 12, **+8.900%/ano**)
- diagnostico: seis posts brigando entre si e nenhum ocupando a head. O GSC mostra "sdd
  tutorial" em pos 4,7 e "como usar spec kit" em pos 16 — a demanda chega, mas se espalha.
  Falta um hub que consolide e distribua.
- acoes:
  - Eleger `sdd-em-laravel-pdf-vendas` como hub da head (é o de melhor tração) e reescrever
    title/meta para `spec driven development`, não para o caso Laravel
  - Adicionar ao hub uma seção "por onde começar" linkando os outros 5 por intenção
  - Nos outros 5, ajustar title/meta para long-tail específico (legado, BMAD,
    overengineering, burocracia, comparativo) e apontar para o hub
  - Atualizar referência de Spec Kit para a versão de 2026
- cta: leve — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao (só no hub, não nos 5 satélites)
  - onde: no bloco "por onde começar", como último item da trilha
  - âncora: "spec resolve o que o agente constrói; arquitetura resolve o que ele é"

## anatomia-de-um-agent-harness-state-tool-execution-feedback-loops-e-guardrails
- publicar_em: 2026-09-03T17:00:00-03:00
- url: https://blog.beerandcode.com.br/tutoriais/anatomia-de-um-agent-harness-state-tool-execution-feedback-loops-e-guardrails
- estado: 1.528 impressões, 15 cliques, **CTR 0,98%**, pos 8,3 — **dwell 2,5s** (653s de
  engajamento em 257 pageviews no GA4)
- keyword_alvo: agent harness / arquitetura de agente — "o que é agent harness" já pinga em
  pos 8,5
- diagnostico: **gate rodado em 31/08 — não é render.** Página responde 200 em 0,59s, 97KB,
  12 H2, texto completo no HTML. E o `<title>` já é bom: "O que é um Agent Harness? As 5
  peças do agente de produção". São outras duas causas, ambas de promessa quebrada:
  (1) **H1 ≠ title** — o H1 é "Anatomia de um Agent Harness: state, tool execution, feedback
  loops e guardrails", jargão em inglês; quem clica no SERP prometido "as 5 peças" acha que
  caiu na página errada. (2) **preâmbulo antes do payload** — a ordem é Introdução → TL;DR →
  contexto → pré-requisitos da série → só então "Os 5 componentes obrigatórios".
- acoes:
  - Reescrever o H1 para casar com o title (a promessa das 5 peças), mantendo "anatomia" e
    os termos em inglês no corpo
  - Subir "Os 5 componentes obrigatórios" para logo depois do TL;DR; rebaixar contexto e
    pré-requisitos para depois do payload
  - Cortar a seção "Pré-requisitos para acompanhar a série" da dobra inicial — ela pressupõe
    um leitor de série que a busca orgânica não é
  - Cruzar link com `anatomia-de-um-harness-em-producao-as-6-camadas...` (273 impr, pos 7,0)
    — os dois competem entre si
- cta: forte — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: depois da seção de guardrails E **só depois** de resolver o dwell de 2,5s — CTA em
    página que ninguém lê é desperdício
  - âncora: "as 6 camadas deste post são o esqueleto do Lab — lá elas são montadas ao vivo"

## quanto-ganha-engenheiro-de-ia-brasil-2026
- publicar_em: 2026-09-04T09:00:00-03:00
- url: https://blog.beerandcode.com.br/noticias/quanto-ganha-engenheiro-de-ia-brasil-2026
- estado: **5.928 impressões**, 32 cliques, **CTR 0,54%**, pos 6,7
- keyword_alvo: quanto ganha engenheiro de ia — cluster `engenheiro de ia` 4.400/mo (+238%/ano)
- diagnostico: CTR de 0,54% em posição 6,7 é metade do esperado. Título ou meta não está
  entregando o número que a busca quer. Maior volume de impressão desperdiçada da vertente.
- acoes:
  - Reescrever title/meta colocando faixa salarial concreta e ano no snippet
  - Atualizar dados para o segundo semestre de 2026
  - Adicionar seção "o que a vaga pede de verdade" — era o post novo cortado
  - Linkar `30-perguntas-entrevista-ai-engineer` e `portfolio-ai-engineer-5-projetos-sem-mestrado`
- cta: forte — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: logo após a faixa salarial, no ponto de maior intenção da página
  - âncora: "o que separa a faixa de baixo da de cima é arquitetura, não anos de casa"
  - nota: melhor par ticket/intenção da semana — R$ 37 contra uma decisão de carreira

## engenheiro-de-ia-2026-o-que-faz
- publicar_em: 2026-09-04T13:00:00-03:00
- url: https://blog.beerandcode.com.br/noticias/engenheiro-de-ia-2026-o-que-faz
- estado: 155 impressões, 4 cliques, pos 9,1
- keyword_alvo: o que faz um engenheiro de ia — 110/mo (+180%/ano); head `engenheiro de ia`
  4.400/mo
- diagnostico: post certo na keyword certa, parado em pos 9,1 com pouca impressão. Precisa
  de profundidade e de sinal interno — hoje quase não recebe link de dentro do blog.
- acoes:
  - Adicionar a rotina concreta hora a hora (quanto é código, quanto é avaliação, quanto é
    reunião) — o ângulo que a SERP genérica não cobre
  - Diferenciar explicitamente de `desenvolvedor-de-ia-vs-engenheiro-de-ia` (244 impr,
    pos 18,6) e linkar
  - Receber link do refresh de `quanto-ganha-engenheiro-de-ia` (publicado no dia anterior)
- cta: forte — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: no fim da rotina hora a hora, quando o leitor acabou de ver o que a função exige
  - âncora: "a rotina acima é o conteúdo do Lab, na mesma ordem"

## o-que-e-embedding
- publicar_em: 2026-09-04T17:00:00-03:00
- url: https://blog.beerandcode.com.br/tutoriais/o-que-e-embedding
- estado: fora do top 130 de páginas
- keyword_alvo: embeddings — 1.600/mo (KD 31, +46%/ano)
- diagnostico: post bom, keyword em alta, zero visibilidade. O título ataca "o que é
  embedding" (singular), enquanto o volume está em `embeddings`.
- acoes:
  - Ajustar title/meta para a forma com volume
  - Adicionar comparativo de modelos de embedding disponíveis em 2026 (dimensão, idioma,
    custo) — hoje o post cobre o conceito mas não a escolha
  - Cruzar link com `rag-do-zero-chunking-embeddings-busca` (165 impr, pos 5,7) e
    `banco-de-dados-vetorial`, definindo o escopo de cada um
- cta: leve — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: no fechamento, depois do comparativo de modelos
  - âncora: "embedding é uma peça; o Lab monta o sistema inteiro em volta dela"

## banco-de-dados-vetorial
- publicar_em: 2026-09-05T09:00:00-03:00
- url: https://blog.beerandcode.com.br/noticias/banco-de-dados-vetorial
- estado: fora do top 130 de páginas
- keyword_alvo: banco de dados vetorial — 590/mo; **top 10 com 0,5 backlink médio**, a SERP
  mais vazia de toda a pesquisa
- diagnostico: **gate rodado em 31/08 — não é indexação.** GSC retorna `PASS /
  "Submitted and indexed"`, último crawl em 13/08, canônica correta, robots liberado. Está
  indexado há semanas e não recebe impressão: é falta de autoridade interna (quase nenhum
  link apontando pra ele) e de profundidade — o post explica o conceito mas não ajuda a
  escolher, que é o que a busca quer. A SERP não tem concorrência com autoridade.
- acoes:
  - Adicionar o comparativo que falta: pgvector vs. Qdrant vs. Pinecone vs. Chroma por
    custo, operação e latência, com o número que define quando o dedicado passa a valer
  - Puxar links internos de `pgvector-postgres-memoria-do-seu-agente`, `rag-do-zero...` e
    `guia-rag-backend-pgvector-laravel`
- cta: leve — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: no fim, junto ao critério de quando o banco dedicado passa a valer
  - âncora: "esse tipo de decisão de arquitetura é o que se treina no Lab"

## arquitetura-de-agentes-de-ia
- publicar_em: 2026-09-05T13:00:00-03:00
- url: https://blog.beerandcode.com.br/noticias/arquitetura-de-agentes-de-ia
- estado: 111 impressões, 2 cliques, pos 6,8
- keyword_alvo: arquitetura de agentes de ia — 50/mo; cluster `agente de ia` 8.100/mo (KD 4)
- diagnostico: é o post que mais se parece com o conteúdo do Lab e o que menos tráfego tem.
  Posição 6,8 com 111 impressões significa keyword de cauda muito estreita — precisa
  ampliar para o cluster, não só para a keyword exata.
- acoes:
  - Adicionar o diagrama de referência preenchível e três problemas reais desenhados do
    zero — era o post novo "do problema ao diagrama" cortado
  - Ampliar para o cluster: incluir seções que respondam `agente de ia` e
    `como criar um agente de ia` sem canibalizar `o-que-e-um-agente-de-ia` e
    `como-criar-um-agente-de-ia-do-zero` (linkar ambos)
  - Reforçar o checklist de produção que o post já tem e transformá-lo em âncora linkável
- cta: forte — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: **duas inserções** — uma logo abaixo do diagrama de referência e outra no fim do
    checklist de produção
  - âncora: "o diagrama acima é o entregável do dia 1 do Lab"
  - nota: post-espelho do evento — é o melhor imóvel da vertente para o CTA

## sistemas-multiagentes-orquestracao-assincrona
- publicar_em: 2026-09-05T17:00:00-03:00
- url: https://blog.beerandcode.com.br/tutoriais/sistemas-multiagentes-orquestracao-assincrona
- estado: fora do top 130 de páginas
- keyword_alvo: sistema multiagente — 140/mo (**+357%/ano**, maior aceleração da pesquisa)
- diagnostico: volume pequeno mas em explosão. Post cobre exatamente a intenção ("quando
  vale dividir e quando NÃO dividir") e não capitaliza. Vale posicionar agora, antes da
  curva subir.
- acoes:
  - Ajustar title/meta para a forma com volume (`sistema multiagente`, singular)
  - Atualizar com a conta de custo e latência de handoff em números de 2026
  - Cruzar link com `multi-agent-com-claude-separando-search-judge-e-writer...` (que ataca o
    caso concreto) definindo hub e satélite
- cta: leve — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: no fechamento, depois da conta de custo e latência de handoff
  - âncora: "decidir dividir ou não é módulo do Lab"

## 4-niveis-autonomia-agentic-code
- publicar_em: 2026-09-06T09:00:00-03:00
- url: https://blog.beerandcode.com.br/noticias/4-niveis-autonomia-agentic-code
- estado: fora do top 130 de páginas
- keyword_alvo: agente autônomo — 140/mo; top 10 com 0,9 backlink médio
- diagnostico: o post fala de "agentic code", termo que o blog cunhou e que não tem volume
  de busca. A demanda existe em `agente autônomo` e `níveis de autonomia`, que o post
  responde mas não menciona no título.
- acoes:
  - Reescrever title/meta para `agente autônomo` / níveis de autonomia, mantendo agentic
    code no corpo
  - Generalizar os 4 níveis para além de código (o post é bom e está preso ao caso de dev)
  - Adicionar a seção human-in-the-loop sem virar gargalo
- cta: leve — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: no fim, junto à seção human-in-the-loop
  - âncora: "subir de nível exige guardrails e observabilidade — os dois estão no Lab"

## evals-para-agentes-de-ia-llm-as-a-judge
- publicar_em: 2026-09-06T13:00:00-03:00
- url: https://blog.beerandcode.com.br/tutoriais/evals-para-agentes-de-ia-llm-as-a-judge
- estado: 249 impressões, 5 cliques, pos 6,5
- keyword_alvo: avaliação de agentes de ia / evals llm — sem volume mensurável no BR
- diagnostico: keyword sem demanda de busca em português. Não adianta otimizar para SEO —
  o valor deste post é conversão e autoridade. Também compete com
  `avaliacao-de-agentes-de-ia-evals-honestos` (119 impr, pos 7,3).
- acoes:
  - Consolidar os dois posts de evals: eleger este como principal e apontar o outro
  - Adicionar a seção do gap teste↔produção ("passou em 47 testes e quebrou com o primeiro
    cliente") — era o post novo cortado
  - Adicionar montagem de conjunto de avaliação a partir de tráfego real
- cta: forte — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: no fim da seção nova do gap teste↔produção, com a dor ainda quente
  - âncora: "montar eval que pega o que o teste não pega é o módulo 10 do Lab"

## observabilidade-agentes-ia-langsmith-langfuse-helicone
- publicar_em: 2026-09-06T17:00:00-03:00
- url: https://blog.beerandcode.com.br/tutoriais/observabilidade-agentes-ia-langsmith-langfuse-helicone
- estado: fora do top 130 de páginas
- keyword_alvo: observabilidade de llm / tracing — sem volume mensurável no BR
- diagnostico: post de 05/2026 comparando ferramentas, com pelo menos uma delas descrita
  como em maintenance mode — conteúdo com prazo de validade curto e já vencido. Sem volume
  de busca, o papel é conversão.
- acoes:
  - Atualizar o estado das três ferramentas para 08/2026 (o que mudou, o que morreu)
  - Adicionar a parte que falta e é a dor real: tracing sem plataforma, o mínimo viável em
    qualquer stack, e o que logar em cada passo do loop — era o post novo cortado
  - Cruzar link com `anatomia-de-um-agent-harness` (refresh de 03/09)
- cta: forte — https://blog.beerandcode.com.br/eventos/ai-engineering-lab-3a-edicao
  - onde: depois da seção "tracing sem plataforma", que é a parte acionável
  - âncora: "responder 'por que ele fez isso' é o módulo 9 do Lab"

---

## Fora da vertente — mas é o maior número do blog

Não entram nesta semana de refresh porque são outro cluster (news-jacking de modelo). Ficam
registrados porque rendem mais que qualquer item acima, e o CTA do Lab deveria estar neles
antes de 19/09 — mesma URL de destino da seção acima.

| página | estado (90d) | ação |
|---|---|---|
| `gpt-5-6-sol-terra-luna-qual-usar` | **44.964 impr**, 380 cliques, CTR 0,85%, pos 6,5 | reescrever title/meta — +1pp de CTR = +450 cliques/90d |
| `codex-limite-de-uso` | 15.784 impr, 729 cliques, pos 5,1 | post nº 1 do blog — bloco de CTA para `/eventos/ai-engineering-lab-3a-edicao` |
| `kimi-k3-benchmarks-vs-claude` | 14.311 impr, 363 cliques | CTA → `/eventos/ai-engineering-lab-3a-edicao` |
| `gpt-5-6-sol-ultra-codex` | 13.528 impr, 272 cliques | CTA → `/eventos/ai-engineering-lab-3a-edicao` |
| `melhor-ia-para-programar-2026-claude-code-vs-codex` | 10.222 impr, 150 cliques, dwell 53s | maior permanência do blog (53s) — melhor imóvel para o CTA → `/eventos/ai-engineering-lab-3a-edicao` |
| `qwen-3-8-max` | 8.487 impr, 224 cliques | CTA → `/eventos/ai-engineering-lab-3a-edicao` |
| `como-economizar-tokens-claude-code-codex-cursor` | 4.645 impr, 107 cliques | CTA → `/eventos/ai-engineering-lab-3a-edicao` + link para o post de custo de 01/09 |
| `limite-de-tokens-chatgpt-ia-esquece` | 1.749 impr, CTR **0,40%** | reescrever title/meta |
| `claude-design-como-usar-para-devs` | 2.021 impr, CTR 0,69% | reescrever title/meta |
| `ngrok-vs-expose...` | 2.697 impr, CTR 0,37% | reescrever title/meta |

Soma das 7 primeiras: ~29 cliques/dia, ~550 visitas até 19/09 sem depender de ranquear
nada novo.

---

## Pós-execução (31/08/2026)

Os 12 refreshes foram aplicados. O que sobrou de aberto, em ordem de urgência:

### 1. CTA para eventos já encerrados no corpo de 6 posts
Achado durante a execução, não estava previsto. Estes posts linkam, no corpo, landing pages
de eventos que **já aconteceram**:

| post | evento morto no corpo |
|---|---|
| `do-legado-ao-sdd-spec-reversa-em-modulo-legado` | `do-prompt-ao-harness...` (11–12/07) |
| `bmad-method-para-quem-ja-usa-sdd` | `do-prompt-ao-harness...` (11–12/07) |
| `agentic-code-vs-vibe-coding-vs-sdd-tabela-decisao` | `do-prompt-ao-harness...` (11–12/07) |
| `paradoxo-da-especificacao-quando-sdd-vira-overengineering` | `harness-engineering-com-claude-code` (16–17/06) |
| `5-sinais-de-que-sua-especificacao-virou-burocracia...` | `harness-engineering-com-claude-code` (16–17/06) |
| `engenheiro-de-ia-2026-o-que-faz` | `harness-engineering-com-claude-code` (16–17/06) — 2 ocorrências |

Os agentes não tocaram porque o spec dizia "não altere mais nada". A varredura provavelmente
pega mais posts fora desta lista — vale um `grep` por `landing-pages/` em todo o acervo antes
de decidir se troca pelo evento atual ou remove.

### 2. Estado das ferramentas em `observabilidade-agentes-ia-langsmith-langfuse-helicone`
O agente **não inventou status** — reescreveu por critério atemporal e deixou marcado. Precisa
de confirmação humana: pricing/self-host do LangSmith em 08/2026; versão do Langfuse e se o
docker-compose ainda sobe os 6 serviços com Postgres 17; e principalmente **se a Helicone ainda
está em maintenance mode** depois da aquisição pela Mintlify (03/03/2026). Se a Helicone morreu
ou voltou, a seção e o FAQ pedem uma passada. Os pacotes PHP citados no exemplo
(`CuracelDev/langfuse-laravel`, `mliviu79/laravel-langfuse-prism`) também não foram verificados.

### 3. Mudança de H1 em dois posts que já ranqueiam — monitorar
`do-legado-ao-sdd` (pos 5,5) e `bmad-method` (pos 6,0) tiveram o campo `title` alterado, o que
muda o H1 visível. É a mudança de maior risco da leva. Acompanhar CTR e posição no GSC por 2–3
semanas; se cair, reverter só o campo `title` mantendo o `meta_title` novo.

### 4. Âncora do checklist em `arquitetura-de-agentes-de-ia`
O heading virou "Checklist de produção de agentes de IA" para ser linkável de outros posts, mas
a string exata da âncora depende da slugificação do tema. Confirmar a âncora renderizada antes
de apontar links para ela.

### 5. Widget de evento do tema já cobre o site inteiro
Verificado em `codex-limite-de-uso`, post que o refresh não tocou: a página já exibe
`landing-pages/ai-engineering-lab`. Ou seja, ao cadastrar o evento no MCP, o tema passou a
promovê-lo em **todas** as páginas do blog automaticamente. Isso reduz a urgência do item "CTA
nos 7 posts de maior tráfego" da tabela acima — mas CTA contextual no corpo converte melhor que
widget, então a ação continua valendo para os 3–4 maiores.
