"""
run_validation.py
=================
End-to-end validation of the wavelib engine on LIVE daily data (TradingView via
tvremix MCP, snapshotted under data/live/*.json). Runs the full stack —
multi-scale auto-labeling, bottom-up degree assignment, reversal confluence, and
a causal walk-forward backtest — then writes reports/VALIDATION_2026-06.md and
SVG charts under charts/.

Run:  python3 scripts/run_validation.py
"""
import datetime
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import wavelib as wl
from wavelib.report_chart import analyze_symbol, render_analysis_page

LIVE = os.path.join(ROOT, "data", "live")
CHARTS = os.path.join(ROOT, "charts")
REPORT = os.path.join(ROOT, "reports", "VALIDATION_2026-06.md")

# Semiconductor-AI watchlist. zone=None -> derived from the recent up-leg.
SYMBOLS = {
    "AVGO": {"file": "avgo_1d_2026-06.json", "zone": (358, 410), "desc": "Broadcom · NASDAQ:AVGO"},
    "MRVL": {"file": "mrvl_1d_2026-06.json", "zone": (229, 266), "desc": "Marvell · NASDAQ:MRVL"},
    "NVDA": {"file": "nvda_1d_2026-06.json", "zone": None, "desc": "Nvidia · NASDAQ:NVDA"},
    "AMD":  {"file": "amd_1d_2026-06.json",  "zone": None, "desc": "AMD · NASDAQ:AMD"},
    "TSM":  {"file": "tsm_1d_2026-06.json",  "zone": None, "desc": "TSMC · NYSE:TSM"},
    "MU":   {"file": "mu_1d_2026-06.json",   "zone": None, "desc": "Micron · NASDAQ:MU"},
}
BACKTEST_WINDOW = 300   # bar-by-bar replay over the recent window (full history is too slow)


def load_bars(fname):
    with open(os.path.join(LIVE, fname)) as fh:
        d = json.load(fh)
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b["v"]) for b in d["bars"]]


def section(sym, cfg, out):
    """Analyze one symbol: build its rich page, run a bounded causal backtest, and
    append a compact markdown block. Returns a summary dict for the dashboard."""
    bars = load_bars(cfg["file"])
    data = analyze_symbol(sym, bars, cfg.get("zone"), bullish=True, desc=cfg.get("desc", sym))
    render_analysis_page(data, output_path=os.path.join(CHARTS, f"{sym.lower()}_analysis.html"))
    zone = tuple(data["zone"])
    macro = data["macro"]

    # bounded causal replay on the recent window (full-history bar-by-bar is too slow)
    bt = bars[-BACKTEST_WINDOW:]
    rets = wl.reversal_returns(bt, score_threshold=4, min_reversal_pct=0.05,
                               degrees=(0.05, 0.10), bullish=True, min_history=60)
    n_ev = len(rets)
    hit = (sum(1 for r in rets if r > 0) / n_ev) if n_ev else 0.0
    sr = wl.sharpe_ratio(rets)
    sk, ku = wl.skew_kurt(rets)
    psr = wl.probabilistic_sharpe_ratio(sr, 0.0, n_ev, sk, ku) if n_ev >= 2 else 0.0
    cp = wl.cpcv_profit_factor(rets)
    swseq = wl.swing_sequence(bars=bt, pct=0.10)   # current developing sequence (recent window)

    out.append(f"## {sym} — {cfg.get('desc', sym)}")
    out.append(f"- **{len(bars)} daily bars**, last close ${data['price']:,.2f}")
    if macro:
        alt = ("; alternates: " + ", ".join(f"{p} {c:.0%}" for p, c in macro["alternates"])
               if macro["alternates"] else "")
        out.append(f"- Macro count (full history): primary **{macro['pattern']}** @ "
                   f"{macro['degree_label']}, **honest confidence {macro['score']:.0%}** "
                   f"(covers {macro['coverage']:.0%}){alt} — multi-year counts are ambiguous")
    out.append(f"- Recent best count: **{data['best_recent'] or 'n/a'}**; reversal zone "
               f"{zone}; live confluence **{data['score']}/7**; "
               f"EWF swing-sequence: {swseq['swings']} ({swseq['status']})")
    fc = wl.forecast_waves(bars)
    if fc:
        tg = ", ".join(f"{lab} {p:.1f}" for lab, p in fc.targets)
        out.append(f"- **Forecast next**: {fc.next_wave} → targets [{tg}], "
                   f"invalidation {fc.invalidation} (confidence {fc.confidence:.0%})")
    power = "UNDERPOWERED — too few events to claim edge" if n_ev < 6 else f"PSR {psr:.0%}"
    cpline = (f"CPCV 5th-pctile OOS profit-factor {cp[0]:.2f} ({cp[2]} folds)" if cp
              else f"CPCV needs ≥6 events (have {n_ev})")
    out.append(f"- Causal backtest (last {len(bt)} bars, score≥4, +5% target): "
               f"decided events={n_ev} hit_rate={hit:.0%}; statistical power: {power}; {cpline}")
    out.append(f"- Chart: `charts/{sym.lower()}_analysis.html`\n")
    return {"sym": sym, "desc": cfg.get("desc", sym), "price": data["price"],
            "change": data["change"], "macro": macro}


