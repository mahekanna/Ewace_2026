"""
build_from_dumps.py — merge Alpaca-MCP get_stock_bars dumps into the bars contract.
===================================================================================
For the MCP path (no REST keys): when you call the Alpaca MCP `get_stock_bars` tool
for many windows, each large result is auto-saved to a file on disk. This script
finds every such dump, keeps the ones for your symbol+timeframe, merges/dedupes them
into one ascending series, and writes the contract JSON (RTH + extended-hours).

  python3 build_from_dumps.py AVGO 15m --out ../data/live
  python3 build_from_dumps.py AVGO 15m --dumps /root/.claude/projects --out ../data/live

It auto-detects the timeframe of each dump by the median spacing between bars, so it
won't mix 15m with 1h/1d files. See docs/02_FETCH_DATA.md for the windowing recipe.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf import in_rth_ny

SECS = {"1m": 60, "5m": 300, "15m": 900, "30m": 1800, "1h": 3600, "4h": 14400, "1d": 86400}


def to_unix(s):
    return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())


def find_dumps(base):
    out = []
    for root, _dirs, fnames in os.walk(base):
        if os.path.basename(root) != "tool-results":
            continue
        for fn in fnames:
            if fn.startswith("mcp-Alpacamn-get_stock_bars-") and fn.endswith(".txt"):
                out.append(os.path.join(root, fn))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol")
    ap.add_argument("timeframe", help="e.g. 15m")
    ap.add_argument("--dumps", default="/root/.claude/projects", help="root to scan for saved MCP results")
    ap.add_argument("--out", default="data/live")
    a = ap.parse_args()
    sym, tf = a.symbol.upper(), a.timeframe.lower()
    want = SECS[tf]
    raw, used = [], 0
    for fp in find_dumps(a.dumps):
        try:
            d = json.load(open(fp))
        except Exception:
            continue
        b = d.get("bars", {})
        if sym not in b or len(b[sym]) < 3:
            continue
        ts = sorted(to_unix(x["t"]) for x in b[sym])
        difs = sorted(ts[i + 1] - ts[i] for i in range(len(ts) - 1))
        if difs[len(difs) // 2] != want:                 # timeframe must match
            continue
        used += 1
        for x in b[sym]:
            raw.append({"t": to_unix(x["t"]), "o": x["o"], "h": x["h"],
                        "l": x["l"], "c": x["c"], "v": x.get("v", 0) or 0})
    raw.sort(key=lambda z: z["t"])
    seen, eh = set(), []
    for z in raw:
        if z["t"] in seen:
            continue
        seen.add(z["t"]); eh.append(z)
    rth = [z for z in eh if in_rth_ny(z["t"])] if tf in ("1m", "5m", "15m", "30m", "1h", "4h") else eh
    os.makedirs(a.out, exist_ok=True)
    asof = datetime.now(timezone.utc).date().isoformat()

    def write(slug, bars):
        json.dump({"symbol": f"ALPACA:{sym}", "interval": slug, "asof": asof, "bars": bars},
                  open(os.path.join(a.out, f"{sym.lower()}_{slug}_{asof[:7]}.json"), "w"))
        n = len(bars)
        if not n:
            print(f"  {slug}: 0 bars"); return
        mono = all(bars[i]["t"] < bars[i + 1]["t"] for i in range(n - 1))
        gaps = sum(1 for i in range(n - 1) if bars[i + 1]["t"] - bars[i]["t"] > 4 * 86400)
        f = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")
        print(f"  {sym.lower()}_{slug}: n={n} {f(bars[0]['t'])}->{f(bars[-1]['t'])} mono={mono} gaps>4d={gaps}")

    print(f"{sym}: merged {used} {tf} dump(s) -> {len(eh)} EH / {len(rth)} RTH bars")
    write(tf, rth)
    write(tf + "_eh", eh)


if __name__ == "__main__":
    main()
