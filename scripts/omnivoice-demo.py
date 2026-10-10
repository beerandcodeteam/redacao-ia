#!/usr/bin/env python3
"""Sobe a demo Gradio do OmniVoice já com a voz do Lucas pré-carregada.

Mesma referência que o pipeline automático usa (generate-audio.sh):
voice/lucas.wav + voice/lucas.txt da skill criar-post-blog, idioma Portuguese.
A aba Voice Clone abre com áudio, transcrição e idioma preenchidos — quem
testa só digita o texto e clica em Generate.

Uso (da raiz do projeto):
    .venv/bin/python scripts/omnivoice-demo.py [--port 7860] [demais flags do omnivoice-demo]
"""
import sys
from pathlib import Path

import gradio as gr
from omnivoice.cli import demo

VOICE_DIR = Path(__file__).resolve().parent.parent / ".claude/skills/criar-post-blog/voice"
REF_AUDIO = str(VOICE_DIR / "lucas.wav")
REF_TEXT = (VOICE_DIR / "lucas.txt").read_text(encoding="utf-8").strip()
LANGUAGE = "Portuguese"

_Audio, _Textbox, _Dropdown = gr.Audio, gr.Textbox, gr.Dropdown


def _audio(*args, **kw):
    if str(kw.get("label", "")).startswith("Reference Audio"):
        kw.setdefault("value", REF_AUDIO)
    return _Audio(*args, **kw)


def _textbox(*args, **kw):
    if str(kw.get("label", "")).startswith("Reference Text"):
        kw.setdefault("value", REF_TEXT)
    return _Textbox(*args, **kw)


def _dropdown(*args, **kw):
    if str(kw.get("label", "")).startswith("Language") and kw.get("value") == "Auto":
        kw["value"] = LANGUAGE
    return _Dropdown(*args, **kw)


# build_demo referencia gr.* em tempo de execução, então o patch no módulo basta.
gr.Audio, gr.Textbox, gr.Dropdown = _audio, _textbox, _dropdown

if __name__ == "__main__":
    sys.exit(demo.main())
