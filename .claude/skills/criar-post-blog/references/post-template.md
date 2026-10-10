# Template de post — Beer & Code

Use como esqueleto. Adapte se o tema pedir, mas mantenha as âncoras: gancho, TL;DR, contexto, mão na massa, limitações, FAQ, conclusão.

> **CTA não é seção.** Quando houver destino de CTA (evento, Clã, repositório, newsletter), ele entra **embutido** em 1–2 frases dentro do corpo — **no primeiro terço do post (~30% da leitura)**, tipicamente fechando a seção de contexto, no trecho que conversa diretamente com o destino; conclusão só como fallback. Sem heading dedicado tipo `## CTA`, `## Entra no Clã` ou `## Inscreva-se`. Sem caixa, sem `---` ao redor. Tom de convite curto, link inline em `[nome do destino](url)`. Detalhes de tom em `references/brand-voice.md`.

---

## Título

Prático ou de impacto. Dois padrões que funcionam:

- `Como usar [Ferramenta] para [Resultado concreto]`
- `O que o [Modelo/Feature] muda no [Setor/Tipo de stack]`

Sem clickbait. Se o título promete X, o post entrega X.

## Introdução (100–150 palavras)

Três parágrafos curtos:

1. **Gancho** — problema real do dev ou impacto da atualização. Não comece com "Você sabia que...".
2. **Solução** — o que é a ferramenta/modelo e o que ela resolve.
3. **O que vai aprender/construir** — expectativa clara do resultado. Ex: "Neste tutorial vamos construir um agente que faz X usando Y."

## TL;DR (resumo rápido)

Bullets, formato fixo:

- **O que é:** [1 linha]
- **Stack/Modelos:** [ex: Python, OpenAI API, LangChain]
- **Custo/Acesso:** [ex: gratuito, open-source, requer chave paga]
- **Repositório/Link útil:** [link direto]

## H2: O contexto — por que [tecnologia/modelo] importa? (200–300 palavras)

Parte de notícia/análise.

- Como era feito antes vs. como muda agora.
- Benchmarks com número e fonte (`O modelo X é 20% mais rápido que Y no teste Z [fonte](url)`).
- `[CITAÇÃO/Link para paper ou anúncio oficial]`
- `[IMAGEM: gráfico de benchmark ou esquema de arquitetura]` (sugestão para a capa secundária ou para inserir no corpo)
- **CTA embutido entra AQUI (se houver destino nos inputs)** — este é o ponto ~30% do post. 1–2 frases fechando a seção, ligando o tema ao destino, link inline. Sem heading, sem caixa. Formato em `references/brand-voice.md` → "Tom comercial (CTA)".

## H2: Pré-requisitos e ferramentas (100–150 palavras)

Checklist do que o leitor precisa antes de começar:

- [ ] Chave de API da [Empresa]
- [ ] Conhecimento básico em [Linguagem/Conceito]
- [ ] Ambiente: [ex: Node 18+, PHP 8.3, Python 3.11]

Inclua link interno para tutorial de setup se aplicável.

## H2: Mão na massa — passo a passo (400–600 palavras)

O coração do post.

### Passo 1: [ação clara]

Explicação curta. Bloco de código ou prompt exato. Print do terminal se ajudar.

```lang
// código aqui
```

### Passo 2: [ação clara]

Dica de ouro: boas práticas de engenharia de prompt ou otimização. Bloco de código.

### Passo 3: [ação clara]

Erros comuns (compilação, alucinação, rate limit) e como sair deles.

## H2: Limitações e pontos de atenção (150–200 palavras)

Onde falha. Onde o leitor vai se queimar se não souber.

- Limitações técnicas reais (ex: limite de contexto, problemas com matemática complexa, alucinação em domínio X).
- Privacidade/segurança (ex: "não jogue dados de cliente nesse prompt sem mascarar").

Esse bloco gera credibilidade. Não pule.

## H2: FAQ rápido (3–4 perguntas)

Foco em dor técnica e dúvida real:

- "Por que recebi erro 429 (rate limit)?"
- "Posso usar comercialmente?"
- "Funciona local ou só na cloud?"

Respostas diretas, 40–60 palavras cada. Link interno para doc oficial ou outro post de aprofundamento.

## Conclusão (100 palavras)

- Resumo do que foi construído/analisado.
- Provocação sobre o futuro: "O próximo passo dessa tecnologia será...".
- Link interno para artigo relacionado: "Agora que você aprendeu X, veja como Y".
- **CTA aqui só como fallback** — o CTA vive no ponto ~30% (fim da seção de contexto). Use a conclusão apenas se não houve encaixe natural antes; nunca os dois (um link de destino por post). Mesmas regras: 1–2 frases na prosa, sem heading, sem caixa, sem `---`. Veja `references/brand-voice.md` → "Tom comercial (CTA)".

---

## Bloco de marcadores que você vai substituir

- `[CITAÇÃO/Link para paper ou anúncio oficial]` — sempre com URL real.
- `[IMAGEM: descrição]` — descreve o que vai ali; não deixa sem.
- `[BLOCO DE CÓDIGO/PROMPT EXATO]` — código que roda, não pseudo-código.
- `[LINK INTERNO → ...]` — links para outros posts do blog (`https://blog.beerandcode.com.br/...`).
