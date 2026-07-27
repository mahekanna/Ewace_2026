"""
data.resample — stdlib timeframe builder (finer → coarser only).
================================================================
Intraday buckets are anchored to each calendar day's FIRST bar (so a US-equity
RTH feed gets 09:30-anchored hourly buckets, matching how Alpaca/TradingView
bucket their bars; a 24h crypto feed starting at 00:00 UTC reduces to fixed UTC
windows). Daily buckets follow the instrument's calendar (New York date for
equities — a 20:00 UTC bar belongs to that NY trading day; UTC date for
crypto/fx). Weekly buckets are the calendar's ISO Monday.

Aggregation per bucket: o = first o, h = max h, l = min l, c = last c, v = Σv.
Bucket timestamp = first source bar's t (open time), consistent with the feeds.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Sequence, Tuple

TF_SECONDS: Dict[str, int] = {
    "1m": 60, "5m": 300, "15m": 900, "30m": 1800,
    "1h": 3600, "4h": 14400, "1d": 86400, "1w": 7 * 86400,
}

_INTRADAY = {"1m", "5m", "15m", "30m", "1h", "4h"}


def _tzinfo(calendar: str):
    if calendar in ("UTC", "", None):
        return timezone.utc
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(calendar)
    except Exception:
        # fixed-offset fallback for America/New_York (EDT); good enough for
        # environments without tzdata — daily bucketing shifts only around DST
        return timezone(timedelta(hours=-4)) if calendar == "America/New_York" else timezone.utc


def _bucket_key(t: int, dst_tf: str, calendar: str) -> int:
    d = datetime.fromtimestamp(t, _tzinfo(calendar))
    if dst_tf == "1d":
        local_midnight = d.replace(hour=0, minute=0, second=0, microsecond=0)
    elif dst_tf == "1w":
        monday = d - timedelta(days=d.weekday())
        local_midnight = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        raise ValueError(f"unsupported destination timeframe '{dst_tf}'")
    return int(local_midnight.timestamp())


def resample(bars: Sequence[Tuple], src_tf: str, dst_tf: str,
             calendar: str = "UTC") -> List[Tuple]:
    """`bars` = ascending (t,o,h,l,c[,v]) tuples in src_tf; returns dst_tf tuples.

    Only finer→coarser is meaningful; equal timeframes pass through and a
    coarser source raises (upsampling would fabricate data)."""
    if src_tf not in TF_SECONDS or dst_tf not in TF_SECONDS:
        raise ValueError(f"unknown timeframe: {src_tf} -> {dst_tf}")
    if TF_SECONDS[src_tf] > TF_SECONDS[dst_tf]:
        raise ValueError(f"cannot upsample {src_tf} -> {dst_tf}")
    if src_tf == dst_tf:
        return list(bars)

    tz = _tzinfo(calendar)
    intraday = dst_tf in _INTRADAY
    secs = TF_SECONDS[dst_tf]
    out: List[list] = []
    current_key = None
    day = None          # (date, first-bar t) anchor for intraday bucketing
    for b in bars:
        t, o, h, l, c = b[0], b[1], b[2], b[3], b[4]
        v = b[5] if len(b) > 5 else 0
        if intraday:
            d = datetime.fromtimestamp(t, tz).date()
            if day is None or d != day[0]:
                day = (d, t)                      # session anchor = day's first bar
            anchor = day[1]
            key = (d, anchor + (t - anchor) // secs * secs)
        else:
            key = _bucket_key(t, dst_tf, calendar)
        if key != current_key:
            out.append([t, o, h, l, c, v])
            current_key = key
        else:
            agg = out[-1]
            agg[2] = max(agg[2], h)
            agg[3] = min(agg[3], l)
            agg[4] = c
            agg[5] += v
    return [tuple(x) for x in out]
