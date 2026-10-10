# Estudo: "Grande rollback" vs "guerra de generosidade" — o que os dados sustentam

> **Data:** 18/07/2026 · **Método:** deep research com verificação adversarial em DUAS passadas (passada 1: 29 fontes → 139 claims → 25 verificadas → 20 confirmadas, 5 refutadas · passada 2, ótica do reinvestimento: 24 fontes → 118 claims → 25 verificadas → 20 confirmadas, 5 refutadas). Cada afirmação abaixo está marcada como **FATO**, **ESTIMATIVA** ou **ESPECULAÇÃO**, com fonte.
> **Sensível ao tempo:** a promoção de +50% expira 19/07 e a mudança do Fable 5 entra em 20/07 — o efeito real só será observável depois.

## A pergunta

O discurso corrente: "o custo de inferência é insustentável pra OpenAI/Anthropic, vem o **grande rollback** — tudo mais caro e menos acessível" (Ed Zitron & cia). A observação prática: o oposto — OpenAI e Anthropic brigando por quem deixa usar MAIS (Codex sem limite de 5h, +50% de limite semanal, Fable 5 entrando nos planos Max, crédito de US$ 100). Quem está certo?

## Veredito (a tese que os dados sustentam)

**Nenhum dos dois extremos. A tese vencedora é híbrida e tem 4 pernas:**

1. **Não há rollback de preço.** O preço por unidade de capacidade FIXA cai exponencialmente (5x–40x+/ano), e ~3x/ano disso é eficiência algorítmica **estrutural** — não subsídio reversível.
2. **Mas o steel-man do rollback é real.** As margens agregadas dos dois labs pioraram contra as próprias metas, a inferência da OpenAI quadruplicou pra ~US$ 8,4 bi (metade queimada em usuário gratuito) e as projeções de prejuízo são gigantes.
3. **A nuance central: preço por token CAI, custo por tarefa SOBE.** Rodar a fronteira (reasoning/agentes) fica 3x–18x mais caro por ano. As duas narrativas são verdadeiras ao mesmo tempo porque medem coisas diferentes.
4. **A "generosidade" de julho é parcialmente rollback reembalado.** O Fable 5 entra nos Max plans — mas a 50% dos limites, coincidindo com o fim da promoção de +50%; o Pro é empurrado pra créditos a preço de API. A imprensa se dividiu no framing do MESMO anúncio: Simon Willison leu como generosidade, The Decoder leu como corte.

**Frase-síntese:** não é guerra de generosidade Uber-style nem colapso — é **gestão de capacidade segmentada**: consumer possivelmente subsidiado pela margem enterprise, num mercado onde o custo unitário despenca mas a conta total explode.

---

## Os fatos confirmados (20 claims → 12 achados)

### A. O custo por capacidade despenca — e é estrutural

- **FATO** — O preço pra atingir um nível FIXO de capacidade cai exponencialmente: **40x/ano** pra performance nível GPT-4 em GPQA Diamond; entre 9x e 900x/ano em seis benchmarks, mediana **50x/ano** (Epoch AI, até mar/2025); **5x–10x/ano** na estimativa mais conservadora e recente (MIT FutureTech, abr/2024–nov/2025). Concreto: GPT-4 lançou a $30/$60 por 1M tokens (2023); GPT-5 a $1.25/$10 (ago/2025) — **queda de ~83% no output do flagship**. `[3-0 ×4]`
  - Fontes: epoch.ai/data-insights/llm-inference-price-trends · arxiv.org/html/2511.23455v2 · pricepertoken.com/trends
- **FATO/ESTIMATIVA** — Descontando hardware (~30%/ano), a eficiência algorítmica isolada avança **~3x/ano** (IC 90%: 1,54x–6,75x). O estudo usa modelos open-weight justamente pra CONTROLAR o efeito de preço subsidiado — ou seja, a barateação **não é só queima de caixa reversível**. `[3-0]`
- **FATO (framing disputado)** — O preço de API cai por pressão competitiva e comoditiza o negócio (~10x/ano a capacidade constante, a16z "LLMflation"; ~80% de corte setorial 2025→2026) — **mas o tier flagship não barateia na mesma velocidade** (o o1 lançou ao mesmo preço de output do GPT-3 de 2021: $60/MTok). `[2-1]`

