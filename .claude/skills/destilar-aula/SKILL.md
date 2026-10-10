---
name: destilar-aula
description: Transforma a transcrição de uma aula/workshop longo (4h a 8h+) num curso destilado — capítulos didáticos ordenados em sequência lógica, concisos e ricos, prontos para o aluno consumir em áudio. Acionar quando o usuário fornecer uma transcrição grande (SRT/VTT/TXT) e pedir para resumir, destilar, extrair os capítulos, organizar o conhecimento ou gerar a versão em áudio de uma aula, palestra, mentoria, workshop ou curso gravado. Faz parsing + janelamento determinístico, extração map-reduce com subagents paralelos (pra manter qualidade apesar do contexto gigante), montagem da sequência lógica, escrita do conteúdo e geração do áudio narrado (clone de voz do Lucas) reaproveitando o pipeline OmniVoice.
---

# Destilar aula longa em curso de áudio

Pega uma transcrição de 4–8h+ e devolve um curso destilado: capítulos curtos, ricos e em **sequência lógica de aprendizado**, cada um com `.md` + `.mp3`, mais um índice mestre. Pensado para o aluno ouvir.

**O problema central é o contexto gigante.** Uma aula de 8h tem ~70k palavras. Ler tudo num passe só degrada a análise. Por isso o pipeline é **map-reduce**: um script quebra a transcrição em janelas (fora do contexto do modelo, zero tokens), subagents paralelos extraem o conhecimento de cada janela com **contexto pequeno = alta fidelidade**, e só então sintetizamos. Nunca enfie a transcrição inteira num único prompt.

## Inputs

- **Transcrição** (obrigatório) — caminho de um `.srt`, `.vtt` ou `.txt`. SRT/VTT com timestamps é o ideal (permite ancorar capítulos por tempo). O usuário sempre fornece pronta.
- **Nome do curso** (obrigatório) — vira o slug do diretório de saída (`aulas/<slug>/`). Se não vier, pergunte ou derive do nome do arquivo.
- **Densidade** (opcional) — default **essência (~10-15%)**: o curso destilado deve dar ~40-50 min de áudio no total, em **poucos capítulos** (tipicamente 6-10, mesmo numa aula de 4-8h), cada um com 5-10 min. Mantém só conceitos, definições e o exemplo mais ilustrativo de cada módulo; corta repetição, divagação, tangentes e exemplos redundantes. Outras opções (peça explicitamente): `equilibrado (~25-30%)` ou `completo (~50%+)`.

## Pré-requisitos do ambiente

Os mesmos do passo de áudio da skill `criar-post-blog` (são reaproveitados):
- `.venv` da raiz com `omnivoice-infer`, `ffmpeg`, `aws` CLI v2, `python3` no PATH.
- `.env` na raiz com as credenciais OCI (`OCI_ACCESS_KEY_ID`, `OCI_SECRET_ACCESS_KEY`, `OCI_BUCKET`, `OCI_ENDPOINT`, `OCI_URL`).
- `voice/lucas.wav` + `voice/lucas.txt` em `.claude/skills/criar-post-blog/voice/` (clone de voz).
- Subagent `roteiro-narracao-aula` (Opus 4.8) carregado (passo de áudio).

Áudio é um passo **gated** no fim — não precisa do ambiente de áudio pra rodar a destilação de texto.

## Pipeline

### 1. Janelar a transcrição (determinístico)

```bash
python3 .claude/skills/destilar-aula/scripts/chunk-transcript.py <transcricao> /tmp/aula-<slug>-work
```

Imprime um **manifesto JSON** na última linha do stdout (capture-o) e escreve `chunk-NNN.txt` + `segments.json` no workdir. Ajuste o tamanho da janela só se necessário: `--minutes 18` (default) e `--overlap 75`. Aula muito densa → janelas menores (`--minutes 12`) aumentam a fidelidade ao custo de mais subagents.

Guarde do manifesto: `segments_file`, `total_chunks`, `duration` e o array `chunks`.

### 2. Destilar via Workflow (map-reduce paralelo)

Defina o diretório de saída: `curso_dir = aulas/<slug>` (caminho **absoluto**).

Chame o **Workflow** com o script bundlado. Esta skill instrui o uso do Workflow — é o opt-in; não peça confirmação extra pra orquestrar.

```
Workflow({
  scriptPath: "<abs>/.claude/skills/destilar-aula/workflows/destilar.js",
  args: {
    curso: "<Nome do curso>",
    curso_dir: "<abs>/aulas/<slug>",
    segments_file: "<segments_file do manifesto>",
    slice_script: "<abs>/.claude/skills/destilar-aula/scripts/slice-transcript.py",
    density: "essência (~10-15%)",
    chunks: [ ...array chunks do manifesto... ]
  }
})
```

