---
name: montar-cta-pitch
description: Monta o CTA/pitch de um post do blog Beer & Code quando o destino é o Clã Beer and Code ou um evento da marca. Acionar na hora de escrever o CTA dentro do fluxo da criar-post-blog (passo 3), ou quando o usuário pedir para "fazer o pitch do Clã", "montar o CTA do evento", "vender o Clã no post", "escrever um post-pitch" ou equivalente. Traduz o pitch de vendas validado ao vivo (tese, dor, 3 pilares, prova social, ancoragem, objeções, garantia) para o formato de blog em 3 níveis de intensidade, sem quebrar a brand voice.
---

# Montar CTA/pitch para o Clã Beer and Code (e eventos)

O pitch do Clã foi validado ao vivo em evento e está destrinchado em `references/arsenal-pitch-cla.md`. Aquilo é uma **coreografia de webinar** — chat, demo ao vivo, micro-compromissos, urgência de encerramento. Num post de blog isso não entra em sequência: entra como arsenal. O trabalho desta skill é escolher **um ângulo** do arsenal, na **intensidade certa**, e costurar no texto sem que o leitor sinta a pausa comercial.

Regra zero: as regras de `criar-post-blog/references/brand-voice.md` → "Tom comercial (CTA)" **continuam valendo e vencem qualquer conflito** (sem heading dedicado, sem caixa, sem hard sell, link inline, teste mental). Esta skill decide *o que dizer*; a brand voice decide *como soar*.

## Constante do projeto (não perguntar)

| destino | URL |
|---|---|
| **Clã Beer and Code** | `https://beerandcode.com.br` |

Essa é a URL oficial do Clã, confirmada pelo Lucas. Quando o destino for o Clã, **use-a direto — não pergunte** (anexe as UTMs do Passo 3.8 por cima). Continue perguntando apenas quando o destino for um **evento** (que tem URL, nome e data próprios) ou outro recurso.

## Inputs

- **Destino** — Clã ou evento. Para o Clã, a URL é a constante acima. Para evento, a URL + nome + data vêm do input do post/batch; se não vierem, pergunte ao usuário — não invente nem reaproveite URL de memória.
- **Tema e persona do post** — de qual dor/assunto o post vem. É isso que escolhe o ângulo.
- **Nível do CTA** — se o usuário não disser, é nível 1.

## Passo 1 — Escolher o nível

| Nível | O que é | Quando usar |
|---|---|---|
| **1 — Menção inline** | 1–2 frases dentro da prosa, no primeiro terço do post (~30%). O formato padrão da brand voice. | Default de todo post com destino de CTA. |
| **2 — Parágrafo-ponte** | 3–5 frases fechando a conclusão: dor do tema → mecanismo do Clã → convite. Ainda sem heading, sem caixa, sem preço. | Usuário pediu "CTA mais forte", post de campanha, ou semana de evento. |
| **3 — Post-pitch** | O post inteiro (ou uma seção final longa) É sobre o Clã/evento. Único nível onde entram preço, garantia, bônus e qualificação negativa completa. | Só quando o usuário pedir explicitamente um post de venda/lançamento. Nunca decida sozinho subir para nível 3. |

## Passo 2 — Escolher UM ângulo (a ponte tema → pitch)

O CTA bom continua o raciocínio do post. Escolha o ângulo pelo tema, não pelo seu favorito:

| Tema do post | Ângulo do arsenal (ver referência) |
|---|---|
| Lançamento de modelo/ferramenta, notícia de IA | Dor da obsolescência → pilar "execução semanal" (B + C) |
| Tutorial hands-on, build, código | "Construir sozinho é mais lento" → comunidade que executa junto (C) |
| Carreira, salário, mercado de trabalho | Tese "engenharia de IA é profissão" + ancoragem salarial ⚠️ (A + F) |
| Vibe coding, hype, "IA vai substituir dev" | "Vibe Coding é técnica, Engenharia de IA é profissão" (A) |
| Post para gestor/PM/empresário/não-dev | Prova social por arquétipo: CTO, PM, empresário (E + J) |
| Comparativo de ferramentas, stack | "Dependente de ferramenta" / "a stack não é mais o problema" (G + J) |
| Post sobre evento (destino = evento) | Bloco M — evento como amostra do ambiente. Sem preço do Clã, sem segundo destino. |

Um ângulo por post. Dois argumentos empilhados no nível 1–2 já soam funil.

