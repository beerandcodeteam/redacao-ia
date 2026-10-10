#!/usr/bin/env bash
# detect.sh — caça news-jacking de IA: bate em todas as fontes em uma passada,
# marca o que é NOVO desde o último run e imprime um radar em markdown.
# Fontes sem credencial: Hacker News, OpenRouter, Polymarket, GitHub, GDELT.
# Fontes com credencial (do ~/.claude/newsjack.env): Reddit, NewsAPI, GitHub token.
#
# Uso:
#   bash detect.sh                         # foco default (IA/LLM/coding agents)
#   bash detect.sh -q "claude OR fable"    # foco custom (sintaxe de busca por fonte)
#   bash detect.sh -h 72                   # janela de 72h (default 48)
#
# Saída: markdown no stdout. Snapshots crus em ../state/.

set -uo pipefail

# ---------- args ----------
QUERY_DEFAULT='GPT-5 OR GPT-5.6 OR Claude OR Fable OR "Gemini 3" OR OpenAI OR Anthropic OR LLM OR Codex OR DeepSeek OR Qwen OR Mistral OR Llama'
QUERY="$QUERY_DEFAULT"
HOURS=48
while [ $# -gt 0 ]; do
  case "$1" in
    -q) QUERY="$2"; shift 2 ;;
    -h) HOURS="$2"; shift 2 ;;
    *)  echo "arg desconhecido: $1" >&2; exit 2 ;;
  esac
done

# ---------- paths / env ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="$SCRIPT_DIR/../state"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
mkdir -p "$STATE_DIR"

command -v jq   >/dev/null 2>&1 || { echo "ERRO: jq não encontrado no PATH." >&2; exit 3; }
command -v curl >/dev/null 2>&1 || { echo "ERRO: curl não encontrado no PATH." >&2; exit 3; }

# Procura o env nesta ordem (carrega TODOS que existirem; o último vence em caso de duplicata):
#   1) $NEWSJACK_ENV  2) ~/.claude/newsjack.env  3) ./.env (cwd)  4) raiz do projeto/.env
LOADED_ENV=""
for f in "${NEWSJACK_ENV:-}" "$HOME/.claude/newsjack.env" "$PWD/.env" "$PROJECT_ROOT/.env"; do
  [ -n "$f" ] && [ -f "$f" ] || continue
  rf="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"   # caminho absoluto p/ dedup
  case " $LOADED_ENV " in *" $rf "*) continue;; esac
  set -a; . <(sed 's/\r$//' "$f"); set +a   # tolera .env salvo com CRLF (Windows)
  LOADED_ENV="${LOADED_ENV} $rf"
done
if [ -n "$LOADED_ENV" ]; then
  echo "> env carregado de:${LOADED_ENV}"
else
  echo "> ⚠️ nenhum env encontrado — rodando só com fontes sem credencial (HN, OpenRouter, GitHub, GDELT)."
fi

CURL='curl -sL --max-time 25'
UA="${REDDIT_USER_AGENT:-beerandcode-newsjack/1.0}"
urlencode() { jq -rn --arg s "$1" '$s|@uri'; }
# epoch de corte (compatível GNU e BSD date)
CUTOFF=$(date -d "$HOURS hours ago" +%s 2>/dev/null || date -v-"${HOURS}"H +%s)

echo "# Radar news-jacking — janela ${HOURS}h"
echo "> foco: \`${QUERY}\`"
echo ""

# ---------- 1. Hacker News (Algolia, sem auth) ----------
# NB: numericFilters do Algolia quebra via curl; filtramos por pontos/recência no jq.
# OR booleano confunde o Algolia, então no foco default buscamos termo a termo e juntamos.
echo "## 🟠 Hacker News (stories recentes com tração)"
HN_TMP="$(mktemp)"
hn_search() {
  $CURL "https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=$2&query=$(urlencode "$1")" \
    | jq -r --argjson c "$CUTOFF" '.hits[]? | select((.points//0)>=20 and (.created_at_i//0)>=$c)
        | "\(.points)\t\(.title)\thttps://news.ycombinator.com/item?id=\(.objectID)"' 2>/dev/null
}
if [ "$QUERY" = "$QUERY_DEFAULT" ]; then
  for t in "GPT-5.6" "GPT-5" "Claude Fable" "Claude Opus" "Claude Code" "Gemini 3" "OpenAI" "Anthropic" "Codex" "DeepSeek" "Qwen" "Mistral"; do
    hn_search "$t" 15 >> "$HN_TMP"
  done
