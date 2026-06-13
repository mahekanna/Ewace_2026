"""
ghost_forward.py — causal ghost-feeding forward test for ANY forecaster.
========================================================================
Walks the bars one candle at a time; at each candle it asks your forecaster for a
call (built from prior bars only), then ghost-feeds the next candles to see whether
the call played out. Writes an honest Markdown report. Pure stdlib.

USAGE
  python3 ghost_forward.py --data DATA.json --forecaster forecasters/example_naive.py:forecast
  python3 ghost_forward.py --data d.json --forecaster my_model.py:forecast \
          --roll 400 --forward all --resolve 32 --out report.md

--roll     bars of history your forecaster sees at each step (default 400)
--forward  how many recent candles to test, or "all" for the whole series (default all)
--resolve  ghost-feed horizon to resolve each call, in bars (default 32)
See docs/04_RUN_GHOST_TEST.md for interpretation.
"""
import argparse
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gf


def dt(t):
    return datetime.fromtimestamp(t, tz=timezone.utc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--forecaster", required=True, help="'file.py:func' or 'module:func'")
    ap.add_argument("--roll", type=int, default=400)
    ap.add_argument("--forward", default="all")
    ap.add_argument("--resolve", type=int, default=32)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    bars, symbol, interval = gf.load_bars(a.data)
    forecaster = gf.load_forecaster(a.forecaster)
    if len(bars) <= a.roll + a.resolve:
        raise SystemExit(f"not enough bars ({len(bars)}) for roll={a.roll}+resolve={a.resolve}")

    rows = list(gf.iter_steps(bars, forecaster, a.roll, a.forward, a.resolve))
    if not rows:
        raise SystemExit("no steps produced — check --roll/--forward/--resolve vs data length")

    hit = {"HIT": 0, "INVALIDATED": 0, "OPEN": 0, "stale": 0, "no-forecast": 0}
    dir_ok = dir_tot = 0
    for r in rows:
        hit[r["outcome"]] = hit.get(r["outcome"], 0) + 1
        if r["fc"] and r["next_up"] is not None:
            dir_tot += 1
            dir_ok += int((r["fc"].direction == "up") == r["next_up"])
    decided = hit["HIT"] + hit["INVALIDATED"]
    hr = hit["HIT"] / decided if decided else 0.0
    da = dir_ok / dir_tot if dir_tot else 0.0
    stale = hit["stale"]
    mod = max(8, len(rows) // 120)

    out = [f"# Ghost forward test — {symbol} {interval}", "",
           f"_At each of {len(rows)} candles "
           f"({dt(rows[0]['t']):%Y-%m-%d %H:%M} → {dt(rows[-1]['t']):%Y-%m-%d %H:%M}) the forecast is "
           f"built from the prior {a.roll} bars only, then the next {a.resolve} bars are ghost-fed. "
           f"Causal; not advice._", "",
           "## Summary",
           f"- **STALE/unusable: {stale}** of {len(rows)} ({stale/len(rows):.0%}) — target already on the "
           "wrong side of price; EXCLUDED from hit-rate.",
           f"- Usable resolved: **{decided}** (HIT {hit['HIT']} / INVALIDATED {hit['INVALIDATED']}); "
           f"OPEN {hit['OPEN']}; no-forecast {hit['no-forecast']}.",
           f"- **Target-hit among usable: {hr:.0%}.**",
           f"- Next-candle directional accuracy: **{da:.0%}** of {dir_tot} (coin-flip = 50%).",
           "",
           f"## Forecast log (every {mod}th candle)",
           "| time | price | dir | kind | conf | target | invalid | outcome |",
           "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rows):
        if i % mod:
            continue
        fc = r["fc"]
        if fc:
            out.append(f"| {dt(r['t']):%Y-%m-%d %H:%M} | {r['price']:,.2f} | {fc.direction} | {fc.kind or '-'} "
                       f"| {fc.confidence:.0%} | {fc.target:,.2f} | {fc.invalidation:,.2f} | {r['outcome']}"
                       + (f" ({r['nbar']})" if r['outcome'] in ('HIT', 'INVALIDATED') else "") + " |")
        else:
            out.append(f"| {dt(r['t']):%Y-%m-%d %H:%M} | {r['price']:,.2f} | - | - | - | - | - | no-forecast |")

    report = "\n".join(out) + "\n"
    path = a.out or f"GHOST_TEST_{os.path.splitext(os.path.basename(a.data))[0]}.md"
    open(path, "w").write(report)
    print("\n".join(out[:11]))
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