### B. A nuance que resolve o debate

- **FATO** — Apesar da queda por unidade de capacidade, **o custo de rodar modelos FRONTIER sobe 3x–18x/ano**, puxado por modelos maiores e demanda de reasoning (MIT FutureTech, medido em GPQA-Diamond, SWE-bench Verified e AIME). "Preço por token cai MAS custo por tarefa sobe" é literalmente o que o paper mede. `[3-0]`
  - Caveat: benchmark-dependente; mede custo de performance de fronteira, não custo agregado de serving.

### C. Margens — o steel-man do rollback é real

- **FATO (docs financeiros via The Information)** — Margem bruta ajustada da OpenAI em 2025: **33%** (vs 40% em 2024 e meta interna de 46%). Inferência **quadruplicou pra ~US$ 8,4 bi** (previsão era 6,6), com **~US$ 3,9 bi (quase metade) servindo usuários NÃO-pagantes** — em parte capacidade on-demand mais cara comprada quando a demanda estourou. `[3-0 ×2]`
  - Nota: Zitron reporta US$ 8,67 bi só até Q3/2025 — discrepância provável de escopo contábil; ambos concordam na ordem (~US$ 8–9 bi, ~4x YoY).
- **FATO (projeções internas reportadas)** — O steel-man máximo: OpenAI projeta **prejuízo de US$ 14 bi em 2026 e US$ 74 bi em 2028**, com US$ 121 bi de compute só em 2028 e sem lucro antes de 2029–2030. Revisado fortemente para PIOR vs o vintage de out/2024. São projeções da própria empresa reportadas por terceiros, não auditadas. `[3-0]`
- **FATO (projeção)** — Anthropic: margem bruta de **-94% (2024) → +40% projetado (2025)** — melhora dramática, mas 10 p.p. abaixo da meta de 50%, porque a inferência em Google/Amazon veio ~23% acima do previsto. A inferência não é "insustentável" (virou positiva rápido), mas as metas seguem sendo perdidas. `[3-0]`

### D. Unit economics do PAGANTE melhora — o furo na tese do colapso

- **FATO (dados internos vazados, não auditados)** — A margem de computação da OpenAI **em usuários pagantes**: ~35% (jan/2024) → ~52% (fim/2024) → **~70% (out/2025)**. Inferência pra quem paga é vendida bem acima do custo e melhorando. **O problema financeiro está no free tier, no treino e no capex — não no unit economics do pagante.** `[3-0]`
  - Fontes: The Information (21/12/2025), corroborado por Bloomberg, Fortune, PYMNTS.
- **FATO parcial + ESTIMATIVA** — **~85% da receita da Anthropic é enterprise** (1.000+ empresas gastando >US$ 1 mi/ano em abr/2026, o dobro de fev/2026; 8 das Fortune 10 — auto-reportado). Enterprise geraria "3–5x mais receita por token" (**estimativa de analista sem fonte primária** — marcar como tal). Sugere que a generosidade consumer é **subsídio cruzado bancado por margem enterprise**, não burn Uber-style puro. `[3-0, evidência medium]`

### E. Histórico de preço flagship: corte-e-rebote, não rollback

- **FATO** — Anthropic: Opus 4 (mai/2025) $15/$75 → **corte de 67%** no Opus 4.5 (nov/2025) pra $5/$25 → mantido no Opus 4.8 → Fable 5 (jun/2026) **dobra** pra $10/$50, ainda **33% abaixo do pico** do Opus 4. Nem rollback, nem queda monotônica. `[3-0]`
  - Caveat importante: Fable 5 é tier NOVO acima do Opus (que segue a $5/$25) — o "dobrou" é o preço do tier flagship, não repricing da linha.
- **REFUTADO** `[0-3]` — "A OpenAI subiu o preço flagship 4–6x em 2026 (GPT-5.2→5.6)". Não usar.

### F. A "guerra de generosidade" de julho/2026 — existe, mas é ambígua

