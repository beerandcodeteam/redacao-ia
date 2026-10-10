#!/usr/bin/env python3
"""Gera data.json com relatório SEO completo do blog Beer & Code.
Fontes: Google Search Console, GA4, DataForSEO, PageSpeed Insights.
Cada fonte é isolada — falha em uma não derruba o resto.

Uso:
    GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/application_default_credentials.json \
    seo-report/.venv/bin/python seo-report/generate.py [--days 90]
"""
import os, sys, json, base64, datetime, traceback, pathlib

import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent  # blog-posts/

# ---- constantes do projeto ----
SITE = "https://blog.beerandcode.com.br/"
DOMAIN = "blog.beerandcode.com.br"
GSC_TOKEN = os.path.expanduser("~/.config/mcp-gsc/token.json")
DFS_LOCATION = "Brazil"
DFS_LANGUAGE = "pt"

DAYS = 90
if "--days" in sys.argv:
    DAYS = int(sys.argv[sys.argv.index("--days") + 1])

END = datetime.date.today()
START = END - datetime.timedelta(days=DAYS)


def load_env():
    env = {}
    envfile = ROOT / ".env"
    if envfile.exists():
        for line in envfile.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def dfs_creds():
    """DataForSEO creds do .env (ou do ambiente)."""
    user = ENV.get("DATAFORSEO_USERNAME") or os.environ.get("DATAFORSEO_USERNAME")
    pwd = ENV.get("DATAFORSEO_PASSWORD") or os.environ.get("DATAFORSEO_PASSWORD")
    if not user or not pwd:
        raise RuntimeError(
            "DATAFORSEO_USERNAME/DATAFORSEO_PASSWORD ausentes no .env "
            f"({ROOT / '.env'}) e no ambiente."
        )
    return user, pwd


ENV = load_env()


def ga4_property(var):
    """ID numérico da property GA4 vem do .env (ou do ambiente); aceita só o número
    ou já no formato 'properties/123'."""
    raw = (ENV.get(var) or os.environ.get(var) or "").strip()
    if not raw:
        raise RuntimeError(f"{var} ausente no .env ({ROOT / '.env'}) e no ambiente.")
    return raw if raw.startswith("properties/") else f"properties/{raw}"


GA4_PROPERTY = ga4_property("GA4_PROPERTY_ID")            # blog
GA4_SITE_PROPERTY = ga4_property("GA4_SITE_PROPERTY_ID")  # site principal (funil)
report = {
    "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
    "period": {"start": START.isoformat(), "end": END.isoformat(), "days": DAYS},
    "site": SITE,
    "sources": {},
    "errors": {},
}


def section(name):
    def deco(fn):
        def wrapped():
            print(f"[{name}] ...", flush=True)
            try:
                report["sources"][name] = fn()
                report["errors"].pop(name, None)
                print(f"[{name}] OK", flush=True)
            except Exception as e:
                report["errors"][name] = f"{type(e).__name__}: {e}"
                print(f"[{name}] FAIL: {e}", flush=True)
                traceback.print_exc()
        return wrapped
    return deco


# ============================ GSC ============================
@section("gsc")
def gsc():
    creds = Credentials.from_authorized_user_file(GSC_TOKEN)
    sc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

    def q(dimensions, rowLimit=25):
        return sc.searchanalytics().query(siteUrl=SITE, body={
            "startDate": START.isoformat(), "endDate": END.isoformat(),
            "dimensions": dimensions, "rowLimit": rowLimit,
        }).execute().get("rows", [])

    def fmt(rows, key="keys0"):
        out = []
        for r in rows:
            out.append({
                "key": r["keys"][0] if r.get("keys") else None,
                "clicks": r.get("clicks", 0),
                "impressions": r.get("impressions", 0),
                "ctr": round(r.get("ctr", 0) * 100, 2),
                "position": round(r.get("position", 0), 1),
            })
        return out

    # totals
    totrows = sc.searchanalytics().query(siteUrl=SITE, body={
        "startDate": START.isoformat(), "endDate": END.isoformat(), "dimensions": [],
    }).execute().get("rows", [])
    tot = totrows[0] if totrows else {}
    totals = {
        "clicks": tot.get("clicks", 0),
        "impressions": tot.get("impressions", 0),
        "ctr": round(tot.get("ctr", 0) * 100, 2),
        "position": round(tot.get("position", 0), 1),
    }

    # timeseries by date
    ts = []
    for r in q(["date"], rowLimit=400):
        ts.append({
            "date": r["keys"][0],
            "clicks": r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1),
        })
    ts.sort(key=lambda x: x["date"])

    top_queries = fmt(q(["query"], 50))
    top_pages = fmt(q(["page"], 50))

    # oportunidades: posição 5-15, ordenado por impressões (quick wins)
    opps = [x for x in fmt(q(["query"], 200)) if 5 <= x["position"] <= 15]
    opps.sort(key=lambda x: x["impressions"], reverse=True)

    return {
        "totals": totals,
        "timeseries": ts,
        "top_queries": top_queries,
        "top_pages": top_pages,
        "opportunities": opps[:30],
    }


