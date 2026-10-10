# Template de saída — Radar + Pauta (evergreen)

Duas camadas. Mostre as duas no chat. Se o usuário pedir pra salvar, grave **só a camada 2** em `pautas/<mês>/semana-N.md` (a tabela de radar é raciocínio, não pauta).

## Camada 1 — Radar (chat)

Tabela de todos os candidatos minerados:

| # | Tema | Fonte | Vol BR / KD | Durabilidade (curva 12m) | SERP | Veredito |
|---|------|-------|-------------|--------------------------|------|----------|
| 1 | O que é RAG | seed+gap | 1.300 / KD 22 | 📈 subindo | rasa | escrever agora |
| 2 | Eager loading Laravel | striking-distance | 480 / KD 18 | ➡️ plana | ganhável | escrever agora |
| 3 | X (nome de modelo) | seed | 900 / KD 12 | 📉 pico único | — | pico → news-jacking |

**Vereditos:** `escrever agora` · `escrever depois` · `atualizar post existente` (canibalização/decay) · `pico → news-jacking` (curva de hype, não evergreen) · `descartar` (vol ~0 / intenção errada / SERP impenetrável).

**Curva:** 📈 subindo · ➡️ plana · 🔁 sazonal (marcar época) · 📉 pico-e-morte (não é evergreen).

Feche com:
- **Top 3 "escrever agora"** — maior durabilidade × volume × viabilidade (KD/SERP).
- **Atualizações de posts existentes** que apareceram — com o slug e se é canibalização ou decay.
- **Oportunidade de cluster** (se houver) — candidatos que juntos formam um hub-and-spoke.

## Camada 2 — Pauta dos aprovados (formato de campos)

Só os `escrever agora`, no formato fixo da `planejar-pauta`:

```
## <Título que casa a intenção informacional — "O que é X", "Como fazer Y", "X vs Y">
- publicar_em: <ISO 8601 -03:00; 09:00 BRT default; mesmo dia escalona a hora>
- autor: lucas-souza-virgu
- categoria: <noticias | tutoriais | pacotes — conceitual → noticias; mão-na-massa/código → tutoriais>
- resumo: <2–4 linhas: o que entrega + por que é durável + se ancora um cluster>
- hook: <1–2 frases no tom da marca>
- bullets:
  - <5 H2 / promessas — priorize as perguntas reais vindas do endpoint keyword_suggestions>
- keyword_principal: <keyword-alvo com demanda estável comprovada>
- keywords_secundarias: <3–5 variações / perguntas reais>
- tags: <reutilizáveis; confirmar com ListTags no criar-post-blog>
- dificuldade: <easy | medium | hard>
- volume: <vol BR + KD + tendência da curva 12m, ex.: "~1.300/mo, KD 22, +52%/ano">
```

## Regras de ouro (não furar)

1. **Gate de durabilidade é trava.** Sem curva de `monthly_searches` (12 meses) plana/subindo, não entra na camada 2 — vira `descartar` ou `pico → news-jacking`. Sem `search_volume_trend.yearly`, aplique o fallback 3m recentes × 3m antigos do passo 2 — nunca trate a ausência como 0. Google Trends é confirmação **opcional**, só quando a curva de 12 meses ficou ambígua.
2. **Volume ~0 reprova** (invertido vs news-jacking): sem demanda estável não é evergreen.
3. **Título casa intenção informacional** — o "explicativo" aqui é o formato certo, não clickbait de drama.
4. **Se já existe post no tema**, é `atualizar existente` (canibalização ou decay), não pauta nova.
5. **Ignorar ruído do baseline**: queries de marca e o falso quick win `quanto-ganha-engenheiro-de-ia` ficam de fora (memória `feedback_seo_falsos_quick_wins`).
