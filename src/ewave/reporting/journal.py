"""
journal.py — the TRADING JOURNAL: every trade the system actually took, why it
took it, and what happened. Built for a human trader to read, not for the engine.
============================================================================
This is the honest answer to "on what basis, and what happened earlier":

- It logs EVERY trade over the WHOLE tested history (wins AND losses), not a
  cherry-picked recent snapshot. Losing trades are shown in full.
- Each row states the exact BASIS: the wave-1 pivots (origin -> broken high),
  the wave-2 retracement %, the confirmation break level (= entry), the
  structural stop (beyond wave-2), and the Fibonacci target.
- It is CAUSAL: `setup_confirmed_t` shows the bar at which the setup became
  knowable; every trade fired on a later bar's close (no repainting). The
  ghost-forward's no-lookahead proof covers the same pipeline.
- It shows SELECTIVITY: the count of trades vs the number of bars scanned — the
  signal fires on a small fraction of candles, and ONLY when R1 + the wave-2
  band + the break confirmation all pass. It does NOT label every stock or
  every swing (that is the analysis report's cosmetic pivot markers, a
  different thing — see docs/RULE_COVERAGE.md).

`ewave journal --symbols AVGO,MRVL --tf 1h --profile experimental`
"""
from __future__ import annotations

import datetime
import html
from pathlib import Path

from ..backtest.engine import backtest_wave3
from ..backtest.fills import FillModel


def _d(t):
    return datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d %H:%M")


def _day(t):
    return datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")


def build_records(symbol, bars, profile, fill_model=None):
    """Run the causal backtest and turn trades into journal records + summary."""
    fm = fill_model or FillModel.from_config()
    trades = backtest_wave3(bars, profile, fill_model=fm)
    recs, cum = [], 0.0
    for i, t in enumerate(trades, 1):
        cum += t.r
        risk = abs(t.entry - t.stop)
        lag_bars = None
        if t.setup_confirmed_t and t.signal_time:
            lag_bars = sum(1 for b in bars
                           if t.setup_confirmed_t <= b[0] <= t.signal_time) - 1
        recs.append({
            "n": i, "symbol": symbol, "dir": t.direction,
            "signal": t.signal_time, "exit": t.exit_time,
            "w1_origin": t.w1_origin, "w1_extreme": t.w1_extreme,
            "w2": t.w2_extreme, "retr": t.retr,
            "entry": t.entry, "stop": t.stop, "target": t.target_1,
            "risk": round(risk, 4), "rr": t.planned_rr,
            "r": t.r, "outcome": t.outcome, "bars_held": t.bars_held,
            "cum_r": round(cum, 3), "strands": t.strands,
            "confirm_lag_bars": lag_bars,
        })
    wins = [r for r in recs if r["r"] > 0]
    gains = sum(r["r"] for r in wins)
    losses = -sum(r["r"] for r in recs if r["r"] < 0)
    n = len(recs)
    scanned = max(len(bars) - 60, 1)
    summ = {
        "symbol": symbol, "trades": n,
        "bars_scanned": scanned,
        "fire_rate_pct": round(100.0 * n / scanned, 2),
        "wins": len(wins), "win_rate": round(len(wins) / n, 4) if n else None,
        "total_r": round(sum(r["r"] for r in recs), 3) if n else 0.0,
        "expectancy_r": round(sum(r["r"] for r in recs) / n, 4) if n else None,
        "profit_factor": round(gains / losses, 3) if losses else None,
        "max_dd_r": _max_dd(recs),
        "avg_bars_held": round(sum(r["bars_held"] for r in recs) / n, 1) if n else None,
        "first": _day(recs[0]["signal"]) if recs else None,
        "last": _day(recs[-1]["exit"]) if recs else None,
    }
    return recs, summ


def _max_dd(recs):
    peak = 0.0; cum = 0.0; dd = 0.0
    for r in recs:
        cum += r["r"]
        peak = max(peak, cum)
        dd = min(dd, cum - peak)
    return round(dd, 3)