# ============================ GA4 ============================
@section("ga4")
def ga4():
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest, DateRange, Dimension, Metric, OrderBy,
    )
    import google.auth
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/analytics.readonly"])
    client = BetaAnalyticsDataClient(credentials=creds)
    dr = [DateRange(start_date=f"{DAYS}daysAgo", end_date="today")]

    def run(dims, mets, order_metric=None, limit=25, desc=True):
        req = RunReportRequest(
            property=GA4_PROPERTY, date_ranges=dr,
            dimensions=[Dimension(name=d) for d in dims],
            metrics=[Metric(name=m) for m in mets],
            limit=limit,
        )
        if order_metric:
            req.order_bys = [OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_metric), desc=desc)]
        resp = client.run_report(req)
        rows = []
        for r in resp.rows:
            d = {dims[i]: r.dimension_values[i].value for i in range(len(dims))}
            for i, m in enumerate(mets):
                d[m] = r.metric_values[i].value
            rows.append(d)
        return rows

    totals_rows = run([], ["sessions", "totalUsers", "engagedSessions",
                           "averageSessionDuration", "engagementRate", "screenPageViews"], limit=1)
    totals = totals_rows[0] if totals_rows else {}

    ts = run(["date"], ["sessions", "totalUsers"], limit=400)
    for r in ts:
        d = r["date"]
        r["date"] = f"{d[:4]}-{d[4:6]}-{d[6:]}"
    ts.sort(key=lambda x: x["date"])

    channels = run(["sessionDefaultChannelGroup"], ["sessions"], "sessions", 12)
    landing = run(["landingPagePlusQueryString"], ["sessions", "engagementRate"], "sessions", 25)
    KEY = ["cta_click", "audio_play", "read_complete", "chat_message", "search",
           "copy_code", "share_click", "outbound_click"]
    ev_all = run(["eventName"], ["eventCount"], "eventCount", 100)
    key_events = [e for e in ev_all if e["eventName"] in KEY]

    return {
        "totals": totals,
        "timeseries": ts,
        "channels": channels,
        "landing": landing,
        "key_events": key_events,
    }


