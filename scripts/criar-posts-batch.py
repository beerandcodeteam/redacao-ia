#!/usr/bin/env python3
"""Roda a skill `criar-post-blog` em batch a partir de um arquivo markdown.

Formato esperado do arquivo de entrada (um post por bloco `##`):

    # Posts: 25 abril → 3 maio

    ## Skills do Claude Code para times de produto
    - publicar_em: 2026-04-26T09:00:00-03:00
    - resumo: o que são skills, como criar, quando usar vs CLAUDE.md
    - autor: lucas                        # opcional

    ## RAG com Laravel + pgvector
    - publicar_em: 2026-04-28T09:00:00-03:00
    - resumo: setup do pgvector, embeddings com OpenAI, busca semântica end-to-end

Cada `##` (h2) vira um post. O título do h2 é o tema. Os bullets carregam
metadados. Linhas livres no bloco viram resumo se `resumo:` não for declarado.

Uso:
    scripts/criar-posts-batch.py posts-25-abril-ate-03-maio.md
    scripts/criar-posts-batch.py arquivo.md --dry-run
    scripts/criar-posts-batch.py arquivo.md --from 3   # retoma do 3º post
    scripts/criar-posts-batch.py arquivo.md --only 2   # só o 2º

CTA embutido (opcional — todo o batch aponta pro mesmo destino):
    scripts/criar-posts-batch.py arquivo.md \\
        --cta-url   "https://lu.ma/beer-and-code-summit" \\
        --cta-label "Beer & Code Summit" \\
        --cta-pitch "workshop ao vivo dia 12/06 — pipeline de IA aplicada em PHP"

    O modelo recebe instrução explícita pra integrar o link em 1–2 frases
    dentro do corpo, no primeiro terço do post (~30% da leitura; conclusão só
    como fallback), sem heading "CTA" e sem caixa separada. Sem `--cta-url`,
    o post sai sem CTA.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
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


def load_env() -> dict[str, str]:
    """Lê .env do projeto e devolve dict {var: valor}."""
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


def parse_posts(text: str) -> list[dict[str, str]]:
    """Quebra o markdown em posts (uma entrada por h2)."""
    blocks = re.split(r"(?m)^##\s+(?!#)", text)
    posts: list[dict[str, str]] = []
    for block in blocks[1:]:
        lines = block.splitlines()
        if not lines:
            continue
        titulo = lines[0].strip()
        body = "\n".join(lines[1:])
        fields: dict[str, str] = {"titulo": titulo}
        free_lines: list[str] = []
        bullet_re = re.compile(
            r"^\s*[-*]\s*\*?\*?([\w_]+)\*?\*?\s*[:\-]\s*(.+?)\s*$"
        )
        for line in body.splitlines():
            m = bullet_re.match(line)
            if m:
                fields[m.group(1).lower()] = m.group(2).strip()
            elif line.strip():
                free_lines.append(line.strip())
        if "resumo" not in fields and free_lines:
            fields["resumo"] = " ".join(free_lines)
        posts.append(fields)
    return posts


def build_prompt(
    post: dict[str, str],
    cta: dict[str, str] | None = None,
) -> str:
    titulo = post.get("titulo", "").strip()
    publicar_em = (
        post.get("publicar_em")
        or post.get("data")
        or post.get("publish_at")
        or post.get("publishedat")
    )
    if not titulo:
        raise ValueError("post sem título (h2)")
    if not publicar_em:
        raise ValueError(f"post '{titulo}' não tem campo `publicar_em`")

    parts = [
        "Crie um post completo no blog Beer & Code usando a skill `criar-post-blog`.",
        "",
        f"Tema: {titulo}",
        f"Data de publicação: {publicar_em}",
    ]
    if post.get("resumo"):
        parts.append(f"Ângulo/resumo: {post['resumo']}")
    if post.get("categoria"):
        parts.append(f"Categoria sugerida: {post['categoria']}")
    if post.get("autor"):
        parts.append(f"Autor: {post['autor']}")
    if post.get("tags"):
        parts.append(f"Tags sugeridas: {post['tags']}")
    if post.get("keyword_principal"):
        parts.append(f"Keyword-alvo (SEO): {post['keyword_principal']}")
    if post.get("keywords_secundarias"):
        parts.append(f"Keywords secundárias: {post['keywords_secundarias']}")
    if post.get("hook"):
        parts.append(f"Hook/gancho: {post['hook']}")

    if cta and cta.get("url"):
        parts += [
            "",
            "CTA embutido — convite ao destino abaixo, integrado de forma orgânica ao corpo do texto:",
            f"- URL: {cta['url']}",
        ]
        if cta.get("label"):
            parts.append(f"- Nome do destino: {cta['label']}")
        if cta.get("pitch"):
            parts.append(f"- Contexto/pitch: {cta['pitch']}")
        parts += [
            "",
            (
                "Regras de integração do CTA (obrigatórias):\n"
                "1. NÃO criar seção dedicada com heading do tipo `## CTA`, "
                "`## Entra no Clã`, `## Inscreva-se`, `## Próximos passos` ou similar.\n"
                "2. NÃO usar caixa, blockquote isolado ou separadores `---` ao redor do convite.\n"
                "3. Mencionar o destino em 1–2 frases curtas, em parágrafo de prosa normal, "
                "no primeiro terço do post (~30% da leitura) — tipicamente fechando a seção "
                "de contexto, num trecho onde o tema conversa diretamente com o evento. "
                "Conclusão só como fallback se não houver encaixe natural antes; nunca os dois.\n"
                "4. Link inline em Markdown puro: `[nome do destino](url)`.\n"
                "5. Tom de convite curto. Sem hard sell. Sem 'imperdível', "
                "'última chamada', 'vagas limitadas', 'garanta sua vaga'.\n"
                "6. O leitor deve ler a frase como continuação natural do raciocínio, "
                "não como pausa comercial."
            ),
        ]

    parts += [
        "",
        (
            "Modo batch — siga o pipeline da skill (pesquisa → outline → escrita → "
            "capa → áudio → revisão SEO → publicação MCP) sem aguardar confirmação humana entre etapas. "
            "Aplique defaults sensatos quando houver ambiguidade. Só pare se faltar "
            "um dado obrigatório que não esteja acima ou se o MCP "
            "`beer-and-code-blog` não estiver carregado."
        ),
        "",
        (
            "Reforço importante — passo 5.1 (reescrita do roteiro de áudio): "
            "delegue OBRIGATORIAMENTE para o subagent `roteiro-narracao` via Agent tool "
            "(subagent_type=\"roteiro-narracao\"). Esse subagent roda em Haiku porque é "
            "transformação de texto pura e não precisa do modelo principal. NÃO reescreva "
            "o roteiro você mesmo neste passo — é desperdício de tokens caros."
        ),
        "",
        (
            "Reforço CRÍTICO — passo 5.2 (geração do áudio TTS): rode o "
            "`generate-audio.sh` como comando BLOQUEANTE em primeiro plano e espere "
            "a saída NO MESMO TURNO. É PROIBIDO rodar o áudio em background "
            "(`&`, run_in_background, nohup) e PROIBIDO usar `ScheduleWakeup` ou "
            "qualquer timer para 'voltar quando o mp3 ficar pronto'. Esta é uma "
            "sessão headless (`claude -p`) sem loop interativo: se você agendar um "
            "wakeup e encerrar o turno, a sessão morre com exit 0 e o post NUNCA é "
            "criado — falha silenciosa que faz o batch reportar sucesso sem publicar. "
            "O script é síncrono (~1–3 min): chame, espere, capture a `audio_url` da "
            "última linha do stdout e só então siga para o gate de SEO e a publicação. "
            "Não encerre o turno sem ter chamado o `create-post` do MCP."
        ),
        "",
        (
            "Reforço importante — passo 5.5 (gate de SEO, ANTES da publicação MCP): "
            "rode OBRIGATORIAMENTE a skill `revisar-seo-post` sobre o draft montado "
            "(title, body, meta_title, meta_description, excerpt, slug, tags) usando a "
            "keyword-alvo acima. Ela corrige as travas que quebram o MCP (em-dash e "
            "tamanho do meta_description, símbolos Unicode no title/slug) e revisa o SEO "
            "on-page. Em modo batch ela NÃO pede confirmação: aplica as travas + as "
            "correções seguras e segue. Publique no passo 6 com os campos corrigidos que "
            "a skill devolver, não com os campos pré-revisão."
        ),
    ]
    return "\n".join(parts)


def run_claude(prompt: str, env: dict[str, str]) -> int:
    cmd = [
        "claude",
        "-p",
        prompt,
        "--dangerously-skip-permissions",
        "--mcp-config",
        str(MCP_FILE),
    ]
    proc_env = {**os.environ, **env}
    return subprocess.call(cmd, cwd=str(PROJECT_ROOT), env=proc_env)


def _summarize_tool_input(inp: object) -> str:
    """Pega um campo representativo do input pra mostrar ao lado do tool name."""
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


def stream_claude(prompt: str, env: dict[str, str]) -> int:
    cmd = [
        "claude",
        "-p",
        prompt,
        "--dangerously-skip-permissions",
        "--mcp-config",
        str(MCP_FILE),
        "--verbose",
        "--output-format",
        "stream-json",
    ]
    proc_env = {**os.environ, **env}
    proc = subprocess.Popen(
        cmd,
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


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("input", help="arquivo markdown com a lista de posts")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="só imprime os prompts que seriam enviados ao Claude",
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
        help="rodar somente o post N e parar",
    )
    ap.add_argument(
        "--show-work",
        action="store_true",
        help="streama eventos do claude (texto, tool calls, resultados) em tempo real",
    )
    ap.add_argument(
        "--cta-url",
        help=(
            "URL do destino do CTA (evento, Clã, repositório, newsletter). "
            "Aplica a todos os posts do batch. Sem este flag, posts saem sem CTA."
        ),
    )
    ap.add_argument(
        "--cta-label",
        help="Nome do destino do CTA (ex: 'Beer & Code Summit'). Vira texto do link inline.",
    )
    ap.add_argument(
        "--cta-pitch",
        help=(
            "1 linha de contexto sobre o destino (formato, data, o que rola). "
            "Ajuda o modelo a integrar o convite com naturalidade no texto."
        ),
    )
    args = ap.parse_args()

    if (args.cta_label or args.cta_pitch) and not args.cta_url:
        print(
            "!! --cta-label e --cta-pitch só fazem sentido com --cta-url. abortando.",
            file=sys.stderr,
        )
        return 2

    cta: dict[str, str] | None = None
    if args.cta_url:
        cta = {
            "url": args.cta_url,
            "label": args.cta_label or "",
            "pitch": args.cta_pitch or "",
        }

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"arquivo não encontrado: {input_path}", file=sys.stderr)
        return 2

    posts = parse_posts(input_path.read_text())
    if not posts:
        print("nenhum post encontrado (use h2 `## Título do post`)", file=sys.stderr)
        return 2

    env = load_env()
    have = {**os.environ, **env}

    print(f"→ {len(posts)} posts em {input_path}")
    if cta:
        label = cta["label"] or "(sem label)"
        print(f"→ CTA embutido: {label} → {cta['url']}")
    if "GEMINI_API_KEY" not in have:
        print(
            "⚠  GEMINI_API_KEY ausente — a geração de capa vai falhar.",
            file=sys.stderr,
        )

    for i, post in enumerate(posts, start=1):
        if i < args.start:
            continue
        if args.only and i != args.only:
            continue

        try:
            prompt = build_prompt(post, cta=cta)
        except ValueError as e:
            print(f"\n!! [{i}] {e}. pulando.", file=sys.stderr)
            continue

        print(f"\n=== [{i}/{len(posts)}] {post.get('titulo', '(sem título)')} ===")

        if args.dry_run:
            print(prompt)
            continue

        rc = stream_claude(prompt, env) if args.show_work else run_claude(prompt, env)
        if rc != 0:
            print(
                f"\n!! falha no post {i} (exit {rc}). retome com: --from {i}",
                file=sys.stderr,
            )
            return rc

        if args.only:
            break

    print("\n✓ batch concluído")
    return 0


if __name__ == "__main__":
    sys.exit(main())
