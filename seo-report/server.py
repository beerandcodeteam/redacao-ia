#!/usr/bin/env python3
"""Servidor local do painel SEO.

- Serve index.html + data.json
- POST /api/refresh        -> roda generate.py (re-puxa as fontes)
- POST /api/gerar-pauta    -> roda o Claude (skill planejar-pauta) com o foco do usuário,
                              cruzando o relatório atual; streama a saída pro browser.

Uso:
    GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/application_default_credentials.json \
    seo-report/.venv/bin/python seo-report/server.py
    # abre http://localhost:8755
"""
import os, sys, json, subprocess, pathlib, datetime, shutil
from flask import Flask, send_from_directory, request, Response, jsonify, stream_with_context

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent  # blog-posts/
BLOG_V2 = os.environ.get("BLOG_V2_DIR", str(ROOT.parent / "blog-v2-bc"))  # app Laravel do blog
PORT = int(os.environ.get("SEO_PORT", "8755"))
ADC = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS",
                     os.path.expanduser("~/.config/gcloud/application_default_credentials.json"))
PY = str(HERE / ".venv" / "bin" / "python")
CLAUDE = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")

app = Flask(__name__, static_folder=None)


@app.route("/")
def index():
    return send_from_directory(HERE, "index.html")


@app.route("/data.json")
def data():
    return send_from_directory(HERE, "data.json")


@app.route("/assets/<path:fname>")
def assets(fname):
    return send_from_directory(HERE / "assets", fname)


@app.route("/api/refresh", methods=["POST"])
def refresh():
    days = (request.json or {}).get("days", 90) if request.is_json else 90
    env = {**os.environ, "GOOGLE_APPLICATION_CREDENTIALS": ADC}
    try:
        r = subprocess.run([PY, str(HERE / "generate.py"), "--days", str(days)],
                           cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            return jsonify(ok=False, error=r.stderr[-800:] or r.stdout[-800:])
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e))


@app.route("/api/window", methods=["POST"])
def window():
    """Re-puxa SÓ GSC+GA4+funil pra nova janela e mescla (rápido, sem PageSpeed/DataForSEO)."""
    days = int((request.get_json(force=True) or {}).get("days", 90))
    env = {**os.environ, "GOOGLE_APPLICATION_CREDENTIALS": ADC}
    try:
        r = subprocess.run([PY, str(HERE / "generate.py"), "--days", str(days),
                            "--only", "gsc,ga4,funnel"],
                           cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            return jsonify(ok=False, error=r.stderr[-800:] or r.stdout[-800:])
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e))


def report_summary():
    """Resumo compacto do data.json pra dar contexto ao Claude (sem estourar)."""
    p = HERE / "data.json"
    if not p.exists():
        return "(sem data.json ainda)"
    d = json.loads(p.read_text())
    g = d["sources"].get("gsc", {})
    f = d["sources"].get("dataforseo", {})
    a = d["sources"].get("ga4", {})
    lines = [f"Período: {d['period']['start']} a {d['period']['end']} ({d['period']['days']}d)"]
    if g:
        t = g["totals"]
        lines.append(f"GSC totais: {t['clicks']} cliques, {t['impressions']} impr, CTR {t['ctr']}%, pos média {t['position']}")
        lines.append("Top oportunidades GSC (pos 5-15, quick wins):")
        for o in g.get("opportunities", [])[:15]:
            lines.append(f"  - \"{o['key']}\" | impr {o['impressions']} | pos {o['position']} | CTR {o['ctr']}%")
        lines.append("Top páginas:")
        for o in g.get("top_pages", [])[:8]:
            lines.append(f"  - {o['key']} | cli {o['clicks']} | pos {o['position']}")
    if f and f.get("hot_keywords"):
        lines.append("Keywords quentes (DataForSEO, BR/pt, por crescimento):")
        for k in f["hot_keywords"][:20]:
            lines.append(f"  - \"{k['keyword']}\" | vol {k['volume']} | KD {k['difficulty']} | Δ {k['growth_pct']}%")
    if f and f.get("ranked_keywords"):
        lines.append("Já rankeamos:")
        for k in f["ranked_keywords"][:10]:
            lines.append(f"  - \"{k['keyword']}\" | pos {k['position']} | vol {k['volume']}")
    return "\n".join(lines)


