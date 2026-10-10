# Fallback manual (sem Workflow)

Use só se o usuário não quiser orquestração via Workflow. É mais frágil — o controle de fluxo vira responsabilidade sua. Prefira `workflows/destilar.js`.

A ideia é a mesma do workflow, feita à mão com a **Agent tool**:

## 1. Extrair (map) — em lotes

Os chunks já estão em `chunk-NNN.txt`. Dispare subagents em paralelo, **em lotes de ~8** (não todos de uma vez), cada um com `subagent_type: "general-purpose"`, model Sonnet quando possível:

> Leia o arquivo `<chunk-NNN.txt>`. Extraia, de forma detalhista e fiel, todas as unidades de ensino (conceitos, definições, exemplos, passos práticos, frases marcantes do instrutor) com timestamps aproximados. Ignore repetição e conversa morta. Marque onde começa um novo grande tópico. Devolva JSON: `{beats:[{topic,summary,concepts[],definitions[],examples[],practical_steps[],key_quotes[],start,end,new_chapter_signal}]}`.

Acumule os beats de todos os chunks num arquivo `/tmp/aula-<slug>-beats.json`.

## 2. Estruturar (reduce) — um agente

Passe TODOS os beats compactados (sem o texto-fonte bruto) a um único agente:

> Agrupe estes beats em capítulos coerentes e ordene-os em sequência LÓGICA de aprendizado (não cronológica). Funda duplicatas do overlap. Devolva `{chapters:[{n,slug,titulo,objetivo,intervalos[],pontos[]}]}`.

Salve em `aulas/<slug>/chapters.json`.

## 3. Escrever — um agente por capítulo

Para cada capítulo, um subagent que **relê o trecho-fonte** com `slice-transcript.py` antes de escrever:

> Escreva o capítulo `<n> — <titulo>` em Markdown narrável (didático, frases curtas, sem código longo), densidade `<density>`, em `aulas/<slug>/capitulos/NN-slug.md`. Antes, leia o trecho-fonte literal: `python3 .../slice-transcript.py <segments.json> "<start>" "<end>"` para cada intervalo. Termine com "## Em resumo".

Depois siga os passos 3–5 do `SKILL.md` (índice + áudio) normalmente.

> Custo: para uma aula de 8h são ~30-48 chunks + ~15-30 capítulos = dezenas de subagents. O Workflow faz isso com cap de concorrência e resume automático; o manual não. Por isso o Workflow é o caminho recomendado.
