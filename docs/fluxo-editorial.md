# Fluxo editorial

Do tema ao post agendado, em quatro etapas: **descobrir** (news-jacking e evergreen), **fechar a pauta**, **rodar o loop** e **medir**. Cada etapa é uma skill; a fonte de verdade de cada uma é o `SKILL.md` correspondente em `.claude/skills/`. Este documento explica como elas se encaixam e por que os critérios são o que são.

Regra geral: as skills de descoberta e de pauta **não escrevem nem publicam**. Elas entregam candidatos e esperam aprovação. Quem escreve é a `criar-post-blog`.

## 1. News-jacking: `/cacar-news-jacking`

**Tese.** Um blog pequeno não ganha de portal grande em termo de cabeça, mas ganha em velocidade: chegar primeiro numa keyword de cauda longa recém-nascida, antes de o Google montar a SERP. Os posts que mais renderam no blog venceram assim, com título de comparação ou drama publicado enquanto só havia dez links azuis.

**Como roda.**

1. **Detectar.** `scripts/detect.sh` bate em todas as fontes numa passada e marca o que é novo desde a última execução:

   ```bash
   bash .claude/skills/cacar-news-jacking/scripts/detect.sh                      # foco default, janela de 48h
   bash .claude/skills/cacar-news-jacking/scripts/detect.sh -q "claude OR fable" # foco custom
   bash .claude/skills/cacar-news-jacking/scripts/detect.sh -h 72                # janela de 72h
   ```

   Fontes: Hacker News, diff do catálogo do OpenRouter (modelo novo ou removido), releases no GitHub, Reddit, NewsAPI ou GDELT. O agente complementa com o RSS dos labs via `WebFetch`.
2. **X/Twitter via Grok.** A skill monta um prompt, você cola no Grok e devolve as tendências. O que só aparece no X ganha bônus de velocidade.
3. **Qualificar** no DataForSEO, tudo em lote: a derivada do volume (não o valor absoluto), a demanda dentro das IAs (`ai_search_volume`), o formato da SERP e, só nos sobreviventes, a SERP ao vivo.
4. **Cruzar** com o Search Console (já pinga impressão?) e com os posts existentes (já tem post? então é atualização, não pauta nova).
5. **Pontuar e entregar** um radar com veredito por candidato: `surfar agora`, `surfar se acelerar`, `atualizar post existente`, `evergreen → planejar-pauta` ou `descartar`.
6. **Conferir** 48 a 72 horas depois de o post ir ao ar: entrou no top 10? virou referência de AI Overview?

**Critérios que definem a frente.**

- Volume BR perto de zero é o estado normal de um termo com 48 horas de vida. Não reprova. O que reprova é curva caindo.
- A janela se mede, não se intui: SERP sem `featured_snippet`, `people_also_ask` e `ai_overview` está aberta. Com esses blocos montados, está fechando.
- Título com número, comparação ou drama. O título explicativo neutro rankeia e não leva clique.

## 2. Evergreen: `/minerar-evergreen`

**Tese.** News-jacking é tráfego em cima de areia: seca em semanas. Evergreen é o piso, a demanda que continua existindo daqui a um ou dois anos.

**Como roda.**

1. **Baseline** do domínio no Search Console e no DataForSEO (o que já rankeia e em que posição).
2. **Minerar** em três frentes: expansão de seeds (perguntas reais de busca), *striking distance* (termos em posição 5 a 20 sem post dedicado) e gap contra concorrentes.
3. **Gate de durabilidade**, obrigatório, na curva de 12 meses de `monthly_searches`:

   | curva | leitura | destino |
   |---|---|---|
   | plana ou subindo | evergreen legítimo | passa |
   | queda forte | tema morto | descarta |
   | foguete | é hype, não evergreen | vai para `cacar-news-jacking` |
   | sazonal previsível | passa | marca a sazonalidade na pauta |

4. **Qualificar** (um post por `core_keyword`, KD, intenção, SERP dos finalistas) e **pontuar**.