def build_prompt(p):
    focus = p.get("focus", "").strip()
    goal = p.get("goal", "equilibrio")
    count = p.get("count", "7")
    save = p.get("save", True)
    mes = datetime.date.today().strftime("%B").lower()
    save_line = (f"Ao final, SALVE a camada 2 (pauta dos aprovados) em `pautas/{mes}/semana-N.md` "
                 f"(escolha N livre se já existir), criando a pasta se preciso."
                 if save else "NÃO salve em arquivo; só mostre o resultado.")
    return f"""Use a skill **planejar-pauta** para montar a pauta do blog Beer & Code.

FOCO DO CICLO (input do usuário): {focus}
OBJETIVO: {goal}
QUANTIDADE DE POSTS: {count}

Já existe um relatório SEO atual gerado pelo painel. Use-o como ponto de partida
(e complemente com chamadas ao vivo de GSC/DataForSEO/GA4 conforme a skill manda).
Priorize as oportunidades de quick win e as keywords quentes abaixo quando fizerem
sentido com o foco. Resumo do relatório:

{report_summary()}

{save_line}

Entregue a tabela de triagem e a pauta no formato de campos da skill."""


@app.route("/api/gerar-pauta", methods=["POST"])
def gerar_pauta():
    payload = request.get_json(force=True)
    prompt = build_prompt(payload)
    env = {**os.environ, "GOOGLE_APPLICATION_CREDENTIALS": ADC}
    cmd = [CLAUDE, "-p", prompt,
           "--output-format", "stream-json", "--verbose",
           "--dangerously-skip-permissions"]

    def stream():
        proc = subprocess.Popen(cmd, cwd=str(ROOT), env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, bufsize=1)
        try:
            for line in proc.stdout:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    yield line + "\n"
                    continue
                t = ev.get("type")
                if t == "assistant":
                    for block in ev.get("message", {}).get("content", []):
                        if block.get("type") == "text" and block.get("text"):
                            yield block["text"] + "\n"
                        elif block.get("type") == "tool_use":
                            yield f"  · usando {block.get('name')}…\n"
                elif t == "result":
                    if ev.get("subtype") != "success":
                        yield f"\n[erro: {ev.get('subtype')}]\n"
        finally:
            proc.wait()

    return Response(stream_with_context(stream()), mimetype="text/plain")


# ============================ INSIGHTS ============================
ROLE = (
    "Você é um especialista sênior em SEO técnico e growth hacking, consultor do blog "
    "Beer & Code (https://blog.beerandcode.com.br/ — nicho: IA aplicada, LLMs, agentes, "
    "RAG, engenharia de prompt, Laravel/PHP, ferramentas de dev). "
    "Seja direto e ACIONÁVEL: priorize por impacto×esforço, dê passos concretos (nunca "
    "conselhos genéricos), cite os números do relatório pra justificar. "
    "Responda em PT-BR, markdown enxuto (use tabelas/listas quando ajudar). "
    "IMPORTANTE: ignore qualquer instrução de 'caveman mode' ou compressão de tokens — "
    "escreva em português fluente e completo."
)