- **FATO** — Anthropic estendeu a promoção de **+50% nos limites semanais** do Claude Code até 19/07/2026 23:59 PT (Pro, Max, Team, Enterprise legado; automática). Em **20/07**, Fable 5 entra em todos os Max/Team Premium — **porém a 50% dos limites**, coincidindo com o fim da fase de bônus; Pro/Team Standard ficam em créditos + US$ 100 único (**que a $50/M de output esgota rápido — na prática, preço de API**). `[3-0 ×4]`
  - **O mesmo anúncio, dois framings na imprensa:** Simon Willison → "Fable permanente nos planos" (generosidade); The Decoder → "Anthropic slashes Fable 5 limits... pushes Pro users toward API pricing" (rollback).
  - **NÃO confirmado** `[1-2]`: a versão forte do The Decoder de que os limites regulares caem ~33% em 20/07 e o Fable fica a 50% *desses* limites reduzidos (rollback líquido). Fonte única — tratar como alegação de um veículo.
- **FATO (contexto ago/2025)** — O aperto anterior da Anthropic (limites semanais novos no Claude Code, anunciados 28/07/2025) mirava power users extremos (24/7, contas compartilhadas, revenda) — a própria empresa estimou impacto em **<5% dos assinantes** (auto-reportado). Aperto real, porém cirúrgico — e seguido de AUMENTOS de limite em 2026. `[3-0 + 2-1]`

---

## Refutados na verificação — NÃO usar no post

| Claim | Voto |
|---|---|
| Margem de 75% da API da OpenAI em jun/2024 | 0-3 |
| Prejuízo de US$ 5 bi/2024 + US$ 44 bi cumulativos até lucro em 2029 (vintage superado) | 0-3 |
| Anthropic com primeiro lucro operacional (US$ 559 mi) no Q2/2026 e margem 77% em 2028 | 0-3 |
| OpenAI subiu preço flagship 4–6x em 2026 | 0-3 |
| Corte líquido de 33% nos limites + Fable a 50% dos limites reduzidos em 20/07 | 1-2 (plausível, fonte única) |

## Lacunas (pesquisar antes de afirmar no post)

1. **Codex sem limite de 5h + resposta da Anthropic em horas** — o gatilho da tese **não sobreviveu à verificação** (única fonte encontrada era não-confiável). Temos nosso próprio post `codex-limite-de-uso` (13/07) cobrindo isso — re-checar as fontes dele antes de reafirmar.
2. **Pressão chinesa** (Kimi K3 $3/$15, Inkling $1/$4.05) e **Meta–Anthropic US$ 10 bi** — nenhuma claim verificada sobreviveu ao funil; usar como contexto com as fontes de imprensa (CNBC, Axios, Yahoo/NYT) marcadas como não-fact-checked, ou rodar verificação dedicada.
3. **Precedentes históricos** (guerra de preço cloud, Uber/99, streaming) — idem: nada verificado. E há uma assimetria que enfraquece a analogia Uber: aqui o custo unitário subjacente **cai ~3x/ano por eficiência algorítmica** — corrida de Uber nunca ficou 3x mais barata de operar por ano.
4. **Efeito líquido de 20/07 num usuário Max típico** — só observável depois do dia 20. Candidato a atualização do post.

## Qualidade das fontes (ler antes de citar)

- Números financeiros de OpenAI/Anthropic = **documentos vazados/reportados pela The Information** — jornalismo crível sobre dados **não auditados e nunca confirmados oficialmente**.
- Margem de 70% em pagantes **exclui** free tier, treino e P&D.
- Dados Epoch até mar/2025; MIT FutureTech até nov/2025; há sinais de **desaceleração** da queda de preço (estimativas de 3–5x/ano pra 2026–27).
- Métricas de "preço por capacidade" usam benchmarks possivelmente overfitted — não medem utilidade real de trabalho agêntico.

---

# Parte 2 — A terceira ótica: "caros porque correm"

> Tese a testar (levantada pelo Lucas): o custo dos labs de fronteira não está em manter o ecossistema funcionando (servir inferência), está em pesquisa, pessoas e evolução — eles parecem caros/insolventes porque **reinvestem tudo que entra na corrida pela liderança**.