def _basis_text(r):
    """One-line plain-English basis for this trade."""
    d = "long" if r["dir"] == "long" else "short"
    brk = "above" if d == "long" else "below"
    return (f"W1 {r['w1_origin']}→{r['w1_extreme']}, W2 pulled back to {r['w2']} "
            f"({r['retr']:.0%} of W1); entered on the close {brk} W1's extreme at "
            f"{r['entry']}; stop {r['stop']} (beyond W2); target {r['target']} "
            f"(1.618×W1).")


# --------------------------------------------------------------------------- #
# CSV
# --------------------------------------------------------------------------- #
_CSV_COLS = ["n", "symbol", "dir", "signal_utc", "exit_utc", "w1_origin",
             "w1_extreme", "w2_extreme", "retr_pct", "entry", "stop", "target",
             "risk", "planned_rr", "r", "outcome", "bars_held", "cum_r",
             "strands", "confirm_lag_bars"]


def write_csv(recs, path):
    import csv
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(_CSV_COLS)
        for r in recs:
            w.writerow([r["n"], r["symbol"], r["dir"], _d(r["signal"]),
                        _d(r["exit"]), r["w1_origin"], r["w1_extreme"], r["w2"],
                        f"{r['retr']:.1%}", r["entry"], r["stop"], r["target"],
                        r["risk"], r["rr"], r["r"], r["outcome"], r["bars_held"],
                        r["cum_r"], r["strands"], r["confirm_lag_bars"]])


# --------------------------------------------------------------------------- #
# HTML
# --------------------------------------------------------------------------- #
_CSS = """
body{background:#0a0d0f;color:#e8eef0;font:14px/1.5 system-ui,Segoe UI,sans-serif;margin:0;padding:22px}
.wrap{max-width:1180px;margin:0 auto}
h1{font-size:22px;margin:0 0 4px}.sub{color:#7c8a91;font-size:12.5px;margin-bottom:16px;line-height:1.55}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin:14px 0}
.kpi{background:#11161a;border:1px solid #1c252b;border-radius:9px;padding:12px 14px}
.kpi .v{font-size:20px;font-weight:700}.kpi .l{font-size:10.5px;color:#7c8a91;text-transform:uppercase;letter-spacing:.5px;margin-top:2px}
.pos{color:#28a35a}.neg{color:#f0524a}.amb{color:#bd8514}
table{width:100%;border-collapse:collapse;font-size:12px;margin-top:8px}
th,td{padding:6px 8px;border-bottom:1px solid #1c252b;text-align:right;white-space:nowrap}
th{color:#7c8a91;font-weight:600;text-align:right;position:sticky;top:0;background:#0a0d0f}
td.l,th.l{text-align:left}
tr:hover td{background:#11161a}
.win{border-left:3px solid #28a35a}.loss{border-left:3px solid #f0524a}
.tag{font-size:10px;padding:1px 6px;border-radius:10px;background:#1c252b}
.note{color:#7c8a91;font-size:11.5px}
.foot{color:#7c8a91;font-size:11px;border-top:1px solid #1c252b;margin-top:16px;padding-top:12px;line-height:1.6}
h2{font-size:15px;color:#27e0c4;margin:22px 0 6px}
.eq{background:#11161a;border:1px solid #1c252b;border-radius:9px;padding:10px;margin-top:8px}
"""


