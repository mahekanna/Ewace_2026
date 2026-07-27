"""
fetch_alpaca_rest.py — pull OHLCV from Alpaca's REST API into the bars contract.
================================================================================
Use this when you have Alpaca market-data keys AND the host is reachable. Pure
stdlib (urllib). Writes data/live/<sym>_<tf>_<asof>.json in the kit's bars shape.

  export APCA_API_KEY_ID=...  APCA_API_SECRET_KEY=...
  python3 fetch_alpaca_rest.py AVGO 15m --rth --feed iex --out data/live
  python3 fetch_alpaca_rest.py AVGO 1d 1h 15m            # several timeframes

--rth   keep only US regular-session bars (recommended for intraday; matches most
        backtest tooling). Omit to keep extended hours.
--feed  iex (free) | sip (paid, all exchanges). Default iex.
Notes: split-adjusted by default; paginates up to --limit bars (default 10000).
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf import in_rth_ny

TF = {"1m": "1Min", "5m": "5Min", "15m": "15Min", "30m": "30Min",
      "1h": "1Hour", "4h": "4Hour", "1d": "1Day", "1w": "1Week"}
BASE = "https://data.alpaca.markets/v2/stocks/{sym}/bars"


def to_unix(s):
    return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())


def fetch(sym, tf, key, sec, limit, feed, adjustment="split"):
    bars, token = [], None
    while len(bars) < limit:
        q = {"timeframe": TF[tf], "limit": min(10000, limit - len(bars)),
             "adjustment": adjustment, "feed": feed, "sort": "asc"}
        if token:
            q["page_token"] = token
        url = BASE.format(sym=urllib.parse.quote(sym)) + "?" + urllib.parse.urlencode(q)
        req = urllib.request.Request(url, headers={"APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": sec})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        for b in (d.get("bars") or []):
            bars.append({"t": to_unix(b["t"]), "o": b["o"], "h": b["h"],
                         "l": b["l"], "c": b["c"], "v": b.get("v", 0)})
        token = d.get("next_page_token")
        if not token:
            break
    return bars


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol")
    ap.add_argument("timeframes", nargs="+", help="e.g. 15m 1h 1d")
    ap.add_argument("--rth", action="store_true")
    ap.add_argument("--feed", default="iex")
    ap.add_argument("--limit", type=int, default=10000)
    ap.add_argument("--out", default="data/live")
    a = ap.parse_args()
    key, sec = os.environ.get("APCA_API_KEY_ID"), os.environ.get("APCA_API_SECRET_KEY")
    if not key or not sec:
        raise SystemExit("set APCA_API_KEY_ID and APCA_API_SECRET_KEY first")
    sym = a.symbol.upper()
    os.makedirs(a.out, exist_ok=True)
    asof = datetime.now(timezone.utc).date().isoformat()
    for tf in a.timeframes:
        tf = tf.lower()
        if tf not in TF:
            print(f"skip {tf}: unknown timeframe"); continue
        bars = fetch(sym, tf, key, sec, a.limit, a.feed)
        if a.rth and tf in ("1m", "5m", "15m", "30m", "1h", "4h"):
            bars = [b for b in bars if in_rth_ny(b["t"])]
        out = {"symbol": f"ALPACA:{sym}", "interval": tf, "asof": asof, "bars": bars}
        path = os.path.join(a.out, f"{sym.lower()}_{tf}_{asof[:7]}.json")
        json.dump(out, open(path, "w"))
        span = (f"{datetime.utcfromtimestamp(bars[0]['t']).date()} -> "
                f"{datetime.utcfromtimestamp(bars[-1]['t']).date()}") if bars else "(empty)"
        print(f"wrote {path}: {len(bars)} bars {span} feed={a.feed} rth={a.rth}")


if __name__ == "__main__":
    main()