else
  hn_search "$QUERY" 40 >> "$HN_TMP"
fi
if [ -s "$HN_TMP" ]; then
  sort -t$'\t' -k1 -rn "$HN_TMP" | awk -F'\t' '!seen[$3]++ {printf "- %s — %s pts — %s\n", $2, $1, $3}' | head -20
else
  echo "- (nada acima de 20 pts na janela de ${HOURS}h)"
fi
rm -f "$HN_TMP"
echo ""

# ---------- 2. OpenRouter (diff de catálogo = modelo novo/bloqueado) ----------
echo "## 🔵 OpenRouter (mudança de catálogo — sinal de modelo novo/bloqueado)"
OR_CUR="$STATE_DIR/openrouter_models.txt"
OR_NEW="$(mktemp)"
$CURL "https://openrouter.ai/api/v1/models" | jq -r '.data[]?.id' | sort -u > "$OR_NEW" 2>/dev/null
if [ -s "$OR_NEW" ]; then
  if [ -f "$OR_CUR" ]; then
    ADDED="$(comm -13 "$OR_CUR" "$OR_NEW")"
    REMOVED="$(comm -23 "$OR_CUR" "$OR_NEW")"
    [ -n "$ADDED" ]   && echo "$ADDED"   | sed 's/^/- 🆕 NOVO: /'
    [ -n "$REMOVED" ] && echo "$REMOVED" | sed 's/^/- ⛔ REMOVIDO (possível bloqueio): /'
    [ -z "$ADDED$REMOVED" ] && echo "- (sem mudança desde o último run)"
  else
    echo "- (primeira execução — baseline de $(wc -l < "$OR_NEW") modelos salvo, sem diff)"
  fi
  mv "$OR_NEW" "$OR_CUR"
else
  echo "- (falha ao consultar OpenRouter)"; rm -f "$OR_NEW"
fi
echo ""

