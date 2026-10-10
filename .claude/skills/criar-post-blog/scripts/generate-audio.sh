#!/usr/bin/env bash
# Gera áudio narrado de um post via OmniVoice (clone de voz com lucas.wav),
# converte pra MP3 e sobe pro OCI Object Storage. Devolve a URL pública na
# última linha do stdout.
#
# Uso:
#   generate-audio.sh <script_path> <slug>
#
# - <script_path>: arquivo .txt com o roteiro narrável (resultado do
#   reescritor — ver references/audio-script.md). UTF-8, texto plano.
# - <slug>: slug do post. Vira nome do objeto: posts/audio/<slug>.mp3.
#
# Lê credenciais OCI do .env do cwd (mesmas do generate-cover.sh):
#   OCI_ACCESS_KEY_ID, OCI_SECRET_ACCESS_KEY, OCI_BUCKET, OCI_ENDPOINT, OCI_URL
#
# Dependências: .venv com omnivoice-infer, ffmpeg, aws CLI v2, python3.
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "uso: $(basename "$0") <script_path> <slug>" >&2
  exit 64
fi

SCRIPT_PATH="$1"
SLUG="$2"

if [[ ! -f "$SCRIPT_PATH" ]]; then
  echo "Roteiro não encontrado: $SCRIPT_PATH" >&2
  exit 1
fi

# Voice ref relativo ao diretório da skill (script roda de qualquer cwd).
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REF_AUDIO="$SKILL_DIR/voice/lucas.wav"
REF_TEXT_FILE="$SKILL_DIR/voice/lucas.txt"

if [[ ! -f "$REF_AUDIO" || ! -f "$REF_TEXT_FILE" ]]; then
  echo "Voice ref faltando em $SKILL_DIR/voice/ (precisa lucas.wav + lucas.txt)" >&2
  exit 1
fi

REF_TEXT="$(cat "$REF_TEXT_FILE")"

# Localiza omnivoice-infer no .venv da raiz do projeto (cwd).
OMNIVOICE="${OMNIVOICE_BIN:-./.venv/bin/omnivoice-infer}"
if [[ ! -x "$OMNIVOICE" ]]; then
  echo "omnivoice-infer não encontrado em $OMNIVOICE. Ative o .venv ou export OMNIVOICE_BIN." >&2
  exit 1
fi

# .env do cwd (mesmas vars do generate-cover.sh).
if [[ -f .env ]]; then
  tmp_env=$(mktemp)
  trap 'rm -f "$tmp_env" "${WAV_OUT:-}" "${MP3_OUT:-}"' EXIT
  tr -d '\r' < .env > "$tmp_env"
  set -a
  # shellcheck disable=SC1090
  source "$tmp_env"
  set +a
else
  trap 'rm -f "${WAV_OUT:-}" "${MP3_OUT:-}"' EXIT
fi

require_var() {
  if [[ -z "${!1:-}" ]]; then
    echo "$1 não está definida. Configure no .env do cwd ou export antes de chamar." >&2
    exit 1
  fi
}

require_var OCI_ACCESS_KEY_ID
require_var OCI_SECRET_ACCESS_KEY
require_var OCI_BUCKET
require_var OCI_ENDPOINT
require_var OCI_URL

for cmd in ffmpeg aws python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Dependência faltando: $cmd" >&2
    exit 1
  fi
done

WAV_OUT=$(mktemp --suffix=.wav)
MP3_OUT=$(mktemp --suffix=.mp3)

# 1. Gera áudio com OmniVoice (voice cloning via ref_audio + ref_text).
# --language "pt" (ISO 639-1). Se OmniVoice reclamar, troque por "Portuguese".
echo "→ Gerando áudio com OmniVoice (clone de voz: $(basename "$REF_AUDIO"))" >&2
"$OMNIVOICE" \
  --text "$(cat "$SCRIPT_PATH")" \
  --output "$WAV_OUT" \
  --ref_audio "$REF_AUDIO" \
  --ref_text "$REF_TEXT" \
  --language pt \
  >&2

if [[ ! -s "$WAV_OUT" ]]; then
  echo "OmniVoice não produziu áudio (output vazio)." >&2
  exit 1
fi

# 2. Converte WAV → MP3 (qualidade ~128kbps VBR — mesmo q:a 4 do pipeline antigo).
echo "→ Convertendo WAV → MP3" >&2
ffmpeg -y -i "$WAV_OUT" -c:a libmp3lame -q:a 4 "$MP3_OUT" -loglevel error >&2

# 3. Sobe pro OCI (S3-compatible, mesmo padrão do generate-cover.sh).
OBJECT_KEY="posts/audio/${SLUG}.mp3"
echo "→ Subindo para OCI: $OBJECT_KEY" >&2

AWS_ACCESS_KEY_ID="$OCI_ACCESS_KEY_ID" \
AWS_SECRET_ACCESS_KEY="$OCI_SECRET_ACCESS_KEY" \
AWS_DEFAULT_REGION=us-east-1 \
AWS_REQUEST_CHECKSUM_CALCULATION=when_required \
AWS_RESPONSE_CHECKSUM_VALIDATION=when_required \
aws s3 cp "$MP3_OUT" "s3://$OCI_BUCKET/$OBJECT_KEY" \
  --endpoint-url "$OCI_ENDPOINT" \
  --content-type "audio/mpeg" \
  --no-progress \
  >&2

# 4. URL pública (única linha em stdout — preserva contrato do generate-cover.sh).
encode_path() {
  python3 -c '
import sys, urllib.parse
print("/".join(urllib.parse.quote(p, safe="") for p in sys.argv[1].split("/")))
' "$1"
}

encoded_key=$(encode_path "$OBJECT_KEY")
public_url="${OCI_URL%/}/${encoded_key}"
echo "Áudio publicado em: $public_url" >&2
echo "$public_url"
