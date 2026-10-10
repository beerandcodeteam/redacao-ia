# DRAFT NÃO PUBLICADO — duplicata detectada no gate de SEO

> Gerado em 2026-07-25 pelo pipeline `criar-post-blog` (modo batch).
> **NÃO foi enviado ao MCP**: já existe o post `jacquard-linguagem-programacao-codigo-ia`
> (mesmo tema, agendado para 2026-07-30T09:00:00-03:00, criado em 24/07 22:54).
> Assets desta sessão (reutilizáveis):
> - Capa: https://grcgbsnjuagf.objectstorage.sa-saopaulo-1.oci.customer-oci.com/n/grcgbsnjuagf/b/site-assets/o/posts/cover-jacquard-linguagem-codigo-ia.png
> - Áudio (voz Lucas, OmniVoice): https://grcgbsnjuagf.objectstorage.sa-saopaulo-1.oci.customer-oci.com/n/grcgbsnjuagf/b/site-assets/o/posts/audio/jacquard-linguagem-codigo-ia.mp3
> - Roteiro de narração: /tmp/audio-script-jacquard-linguagem-codigo-ia.txt (3100 palavras)
> ⚠️ O áudio foi narrado a partir do body DESTE draft, não do body do post já agendado.

## Campos

- title: Jacquard: a linguagem para código escrito por IA e revisado por humanos
- slug: jacquard-linguagem-codigo-ia
- category_slug: noticias
- author_slug: lucas-souza-virgu
- published_at: 2026-07-25T09:00:00-03:00
- tags: ai-agents, agentic-code, code-review, seguranca-ia, engenharia-de-software
- meta_title: Jacquard: a linguagem para código escrito por IA
- meta_description: Conheça Jacquard, a linguagem para código escrito por IA: efeitos declarados na assinatura da função e permissões explícitas no runtime.
- excerpt: A IA escreve, você revisa — mas o diff não mostra o que o código pode tocar. Jacquard, linguagem que subiu ao topo do Hacker News, coloca os efeitos na assinatura da função e nega tudo por padrão no runtime. Entenda o effect system, a identidade content-addressed e o que isso sinaliza pro futuro do code review de código gerado por IA.

## Body

Seu code review de código gerado por IA tem um problema: você lê o diff, mas não vê o que aquele código pode tocar. A função parece inofensiva. Os testes passam. E nada na assinatura te diz se, três chamadas abaixo, ela abre conexão de rede, escreve em disco ou lê variável de ambiente.

