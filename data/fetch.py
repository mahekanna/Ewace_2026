"""
data/fetch.py — OHLCV loader for wavelib.
=========================================
Two halves, deliberately separated:

* **Loading** (stdlib only, always available): read a bar snapshot from
  ``data/live/<slug>_<tf>_<tag>.json`` into the ``(t,o,h,l,c,v)`` tuples every
  wavelib entry point expects.  ``load_bars("AVGO", "1d")`` picks the newest tag.

* **Fetching** (optional, needs ``pip install yfinance``): pull split-adjusted
  bars from Yahoo Finance, write them in the exact snapshot contract that
  ``scripts/alpaca_fetch.py`` and the TradingView pulls used, and optionally
  regenerate the curated fixture arrays in ``data/avgo.py`` / ``data/mrvl.py``.

Snapshot contract (``docs/COLLAB_RUNBOOK.md``)::

    {"symbol": "YF:AVGO", "interval": "1d", "asof": "2026-11-06",
     "bars": [{"t": 1762318800, "o": 311.89, "h": 314.0, "l": 290.12, "c": 291.53, "v": 53372113}, ...]}

* ``t`` = unix seconds (UTC), bars ascending, regular session only.
* Prices split-adjusted but NOT dividend-adjusted (``auto_adjust=False``), which
  is the same adjustment Alpaca's ``adjustment=split`` applies — the two sources
  agree to the cent on overlapping closes.
* Daily bars carry Yahoo's native stamp (midnight America/New_York, i.e.
  04:00/05:00 UTC); intraday bars start at 09:30 ET.  4h bars are built here from
  1h bars, session-aligned (09:30 and 13:30 ET), matching the legacy H4 fixture.
  Weekly bars are built here from daily bars (Mon-Fri, stamped Monday 00:00 ET):
  Yahoo's own weekly series is not week-aligned for every ticker (MRVL's runs
  Thursday to Wednesday).

Yahoo depth limits: 15m ≤ 60 days, 1h ≤ 730 days, 1d/1w unlimited.

CLI::

    python3 data/fetch.py                         # AVGO + MRVL, 1d 1w 1h 4h snapshots
    python3 data/fetch.py AVGO MRVL --fixtures    # ... and regenerate data/avgo.py, data/mrvl.py
    python3 data/fetch.py NVDA --tf 1d 1w         # any symbol, chosen timeframes
    python3 data/fetch.py AVGO --tag 2026-11      # explicit snapshot tag (default: current YYYY-MM)
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
LIVE = os.path.join(DATA, "live")
NY = ZoneInfo("America/New_York")

TIMEFRAMES = ("15m", "1h", "4h", "1d", "1w")
_YF_INTERVAL = {"15m": "15m", "1h": "1h", "1d": "1d"}
# default history span per timeframe (Yahoo caps intraday depth)
_DEFAULT_SPAN = {
    "15m": {"period": "60d"},
    "1h": {"period": "730d"},
    "4h": {"period": "730d"},
    "1d": {"start": "2009-01-01"},
    "1w": {"start": "2009-01-01"},
}
_TAG_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")

# fixture array sizing (what lands in data/<slug>.py)
FIXTURE_WEEKLY_START = "2022-01-01"
FIXTURE_DAILY_START = "2021-01-01"
FIXTURE_H1_BARS = 420          # ~60 trading days of 1h bars
FIXTURE_H4_BARS = 120          # ~60 trading days of 4h bars
FIXTURE_FRESH_BARS = 60        # enough for the RSI/MACD strands (>50 bars)
_CURATED_MARKER = "# >>> hand-curated below — preserved verbatim by data/fetch.py >>>"


# ----------------------------------------------------------------------------
# loading (stdlib only)
# ----------------------------------------------------------------------------
def slug_of(symbol: str) -> str:
    """'NASDAQ:AVGO' / 'YF:AVGO' / 'avgo' -> 'avgo'."""
    return symbol.split(":")[-1].strip().lower()


def snapshot_path(symbol: str, tf: str, tag: str) -> str:
    return os.path.join(LIVE, f"{slug_of(symbol)}_{tf}_{tag}.json")


def available_tags(symbol: str, tf: str) -> list[str]:
    """Snapshot tags on disk for symbol/tf, oldest -> newest (YYYY-MM sorts lexically)."""
    prefix = f"{slug_of(symbol)}_{tf}_"
    tags = []
    for p in glob.glob(os.path.join(LIVE, prefix + "*.json")):
        tag = os.path.basename(p)[len(prefix):-len(".json")]
        if _TAG_RE.match(tag):          # skips variants such as avgo_15m_eh_2026-06.json
            tags.append(tag)
    return sorted(tags)


def latest_tag(symbol: str, tf: str) -> str | None:
    tags = available_tags(symbol, tf)
    return tags[-1] if tags else None


def read_snapshot(path: str) -> dict:
    with open(path) as fh:
        return json.load(fh)


def bars_from_snapshot(d: dict) -> list[tuple]:
    bars = [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0) for b in d["bars"]]
    bars.sort(key=lambda b: b[0])
    return bars


def load_bars(symbol: str, tf: str = "1d", tag: str | None = None, with_meta: bool = False):
    """Return ``(t,o,h,l,c,v)`` bars from ``data/live``; newest snapshot unless ``tag`` given.

    ``with_meta=True`` returns ``(bars, meta)`` where meta is the snapshot header
    (symbol, interval, asof, tag, path).
    """
    if tf not in TIMEFRAMES:
        raise ValueError(f"tf must be one of {TIMEFRAMES}, got {tf!r}")
    if tag is None:
        tag = latest_tag(symbol, tf)
        if tag is None:
            raise FileNotFoundError(
                f"no {tf} snapshot for {symbol} in {LIVE} — run "
                f"`python3 data/fetch.py {symbol.upper()} --tf {tf}`")
    path = snapshot_path(symbol, tf, tag)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} not found; available tags for {symbol} {tf}: "
            f"{available_tags(symbol, tf) or 'none'}")
    d = read_snapshot(path)
    bars = bars_from_snapshot(d)
    if not with_meta:
        return bars
    meta = {k: v for k, v in d.items() if k != "bars"}
    meta.update(tag=tag, path=path, n=len(bars))
    return bars, meta


# ----------------------------------------------------------------------------
# bar utilities (stdlib only)
# ----------------------------------------------------------------------------
def resample_4h(bars_1h: list[tuple]) -> list[tuple]:
    """Session-aligned 4h bars from 1h bars: buckets open at 09:30 and 13:30 ET.

    Each output bar is stamped with its first 1h bar's ``t`` (09:30 / 13:30 ET),
    the convention the legacy ``H4`` / ``FRESH_4H_VOL`` fixtures used.
    """
    out: dict[tuple, list] = {}
    order: list[tuple] = []
    for t, o, h, l, c, v in bars_1h:
        loc = dt.datetime.fromtimestamp(t, NY)
        sess = loc.replace(hour=9, minute=30, second=0, microsecond=0)
        idx = int((loc - sess).total_seconds() // 14400)      # -1 pre-market, 0, 1, (2 post)
        key = (loc.date(), idx)
        if key not in out:
            out[key] = [t, o, h, l, c, v]
            order.append(key)
        else:
            b = out[key]
            b[2] = max(b[2], h)
            b[3] = min(b[3], l)
            b[4] = c
            b[5] += v
    return [tuple(out[k]) for k in order]


def resample_weekly(bars_1d: list[tuple]) -> list[tuple]:
    """Mon-Fri weekly bars from daily bars, stamped Monday 00:00 America/New_York."""
    out: dict[dt.date, list] = {}
    for t, o, h, l, c, v in bars_1d:
        day = dt.datetime.fromtimestamp(t, NY).date()
        monday = day - dt.timedelta(days=day.weekday())
        if monday not in out:
            t0 = int(dt.datetime.combine(monday, dt.time(0, 0), tzinfo=NY).timestamp())
            out[monday] = [t0, o, h, l, c, v]
        else:
            b = out[monday]
            b[2] = max(b[2], h)
            b[3] = min(b[3], l)
            b[4] = c
            b[5] += v
    return [tuple(out[k]) for k in sorted(out)]


def slice_from(bars: list[tuple], start_date: str) -> list[tuple]:
    """Bars whose ``t`` is on/after ``start_date`` (YYYY-MM-DD, interpreted in ET)."""
    t0 = int(dt.datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=NY).timestamp())
    return [b for b in bars if b[0] >= t0]


# ----------------------------------------------------------------------------
# fetching (optional dependency: yfinance)
# ----------------------------------------------------------------------------
def _yf():
    try:
        import yfinance  # noqa: WPS433 — optional extra
    except ImportError as e:                       # pragma: no cover
        raise ImportError(
            "yfinance is not installed — it is an OPTIONAL extra "
            "(see requirements.txt). Install with:  pip install yfinance") from e
    return yfinance


def fetch_bars(symbol: str, tf: str = "1d", start: str | None = None,
               end: str | None = None, period: str | None = None) -> list[tuple]:
    """Pull ``(t,o,h,l,c,v)`` bars from Yahoo Finance via yfinance.

    Defaults: 1d/1w from 2009-01-01, 1h/4h last 730 days, 15m last 60 days.
    Regular session only, split-adjusted, not dividend-adjusted.  ``4h`` is
    resampled here from 1h bars (Yahoo has no native 4h interval) and ``1w``
    from daily bars (see module docstring).
    """
    if tf not in TIMEFRAMES:
        raise ValueError(f"tf must be one of {TIMEFRAMES}, got {tf!r}")
    if tf == "4h":
        return resample_4h(fetch_bars(symbol, "1h", start=start, end=end, period=period))
    if tf == "1w":
        return resample_weekly(fetch_bars(symbol, "1d", start=start, end=end, period=period))
    yf = _yf()
    kw = dict(interval=_YF_INTERVAL[tf], auto_adjust=False, actions=False, prepost=False)
    if start or end:
        kw.update(start=start, end=end)
    elif period:
        kw["period"] = period
    else:
        kw.update(_DEFAULT_SPAN[tf])
    df = yf.Ticker(slug_of(symbol).upper()).history(**kw)
    bars = []
    for ts, row in df.iterrows():
        o, h, l, c = row["Open"], row["High"], row["Low"], row["Close"]
        if any(x != x for x in (o, h, l, c)):      # NaN guard (holiday / partial rows)
            continue
        v = row.get("Volume", 0)
        bars.append((int(ts.timestamp()), round(float(o), 4), round(float(h), 4),
                     round(float(l), 4), round(float(c), 4), int(v) if v == v else 0))
    bars.sort(key=lambda b: b[0])
    dedup = {b[0]: b for b in bars}                # Yahoo occasionally repeats a stamp
    return [dedup[t] for t in sorted(dedup)]


def write_snapshot(symbol: str, tf: str, bars: list[tuple], tag: str | None = None,
                   source: str = "YF") -> str:
    """Write bars in the ``data/live`` contract; returns the path."""
    asof = dt.datetime.now(dt.timezone.utc).date().isoformat()
    tag = tag or asof[:7]
    os.makedirs(LIVE, exist_ok=True)
    out = {"symbol": f"{source}:{slug_of(symbol).upper()}", "interval": tf, "asof": asof,
           "bars": [{"t": t, "o": o, "h": h, "l": l, "c": c, "v": v} for t, o, h, l, c, v in bars]}
    path = snapshot_path(symbol, tf, tag)
    with open(path, "w") as fh:
        json.dump(out, fh)
    return path


# ----------------------------------------------------------------------------
# fixture regeneration (data/<slug>.py)
# ----------------------------------------------------------------------------
def _fmt_array(name: str, rows: list[tuple], width: int = 108) -> str:
    """``NAME = [`` + wrapped rows + ``]`` — several tuples per line, diff-friendly."""
    lines, cur = [], "   "
    for r in rows:
        s = " " + repr(tuple(r)) + ","
        if len(cur) + len(s) > width and cur.strip():
            lines.append(cur)
            cur = "   "
        cur += s
    if cur.strip():
        lines.append(cur)
    return f"{name} = [\n" + "\n".join(lines) + "\n]\n"


def _curated_tail(path: str) -> str:
    """Hand-maintained block (e.g. MRVL MACRO_PIVOTS) carried over on regeneration."""
    if not os.path.exists(path):
        return ""
    with open(path) as fh:
        text = fh.read()
    if _CURATED_MARKER in text:
        return text.split(_CURATED_MARKER, 1)[1].lstrip("\n")
    # legacy file: keep MACRO_PIVOTS (and its leading comment lines) if present
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("MACRO_PIVOTS"):
            j = i
            while j > 0 and lines[j - 1].startswith("#"):
                j -= 1
            return "\n".join(lines[j:]).rstrip("\n") + "\n"
    return ""


def build_fixture_arrays(daily: list[tuple], weekly: list[tuple], h1: list[tuple]) -> dict:
    h4 = resample_4h(h1)
    return {
        "WEEKLY": [(t, h, l, c) for t, _o, h, l, c, _v in slice_from(weekly, FIXTURE_WEEKLY_START)],
        "DAILY": slice_from(daily, FIXTURE_DAILY_START),
        "H4": [(t, h, l, c) for t, _o, h, l, c, _v in h4[-FIXTURE_H4_BARS:]],
        "H1": [(t, o, h, l, c) for t, o, h, l, c, _v in h1[-FIXTURE_H1_BARS:]],
        "FRESH_4H_VOL": h4[-FIXTURE_FRESH_BARS:],
    }


def write_fixture_module(symbol: str, arrays: dict) -> str:
    sym = slug_of(symbol).upper()
    path = os.path.join(DATA, f"{slug_of(symbol)}.py")
    tail = _curated_tail(path)
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    last = arrays["DAILY"][-1] if arrays["DAILY"] else None
    last_s = (f"last daily bar {dt.datetime.fromtimestamp(last[0], NY).date()} close {last[4]}"
              if last else "no daily bars")
    head = (f'"""{sym} price data — auto-generated by data/fetch.py from Yahoo Finance '
            f'(yfinance) on {today}; {last_s}.\n'
            'WEEKLY=(t,h,l,c)  DAILY=(t,o,h,l,c,v)  H4=(t,h,l,c)  H1=(t,o,h,l,c)  '
            'FRESH_4H_VOL=(t,o,h,l,c,v)\n'
            't = unix seconds UTC; split-adjusted (not dividend-adjusted); regular session only; '
            '4h bars open 09:30/13:30 ET.\n'
            f'Regenerate:  python3 data/fetch.py {sym} --fixtures\n"""\n')
    body = "".join(_fmt_array(k, v) + "\n" for k, v in arrays.items())
    text = head + body
    if tail:
        text += _CURATED_MARKER + "\n" + tail
    with open(path, "w") as fh:
        fh.write(text)
    return path


