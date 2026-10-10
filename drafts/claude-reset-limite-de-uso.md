O reset do Claude é um botão que devolve o seu limite de uso ao máximo na hora, de graça. Chama **Reset for free**, a Anthropic colocou um na conta de cada assinante em setembro e ele expira em **22 de outubro de 2026**.

O cenário em que ele salva: quarta-feira, meio da tarde, o Claude avisa que o limite semanal acabou. O contador só volta no domingo. Você tem um deploy na sexta.

Pouca gente abriu a tela onde esse botão mora. Neste post: onde clicar, o que o reset zera de verdade, o que não zera e qual é o melhor momento pra gastar o seu.

## TL;DR

- **O que é:** um reset de limite de uso do Claude que fica guardado na conta e você dispara quando quiser.
- **Quem tem:** assinantes Pro, Max, Team e Enterprise por assento. Plano Free e uso por API ficam de fora.
- **Onde fica:** Settings > Usage > Resets, no navegador ou no Claude Desktop. Atalho: `clau.de/reset`.
- **Custo:** zero. É um por conta e não dá pra desfazer.
- **Prazo:** expira em 22 de outubro de 2026.

## O que é o reset que a Anthropic liberou

Até agosto, reset de limite era coisa que acontecia com você. A Anthropic decidia o dia, zerava o contador de todo mundo ao mesmo tempo e avisava no X. O [rastreador claude-resets.com](https://claude-resets.com/) conta 14 desses desde abril de 2026, um a cada 12 dias em média. Virou evento a ponto de ter [mercado de aposta no Polymarket](https://polymarket.com/event/anthropic-resets-claude-usage-limit-by-20260908) sobre a data do próximo.

O problema do reset global é óbvio: ele cai quando a Anthropic quer, não quando você precisa. Se o seu contador estava em 10%, você não ganhou nada.

Junto com o lançamento do Opus 5.5, na virada de 21 para 22 de setembro, o formato mudou. Em vez de zerar todo mundo, a Anthropic colocou um reset na conta de cada assinante. A [central de ajuda](https://support.claude.com/en/articles/17007452-what-is-a-limit-reset) define assim: uma concessão ocasional para planos elegíveis que devolve seus limites ao máximo "quando você escolher usar".

O contexto ajuda a ler o gesto. Uma semana antes, em 14 de setembro, o bônus de 50% no limite semanal do Claude Code tinha virado 25% permanente, o que na prática foi um [corte de 17% sobre o que estava valendo](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-is-cutting-claude-codes-current-weekly-limits-by-17-percent/). O reset guardável chegou logo depois.

Agora, uma coisa precisa ser dita. Limite estourado é o sintoma que aparece na tela. A causa quase sempre é contexto inchado, agente rodando em loop e modelo caro fazendo tarefa barata. Um botão resolve a quarta-feira; saber onde os tokens estão indo resolve o mês, e essa é a diferença entre usar IA e construir com IA que a gente pratica toda semana, ao vivo, no [Clã Beer and Code](https://beerandcode.com.br?utm_source=blog&utm_medium=post&utm_campaign=claude-reset-limite-de-uso&utm_content=a-n1).

## Como usar o reset do Claude

São quatro cliques.

1. Abra o Claude no navegador ou no app desktop.
2. Vá em **Settings > Usage**.
3. Ache a seção **Resets**.
4. Clique em **Reset for free** e confirme clicando de novo.

O atalho direto é este:

```text
https://clau.de/reset
```

O mesmo botão aparece na mensagem de limite atingido. E você não precisa ter batido o limite pra usar.

Atenção se você vive no terminal: o botão **não existe no Claude Code nem no app mobile**. Só web e desktop. Mas o limite é um só por conta. Resetou no navegador, voltou a valer no Claude Code e no celular na mesma hora.

## O que o reset zera (e o que não zera)

Aqui mora a confusão. A documentação oficial diz que o reset recarrega **o limite de sessão de cinco horas ou o limite semanal**, "dependendo do reset exibido". Um dos dois. Qual deles você recebeu está escrito em Settings > Usage.

Parte da imprensa reportou diferente. A [XDA](https://www.xda-developers.com/claude-now-lets-you-manually-trigger-your-own-weekly-reset/) descreveu o botão como um reset semanal que também limpa a janela de cinco horas. Na dúvida, vale o que está na sua tela, não o que está no artigo de alguém.

O que ele não faz:

- **Não muda o seu ciclo semanal.** O contador continua virando no mesmo dia e na mesma hora de sempre.
- **Não devolve dinheiro.** Uso extra já cobrado continua cobrado e o saldo de créditos não muda.
- **Não tem volta.** Clicou, gastou.
- **Não sobrevive a downgrade.** Cancelou ou baixou de plano antes de usar, o reset some.

## Quando gastar: a conta do timing

É um só. Gastar errado é o único jeito de perder.

**Se o seu reset é semanal**, ele vale tanto quanto os dias que faltam pro seu ciclo virar. Bateu o teto com quatro dias pela frente? Você compra quatro dias de trabalho. Bateu na véspera da virada? Compra algumas horas de algo que ia voltar sozinho.

**Se o seu reset é de sessão**, a conta muda. A janela de cinco horas volta sozinha em no máximo cinco horas, então só compensa quando esperar custa caro: demo ao vivo, incidente em produção, entrega no mesmo dia. E lembre que encher a sessão de novo faz você comer o limite semanal mais rápido.

**A regra do prazo:** se chegar 21 de outubro e o reset ainda estiver lá, use. Reset expirado vale menos que reset mal gasto.

## E o /limit-reset do Claude Code?

É outra coisa. No começo de setembro apareceu no Claude Code um comando `/limit-reset`, sem anúncio. Segundo [quem dissecou o comando](https://www.thinkfacility.com/blog/claude-code-limit-reset/), ele zera só a janela de cinco horas, pode ser usado uma vez por semana e avisa na própria resposta que o limite semanal continua valendo.

O ponto fraco: não está documentado oficialmente e nem toda conta recebe. Pode mudar ou sumir sem aviso. Trate como bônus, não como plano.

## Limitações e pontos de atenção

A palavra que a Anthropic usa é "ocasional". Não existe regra publicada de frequência, nem critério de quem recebe, nem promessa de que vem outro depois de 22 de outubro. Não dá pra montar o fluxo do time contando com isso.

O reset também não mexe no tamanho do limite. Ele enche de novo o mesmo balde. Se você estoura toda semana, a discussão é outra, e passa pelo [processo que acusa o Max 20x de entregar 6x](https://blog.beerandcode.com.br/noticias/claude-max-20x-limite-processo) e pela [guerra de limites entre Codex e Claude Code](https://blog.beerandcode.com.br/noticias/codex-limite-de-uso).

Em plano Team e Enterprise, confira na sua própria conta antes de prometer qualquer coisa pro time. O reset é por usuário, não por organização.

## FAQ

### O reset do Claude funciona no Claude Code?

Funciona, mas você não dispara por lá. O botão só existe na web e no Claude Desktop. Como o limite é compartilhado na conta, depois do clique o Claude Code volta a responder normalmente.

### O reset zera o limite semanal e o de cinco horas?

Segundo a documentação oficial, um ou outro, dependendo do reset que aparece na sua conta. Confira em Settings > Usage antes de clicar.

### Dá pra guardar o reset pra depois de 22 de outubro?

Não. O que não for usado até a data mostrada na oferta expira.

### Quem está no plano Free recebe?

Não. O reset foi liberado para Pro, Max, Team e Enterprise por assento.

## Conclusão

A Anthropic trocou o reset que cai do céu por um que fica no seu bolso. É uma mudança pequena e boa: quem decide a hora agora é você. Só que é um, tem data pra morrer e não conserta consumo ruim.

Abra Settings > Usage hoje, veja qual reset você tem e decida o momento com a conta na mão. A aposta razoável é que esse formato volte a cada lançamento grande de modelo, mas é aposta, não promessa.

E se o limite é visita frequente por aí, o próximo passo é atacar a causa: [como economizar tokens no Claude Code, Codex e Cursor](https://blog.beerandcode.com.br/tutoriais/como-economizar-tokens-claude-code-codex-cursor).
