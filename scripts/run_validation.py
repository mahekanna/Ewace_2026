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

LIVE = os.path.join(ROOT, "data", "live")
CHARTS = os.path.join(ROOT, "charts")
REPORT = os.path.join(ROOT, "reports", "VALIDATION_2026-06.md")

# documented structural reversal zones + bias (README / DOCUMENTATION)
SYMBOLS = {
    "AVGO": {"file": "avgo_1d_2026-06.json", "zone": (358, 410), "bullish": True},
    "MRVL": {"file": "mrvl_1d_2026-06.json", "zone": (229, 266), "bullish": True},
}


def load_bars(fname):
    with open(os.path.join(LIVE, fname)) as fh:
        d = json.load(fh)
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b["v"]) for b in d["bars"]]


def section(sym, cfg, out):
    bars = load_bars(cfg["file"])
    last = bars[-1]
    out.append(f"## {sym} — {len(bars)} daily bars, last close {last[4]:.2f}\n")

    # 1) multi-scale pivots
    streams = wl.zigzag_multiscale(bars, scales=(0.05, 0.10, 0.15))
    counts = {s: len(v) for s, v in streams.items()}
    out.append(f"**Multi-scale pivots** (scale→count): {counts}  "
               f"— non-increasing with scale: "
               f"{all(a >= b for a, b in zip(list(counts.values()), list(counts.values())[1:]))}\n")

    # 2) auto-labeling
    cands = wl.label_and_validate(bars, degrees=(0.05, 0.10, 0.15), max_candidates=5)
    out.append(f"**Auto-labeling** (`label_and_validate`) → {len(cands)} candidate(s):\n")
    out.append("| rank | type | degree | hard_fails | warns | fib_score |")
    out.append("|---|---|---|---|---|---|")
    for i, c in enumerate(cands, 1):
        out.append(f"| {i} | {c.count_type} | {c.degree} | {c.hard_fails} | {c.warns} | {c.fib_score:.2f} |")
    out.append("")

    # 3) bottom-up degree
    deg = wl.assign_degrees_neely(bars, base_scale=0.05)
    types = {}
    for c in deg:
        types[c.count_type] = types.get(c.count_type, 0) + 1
    out.append(f"**Auto-degree** (`assign_degrees_neely`) → {len(deg)} validated candidate(s) "
               f"{types}; all degree_confidence="
               f"{set(c.degree_confidence for c in deg) or '{}'}\n")

    # 4) reversal confluence at the documented zone
    rep = wl.score_reversal(sym, bars, cfg["zone"], bullish=cfg["bullish"])
    out.append(f"**Reversal confluence** at zone {cfg['zone']} (bullish={cfg['bullish']}):\n")
    out.append("```")
    out.append(str(rep).strip())
    out.append("```")
    if getattr(rep, "warnings", None):
        out.append(f"_warnings: {rep.warnings}_\n")

    # 5) causal backtest + walk-forward
    flat = wl.backtest_reversals(bars, score_threshold=4, min_reversal_pct=0.05,
                                 degrees=(0.05, 0.10), bullish=cfg["bullish"], min_history=60)
    out.append("**Causal backtest** (whole series, score≥4, reversal=+5%):")
    out.append(f"- signals={flat.n_signals} reversals={flat.n_reversals} "
               f"invalidations={flat.n_invalidations} open={flat.n_open} "
               f"hit_rate={flat.hit_rate:.2f} profit_factor={flat.profit_factor:.2f}")
    wfo = wl.backtest_reversals(bars, score_threshold=4, degrees=(0.05, 0.10),
                                bullish=cfg["bullish"], min_history=60,
                                wfo_train_size=120, wfo_test_size=40, wfo_step_size=40)
    out.append(f"- walk-forward efficiency (OOS/IS PF): {wfo.wfe}")
    out.append("")

    # 6) chart
    waves = wl.pivots_to_waves(wl.zigzag_causal(bars, pct=0.08))
    svg_path = os.path.join(CHARTS, f"{sym.lower()}_1d_auto.svg")
    wl.render_chart(waves, zones=[cfg["zone"]], title=f"{sym} 1D — auto zigzag (pct=0.08)",
                    output_path=svg_path)
    out.append(f"**Chart:** `charts/{sym.lower()}_1d_auto.svg` ({len(waves)} legs)\n")
    return {"sym": sym, "last": last[4], "zone": cfg["zone"], "score": rep.score,
            "type": cands[0].count_type if cands else "-",
            "fib": cands[0].fib_score if cands else 0.0,
            "svg": f"{sym.lower()}_1d_auto.svg"}


def write_dashboard(summaries):
    """Build a single self-contained HTML dashboard embedding the SVG charts."""
    today = datetime.date.today().isoformat()
    blocks = []
    for s in summaries:
        with open(os.path.join(CHARTS, s["svg"])) as fh:
            svg = fh.read()
        tier = ("HIGH-CONFIDENCE" if s["score"] >= 4
                else "BUILDING — not yet confirmed" if s["score"] >= 2
                else "structurally allowed only")
        blocks.append(
            f'<section><h2>{s["sym"]} — last close {s["last"]:.2f}</h2>'
            f'<p>Auto-detected best count: <b>{s["type"]}</b> '
            f'(quality {s["fib"]:.0%}) at zone {s["zone"][0]}-{s["zone"][1]}. '
            f'Reversal confluence: <b>{s["score"]}/7</b> ({tier}).</p>'
            f'<div class="chart">{svg}</div></section>')
    html = (
        "<!doctype html><meta charset='utf-8'>"
        "<title>wavelib — wave analysis dashboard</title>"
        "<style>body{font-family:sans-serif;max-width:1000px;margin:24px auto;color:#222;"
        "padding:0 16px}h1{margin-bottom:4px}.sub{color:#666;margin-top:0}"
        "section{margin:28px 0;border-top:1px solid #eee;padding-top:12px}"
        ".chart{border:1px solid #eee;border-radius:6px;overflow:auto}"
        "p{line-height:1.5}</style>"
        "<h1>Elliott Wave / NeoWave — analysis dashboard</h1>"
        f"<p class='sub'>Regenerated {today} · data as of 2026-06-05 close · "
        "analysis tooling only, not investment advice</p>"
        + "".join(blocks))
    path = os.path.join(CHARTS, "analysis_2026-06.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
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