# ============================ Funil blog → site ============================
@section("funnel")
def funnel():
    """Funil cross-property: audiência do blog (GA4_PROPERTY_ID) → chegada e conversão
    no site principal (GA4_SITE_PROPERTY_ID). Origem no site = sessionSource contendo
    "blog" (cobre utm_source=blog e referral blog.beerandcode.com.br)."""
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest, DateRange, Dimension, Metric, OrderBy,
        Filter, FilterExpression, FilterExpressionList,
    )
    import google.auth
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/analytics.readonly"])
    client = BetaAnalyticsDataClient(credentials=creds)
    dr = [DateRange(start_date=f"{DAYS}daysAgo", end_date="today")]

    def run(prop, dims, mets, dim_filter=None, limit=50, order_metric=None):
        req = RunReportRequest(
            property=prop, date_ranges=dr,
            dimensions=[Dimension(name=d) for d in dims],
            metrics=[Metric(name=m) for m in mets],
            limit=limit,
        )
        if dim_filter is not None:
            req.dimension_filter = dim_filter
        if order_metric:
            req.order_bys = [OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_metric), desc=True)]
        rows = []
        for r in client.run_report(req).rows:
            d = {dims[i]: r.dimension_values[i].value for i in range(len(dims))}
            for i, m in enumerate(mets):
                d[m] = int(float(r.metric_values[i].value or 0))
            rows.append(d)
        return rows

    def ev_in(names):
        return FilterExpression(filter=Filter(
            field_name="eventName", in_list_filter=Filter.InListFilter(values=names)))

    def contains(field, value):
        return FilterExpression(filter=Filter(field_name=field, string_filter=Filter.StringFilter(
            match_type=Filter.StringFilter.MatchType.CONTAINS, value=value)))

    def and_(*exprs):
        return FilterExpression(and_group=FilterExpressionList(expressions=list(exprs)))

    # ---- lado blog ----
    tot = run(GA4_PROPERTY, [], ["totalUsers", "sessions"], limit=1)
    blog_users = tot[0]["totalUsers"] if tot else 0
    blog_sessions = tot[0]["sessions"] if tot else 0
    ev = {r["eventName"]: r for r in run(
        GA4_PROPERTY, ["eventName"], ["eventCount", "totalUsers"],
        ev_in(["read_complete", "cta_click"]))}
    cta_locations = [
        {"location": r.get("customEvent:cta_location") or "(not set)",
         "events": r["eventCount"], "users": r["totalUsers"]}
        for r in run(GA4_PROPERTY, ["customEvent:cta_location"], ["eventCount", "totalUsers"],
                     ev_in(["cta_click"]), limit=20, order_metric="eventCount")
    ]

    # ---- lado site (beerandcode.com.br) ----
    blog_src = contains("sessionSource", "blog")
    arr = run(GA4_SITE_PROPERTY, [], ["sessions", "totalUsers"], blog_src, limit=1)
    CONV = ["view_item", "generate_lead", "begin_checkout", "purchase"]
    conv_blog = run(GA4_SITE_PROPERTY, ["eventName"], ["eventCount", "totalUsers"],
                    and_(blog_src, ev_in(CONV)))
    conv_all = run(GA4_SITE_PROPERTY, ["eventName"], ["eventCount", "totalUsers"], ev_in(CONV))
    pages_blog = run(GA4_SITE_PROPERTY, ["pagePath"], ["sessions", "totalUsers"],
                     blog_src, limit=12, order_metric="sessions")

    def evrow(d, name):
        r = next((x for x in d if x["eventName"] == name), {})
        return {"events": r.get("eventCount", 0), "users": r.get("totalUsers", 0)}

    return {
        "blog_property": GA4_PROPERTY,
        "site_property": GA4_SITE_PROPERTY,
        "blog": {
            "users": blog_users,
            "sessions": blog_sessions,
            "read_complete": {"events": ev.get("read_complete", {}).get("eventCount", 0),
                              "users": ev.get("read_complete", {}).get("totalUsers", 0)},
            "cta_click": {"events": ev.get("cta_click", {}).get("eventCount", 0),
                          "users": ev.get("cta_click", {}).get("totalUsers", 0)},
            "cta_locations": cta_locations,
        },
        "site": {
            "arrivals": {"sessions": arr[0]["sessions"] if arr else 0,
                         "users": arr[0]["totalUsers"] if arr else 0},
            "view_item": evrow(conv_blog, "view_item"),
            "generate_lead": evrow(conv_blog, "generate_lead"),
            "begin_checkout": evrow(conv_blog, "begin_checkout"),
            "purchase": evrow(conv_blog, "purchase"),
            "totals_all_sources": {c: evrow(conv_all, c) for c in CONV},
            "top_pages_blog": pages_blog,
        },
    }


