#!/usr/bin/env python3
"""Imprime o trecho LITERAL da transcrição num intervalo de tempo.

Usado pelos agentes escritores (fase 3) pra ler as palavras exatas do capítulo
que estão escrevendo — em vez de confiar só nas notas destiladas. Mantém a
fidelidade alta: o escritor ancora no texto-fonte, não numa paráfrase.

Uso:
    slice-transcript.py <segments.json> <start> <end>

<start>/<end> aceitam HH:MM:SS, MM:SS ou segundos (ex: 1230).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def to_seconds(v: str) -> float:
    v = v.strip()
    if ":" in v:
        parts = [float(p) for p in v.split(":")]
        s = 0.0
        for p in parts:
            s = s * 60 + p
        return s
    return float(v)


def main() -> int:
    if len(sys.argv) != 4:
        print("uso: slice-transcript.py <segments.json> <start> <end>", file=sys.stderr)
        return 64
    seg_file = Path(sys.argv[1])
    start = to_seconds(sys.argv[2])
    end = to_seconds(sys.argv[3])
    segments = json.loads(seg_file.read_text(encoding="utf-8"))
    out = [s["text"] for s in segments if s["end"] >= start and s["start"] <= end]
    if not out:
        print("(nenhum segmento nesse intervalo)", file=sys.stderr)
        return 0
    print(" ".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
