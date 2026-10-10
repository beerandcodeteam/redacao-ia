# Pauta news-jacking — 27/07/2026 (publicar HOJE, horários escalonados)

Origem: `cacar-news-jacking` rodada em 27/07/2026 11:26 BRT. Três candidatos aprovados dos quatro do radar (o #4, Claude Cowork, ficou de fora desta leva).

Cuidado de agenda: o post do Jacquard já está agendado para 30/07/2026 — nenhum destes conflita.

## Claude Opus 5 fora do ar de novo: 4 incidentes em 48 horas (e um aberto agora)
- publicar_em: 2026-07-27T13:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Timeline dos incidentes de "elevated errors" do Claude Opus 5 desde o lançamento (24/07), com o feed oficial de status como fonte, e o playbook de resiliência para quem já apontou agente em produção pro modelo novo. VERIFICADO em `status.claude.com/history.rss` às 11:26 BRT de 27/07 — três incidentes nominais do Opus 5 só hoje (08:16–09:03 UTC resolvido, 11:27–11:47 UTC resolvido, e 13:39 UTC AINDA EM ABERTO, este último atingindo também o Haiku 4.5) mais um em 26/07 (10:34 UTC, resolvido). Contexto que evita o alarmismo: em 25/07 caíram também Fable 5, Mythos 5, Sonnet 5, Sonnet 4.6 e Haiku 4.5 — ou seja, não é defeito exclusivo do Opus 5, é a Anthropic sob carga. FORMATO VIVO: atualizar a timeline quando o incidente aberto for resolvido (e marcar a hora do "resolved" no post). Links internos: `claude-opus-5`, `claude-fable-5-vs-opus-4-8`, `claude-opus-4-8-producao-ia`.
- hook: Você apontou produção pro Opus 5 na sexta. Hoje ele já quebrou três vezes — e no momento em que este post subiu, o incidente ainda estava aberto. Não é azar: é o preço de ser early adopter, e dá pra se proteger dele.
- bullets:
  - A timeline hora a hora: os 4 incidentes do Opus 5 desde o lançamento
  - Não é só o Opus 5: o dia em que Fable, Mythos, Sonnet e Haiku caíram juntos
  - Por que todo modelo recém-lançado passa por isso (a conta de capacidade pós-launch)
  - O fallback silencioso pro Opus 4.8 e a instrução que limita subagents no Claude Code
  - Retry com backoff, fallback explícito e monitoramento: o checklist pra blindar seu agente
- keyword_principal: claude opus 5 fora do ar
- keywords_secundarias: claude fora do ar, claude opus 5 erro, claude opus 5 instável, opus 5 elevated errors, anthropic fora do ar
- tags: claude, anthropic, noticias, ai-agents, claude-code
- dificuldade: easy
- volume: "claude fora do ar" 2.400/mês BR (pico de 8.100 em junho), KD 1, intenção informacional, tendência anual +4.665%; a cauda "opus 5 fora do ar" é ~0 porque nasceu hoje. O padrão "fable 5 voltou" já rendeu 1.096 impressões no GSC — a demanda por status de modelo é provada. SERP atual só tem portais genéricos com incidentes de fevereiro, março, junho e 06/07: nenhum cobre o Opus 5.

## Kimi K3 liberou os pesos: o maior modelo aberto da história é de graça — mas roda em quê?
- publicar_em: 2026-07-27T16:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A Moonshot AI publicou os pesos abertos do Kimi K3 em 26/07/2026 (~19h30 EDT), um dia antes do fim do countdown que ela mesma anunciou. O post cobre o que exatamente foi liberado (licença, formato, onde baixar), o hardware que um MoE de 2,8T exige de verdade para inferência, a conta de rodar local versus a API a US$ 3/US$ 15 por milhão de tokens, e o que as sanções americanas alcançam (ou não) de quem baixa pesos no Brasil. VERIFICADO: release dos pesos e preço da API; confirmar no card do Hugging Face a licença e o formato antes de escrever. Não canibaliza `kimi-k3-benchmarks-vs-claude` (17/07, sobre benchmarks do lançamento) — este é sobre os pesos e o custo de rodar; obrigatório linkar os dois entre si. Links internos: `kimi-k3-benchmarks-vs-claude`, `sancoes-ia-chinesa-open-source`, `deepseek-v4-flash-local-5090`, `claude-opus-4-8-vs-minimax-m3-vs-qwen-3-local`.
- hook: O "Fable 5 chinês" agora é de graça: os pesos estão no ar, um dia antes do prometido. A pergunta que o hype não responde é a única que importa pra você: precisa de quantas GPUs pra dar um `docker run` nisso?
- bullets:
  - O que a Moonshot liberou de fato: licença, formato e onde baixar
  - 2,8 trilhões de parâmetros MoE: o hardware real pra inferência (spoiler: não é sua 4090)
  - Rodar local vs API a US$ 3/15: a conta pro dev solo e pra empresa brasileira
  - As sanções dos EUA mudam alguma coisa pra quem baixar os pesos daqui?
  - Quando pesos abertos desse porte fazem sentido — e quando é só troféu
- keyword_principal: kimi k3 pesos abertos
- keywords_secundarias: kimi k3 open weights, baixar kimi k3, rodar kimi k3 local, kimi k3 requisitos, kimi k3 download
- tags: kimi, moonshot-ai, modelos-open-source, llm, china
- dificuldade: medium
- volume: cauda ~0 BR (o termo nasceu ontem), mas o domínio já pinga forte no cluster: "kimi k3 preço" com 420 impressões na posição 7,0 e "kimi k3 vs claude" com 9 cliques/CTR 8,41% no GSC — quick win com janela aberta, sem cobertura PT-BR do release dos pesos.

## GPT-4o tem data pra morrer: 23 de outubro. O checklist pra migrar sem quebrar produção
- publicar_em: 2026-07-27T19:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: A página oficial de depreciações da OpenAI confirma que `gpt-4o-2024-05-13` e `gpt-4o-mini` são desligados em 23/10/2026, com migração recomendada para `gpt-5.6-sol` ou `gpt-5.6-terra`; e que as famílias legadas de áudio/realtime (`gpt-realtime`, `gpt-audio`, `gpt-4o-audio`, `gpt-realtime-mini`) morrem em 20/01/2027, avisadas em 20/07/2026. VERIFICADO em developers.openai.com/api/docs/deprecations. Diferencial editorial: portais gringos noticiaram como "descontinuação abrupta sem caminho de migração", o que é falso — o post corrige com a fonte primária e entrega o checklist técnico. Sinal de apoio: o OpenRouter removeu `openai/gpt-4o-mini-search-preview` do catálogo nas últimas 48h. Post de validade longa (a demanda por migração cresce até outubro). Links internos: `gpt-5-6-sol-terra-luna-qual-usar`, `gpt-5-6-sol-ultra-codex`, `gpt-6-lancamento-rastreador`.
- hook: O modelo que virou sinônimo de ChatGPT tem data marcada pra desligar. Se você tem `gpt-4o` hardcoded em algum lugar, o prazo é 23 de outubro — e a migração não é só trocar uma string no `.env`.
- bullets:
  - O que a OpenAI anunciou de verdade (e o que os portais inventaram de "abrupto")
  - As datas que importam: 23/10/2026 pro 4o e 4o-mini, 20/01/2027 pra áudio e realtime
  - Sol ou Terra? Pra onde migrar cada caso de uso — e o que muda no custo por token
  - O que quebra na migração: comportamento, latência e prompt calibrado no 4o
  - Checklist de migração em 6 passos pra não descobrir o desligamento em produção
- keyword_principal: gpt-4o descontinuado
- keywords_secundarias: fim do gpt-4o, gpt-4o desligado, migrar do gpt-4o, gpt-4o shutdown, gpt-4o para gpt-5.6
- tags: openai, chatgpt, modelos-de-ia, noticias
- dificuldade: easy
- volume: caudas ~0 BR (notícia de ontem), head "gpt-4o" com 1.900/mês e KD 17 — volume em queda natural (-84% no ano), mas a intenção de migração é nova e cresce até o shutdown. SERP sem material PT-BR com a fonte oficial.

---

## Atualizações de posts existentes (fora desta leva, sem pauta nova)

- `agente-openai-fugiu-sandbox-hugging-face` — acrescentar que a OpenAI levou cerca de uma semana para atribuir o hack ao próprio agente e que a Hugging Face passou a cobrar transparência publicamente (26/07).
- `gpt-6-lancamento-rastreador` — nova linha na timeline: briefing de Sam Altman à Casa Branca e ao Congresso sobre o próximo modelo (26/07).
- `kimi-k3-benchmarks-vs-claude` e `claude-opus-5` — nota curta no topo com link para os posts novos assim que publicarem.
