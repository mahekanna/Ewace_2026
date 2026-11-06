"""
run_validation.py
=================
End-to-end validation of the wavelib engine on LIVE daily data (TradingView via
tvremix MCP, snapshotted under data/live/*.json). Runs the full stack —
multi-scale auto-labeling, bottom-up degree assignment, reversal confluence, and
a causal walk-forward backtest — then writes reports/VALIDATION_2026-06.md and
SVG charts under charts/.

Run:  python3 scripts/run_validation.py                       # June-2026 baseline snapshots
      python3 scripts/run_validation.py --tag 2026-11 --symbols AVGO MRVL
                                                              # a newer data/live snapshot tag
                                                              # (e.g. from data/fetch.py)
Hand-set reversal zones apply only to the baseline tag; for any other tag the zone
is derived from the recent up-leg (zone=None), because those levels were tied to the
June-2026 structure.
"""
import argparse
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
DEFAULT_TAG = "2026-06"          # the snapshot tag the hand-set zones below were drawn on

# Semiconductor-AI watchlist. zone=None -> derived from the recent up-leg.
SYMBOLS = {
    "AVGO": {"zone": (358, 410), "desc": "Broadcom · NASDAQ:AVGO"},
    "MRVL": {"zone": (229, 266), "desc": "Marvell · NASDAQ:MRVL"},
    "NVDA": {"zone": None, "desc": "Nvidia · NASDAQ:NVDA"},
    "AMD":  {"zone": None, "desc": "AMD · NASDAQ:AMD"},
    "TSM":  {"zone": None, "desc": "TSMC · NYSE:TSM"},
    "MU":   {"zone": None, "desc": "Micron · NASDAQ:MU"},
    "ARM":  {"zone": None, "desc": "Arm Holdings · NASDAQ:ARM"},
    "SMCI": {"zone": None, "desc": "Super Micro · NASDAQ:SMCI"},
    "QCOM": {"zone": None, "desc": "Qualcomm · NASDAQ:QCOM"},
    "ASML": {"zone": None, "desc": "ASML · NASDAQ:ASML"},
    "LRCX": {"zone": None, "desc": "Lam Research · NASDAQ:LRCX"},
    "AMAT": {"zone": None, "desc": "Applied Materials · NASDAQ:AMAT"},
}
BACKTEST_WINDOW = 300   # bar-by-bar replay over the recent window (full history is too slow)


def snapshot_file(sym, tag):
    return os.path.join(LIVE, f"{sym.lower()}_1d_{tag}.json")


def load_bars(path):
    with open(path) as fh:
        d = json.load(fh)
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b["v"]) for b in d["bars"]]


def section(sym, cfg, out, tag=DEFAULT_TAG):
    """Analyze one symbol: build its rich page, run a bounded causal backtest, and
    append a compact markdown block. Returns a summary dict for the dashboard."""
    bars = load_bars(snapshot_file(sym, tag))
    zone_in = cfg.get("zone") if tag == DEFAULT_TAG else None   # hand zones are June-2026 levels
    page = f"{sym.lower()}_analysis.html" if tag == DEFAULT_TAG else f"{sym.lower()}_analysis_{tag}.html"
    data = analyze_symbol(sym, bars, zone_in, bullish=True, desc=cfg.get("desc", sym))
    render_analysis_page(data, output_path=os.path.join(CHARTS, page))
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

    last_day = datetime.datetime.fromtimestamp(bars[-1][0], datetime.timezone.utc).date()
    out.append(f"## {sym} — {cfg.get('desc', sym)}")
    out.append(f"- **{len(bars)} daily bars** through {last_day}, last close ${data['price']:,.2f}")
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
    # NeoWave (Neely) surfaced: monowave bias + S&B on the recent structure
    rp = [p for p in wl.zigzag_causal(bt, pct=0.06) if p.confirmed_t is not None]
    if len(rp) >= 4:
        lab = wl.label_monowaves(rp)
        mm = sum(1 for _w, l in lab if l.startswith(":5"))
        cc = sum(1 for _w, l in lab if l.startswith(":3"))
        nw = f"{mm} motive(:5) / {cc} corrective(:3) monowaves"
        if len(rp) >= 6:
            t5 = wl.terminal_rules(wl.pivots_to_waves(rp[-6:]))[0]
            nw += f"; terminal check: {t5.detail}"
        out.append(f"- NeoWave: {nw}")
    power = "UNDERPOWERED — too few events to claim edge" if n_ev < 6 else f"PSR {psr:.0%}"
    cpline = (f"CPCV 5th-pctile OOS profit-factor {cp[0]:.2f} ({cp[2]} folds)" if cp
              else f"CPCV needs ≥6 events (have {n_ev})")
    out.append(f"- Causal backtest (last {len(bt)} bars, score≥4, +5% target): "
               f"decided events={n_ev} hit_rate={hit:.0%}; statistical power: {power}; {cpline}")
    out.append(f"- Chart: `charts/{page}`\n")
    return {"sym": sym, "desc": cfg.get("desc", sym), "price": data["price"],
            "change": data["change"], "macro": macro, "page": page, "last_day": last_day}