def refresh(symbols=("AVGO", "MRVL"), tfs=("1d", "1w", "1h", "4h"), tag: str | None = None,
            fixtures: bool = False, log=print) -> dict:
    """Fetch snapshots for each symbol/tf (and fixtures if asked). Returns {symbol: {tf: path}}."""
    written: dict = {}
    for sym in symbols:
        written[sym] = {}
        got: dict = {}
        need = set(tfs) | ({"1d", "1w", "1h"} if fixtures else set())
        if "4h" in need:
            need.add("1h")
        if "1w" in need:
            need.add("1d")
        for tf in ("1d", "1h", "15m"):
            if tf in need:
                got[tf] = fetch_bars(sym, tf)
        if "4h" in need:
            got["4h"] = resample_4h(got["1h"])
        if "1w" in need:
            got["1w"] = resample_weekly(got["1d"])
        for tf in tfs:
            bars = got[tf]
            if not bars:
                log(f"{sym} {tf}: no bars returned — skipped")
                continue
            p = write_snapshot(sym, tf, bars, tag=tag)
            written[sym][tf] = p
            d0 = dt.datetime.fromtimestamp(bars[0][0], NY).date()
            d1 = dt.datetime.fromtimestamp(bars[-1][0], NY).date()
            log(f"wrote {os.path.relpath(p, ROOT)}: {len(bars)} bars  {d0} -> {d1}")
        if fixtures:
            arrays = build_fixture_arrays(got["1d"], got["1w"], got["1h"])
            p = write_fixture_module(sym, arrays)
            written[sym]["fixture"] = p
            log(f"wrote {os.path.relpath(p, ROOT)}: " +
                ", ".join(f"{k}={len(v)}" for k, v in arrays.items()))
    return written


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__.split("CLI::", 1)[-1])
    ap.add_argument("symbols", nargs="*", default=["AVGO", "MRVL"])
    ap.add_argument("--tf", nargs="+", default=["1d", "1w", "1h", "4h"], choices=TIMEFRAMES)
    ap.add_argument("--tag", default=None, help="snapshot tag (default: current YYYY-MM)")
    ap.add_argument("--fixtures", action="store_true",
                    help="also regenerate data/<slug>.py arrays (WEEKLY/DAILY/H4/H1/FRESH_4H_VOL)")
    a = ap.parse_args(argv)
    refresh([s.upper() for s in a.symbols], tfs=a.tf, tag=a.tag, fixtures=a.fixtures)


if __name__ == "__main__":
    main(sys.argv[1:])
