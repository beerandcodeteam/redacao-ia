# Referência de voz (clone do TTS)

O `generate-audio.sh` clona a voz a partir de dois arquivos nesta pasta, que **não são versionados** (amostra de voz é dado biométrico):

| arquivo | o quê |
|---|---|
| `lucas.wav` | 20 a 40 s de fala limpa, mono, sem música nem ruído de fundo |
| `lucas.txt` | transcrição **literal** do que é dito no `.wav`, em uma linha |

Grave a sua amostra e salve com esses nomes (ou ajuste `REF_AUDIO`/`REF_TEXT_FILE` no script). Sem os dois arquivos o passo de áudio falha com "Voice ref faltando"; o resto do pipeline segue normal se o post for criado sem áudio.