def write_dashboard(summaries, tag=DEFAULT_TAG):
    """Build the index that links each symbol's standalone analysis page."""
    today = datetime.date.today().isoformat()
    asof = max(s["last_day"] for s in summaries).isoformat() if summaries else "n/a"
    cards = []
    for s in summaries:
        mc = (f"macro {s['macro']['pattern']} {s['macro']['score']:.0%}"
              if s["macro"] else "macro n/a")
        cards.append(
            f"<a class='tile' href='{s['page']}'>"
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
             f"<div class='sub'>Regenerated {today} · snapshot {tag} · data through {asof} close · "
             "analysis tooling only, not investment advice</div>"
             f"<div class='tiles'>{''.join(cards)}</div>"
             "<div class='foot'>Each page: causal ZigZag pivots &rarr; Elliott/NeoWave rule checks "
             "&rarr; Fibonacci target levels &rarr; live reversal-confluence score, drawn on the "
             "daily price line.</div></div></body></html>")
    path = os.path.join(CHARTS, f"analysis_{tag}.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(index)
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description="wavelib end-to-end validation on daily snapshots")
    ap.add_argument("--tag", default=DEFAULT_TAG,
                    help=f"data/live snapshot tag, e.g. 2026-11 (default {DEFAULT_TAG})")
    ap.add_argument("--symbols", nargs="+", default=None,
                    help="subset of symbols to run (default: all in SYMBOLS)")
    a = ap.parse_args(argv)
    tag = a.tag
    syms = [s.upper() for s in a.symbols] if a.symbols else list(SYMBOLS)
    report = os.path.join(ROOT, "reports", f"VALIDATION_{tag}.md")
    today = datetime.date.today().isoformat()
    out = ["# Validation Report — wavelib on live daily data",
           "",
           f"_Regenerated {today} by `scripts/run_validation.py` on the `{tag}` daily snapshots "
           "in `data/live/`. Analysis tooling only — not investment advice._", ""]
    summaries = []
    for sym in syms:
        cfg = SYMBOLS.get(sym, {"zone": None, "desc": sym})
        if not os.path.exists(snapshot_file(sym, tag)):
            out.append(f"## {sym} — {cfg.get('desc', sym)}\n- _data not available; skipped._\n")
            out.append("---\n")
            continue
        summaries.append(section(sym, cfg, out, tag=tag))
        out.append("---\n")
    dash = write_dashboard(summaries, tag=tag)
    out.append("### How to reproduce\n")
    cmd = "python3 scripts/run_validation.py" + ("" if tag == DEFAULT_TAG else f" --tag {tag}")
    out.append(f"```\n{cmd}\npython3 -m unittest discover -s tests\n```")
    text = "\n".join(out) + "\n"
    os.makedirs(os.path.dirname(report), exist_ok=True)
    with open(report, "w") as fh:
        fh.write(text)
    print(text)
    print(f"\nwrote {report}")
    print(f"wrote {dash}")


if __name__ == "__main__":
    main()