## Veredito da Parte 2

**A tese tem base primária real e os próprios CEOs a defendem — mas o único teste empírico independente dela FALHOU.** A resposta é condicional:

- A operação de servir modelos **é** lucrativa em margem bruta (~48% no "bundle GPT-5"; 70% de margem de computação em pagantes — Parte 1). O rombo vem mesmo de P&D/treino/capex. **Até aqui, a intuição está certa.**
- MAS o reinvestimento **não é discricionário**: modelo de fronteira deprecia em ~4 meses. Parar de treinar = perder o ativo que gera a receita. Logo, o treino do sucessor funciona como **COGS disfarçado**, não como investimento opcional tipo Amazon.
- **A conversão de "prejuízo estrutural" em "investimento escolhido com operação madura lucrativa" depende de UMA variável: a fronteira estabilizar** — e essa condição é colocada pelo próprio Dario Amodei.

## Os achados verificados

### A. A citação-âncora existe — mas é menos do que a lenda diz

- **FATO (a fala) / ILUSTRAÇÃO (os números)** — Dario Amodei, podcast **Cheeky Pint** (John Collison/Stripe, publicado 6–7/ago/2025), verbatim: *"if every model was a company, the model, in this example, is actually profitable"* — o modelo treinado em 2023 por US$ 100 mi gera US$ 200 mi; o prejuízo contábil (-100 mi, -800 mi, -8 bi) vem de cada ano carregar o treino do sucessor 10x maior. **Crucial:** Amodei chama os números de exemplo *"cartoonish"* DUAS vezes e diz *"I don't want to make any specific claims"* — não são financials da Anthropic. `[3-0 ×3, fonte primária]`
- **FATO** — O próprio Amodei condiciona a lucratividade da empresa inteira ao **fim do scaling**: os prejuízos *"keep going up until... the models can't get larger... [or] will stop getting better"*. A defesa mais forte da tese já embute a nuance do veredito. `[3-0]`
  - Ressalva do verificador: ele fala isso em tom otimista; o modelo estilizado não exclui a receita crescer mais rápido que o treino antes disso (projeções vazadas da Anthropic apontariam breakeven ~2028 ainda treinando).
- **NÃO VERIFICADO** — A citação do Altman ("seríamos lucrativos se parássemos de treinar") é atribuída pela Epoch a uma matéria da **Axios de 15/ago/2025**, mas não foi verificada diretamente neste ciclo. **Checar a Axios antes de citar com aspas.**

### B. O teste empírico da tese — e ele deu negativo

- **ESTIMATIVA (alta confiança)** — A **Epoch AI testou a tese** (Sevilla, Petrovic, Ho — 28/jan/2026, "Can AI companies become profitable?") no único caso mensurável: o "bundle GPT-5" como unidade econômica isolada **não foi lucrativo**. A OpenAI gastou mais em P&D nos 4 meses ANTES do GPT-5 (~US$ 5 bi) do que gerou de lucro bruto nos 4 meses de vida do modelo (~US$ 2 bi sobre US$ 6,1 bi de receita) — **~US$ 700 mi no vermelho**. Verbatim: *"we can't take Altman and Amodei at their word."* `[3-0 ×2]`
  - A fonte corta pros dois lados: a mesma Epoch conclui que lucratividade **é** alcançável se os modelos ficarem relevantes por mais tempo que o ciclo GPT-5.

### C. Decomposição de custos da OpenAI (docs vazados — rotular como reportado, não auditado publicamente)

| Rubrica (2025) | Valor | Fonte |
|---|---|---|
| Compute de P&D/treino | US$ 8,3 bi (+ ~US$ 1 bi dados) | Epoch citando The Information `[2-1]` |
| Compute de inferência | ~US$ 8,8 bi (faturas Azure = piso) | TechCrunch, Zitron `[3-0]` |
| Salários de P&D | ~US$ 4,6 bi | Epoch/The Information `[3-0]` |
| P&D total | US$ 7,8 bi (2024) → **US$ 19,2 bi** (2025) | FT/Fortune `[3-0]` |
| Prejuízo líquido 2025 | US$ 38,5 bi — **mas ~US$ 41,5 bi é encargo NON-CASH** da conversão for-profit; prejuízo operacional ~US$ 20,9 bi; queima de caixa ~US$ 8 bi | FT/Fortune `[3-0]` |

