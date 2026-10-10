# Setup: credenciais, MCPs e ferramentas externas

Tudo que o pipeline precisa para rodar em uma máquina nova. Nenhum valor real mora no repositório: os modelos são `.env.example` e `.mcp.json.example`.

## Ferramentas de sistema

| ferramenta | usada por | nota |
|---|---|---|
| [Claude Code](https://claude.com/claude-code) (`claude`) | tudo | as skills em `.claude/skills/` são carregadas ao abrir a sessão na raiz do repo |
| `jq`, `curl` | `detect.sh`, `generate-cover.sh` | o detector aborta sem eles |
| `python3` (3.12) | scripts, painel SEO, TTS | |
| `ffmpeg` | `generate-audio.sh` | converte WAV em MP3 |
| `aws` CLI v2 | `generate-cover.sh`, `generate-audio.sh` | fala com o storage pela API S3-compatible |
| `pipx` | MCP `analytics-mcp` | `pipx run analytics-mcp` |
| `uv` / `uvx` | MCP `gscServer` | `uvx mcp-search-console` |
| `gcloud` | credencial do GA4 (ADC) | instale fora do repo |

## Variáveis de ambiente (`.env`)

Copie `.env.example` para `.env`. Os scripts `.sh` fazem `source` do arquivo, então **valor com espaço precisa de aspas** (o `REDDIT_USER_AGENT` sem aspas quebra o `generate-cover.sh` com `by: command not found`).

| variável | serviço | onde conseguir | quem lê |
|---|---|---|---|
| `GEMINI_API_KEY` | Gemini API | [Google AI Studio](https://aistudio.google.com/apikey) | `generate-cover.sh` |
| `OCI_ACCESS_KEY_ID`, `OCI_SECRET_ACCESS_KEY` | OCI Object Storage | Customer Secret Key do usuário OCI | `generate-cover.sh`, `generate-audio.sh` |
| `OCI_BUCKET`, `OCI_ENDPOINT`, `OCI_URL` | idem | console do bucket | idem |
| `OCI_NAMESPACE`, `OCI_REGION` | idem | console OCI | referência (compõem endpoint e URL) |
| `BLOG_MCP_TOKEN` | MCP do blog | gerado no app do blog | referência (o valor em uso fica no `.mcp.json`) |
| `DATAFORSEO_USERNAME`, `DATAFORSEO_PASSWORD` | DataForSEO | [painel da API](https://app.dataforseo.com/api-access) | `seo-report/generate.py` |
| `PAGESPEED_API_KEY` | PageSpeed Insights | Google Cloud, chave restrita à PageSpeed Insights API | `seo-report/generate.py` |
| `GA4_PROPERTY_ID`, `GA4_SITE_PROPERTY_ID` | Google Analytics 4 | Admin > Property settings (ID numérico do blog e do site principal) | `seo-report/generate.py`, skills `planejar-pauta`, `minerar-evergreen`, `cacar-news-jacking` |
| `GITHUB_TOKEN` | GitHub | PAT read-only | `detect.sh` (opcional) |
| `NEWSAPI_KEY` | NewsAPI | [newsapi.org](https://newsapi.org) | `detect.sh` (opcional; sem ela usa GDELT) |
| `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT` | Reddit | app em reddit.com/prefs/apps | `detect.sh` (opcional; sem elas usa RSS) |

O storage é qualquer um compatível com S3. O projeto usa OCI Object Storage com bucket de leitura pública; para trocar por S3, R2 ou MinIO basta ajustar `OCI_ENDPOINT` e `OCI_URL`.

O detector também carrega `$NEWSJACK_ENV` e `~/.claude/newsjack.env`, caso você prefira manter as chaves das fontes fora do projeto.

## Credenciais do Google

Ficam **fora do repositório**, no diretório de config do usuário.

**GA4 (Application Default Credentials).** Usada pelo MCP `analytics-mcp` e pelo painel SEO:

```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform
# grava ~/.config/gcloud/application_default_credentials.json
```

A conta precisa de acesso de leitura à propriedade do GA4, e o projeto GCP precisa da Google Analytics Data API habilitada.

**Search Console (OAuth).** Crie um OAuth Client ID do tipo "Desktop app" no Google Cloud, habilite a Search Console API, baixe o `client_secret_*.json` e guarde em `~/.config/mcp-gsc/`. Aponte `GSC_OAUTH_CLIENT_SECRETS_FILE` para ele no `.mcp.json`. Na primeira chamada o MCP abre o navegador e grava o token em `~/.config/mcp-gsc/token.json`, que o painel SEO reaproveita.

## Servidores MCP do projeto (`.mcp.json`)

Copie `.mcp.json.example` para `.mcp.json` e preencha. São quatro:

| server | transporte | autenticação | usado por |
|---|---|---|---|
| `beer-and-code-blog` | HTTP | `Authorization: Bearer <token>` | `criar-post-blog`, `revisar-seo-post`, dedup nas skills de pauta |
| `gscServer` | stdio (`uvx mcp-search-console`) | OAuth, arquivo de client secret | `planejar-pauta`, `minerar-evergreen`, `cacar-news-jacking` |
| `analytics-mcp` | stdio (`pipx run analytics-mcp`) | ADC do gcloud | `planejar-pauta` |
| `dfs-mcp` | HTTP (`https://mcp.dataforseo.com/v3/mcp`) | `Authorization: Basic <base64 de login:senha>` | as três skills de pauta e a auditoria opcional pós-publicação |

Para gerar o header do DataForSEO:

```bash
printf '%s' 'login:senha' | base64
```

Duas particularidades que as skills já tratam, mas vale conhecer:

- O `dfs-mcp` é um gateway genérico: não há uma tool por endpoint, tudo passa por `api_request` com `method`, `path` e `data` (sempre array). As tools são *deferred* no Claude Code, então a primeira chamada precisa de um `ToolSearch` antes.
- As chamadas ao DataForSEO são pagas. As skills filtram no servidor e agrupam keywords em lote; a seção "Custo" de cada `SKILL.md` explica o que encarece.

### MCP do blog

É o único componente que não vem de terceiros: um servidor MCP HTTP exposto pelo próprio app do blog (Laravel). Para usar este pipeline com outro CMS, exponha um servidor com o mesmo contrato:

| tool | papel no pipeline |
|---|---|
| `list-categories`, `list-authors`, `list-tags` | escolher categoria e autor, reaproveitar tags |
| `create-tag`, `create-category` | só quando faltar |
| `upload-image` | recebe a URL pública da capa, devolve o `path` |
| `create-post` | cria o post (`title`, `body` em Markdown, `category_slug`, `author_slug`, `published_at`, `tags`, `excerpt`, `cover_image_path`, `audio_url`, `meta_*`); o default é agendado |
| `enrich-post` | gera `meta_title`, `meta_description` e tags quando não foram enviados |
| `update-post`, `get-post`, `list-posts` | edição, dedup anti-canibalização e link interno |
| `publish-post` | só com OK explícito |
| `upsert-post-translation`, `list-events`, `create-event`, `update-event`, `search-file-storage` | traduções, eventos e base de conhecimento |

Limitações conhecidas do servidor, que a `revisar-seo-post` corrige antes de chamar: travessão (`—`) em `meta_description`, `meta_description` acima de ~155 caracteres e símbolos Unicode como `≠` em `title` ou `slug` derrubam a chamada com o erro genérico `-32603`.

## MCPs e plugins de apoio (opcionais)

Não fazem parte do pipeline de post. São configurados no nível do usuário (`claude mcp add`) e aparecem no trabalho do dia a dia neste repositório:

| MCP | uso aqui |
|---|---|
| [Context7](https://context7.com) | documentação atualizada de libs e SDKs durante a pesquisa de um post técnico |
| [Higgsfield](https://higgsfield.ai) | imagens e vídeos de apoio (explainers, mascote) |
| [HeyGen](https://heygen.com) | vídeo com avatar a partir de roteiro |
| vidIQ, Algrow | pesquisa de YouTube |
| A/B testing (first-party) | resultados de experimentos das landing pages do site, para decidir CTA |
| Notion, Google Drive, Sheets, Gmail (conectores claude.ai) | material de apoio e operação |
| mem0, Basic Memory | memória entre sessões |

Plugins do Claude Code em uso: `ralph-loop` (loop autônomo em sessão) e `caveman` (respostas comprimidas para economizar tokens). O RTK (Rust Token Killer) roda como hook e reescreve comandos de shell para reduzir tokens de saída.

Ferramenta fora do Claude Code: o app do **Grok**, usado no passo 2 da `cacar-news-jacking`. A skill gera um prompt, você cola no Grok (que tem busca nativa no X) e devolve o resultado para a sessão.

## TTS local (OmniVoice)

O áudio narrado usa o [OmniVoice](https://huggingface.co/k2-fsa/OmniVoice) rodando na própria máquina, com clone de voz.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt   # torch + CUDA: vários GB
```

A primeira execução baixa o checkpoint do Hugging Face. Com GPU, um post leva de 1 a 3 minutos. O `generate-audio.sh` procura o binário em `./.venv/bin/omnivoice-infer` (ou em `$OMNIVOICE_BIN`).

O `requirements.txt` da raiz é o freeze desse ambiente e fixa `torch==2.8.0+cu128`; em máquina sem GPU NVIDIA, instale o `torch` adequado antes.

## Arquivos que você precisa fornecer

Três coisas ficam de fora do repositório de propósito:

| arquivo | por quê | o que acontece sem ele |
|---|---|---|
| `.claude/skills/criar-post-blog/voice/lucas.wav` + `lucas.txt` | amostra de voz é dado biométrico | o passo de áudio falha; crie o post sem áudio ou grave a sua amostra (instruções no `README.md` da pasta) |
| `.claude/skills/montar-cta-pitch/references/arsenal-pitch-cla.md` | playbook comercial interno | a skill de CTA fica sem os argumentos; escreva o seu arsenal com teses, dores, provas e objeções do seu produto |
| `seo-report/data.json` | dados reais de Search Console e GA4 | o painel abre vazio até você rodar `generate.py` |

## Conferindo o ambiente

```bash
claude mcp list                                              # os 4 servers conectados
bash .claude/skills/cacar-news-jacking/scripts/detect.sh     # radar em markdown, avisa fonte sem credencial
scripts/criar-posts-batch.py pautas/julho/semana-1-batch.md --dry-run   # imprime os prompts, não cria nada
```