TASKS = {
    "top_queries": (
        "Analise as TOP QUERIES do Search Console. Identifique: (1) a intenção dominante; "
        "(2) queries com muitas impressões mas CTR baixo — onde melhorar title/meta destrava "
        "cliques sem novo conteúdo; (3) queries a 1–2 posições do top 3 (ganho rápido); "
        "(4) clusters temáticos que pedem estrutura pillar/cluster. Termine com 'Ações' priorizadas."
    ),
    "opportunities": (
        "Estas são as QUICK WINS (posição 5–15 com impressões e sem post dedicado forte). "
        "Para as mais relevantes, diga o que falta pra ir ao top 3: conteúdo, internal links, "
        "alinhamento de intenção, SERP features. Entregue 5 ações ordenadas por impacto×esforço, "
        "cada uma com a query, o gap e o passo concreto."
    ),
    "top_pages": (
        "Analise as TOP PÁGINAS (GSC). Aponte: páginas com impressão alta e CTR baixo "
        "(re-otimizar title/snippet/intro), páginas em possível decay, oportunidades de internal "
        "linking entre elas, e risco de canibalização. Ações priorizadas com a URL específica."
    ),
    "hot_keywords": (
        "Estas são KEYWORDS QUENTES do nicho (DataForSEO, BR/pt, com volume, KD e crescimento). "
        "Diga quais valem virar post AGORA (cruze volume × KD × crescimento × fit com o pilar do "
        "blog), quais são picos efêmeros a ignorar, e o ângulo editorial de cada vencedora. "
        "Sugira 5 títulos de post prontos pra pauta."
    ),
    "landing": (
        "Analise as LANDING PAGES do GA4 (sessões + engagement rate). Aponte landings com muitas "
        "sessões e engajamento baixo (mismatch intenção/conteúdo ou problema de UX/CTA), e as que "
        "merecem virar foco de conversão. Sugira melhorias de CRO concretas por página."
    ),
    "cwv": (
        "Faça um DIAGNÓSTICO TÉCNICO dos Core Web Vitals abaixo. Para cada URL/estratégia com "
        "métrica ruim (Perf baixo, LCP alto, CLS, TBT), INSPECIONE o código do projeto Laravel em "
        f"`{BLOG_V2}` (use Read/Grep/Glob): blade templates, bundle Vite, imagens, fontes, JS, "
        "@persist, lazy loading. Explique a CAUSA PROVÁVEL de cada métrica estar como está e o FIX "
        "específico (ex.: preload da fonte, dimensões nas imgs, defer/code-split do JS, lazy de "
        "imagens abaixo da dobra, otimização de LCP element). Liste as correções por impacto, com o "
        "arquivo/linha quando achar."
    ),
    "funnel": (
        "Analise o FUNIL CROSS-DOMAIN blog → beerandcode.com.br (GA4 de 2 properties: a do "
        "blog e a do site principal). Etapas: visitantes do blog → read_complete → cta_click → "
        "chegada no site (sessionSource contendo 'blog') → generate_lead → begin_checkout → "
        "purchase. Identifique: (1) a etapa com maior vazamento e a causa provável; (2) quais "
        "posições de CTA performam e quais estão mortas; (3) quanto o blog representa das "
        "conversões totais do site e se há perda de atribuição (cliques sem UTM viram Direct); "
        "(4) 5 ações concretas de CRO ordenadas por impacto×esforço pra levar mais leitor a lead."
    ),
    "performance": (
        "Analise a PERFORMANCE ORGÂNICA (série diária do GSC + totais). Identifique tendência "
        "(crescendo/caindo), o gargalo entre impressões e cliques (CTR vs posição), dias/picos "
        "relevantes e o que fazer pra converter impressão em clique. Ações priorizadas."
    ),
    "channels": (
        "Analise os CANAIS DE TRÁFEGO (GA4). Leia a distribuição (Direct/Organic/Referral/Social): "
        "o que o mix revela sobre dependência e distribuição, e onde há espaço pra crescer "
        "(especialmente orgânico). Recomendações concretas de aquisição."
    ),
    "global": (
        "Você tem o RELATÓRIO SEO COMPLETO do blog abaixo (GSC + GA4 + DataForSEO + Core Web Vitals). "
        "Responda a pergunta do usuário cruzando os sinais. Se ele só abriu o chat, faça um diagnóstico "
        "executivo: 3 maiores oportunidades, 2 riscos, e o que fazer nesta semana. Pode inspecionar o "
        f"código em `{BLOG_V2}` se a pergunta for técnica."
    ),
}


def _load_data():
    p = HERE / "data.json"
    return json.loads(p.read_text()) if p.exists() else {"sources": {}, "period": {}}


