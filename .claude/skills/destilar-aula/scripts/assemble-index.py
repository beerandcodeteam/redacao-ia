#!/usr/bin/env python3
"""Monta o índice mestre (INDICE.md) do curso destilado a partir do
chapters.json e dos .md de capítulo já escritos.

Uso:
    assemble-index.py <curso_dir>

Espera:
    <curso_dir>/chapters.json  : {"curso": "...", "fonte": "...",
        "chapters": [{"n": 1, "slug": "...", "titulo": "...",
                      "objetivo": "...", "intervalo": "00:00 → 12:30",
                      "audio_url": "..."(opcional)}]}
    <curso_dir>/capitulos/NN-slug.md

Gera <curso_dir>/INDICE.md com objetivo, link do .md e (se houver) link do áudio.
Roda de novo depois de gerar os áudios pra atualizar os links.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("uso: assemble-index.py <curso_dir>", file=sys.stderr)
        return 64
    curso = Path(sys.argv[1])
    meta_file = curso / "chapters.json"
    if not meta_file.is_file():
        print(f"chapters.json não encontrado em {curso}", file=sys.stderr)
        return 1
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    chapters = meta.get("chapters", [])

    lines = [f"# {meta.get('curso', 'Curso destilado')}", ""]
    if meta.get("fonte"):
        lines.append(f"_Fonte: {meta['fonte']}_")
        lines.append("")
    lines.append(f"**{len(chapters)} capítulos** · sequência lógica para consumo em áudio.")
    lines.append("")

    with_audio = 0
    for ch in chapters:
        n = ch.get("n")
        slug = ch.get("slug", "")
        md_rel = f"capitulos/{n:02d}-{slug}.md" if isinstance(n, int) else f"capitulos/{slug}.md"
        titulo = ch.get("titulo", slug)
        lines.append(f"## {n:02d}. {titulo}" if isinstance(n, int) else f"## {titulo}")
        if ch.get("intervalo"):
            lines.append(f"_Trecho da aula: {ch['intervalo']}_")
        if ch.get("objetivo"):
            lines.append("")
            lines.append(ch["objetivo"])
        lines.append("")
        links = [f"[📄 Texto]({md_rel})"]
        if ch.get("audio_url"):
            links.append(f"[🎧 Áudio]({ch['audio_url']})")
            with_audio += 1
        elif ch.get("audio_file"):
            links.append(f"[🎧 Áudio]({ch['audio_file']})")
            with_audio += 1
        lines.append(" · ".join(links))
        lines.append("")

    out = curso / "INDICE.md"
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"→ INDICE.md gerado: {len(chapters)} capítulos, {with_audio} com áudio",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
