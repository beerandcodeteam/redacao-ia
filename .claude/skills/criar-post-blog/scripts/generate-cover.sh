#!/usr/bin/env bash
# Gera capa de post via Gemini nano-banana (gemini-3.1-flash-image-preview)
# e sobe a imagem para o OCI Object Storage (S3-compatible), devolvendo a
# URL pública na última linha do stdout.
#
# Uso:
#   generate-cover.sh "<prompt>" <output_path> [object_key]
#
# - <output_path>: caminho local onde salvar o PNG (ex.: /tmp/cover-foo.png).
# - [object_key]: nome do objeto no bucket. Default: posts/<basename do output>.
#
# Lê GEMINI_API_KEY e credenciais OCI do .env do cwd se não houver no ambiente.
# Variáveis OCI obrigatórias:
#   OCI_ACCESS_KEY_ID, OCI_SECRET_ACCESS_KEY, OCI_BUCKET, OCI_ENDPOINT, OCI_URL
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "uso: $(basename "$0") \"<prompt>\" <output_path> [object_key]" >&2
  exit 64
fi

PROMPT="$1"
OUTPUT="$2"
OBJECT_KEY="${3:-posts/$(basename "$OUTPUT")}"

if [[ -f .env ]]; then
  # tolera CRLF no .env (arquivo editado no Windows)
  tmp_env=$(mktemp)
  trap 'rm -f "$tmp_env"' EXIT
  tr -d '\r' < .env > "$tmp_env"
  set -a
  # shellcheck disable=SC1090
  source "$tmp_env"
  set +a
fi

require_var() {
  if [[ -z "${!1:-}" ]]; then
    echo "$1 não está definida. Configure no .env do cwd ou export antes de chamar." >&2
    exit 1
  fi
}

require_var GEMINI_API_KEY
require_var OCI_ACCESS_KEY_ID
require_var OCI_SECRET_ACCESS_KEY
require_var OCI_BUCKET
require_var OCI_ENDPOINT
require_var OCI_URL

for cmd in curl jq base64 aws; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Dependência faltando: $cmd" >&2
    exit 1
  fi
done

# 1. Gera imagem via Gemini
payload=$(jq -nc --arg p "$PROMPT" '{contents:[{parts:[{text:$p}]}]}')

response=$(curl -sS -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  --data "$payload")

img_b64=$(printf '%s' "$response" | jq -r '
  .candidates[0].content.parts[]?
  | select(.inlineData)
  | .inlineData.data
' | head -n1)

if [[ -z "$img_b64" || "$img_b64" == "null" ]]; then
  echo "Resposta sem imagem. Conteúdo bruto:" >&2
  printf '%s\n' "$response" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
printf '%s' "$img_b64" | base64 -d > "$OUTPUT"
echo "Capa gerada: $OUTPUT" >&2

# 2. Sobe pro OCI Object Storage (S3 compat).
# OCI exige SigV4 mas o aws-cli v2 valida o nome da região; usamos us-east-1
# só para o cálculo da assinatura — o endpoint é o que define o destino real.
content_type="image/png"
case "${OUTPUT,,}" in
  *.jpg|*.jpeg) content_type="image/jpeg" ;;
  *.webp)       content_type="image/webp" ;;
  *.gif)        content_type="image/gif" ;;
esac

AWS_ACCESS_KEY_ID="$OCI_ACCESS_KEY_ID" \
AWS_SECRET_ACCESS_KEY="$OCI_SECRET_ACCESS_KEY" \
AWS_DEFAULT_REGION=us-east-1 \
AWS_REQUEST_CHECKSUM_CALCULATION=when_required \
AWS_RESPONSE_CHECKSUM_VALIDATION=when_required \
aws s3 cp "$OUTPUT" "s3://$OCI_BUCKET/$OBJECT_KEY" \
  --endpoint-url "$OCI_ENDPOINT" \
  --content-type "$content_type" \
  --no-progress \
  >&2

# 3. Imprime a URL pública (única linha em stdout).
# Codifica cada segmento do path preservando "/" para evitar URLs quebradas
# quando o object key contiver espaços ou acentos.
encode_path() {
  python3 -c '
import sys, urllib.parse
print("/".join(urllib.parse.quote(p, safe="") for p in sys.argv[1].split("/")))
' "$1"
}

encoded_key=$(encode_path "$OBJECT_KEY")
public_url="${OCI_URL%/}/${encoded_key}"
echo "Capa publicada em: $public_url" >&2
echo "$public_url"