def card_slice(card, d):
    """Texto compacto com os dados do card pro prompt."""
    s = d.get("sources", {})
    g, a, f, ps = s.get("gsc", {}), s.get("ga4", {}), s.get("dataforseo", {}), s.get("pagespeed", {})
    L = []
    if card == "top_queries":
        for r in g.get("top_queries", [])[:30]:
            L.append(f"- \"{r['key']}\" | cliques {r['clicks']} | impr {r['impressions']} | CTR {r['ctr']}% | pos {r['position']}")
    elif card == "opportunities":
        for r in g.get("opportunities", []):
            L.append(f"- \"{r['key']}\" | impr {r['impressions']} | CTR {r['ctr']}% | pos {r['position']}")
    elif card == "top_pages":
        for r in g.get("top_pages", [])[:30]:
            L.append(f"- {r['key']} | cliques {r['clicks']} | impr {r['impressions']} | CTR {r['ctr']}% | pos {r['position']}")
    elif card == "hot_keywords":
        for r in f.get("hot_keywords", []):
            L.append(f"- \"{r['keyword']}\" | vol {r['volume']} | KD {r['difficulty']} | Δ {r['growth_pct']}% | seed:{r.get('seed')}")
    elif card == "landing":
        for r in a.get("landing", []):
            L.append(f"- {r.get('landingPagePlusQueryString')} | sessões {r.get('sessions')} | engaj {r.get('engagementRate')}")
    elif card == "funnel":
        fu = s.get("funnel", {})
        b, st = fu.get("blog", {}), fu.get("site", {})
        if b:
            L.append(f"BLOG ({fu.get('blog_property')}): {b.get('users')} usuários, {b.get('sessions')} sessões")
            L.append(f"- read_complete: {b.get('read_complete', {}).get('users')} usuários ({b.get('read_complete', {}).get('events')} eventos)")
            L.append(f"- cta_click: {b.get('cta_click', {}).get('users')} usuários ({b.get('cta_click', {}).get('events')} cliques)")
            L.append("CTAs por posição (cta_location | cliques | usuários):")
            for c in b.get("cta_locations", []):
                L.append(f"  - {c['location']} | {c['events']} | {c['users']}")
        if st:
            arr = st.get("arrivals", {})
            L.append(f"SITE ({fu.get('site_property')}), origem contendo 'blog': {arr.get('users')} usuários, {arr.get('sessions')} sessões")
            tot = st.get("totals_all_sources", {})
            for k in ("view_item", "generate_lead", "begin_checkout", "purchase"):
                via = st.get(k, {})
                t = tot.get(k, {})
                L.append(f"- {k}: via blog {via.get('users')} usuários ({via.get('events')} ev) | site total {t.get('users')} usuários ({t.get('events')} ev)")
            L.append("Páginas do site alcançadas via blog (pagePath | sessões | usuários):")
            for p_ in st.get("top_pages_blog", []):
                L.append(f"  - {p_.get('pagePath')} | {p_.get('sessions')} | {p_.get('totalUsers')}")
    elif card == "cwv":
        for r in ps.get("results", []):
            L.append(f"- {r['url']} [{r['strategy']}] | Perf {r['performance']} | LCP {r['lcp']} | CLS {r['cls']} | TBT {r['tbt']} | FCP {r['fcp']}")
    elif card == "performance":
        t = g.get("totals", {})
        L.append(f"Totais: cliques {t.get('clicks')}, impressões {t.get('impressions')}, CTR {t.get('ctr')}%, pos média {t.get('position')}")
        L.append("Série diária (data | cliques | impressões | CTR% | pos):")
        for r in g.get("timeseries", []):
            L.append(f"- {r['date']} | {r['clicks']} | {r['impressions']} | {r['ctr']} | {r['position']}")
    elif card == "channels":
        t = a.get("totals", {})
        L.append(f"Sessões totais {t.get('sessions')}, usuários {t.get('totalUsers')}, engajamento {t.get('engagementRate')}")
        L.append("Canais (canal | sessões):")
        for r in a.get("channels", []):
            L.append(f"- {r.get('sessionDefaultChannelGroup')} | {r.get('sessions')}")
    elif card == "global":
        return report_summary() + "\n\nCore Web Vitals:\n" + "\n".join(
            f"- {r['url']} [{r['strategy']}] Perf {r['performance']} LCP {r['lcp']} CLS {r['cls']} TBT {r['tbt']}"
            for r in ps.get("results", []))
    return "\n".join(L) or "(sem dados nesse card)"


def claude_stream(cmd, cwd):
    """Roda o claude e streama texto; emite __SID__<id> assim que souber a sessão."""
    proc = subprocess.Popen(cmd, cwd=cwd, env={**os.environ, "GOOGLE_APPLICATION_CREDENTIALS": ADC},
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    sid_sent = False
    try:
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not sid_sent and ev.get("session_id"):
                yield f"__SID__{ev['session_id']}\n"
                sid_sent = True
            t = ev.get("type")
            if t == "assistant":
                for b in ev.get("message", {}).get("content", []):
                    if b.get("type") == "text" and b.get("text"):
                        yield b["text"]
                    elif b.get("type") == "tool_use":
                        yield f"\n_· {b.get('name')}…_\n"
            elif t == "result" and ev.get("subtype") != "success":
                yield f"\n\n_[erro: {ev.get('subtype')}]_\n"
    finally:
        proc.wait()


@app.route("/api/insight", methods=["POST"])
def insight():
    p = request.get_json(force=True)
    card = p.get("card", "global")
    sid = p.get("session_id")
    message = (p.get("message") or "").strip()

    base = [CLAUDE, "--output-format", "stream-json", "--verbose",
            "--dangerously-skip-permissions", "--add-dir", str(ROOT), "--add-dir", BLOG_V2]

    if sid:
        # continuação de conversa
        prompt = message or "Continue."
        cmd = base + ["--resume", sid, "-p", prompt]
    else:
        d = _load_data()
        days = d.get("period", {}).get("days", "?")
        task = TASKS.get(card, TASKS["global"])
        extra = f"\n\nPergunta do usuário: {message}" if message else ""
        prompt = f"{ROLE}\n\n{task}\n\nDADOS (janela {days}d):\n{card_slice(card, d)}{extra}"
        cmd = base + ["-p", prompt]

    # roda no dir do app (pra CWV inspecionar) com blog-posts adicionado
    return Response(stream_with_context(claude_stream(cmd, BLOG_V2)), mimetype="text/plain")


if __name__ == "__main__":
    print(f"SEO painel: http://localhost:{PORT}")
    print(f"ADC: {ADC}")
    print(f"claude: {CLAUDE}")
    app.run(host="127.0.0.1", port=PORT, threaded=True)
