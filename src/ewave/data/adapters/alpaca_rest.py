"""
Alpaca REST market-data adapter (port of scripts/alpaca_fetch.py — the fetch
that produced the validated year-long forward-test datasets).
Pure stdlib (urllib). Needs APCA_API_KEY_ID / APCA_API_SECRET_KEY in the
environment and network egress to data.alpaca.markets — raise-with-reason
otherwise. Split-adjusted by default (keeps the series continuous).
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Optional

from . import AdapterUnavailable, DataProvider
from ..models import BarSeries

_TF = {"1m": "1Min", "5m": "5Min", "15m": "15Min", "30m": "30Min",
       "1h": "1Hour", "4h": "4Hour", "1d": "1Day", "1w": "1Week"}
_BASE = "https://data.alpaca.markets/v2/stocks/{sym}/bars"


def _to_unix(s: str) -> int:
    return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())


class AlpacaRest(DataProvider):
    name = "alpaca"

    def __init__(self, key: Optional[str] = None, secret: Optional[str] = None,
                 feed: str = "iex", adjustment: str = "split", limit: int = 10000):
        self.key = key or os.environ.get("APCA_API_KEY_ID")
        self.secret = secret or os.environ.get("APCA_API_SECRET_KEY")
        self.feed, self.adjustment, self.limit = feed, adjustment, limit

    def fetch(self, symbol: str, tf: str, start: Optional[str] = None,
              end: Optional[str] = None, **kw) -> BarSeries:
        if not self.key or not self.secret:
            raise AdapterUnavailable(
                "alpaca: set APCA_API_KEY_ID and APCA_API_SECRET_KEY (see .env.example)")
        if tf not in _TF:
            raise AdapterUnavailable(f"alpaca: unsupported timeframe '{tf}'")
        sym = symbol.split(":")[-1].upper()
        rows, token = [], None
        while len(rows) < self.limit:
            q = {"timeframe": _TF[tf], "limit": min(10000, self.limit - len(rows)),
                 "adjustment": self.adjustment, "feed": kw.get("feed", self.feed),
                 "sort": "asc"}
            if start:
                q["start"] = f"{start}T00:00:00Z"
            if end:
                q["end"] = f"{end}T23:59:59Z"
            if token:
                q["page_token"] = token
            url = _BASE.format(sym=urllib.parse.quote(sym)) + "?" + urllib.parse.urlencode(q)
            req = urllib.request.Request(url, headers={
                "APCA-API-KEY-ID": self.key, "APCA-API-SECRET-KEY": self.secret})
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    d = json.load(r)
            except Exception as e:
                raise AdapterUnavailable(f"alpaca: request failed ({e})") from e
            for b in (d.get("bars") or []):
                rows.append((_to_unix(b["t"]), b["o"], b["h"], b["l"], b["c"],
                             b.get("v", 0)))
            token = d.get("next_page_token")
            if not token:
                break
        asof = datetime.now(timezone.utc).date().isoformat()
        return BarSeries.from_rows(f"ALPACA:{sym}", tf, asof, rows,
                                   source="alpaca_rest", adjustment=self.adjustment,
                                   session="regular")
