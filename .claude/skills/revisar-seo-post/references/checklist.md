# Formato do relatório de revisão de SEO

Compacto, número/regra na frente, uma linha por item. Só detalhe o que não passou.

```
## Revisão SEO — <title do post>
keyword-alvo: `<keyword_principal>`  ·  modo: <batch|interativo>

### Camada 1 — Trava MCP
- ✅ em-dash em meta_description: ausente
- ⚠️ meta_description: 172 chars → cortado para 148
- ✅ símbolos Unicode em title/slug: nenhum

### Camada 2 — SEO on-page
- ✅ keyword no title / 1º parágrafo / H2 / slug
- ✅ abertura citável: 1ª frase responde a keyword sozinha
- ❌ cobertura de PAA: 1 de 4 `perguntas_paa` vira H2 (aviso; mexer em H2 não é correção segura) · sem o campo → `(não verificado)`
- ⚠️ meta_title: 71 chars → reescrito para 58
- ⚠️ link interno: nenhum → adicionado link para `o-que-e-um-agente-de-ia`
- ❌ profundidade: ~520 palavras contra SERP densa (aviso; não bloqueante em batch)
- ✅ intenção informational · sem canibalização (ListPosts)

### Correções aplicadas (campos finais p/ CreatePost)
- meta_description: "<texto final ≤155 chars, sem em-dash>"
- meta_title: "<texto final ≤60 chars>"
- slug: <mantido | novo>
- body: <inalterado | +1 link interno no parágrafo de conclusão>

### Veredito
PUBLICAR  — travas ok, correções seguras aplicadas. 2 avisos registrados (profundidade, PAA).
```

## Convenções

- **✅** ok, nada a fazer. **⚠️** corrigível, mostre `antes → depois`. **❌** problema sério; em batch vira aviso não-bloqueante, em interativo segura até decisão.
- Não liste em prosa o que está ✅ — uma linha basta. Gaste tinta só no que mudou.
- O veredito é sempre a última linha: `PUBLICAR` ou `SEGURAR`.
- Se um check não pôde ser verificado (ex.: MCP fora → sem `ListPosts`), marque `· (não verificado)` em vez de ✅.
