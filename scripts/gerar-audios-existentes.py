#!/usr/bin/env python3
"""Gera áudio narrado para posts já publicados/agendados do blog Beer & Code
que ainda não têm `audio_path` setado.

Padrão idêntico ao `criar-posts-batch.py`: uma invocação `claude -p` por
post, retomável com `--from N`. A diferença é a fase de descoberta inicial,
que lista os posts sem áudio via MCP e grava uma queue em /tmp.

Uso:
    scripts/gerar-audios-existentes.py
    scripts/gerar-audios-existentes.py --discover-only
    scripts/gerar-audios-existentes.py --queue /tmp/audio-queue-<ts>.json
    scripts/gerar-audios-existentes.py --from 3
    scripts/gerar-audios-existentes.py --only 2
    scripts/gerar-audios-existentes.py --dry-run
    scripts/gerar-audios-existentes.py --show-work

Fluxo padrão (sem flags):
1. Chama Claude pra descobrir posts publicados+agendados sem audio_path.
   O agente grava {"posts":[{"slug":"..","title":".."}]} em /tmp/audio-queue-<ts>.json.
2. Lê a queue e processa post por post: get-post → reescrever body
   (prompt de references/audio-script.md) → generate-audio.sh → update-post
   com audio_url.

Idempotente: posts que já têm audio_path são pulados pelo agente da etapa
do post (re-checa antes de regerar).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
MCP_FILE = PROJECT_ROOT / ".mcp.json"

USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
DIM = "\033[2m" if USE_COLOR else ""
RESET = "\033[0m" if USE_COLOR else ""
CYAN = "\033[36m" if USE_COLOR else ""
GREEN = "\033[32m" if USE_COLOR else ""
RED = "\033[31m" if USE_COLOR else ""
YELLOW = "\033[33m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""


DISCOVERY_PROMPT = """\
Tarefa de descoberta: listar posts do blog Beer & Code que precisam de áudio narrado.

Passos:
1. Chame `mcp__beer-and-code-blog__list-posts` duas vezes:
   - `status=published, limit=200`
   - `status=scheduled, limit=200`
2. Junte os dois retornos. Deduplique por slug.
3. Para cada post, chame `mcp__beer-and-code-blog__get-post` e verifique o
   campo `audio_path`. Mantenha SOMENTE os posts cujo `audio_path` está
   vazio, null ou ausente.
4. Use a tool `Write` para gravar o arquivo `{queue_path}` com o conteúdo
   exato (UTF-8, JSON válido):

   {{"discovered_at": "<ISO8601 do agora>", "total": <N>, "posts": [
       {{"slug": "...", "title": "..."}}, ...
   ]}}

5. Termine com uma linha curta de texto confirmando: "queue gravada em
   {queue_path} com N posts."

Não chame `generate-audio.sh`, `update-post`, ou qualquer tool que altere
posts. Esta tarefa é apenas leitura + escrita do arquivo de queue.
"""


POST_PROMPT_TEMPLATE = """\
Gere áudio narrado para UM post do blog Beer & Code.

Slug do post: {slug}

Pipeline (siga o passo 5 da skill `criar-post-blog`; se a skill não estiver
carregada na sessão, use o conteúdo de `.claude/skills/criar-post-blog/SKILL.md`
e `.claude/skills/criar-post-blog/references/audio-script.md` como referência):

1. `mcp__beer-and-code-blog__get-post` com `slug={slug}` → leia title, excerpt,
   body e audio_path. Se `audio_path` já estiver preenchido (não null/vazio),
   NÃO regenere: imprima "ja tem audio, pulando" e termine com sucesso.

2. Reescreva o body em roteiro narrável aplicando o prompt de
   `.claude/skills/criar-post-blog/references/audio-script.md`. A entrada
   deve ser formatada como:

       TÍTULO: <title>

       RESUMO: <excerpt>

       CORPO:

       <body em markdown>

   A saída precisa ser texto plano UTF-8, sem markdown, pronto para TTS.
   Use a tool `Write` pra salvar em `/tmp/audio-script-{slug}.txt`.

3. Rode via Bash:
       .claude/skills/criar-post-blog/scripts/generate-audio.sh \\
           /tmp/audio-script-{slug}.txt {slug}

   A URL pública do mp3 sai na ÚLTIMA linha do stdout. Capture-a.

