# Batch semana-5 (29/jun) — entrada para criar-posts-batch.py
# Fonte: pautas/junho/semana-5.md (só os 2 posts; updates/descartados ficam fora)

## Claude Code enganado a instalar malware: como o ataque do repo "limpo" funciona (e como blindar seu setup)
- publicar_em: 2026-06-29T18:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: O time 0din da Mozilla mostrou que dá pra esconder instruções maliciosas dentro de um repositório GitHub aparentemente limpo e fazer o Claude Code (e outros coding agents) instalar malware sozinho — explorando a própria prestatividade do agente. VERIFICADO (Tom's Hardware, Slashdot, demo do 0din). Post explica o vetor de ataque passo a passo, conecta com o caso do usuário cujo Claude Code tentou abrir um Remote Desktop, e entrega um checklist defensivo prático. Formato vivo: atualizável conforme a Anthropic responder.
- hook: Seu agente de código confia em tudo que lê no repositório — e é exatamente por isso que ele pode ser enganado. Um README "limpo" foi suficiente pra transformar o Claude Code em vetor de malware.
- bullets:
  - O que o 0din da Mozilla demonstrou: prompt injection escondido em arquivo de repo comum
  - Por que a "prestatividade" do agente é o próprio buraco de segurança (não é bug, é design)
  - O caso real: Claude Code tentando abrir Remote Desktop num PC e o que isso revela
  - Coding agents afetados além do Claude Code (Codex, Cursor) e o que muda no seu fluxo
  - Checklist de blindagem: permissions, allowlist, sandbox, revisão de repos de terceiros
  - Interlink com claude-code-o-que-e-como-funciona e claude-code-hooks-slash-commands-mcp
- keyword_principal: claude code malware
- keywords_secundarias: claude code é seguro, claude code segurança, prompt injection claude code, claude code vulnerabilidade, coding agent malware
- tags: ia, claude-code, anthropic, seguranca-ia, prompt-injection
- dificuldade: easy
- volume: ~0 BR, KD não medido (termo novo). Vale pela janela: SERP em PT vazia (só TecMundo cobrindo um incidente antigo de abril/2026), pilar Claude Code onde o blog já tem 6 posts e autoridade, e ângulo defensivo evergreen que segura tráfego depois da notícia.

## Fable 5 vai voltar? EUA recuam e a liberação do modelo da Anthropic está perto — o que se sabe
- publicar_em: 2026-06-29T20:00:00-03:00
- autor: lucas-souza-virgu
- categoria: noticias
- resumo: Depois de mandar a Anthropic desligar o Fable 5 e o Mythos para estrangeiros, o governo dos EUA está recuando: o Trump derrubou parte do ban (WSJ), Axios/Reuters dizem que a liberação do Fable 5 está próxima e o Mythos já foi liberado a "trusted partners". Em paralelo, a Áustria pressiona a UE pra hospedar a Anthropic na Europa. Post responde a pergunta que o BR está buscando ("Fable 5 voltou?") com o status real, marcando o que é VERIFICADO (recuo em andamento, fontes Axios/Reuters/WSJ) vs o que ainda NÃO está consumado. Formato vivo: atualiza conforme a liberação se confirmar.
- hook: Você tentou usar o Fable 5 e bateu num "indisponível na sua região"? A boa notícia: os EUA estão recuando e a liberação está perto. A má: "perto" ainda não é "agora". O que mudou nas últimas 48h.
- bullets:
  - O recuo: o que o Trump derrubou do ban (WSJ) e o que ainda continua valendo
  - "Close to restore": o que Axios/Reuters realmente disseram (e o que NÃO disseram)
  - Mythos liberado a "trusted partners" — quem entra nessa lista e quem fica de fora
  - A jogada da Áustria: por que a UE quer hospedar a Anthropic e o que isso muda
  - O que isso significa pra dev no Brasil: quando você volta a ter acesso (cenários)
  - Interlink obrigatório com anthropic-acesso-bloqueado-brasil (o post do bloqueio) e fable-5-bloqueado-openrouter-fusion
- keyword_principal: fable 5 voltou
- keywords_secundarias: fable 5 liberado, fable 5 vai voltar, fable 5 volta quando, anthropic liberada, fable 5 retorno
- tags: ia, llm, anthropic, fable-5, mythos, export-controls
- dificuldade: easy
- volume: ~0 BR (termo recém-nascido), mas demanda PROVADA na GSC: "fable 5 voltou" / "fable 5 volta quando" / "claude fable vai voltar?" / "fable 5 liberado" (pos 18) / "fable 5 retorno" (pos 20) já pingam SEM post dedicado. Quick win de intent novo, distinto do post de bloqueio. Janela curta: decai quando a liberação for oficializada.