def write_dashboard(summaries):
    """Build the index that links each symbol's standalone analysis page."""
    today = datetime.date.today().isoformat()
    cards = []
    for s in summaries:
        mc = (f"macro {s['macro']['pattern']} {s['macro']['score']:.0%}"
              if s["macro"] else "macro n/a")
        cards.append(
            f"<a class='tile' href='{s['sym'].lower()}_analysis.html'>"
            f"<div class='sym'>{s['sym']}</div>"
            f"<div class='meta'>{s['desc']}</div>"
            f"<div class='meta'>last ${s['price']:,.2f} · {s['change']}</div>"
            f"<div class='meta'>{mc}</div>"
            f"<div class='open'>open chart &rarr;</div></a>")
    index = ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
             "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
             "<title>wavelib — analysis dashboard</title><style>"
             "body{background:#0a0d0f;color:#e8eef0;font-family:system-ui,sans-serif;padding:28px;margin:0}"
             ".wrap{max-width:820px;margin:0 auto}h1{font-size:24px}.sub{color:#7c8a91;margin:6px 0 22px}"
             ".tiles{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:640px){.tiles{grid-template-columns:1fr}}"
             ".tile{display:block;background:#11161a;border:1px solid #1c252b;border-radius:12px;padding:20px;"
             "text-decoration:none;color:#e8eef0}.tile:hover{border-color:#27e0c4}"
             ".sym{font-size:22px;font-weight:700;color:#27e0c4}.meta{font-size:12.5px;color:#cdd6da;margin-top:6px}"
             ".open{margin-top:12px;font-size:12px;color:#f2b134}.foot{color:#7c8a91;font-size:11px;margin-top:24px}"
             "</style></head><body><div class='wrap'>"
             "<h1>Elliott Wave / NeoWave — analysis dashboard</h1>"
             f"<div class='sub'>Regenerated {today} · data as of 2026-06-05 close · "
             "analysis tooling only, not investment advice</div>"
             f"<div class='tiles'>{''.join(cards)}</div>"
             "<div class='foot'>Each page: causal ZigZag pivots &rarr; Elliott/NeoWave rule checks "
             "&rarr; Fibonacci target levels &rarr; live reversal-confluence score, drawn on the "
             "daily price line.</div></div></body></html>")
    path = os.path.join(CHARTS, "analysis_2026-06.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(index)
    return path


def main():
    today = datetime.date.today().isoformat()
    out = ["# Validation Report — wavelib on live daily data",
           "",
           f"_Regenerated {today} by `scripts/run_validation.py` on TradingView/tvremix "
           "daily snapshots in `data/live/` (price data as of 2026-06-05 close). "
           "Analysis tooling only — not investment advice._", ""]
    summaries = []
    for sym, cfg in SYMBOLS.items():
        summaries.append(section(sym, cfg, out))
        out.append("---\n")
    dash = write_dashboard(summaries)
    out.append("### How to reproduce\n")
    out.append("```\npython3 scripts/run_validation.py\npython3 -m unittest discover -s tests\n```")
    text = "\n".join(out) + "\n"
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w") as fh:
        fh.write(text)
    print(text)
    print(f"\nwrote {REPORT}")
    print(f"wrote {dash}")


if __name__ == "__main__":
    main()