def _equity_svg(recs, w=1140, h=140):
    if not recs:
        return ""
    cum = [r["cum_r"] for r in recs]
    lo, hi = min(0, min(cum)), max(0, max(cum))
    rng = (hi - lo) or 1
    n = len(cum)
    def X(i): return 8 + i / max(n - 1, 1) * (w - 16)
    def Y(v): return 8 + (hi - v) / rng * (h - 16)
    zero = Y(0)
    pts = " ".join(f"{'M' if i == 0 else 'L'}{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(cum))
    return (f'<div class="eq"><svg viewBox="0 0 {w} {h}" style="width:100%;height:auto">'
            f'<line x1="8" y1="{zero:.1f}" x2="{w-8}" y2="{zero:.1f}" stroke="#1c252b" stroke-width="1"/>'
            f'<path d="{pts}" fill="none" stroke="#2f8fe6" stroke-width="2"/>'
            f'<text x="10" y="16" fill="#7c8a91" font-size="10">cumulative R</text>'
            f'<text x="{w-8}" y="{Y(cum[-1])-4:.1f}" fill="#e8eef0" font-size="11" '
            f'text-anchor="end">{cum[-1]:+.2f}R</text></svg></div>')


def render_html(recs, summ, tf, profile_name, path):
    def kpi(v, l, cls=""):
        return f'<div class="kpi"><div class="v {cls}">{v}</div><div class="l">{l}</div></div>'
    tot = summ["total_r"] or 0
    exp = summ["expectancy_r"]
    kpis = "".join([
        kpi(summ["trades"], "trades taken"),
        kpi(f'{summ["win_rate"]:.0%}' if summ["win_rate"] is not None else "—", "win rate"),
        kpi(f'{tot:+.2f}R', "net result", "pos" if tot > 0 else "neg"),
        kpi(f'{exp:+.3f}R' if exp is not None else "—", "per trade", "pos" if (exp or 0) > 0 else "neg"),
        kpi(summ["profit_factor"] if summ["profit_factor"] else "—", "profit factor"),
        kpi(f'{summ["max_dd_r"]:.2f}R', "max drawdown", "neg"),
        kpi(f'{summ["fire_rate_pct"]}%', "of bars traded"),
    ])
    rows = []
    for r in recs:
        cls = "win" if r["r"] > 0 else "loss"
        oc = r["outcome"]
        oc_cls = "pos" if r["r"] > 0 else "neg"
        lag = r["confirm_lag_bars"]
        rows.append(
            f'<tr class="{cls}">'
            f'<td>{r["n"]}</td>'
            f'<td class="l"><span class="tag">{r["dir"]}</span></td>'
            f'<td class="l">{_d(r["signal"])}</td>'
            f'<td class="l note">{html.escape(_basis_text(r))}</td>'
            f'<td>{r["entry"]}</td><td>{r["stop"]}</td><td>{r["target"]}</td>'
            f'<td>{r["rr"]}</td>'
            f'<td class="{oc_cls}">{oc}</td>'
            f'<td class="{oc_cls}">{r["r"]:+.2f}</td>'
            f'<td>{r["cum_r"]:+.2f}</td>'
            f'<td>{r["bars_held"]}</td>'
            f'<td>{lag if lag is not None else "—"}</td>'
            f'</tr>')
    head = ("<tr><th>#</th><th class='l'>dir</th><th class='l'>signal (UTC)</th>"
            "<th class='l'>basis — why this trade fired</th><th>entry</th><th>stop</th>"
            "<th>target</th><th>R:R</th><th>exit</th><th>R</th><th>cum R</th>"
            "<th>held</th><th>lag</th></tr>")
    doc = (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
           f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"<title>{summ['symbol']} journal</title><style>{_CSS}</style></head><body><div class='wrap'>"
           f"<h1>Trading journal — {summ['symbol']} · {tf} · {profile_name}</h1>"
           f"<div class='sub'>Every wave-3 trade the system took over "
           f"{summ['first']} → {summ['last']} ({summ['bars_scanned']} bars scanned), "
           f"wins and losses, in the order they happened. Each row is causal — the "
           f"setup was knowable before entry (see 'lag' = bars from setup-confirmed to "
           f"fire). This is a backtest/ghost record, not advice.</div>"
           f"<div class='kpis'>{kpis}</div>"
           f"<h2>Equity curve (cumulative R)</h2>{_equity_svg(recs)}"
           f"<h2>Trade-by-trade log</h2>"
           f"<table>{head}{''.join(rows)}</table>"
           f"<div class='foot'>Basis columns are reconstructed from the actual "
           f"signal that fired: <b>W1</b> = the impulse leg (origin→broken extreme), "
           f"<b>W2</b> = the pullback the entry followed, <b>retr</b> = W2 as a % of W1 "
           f"(must sit in the profile's golden band and never exceed W1's origin — "
           f"Elliott rule R1). Entry = the close that broke W1's extreme; stop = beyond "
           f"W2; target = 1.618×W1. Selectivity: only {summ['fire_rate_pct']}% of bars "
           f"produced a trade — the signal is rare and rule-gated, it does NOT label "
           f"every swing. R results are net of modeled slippage + commission. "
           f"See docs/RULE_COVERAGE.md for what does and doesn't gate a trade.</div>"
           f"</div></body></html>")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(doc)
    return doc