[Jacquard](https://github.com/jbwinters/jacquard-lang) nasceu pra atacar exatamente isso. É uma linguagem de pesquisa criada para um regime bem específico: aquele em que "a maior parte do código é escrita por modelos de machine learning e revisada por pessoas", nas palavras do próprio README. Se quem escreve mudou, a linguagem precisa mudar junto. E a primeira mudança é essa: a função declara, na assinatura, quais efeitos externos ela pode causar — e o runtime recusa qualquer efeito que você não autorizou.

Neste post você vai entender como funciona o effect system do Jacquard, por que isso muda o code review de código gerado por IA, o que a identidade content-addressed resolve em pipelines com agentes, e onde o protótipo ainda não chega.

## TL;DR

- **O que é:** linguagem de pesquisa para código escrito por IA e revisado por humanos, com efeitos explícitos na assinatura da função e permissões controladas no runtime.
- **Stack:** implementada em OCaml; roda interpretada ou compila binário nativo via C; dois formatos — `.jac` (superfície legível) e `.jqd` (kernel de 27 formas).
- **Custo/Acesso:** open source, Apache 2.0. Versão 0.1 (release candidate) — protótipo de pesquisa, não linguagem de produção.
- **Repositório:** [github.com/jbwinters/jacquard-lang](https://github.com/jbwinters/jacquard-lang)

## Por que uma linguagem desenhada pra IA importa

Toda linguagem que você usa hoje foi desenhada com uma premissa implícita: quem escreve o código é quem entende o código. Python, JavaScript, PHP, Go — todas otimizam a escrita. Legibilidade, expressividade, produtividade de quem digita.

Só que essa premissa quebrou. Com agentes escrevendo cada vez mais código, o gargalo saiu da escrita e foi pra revisão. Você não digita mais a maior parte das linhas — você audita. E auditar num diff é péssimo: o diff mostra o que mudou, não o que o código alcança.

O Jacquard parte dessa inversão. Foi apresentado num [Show HN em julho](https://news.ycombinator.com/item?id=48894630) que somou 102 pontos e rendeu uma discussão boa sobre até onde uma linguagem nova consegue competir com o corpus gigante de Python e JavaScript. A tese do autor: pra código gerado por IA, o que importa não é ergonomia de escrita. É verificabilidade de leitura.

Essa é a mesma virada que separa usar IA de construir software com IA — e treinar essa segunda habilidade, toda semana, junto com outros devs, é o que a gente faz no [Clã Beer and Code](https://beerandcode.com.br?utm_source=blog&utm_medium=post&utm_campaign=jacquard-linguagem-codigo-ia&utm_content=a-n1).

## A função que declara o que pode tocar

O coração do Jacquard é a linha de efeitos na assinatura. Assim:

```text
normalize-name : (text) ->{net} text
```

Lê-se: recebe texto, devolve texto, e pode fazer rede. Só rede. Se essa função tentar escrever em disco, não compila. E os efeitos se propagam sozinhos pelo call graph: se `a` chama `b` e `b` faz `{fs}`, o `{fs}` sobe pra assinatura de `a` sem anotação manual.

A segunda metade é o runtime. Declarar não basta — tem que autorizar:

```bash
jac run programa.jac --allow net
```

O runtime recusa qualquer efeito que não foi concedido na linha de comando. Vale até pra código carregado dinamicamente. Isso é capability-based security embutida na linguagem: em vez de confiar que o código se comporta, você concede autoridade explícita, e o resto é negado por padrão.

Compara com o que você faz hoje pra rodar código de agente: sandbox, container, firewall de saída. Tudo por fora do processo, tudo no nível do processo inteiro. No Jacquard a fronteira é por função, e aparece no lugar onde o review acontece: a assinatura.

Tem um bônus grande pra teste. Os efeitos são implementados como efeitos algébricos com handlers — então dá pra trocar o handler de `net` por um fake e testar hermeticamente código que fala com o mundo, sem mock framework, sem monkey patch. Foi um dos pontos mais elogiados na thread do HN.

## Hash do significado, não do texto

Segunda ideia forte: identidade content-addressed. O Jacquard não faz hash dos bytes do arquivo — faz hash da estrutura canônica resolvida do programa. Renomear variável, reformatar, reordenar imports: nada disso muda a identidade.

Parece detalhe. Não é. Agente de IA renomeia e reformata o tempo todo. Num pipeline em que cada mudança de byte invalida cache e re-roda suíte de teste, o loop do agente fica caro. Se a identidade é semântica, refactor cosmético não recompila nem re-testa nada. Quem conhece [Unison](https://www.unison-lang.org/) reconhece a ideia — o Jacquard aplica ela ao cenário de código gerado.

E tem a decisão mais explícita de design pra agentes: o kernel `.jqd` tem 27 formas fixas. Deliberadamente pequeno pra que um modelo sem nenhum Jacquard no corpus de treino consiga trabalhar a partir de um único arquivo de especificação.

## Rodando na prática

Binário pré-compilado pra Linux x86-64 e macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/jbwinters/jacquard-lang/jacquard-core-0.1-rc3/scripts/install.sh | sh
```

Os três comandos do dia a dia:

```bash
jac check programa.jac              # typecheck + inferência de efeitos
jac run programa.jac --allow net    # roda com permissões explícitas
jac build programa.jac -o app       # compila binário nativo
```

O binário compilado produz saída byte-idêntica ao `jac run` — o que importa se você quiser assinar e verificar artefatos gerados por agente.

## Limitações e pontos de atenção

Sejamos claros: é protótipo de pesquisa, versão 0.1. O próprio README avisa que funciona ponta a ponta mas não é linguagem de produção. Não tem VM nem JIT, não tem gerenciador de pacotes, não tem provas formais de soundness.

Os pontos mais duros da discussão no HN:

- **Multi-shot handlers são difíceis de revisar.** O Jacquard permite handlers que retomam a continuação várias vezes — poderoso pra busca exaustiva e inferência probabilística, mas brutal pra um humano raciocinar. O autor reconheceu a crítica e disse que trabalha na distinção entre handlers one-shot e multi-shot.
- **Cold start de corpus.** "Qualquer LLM que você tentar usar com ela vai começar do zero", resumiu um comentário. O kernel pequeno é a aposta contra isso, mas a vantagem de Python e JavaScript em dados de treino é real.
- **Effect system não é novidade.** Koka, Flix e Eff exploram efeitos há anos; Unison faz hashing de AST. A novidade do Jacquard é o pacote fechado apontado pro regime IA-escreve-humano-revisa.

## FAQ rápido

**Posso usar Jacquard em produção?**
Não. É pesquisa, versão 0.1. Use pra estudar as ideias — effect rows, capabilities, identidade semântica — que provavelmente vão aparecer em linguagens de produção nos próximos anos.

**Preciso saber OCaml?**
Não. OCaml é a linguagem de implementação do compilador. Você escreve `.jac` e usa o binário `jac`.

**Sandbox e container já não resolvem isso?**
Resolvem outra camada. Container limita o processo inteiro, por fora, e não aparece no code review. Effect row limita por função e fica visível exatamente onde o revisor olha: a assinatura.

**Qual a diferença pra Rust?**
Rust rastreia memória e ownership — te diz quem pode mutar o quê. Não te diz se a função abre socket. São eixos ortogonais: dá pra imaginar as duas coisas na mesma linguagem.

## Conclusão

O Jacquard em si talvez nunca chegue em produção — e tudo bem. O que importa é a pergunta que ele responde: quando a IA escreve e o humano revisa, o que a linguagem deve mostrar primeiro? A resposta dele — efeitos na assinatura, autoridade negada por padrão, identidade semântica — é um mapa do que vem por aí. Se o seu review de código de agente hoje se resume a ler diff e torcer, vale rodar os demos do [repositório](https://github.com/jbwinters/jacquard-lang) e sentir como é revisar código que declara o que pode tocar.