O workflow faz três fases (veja `meta.phases`):
1. **Extrair** — um agente Sonnet por chunk extrai beats (conceitos, definições, exemplos, passos, frases). Contexto pequeno por agente = qualidade alta.
2. **Estruturar** — um agente funde os beats, dedup do overlap, e ordena em **sequência lógica de aprendizado** (não cronológica). Agrupa de forma **agressiva** em poucos módulos temáticos (6-10) — cada capítulo é um módulo inteiro, não um sub-tópico. Devolve o plano de capítulos com intervalos de tempo.
3. **Escrever** — um agente por capítulo relê o **trecho-fonte literal** (via `slice-transcript.py`) e escreve o `.md` em `aulas/<slug>/capitulos/NN-slug.md`, em prosa narrável.

Retorno do workflow: `{ curso, curso_dir, total_beats, chapters: [{n, slug, titulo, objetivo, intervalo, path}] }`.

Se o usuário não quiser orquestração via Workflow, há fallback manual em `references/fallback-manual.md` (fan-out com a Agent tool em lotes). Prefira o Workflow.

### 3. Índice + revisão (gate)

A partir do retorno do workflow, escreva `aulas/<slug>/chapters.json`:

```json
{ "curso": "<Nome>", "fonte": "<arquivo da transcrição>",
  "chapters": [ {"n":1,"slug":"...","titulo":"...","objetivo":"...","intervalo":"00:00 → 12:30"}, ... ] }
```

Depois gere o índice mestre:

```bash
python3 .claude/skills/destilar-aula/scripts/assemble-index.py aulas/<slug>
```

Mostre ao usuário o `INDICE.md` e 1–2 capítulos de amostra. **Pare e espere `ok`** antes de gerar áudio — áudio é caro e demorado, e o texto é o que vale revisar. Se o usuário pedir ajuste de ordem, fusão de capítulos ou mais/menos densidade, corrija o `chapters.json`/os `.md` antes de seguir.

### 4. Áudio narrado por capítulo (gated)

Só depois do `ok`. Reaproveita 100% o pipeline da `criar-post-blog`. Para **cada** capítulo, em sequência (o TTS roda um de cada vez):

1. **Roteiro narrável — via subagent `roteiro-narracao-aula` (Opus 4.8).** Use este, **não** o `roteiro-narracao` (Haiku) do blog: o áudio é o produto final que o aluno consome, então a fidelidade e o ritmo didático valem o modelo mais forte. Mesmo assim não reescreva você mesmo no fluxo principal — delegue ao subagent. Passe o body do `.md` do capítulo:

   ```
   Agent({
     subagent_type: "roteiro-narracao-aula",
     description: "Roteiro de áudio do capítulo NN <slug>",
     prompt: "Reescreva o body abaixo em texto narrável e salve em /tmp/audio-script-aula-<slug>-NN.txt.\n\nslug: aula-<slug>-NN\ntitle: <titulo>\nobjetivo: <objetivo do capítulo>\n\nbody:\n<markdown do capítulo>"
   })
   ```

2. **TTS + upload** (mesmo script da skill de blog, clone do Lucas):

   ```bash
   .claude/skills/criar-post-blog/scripts/generate-audio.sh \
     /tmp/audio-script-aula-<slug>-NN.txt aula-<slug>-NN
   ```

   Usa um slug com prefixo `aula-` pra não colidir com os mp3 dos posts (sobe pra `posts/audio/aula-<slug>-NN.mp3`). Captura a URL pública na última linha do stdout.

3. Grave a `audio_url` no objeto do capítulo em `chapters.json`.

Quando todos terminarem, rode `assemble-index.py` de novo pra atualizar os links de áudio no `INDICE.md`.

Se algum capítulo for muito longo (> ~3500 palavras no roteiro), o TTS pode demorar/cortar — divida o `.md` em duas partes antes do passo 1, ou avise o usuário.

### 5. Entrega

Mostre o caminho de `aulas/<slug>/INDICE.md`, a contagem de capítulos e quantos têm áudio. Resumo curto da sequência lógica (1 linha por capítulo).

## Layout de saída

```
aulas/<slug>/
├── INDICE.md           # índice mestre com objetivos e links de texto/áudio
├── chapters.json       # metadados ordenados (fonte de verdade do índice)
└── capitulos/
    ├── 01-<slug>.md
    ├── 02-<slug>.md
    └── ...
```
Os `.mp3` ficam no OCI (`posts/audio/aula-<slug>-NN.mp3`), referenciados por URL no índice.

## Princípios (não negociáveis)

- **Nunca** leia a transcrição inteira num único prompt. Sempre chunk → map-reduce.
- **Fidelidade > brevidade.** Condensar é cortar repetição e enrolação, não inventar nem omitir conceito ensinado. Os agentes escritores releem o trecho-fonte literal justamente pra não alucinar.
- **Sequência lógica, não cronológica.** Se o instrutor adiantou ou voltou num conceito, o capítulo reorganiza.
- **Texto é o gate.** Áudio só depois do `ok` do usuário no índice.
- Correção do usuário se aplica sem rediscutir — uma confirmação por etapa, não três.
