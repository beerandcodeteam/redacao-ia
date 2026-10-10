# Painel SEO — Beer & Code

Relatório SEO self-contained do blog (`blog.beerandcode.com.br`) cruzando
**Google Search Console**, **GA4**, **DataForSEO** e **PageSpeed Insights**,
com um botão que dispara o **Claude** (skill `planejar-pauta`) pra gerar a pauta
da semana a partir do relatório atual + um foco que você digita.

## Arquivos

| arquivo | o quê |
|---|---|
| `generate.py` | puxa as 4 fontes → grava `data.json` |
| `index.html`  | dashboard (Chart.js); lê `data.json` |
| `server.py`   | serve o painel + `/api/refresh` + `/api/gerar-pauta` (roda o Claude) |
| `data.json`   | snapshot dos dados (gerado) |
| `.venv/`      | venv com as deps (não versionado) |

`data.json` também não é versionado: ele guarda dados reais de Search Console e GA4. Rode o `generate.py` para criar o seu.

## Instalar

```bash
python3 -m venv seo-report/.venv
seo-report/.venv/bin/pip install -r seo-report/requirements.txt
```

Credenciais e variáveis: ver [docs/setup.md](../docs/setup.md). As constantes do blog (domínio, propriedades do GA4, locale do DataForSEO) ficam no topo do `generate.py`.

## Rodar

```bash
# a partir da raiz do repositório
GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/application_default_credentials.json \
  seo-report/.venv/bin/python seo-report/server.py
# abre http://localhost:8755
```

- **Seletor de janela (7/28/90 dias)** → re-puxa **só GSC+GA4+funil** pra nova janela
  e mescla (~3–5s). DataForSEO (volume = média mensal) e PageSpeed (estado atual) não
  dependem de janela, então são preservados.
- **↻ Atualizar tudo** → re-roda `generate.py` completo (lento; PageSpeed ~1–2 min).
- **✨ Gerar pauta da semana** → digita o foco, escolhe objetivo/qtd, clica Gerar.
  O Claude roda de verdade na raiz deste repositório (usa os MCP do `.mcp.json` e
  a skill `planejar-pauta`), streama a saída e, se marcado, salva em
  `pautas/<mês>/semana-N.md`.

Só gerar o `data.json` sem servidor:

```bash
GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/application_default_credentials.json \
  seo-report/.venv/bin/python seo-report/generate.py --days 90
```

## Insights com IA (por card + chat global)

Cada card analítico (Top queries, Oportunidades, Top páginas, Keywords quentes,
Landing pages, Core Web Vitals) tem um botão **💡 insights** que abre um modal e
roda o Claude como consultor de SEO/growth, **streamando** a resposta em markdown.

- **Conversa contínua**: dá pra perguntar de volta no mesmo modal — o follow-up
  usa `claude --resume <session_id>`, mantendo o contexto.
- **Core Web Vitals**: o Claude **inspeciona o código** do app do blog (diretório em `BLOG_V2_DIR`) pra
  explicar a causa de cada métrica e sugerir fix específico (preload, lazy, etc.).
- **💬 Chat SEO** (header): chat global que lê TODAS as métricas e cruza sinais.

Endpoint: `POST /api/insight {card, session_id?, message?}` → streama texto; a 1ª
linha é `__SID__<session_id>` (o front captura e descarta). O Claude roda com
`cwd=$BLOG_V2_DIR` + `--add-dir <raiz deste repo>`, `--dangerously-skip-permissions`.

## Fontes / credenciais

| fonte | auth |
|---|---|
| Search Console | token OAuth `~/.config/mcp-gsc/token.json` (escopo webmasters) |
| GA4 (blog) | ADC (`application_default_credentials.json`); property em `GA4_PROPERTY_ID` no `../.env` |
| GA4 funil (blog → site) | mesma ADC; property do site em `GA4_SITE_PROPERTY_ID` no `../.env`; no site, origem = `sessionSource` contendo "blog" |
| DataForSEO | `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD` no `../.env` |
| PageSpeed | `PAGESPEED_API_KEY` no `../.env` |

Cada fonte é isolada: se uma falhar, o painel mostra o erro e renderiza o resto.

## Notas

- `server.py` roda o Claude com `--dangerously-skip-permissions` (execução
  desacompanhada). Use só localmente, nunca exposto na rede.
- Variáveis opcionais: `BLOG_V2_DIR` (default: `../blog-v2-bc`, irmão deste repo)
  e `SEO_PORT` (default `8755`).
- `hot_keywords` é filtrado pelo vocabulário do nicho (IA/LLM/dev) pra não vazar
  termo sazonal off-topic do `keyword_ideas`.