# X/Twitter via Grok (handoff manual)

No passo 2 da skill: preencha o template abaixo ({HORAS}/{FOCO}/{DATA_ISO}) e **mostre pro usuário copiar e colar no chat do Grok**. Quando ele devolver, trate cada item como candidato adicional → qualificação (passo 3).

O app do Grok tem X Search nativo (`x_keyword_search`/`x_semantic_search`), então o template força essas tools. Se o X estiver fora do ar (timeout), é best-effort — siga com HN/Reddit/News.

## Template (preencher {HORAS}/{FOCO}/{DATA_ISO})

```
Use suas ferramentas NATIVAS de X: x_keyword_search e x_semantic_search.
Janela: últimas {HORAS}h (use since:{DATA_ISO}). Foco: {FOCO}.
Faça buscas simples e separadas (um termo por vez: "GPT-5.6", "Claude Fable", "Gemini",
"OpenAI", "coding agent"...) com min_faves entre 20 e 100 para pegar só o que tem tração.
Se uma busca der timeout, tente de novo 1x com query mais curta; se persistir, pule esse termo.
NÃO rode scripts locais nem a skill cacar-news-jacking/detect.sh — quero só o sinal do X.

Me liste os 8–12 assuntos de IA que estão BOMBANDO no X agora, priorizando:
- lançamentos/rumores de modelo (datas, specs, preços vazados);
- dramas/conflitos (bloqueios, bans, processos, polêmicas de empresa);
- benchmarks novos e brigas de "X vs Y";
- posts de pesquisadores/labs com muito engajamento.

Para CADA assunto devolva, em uma linha:
- TÍTULO curto do assunto
- por que está em alta (1 frase)
- a conta/post de origem mais relevante (@handle ou link)
- quão recente (hoje / ontem / X horas)
- está só no X ou já virou notícia em portal?

Ordene do mais quente pro menos quente. Sem enrolação, só a lista.
```

## Ao receber a resposta

- Deduplique contra o que o `detect.sh` já trouxe (mesmo assunto em HN/Reddit/News).
- Itens "só no X, ainda não virou notícia" = **janela mais aberta** → bônus de velocidade na pontuação.
- Itens que já viraram portal = janela fechando → marque.
