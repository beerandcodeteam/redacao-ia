# Template do relatório de pauta

Saída em duas camadas. Tom: direto, número na frente, sem encher linguiça. Mesmo espírito da `criar-post-blog`.

---

## Camada 1 — Triagem (no chat)

## Relatório de pauta — <data> (janela: <período>)

**Objetivo do ciclo:** <quick wins | autoridade | volume | equilíbrio (default)>
**Temas analisados:** <n> · **Aprovados:** <m>

### Priorização

| # | Tema | Keyword-alvo | Vol/mês | KD | Intenção | Quick win? | Score | Veredito |
|---|------|--------------|--------:|---:|----------|:----------:|------:|----------|
| 1 | ... | `...` | 1.300 | 22 | Info | ✅ pos.8 | 87 | escrever agora |
| 2 | ... | `...` | 480 | 35 | Info | — | 64 | escrever depois |
| 3 | ... | `...` | 90 | 70 | Trans | — | 18 | descartar |

Vereditos: `escrever agora` · `escrever depois` · `otimizar post existente` · `reposicionar` · `descartar`.

### Comece por estes (top 3)

1. **<tema>** — <1 frase: por que é o primeiro> (keyword `...`, vol X, KD Y, quick win em pos. Z).
2. ...
3. ...

### Otimizações de posts existentes (se houver)

- `<slug>` — está em pos. <X> para `<keyword>`; falta <profundidade / keyword no title / FAQ / atualizar>.

---

## Camada 2 — Pauta dos aprovados (formato de campos)

Um bloco por tema aprovado, na ordem de produção. Este é o formato que vai para `pautas/<mês>/semana-N.md`.

```
## <Título do post>
- publicar_em: <ISO 8601 com -03:00; 09:00 BRT default; posts no mesmo dia escalonam a hora, ex.: 09:00, 11:00>
- autor: <slug, ex.: lucas>
- categoria: <uma das reais (ListCategories): conceitual/explicativo → Notícias; mão-na-massa/código → Tutoriais; pacote Laravel → Pacotes>
- resumo: <2–4 linhas: o que entrega + o diferencial contra a SERP>
- hook: <1–2 frases no tom da marca>
- bullets:
  - <H2 / promessa 1>
  - <H2 / promessa 2>
  - <H2 / promessa 3>
  - <H2 / promessa 4>
  - <H2 / promessa 5 — onde entra código / exemplo prático>
- perguntas_paa:
  - <pergunta literal 1 do bloco people_also_ask da SERP>
  - <pergunta literal 2>
  - <pergunta literal 3>
- keyword_principal: <keyword-alvo>
- keywords_secundarias: <2–4 variações / long-tail / pergunta da SERP>
- tags: <tags reutilizáveis (ListTags antes de criar tag nova)>
- dificuldade: <easy | medium | hard>
- volume: <vol/mês + KD + tendência, ex.: ~1.300/mo (KD 23, +60%/ano)>
```

### Regras dos campos

- **publicar_em:** ISO 8601 com offset `-03:00`. Para 09:00 BRT, enviar `T09:00:00-03:00`. Dois posts no mesmo dia → escalonar a hora.
- **categoria / autor / tags:** valores reais do blog. Confirme `categoria` com ListCategories e reaproveite tags com ListTags em vez de inventar.
- **bullets:** 5 itens, cada um vira um H2 ou uma promessa do post; o último costuma ser o exemplo prático/código.
- **perguntas_paa:** 3–5 perguntas **copiadas literalmente** dos `title` do bloco `people_also_ask` da SERP (passo 2c) — são elas que viram H2/FAQ do post. Sem inventar nem reescrever; se a SERP não trouxe bloco PAA, escreva `perguntas_paa: —` em vez de omitir o campo.
- **volume:** sempre com o número na frente (vol/mês, KD, tendência). Se o tema entrou mesmo sem volume (aposta de autoridade), diga isso explicitamente no campo.
- Só entram aqui os temas com veredito `escrever agora` / `escrever depois`. `descartar` / `reposicionar` ficam só na triagem (camada 1), com o porquê.