# ---------- 3. GitHub (releases de repos-chave) ----------
echo "## ⚫ GitHub (releases recentes em repos-chave)"
GH_AUTH=(); [ -n "${GITHUB_TOKEN:-}" ] && GH_AUTH=(-H "Authorization: Bearer $GITHUB_TOKEN")
for repo in ggml-org/llama.cpp ollama/ollama vllm-project/vllm; do
  $CURL "${GH_AUTH[@]}" -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$repo/releases?per_page=2" \
    | jq -r --arg r "$repo" '.[]? | select(.published_at != null) | "- [\($r)] \(.name // .tag_name) — \(.published_at) — \(.html_url)"' \
    2>/dev/null
done
[ -z "${GITHUB_TOKEN:-}" ] && echo "> (sem GITHUB_TOKEN — rate limit baixo)"
echo ""

# ---------- 4. Reddit (top do dia nos subs de IA) ----------
# Primário: OAuth (app web/script via client_credentials, ou password grant se houver USER/PASS).
#           OAuth traz ups/comentários e não toma 429. Fallback: RSS público best-effort.
echo "## 🔴 Reddit (top do dia nos subs de IA)"
SUBS="LocalLLaMA ClaudeAI OpenAI singularity ArtificialInteligence MachineLearning"
reddit_token() {
  [ -z "${REDDIT_CLIENT_ID:-}" ] && return 1
  local resp
  if [ -n "${REDDIT_USERNAME:-}" ] && [ -n "${REDDIT_PASSWORD:-}" ]; then
    resp=$($CURL -A "$UA" --user "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" \
      -d grant_type=password -d "username=$REDDIT_USERNAME" -d "password=$REDDIT_PASSWORD" \
      https://www.reddit.com/api/v1/access_token)
  else
    resp=$($CURL -A "$UA" --user "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" \
      -d grant_type=client_credentials https://www.reddit.com/api/v1/access_token)
  fi
  printf '%s' "$resp" | jq -r '.access_token // empty' 2>/dev/null
}
reddit_rss() {   # fallback sem credencial; ecoa __RL__ se 429
  local sub="$1" n="${2:-6}" t=0 code tmp; tmp="$(mktemp)"
  while [ "$t" -lt 2 ]; do
    code=$($CURL -A "$UA" -o "$tmp" -w '%{http_code}' "https://www.reddit.com/r/$sub/top.rss?t=day&limit=$n")
    [ "$code" = "200" ] && break; t=$((t+1)); sleep 8
  done
  if [ "$code" != "200" ]; then echo "__RL__"; rm -f "$tmp"; return; fi
  tr -d '\n' < "$tmp" | sed 's/<entry>/\n<entry>/g' | grep '<entry>' | head -n "$n" \
    | while IFS= read -r e; do
        title=$(printf '%s' "$e" | sed -n 's:.*<title>\([^<]*\)</title>.*:\1:p' \
                  | sed 's/&amp;/\&/g; s/&#39;/'"'"'/g; s/&quot;/"/g; s/&lt;/</g; s/&gt;/>/g')
        link=$(printf '%s' "$e" | grep -o 'href="[^"]*"' | head -1 | sed 's/href="//; s/"$//')
        [ -n "$title" ] && printf -- "- [r/%s] %s — %s\n" "$sub" "$title" "$link"
      done
  rm -f "$tmp"
}
TOK="$(reddit_token)"
if [ -n "$TOK" ]; then
  for sub in $SUBS; do
    $CURL -A "$UA" -H "Authorization: bearer $TOK" "https://oauth.reddit.com/r/$sub/top?t=day&limit=6" \
      | jq -r --arg s "$sub" '.data.children[]? | "- [r/\($s)] \(.data.title) — \(.data.ups) ups / \(.data.num_comments) com — https://reddit.com\(.data.permalink)"' \
      2>/dev/null
  done
else
  echo "> (sem OAuth — usando RSS público best-effort; pode dar 429)"
  R_OUT=""; RL=0
  for sub in LocalLLaMA ClaudeAI OpenAI; do
    out="$(reddit_rss "$sub" 6)"
    case "$out" in *__RL__*) RL=1;; *) R_OUT="${R_OUT}${out}
";; esac
    sleep 4
  done
  printf '%s' "$R_OUT" | grep -q '.' && printf '%s' "$R_OUT" | grep '.'
  [ "$RL" = "1" ] && echo "> ⚠️ Reddit 429 (rate-limit sem OAuth). HN cobre boa parte."
fi
echo ""

# ---------- 5. Notícias (NewsAPI ou GDELT) ----------
echo "## 📰 Notícias (momentum recente)"
if [ -n "${NEWSAPI_KEY:-}" ]; then
  FROM=$(date -u -d "$HOURS hours ago" +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -u -v-"${HOURS}"H +%Y-%m-%dT%H:%M:%S)
  # searchIn=title corta ruído (matches no corpo pegam qualquer menção); excludeDomains tira pacote/repo/blog.
  NEWS_EXCL="pypi.org,github.com,blogger.com,blogspot.com,cnblogs.com,medium.com,npmjs.com"
  NEWS_OUT=$($CURL "https://newsapi.org/v2/everything?q=$(urlencode "$QUERY")&searchIn=title&excludeDomains=${NEWS_EXCL}&from=${FROM}&sortBy=publishedAt&pageSize=15&language=en&apiKey=${NEWSAPI_KEY}" \
    | jq -r '.articles[]? | "- \(.title) — \(.source.name) — \(.publishedAt) — \(.url)"' 2>/dev/null)
  [ -n "$NEWS_OUT" ] && echo "$NEWS_OUT" || echo "- (NewsAPI sem resultados ou chave inválida)"
else
  # GDELT é o fallback sem chave; query simples e estática (não aceita bem dots/hifens/booleano longo).
  GDELT_OUT=$($CURL "https://api.gdeltproject.org/api/v2/doc/doc?query=$(urlencode '(OpenAI OR Anthropic OR Gemini OR ChatGPT OR "language model")')&mode=artlist&maxrecords=15&sort=datedesc&format=json&sourcelang=eng" \
    | jq -r '.articles[]? | "- \(.title) — \(.domain) — \(.seendate) — \(.url)"' 2>/dev/null)
  [ -n "$GDELT_OUT" ] && echo "$GDELT_OUT" || echo "- (GDELT indisponível/rate-limit — defina NEWSAPI_KEY para fonte confiável)"
  echo "> (usando GDELT, cobertura grosseira — defina NEWSAPI_KEY p/ usar seu foco -q e melhor ranqueamento)"
fi
echo ""

echo "---"
echo "_Gerado por detect.sh. Próximo passo: rode o handoff do Grok (references/grok-prompt.md) e qualifique os candidatos com DataForSEO + GSC (passo 3 da SKILL.md)._"