**Critérios que definem a frente.**

- **Gate de dor, antes de todos os outros.** O que funciona é dor de consciência baixa: quem busca tem um problema concreto e ainda não escolheu produto ("como economizar tokens", "qual a melhor IA para programar"). Pauta centrada em produto ("como instalar X") é news-jacking disfarçado e morre quando a ferramenta muda. Produto só entra como resposta, nunca como título.
- Aqui volume zero **é** problema: significa tema sem demanda.
- Título casa a intenção informacional. É a regra inversa do news-jacking.
- SERP cujo top 10 tem mais de ~300 domínios de referência está fora de alcance, por mais baixo que o KD pareça.

## 3. Criação de pauta: `/planejar-pauta`

Recebe uma lista de temas (vinda das duas frentes acima, do painel SEO ou da sua cabeça) e devolve duas camadas:

1. **Tabela de triagem**, no chat: todos os temas com keyword-alvo, volume, KD, intenção, sinal de quick win e veredito (`escrever agora`, `escrever depois`, `otimizar post existente`, `reposicionar`, `descartar`). É o raciocínio, não vai para arquivo.
2. **Pauta dos aprovados**, em formato fixo de campos, gravada em `pautas/<mês>/semana-N.md`.

Os sinais cruzados: Search Console (tração e striking distance), DataForSEO (volume, KD, intenção, SERP, perguntas do PAA), GA4 (o conteúdo vizinho engaja depois do clique?). Duas travas rebaixam qualquer tema: canibalização (já existe post rankeando) e ganhabilidade (SERP dominada por domínios muito mais fortes).

### Formato do arquivo de pauta

Um post por `## h2`. É exatamente o que o loop consome:

```markdown
## Título do post
- publicar_em: 2026-09-15T09:00:00-03:00
- autor: slug-do-autor
- categoria: tutoriais
- resumo: 2 a 4 linhas com o que o post entrega e o diferencial
- hook: 1 ou 2 frases no tom da marca
- bullets:
  - os H2 previstos do post
- perguntas_paa:
  - perguntas literais do bloco "As pessoas também perguntam"
- keyword_principal: keyword-alvo
- keywords_secundarias: variações, long-tail, termos de decisão
- tags: tags reutilizáveis
- dificuldade: easy | medium | hard
- volume: ~1.300/mo (KD 23, +60%/ano)
```

`publicar_em` é obrigatório (post sem data é pulado) e sempre com offset `-03:00`. Posts no mesmo dia escalonam a hora. O campo `volume` também carrega as notas de anti-canibalização e os links internos obrigatórios, que o loop repassa ao escritor.

A pasta `pautas/` traz o histórico real: arquivos `semana-N.md` (pauta da semana), `semana-N-newsjacking-DD-MM.md` (caça do dia), `semana-N-evergreen-DD-MM.md` (mineração) e `semana-N-batch.md` (o merge das duas frentes pronto para rodar).

## 4. Rodar o loop: `criar-posts-batch`

O loop pega um arquivo de pauta e produz um post completo por `## h2`. Há duas implementações do mesmo pipeline.

### Opção A: workflow (recomendada)

Dentro da sessão do Claude Code, peça o workflow pelo nome e passe o arquivo:

```
Rode o workflow criar-posts-batch com o arquivo pautas/setembro/semana-1-batch.md
```

Os argumentos chegam ao script como JSON (`{ "file": "pautas/setembro/semana-1-batch.md" }`), então peça em linguagem natural em vez de digitar o caminho solto depois de uma barra.

O workflow (`.claude/workflows/criar-posts-batch.js`) roda em quatro fases:

| fase | o que faz | modelo |
|---|---|---|
| Parse | lê o `.md` e quebra em posts | principal |
| Pesquisa + Escrita | passos 1 a 3 da `criar-post-blog`: fontes oficiais, outline, body em Markdown | principal |
| Roteiro | reescreve o body em texto narrável | Haiku (subagent `roteiro-narracao`) |
| Capa + Áudio + Publicar | `generate-cover.sh`, `generate-audio.sh`, `UploadImage` e `CreatePost` agendado | principal |