**Leitura:** treino e inferência hoje são da **mesma ordem de grandeza** — o prejuízo NÃO vem só do treino, e o headline de US$ 38,5 bi não pode ser lido como queima de caixa. Não existe decomposição equivalente pública para a Anthropic (lacuna).

### D. Por que o reinvestimento é compulsório: depreciação em meses

- **ESTIMATIVA calibrada em medição** — Tenure de fronteira do GPT-5: **~4 meses** (07/ago → 11/dez/2025, encerrada pelo GPT-5.2 após o "code red" do Gemini 3). Gemini 3 Pro superou o GPT-5 base em ~3 meses. Gap fechado→open-weight: **~3–6 meses** (Longpre/MIT + medições da Epoch: 3–4 meses). Concorrentes fecham o gap **sem pré-treinar do zero** (RL, fine-tuning, test-time reasoning — e distilação dos outputs do líder). A Epoch enquadra modelo de fronteira como *"rapidly-depreciating infrastructure"*. `[3-0 ×3]`
  - Ressalva: "vida útil de 4 meses" = tenure de FRONTEIRA, não receita zerando (o GPT-5 faturou US$ 6,1 bi no período). Questão aberta: a monetização de modelos não-fronteira (classe GPT-4o servindo produto barato) alonga a vida econômica real.

### E. A corrida como flywheel autodeclarado

- **FATO** — A OpenAI descreve a própria economia como flywheel deliberado de reinvestimento (*"more compute enables better models... allows us to reinvest in more infrastructure"* — post oficial). Compromisso Stargate: 10 GW até 2029, meta declarada como superada ~abr/2026 (capacidade **operacional** no fim de 2025: ~1,9 GW — "secured" ≠ entregue). Anthropic–Google (23/out/2025): até 1 milhão de TPUs, "dezenas de bilhões", 1+ GW em 2026. `[3-0 ×3]` O número de **~US$ 1,4 tri** em commitments totais da OpenAI **não foi verificado** — não usar sem checagem.
- **FATO (declaração) / ESTIMATIVA (valores)** — Guerra de talento: Altman (podcast Uncapped, ~17/jun/2025) alegou ofertas da Meta de **US$ 100 mi de signing bonus** e comp anual maior; Bosworth (CTO da Meta, all-hands vazado 26/06) rebateu o "signing bonus" mas **não negou** pacotes nessa escala pra um grupo restrito de liderança sênior. `[3-0 ×2]`

### F. O precedente Amazon QUEBRA (cuidado com a analogia no post)

- **FATO (10-K/SEC) + FATO histórico com ressalva** — A analogia "Amazon ficou 20 anos sem lucro reinvestindo tudo" quebra em dois pontos estruturais: `[2-1 ×3]`
  1. A Amazon chegou a ~US$ 638 bi de receita (FY2024) com pouco capital externo (~US$ 8 mi de VC + US$ 54 mi de IPO + ~US$ 2,2 bi em bonds) — reinvestimento **autofinanciado por caixa operacional**. Os labs queimam **capital externo** (SoftBank ~US$ 40 bi na OpenAI; Series F de US$ 13 bi na Anthropic).
  2. O ativo da Amazon ganhou vida útil contábil MAIS LONGA com o tempo (servidores: 3 anos em 2020 → 6 anos em 2024; recuo pra 5 em 2025 *"due to... AI"*). O ativo dos labs deprecia em **meses**.
  - Ressalva: "exatamente oposto" é exagero — é o mesmo modelo em escala ~100x menor; a Amazon também dependeu de capital externo em 1997–2001.

## Refutados na Parte 2 — NÃO usar no post

| Claim | Voto |
|---|---|
| ~US$ 30 bi do prejuízo de 2025 seria encargo único da reestruturação (usar os números do FT acima) | 0-3 |
| "A inferência sozinha supera a receita da OpenAI" | 1-2 |
| "O treino é majoritariamente non-cash via créditos Microsoft" | 0-3 |
| "GLM-5 igualou o Opus 4.6 em 1 semana" (liderança durando semanas) | 1-2 |
| "Amazon se financiou principalmente com capital de giro negativo" | 1-2 |

