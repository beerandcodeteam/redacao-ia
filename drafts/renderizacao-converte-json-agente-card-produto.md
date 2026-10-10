O agente devolve um JSON impecável. Foto, preço, delta, link, resumo de review. Tudo estruturado, validado, pronto.

Aí o front renderiza ` ```json ... ``` ` na tela.

Conversão: zero.

Esse é o pedaço que todo tutorial de tool use, agente e RAG esquece. O backend cumpriu a parte dele — o usuário, não. Ele queria clicar num card, não ler um objeto. Neste post a gente conecta as pontas: pegar a saída estruturada do agente e transformar em UI que converte. Card com foto, preço atual, delta de preço (verde/vermelho), link de checkout e resumo de review. Stack moderna: Claude com [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) ou OpenAI, renderizando via [Vercel AI SDK](https://ai-sdk.dev/docs/ai-sdk-ui/generative-user-interfaces) ou [LangGraph](https://docs.langchain.com/langsmith/generative-ui-react).

## TL;DR

- **O que é:** padrão para mapear tool output estruturado de um agente em componente React renderizado em tempo de resposta.
- **Stack/Modelos:** Next.js + Vercel AI SDK 5, Claude Sonnet 4.6 ou Opus 4.7 com `output_config.format`, Zod no schema.
- **Custo/Acesso:** API paga do modelo (Claude/OpenAI). AI SDK e LangGraph open-source.
- **Repositório/Link útil:** [vercel/ai no GitHub](https://github.com/vercel/ai) e [langchain-ai/langgraphjs-gen-ui-examples](https://github.com/langchain-ai/langgraphjs-gen-ui-examples).

## O contexto — por que o agente "só texto" virou commodity

Em fevereiro de 2026, structured outputs ficou [GA na Claude Developer Platform](https://claude.com/blog/structured-outputs-on-the-claude-developer-platform), suportando Sonnet 4.5+, Opus 4.5+ e Haiku 4.5. A OpenAI já tinha lançado o equivalente antes, com GPT-4o atingindo 100% de aderência ao schema em avaliação interna ([fonte](https://openai.com/index/introducing-structured-outputs-in-the-api/)).

O que isso muda na prática? O modelo deixa de "tentar" devolver JSON. A geração é restringida em tempo de inferência por uma grammar derivada do seu schema. A própria doc da Anthropic é direta:

> "Structured outputs guarantee schema-compliant responses through constrained decoding: Always valid. No more `JSON.parse()` errors."

Beleza. Você tem JSON garantido. E daí?

E daí que o seu produto continua mostrando texto. O agente recomenda três tênis com base no histórico do usuário, devolve um array tipado com nome, preço, delta, foto e link, e o front renderiza isso como uma lista chata de bullet points. O ganho técnico não vira ganho de produto.

A peça que fecha o ciclo é **generative UI**: amarrar o tool call do agente a um componente React. O [Vercel AI SDK 3.0 trouxe esse padrão pro mainstream](https://vercel.com/blog/ai-sdk-3-generative-ui), e em janeiro de 2026 a Vercel ainda [open-sourceou o json-render](https://www.infoq.com/news/2026/03/vercel-json-render/) — um framework Apache 2.0 onde você define um catálogo de componentes em Zod e o LLM gera um spec JSON restrito a esse catálogo. LangGraph foi pelo mesmo caminho com `push_ui_message()` e `LoadExternalComponent`.

Em todos os casos a ideia é a mesma: o JSON do agente não é resposta final. É instrução de renderização.

## Pré-requisitos e ferramentas

Antes de codar:

- [ ] API key da Claude ou OpenAI (qualquer modelo com structured outputs)
- [ ] Next.js 15+ ou React 19 com Vercel AI SDK 5
- [ ] Conhecimento básico de tool use / function calling
- [ ] Catálogo de produtos exposto via API interna (preço, estoque, foto)
- [ ] Tailwind ou seu sistema de design pronto — você não vai estilizar do zero no calor da entrega

Se você nunca configurou tool use com Claude, vale dar uma passada pela [doc oficial](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) antes — a sintaxe migrou de `output_format` (beta) para `output_config.format` e quebra exemplos antigos.

## Mão na massa — do JSON ao card clicável

A receita tem cinco passos. O exemplo é uma loja que recomenda produtos via agente.

### Passo 1: defina o schema do que o agente devolve

Sem schema, sem garantia. O Zod resolve os dois lados — input do tool e tipo do componente React.

```ts
// schemas/product-card.ts
import { z } from 'zod';

export const productCardSchema = z.object({
  sku: z.string(),
  name: z.string(),
  imageUrl: z.string().url(),
  currentPrice: z.number().positive(),
  previousPrice: z.number().positive().nullable(),
  reviewSummary: z.string().max(220),
  reviewScore: z.number().min(0).max(5),
  checkoutUrl: z.string().url(),
});

export const recommendOutputSchema = z.object({
  products: z.array(productCardSchema).min(1).max(4),
  reasoning: z.string().max(280),
});

export type ProductCard = z.infer<typeof productCardSchema>;
```

Repare em três detalhes que evitam dor depois:

1. `imageUrl` e `checkoutUrl` validados como URL — corta meia dúzia de alucinações que o modelo ainda solta de vez em quando.
2. `previousPrice` é `nullable`, não opcional — o agente é obrigado a se posicionar (tem ou não tem preço anterior).
3. `min(1).max(4)` no array — usuário não quer 12 cards. Quer uma decisão.

### Passo 2: execute a tool dentro do agente

Aqui o agente decide chamar a tool quando o usuário pede recomendação. O AI SDK 5 já fala a língua do Zod nativamente:

```ts
// app/api/chat/route.ts
import { streamText, tool } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { recommendOutputSchema } from '@/schemas/product-card';
import { findProducts } from '@/lib/catalog';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const recommendProducts = tool({
    description: 'Recomenda até 4 produtos com card pronto pra renderizar.',
    inputSchema: z.object({
      intent: z.string().describe('O que o usuário está procurando.'),
      budgetMax: z.number().nullable(),
    }),
    execute: async ({ intent, budgetMax }) => {
      const products = await findProducts({ intent, budgetMax });
      return recommendOutputSchema.parse({
        products,
        reasoning: `Selecionei com base em: ${intent}`,
      });
    },
  });

  return streamText({
    model: anthropic('claude-sonnet-4-6'),
    messages,
    tools: { recommendProducts },
  }).toDataStreamResponse();
}
```

Detalhe importante: a tool **não confia no LLM para inventar produto**. Ela busca no catálogo real (`findProducts`) e devolve os dados verificados. O modelo escolhe quando chamar e com qual intenção. O preço, foto e link vêm do seu banco. Esse é o ponto que separa demo de produção.

### Passo 3: mapeie o tool call em um componente React

No client, cada parte da mensagem tem um tipo. Tool calls aparecem como `tool-${nome}` com estados bem definidos:

```tsx
// components/chat-messages.tsx
import { ProductCardGrid } from './product-card-grid';
import { ProductCardSkeleton } from './product-card-skeleton';

{message.parts.map((part, index) => {
  if (part.type === 'tool-recommendProducts') {
    switch (part.state) {
      case 'input-available':
        return <ProductCardSkeleton key={index} count={3} />;
      case 'output-available':
        return <ProductCardGrid key={index} {...part.output} />;
      case 'output-error':
        return (
          <p key={index} className="text-sm text-red-500">
            Não rolou recomendar agora. Tenta de novo.
          </p>
        );
    }
  }

  if (part.type === 'text') {
    return <p key={index}>{part.text}</p>;
  }
})}
```

Três estados, três UIs. `input-available` significa que o agente decidiu chamar a tool e tá rodando — você mostra skeleton. `output-available` é o JSON validado chegando. `output-error` é a sua chance de não deixar a UI quebrar.

### Passo 4: o card em si — composição que converte

Card de produto não é card de blog post. Tem hierarquia visual rígida: foto domina, preço dá nó na cabeça, delta empurra a decisão.

```tsx
// components/product-card.tsx
import Image from 'next/image';
import type { ProductCard } from '@/schemas/product-card';

export function ProductCardItem({ product }: { product: ProductCard }) {
  const delta = product.previousPrice
    ? product.currentPrice - product.previousPrice
    : null;

  const deltaPct = delta && product.previousPrice
    ? Math.round((delta / product.previousPrice) * 100)
    : null;

  return (
    <a
      href={product.checkoutUrl}
      className="group block rounded-xl border border-zinc-200 bg-white p-3 transition hover:shadow-lg dark:border-zinc-800 dark:bg-zinc-900"
    >
      <div className="relative aspect-square overflow-hidden rounded-lg bg-zinc-100">
        <Image
          src={product.imageUrl}
          alt={product.name}
          fill
          sizes="(max-width: 640px) 50vw, 240px"
          className="object-cover transition group-hover:scale-105"
          onError={(e) => {
            (e.target as HTMLImageElement).src = '/img/product-fallback.png';
          }}
        />
      </div>

      <h3 className="mt-3 line-clamp-2 text-sm font-medium">{product.name}</h3>

      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-lg font-semibold">
          {formatBRL(product.currentPrice)}
        </span>
        {product.previousPrice && (
          <span className="text-xs text-zinc-500 line-through">
            {formatBRL(product.previousPrice)}
          </span>
        )}
        {deltaPct !== null && deltaPct < 0 && (
          <span className="rounded-full bg-emerald-500/15 px-2 py-0.5 text-xs font-medium text-emerald-700 dark:text-emerald-400">
            {deltaPct}%
          </span>
        )}
      </div>

      <p className="mt-2 line-clamp-2 text-xs text-zinc-600 dark:text-zinc-400">
        ★ {product.reviewScore.toFixed(1)} — {product.reviewSummary}
      </p>
    </a>
  );
}

function formatBRL(value: number) {
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}
```

Cinco coisas que esse card faz e o JSON sozinho não faz:

1. **Foto com fallback** — `onError` troca pra placeholder. Imagem quebrada destrói confiança.
2. **Preço dominante** — `text-lg font-semibold` no atual, riscado pequeno no anterior.
3. **Delta em verde** — só mostra desconto. Subida de preço você não anuncia, óbvio.
4. **Review compacta** — score + uma linha, não o histórico inteiro de comentários.
5. **Card inteiro é o link** — não tem CTA "ver produto". O card É o CTA.

### Passo 5: streaming progressivo de N cards

Se a tool demora, o usuário olha pro skeleton. Se a tool retorna 3 cards de uma vez, eles entram juntos. Bom o suficiente.

Quando o seu agente fizer múltiplas chamadas (recomendar + comparar + buscar review), o `message.parts` vai ter várias entradas. Renderiza na ordem que chegar — o AI SDK já garante streaming SSE por baixo.

```tsx
// components/product-card-grid.tsx
export function ProductCardGrid({ products, reasoning }: ProductCardGridProps) {
  return (
    <div className="space-y-3">
      <p className="text-xs text-zinc-500">{reasoning}</p>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        {products.map((p) => (
          <ProductCardItem key={p.sku} product={p} />
        ))}
      </div>
    </div>
  );
}
```

## Limitações e pontos de atenção

Onde isso quebra na vida real:

- **Schema rígido demais castra o agente.** Se você obriga `previousPrice` a ser `number`, o produto que nunca teve histórico vai virar mentira. `nullable` resolve. Pense no schema como contrato, não como gaiola.
- **Imagens nem sempre existem.** Catálogo legado tem SKU sem foto. Sem fallback no `<Image>`, o card vira buraco branco. Pior: vira layout shift.
- **Delta de preço pede fonte verificada.** Não deixe o LLM inventar `previousPrice`. Esse campo vem do seu banco, sempre. Modelo só escolhe SKU.
- **Acessibilidade não é detalhe.** Foto sem `alt`, card sem `<a>` com URL real, contraste de delta em fundo claro — tudo isso quebra leitor de tela e SEO.
- **Performance com N cards.** Mais de 12 cards na tela exige virtualização (`react-virtuoso` ou similar). Streaming não substitui paginação.
- **Privacidade nos prompts.** Histórico de compra entrando direto no system prompt vaza dado pessoal pro provedor. Mascare CPF, e-mail, endereço antes.

## Pra fechar: a UI é o produto

Backend bonito que renderiza JSON cru não é produto. É demo de feira.

O dev sênior de IA aplicada hoje precisa pensar nas duas pontas: o agente que decide e a UI que entrega. Schema rígido + componente bem composto é o que separa "ferramenta interna que funciona" de "feature que o usuário usa todo dia".

No [Clã Beer & Code](https://beerandcode.com.br/cla) a gente tá construindo exatamente esse caminho — agentes, RAG, tool use e produto real, com Laravel no back e React no front. Se você tá cansado de tutorial de prompt mágico e quer construir feature de IA que aguenta produção, esse é o lugar.

## FAQ rápido

**O modelo pode quebrar o schema mesmo com structured outputs?**

Em modelos suportados (Sonnet 4.5+, Opus 4.5+, Haiku 4.5+, GPT-4o), não. A doc da Anthropic é explícita: "no more `JSON.parse()` errors". O que pode acontecer é o modelo recusar a tarefa — aí o tool call não acontece e você trata na UI.

**Vale usar Vercel AI SDK ou LangGraph?**

Depende do stack. AI SDK é melhor pra Next.js puro, com integração nativa de streaming SSE. LangGraph compensa quando você tem grafo de agente complexo (múltiplos passos, condicional, retry) — ele tem `push_ui_message()` justamente pra emitir UI no meio do fluxo.

**Posso renderizar isso server-side com RSC?**

Pode. O AI SDK suporta React Server Components há alguns releases — a tool é mapeada pra um RSC e streamada via Suspense. Reduz JS no cliente e é ótimo pra SEO de catálogo. A doc oficial tem [um template pronto](https://vercel.com/templates/next.js/rsc-genui).

**E o JSON-Render que a Vercel lançou? Substitui isso tudo?**

Não substitui — abstrai. Você define um catálogo de componentes em Zod e o modelo gera um spec JSON restrito a ele. Ótimo quando o leque de UIs é grande e você não quer hard-codar cada `tool-${name}`. Pra uma feature focada como "card de produto", o padrão deste post é mais direto e dá mais controle.

## Conclusão

A gente saiu de "agente devolve JSON" e chegou em "card que converte". O caminho passa por schema sério (Zod), structured outputs no modelo, tool execution que confia no seu catálogo (não no LLM) e componente React que respeita hierarquia visual.

O próximo passo dessa stack é generative UI orientada a evento — o agente não escolhe um componente fixo, ele compõe um layout em runtime baseado no contexto. Vercel json-render e LangGraph já apontam pra lá. Mas antes de chegar nesse hype, garante o básico: seu agente já está conseguindo virar feature visível pro usuário?

Se a resposta é "ainda não", esse post é seu mapa.
