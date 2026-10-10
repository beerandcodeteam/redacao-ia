# Watchlists e fontes

O `detect.sh` já cobre as APIs (HN, OpenRouter, Polymarket, GitHub, Reddit, NewsAPI/GDELT).
As fontes abaixo são complementos que o agente busca via `WebFetch` no passo 1 da skill, ou parâmetros editáveis do script.

## RSS / blogs oficiais dos labs (WebFetch no passo 1)

Anúncio oficial é o gatilho mais forte de news-jacking. Use `WebFetch` pedindo "os posts/notas das últimas {HORAS}h e o que mudou":

- OpenAI News — https://openai.com/news/
- Anthropic News — https://www.anthropic.com/news
- Google DeepMind blog — https://deepmind.google/discover/blog/
- Google AI / Gemini — https://blog.google/technology/ai/
- Mistral AI news — https://mistral.ai/news/
- Meta AI blog — https://ai.meta.com/blog/
- OpenRouter announcements — https://openrouter.ai/announcements
- Hugging Face blog — https://huggingface.co/blog
- Simon Willison (ótimo curador de lançamentos) — https://simonwillison.net/

## Polymarket — odds/data de lançamento (WebFetch sob demanda)

A API do Polymarket **não** expõe os mercados de IA de forma confiável (por isso saiu do `detect.sh`). Quando um rumor de lançamento aparecer, busque a página do evento via `WebFetch` pra extrair a probabilidade/data — ex.: pesquise "polymarket gpt-5.6" ou acesse o evento direto:
- Busca de eventos — https://polymarket.com/markets/ai (filtrar por modelo/empresa)
- Ou via WebSearch "polymarket <modelo> release" e WebFetch na página do evento.

## Subreddits monitorados (no detect.sh, editável)

`LocalLLaMA` · `ClaudeAI` · `OpenAI` · `singularity` · `ArtificialInteligence` · `MachineLearning`
(adicionar/remover na lista `for sub in ...` do script.)

## Repos GitHub monitorados (no detect.sh, editável)

`ggml-org/llama.cpp` · `ollama/ollama` · `vllm-project/vllm`
(suporte a um modelo novo nesses repos costuma anteceder a cobertura em PT-BR.)

## Foco/keywords default (no detect.sh, sobrescreve com -q)

`GPT-5 OR GPT-5.6 OR Claude OR Fable OR "Gemini 3" OR OpenAI OR Anthropic OR LLM OR Codex OR DeepSeek OR Qwen OR Mistral OR Llama`

Ajuste por sessão: `detect.sh -q "claude OR anthropic OR fable"`.

## Ângulos que mais convertem no blog (histórico)

- **Modelo bloqueado/liberado no OpenRouter** (ex.: `fable-5-bloqueado-openrouter-fusion`, CTR 6,23%) — o diff do OpenRouter no detect.sh dispara isso sozinho.
- **X vs Y** entre modelos (ex.: `claude-fable-5-vs-opus-4-8`, 50 cliques/1005 imp).
- **Rumor/tracker de lançamento** (data + specs vazadas), marcando fato vs boato.
- **"O que os americanos estão fazendo com X"** — curadoria de HN/Reddit logo após lançamento.
