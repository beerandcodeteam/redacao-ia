# Template de saída — Radar + Pauta

Duas camadas. Mostre as duas no chat. Se o usuário pedir pra salvar, grave **só a camada 2** em `pautas/<mês>/semana-N.md` (a tabela de radar é raciocínio, não pauta).

## Camada 1 — Radar (chat)

Tabela de todos os candidatos detectados:

| # | Tema | Fonte(s) | Velocidade | Vol BR / KD | Janela | Veredito |
|---|------|----------|-----------|-------------|--------|----------|
| 1 | ... | HN+Reddit+X | 🔥 subindo | ~0 / KD 8 | aberta | surfar agora |
| 2 | ... | OpenRouter diff | 🆕 modelo novo | n/a | aberta | surfar agora |
| 3 | ... | News | morno | 1.300 / KD 40 | fechando | evergreen → planejar-pauta |

**Vereditos:** `surfar agora` · `surfar se acelerar` (re-checar em 24–48h) · `atualizar post existente` (canibalização) · `evergreen → planejar-pauta` · `descartar`.

Feche com:
- **Top 3 "surfar agora"** — os de maior velocidade + janela aberta + viabilidade.
- **Atualizações de posts existentes** que apareceram (se houver) — com o slug do post a reforçar.

## Camada 2 — Pauta dos aprovados (formato de campos)

Só os `surfar agora`, no formato fixo da `planejar-pauta`:

```
## <Título com gancho de CTR — número/comparação/drama>
- publicar_em: <ISO 8601 -03:00; 09:00 BRT default; mesmo dia escalona a hora>
- autor: lucas-souza-virgu
- categoria: <noticias | tutoriais | pacotes — conceitual/notícia → noticias>
- resumo: <2–4 linhas: o que entrega + o gatilho de news-jacking + se é formato vivo/atualizável>
- hook: <1–2 frases no tom da marca, com a tensão da notícia>
- bullets:
  - <5 H2 / promessas>
- keyword_principal: <termo de cauda-longa que você chega primeiro>
- keywords_secundarias: <3–5 variações reais>
- tags: <reutilizáveis; confirmar com ListTags no criar-post-blog>
- dificuldade: <easy | medium | hard>
- volume: <vol BR + KD + por que vale apesar do volume (ex.: "~0 BR, KD 8, janela de lançamento")>
```

## Regras de ouro (não furar)

1. **Marcar VERIFICADO vs RUMOR** no resumo de qualquer tema especulativo (lançamento não confirmado). Queimar credibilidade mata o canal.
2. **Título com gancho de CTR** sempre (ver fórmula na SKILL.md). Sem gancho → não entra na camada 2.
3. **Se já existe post no tema**, é `atualizar existente`, não pauta nova.
4. **Volume ~0 não reprova** tema de news-jacking — velocidade + KD baixo + janela aberta decidem.
