"""
mcp_bridge — normalize MCP finance-tool payloads into the bars contract.
========================================================================
In the cloud sandbox, market-data hosts are proxy-blocked for Python but the
MCP finance tools work. The bridge flow (docs/COLLAB_RUNBOOK.md):

  1. Claude calls the MCP tool (FMP chart / yfinance history / tvremix
     get_ohlcv / Alpaca get_stock_bars) and saves the raw payload to a file.
  2. `python scripts/mcp_export.py --format fmp|yf|tv|alpaca-mcp --symbol X
     --tf 1h payload.json` normalizes it here and writes contract JSON into
     data/live/ via the Store.

Parsers are deliberately tolerant (key aliases, s/ms epochs, ISO strings,
newest-first ordering) because MCP payload shapes vary by server version;
`BarSeries.from_rows` re-sorts and dedupes regardless.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional, Tuple

from ..models import BarSeries

_TIME_KEYS = ("t", "time", "timestamp", "date", "datetime", "Date", "Datetime", "index")
_FIELD_KEYS = {
    "o": ("o", "open", "Open"),
    "h": ("h", "high", "High"),
    "l": ("l", "low", "Low"),
    "c": ("c", "close", "Close", "adjClose", "Adj Close", "adjclose"),
    "v": ("v", "volume", "Volume", "vol"),
}


def _parse_time(val, tz: str = "UTC") -> int:
    """Accept unix seconds, unix ms, or ISO strings (naive strings use `tz`)."""
    if isinstance(val, (int, float)):
        return int(val / 1000) if val > 1e11 else int(val)
    s = str(val).strip().replace("Z", "+00:00")
    d = datetime.fromisoformat(s)
    if d.tzinfo is None:
        if tz == "UTC":
            d = d.replace(tzinfo=timezone.utc)
        else:
            try:
                from zoneinfo import ZoneInfo
                d = d.replace(tzinfo=ZoneInfo(tz))
            except Exception:
                from datetime import timedelta
                d = d.replace(tzinfo=timezone(timedelta(hours=-4)))
    return int(d.timestamp())


def _record_to_row(rec: dict, tz: str) -> Optional[Tuple]:
    t = None
    for k in _TIME_KEYS:
        if k in rec and rec[k] is not None:
            t = _parse_time(rec[k], tz)
            break
    if t is None:
        return None
    vals = {}
    for canon, names in _FIELD_KEYS.items():
        for k in names:
            if k in rec and rec[k] is not None:
                vals[canon] = float(rec[k])
                break
    if not all(k in vals for k in ("o", "h", "l", "c")):
        return None
    return (t, vals["o"], vals["h"], vals["l"], vals["c"], vals.get("v", 0.0))


def _rows_from_records(records, tz: str) -> List[Tuple]:
    rows = []
    for rec in records or []:
        if isinstance(rec, dict):
            row = _record_to_row(rec, tz)
            if row:
                rows.append(row)
    return rows


def _series(symbol: str, tf: str, rows: List[Tuple], source: str,
            session: str = "regular") -> BarSeries:
    asof = datetime.now(timezone.utc).date().isoformat()
    return BarSeries.from_rows(symbol.split(":")[-1].upper(), tf, asof, rows,
                               source=source, adjustment="split", session=session)


# ------------------------- per-source entry points -------------------------
def from_fmp_chart(payload, symbol: str, tf: str) -> BarSeries:
    """mcp__FMP__chart / FMP REST: list of {"date","open",...} (intraday dates
    are America/New_York wall-clock, newest first) or {"historical": [...]}."""
    records = payload
    if isinstance(payload, dict):
        records = payload.get("historical") or payload.get("results") or payload.get("data")
    tz = "America/New_York" if tf in ("1m", "5m", "15m", "30m", "1h", "4h") else "UTC"
    return _series(symbol, tf, _rows_from_records(records, tz), "mcp:fmp")


def from_yfinance_history(payload, symbol: str, tf: str) -> BarSeries:
    """mcp__Finance__yfinance_*history: record list, {"data": [...]}, or a
    dict-of-dicts {timestamp: {"Open": ...}} (pandas to_dict orient variants)."""
    records = payload
    if isinstance(payload, dict):
        inner = payload.get("data") or payload.get("history") or payload.get("rows")
        if inner is not None:
            records = inner
        elif payload and all(isinstance(v, dict) for v in payload.values()):
            records = [dict(v, date=k) for k, v in payload.items()]
    return _series(symbol, tf, _rows_from_records(records, "UTC"), "mcp:yfinance")


def from_tvremix_ohlcv(payload, symbol: str, tf: str) -> BarSeries:
    """mcp__Tvremix_d__get_ohlcv: {"bars": [...]} / {"ohlcv": [...]} / list,
    with unix-seconds "time" keys."""
    records = payload
    if isinstance(payload, dict):
        records = payload.get("bars") or payload.get("ohlcv") or payload.get("data")
    return _series(symbol, tf, _rows_from_records(records, "UTC"), "mcp:tvremix",
                   session="full")


def from_alpaca_mcp(payload, symbol: str, tf: str) -> BarSeries:
    """Alpaca MCP get_stock_bars dumps: {"bars": {"AVGO": [{"t": ISO, ...}]}}
    (the shape ghost_forward_kit/build_from_dumps.py merges)."""
    sym = symbol.split(":")[-1].upper()
    records = payload
    if isinstance(payload, dict):
        b = payload.get("bars", payload)
        records = b.get(sym) if isinstance(b, dict) else b
    return _series(symbol, tf, _rows_from_records(records, "UTC"), "mcp:alpaca",
                   session="full")


FORMATS = {
    "fmp": from_fmp_chart,
    "yf": from_yfinance_history,
    "yfinance": from_yfinance_history,
    "tv": from_tvremix_ohlcv,
    "tvremix": from_tvremix_ohlcv,
    "alpaca-mcp": from_alpaca_mcp,
}


def normalize(payload, fmt: str, symbol: str, tf: str) -> BarSeries:
    if fmt not in FORMATS:
        raise KeyError(f"unknown format '{fmt}' (have: {', '.join(sorted(FORMATS))})")
    series = FORMATS[fmt](payload, symbol, tf)
    if not series.bars:
        raise ValueError(
            f"{fmt}: no bars could be parsed for {symbol} {tf} — payload shape "
            "not recognized (inspect the raw file and extend mcp_bridge if needed)")
    return series
