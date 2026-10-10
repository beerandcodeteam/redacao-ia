# Pauta Beer & Code — Semana 4 (Seg 22/06 a Dom 28/06/2026)

> Pauta FOCADA de news-jacking. **10 posts**: 2 das janelas GPT-5.6/Fable (abaixo) + 8 da caçada de 22/jun (foco: notícias de IA, IA como assistente de código e construção de agents — altas impressões/CTR no BR).
> Estratégia: replicar o padrão que já venceu (claude-fable-5-vs-opus-4-8 = 50 cliques/1005 imp; fable-5-bloqueado = CTR 6,23%) — chegar primeiro em termo de cauda-longa de baixa concorrência. Ver memória project_padrao_vencedor_newsjacking.
> Ordem de publicação por decaimento: notícia que decai rápido sai primeiro (GLM-5.2, bug do Codex, Mythos); evergreen que vale ranquear cedo entra logo em seguida pra já estar relevante quando o volume BR chegar (CLAUDE.md, Copilot, agentes).
> ⚠️ Marcar VERIFICADO vs RUMOR no corpo (vale pra GPT-5.6, pro "hack da NSA" pelo Mythos e pros números do post "americanos contra a IA"), senão queima credibilidade.
> Anti-canibalização: o blog já tem 40+ posts no cluster "agentes de IA"; só ângulo newsy específico (ex.: Sakana Fugu) vira pauta nova — não duplicar tema genérico de "construir agente".

## As cláusulas do CLAUDE.md que o Karpathy usa (e a 5ª que virou game changer pra comunidade)
- publicar_em: 2026-06-25T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: tutoriais
- resumo: O post mais votado da semana no r/ClaudeAI (1434 ups) parte das 4 cláusulas de CLAUDE.md sugeridas pelo Andrej Karpathy e adiciona uma 5ª. Vira um guia prático de como escrever um CLAUDE.md que o Claude Code realmente obedece. Semi-evergreen: publicar agora pra ranquear cedo no termo "claude code" (135k/mês), que só cresce no BR.
- hook: O Karpathy resumiu o CLAUDE.md em 4 cláusulas. A comunidade adicionou uma 5ª — e ela é a que mais muda o comportamento do agente.
- bullets:
  - As 4 cláusulas do Karpathy: o que cada uma faz e por que enxugar o CLAUDE.md importa
  - A 5ª cláusula da comunidade: o que ela adiciona e por que virou game changer
  - CLAUDE.md em camadas: global vs projeto vs subpasta (interlink com claude-code-monorepo)
  - Anti-padrões: o CLAUDE.md inchado que o modelo ignora
  - Template pronto pra copiar — e como medir se o agente está obedecendo
  - Interlink com claude-code-hooks-slash-commands-mcp e claude-code-o-que-e-como-funciona
- keyword_principal: claude.md
- keywords_secundarias: claude md exemplo, como escrever claude.md, claude code claude.md, claude.md boas práticas, karpathy claude.md
- tags: ia, claude, claude-code, anthropic, produtividade
- dificuldade: medium (cluster Claude Code forte; ângulo CLAUDE.md ainda livre — não canibalizar hooks/monorepo)
- volume: ride do termo "claude code" (135k/mês, KD36); evergreen pra ranquear cedo

## [#1] Mistral OCR 4: testei o novo modelo de OCR e ele lê PDF melhor que o ChatGPT?
- publicar_em: 2026-06-24T18:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A Mistral lançou o OCR 4 e ele foi direto pro topo do Hacker News (476 pts). Mostramos o que muda na extração de texto de PDF/documento, comparamos com a leitura de OCR do ChatGPT/Gemini e dizemos quando vale plugar na stack. VERIFICADO: lançamento oficial. Formato testável/atualizável conforme saem benchmarks. Único candidato 100% net-new com demanda mensurável e zero overlap com o cluster Anthropic.
- hook: OCR sempre foi a parte chata do pipeline de documentos. O Mistral OCR 4 promete resolver — e roda barato. Será que aguenta nota fiscal e PDF torto?
- bullets:
  - O que o Mistral OCR 4 entrega de novo (e o que mudou da v3)
  - Teste real: PDF, documento multipágina e imagem torta
  - Mistral OCR 4 vs OCR do ChatGPT/Gemini: precisão e custo
  - Como plugar via API compatível na sua stack (snippet)
  - Quando vale trocar seu OCR atual — e quando não
- keyword_principal: mistral ocr 4
- keywords_secundarias: mistral ocr, ocr ia, ocr com ia, extrair texto de pdf com ia, ocr open source
- tags: ia, llm, mistral, ocr, modelos-de-ia
- dificuldade: easy
- volume: "mistral ocr" KD 14 (baixo); categoria "ocr ia" 140/mês BR + "ocr open source" 70/mês; "mistral ocr 4" ~0 ainda = cauda-longa de lançamento, janela aberta

