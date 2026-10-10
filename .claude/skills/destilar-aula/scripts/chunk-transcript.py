#!/usr/bin/env python3
"""Quebra uma transcrição grande (SRT/VTT/TXT) em janelas (chunks) sobrepostas
para processamento map-reduce por subagents.

Por que existe: uma aula de 4-8h tem 40-80k palavras. Lê-la inteira num único
contexto degrada a qualidade da análise. Este script faz o trabalho determinístico
(parse + janelamento) FORA do contexto do modelo — zero tokens — e entrega chunks
pequenos que cada subagent processa com alta fidelidade.

Uso:
    chunk-transcript.py <transcript> <workdir> [--minutes 18] [--overlap 75]

Saída:
    - <workdir>/segments.json   : segmentos normalizados [{start, end, text}]
    - <workdir>/chunk-001.txt … : um arquivo por janela (com header de tempo)
    - stdout                    : manifesto JSON (passe como `args` pro workflow)

Aceita .srt, .vtt e .txt. Para .txt sem timestamps, janela por contagem de
palavras (~150 palavras/min de fala) e os "tempos" viram índices aproximados.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

WORDS_PER_MIN = 150  # estimativa de fala para .txt sem timestamps

TS_RE = re.compile(
    r"(?P<h>\d{1,2}):(?P<m>\d{2}):(?P<s>\d{2})[.,](?P<ms>\d{1,3})"
)
CUE_RE = re.compile(
    r"(\d{1,2}:\d{2}:\d{2}[.,]\d{1,3})\s*-->\s*(\d{1,2}:\d{2}:\d{2}[.,]\d{1,3})"
)


def ts_to_seconds(ts: str) -> float:
    m = TS_RE.match(ts.strip())
    if not m:
        raise ValueError(f"timestamp inválido: {ts!r}")
    return (
        int(m["h"]) * 3600
        + int(m["m"]) * 60
        + int(m["s"])
        + int(m["ms"].ljust(3, "0")) / 1000.0
    )


def seconds_to_hms(s: float) -> str:
    s = int(round(s))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def clean_text(t: str) -> str:
    # remove tags VTT (<c>, <00:00:00.000>), normaliza espaços
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def parse_timed(raw: str) -> list[dict]:
    """Parse SRT/VTT em segmentos {start, end, text}. Funde cues consecutivos
    e descarta duplicatas (comum em legendas auto-geradas com rolagem)."""
    segments: list[dict] = []
    blocks = re.split(r"\n\s*\n", raw)
    last_text = ""
    for block in blocks:
        cue = CUE_RE.search(block)
        if not cue:
            continue
        start = ts_to_seconds(cue.group(1))
        end = ts_to_seconds(cue.group(2))
        # texto = linhas após a linha do cue
        lines = block.splitlines()
        text_lines = []
        seen_cue = False
        for line in lines:
            if CUE_RE.search(line):
                seen_cue = True
                continue
            if seen_cue and line.strip() and not line.strip().isdigit():
                text_lines.append(line)
        text = clean_text(" ".join(text_lines))
        if not text or text == last_text:
            continue
        # dedup parcial de rolagem: se o novo texto começa com o final do anterior
        if last_text and text.startswith(last_text[-40:]) and len(last_text) > 40:
            text = text[len(last_text[-40:]):].strip()
        if not text:
            continue
        segments.append({"start": start, "end": end, "text": text})
        last_text = clean_text(" ".join(text_lines))
    return segments


def parse_plain(raw: str) -> list[dict]:
    """Parse .txt: quebra em pseudo-segmentos por sentença, com tempos
    estimados por contagem de palavras."""
    raw = clean_text(raw)
    sentences = re.split(r"(?<=[.!?])\s+", raw)
    segments: list[dict] = []
    elapsed = 0.0
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        dur = max(1.0, len(sent.split()) / WORDS_PER_MIN * 60)
        segments.append({"start": elapsed, "end": elapsed + dur, "text": sent})
        elapsed += dur
    return segments


def window(segments: list[dict], target_min: float, overlap_s: float) -> list[dict]:
    """Agrupa segmentos em janelas de ~target_min minutos com overlap_s segundos
    de sobreposição entre janelas consecutivas (pra não cortar conceito no meio)."""
    if not segments:
        return []
    target_s = target_min * 60
    chunks: list[dict] = []
    i = 0
    n = len(segments)
    while i < n:
        start_t = segments[i]["start"]
        j = i
        while j < n and segments[j]["end"] - start_t < target_s:
            j += 1
        # j é exclusivo; inclui pelo menos 1 segmento
        j = max(j, i + 1)
        group = segments[i:j]
        chunks.append(
            {
                "start": group[0]["start"],
                "end": group[-1]["end"],
                "text": " ".join(s["text"] for s in group),
            }
        )
        if j >= n:
            break
        # recua o início da próxima janela pra criar overlap
        next_start_time = segments[j]["start"] - overlap_s
        k = j
        while k > i + 1 and segments[k - 1]["start"] >= next_start_time:
            k -= 1
        i = k
    return chunks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("workdir")
    ap.add_argument("--minutes", type=float, default=18.0,
                    help="duração-alvo de cada chunk em minutos (default 18)")
    ap.add_argument("--overlap", type=float, default=75.0,
                    help="overlap entre chunks em segundos (default 75)")
    args = ap.parse_args()

    src = Path(args.transcript)
    if not src.is_file():
        print(f"transcrição não encontrada: {src}", file=sys.stderr)
        return 1
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    raw = src.read_text(encoding="utf-8", errors="replace")
    suffix = src.suffix.lower()
    if suffix in (".srt", ".vtt") or CUE_RE.search(raw):
        segments = parse_timed(raw)
        timed = True
    else:
        segments = parse_plain(raw)
        timed = False

    if not segments:
        print("nenhum segmento extraído — formato não reconhecido?", file=sys.stderr)
        return 1

    chunks = window(segments, args.minutes, args.overlap)

    (workdir / "segments.json").write_text(
        json.dumps(segments, ensure_ascii=False), encoding="utf-8"
    )

    manifest_chunks = []
    for idx, c in enumerate(chunks, 1):
        fname = f"chunk-{idx:03d}.txt"
        words = len(c["text"].split())
        header = (
            f"[CHUNK {idx}/{len(chunks)}]  "
            f"{seconds_to_hms(c['start'])} → {seconds_to_hms(c['end'])}  "
            f"(~{words} palavras)\n"
            f"{'-' * 60}\n"
        )
        (workdir / fname).write_text(header + c["text"], encoding="utf-8")
        manifest_chunks.append(
            {
                "id": idx,
                "file": str(workdir / fname),
                "start": seconds_to_hms(c["start"]),
                "end": seconds_to_hms(c["end"]),
                "start_s": round(c["start"], 1),
                "end_s": round(c["end"], 1),
                "words": words,
            }
        )

    total_words = sum(len(s["text"].split()) for s in segments)
    manifest = {
        "workdir": str(workdir),
        "segments_file": str(workdir / "segments.json"),
        "timed": timed,
        "duration": seconds_to_hms(segments[-1]["end"]),
        "total_words": total_words,
        "total_chunks": len(chunks),
        "chunks": manifest_chunks,
    }
    print(json.dumps(manifest, ensure_ascii=False))
    print(
        f"→ {len(chunks)} chunks de ~{args.minutes:g}min, "
        f"{total_words} palavras, duração {manifest['duration']} em {workdir}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