**Anti-repetição (obrigatório em batch):** o mesmo ângulo com a mesma frase em vários posts faz o blog cheirar a automação. Em batch (`criar-posts-batch`), **rotacione os ângulos entre os posts da leva** — mesmo quando a tabela permitiria repetir — e reescreva cada CTA do zero. No fluxo single-post, se o MCP do blog estiver na sessão, espie o CTA dos 3–5 últimos posts publicados (`ListPosts` + `GetPost` — procure no primeiro terço e na conclusão) e não parafraseie um CTA recente.

## Passo 3 — Escrever

1. **Leia `references/arsenal-pitch-cla.md`** e pegue as linhas prontas do ângulo escolhido. São exemplo de *estrutura*, não texto final — reescreva no ritmo do post e **nunca reutilize a mesma frase (ou quase) em mais de um post**.
2. **O CTA nasce do texto, não interrompe** (ponto 1 do pitch original, "gancho orgânico"). A frase anterior ao link tem que estar falando do tema do post; o Clã/evento entra como o próximo passo lógico daquilo.
3. **Um link para o destino por post.** Posição default: **primeiro terço do post (~30% da leitura)**, no trecho do corpo que mais conversa com o destino (ex.: *"esse pipeline a gente construiu ao vivo no Clã"* logo depois do trecho técnico correspondente). Conclusão só como fallback quando não houver encaixe natural antes — um ou outro, nunca os dois. Racional: a maioria dos leitores (news-jacking em especial) não chega ao fim do post; a menção cedo pega o leitor ainda engajado.
4. **Nível 2 pode usar UMA afirmação de concordância** antes do convite (adaptação escrita dos micro-compromissos do pitch ao vivo): *"Construir sozinho é mais lento — você já sentiu isso."* Uma só. Pergunta retórica escrita ("Cansado de perder tempo?") lê como página de vendas antiga — evite; e empilhar três é webinar, não blog.
5. **Transparência em vez de disfarce** (adaptação do "desarme da objeção de venda"): quando a menção for ao Clã, não finja que não é produto. Naturalidade > eufemismo. Ex.: *"é pago, é assinatura, e é exatamente o ambiente que esse post descreve"* funciona melhor que rodeio.
6. **Dados perecíveis (⚠️ na referência) exigem confirmação do usuário na sessão antes de entrar no texto.** Isso cobre preço, bônus, pesquisa salarial e urgência de preço — e também os **operacionais**: dia/hora da live ("toda terça, 19h") e volume de conteúdo ("500+ horas") mudam sem aviso e ficam errados em post indexado. Em nível 1–2, use a forma segura: *"toda semana, ao vivo"*. Nunca recicle urgência de evento passado ("último evento nesse preço") em post evergreen.
7. **Preço, garantia e bônus só no nível 3.** No nível 1–2 o leitor clica para descobrir; no nível 3 o post é a página de vendas e aí entra a ancoragem em três camadas, a garantia e o filtro negativo completos.
8. **Medição (UTM).** Se o destino é URL própria da marca e veio sem UTMs, anexe: `?utm_source=blog&utm_medium=post&utm_campaign=<slug-do-post>&utm_content=<bloco>-n<nivel>` (ex.: `utm_content=c-n1` = bloco C, nível 1). É o que permite comparar no GA4 qual ângulo converte e evoluir a tabela do Passo 2 com dado em vez de intuição. Se a URL já vier com UTMs do input, não sobrescreva.

## Passo 4 — Checklist antes de devolver

- [ ] Passa no teste mental da brand voice: se o leitor pular o link, a frase ainda fecha o raciocínio?
- [ ] Um ângulo só (nível 1–2)?
- [ ] Um único link para o destino no post inteiro, em uma única posição?
- [ ] Não repete nem parafraseia de perto o CTA de outro post recente / da mesma leva de batch?
- [ ] Sem heading/caixa/`---`/botão? Link inline `[nome](url)`?
- [ ] Zero vocabulário proibido: "imperdível", "última chamada", "vagas limitadas", "garanta sua vaga", "não fique de fora"?
- [ ] Nenhum dado perecível sem confirmação — incluindo dia/hora da live e "500+ horas", não só preço?
- [ ] UTM `utm_content=<bloco>-n<nivel>` no link (URL própria, sem UTM prévia no input)?
- [ ] Se nível 3: qualificação negativa presente (o filtro "pra quem NÃO é" é o que diferencia pitch do Clã de pitch de guru)?

## Saída

Devolva o trecho de CTA pronto (ou o outline do post-pitch, se nível 3) + uma linha dizendo qual ângulo do arsenal foi usado e por quê. Quem chama (usuário ou a skill `criar-post-blog`) integra no body.