# ============================ DataForSEO ============================
@section("dataforseo")
def dataforseo():
    user, pwd = dfs_creds()
    auth = base64.b64encode(f"{user}:{pwd}".encode()).decode()
    H = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
    BASE = "https://api.dataforseo.com/v3"

    def post(path, payload):
        r = requests.post(BASE + path, headers=H, json=[payload], timeout=120)
        d = r.json()
        task = d.get("tasks", [{}])[0]
        return task.get("result") or []

    out = {}

    # 1. keywords que o domínio JÁ rankeia (uma chamada)
    ranked = post("/dataforseo_labs/google/ranked_keywords/live", {
        "target": DOMAIN, "location_name": DFS_LOCATION, "language_code": DFS_LANGUAGE,
        "limit": 100, "order_by": ["ranked_serp_element.serp_item.rank_group,asc"],
    })
    rk = []
    items = (ranked[0].get("items") if ranked else []) or []
    for it in items:
        kd = it.get("keyword_data", {})
        ki = kd.get("keyword_info", {})
        se = it.get("ranked_serp_element", {}).get("serp_item", {})
        rk.append({
            "keyword": kd.get("keyword"),
            "position": se.get("rank_group"),
            "volume": ki.get("search_volume"),
            "cpc": ki.get("cpc"),
            "competition": ki.get("competition"),
            "url": se.get("url"),
        })
    out["ranked_keywords"] = rk

    # 2. ideias "quentes" no nicho — keyword_suggestions por seed do pilar.
    # suggestions retorna SÓ keywords que contêm o seed (relevância garantida),
    # ao contrário de keyword_ideas (expande fuzzy e vaza off-topic).
    seeds = ["agentes de ia", "claude", "mcp", "rag", "engenharia de prompt",
             "llm", "ia para desenvolvedores", "laravel ia"]
    seen = {}
    for seed in seeds:
        res = post("/dataforseo_labs/google/keyword_suggestions/live", {
            "keyword": seed, "location_name": DFS_LOCATION, "language_code": DFS_LANGUAGE,
            "limit": 40,
            "filters": [["keyword_info.search_volume", ">", 30]],
            "order_by": ["keyword_info.search_volume,desc"],
        })
        items = (res[0].get("items") if res else []) or []
        for it in items:
            kw = it.get("keyword")
            if not kw or kw in seen:
                continue
            ki = it.get("keyword_info", {})
            kp = it.get("keyword_properties", {})
            trend = ki.get("monthly_searches") or []
            vols = [m.get("search_volume", 0) for m in trend][:6]
            growth = None
            if len(vols) >= 6 and sum(vols[3:]) > 0:
                growth = round((sum(vols[:3]) - sum(vols[3:])) / sum(vols[3:]) * 100)
            seen[kw] = {
                "keyword": kw,
                "volume": ki.get("search_volume"),
                "difficulty": kp.get("keyword_difficulty"),
                "cpc": ki.get("cpc"),
                "competition": ki.get("competition_level"),
                "growth_pct": growth,
                "seed": seed,
            }
    hot = list(seen.values())
    # ordena por crescimento desc (quentes), depois volume
    hot.sort(key=lambda x: ((x["growth_pct"] or -999), (x["volume"] or 0)), reverse=True)
    out["hot_keywords"] = hot[:50]

    return out


# ============================ PageSpeed ============================
@section("pagespeed")
def pagespeed():
    key = ENV.get("PAGESPEED_API_KEY")
    if not key:
        raise RuntimeError("PAGESPEED_API_KEY ausente no .env")

    # mede home + top 4 páginas do GSC (se disponíveis)
    urls = [SITE]
    gsc_data = report["sources"].get("gsc", {})
    for p in gsc_data.get("top_pages", [])[:4]:
        if p["key"] and p["key"] not in urls:
            urls.append(p["key"])

    results = []
    for url in urls:
        for strat in ("mobile", "desktop"):
            r = requests.get(
                "https://www.googleapis.com/pagespeedonline/v5/runPagespeed",
                params={"url": url, "strategy": strat, "key": key,
                        "category": "performance"},
                timeout=120,
            )
            d = r.json()
            lh = d.get("lighthouseResult", {})
            audits = lh.get("audits", {})
            def metric(aid):
                return audits.get(aid, {}).get("displayValue")
            results.append({
                "url": url, "strategy": strat,
                "performance": round(lh.get("categories", {}).get("performance", {}).get("score", 0) * 100),
                "lcp": metric("largest-contentful-paint"),
                "cls": metric("cumulative-layout-shift"),
                "tbt": metric("total-blocking-time"),
                "fcp": metric("first-contentful-paint"),
                "speed_index": metric("speed-index"),
            })
    return {"results": results}


# ---- run ----
# --only gsc,ga4  -> re-puxa só essas fontes e MESCLA no data.json existente
# (DataForSEO/PageSpeed independem da janela de datas, não precisam re-rodar).
ONLY = None
if "--only" in sys.argv:
    ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    prev_file = HERE / "data.json"
    if prev_file.exists():
        prev = json.loads(prev_file.read_text())
        report["sources"] = prev.get("sources", {})
        report["errors"] = prev.get("errors", {})

ALL = {"gsc": gsc, "ga4": ga4, "funnel": funnel, "dataforseo": dataforseo, "pagespeed": pagespeed}
run = ONLY or set(ALL)
for name in ("gsc", "ga4", "funnel", "dataforseo", "pagespeed"):
    if name in run:
        ALL[name]()

out = HERE / "data.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(f"\n-> {out}")
print("sources OK:", [k for k in report["sources"]])
if report["errors"]:
    print("ERROS:", report["errors"])
