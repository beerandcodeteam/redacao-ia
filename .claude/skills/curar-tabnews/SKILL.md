---
name: curar-tabnews
description: Curadoria de posts do TabNews para comentar agora (Fase 0 da estratégia TabNews). Busca posts recentes na API pública, filtra pelos temas de autoridade da Beer And Code (IA aplicada, agentes, RAG, LLMs, Claude/Codex, Laravel/PHP, carreira dev), pontua por frescor/tração/encaixe e devolve 3-5 candidatos ranqueados com ângulo de comentário sugerido. Acionar quando o usuário pedir "curar tabnews", "quais posts comentar", "achar post pra comentar", "/curar-tabnews" ou equivalente.
---

# Curadoria TabNews — em qual post comentar agora

Objetivo: em vez de o Lucas garimpar o feed, entregar os 3-5 melhores alvos de
comentário do momento, com ângulo sugerido. Contexto da estratégia:
`tabnews/README.md` (Fase 0 = 2-3 comentários/dia com substância).

## Passo 1 — Coletar candidatos (API pública, sem auth)

Buscar duas estratégias e juntar (dedup por `owner_username/slug`):

```bash
curl -s "https://www.tabnews.com.br/api/v1/contents?strategy=new&per_page=30&page=1"
curl -s "https://www.tabnews.com.br/api/v1/contents?strategy=relevant&per_page=30&page=1"
```

Campos que importam: `title`, `owner_username`, `slug`, `published_at`,
`tabcoins`, `children_deep_count` (nº de comentários na thread).

## Passo 2 — Filtrar

Excluir:

- Posts com mais de **36h** (leitor ativo já foi embora).
- `tabcoins < 0` (thread queimada).
- Autor `NewsletterOficial` só entra se o tema for MUITO nosso (é bot — comentar
  lá dá visibilidade mas não constrói relação; despriorizar, não proibir).
- Posts já comentados: conferir `tabnews/data.js` (array `comentarios`) e as
  pastas em `respostas-tabnews/`.
- Pitch de projeto sem relação com nossos temas.

## Passo 3 — Pontuar (0-10)

- **Encaixe de tema (peso 4):** agentes de IA, RAG, evals, harness, LLMs em
  produção, Claude/Codex/modelos open source, IA local, Laravel/PHP, carreira
  dev/IA. Fora disso, corta.
- **Frescor (peso 3):** <6h = nota cheia; decai até 36h.
- **Conversa viva (peso 2):** 1-8 comentários = ideal (tem gente lendo e ainda
  dá pra se destacar). 0 = ok se fresco. >15 = comentário se perde.
- **Potencial de autoridade (peso 1):** dá pra agregar experiência própria de
  produção? Pergunta aberta que a gente sabe responder? Opinião polêmica que
  merece contraponto educado?

## Passo 4 — Entregar

Para cada um dos top 3-5, mostrar:

1. Título + link (`https://www.tabnews.com.br/{owner_username}/{slug}`)
2. Idade, tabcoins, nº de comentários
3. **Ângulo sugerido** (1-2 frases): o que o comentário agregaria — experiência
   própria, dado, correção educada, pergunta boa. Nunca "ótimo post".

Se o usuário escolher um, buscar o corpo para ler antes de escrever:

```bash
curl -s "https://www.tabnews.com.br/api/v1/contents/{owner_username}/{slug}"
```

## Passo 5 — Depois que o comentário for feito

1. Criar pasta `respostas-tabnews/AAAA-MM-DD-slug/` com `post-original.txt`
   (corpo do post) e `resposta.txt` (comentário publicado).
2. Adicionar entrada no array `comentarios` de `tabnews/data.js`.
3. Lembrar o usuário de voltar em algumas horas pra responder réplicas.

## Regras de tom (herdam da Fase 0)

- Comentário precisa agregar: experiência real, dado, contraponto, pergunta boa.
- Sem link pro blog em comentário de Fase 0, salvo se genuinamente essencial.
- Sem pitch de Clã/evento. Sem emoji em excesso. Tom sóbrio da casa.
