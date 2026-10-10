# Varredura de canibalização — blog Beer & Code — 13/09/2026

Três rodadas de workflow: 39 clusters temáticos julgados (281 posts do sitemap), 61 ações propostas, cada uma refutada por duas lentes (SEO e editorial). Sobreviveram 55 na rodada 1 e 4 na rodada 3 (crítico de completude). Aplicação via `update-post` só de title/meta/excerpt/body; nada foi despublicado, nenhum slug ou data mudou.

Evidência principal: pares query×página do Search Console (15/06 a 12/09), 26 pares de posts dividindo impressões na mesma query, mais comparação de título/H1/meta por cluster.

## Remover (com redirect 301 para o canônico)

Não existe tool de remoção no MCP e despublicar sem redirect perde links e histórico. Estes seis já receberam callout apontando pro canônico e título de-otimizado; a remoção é decisão do Lucas.

| remover | redirect 301 para | por quê |
|---|---|---|
| `noticias/melhor-ia-para-programacao-2026` | `noticias/melhor-ia-para-programar-2026-claude-code-vs-codex` | Mira exatamente a mesma pergunta ('Qual a melhor IA para programar?' é a primeira frase do body) e tem 0 impressões em 90 dias contra 3500 do canônico. O que ele tem de único (enquadramento modelo vs ferramenta vs fluxo, |
| `tutoriais/agentic-rag-quando-o-agente-decide-o-que-buscar` | `tutoriais/agentic-rag-quando-seu-rag-vira-agente` | Competing pair no GSC ('agentic rag': 5 imp pos 34 aqui vs 74 imp pos 28.4 no canônico). Conteúdo quase duplicado: mesmo H1 'Agentic RAG: quando...', mesmo TL;DR, mesmo paper (arXiv 2601.07711) com os mesmos números, mes |
| `noticias/engenheiro-de-ia-o-que-faz-no-dia-a-dia` | `noticias/engenheiro-de-ia-2026-o-que-faz` | Canibalização forte: mesma intenção ('o que faz um engenheiro de IA / rotina') do canônico. GSC mostra 'engenheiro de ia' com 17 imp pos 30.5 aqui vs 18 imp pos 27.3 no canônico, ambos 21 impressões e 0 cliques. Títulos  |
| `tutoriais/programmatic-tool-calling-futuro-agente` | `tutoriais/programmatic-tool-calling` | Redundante com o canônico: mesma head keyword no título/meta_title ('Programmatic Tool Calling: o futuro do agente em código' vs 'Programmatic tool calling: o agente escreve o código'), mesma capa, mesmo passo a passo (a |
| `tutoriais/como-criar-mcp-server` | `tutoriais/como-criar-um-servidor-mcp-do-zero` | Redundante com o canônico publicado 17 dias depois: 'Como criar seu primeiro MCP server (tool + resource) e plugar no Claude' vs 'Como criar um servidor MCP do zero: tools, resources e prompts, do stdio ao HTTP'. Mesma s |
| `noticias/o-que-e-harness-de-ia` | `tutoriais/anatomia-de-um-agent-harness-state-tool-execution-feedback-loops-e-guardrails` | Mesma intenção informacional do canônico ('O que é Harness de IA?' vs meta_title 'O que é um Agent Harness?' + H2 'O que é um agent harness?' + FAQ 'O que significa harness em IA?'). 0 impressões em 90 dias após 3 meses  |

## Ações aplicadas

| post | ação | canônico | novo título (se mudou) | status |
|---|---|---|---|---|
| `noticias/engenheiro-de-ia-o-que-faz-no-dia-a-dia` | merge_into | `noticias/engenheiro-de-ia-2026-o-que-faz` | 4 mitos sobre o engenheiro de IA: o que ele NÃO faz em 2026 | aplicado (rodada 1, confirmado na 2) |
| `tutoriais/agentic-rag-quando-o-agente-decide-o-que-buscar` | merge_into | `tutoriais/agentic-rag-quando-seu-rag-vira-agente` | Retriever como tool: o padrão de 4 nós do LangGraph (grade e rewrite) | aplicado (rodada 1) |
| `tutoriais/como-criar-mcp-server` | merge_into | `tutoriais/como-criar-um-servidor-mcp-do-zero` | Tool async com API externa e resource template num MCP server (ViaCEP) | aplicado (rodada 2) |
| `tutoriais/programmatic-tool-calling-futuro-agente` | merge_into | `tutoriais/programmatic-tool-calling` | Function calling clássico vs. code execution: a comparação lado a lado (37% menos tokens) | aplicado (rodada 2) |
| `noticias/alucinacao-de-ia-grounding` | deoptimize_and_link | `noticias/por-que-a-ia-alucina-e-como-reduzir-alucinacao-no-seu-produto` | Grounding de LLM: as 4 camadas que prendem a resposta da IA no seu dado (e validam antes d | aplicado (rodada 2) |
| `noticias/claude-opus-5-vazamento` | deoptimize_and_link | `noticias/claude-opus-5` | Vazamento do Claude Opus 5: do Honeycomb ao lançamento (tracker encerrado) | aplicado (rodada 1) |
| `noticias/gpt-5-6-data-lancamento-vazamentos-rastreador` | deoptimize_and_link | `noticias/gpt-5-6-sol-terra-luna-qual-usar` | GPT 5.6: data de lançamento, o vazamento no Codex e o que os rumores acertaram (rastreador | aplicado (rodada 1) |
| `noticias/gpt-6-lancamento-rastreador` | deoptimize_and_link | `noticias/gpt-6-astra-vs-fable-5-1-vs-gpt-5-6-sol` | Linha do tempo do GPT-6: de Altman em Washington ao lançamento do Astra (rastreador encerr | aplicado (rodada 1, confirmado na 2) |
| `noticias/openai-astra-rastreador` | deoptimize_and_link | `noticias/gpt-6-astra-vs-fable-5-1-vs-gpt-5-6-sol` | Antes do GPT-6: os 10 problemas de matemática que o Astra da OpenAI resolveu, as provas em | aplicado (rodada 1, confirmado na 2) |
| `tutoriais/adocao-segura-ia-empresa-eu-ai-act-nist-rmf` | deoptimize_and_link | `tutoriais/compliance-eu-ai-act-nist-rmf-checklist-18-itens-brasil` | Os 4 níveis de risco do EU AI Act: como classificar sua feature de IA (+ template de AI De | aplicado (rodada 2) |
| `noticias/claude-code-vazando-email-curl-user-agent` | retitle | `noticias/claude-code-auto-mode-padrao` | Claude Code vazando email no curl: o que a issue #78431 prova e o checklist de deny rules  | aplicado (rodada 1) |
| `tutoriais/avaliacao-de-agentes-de-ia-evals-honestos` | retitle | `tutoriais/evals-para-agentes-de-ia-llm-as-a-judge` | Métricas de avaliação de agentes de IA: o que medir em cada etapa (retrieval, tool, respos | aplicado (rodada 1) |
| `tutoriais/code-review-com-ia-sem-virar-carimbador` | retitle | `tutoriais/5-padroes-prompt-code-review-llm` | Code review com IA: benchmark de 7 ferramentas (precision e recall) e como medir se o seu  | aplicado (rodada 1) |
| `tutoriais/engenharia-de-contexto-vence-prompt-engineering` | retitle | `noticias/engenharia-de-prompt-acabou-engenharia-de-contexto` | Engenharia de contexto na prática: 3 experimentos com tokens, custo e testes (8/8 vs 4/8) | aplicado (rodada 2) |
| `noticias/agentic-code-quando-agente-escreve-executa-testa-proprio-codigo` | link_only | `noticias/4-niveis-autonomia-agentic-code` |  | aplicado (rodada 1) |
| `noticias/agentic-code-vs-vibe-coding-vs-sdd-tabela-decisao` | link_only | `tutoriais/sdd-vs-bmad-vs-vibe-coding-qual-metodologia-faz-sentido` |  | aplicado (rodada 1, confirmado na 2) |
| `noticias/anthropic-verificacao-de-identidade-claude` | link_only | `noticias/anthropic-acesso-bloqueado-brasil` |  | aplicado (rodada 1, confirmado na 2) |
| `noticias/claude-fable-5-vs-opus-4-8` | link_only | `noticias/claude-fable-5-1-vs-opus-5` |  | aplicado (rodada 1) |
| `noticias/claude-hackeou-3-empresas` | link_only | `noticias/claude-invadiu-empresas-pacote-pypi` |  | aplicado (rodada 3) |
| `noticias/custo-agente-ia-producao-2026-planilha-tco` | link_only | `tutoriais/quanto-custa-agente-ia-producao-conta-tokens` | TCO de um agente de IA em produção: os 6 baldes de custo que a calculadora esconde (planil | aplicado (rodada 1) |
| `noticias/deepseek-v4-flash-0731` | link_only | `noticias/deepseek-v4-pro-0813` |  | aplicado (rodada 2) |
| `noticias/deepseek-v4-preco` | link_only | `noticias/deepseek-v4-pro-0813` | DeepSeek V4 peak/valley: o preço por horário de pico e a pegadinha de fuso que favorece o  | aplicado (rodada 2) |
| `noticias/engenharia-de-contexto-o-que-vai-no-prompt` | link_only | `tutoriais/ferramentas-de-engenharia-de-contexto-em-producao` |  | aplicado (rodada 1, confirmado na 2) |
| `noticias/engenharia-de-prompt-acabou-engenharia-de-contexto` | link_only | `noticias/engenharia-de-prompt-guia-honesto` |  | aplicado (rodada 1, confirmado na 2) |
| `noticias/fable-5-bloqueado-openrouter-fusion` | link_only | `tutoriais/openrouter-o-que-e-como-usar-e-quando-vale-a-pena` |  | aplicado (rodada 2) |
| `noticias/gpt-5-6-sol-ultra-codex` | link_only | `noticias/gpt-5-6-sol-terra-luna-qual-usar` |  | aplicado (rodada 3) |
| `noticias/kimi-k3-benchmarks-vs-claude` | link_only | `noticias/kimi-k3-pesos-abertos` |  | aplicado (rodada 2) |
| `noticias/laravel-ai-sdk-vale-migrar-do-prism` | link_only | `tutoriais/laravel-ai-sdk-vs-prism` | Migrei um projeto real de Prism pro Laravel AI SDK: 47 linhas a menos, diff aberto | aplicado (rodada 1) |
| `noticias/melhor-ia-para-programacao-2026` | link_only | `noticias/melhor-ia-para-programar-2026-claude-code-vs-codex` | Melhor IA para programação em 2026: Claude Code, Cursor e Copilot na mesma task Laravel | aplicado (rodada 1) |
| `noticias/meta-proibe-claude-code-engenheiros` | link_only | `noticias/alibaba-baniu-claude-code` |  | aplicado (rodada 1) |
| `noticias/o-que-e-fine-tuning` | link_only | `noticias/fine-tuning-rag-ou-prompt-qual-escolher` |  | aplicado (rodada 2) |
| `noticias/o-que-e-harness-de-ia` | link_only | `tutoriais/anatomia-de-um-agent-harness-state-tool-execution-feedback-loops-e-guardrails` | O que é Harness de IA? O ambiente que faz seu agente parar de travar | aplicado (rodada 1, confirmado na 2) |
| `noticias/o-que-e-harness-engineering-e-por-que-seu-claude-code-trava-em-tarefas-longas` | link_only | `tutoriais/anatomia-de-um-agent-harness-state-tool-execution-feedback-loops-e-guardrails` |  | aplicado (rodada 3) |
| `noticias/quando-usar-rag-fine-tuning-ou-contexto` | link_only | `noticias/fine-tuning-rag-ou-prompt-qual-escolher` | Quando usar RAG: os 4 critérios que decidem (e quando contexto longo ou fine-tuning ganham | aplicado (rodada 1) |
| `noticias/qwen-3-8-max` | link_only | `noticias/qwen-3-8-max-pesos-abertos` |  | aplicado (rodada 2) |
| `tutoriais/5-sinais-de-que-sua-especificacao-virou-burocracia-e-como-voltar-a-base-bem-feita` | link_only | `tutoriais/paradoxo-da-especificacao-quando-sdd-vira-overengineering` | 5 sinais de que sua especificação virou burocracia (e como voltar à base bem feita) | aplicado (rodada 1) |
| `tutoriais/agente-bolao-copa-whatsapp-evolution-api-n8n` | link_only | `tutoriais/como-criar-um-agente-de-ia-para-whatsapp` |  | aplicado (rodada 2) |
| `tutoriais/anatomia-de-um-harness-em-producao-as-6-camadas-que-separam-poc-de-sistema-confiavel` | link_only | `tutoriais/anatomia-de-um-agent-harness-state-tool-execution-feedback-loops-e-guardrails` |  | aplicado (rodada 2) |
| `tutoriais/como-implementar-busca-semantica-no-laravel-com-embeddings-e-postgresql-pgvector` | link_only | `tutoriais/guia-rag-backend-pgvector-laravel` |  | aplicado (rodada 1) |
| `tutoriais/como-rodar-llm-local` | link_only | `noticias/llm-local-vs-api-2026-planilha-90-dias` |  | aplicado (rodada 2) |
| `tutoriais/cortando-custo-em-80-prompt-caching-batch-e-quando-nao-usar-reranker` | link_only | `tutoriais/reduzir-custo-api-de-ia` |  | aplicado (rodada 1) |
| `tutoriais/cross-encoder-reranker-roi-agente-rag` | link_only | `tutoriais/reranker-rag` | Cross-encoder reranker: o componente que mais eleva qualidade do seu agente por dólar | aplicado (rodada 1) |
| `tutoriais/hooks-slash-commands-e-mcps-a-anatomia-de-um-harness-produtivo` | link_only | `tutoriais/claude-code-hooks-slash-commands-mcp` | Anatomia de um harness produtivo no Claude Code: quando usar cada peça (com exemplos Larav | aplicado (rodada 1) |
| `tutoriais/llm-as-a-judge-avaliacao-automatizada-agente-ofertas` | link_only | `tutoriais/model-graders-usando-llms-para-avaliar-llms-e-os-3-erros-que-invalidam-o-seu-eval` | LLM-as-a-Judge em Laravel com Prism: avaliando um agente de ofertas sem abrir planilha | aplicado (rodada 1) |
| `tutoriais/memoria-agente-assistente-compras` | link_only | `tutoriais/memoria-de-agente-de-ia` | Assistente de compras que esquece o usuário: 3 camadas de memória (contexto, sumário rolan | aplicado (rodada 2) |
| `tutoriais/model-graders-usando-llms-para-avaliar-llms-e-os-3-erros-que-invalidam-o-seu-eval` | link_only | `tutoriais/evals-para-agentes-de-ia-llm-as-a-judge` | Model graders (LLM-as-a-judge): 3 padrões de grader e os 3 erros que invalidam o seu eval | aplicado (rodada 1) |
| `tutoriais/multi-agent-com-claude-separando-search-judge-e-writer-e-quando-isso-e-overengineering` | link_only | `tutoriais/sistemas-multiagentes-orquestracao-assincrona` | Multi-agent com Claude: search, judge e writer em código (orquestrador mínimo e handoff ti | aplicado (rodada 1) |
| `tutoriais/prompt-injection-agente-site-raspado-system-prompt` | link_only | `noticias/prompt-injection-o-que-e-ataques-2026` |  | aplicado (rodada 2) |
| `tutoriais/prompts-resilientes-evals-adversariais-edge-cases` | link_only | `tutoriais/pipeline-eval-continuo-prompts-producao` |  | aplicado (rodada 1, confirmado na 2) |
| `tutoriais/rag-do-zero-chunking-embeddings-busca` | link_only | `tutoriais/guia-rag-backend-pgvector-laravel` |  | aplicado (rodada 1) |
| `tutoriais/rag-nao-e-so-vector-search-busca-semantica-sql-tools` | link_only | `tutoriais/rag-hibrido-na-pratica-bm25-embeddings-reranker` |  | aplicado (rodada 1) |
| `tutoriais/sdd-vs-bmad-vs-vibe-coding-qual-metodologia-faz-sentido` | link_only | `tutoriais/bmad-method-para-quem-ja-usa-sdd` |  | aplicado (rodada 1, confirmado na 2) |
| `tutoriais/spec-minima-viavel-framework-1-pagina` | link_only | `tutoriais/spec-que-o-agente-realmente-entende` |  | aplicado (rodada 3) |
| `tutoriais/tool-calling-na-pratica` | link_only | `tutoriais/tool-use-na-pratica-desenhando-ferramentas-llm` | Tool calling na prática: como o agente decide chamar uma ferramenta | aplicado (rodada 1, confirmado na 2) |
| `tutoriais/tool-use-na-pratica-desenhando-ferramentas-llm` | link_only | `tutoriais/tool-calling-nao-funciona` |  | aplicado (rodada 1, confirmado na 2) |
| `tutoriais/top-10-busca-vs-top-10-usuario-serp-bruta-sabota-agente` | link_only | `tutoriais/trust-layer-agente-reputacao-fonte` |  | aplicado (rodada 1, confirmado na 2) |
| `tutoriais/versionando-specs-documentacao-viva-sem-readme-abandonado` | link_only | `tutoriais/como-documentar-decisoes-tecnicas-com-ia-adrs-que-envelhecem-bem` |  | aplicado (rodada 1) |

## Refutados (não aplicar)

- **noticias/melhor-ia-para-programar-2026-claude-code-vs-codex** (retitle → ``): A premissa da ação ("a head keyword sumiu do GSC e precisa ser restaurada") não se sustenta nos dados. GSC 01/06–13/09, filtro query contém "melhor ia": o post canônico recebeu só 9 impressões em "melhor ia para programar 2026" (pos. 9,6) e 5 em "melhor ia par / A premissa ("head keyword sumiu do GSC, restaurar no title") não bate com o GSC. (1) "melhor ia para programar 2026" nunca sustentou esse post: no período ANTES do retitle de 15/08 (15/06–14/08) a query deu 9 impressões / 0 cliques (pos 9,6) pra ele, e "melhor
- **noticias/ia-para-programar-sem-virar-refem** (link_only → `noticias/melhor-ia-para-programar-2026-claude-code-vs-codex`): Não há canibalização. Intenções distintas: o secundário é "IA para programar: como usar sem virar refém da ferramenta" (workflow, atrofia, checklist de dependência — meta_title "IA para programar sem virar refém da ferramenta") e o canônico é "Claude Code ou C / Não é canibalização. Títulos: "IA para programar: como usar sem virar refém da ferramenta" (intenção: workflow/como usar, com METR 19%, atrofia, 4 regras, checklist) vs "Claude Code ou Codex: o Codex ganha o terminal por 13 pontos..." (intenção: qual escolher,
- **tutoriais/subagentes-na-pratica-dividindo-contexto-token-budget** (link_only → `tutoriais/sistemas-multiagentes-orquestracao-assincrona`): Não é canibalização: as intenções de busca são distintas. "Subagentes na prática: dividindo contexto entre Claudes para não estourar o token budget" (meta_title "Subagentes na prática com Claude e token budget") mira "subagentes claude code / token budget" e é
- **tutoriais/pipeline-eval-continuo-prompts-producao** (link_only → `tutoriais/prompts-resilientes-evals-adversariais-edge-cases`): Não há canibalização. Intenções de busca distintas: "Do prompt frágil ao sistema confiável: pipeline de eval contínuo para prompts em produção" (meta_title "Pipeline de eval contínuo para prompts em produção") mira CI/regressão/gate no PR com GitHub Actions; "
- **noticias/qwen-3-8-27b** (link_only → `noticias/qwen-3-8-flash-next-125b-a6b`): Não há canibalização entre "Qwen 3.8 27B tem a mesma arquitetura do 3.6..." (keyword-alvo: qwen 3.8 27b, meta_title "Qwen 3.8 27B: mesma arquitetura, ganho todo no treino") e "Qwen3.8-Flash-Next: 125B com 6B ativos..." (keyword-alvo: qwen 3.8 flash next). São 
- **noticias/longcat-2-0-owl-alpha-openrouter** (link_only → `tutoriais/openrouter-o-que-e-como-usar-e-quando-vale-a-pena`): Não há canibalização entre os dois posts, e a própria proposta admite isso ("intenção própria", "sem competing_pairs"). GSC 90 dias confirma queries totalmente disjuntas: a notícia rankeia por "owl alpha" (107 impr, pos 5.7), "owl-alpha", "longcat 2.0 openrout
- **noticias/chatbot-nao-e-agente-teste-3-turnos** (link_only): Refutado. A evidência apresentada é semelhança superficial, não sobreposição de intenção de busca principal:  1) **O próprio pipeline de clustering NÃO agrupa esses dois posts juntos.** "o-que-e-um-agente-de-ia" está no cluster "agentes-fundamentos" (junto com
- **noticias/ferramentas-de-ia-backend-top-12-testadas-2026** (link_only): Refutado. A própria justificativa da ação já desmonta o caso de canibalização antes de propor a intervenção: GSC mostra 0 competing_pairs para os dois clusters (agentic-code-melhor-ia e carreira-engenheiro-ia) — nenhuma query compartilhada em 90d — e impressõe
- **noticias/glossario-ai-engineer-vol-2-2026** (link_only): A evidência é majoritariamente semelhança superficial de título/categoria, e o único dado quantitativo (GSC) contraria a tese. (1) O próprio dataset de competing_pairs para o cluster "carreira-engenheiro-ia" NÃO lista o par glossario-ai-engineer-2026-30-termos / A refutação se apoia em três pontos:  1) MATEMÁTICA ERRADA na própria justificativa: o texto diz "12 dias de distância" entre os posts, mas published_at real é 2026-05-11 (Vol.1) e 2026-05-26 (Vol.2) = 15 dias. Erro factual no argumento que sustenta a proximid
- **noticias/modelos-de-ia-open-source-valem-a-pena-2026** (link_only): Evidência insuficiente de canibalização real. (1) GSC: os dois posts têm 0 impressões e 0 cliques em 90 dias — não há UMA query sequer em que os dois disputem SERP; o pipeline de competing_pairs (que corretamente identificou pares reais em outros clusters, ex. / Os dois posts não miram a mesma intenção de busca principal — o critério que define canibalização segundo as próprias regras da ação. Os meta_titles/títulos já divergem: A = "Modelos de IA open source valem a pena em 2026?" (pergunta sobre licença/qualidade/pa
- **anti-patterns-agentes-ia-producao** (link_only): A própria proposta já admite que "não é canibalização de keyword no sentido estrito" — e os dados confirmam: os dois posts miram intenções de busca claramente distintas. "5 anti-patterns..." (noticias, meta_title "5 anti-patterns que quebram agentes de IA em p

## Suspeitas do crítico descartadas após leitura completa

- agente-minimo-laravel: Não é canibalização — são dois posts do mesmo pilar (agentes em Laravel + Claude API, sem framework) mas com keyword-alvo e profundidade de conteúdo distintas, e a suspeita se baseou só na semelhança superficial dos excerpts ("sem framework de agente"). Diferenças de fato: (1) Post "agente-minimo-vi
- arquitetura-6-camadas: Li os dois posts inteiros e não é canibalização — são keywords distintas do mesmo pilar "arquitetura de agentes", não a mesma intenção de busca:

1. GSC não mostra overlap: no cluster "agentes-fundamentos" (wf_args.json), competing_pairs está vazio para este par — o detector automático de queries co
- rag-fine-tuning-juntos: Não é canibalização real, apesar do par de keyword bater no GSC. Li os dois posts inteiros e a intenção de busca principal é diferente, mesmo compartilhando o par lexical "rag" + "fine-tuning": "fine-tuning-rag-ou-prompt-qual-escolher" é uma árvore de decisão pra ESCOLHER entre as três opções (promp
- roadmap-90-dias: Li os dois posts inteiros. Não é canibalização: a intenção de busca principal é diferente, apesar de os dois mencionarem "90 dias" e viverem no mesmo pilar (carreira AI engineer). "roadmap-ai-engineer-90-dias" é um tutorial hands-on de 13 semanas para dev backend virar AI engineer (tool use, harness
- context-engineering-skill: Não é canibalização. Os dois posts usam o termo "engenharia de contexto" mas miram intenções de busca diferentes: o canônico sugerido (noticias/engenharia-de-contexto-o-que-vai-no-prompt) é um "o que é"/framework de decisão — o que entra e o que não entra no prompt, sem código, baseado em pesquisa (

## Correção de pauta

O retitle do `melhor-ia-para-programar-2026-claude-code-vs-codex` para restaurar "Melhor IA para programar" foi refutado com dado: o post nunca rankeou para essa keyword (9 impressões no período); 100% dos 52 cliques vêm de "codex ou claude code" e variações. Trocar o título perderia o tráfego real. A keyword de 2.900 buscas/mês precisa de um hub novo, não desse post. Ajustar na pauta de setembro.


---

# Ajustes pós-varredura — 14/09/2026

Objetivo: resolver os problemas identificados na varredura e na análise de performance de 13/09.

## 1. Auditoria das 65 edições aplicadas (Sonnet, 13 agentes)

Auditados 65 posts (57 editados + 8 canônicos). Correções aplicadas em 12:

- `noticias/alucinacao-de-ia-grounding`: Removido o parágrafo duplicado na Conclusão que repetia o link para noticias/por-que-a-ia-alucina-e-como-reduzir-alucinacao-no-seu-produto, mantendo apenas o ca
- `noticias/claude-invadiu-empresas-pacote-pypi`: Adicionado o callout recíproco (blockquote) logo após o bloco TL;DR, linkando para /noticias/claude-hackeou-3-empresas ('Veio pela manchete curta?...').
- `noticias/claude-opus-5-vazamento`: Reordenado o body: os 3 parágrafos de abertura + TL;DR agora vêm primeiro, e o callout 'Tracker encerrado' foi movido para logo após o bloco TL;DR (antes de '##
- `noticias/custo-agente-ia-producao-2026-planilha-tco`: meta_title encurtado para 'Custo de agente de IA em produção 2026: planilha real' (53 caracteres).
- `noticias/deepseek-v4-flash-0731`: Removida a cópia extra do callout na seção Rastreador; mantido apenas o callout logo após o TL;DR (posição correta). Na seção Rastreador ficou uma nota curta em
- `noticias/engenheiro-de-ia-2026-o-que-faz`: meta_description reescrita para 148 caracteres, mantendo o sentido: 'A rotina real de um engenheiro de IA em 2026: quanto do dia é código, eval e trace, o stack
- `tutoriais/anatomia-de-um-harness-em-producao-as-6-camadas-que-separam-poc-de-sistema-confiavel`: meta_title atualizado via update-post para 'Harness em produção: 6 camadas do POC ao confiável' (50 chars)
- `tutoriais/cortando-custo-em-80-prompt-caching-batch-e-quando-nao-usar-reranker`: meta_title encurtado para "Cortando custo de LLM em 80%: caching, batch e reranker" (55 chars) via update-post
- `tutoriais/programmatic-tool-calling-futuro-agente`: Corrigido o link para https://blog.beerandcode.com.br/tutoriais/anatomia-de-um-agent-harness-state-tool-execution-feedback-loops-e-guardrails via update-post (b
- `tutoriais/prompts-resilientes-evals-adversariais-edge-cases`: meta_title encurtado para "Prompts resilientes: evals com 50 casos adversariais" (52 chars)
- `tutoriais/top-10-busca-vs-top-10-usuario-serp-bruta-sabota-agente`: meta_title encurtado para 'Top-10 da busca não é top-10 do usuário: filtre a SERP' (54 chars)
- `tutoriais/versionando-specs-documentacao-viva-sem-readme-abandonado`: meta_title encurtado para 'Versionando specs: doc viva sem README abandonado' (49 chars)

Decisão humana pendente:

- `noticias/custo-agente-ia-producao-2026-planilha-tco`: No final do post há um link cujo texto âncora promete um post específico ('como pensar arquitetura de agente em PHP/Laravel sem reinventar o framework') mas o href aponta só para a home do blog (https://blog.beerandcode.com.br), sem slug. Parece um link quebra
- `noticias/gpt-5-6-sol-terra-luna-qual-usar`: Confirmar se o blockquote 'Atualizado em 15/08/2026' no topo do body (antes do TL;DR) é conteúdo editorial intencional ou deveria ser movido/removido — ele não é o callout canônico verificado (esse está correto, logo após o TL;DR, único, apontando para gpt-5-6
- `noticias/gpt-5-6-sol-ultra-codex`: Mesma dúvida do post gpt-5-6-sol-terra-luna-qual-usar: confirmar se o blockquote de atualização de preço antes do TL;DR é intencional. O callout canônico em si (logo após o TL;DR, apontando para /noticias/gpt-5-6-sol-terra-luna-qual-usar) está correto e único.

## 2. Título e meta das páginas de CTR baixo

Base: top queries reais do Search Console por página. Cada proposta passou por um refutador (keyword, clickbait, limites, voz da marca). Os cinco refutados foram só pelo bloco extra de body (repetia o TL;DR); título e meta foram aprovados e aplicados sem o bloco.

| post | título antes | título depois | query dominante |
|---|---|---|---|
| `gpt-5-6-sol-terra-luna-qual-usar` | GPT-5.6 Sol, Terra ou Luna: a diferença real e por que o Sol custa 25x mais que  | Diferença entre GPT-5.6 Sol, Terra e Luna: preço por tier e qual usar |  |
| `noticias/qwen-3-8-max` | Qwen 3.8 Max chegou: a Alibaba lançou um "Fable open source"? Benchmarks e prime | Qwen 3.8 Max (2.4T): benchmark vs Kimi K3, preço e pesos abertos | qwen 3.8 / qwen 3.8 max |
| `tutoriais/como-rodar-llm-local` | Como rodar um LLM local: guia do zero (Ollama, hardware e quando vale a pena) | Como rodar LLM local: passo a passo com Ollama em 2 comandos (sem GPU) | llm local / como rodar llm localmente |
| `noticias/claude-code-auto-mode-padrao` | Claude Code Auto Mode vira padrão dia 14: o que muda e como desativar | Auto Mode do Claude Code: o que é, como ativar/desativar, o que libera | auto mode claude |
| `tutoriais/5-padroes-prompt-code-review-llm` | 5 padrões de prompt que sobem o sinal do code review com LLM de 12% pra 67% | Prompt para code review: 5 padrões que sobem o sinal de 12% pra 67% | prompt para code review |
| `noticias/gpt-6-astra-vs-fable-5-1-vs-gpt-5-6-sol` | GPT-6 Astra vs Claude Fable 5.1 vs GPT-5.6 Sol: os números, o preço e o 99,9% qu | GPT-6 Astra vs Fable 5.1 vs GPT-5.6 Sol: o que é, preço e benchmarks | gpt astra / gpt 6 astra |
| `noticias/kimi-k3-benchmarks-vs-claude` | Kimi K3 chegou: o "Fable 5 chinês" que bate o Opus 4.8 — o que é real nos benchm | Kimi K3 preço: US$ 3/15 por milhão, tem grátis? Benchmarks vs Claude | kimi k3 preço |

No comparativo do GPT-6 Astra, além de title/meta, entrou uma linha após o TL;DR linkando o rastreador do OpenAI Astra (o link pro rastreador do GPT-6 já existia no corpo).

## 3. Redirect 301 para as remoções (código, não deployado)

O app não tinha mecanismo de redirect. Implementado em worktree separado, branch `feat/post-redirect-301` em `../blog-v2-bc-redirects` (o repo principal tem WIP não commitado em `main`, não foi tocado):

- migration `2026_09_14_000000_add_redirect_to_to_posts_table.php` (coluna `redirect_to` nullable)
- `Post` fillable + `PostController` devolve 301 quando `redirect_to` está preenchido, antes do 404 (funciona com o post em draft)
- `update-post` do MCP aceita `redirect_to` (só caminho interno, regex) e `get-post` expõe o campo
- `tests/Feature/Blog/PostRedirectTest.php` com 5 casos (draft+redirect, published+redirect, sem redirect, via MCP, URL externa rejeitada)

Não commitado e não testado: Docker/Sail estava fora. Receita de remoção depois do deploy: `update-post {slug, status: "draft", redirect_to: "/categoria/canonico"}` para cada um dos 6 posts da lista de remoção. Sitemap e feed já filtram por published, então o draft some deles sozinho.

## 4. Fora do alcance desta rodada

- Deploy do redirect e execução das 6 remoções: exige mexer em prod, aguarda autorização.
- Hub novo "Melhor IA para programar em 2026" (2.900 buscas/mês): pauta, não ajuste.
- CLS 0,26 no template do post do Kimi K3: correção no app (blade/CSS), não no conteúdo.
