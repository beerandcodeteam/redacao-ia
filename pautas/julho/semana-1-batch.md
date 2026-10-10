# Batch julho semana-1 (30/jun) — entrada para criar-posts-batch.py
# Fonte: pautas/julho/semana-1.md (só os 3 posts; updates/descartados ficam fora)
# CTA fixo de todos os posts → https://beerandcode.com.br/landing-pages/do-prompt-ao-harness-construindo-um-agent-de-vendas
#   Inserir como bloco de fechamento (após a conclusão, antes do interlink final). Copy contextual por post no campo `cta`.

## Meta proibiu o Claude Code (e o Codex) dos próprios engenheiros — o que aconteceu
- publicar_em: 2026-07-01T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO (Crypto Briefing, Business Insider, 29/jun). A Meta restringiu o uso de Claude Code e Codex pelos seus engenheiros para proteger dados de treino de IA — no mesmo momento em que a comunidade no r/ClaudeAI levanta a tese de "telemetria/spyware" no Claude Code. Post explica o motivo real (vazamento de dado proprietário via agente), separa fato de boato e entrega o checklist do que isso significa pra quem usa coding agent em código fechado. Formato vivo: atualizar conforme Meta/Anthropic se pronunciarem.
- hook: A Meta gastou bilhões treinando IA — e acabou de proibir os próprios engenheiros de usar a IA dos concorrentes pra escrever código. Não é birra: é medo de vazar o que está dentro do repositório.
- bullets:
  - O que a Meta proibiu exatamente (Claude Code, Codex) e por quê — proteger dados de treino
  - "Spyware no Claude Code?": o que o agente realmente envia — fato vs boato (r/ClaudeAI)
  - O risco real: dados proprietários saindo do repo pelo prompt/contexto do agente
  - O que muda pra quem usa coding agent sob NDA, em código de cliente ou closed-source
  - Checklist: como blindar o setup (allowlist, sandbox, telemetria off) sem largar o agente
  - Interlink com claude-code-malware-repo-limpo e melhor-ia-para-programar-2026-claude-code-vs-codex
- keyword_principal: meta proíbe claude code
- keywords_secundarias: meta restringe codex, claude code dados de treino, claude code spyware, meta proíbe ia concorrente engenheiros, claude code é seguro empresa
- tags: ia, claude-code, codex, anthropic, seguranca-ia
- dificuldade: easy
- volume: ~0 BR (termo novo, KD não medido). Vence por velocidade (notícia de 29/jun) + janela totalmente aberta (SERP PT vazia) + pilar Claude Code, onde o domínio já tem 6+ posts e autoridade. Ângulo defensivo/governança segura tráfego depois da notícia (evergreen).
- cta: https://beerandcode.com.br/landing-pages/do-prompt-ao-harness-construindo-um-agent-de-vendas — Gancho: "Proibir é fácil; o difícil é construir um agente sob controle, com permissões e contexto que você manda." Convide o leitor que não quer só blindar, mas dominar a engenharia de agentes, a ver o passo a passo: **Do prompt ao harness: construindo um agent de vendas**.

## DeepSeek V4 vai custar por horário de pico: o preço peak/valley que muda a conta do open source
- publicar_em: 2026-07-02T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO no preview (HF/OpenRouter: V4-Pro 1,6T MoE, contexto 1M, ~US$0,44) + RUMOR de data ("mid-July" via KuCoin/flash). A novidade é o modelo de cobrança peak/valley (preço dinâmico por horário) anunciado pra V4. Post explica o que é o peak/valley, quanto fica mais barato rodar fora do pico, e faz a conta vs Claude Opus 4.8 pra dev BR. Formato vivo: confirmar data e tabela de preço no lançamento oficial.
- hook: O open source já alcançou o topo em código. Agora a DeepSeek quer te cobrar como conta de luz — barato de madrugada, caro no pico. Vale ajustar seu fluxo ao relógio?
- bullets:
  - O que é o preço peak/valley (dinâmico por horário) da DeepSeek V4
  - Quanto realmente custa rodar fora do pico vs Claude Opus 4.8 (conta em USD/BRL)
  - V4-Pro 1,6T MoE + contexto de 1M: o que muda pra coding agent
  - DeepSeek V4 é grátis? Onde roda (web, API, OpenRouter, self-host)
  - Quando lança de fato e o que ainda é rumor (separar VERIFICADO de boato)
  - Interlink com glm-5-2-open-source-melhor-codigo e claude-opus-4-8-vs-minimax-m3-vs-qwen-3-local