Os posts andam em paralelo, em blocos de 3 (`CONCURRENCY`), porque o TTS roda local e é pesado. Argumentos aceitos:

| argumento | efeito |
|---|---|
| `file` | caminho do markdown (obrigatório) |
| `cta` | `{ url, label, pitch }` aplicado a todos os posts |
| `from` / `only` | retoma do N-ésimo post, ou roda só ele |
| `dryRun` | para depois do Parse e devolve os prompts |
| `withAudio: false` | pula roteiro e TTS |

### Opção B: script headless

Fora da sessão, uma invocação `claude -p` por post, em sequência:

```bash
scripts/criar-posts-batch.py pautas/setembro/semana-1-batch.md
scripts/criar-posts-batch.py arquivo.md --dry-run      # só imprime os prompts
scripts/criar-posts-batch.py arquivo.md --from 3       # retoma do 3º
scripts/criar-posts-batch.py arquivo.md --only 2       # só o 2º
scripts/criar-posts-batch.py arquivo.md \
    --cta-url "https://exemplo.com/evento" \
    --cta-label "Nome do evento" \
    --cta-pitch "uma linha de contexto"
```

Roda com `--dangerously-skip-permissions` e lê `.env` e `.mcp.json` da raiz.

### O que acontece com cada post

1. **Pesquisa** em fontes oficiais. Fato sem fonte verificável não entra.
2. **Outline** e **escrita** no tom da marca (`references/brand-voice.md`), com a keyword principal no título, no primeiro parágrafo, num H2 e no slug.
3. **CTA embutido**, quando há destino: 1 ou 2 frases em prosa no primeiro terço do post, sem seção dedicada. Sem destino, o post sai sem CTA.
4. **Capa** gerada no Gemini e enviada ao storage.
5. **Áudio**: roteiro narrável em Haiku, depois TTS com voz clonada e upload do mp3.
6. **Gate de SEO** (`revisar-seo-post`): corrige as travas que derrubam o MCP e revisa o on-page. Em batch aplica as correções seguras e segue; o que exigiria reescrever vira aviso no relatório.
7. **Publicação** via MCP com status agendado. O scheduler do blog publica quando `published_at` chega.

### Cuidados que já custaram um batch

- **O TTS precisa ser síncrono.** Sessão headless não tem loop para "acordar depois": se o áudio rodar em background, a sessão encerra com sucesso e o post nunca é criado.
- **`audio_url` vai com o domínio do blog**, não com a URL nativa do storage, senão o player quebra com 404.
- **Categoria, autor e tags vêm do MCP** (`ListCategories`, `ListAuthors`, `ListTags`), nunca inventados.
- Nada é publicado direto: `PublishPost` só com OK explícito.

### Post avulso e manutenção

- Um post só, com revisão humana em cada etapa (outline, capa, relatório de SEO): peça o post na sessão e a skill `criar-post-blog` conduz.
- Posts que ficaram sem áudio: `scripts/gerar-audios-existentes.py` (aceita `--discover-only`, `--from`, `--only`, `--dry-run`).

## 5. Medir: painel SEO

O painel em `seo-report/` fecha o ciclo. Ele cruza Search Console, GA4, DataForSEO e PageSpeed, e tem um botão que dispara a `planejar-pauta` com o relatório atual como ponto de partida. Detalhes em [seo-report/README.md](../seo-report/README.md).

O que voltar como oportunidade (posição 5 a 15 com impressão, keyword quente, post com impressão alta e engajamento baixo) é a entrada da próxima pauta.

## Skills de apoio

| skill | papel |
|---|---|
| `montar-cta-pitch` | escolhe ângulo e nível do CTA quando o destino é o produto ou um evento da marca |
| `curar-tabnews` | acha posts do TabNews para comentar, com ângulo sugerido |
| `destilar-aula` | transforma transcrição de aula longa em capítulos com áudio |