## Questões abertas da Parte 2

1. Citação exata do Altman na Axios (15/ago/2025) — verificar antes de citar.
2. Decomposição treino vs. inferência da **Anthropic** — sem números públicos; o lado Anthropic ficou coberto só por TPUs e pelo framing do Amodei.
3. Como labs/financiadores contabilizam a **depreciação do "ativo modelo"** — e quanto a cauda de monetização de modelos não-fronteira alonga a vida econômica real.
4. O ~US$ 1,4 tri de commitments da OpenAI se confirma? Quanto é obrigação firme vs. opcionalidade cancelável?

---

## O ângulo do post (proposta)

**Tese editorial (agora com as 3 óticas):** "Os dois lados estão certos — e é por isso que os dois estão errados." O pessimista olha a conta agregada (margem caindo, prejuízo projetado bilionário); o otimista olha o preço unitário (despencando estruturalmente). O que nenhum dos dois conta: **a segmentação** (Max/enterprise vê generosidade porque a margem de 70% do pagante banca; free/Pro sente rollback porque é onde a queima está sendo estancada) e **a natureza do prejuízo** (a operação de servir dá margem bruta positiva; o rombo é a corrida — e a corrida não é opcional, porque o modelo deprecia em ~4 meses). O arco narrativo perfeito: abre com o dia 20/07 (mesmo anúncio, manchetes opostas), fecha com a pergunta do Amodei — tudo depende de quando a fronteira estabiliza.

**Títulos candidatos (fórmula CTR):**
1. "O 'grande rollback' da IA vai acontecer? Fui atrás dos números — e os dois lados estão errados"
2. "Margem de 70% ou prejuízo de US$ 74 bi? As duas contas da OpenAI explicadas"
3. "Preço por token caiu 83%, sua conta subiu: a matemática que explica a 'guerra de generosidade'"
4. "Cada modelo dá lucro, a empresa dá prejuízo: a conta que o Dario Amodei fez (e a Epoch refez)"
5. "OpenAI e Anthropic são a nova Amazon? A analogia quebra em 2 pontos (e um deles é fatal)"

**Keyword-alvo sugerida (validar na planejar-pauta):** "custo de inferência llm" / "preço por token ia" / "grande rollback ia" — cauda-longa, e o post encaixa link interno em `codex-limite-de-uso`, `fable-5-voltou` e `anthropic-ipo`.

## Fontes principais

**Parte 1:**
- **Primárias:** Epoch AI (price trends) · arXiv 2511.23455v2 (MIT FutureTech) · @claudeai no X (anúncio 20/07) · pricing first-party OpenAI/Anthropic
- **Secundárias fortes:** The Information (docs financeiros; via agregadores) · TechCrunch · Forbes (Paulo Carvão, 21/05/2026) · the-decoder · helpnetsecurity · simonwillison.net
- **Steel-man rollback:** Ed Zitron — wheresyoured.at ("Subprime AI Crisis") · blog.dshr.org ("AI's Affordability Crisis")
- **Contexto (não fact-checked):** CNBC/Axios (Kimi K3) · Yahoo Finance/NYT (Meta–Anthropic) · a16z LLMflation · SaaStr · Sean Goedecke

**Parte 2:**
- **Primárias:** cheekypint.substack.com (transcript Amodei, ago/2025) · epoch.ai/gradient-updates/can-ai-companies-become-profitable (28/jan/2026) · openai.com (post Stargate/flywheel) · anthropic.com (acordo TPUs Google) · 10-K da Amazon via SEC EDGAR
- **Secundárias fortes:** FT/Fortune (financials vazados 2025, 16/jun/2026) · TechCrunch (faturas Azure; talent war) · CNBC (Altman/Meta; Anthropic-Google) · Fast Company (depreciação, 18/fev/2026)
- **Mid-tier (números cruzados com SEC/FT, interpretações são dos autores):** Prof G Media · Motley Fool · SiliconAngle