## [#4] OpenAI DayBreak: o GPT-5.5-Cyber que caça e corrige vulnerabilidades sozinho — o que muda pro dev
- publicar_em: 2026-06-25T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A OpenAI lançou o DayBreak (GPT-5.5-Cyber), modelo voltado a defensores que encontra e remenda falhas de segurança — HN 213 pts + cobertura (Infosecurity, IBM subiu 4,7% no anúncio). Explicamos o que ele faz na prática, onde entra no fluxo de um dev e os limites de confiar correção de vuln a um modelo. VERIFICADO: lançamento oficial; separar marketing de capacidade real. Post não-Anthropic que equilibra a semana.
- hook: A OpenAI soltou um modelo que promete achar e corrigir bugs de segurança antes de você. Ferramenta de defensor ou mais uma camada que você vai ter que revisar na mão?
- bullets:
  - O que é o DayBreak / GPT-5.5-Cyber e o que a OpenAI promete
  - Caçar vs corrigir vulnerabilidade: o que o modelo realmente faz no fluxo
  - Onde isso entra no dia a dia de quem programa (CI, code review, SAST)
  - Os limites: falso positivo, patch que quebra, e por que revisão humana continua
  - Como testar com responsabilidade (e o que NÃO automatizar ainda)
- keyword_principal: openai daybreak
- keywords_secundarias: gpt 5.5 cyber, openai modelo seguranca, ia que corrige vulnerabilidade, openai cybersecurity, daybreak openai
- tags: ia, openai, seguranca, gpt-5-5, llm
- dificuldade: medium (termo recém-nascido, SERP PT vazia; fit médio com o pilar dev)
- volume: ~0 BR (lançamento); cauda-longa de segurança+OpenAI sem concorrência PT-BR

## [#3] Fable 5 foi jailbroken em poucos dias — o que quebrou e o que isso diz sobre segurança de LLM
- publicar_em: 2026-06-26T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Bruce Schneier publicou que o Fable 5 da Anthropic foi jailbroken poucos dias após o lançamento. Explicamos o que significa "jailbreak" de um frontier, por que acontece tão rápido e o que muda pra quem coloca esses modelos em produção. VERIFICADO via Schneier; marcar o que é demonstração de pesquisa vs risco prático. Domínio já ranqueia forte em "fable" (pos 4–13 no GSC) = autoridade herdada.
- hook: A Anthropic vende o Fable 5 como o modelo mais alinhado da casa. Dias depois, já tinha jailbreak circulando. O que isso revela sobre confiar LLM em produção?
- bullets:
  - O que é jailbreak de LLM, em 2 minutos
  - O caso Fable 5: o que foi quebrado (e por quem)
  - Por que modelos novos caem rápido
  - O que isso significa pra quem usa Fable/Claude em produto
  - Como reduzir o risco no seu app (guardrails na prática)
- keyword_principal: fable 5 jailbreak
- keywords_secundarias: jailbreak llm, fable 5 seguranca, jailbreak claude, seguranca de llm em producao
- tags: ia, llm, claude, anthropic, fable-5, seguranca-ia
- dificuldade: medium
- volume: ~0 BR (lançamento); autoridade herdada do cluster Fable (pos 4–13 GSC); cauda-longa de segurança sem concorrência PT-BR

## [#2] Brasil bloqueado: por que os EUA não deixam você usar o Mythos da Anthropic (e o processo que quer mudar isso)
- publicar_em: 2026-06-27T17:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A Legion entrou na Justiça contra o governo dos EUA pela ordem que limita o acesso estrangeiro aos modelos top da Anthropic (Mythos/Fable). Explicamos o que a diretiva proíbe na prática, por que o Brasil cai no "estrangeiro" bloqueado e o que o processo pode mudar. VERIFICADO: processo é real; separar decisão judicial de especulação. Formato vivo (atualiza conforme o processo anda). Ângulo único pra audiência BR.
- hook: Você tentou usar o Fable/Mythos e bateu num "indisponível na sua região"? Não é bug — é política de controle de exportação dos EUA. Agora tem gente processando pra derrubar.
- bullets:
  - O que a ordem dos EUA proíbe (e por que pega o Brasil)
  - Quem é a Legion e o que o processo pede
  - Mythos, Fable e a régua de "modelo de fronteira"
  - O que muda pra quem desenvolve fora dos EUA
  - Cenários: o que acontece se o processo ganhar ou perder
- keyword_principal: anthropic acesso bloqueado brasil
- keywords_secundarias: mythos anthropic, fable 5 indisponivel, modelo anthropic bloqueado, acesso estrangeiro modelos ia
- tags: ia, llm, anthropic, mythos, fable-5, export-controls
- dificuldade: medium
- volume: ~0 BR (termo recém-nascido); GSC já pinga "fable 5 indisponivel" pos 4,6 e "claude fable 5 indisponivel" pos 2 = demanda provada por bloqueio; interlink p/ fable-5-bloqueado-openrouter-fusion e mythos-anthropic-invadiu-nsa-fato-ou-boato

---

## Updates (NÃO são posts novos — anti-canibalização)

### [#6] Atualizar tracker GPT-5.6 — `gpt-5-6-data-lancamento-vazamentos-rastreador`
- quando: hoje 24/jun (baixo custo, time-sensitive)
- o quê: adicionar a entrada do atraso ("June delays 5.6", r/singularity 222 ups, 24/jun). Atualizar a tabela fato/boato + a linha do Polymarket se a odds mudou. É um tracker, feito pra isso → atualiza `updated_at` (sinal de frescor).

### [#5] Micro-update Sakana Fugu — `sakana-fugu`
- quando: hoje 24/jun (1 linha)
- o quê: o post JÁ cobre Fugu Ultra + guerra de benchmark + preço + export-controls. Única novidade: o `fugu-ultra` entrou no **catálogo do OpenRouter** (o post só cita a API própria da Sakana). Adicionar 1 frase no FAQ/TL;DR ("agora disponível também via OpenRouter") e refrescar `updated_at`. **NÃO abrir post novo** — canibalizaria a mesma keyword.
