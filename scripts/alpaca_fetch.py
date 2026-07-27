"""
alpaca_fetch.py  —  pull OHLCV from Alpaca into the data/live/ JSON format.
==========================================================================
Run this in the session/ENVIRONMENT where Alpaca is reachable (the Alpaca MCP is
NOT required — this uses Alpaca's REST market-data API directly). It writes the
exact `{"symbol","interval","asof","bars":[{t,o,h,l,c,v}]}` shape every wavelib
script expects, so the dev session can forward-test on it after a git pull.

Requires env vars:  APCA_API_KEY_ID  and  APCA_API_SECRET_KEY
(Free keys work; data is split-adjusted by default, which fixes the split
artifacts seen in the TradingView pulls.)

Usage:
  python3 scripts/alpaca_fetch.py AVGO 15m
  python3 scripts/alpaca_fetch.py MRVL 1d 1h 15m        # several timeframes
  python3 scripts/alpaca_fetch.py AVGO 15m --feed sip   # if you have SIP data
Pure stdlib (urllib) — no pip install needed.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(ROOT, "data", "live")
TF = {"1m": "1Min", "5m": "5Min", "15m": "15Min", "30m": "30Min",
      "1h": "1Hour", "4h": "4Hour", "1d": "1Day", "1w": "1Week"}
BASE = "https://data.alpaca.markets/v2/stocks/{sym}/bars"
KEY = os.environ.get("APCA_API_KEY_ID")
SEC = os.environ.get("APCA_API_SECRET_KEY")


def to_unix(s):
    return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())


def fetch(sym, tag, limit=10000, feed="iex", adjustment="split"):
    """Paginated bar pull (up to `limit` bars), newest history. Returns our bar dicts."""
    tfa = TF[tag]
    bars, token = [], None
    while len(bars) < limit:
        q = {"timeframe": tfa, "limit": min(10000, limit - len(bars)),
             "adjustment": adjustment, "feed": feed, "sort": "asc"}
        if token:
            q["page_token"] = token
        url = BASE.format(sym=urllib.parse.quote(sym)) + "?" + urllib.parse.urlencode(q)
        req = urllib.request.Request(url, headers={"APCA-API-KEY-ID": KEY or "",
                                                   "APCA-API-SECRET-KEY": SEC or ""})
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
    if not KEY or not SEC:
        print("ERROR: set APCA_API_KEY_ID and APCA_API_SECRET_KEY env vars first.")
        sys.exit(1)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    feed = "iex"
    if "--feed" in sys.argv:
        feed = sys.argv[sys.argv.index("--feed") + 1]
    sym = (args[0] if args else "AVGO").upper()
    tags = [a.lower() for a in args[1:] if a.lower() in TF] or ["15m"]
    os.makedirs(LIVE, exist_ok=True)
    for tag in tags:
        try:
            bars = fetch(sym, tag, feed=feed)
        except Exception as e:
            print(f"{sym} {tag}: FETCH ERROR {e}")
            continue
        out = {"symbol": f"ALPACA:{sym}", "interval": tag,
               "asof": datetime.now(timezone.utc).date().isoformat(), "bars": bars}
        path = os.path.join(LIVE, f"{sym.lower()}_{tag}_2026-06.json")
        json.dump(out, open(path, "w"))
        span = (f"{datetime.utcfromtimestamp(bars[0]['t']).date()} -> "
                f"{datetime.utcfromtimestamp(bars[-1]['t']).date()}") if bars else "(empty)"
        print(f"wrote {path}: {len(bars)} bars  {span}  feed={feed}")


if __name__ == "__main__":
    main()