- keyword_principal: deepseek v4 preço
- keywords_secundarias: deepseek v4 quando lança, deepseek v4 pro preço, deepseek v4 peak valley, deepseek v4 é gratuito, deepseek v4 vs claude
- tags: ia, llm, deepseek, modelos-open-source, custos
- dificuldade: easy
- volume: head "deepseek v4" 3.600 BR / KD 5, mas a SERP do head já tem datacamp.com/pt e eigent.ai/pt + oficial/HF/r/brdev. Entrar pelo ângulo PREÇO/peak-valley/lançamento (cauda longa sem post PT — related searches "deepseek v4 quando lança", "deepseek v4 pro preço", "deepseek v4 é gratuito" provam demanda). Janela meia-aberta no head, aberta no ângulo de preço; decai quando o lançamento for oficializado.
- cta: https://beerandcode.com.br/landing-pages/do-prompt-ao-harness-construindo-um-agent-de-vendas — Gancho: "Escolher o modelo mais barato é a parte fácil — o que transforma um LLM num produto que fatura é a engenharia em volta dele." Leve o leitor que quer parar de comparar preço e começar a construir: **Do prompt ao harness: construindo um agent de vendas**.

## O modelo fantasma "owl-alpha" sumiu do OpenRouter — e era a LongCat-2.0 de 1,6 trilhão de parâmetros
- publicar_em: 2026-07-03T09:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: VERIFICADO pela comunidade (diff do catálogo OpenRouter + r/LocalLLaMA, 353↑): o modelo stealth que rodava como "owl-alpha" no OpenRouter sumiu e foi revelado como LongCat-2.0 — MoE de 1,6T de parâmetros totais (~48B ativados/token) da Meituan. Post conta a história do modelo-fantasma (como labs testam modelos disfarçados antes do anúncio), o que se sabe da arquitetura e benchmarks, e onde a LongCat-2.0 se encaixa na corrida open source chinesa (GLM 5.2, DeepSeek V4, Qwen). Formato vivo: detalhes oficiais da Meituan ainda saindo.
- hook: Por semanas um modelo anônimo chamado "owl-alpha" apareceu no OpenRouter e impressionou — depois sumiu do nada. O motivo: era a LongCat-2.0, e os labs testam modelos disfarçados na sua frente sem você saber.
- bullets:
  - O que é um "stealth model" e por que labs publicam modelos disfarçados (owl-alpha, "cloaked")
  - Como a comunidade desmascarou: o diff do OpenRouter + o anúncio no r/LocalLLaMA
  - LongCat-2.0 por dentro: MoE 1,6T total / ~48B ativados, e quem é a Meituan
  - Onde ela entra na corrida open source chinesa: vs GLM 5.2, DeepSeek V4 e Qwen
  - Vale testar? Onde roda hoje e o que ainda falta a Meituan confirmar
  - Interlink com glm-5-2-open-source-melhor-codigo e o post de DeepSeek V4
- keyword_principal: longcat 2.0
- keywords_secundarias: owl-alpha openrouter, longcat meituan, modelo stealth openrouter, longcat llm, modelo fantasma openrouter
- tags: ia, llm, modelos-open-source, china, openrouter
- dificuldade: easy
- volume: ~0 BR — "longcat 2.0" / "owl-alpha" / "longcat llm" sem dado no DataForSEO (termos recém-nascidos; o vol 4.400 de "longcat" é o MEME do gato, não o modelo — ignorar). Keyword virgem + SERP PT vazia = janela aberta pura. Vence por velocidade (sinal de ouro do OpenRouter diff) + ângulo "modelo fantasma" com gancho de mistério/CTR. Menor prioridade dos 3 (nicho), mas zero concorrência.
- cta: https://beerandcode.com.br/landing-pages/do-prompt-ao-harness-construindo-um-agent-de-vendas — Gancho: "Tem modelo novo toda semana; o que vira produto não é o modelo, é o harness em volta dele." Convide quem se empolgou com a corrida de modelos a aprender a parte que dá dinheiro: **Do prompt ao harness: construindo um agent de vendas**.