4. `mcp__beer-and-code-blog__update-post` com `slug={slug}` e `audio_url=<URL>`.
   Apenas esses dois campos — não toque em nada mais.

Modo batch: aplique defaults sensatos sem aguardar confirmação humana.
Pare somente se `generate-audio.sh` ou o MCP retornarem erro.
"""


def load_env() -> dict[str, str]:
    if not ENV_FILE.exists():
        return {}
    env: dict[str, str] = {}
    for raw in ENV_FILE.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _summarize_tool_input(inp: object) -> str:
    if not isinstance(inp, dict):
        return ""
    for key in (
        "title",
        "slug",
        "name",
        "path",
        "file_path",
        "command",
        "description",
        "url",
        "query",
        "prompt",
    ):
        v = inp.get(key)
        if isinstance(v, str) and v.strip():
            v = v.strip().splitlines()[0]
            return v if len(v) <= 100 else v[:97] + "..."
    return ""


def _render_event(event: dict) -> None:
    etype = event.get("type")

    if etype == "system" and event.get("subtype") == "init":
        model = event.get("model") or ""
        tools = event.get("tools") or []
        print(f"{DIM}· session iniciada ({model}, {len(tools)} tools){RESET}")
        return

    if etype == "assistant":
        for block in event.get("message", {}).get("content", []) or []:
            btype = block.get("type")
            if btype == "text":
                text = (block.get("text") or "").rstrip()
                if text:
                    print(text)
            elif btype == "tool_use":
                name = block.get("name", "?")
                summary = _summarize_tool_input(block.get("input"))
                tail = f" {DIM}{summary}{RESET}" if summary else ""
                print(f"{CYAN}→ {name}{RESET}{tail}")
            elif btype == "thinking":
                snippet = (block.get("thinking") or "").strip().splitlines()
                if snippet:
                    print(f"{DIM}{YELLOW}… {snippet[0][:120]}{RESET}")
        return

    if etype == "user":
        for block in event.get("message", {}).get("content", []) or []:
            if block.get("type") != "tool_result":
                continue
            is_error = bool(block.get("is_error"))
            content = block.get("content")
            if isinstance(content, list):
                content = " ".join(
                    c.get("text", "")
                    for c in content
                    if isinstance(c, dict) and c.get("type") == "text"
                )
            preview = ""
            if isinstance(content, str) and content.strip():
                first = content.strip().splitlines()[0]
                preview = first if len(first) <= 120 else first[:117] + "..."
            color = RED if is_error else GREEN
            marker = "✗" if is_error else "←"
            print(f"{color}{marker}{RESET} {DIM}{preview}{RESET}")
        return

    if etype == "result":
        if event.get("is_error"):
            err = event.get("result") or event.get("error") or ""
            print(f"{RED}✗ erro: {err}{RESET}")
        cost = event.get("total_cost_usd")
        duration_ms = event.get("duration_ms")
        if cost is not None and duration_ms is not None:
            print(
                f"{DIM}· concluído em {duration_ms / 1000:.1f}s · "
                f"${cost:.4f}{RESET}"
            )
        return


def _claude_cmd(prompt: str, stream: bool) -> list[str]:
    cmd = [
        "claude",
        "-p",
        prompt,
        "--dangerously-skip-permissions",
        "--mcp-config",
        str(MCP_FILE),
    ]
    if stream:
        cmd += ["--verbose", "--output-format", "stream-json"]
    return cmd


def run_claude(prompt: str, env: dict[str, str], stream: bool) -> int:
    proc_env = {**os.environ, **env}
    if not stream:
        return subprocess.call(
            _claude_cmd(prompt, stream=False),
            cwd=str(PROJECT_ROOT),
            env=proc_env,
        )

    proc = subprocess.Popen(
        _claude_cmd(prompt, stream=True),
        cwd=str(PROJECT_ROOT),
        env=proc_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        text=True,
    )
    assert proc.stdout is not None
    try:
        for line in proc.stdout:
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                print(line)
                continue
            _render_event(event)
    except KeyboardInterrupt:
        proc.terminate()
        raise
    return proc.wait()


def discover(env: dict[str, str], stream: bool) -> Path:
    """Pede ao Claude pra listar posts sem áudio e gravar /tmp/audio-queue-<ts>.json."""
    queue_path = Path(f"/tmp/audio-queue-{int(time.time())}.json")
    prompt = DISCOVERY_PROMPT.format(queue_path=queue_path)

    print(f"{BOLD}→ Descobrindo posts sem áudio...{RESET}")
    print(f"{DIM}  queue será gravada em {queue_path}{RESET}")
    rc = run_claude(prompt, env, stream=stream)
    if rc != 0:
        raise SystemExit(f"discovery falhou (exit {rc}). queue não foi gravada.")
    if not queue_path.exists():
        raise SystemExit(
            f"discovery terminou mas {queue_path} não existe. agente não chamou Write?"
        )

    return queue_path


def load_queue(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise SystemExit(f"queue inválida em {path}: {e}")

    posts = data.get("posts") if isinstance(data, dict) else None
    if not isinstance(posts, list):
        raise SystemExit(f"queue em {path} não tem campo 'posts' (lista).")
    return posts


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--queue",
        help=(
            "Path de uma queue já existente (JSON com {posts:[{slug,title}]}). "
            "Se omitido, faz a descoberta automaticamente."
        ),
    )
    ap.add_argument(
        "--discover-only",
        action="store_true",
        help="só descobre os posts e grava a queue; não processa nada.",
    )
    ap.add_argument(
        "--from",
        dest="start",
        type=int,
        default=1,
        help="começar do post N (1-indexed). Útil pra retomar batch que falhou.",
    )
    ap.add_argument(
        "--only",
        type=int,
        help="rodar somente o post N e parar.",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="só imprime os prompts que seriam enviados ao Claude.",
    )
    ap.add_argument(
        "--show-work",
        action="store_true",
        help="streama eventos do claude (texto, tool calls, resultados) em tempo real.",
    )
    args = ap.parse_args()

    env = load_env()

    # Fase 1: descoberta (a menos que --queue tenha sido passada).
    if args.queue:
        queue_path = Path(args.queue)
        if not queue_path.exists():
            print(f"queue não encontrada: {queue_path}", file=sys.stderr)
            return 2
    else:
        if args.dry_run:
            print(
                "{YELLOW}--dry-run sem --queue não tem o que mostrar (ainda não há fila). "
                "Rode primeiro com --discover-only.{RESET}".format(
                    YELLOW=YELLOW, RESET=RESET
                ),
                file=sys.stderr,
            )
            return 2
        queue_path = discover(env, stream=args.show_work)

    posts = load_queue(queue_path)
    print(f"\n{BOLD}→ {len(posts)} posts na queue ({queue_path}){RESET}")
    for i, p in enumerate(posts, start=1):
        slug = p.get("slug", "(sem slug)")
        title = p.get("title", "")
        print(f"  {i:3d}. {slug}{DIM}  {title}{RESET}")

    if args.discover_only:
        print(f"\n{GREEN}✓ descoberta finalizada (--discover-only).{RESET}")
        print(
            f"{DIM}  rode novamente passando --queue {queue_path} "
            f"pra processar.{RESET}"
        )
        return 0

    if not posts:
        print(f"\n{GREEN}✓ nada pra fazer — todos os posts já têm áudio.{RESET}")
        return 0

    # Fase 2: gera áudio post a post.
    failed = 0
    skipped = 0
    processed = 0

    for i, post in enumerate(posts, start=1):
        if i < args.start:
            continue
        if args.only and i != args.only:
            continue

        slug = post.get("slug")
        if not slug:
            print(f"\n!! [{i}] post sem slug, pulando.", file=sys.stderr)
            skipped += 1
            continue

        title = post.get("title", "")
        prompt = POST_PROMPT_TEMPLATE.format(slug=slug)

        print(f"\n=== [{i}/{len(posts)}] {slug} {DIM}— {title}{RESET} ===")

        if args.dry_run:
            print(prompt)
            continue

        rc = run_claude(prompt, env, stream=args.show_work)
        if rc != 0:
            failed += 1
            print(
                f"\n!! falha no post {i} ({slug}, exit {rc}). "
                f"retome com: --queue {queue_path} --from {i}",
                file=sys.stderr,
            )
            return rc

        processed += 1
        if args.only:
            break

    print(
        f"\n{GREEN}✓ batch concluído{RESET} — "
        f"processados={processed}, pulados={skipped}, falhas={failed}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
