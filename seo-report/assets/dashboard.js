/* ============ SEO Dashboard — live (data.json + Claude endpoints) ============ */
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const NS = "http://www.w3.org/2000/svg";
  const el = (n, a) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); return e; };
  const fmtN = (n) => (n == null || n === "" ? "–" : Number(n).toLocaleString("pt-BR", { maximumFractionDigits: 1 }));
  const esc = (s) => (s == null ? "" : String(s)).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
  const path = (u) => { if (!u) return "/"; let s = String(u).replace(/^https?:\/\/[^/]+/, ""); return s || "/"; };
  const trunc = (s, n) => (s && s.length > n ? s.slice(0, n) + "…" : s || "");

  function posBadge(p) {
    p = +p; const c = p < 5 ? "b-green" : p < 11 ? "b-amber" : p < 20 ? "b-orange" : "b-red";
    return `<span class="badge ${c}">${(+p).toFixed(p % 1 ? 1 : 0)}</span>`;
  }
  function perfBadge(p) {
    p = +p; const c = p >= 90 ? "b-green" : p >= 50 ? "b-amber" : "b-red";
    return `<span class="badge ${c}">${p}</span>`;
  }
  function deltaChip(v) {
    if (v == null) return "";
    const up = v >= 0; return `<span class="chip ${up ? "b-green" : "b-red"}">${up ? "+" : ""}${v}%</span>`;
  }

  /* ---------- charts (SVG, do handoff) ---------- */
  function lineChart(svg, data) {
    if (!svg || !data.length) return;
    const W = 880, H = 300, P = { t: 18, r: 46, b: 30, l: 38 };
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    const iw = W - P.l - P.r, ih = H - P.t - P.b;
    const maxC = Math.max(6, ...data.map((p) => p.clicks));
    const maxI = Math.max(50, ...data.map((p) => p.impr));
    const x = (i) => P.l + (i / (data.length - 1 || 1)) * iw;
    const yC = (v) => P.t + ih - (v / maxC) * ih;
    const yI = (v) => P.t + ih - (v / maxI) * ih;
    svg.innerHTML = "";
    for (let g = 0; g <= 3; g++) { const v = (maxC / 3) * g, yy = yC(v); svg.appendChild(el("line", { class: "grid-line", x1: P.l, y1: yy, x2: W - P.r, y2: yy })); const t = el("text", { x: P.l - 8, y: yy + 4, "text-anchor": "end" }); t.textContent = Math.round(v); svg.appendChild(t); }
    for (let g = 0; g <= 3; g++) { const v = (maxI / 3) * g, yy = yI(v); const t = el("text", { x: W - P.r + 8, y: yy + 4, "text-anchor": "start" }); t.textContent = Math.round(v); svg.appendChild(t); }
    const n = data.length, ticks = [...new Set([0, Math.floor(n * .2), Math.floor(n * .4), Math.floor(n * .6), Math.floor(n * .8), n - 1])];
    ticks.forEach((i) => { const dd = data[i].date; const lbl = dd.slice(5).replace("-", "/"); const t = el("text", { x: x(i), y: H - 10, "text-anchor": "middle" }); t.textContent = lbl; svg.appendChild(t); });
    const pp = (pts) => pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" ");
    const imprPts = data.map((p, i) => [x(i), yI(p.impr)]), clkPts = data.map((p, i) => [x(i), yC(p.clicks)]);
    const grad = el("linearGradient", { id: "imprGrad", x1: 0, y1: 0, x2: 0, y2: 1 });
    grad.appendChild(el("stop", { offset: "0%", "stop-color": "#0a84ff", "stop-opacity": "0.16" }));
    grad.appendChild(el("stop", { offset: "100%", "stop-color": "#0a84ff", "stop-opacity": "0" }));
    const defs = el("defs", {}); defs.appendChild(grad); svg.appendChild(defs);
    svg.appendChild(el("path", { d: `${pp(imprPts)} L ${x(n - 1)} ${P.t + ih} L ${P.l} ${P.t + ih} Z`, fill: "url(#imprGrad)" }));
    svg.appendChild(el("path", { d: pp(imprPts), fill: "none", stroke: "#0a84ff", "stroke-width": "1.8", "stroke-linejoin": "round" }));
    svg.appendChild(el("path", { d: pp(clkPts), fill: "none", stroke: "#ff9500", "stroke-width": "2.2", "stroke-linejoin": "round" }));
  }

  function donut(svg, segs, centerTotal) {
    if (!svg || !segs.length) return;
    const total = segs.reduce((s, x) => s + x.v, 0) || 1;
    const R = 70, r = 44, C = 100;
    svg.setAttribute("viewBox", "0 0 200 200"); svg.innerHTML = "";
    let a0 = -Math.PI / 2;
    const arc = (start, end, color) => { const large = end - start > Math.PI ? 1 : 0; const x1 = C + R * Math.cos(start), y1 = C + R * Math.sin(start), x2 = C + R * Math.cos(end), y2 = C + R * Math.sin(end), xi2 = C + r * Math.cos(end), yi2 = C + r * Math.sin(end), xi1 = C + r * Math.cos(start), yi1 = C + r * Math.sin(start); const p = el("path", { fill: color, d: `M ${x1} ${y1} A ${R} ${R} 0 ${large} 1 ${x2} ${y2} L ${xi2} ${yi2} A ${r} ${r} 0 ${large} 0 ${xi1} ${yi1} Z` }); return p; };
    segs.forEach((s) => { const a1 = a0 + (s.v / total) * Math.PI * 2; svg.appendChild(arc(a0 + 0.012, a1 - 0.012, s.c)); a0 = a1; });
    const big = el("text", { x: C, y: C - 2, "text-anchor": "middle", class: "big", fill: "#1d1d1f" }); big.textContent = (centerTotal || total).toLocaleString("pt-BR");
    const lbl = el("text", { x: C, y: C + 15, "text-anchor": "middle", class: "lbl" }); lbl.textContent = "SESSÕES";
    svg.appendChild(big); svg.appendChild(lbl);
    const leg = $("#donut-legend");
    if (leg) leg.innerHTML = segs.map((s) => `<div class="row"><span class="swatch" style="background:${s.c}"></span><span class="name">${esc(s.n)}</span><span class="pct tnum">${Math.round((s.v / total) * 100)}%</span></div>`).join("");
  }

  function spark(svg, vals, color) {
    if (!svg || !vals.length) return;
    const W = 120, H = 30, max = Math.max(...vals), min = Math.min(...vals);
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`); svg.setAttribute("preserveAspectRatio", "none");
    const x = (i) => (i / (vals.length - 1 || 1)) * W, y = (v) => H - 3 - ((v - min) / (max - min || 1)) * (H - 6);
    const d = vals.map((v, i) => (i ? "L" : "M") + x(i).toFixed(1) + " " + y(v).toFixed(1)).join(" ");
    svg.innerHTML = `<path d="${d} L ${W} ${H} L 0 ${H} Z" fill="${color}" opacity="0.1"/><path d="${d}" fill="none" stroke="${color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`;
  }

  /* ---------- sortable ---------- */
  function parseNum(s) { if (s == null) return -Infinity; s = String(s).replace(/\s/g, ""); if (/^—$|^-$|^$/.test(s)) return -Infinity; let m = s.replace("%", "").replace(/ms|s$/i, "").replace("+", "").replace(/\.(?=\d{3}\b)/g, "").replace(",", "."); const n = parseFloat(m); return isNaN(n) ? s.toLowerCase() : n; }
  function makeSortable(table) {
    const ths = table.tHead.rows[0].cells;
    Array.from(ths).forEach((th, idx) => {
      if (th.classList.contains("no-sort")) return;
      th.classList.add("sortable"); th.insertAdjacentHTML("beforeend", '<span class="arrow"></span>');
      th.addEventListener("click", () => {
        const dir = th.getAttribute("data-dir") === "asc" ? "desc" : "asc";
        Array.from(ths).forEach((o) => o.removeAttribute("data-dir")); th.setAttribute("data-dir", dir);
        const body = table.tBodies[0], rows = Array.from(body.rows);
        rows.sort((a, b) => { const av = parseNum(a.cells[idx].getAttribute("data-v") || a.cells[idx].textContent.trim()), bv = parseNum(b.cells[idx].getAttribute("data-v") || b.cells[idx].textContent.trim()); if (typeof av === "number" && typeof bv === "number") return dir === "asc" ? av - bv : bv - av; return dir === "asc" ? String(av).localeCompare(bv) : String(bv).localeCompare(av); });
        rows.forEach((r) => body.appendChild(r));
      });
    });
  }

  /* ---------- render ---------- */
  const DONUT_COLORS = ["#ff9500", "#0a84ff", "#30d158", "#5e5ce6", "#ff375f", "#64d2ff", "#bf5af2", "#8e8e93"];
  let DATA = null;

  function sumHalfDelta(series, key) {
    if (!series || series.length < 4) return null;
    const h = Math.floor(series.length / 2);
    const a = series.slice(0, h).reduce((s, x) => s + (+x[key] || 0), 0);
    const b = series.slice(h).reduce((s, x) => s + (+x[key] || 0), 0);
    if (!a) return null; return Math.round((b - a) / a * 100);
  }

  function render(d) {
    DATA = d;
    const s = d.sources || {}, g = s.gsc || {}, a = s.ga4 || {}, f = s.dataforseo || {}, ps = s.pagespeed || {};
    const wrap = $("#wrap");
    wrap.innerHTML = ""; wrap.appendChild($("#tpl-dashboard").content.cloneNode(true));

    $("#meta").textContent = `${d.period.start} → ${d.period.end} (${d.period.days}d) · gerado ${(d.generated_at || "").replace("T", " ")}`;
    const wsel = $("#window-sel"); if (wsel) wsel.value = String(d.period.days);

    // erros
    if (Object.keys(d.errors || {}).length) {
      $("#err-slot").innerHTML = `<div class="banner-err">⚠ Fontes com erro: ${Object.entries(d.errors).map(([k, v]) => `${k} (${esc(v)})`).join(" · ")}</div>`;
    }

    // KPIs
    const gt = g.totals || {}, at = a.totals || {};
    $("#kpi-clicks").textContent = fmtN(gt.clicks);
    $("#kpi-impr").textContent = fmtN(gt.impressions);
    $("#kpi-ctr").textContent = gt.ctr != null ? gt.ctr + "%" : "–";
    $("#kpi-pos").textContent = gt.position != null ? fmtN(gt.position) : "–";
    $("#kpi-sessions").textContent = fmtN(at.sessions);
    $("#kpi-users").textContent = fmtN(at.totalUsers);
    $("#kpi-engage").textContent = at.engagementRate != null ? (at.engagementRate * 100).toFixed(1) + "%" : "–";
    const di = sumHalfDelta(g.timeseries, "impressions");
    if (di != null) $("#sub-impr").innerHTML = `<span class="delta ${di >= 0 ? "up" : "down"}">${di >= 0 ? "▲" : "▼"} ${Math.abs(di)}%</span> vs. 1ª metade`;
    const dssub = sumHalfDelta(a.timeseries, "sessions");
    if (dssub != null) $("#sub-sessions").innerHTML = `<span class="delta ${dssub >= 0 ? "up" : "down"}">${dssub >= 0 ? "▲" : "▼"} ${Math.abs(dssub)}%</span> vs. 1ª metade`;

    // charts
    const ts = (g.timeseries || []).map((x) => ({ date: x.date, clicks: x.clicks, impr: x.impressions }));
    lineChart($("#line-chart"), ts);
    const tail = ts.slice(-28);
    spark($("#spark-clicks"), tail.map((p) => p.clicks), "#ff9500");
    spark($("#spark-impr"), tail.map((p) => p.impr), "#0a84ff");
    const channels = (a.channels || []).map((c, i) => ({ n: c.sessionDefaultChannelGroup || "(not set)", v: +c.sessions || 0, c: DONUT_COLORS[i % DONUT_COLORS.length] }));
    donut($("#donut-chart"), channels, +(at.sessions || 0));

    // tables
    const cellNum = (v, disp) => `<td data-v="${v == null ? "" : v}">${disp == null ? fmtN(v) : disp}</td>`;
    rows("#tb-queries", g.top_queries, (r) => `<tr><td><span class="q">${esc(r.key)}</span></td>${cellNum(r.clicks)}${cellNum(r.impressions)}${cellNum(r.ctr, r.ctr + "%")}<td data-v="${r.position}">${posBadge(r.position)}</td></tr>`);
    rows("#tb-opps", g.opportunities, (r) => `<tr><td><span class="q">${esc(r.key)}</span></td>${cellNum(r.impressions)}${cellNum(r.ctr, r.ctr + "%")}<td data-v="${r.position}">${posBadge(r.position)}</td></tr>`);
    rows("#tb-pages", g.top_pages, (r) => `<tr><td><a class="path" href="${esc(r.key)}" target="_blank" title="${esc(r.key)}">${esc(trunc(path(r.key), 64))}</a></td>${cellNum(r.clicks)}${cellNum(r.impressions)}${cellNum(r.ctr, r.ctr + "%")}<td data-v="${r.position}">${posBadge(r.position)}</td></tr>`);
    rows("#tb-hot", f.hot_keywords, (r) => `<tr><td><span class="q">${esc(r.keyword)}</span></td>${cellNum(r.volume)}${cellNum(r.difficulty)}<td data-v="${r.growth_pct == null ? "" : r.growth_pct}">${deltaChip(r.growth_pct)}</td></tr>`);
    rows("#tb-ranked", f.ranked_keywords, (r) => `<tr><td><span class="q">${esc(r.keyword)}</span></td><td data-v="${r.position}">${posBadge(r.position)}</td>${cellNum(r.volume)}</tr>`);
    rows("#tb-landing", a.landing, (r) => { const lp = r.landingPagePlusQueryString || "(not set)"; const isUrl = lp.startsWith("/") || lp.startsWith("http"); const cell = isUrl ? `<a class="path" href="${esc(lp)}" target="_blank" title="${esc(lp)}">${esc(trunc(path(lp), 60))}</a>` : `<span class="q muted">${esc(lp)}</span>`; const er = r.engagementRate != null ? (r.engagementRate * 100).toFixed(1) + "%" : "–"; return `<tr><td>${cell}</td>${cellNum(r.sessions)}<td data-v="${r.engagementRate}">${er}</td></tr>`; });
    rows("#tb-cwv", ps.results, (r) => `<tr><td><a class="path" href="${esc(r.url)}" target="_blank" title="${esc(r.url)}">${esc(trunc(path(r.url), 52))}</a></td><td><span class="device">${esc(r.strategy)}</span></td><td data-v="${r.performance}">${perfBadge(r.performance)}</td><td>${esc(r.lcp || "–")}</td><td>${esc(r.cls != null ? r.cls : "–")}</td><td>${esc(r.tbt || "–")}</td><td>${esc(r.fcp || "–")}</td></tr>`);

    // eventos-chave
    const kev = $("#key-events");
    const ke = a.key_events || [];
    if (ke.length) {
      kev.innerHTML = `<div class="tbl-scroll"><table data-sortable><thead><tr><th>Evento</th><th>Count</th></tr></thead><tbody>${ke.map((e) => `<tr><td><span class="q">${esc(e.eventName)}</span></td>${cellNum(e.eventCount)}</tr>`).join("")}</tbody></table></div>`;
    } else {
      kev.innerHTML = `<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:240px;text-align:center;gap:14px"><svg width="42" height="42" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="#c7c7cc" stroke-width="1.6"/><path d="M12 8v4l2.5 1.5" stroke="#c7c7cc" stroke-width="1.6" stroke-linecap="round"/></svg><div class="empty">Sem eventos ainda <br/>(recém-publicado).</div></div>`;
    }

    // funil blog → site
    renderFunnel(s.funnel);

    wrap.querySelectorAll("table[data-sortable]").forEach(makeSortable);
    injectInsightButtons();
  }

  function renderFunnel(fu) {
    const viz = $("#funnel-viz");
    if (!viz) return;
    if (!fu || !fu.blog) {
      viz.innerHTML = '<div class="empty" style="padding:36px;text-align:center">Sem dados de funil ainda — rode ↻ Atualizar dados.</div>';
      rows("#tb-funnel-conv", null, () => "");
      rows("#tb-funnel-cta", null, () => "");
      return;
    }
    const b = fu.blog, st = fu.site || {};
    const u = (o) => +(o || {}).users || 0;
    const steps = [
      { label: "Visitantes do blog", v: u(b), cls: "f-blog", sub: fmtN(b.sessions) + " sessões" },
      { label: "Leram até o fim", v: u(b.read_complete), cls: "f-blog", sub: "read_complete" },
      { label: "Clicaram em CTA", v: u(b.cta_click), cls: "f-blog", sub: fmtN((b.cta_click || {}).events) + " cliques" },
      { label: "Chegaram no site", v: u(st.arrivals), cls: "f-site", sub: fmtN((st.arrivals || {}).sessions) + " sessões", jump: true },
      { label: "Viraram lead", v: u(st.generate_lead), cls: "f-conv", sub: "generate_lead" },
      { label: "Iniciaram checkout", v: u(st.begin_checkout), cls: "f-conv", sub: "begin_checkout" },
      { label: "Compraram", v: u(st.purchase), cls: "f-conv", sub: "purchase" },
    ];
    const top = steps[0].v || 1;
    viz.innerHTML = steps.map((s, i) => {
      const prev = i ? steps[i - 1].v : 0;
      const pct = i ? (prev ? (s.v / prev * 100) : 0) : 100;
      const pctTxt = i ? (pct >= 10 ? Math.round(pct) : pct.toFixed(1)) + "%" : "100%";
      const w = Math.max(1.2, s.v / top * 100).toFixed(1);
      const jump = s.jump ? '<div class="funnel-jump"><span>salto de domínio · blog → beerandcode.com.br</span></div>' : "";
      return jump + `<div class="funnel-row">
        <div class="fl"><b>${esc(s.label)}</b><span>${esc(s.sub || "")}</span></div>
        <div class="fb-track"><div class="funnel-bar ${s.cls}" style="width:${w}%"></div></div>
        <div class="fv tnum"><b>${fmtN(s.v)}</b><span class="${i && pct < 15 ? "low" : ""}">${pctTxt}${i ? " da etapa ant." : ""}</span></div>
      </div>`;
    }).join("");

    // conversões: via blog vs site total
    const allT = st.totals_all_sources || {};
    const CONV_LABELS = { view_item: "Viu oferta (view_item)", generate_lead: "Lead (generate_lead)", begin_checkout: "Checkout (begin_checkout)", purchase: "Compra (purchase)" };
    const convRows = Object.keys(CONV_LABELS).map((k) => {
      const blogU = u(st[k]), totU = u(allT[k]);
      return { name: CONV_LABELS[k], blog: blogU, tot: totU, share: totU ? (blogU / totU * 100) : null };
    });
    rows("#tb-funnel-conv", convRows, (r) =>
      `<tr><td><span class="q">${esc(r.name)}</span></td><td data-v="${r.blog}">${fmtN(r.blog)}</td><td data-v="${r.tot}">${fmtN(r.tot)}</td><td data-v="${r.share == null ? "" : r.share}">${r.share == null ? "–" : (r.share < 1 && r.share > 0 ? r.share.toFixed(1) : Math.round(r.share)) + "%"}</td></tr>`);
    rows("#tb-funnel-cta", b.cta_locations, (r) =>
      `<tr><td><span class="q">${esc(r.location)}</span></td><td data-v="${r.events}">${fmtN(r.events)}</td><td data-v="${r.users}">${fmtN(r.users)}</td></tr>`);
  }

  function rows(sel, arr, fn) { const tb = $(sel); if (!tb) return; tb.innerHTML = (arr && arr.length) ? arr.map(fn).join("") : `<tr><td colspan="9" class="muted" style="text-align:center;padding:20px">(sem dados)</td></tr>`; }

  /* ---------- load + window + refresh ---------- */
  async function load() {
    try {
      const d = await (await fetch("data.json?_=" + Date.now())).json();
      render(d);
    } catch (e) {
      $("#wrap").innerHTML = `<div class="banner-err">Não consegui carregar data.json. Rode o generate.py (ou use o server.py).<br>${esc(String(e))}</div>`;
    }
  }

  function toast(msg) { let t = $(".toast"); if (!t) { t = document.createElement("div"); t.className = "toast"; document.body.appendChild(t); } t.textContent = msg; t.classList.add("show"); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("show"), 2800); }

  function initTopbar() {
    document.addEventListener("change", async (e) => {
      if (e.target.id !== "window-sel") return;
      const sel = e.target, days = +sel.value; sel.disabled = true;
      const meta = $("#meta"); const old = meta.textContent; meta.textContent = "recalculando GSC/GA4…";
      try { const j = await (await fetch("/api/window", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ days }) })).json(); if (j.ok) await load(); else { toast("Falha: " + j.error); meta.textContent = old; } }
      catch (err) { toast("server.py rodando? " + err); meta.textContent = old; }
      finally { sel.disabled = false; }
    });
    document.addEventListener("click", async (e) => {
      const r = e.target.closest("#refresh"); if (!r) return;
      r.classList.add("spinning"); toast("↻ Atualizando GSC · GA4 · DataForSEO · PageSpeed…");
      try { const j = await (await fetch("/api/refresh", { method: "POST" })).json(); if (j.ok) { await load(); toast("✓ Dados atualizados"); } else toast("Falha: " + j.error); }
      catch (err) { toast("server.py rodando? " + err); }
      finally { r.classList.remove("spinning"); }
    });
  }

  /* ---------- panels ---------- */
  function closeAll() { $("#scrim").classList.remove("open"); $("#panel").classList.remove("open"); $("#insights").classList.remove("open"); }
  function initPauta() {
    $("#open-pauta").addEventListener("click", () => { $("#insights").classList.remove("open"); $("#scrim").classList.add("open"); $("#panel").classList.add("open"); });
    $("#panel-close").addEventListener("click", closeAll);
    $("#scrim").addEventListener("click", closeAll);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeAll(); });
    $("#gerar-pauta").addEventListener("click", runPauta);
  }
  async function runPauta() {
    const btn = $("#gerar-pauta"), out = $("#pauta-out");
    const payload = { focus: $("#foco").value.trim(), goal: $("#objetivo").value, count: $("#n-posts").value, save: $("#save-pauta").checked };
    if (!payload.focus) { $("#foco").focus(); return; }
    btn.disabled = true; out.classList.add("show"); out.innerHTML = '<span class="muted">▶ Rodando Claude (planejar-pauta)…</span>';
    let acc = "";
    try {
      const resp = await fetch("/api/gerar-pauta", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
      const reader = resp.body.getReader(), dec = new TextDecoder();
      for (; ;) { const { done, value } = await reader.read(); if (done) break; acc += dec.decode(value, { stream: true }); out.innerHTML = marked.parse(acc); out.scrollTop = out.scrollHeight; }
      if (!acc.trim()) out.innerHTML = '<span class="muted">(sem saída — veja o terminal do server)</span>';
    } catch (e) { out.innerHTML = `<span class="banner-err">Erro: ${esc(String(e))}</span>`; }
    finally { btn.disabled = false; }
  }

  /* ---------- insights chat ---------- */
  const SPARKLE = '<svg viewBox="0 0 16 16" fill="none" width="13" height="13"><path d="M8 1.5l1.6 4.3 4.4.3-3.4 2.8 1.1 4.3L8 11l-3.7 2.5 1.1-4.3L2 6.1l4.4-.3z" fill="currentColor"/></svg>';
  const CHIPS = {
    performance: ["Por que o CTR está baixo?", "Quais dias puxaram os picos?", "O que priorizar esta semana?"],
    channels: ["Como crescer o orgânico?", "Direct alto é bom ou ruim?", "Vale investir em Social?"],
    top_queries: ["Quais queries viram post?", "Onde estou perdendo cliques?", "Agrupar por tema"],
    opportunities: ["Qual dá resultado mais rápido?", "Montar um cluster", "Gerar pauta destes"],
    top_pages: ["Quais páginas dar refresh?", "Oportunidades de internal link", "Risco de canibalização?"],
    hot_keywords: ["Quais valem post agora?", "Sugira 5 títulos", "Quais são efêmeras?"],
    landing: ["Onde focar conversão?", "Engajamento baixo: por quê?", "Melhorias de CRO"],
    funnel: ["Onde está o maior vazamento?", "Como levar mais leitor pro site?", "Quais CTAs melhorar primeiro?"],
    cwv: ["Como baixar o LCP mobile?", "Qual página priorizar?", "Isso afeta ranking?"],
    global: ["3 maiores oportunidades", "O que fazer esta semana?", "Maiores riscos agora"],
  };
  let chat = { card: null, sid: null, busy: false, reader: null };

  function addMsg(role, html) {
    const m = document.createElement("div"); m.className = "msg " + role;
    const who = role === "assistant" ? `<div class="who">${SPARKLE} Claude</div>` : "";
    m.innerHTML = who + `<div class="bubble">${html}</div>`;
    $("#chat-thread").appendChild(m); $("#chat-thread").scrollTop = $("#chat-thread").scrollHeight; return m;
  }
  const TYPING = `<span class="typing"><span></span><span></span><span></span></span>`;

  async function ask(message) {
    if (chat.busy) return; chat.busy = true; $("#chat-send").disabled = true;
    if (message) addMsg("user", esc(message));
    const m = addMsg("assistant", TYPING); const bub = m.querySelector(".bubble");
    let acc = "", buf = "", sidDone = false, started = false;
    try {
      const resp = await fetch("/api/insight", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ card: chat.card, session_id: chat.sid, message }) });
      if (!resp.ok) { bub.innerHTML = "Erro HTTP " + resp.status; return; }
      const reader = resp.body.getReader(), dec = new TextDecoder(); chat.reader = reader;
      for (; ;) {
        const { done, value } = await reader.read(); if (done) break;
        buf += dec.decode(value, { stream: true });
        if (!sidDone) { if (buf.startsWith("__SID__")) { const nl = buf.indexOf("\n"); if (nl < 0) continue; chat.sid = buf.slice(7, nl).trim(); buf = buf.slice(nl + 1); sidDone = true; } else if (buf.length >= 7) { sidDone = true; } else continue; }
        if (buf) { acc += buf; buf = ""; }
        if (!started && acc.trim()) started = true;
        bub.innerHTML = started ? marked.parse(acc) : TYPING;
        $("#chat-thread").scrollTop = $("#chat-thread").scrollHeight;
      }
      if (!acc.trim()) bub.innerHTML = '<span style="color:var(--text-3)">(sem resposta — veja o terminal do server)</span>';
    } catch (e) { bub.innerHTML = `<span style="color:var(--red)">Erro: ${esc(String(e))}</span>`; }
    finally { chat.busy = false; chat.reader = null; $("#chat-send").disabled = false; }
  }

  function openInsight(card, name, source) {
    chat = { card, sid: null, busy: false, reader: null };
    $("#ctx-name").textContent = name || "Métricas"; $("#ctx-source").textContent = source || "todas as fontes";
    $("#chat-thread").innerHTML = "";
    const sg = $("#chat-suggest"); sg.innerHTML = "";
    (CHIPS[card] || []).forEach((c) => { const b = document.createElement("button"); b.textContent = c; b.addEventListener("click", () => ask(c)); sg.appendChild(b); });
    $("#panel").classList.remove("open"); $("#scrim").classList.add("open"); $("#insights").classList.add("open");
    ask("");  // diagnóstico automático
  }

  function injectInsightButtons() {
    document.querySelectorAll("[data-card]").forEach((card) => {
      if (card.querySelector(".insights-btn")) return;
      const title = card.querySelector(".card-head .card-title"); if (!title) return;
      const btn = document.createElement("button"); btn.className = "insights-btn"; btn.innerHTML = SPARKLE + " Insights";
      title.insertAdjacentElement("afterend", btn);
      btn.addEventListener("click", () => openInsight(card.dataset.card, card.dataset.name, card.dataset.source));
    });
  }

  function initInsights() {
    $("#open-chat").addEventListener("click", () => openInsight("global", "Todas as métricas", "GSC · GA4 · DataForSEO · CWV"));
    $("#insights-close").addEventListener("click", () => { $("#scrim").classList.remove("open"); $("#insights").classList.remove("open"); if (chat.reader) try { chat.reader.cancel(); } catch (e) { } });
    const input = $("#chat-text");
    $("#chat-send").addEventListener("click", () => { const v = input.value.trim(); if (v) { input.value = ""; input.style.height = "auto"; ask(v); } });
    input.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); const v = input.value.trim(); if (v) { input.value = ""; input.style.height = "auto"; ask(v); } } });
    input.addEventListener("input", function () { this.style.height = "auto"; this.style.height = Math.min(this.scrollHeight, 120) + "px"; });
  }

  /* ---------- boot ---------- */
  document.addEventListener("DOMContentLoaded", () => { initTopbar(); initPauta(); initInsights(); load(); });
})();
