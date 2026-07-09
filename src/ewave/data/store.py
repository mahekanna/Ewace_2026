"""
data.store — the contract-JSON store over data/live/.
=====================================================
Path scheme (unchanged from the research phase, so the two-session git workflow
in docs/COLLAB_RUNBOOK.md keeps working):

    data/live/<slug>_<tf>[_eh]_<stamp>.json      e.g. avgo_15m_2026-06.json

`slug` = lowercase bare ticker, `stamp` = YYYY-MM (fetch month). `latest()`
resolves the newest stamp for a symbol+timeframe. `merge()` folds new bars into
an existing series (dedupe on t, last write wins, ascending).
"""
from __future__ import annotations

import glob
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .models import BarSeries

_FNAME = re.compile(r"^(?P<slug>[a-z0-9]+)_(?P<tf>\d+[mhdw])(?P<eh>_eh)?_(?P<stamp>\d{4}-\d{2})\.json$")


def slugify(symbol: str) -> str:
    """'ALPACA:AVGO' -> 'avgo'."""
    return re.sub(r"[^a-z0-9]", "", symbol.split(":")[-1].lower())


def default_store_dir() -> Path:
    env = os.environ.get("EWAVE_STORE_DIR")
    if env:
        return Path(env)
    cwd = Path.cwd() / "data" / "live"
    if cwd.is_dir():
        return cwd
    here = Path(__file__).resolve()
    for parent in here.parents:
        cand = parent / "data" / "live"
        if cand.is_dir():
            return cand
    return cwd


class Store:
    def __init__(self, base_dir: Optional[str] = None):
        self.dir = Path(base_dir) if base_dir else default_store_dir()

    def path_for(self, symbol: str, tf: str, stamp: Optional[str] = None,
                 extended: bool = False) -> Path:
        stamp = stamp or datetime.now(timezone.utc).strftime("%Y-%m")
        eh = "_eh" if extended else ""
        return self.dir / f"{slugify(symbol)}_{tf}{eh}_{stamp}.json"

    def list(self, symbol: Optional[str] = None, tf: Optional[str] = None,
             extended: Optional[bool] = None) -> List[Path]:
        """All contract files, optionally filtered; sorted by (slug, tf, stamp)."""
        out = []
        for p in sorted(glob.glob(str(self.dir / "*.json"))):
            m = _FNAME.match(os.path.basename(p))
            if not m:
                continue
            if symbol is not None and m["slug"] != slugify(symbol):
                continue
            if tf is not None and m["tf"] != tf:
                continue
            if extended is not None and bool(m["eh"]) is not extended:
                continue
            out.append(Path(p))
        return out

    def latest(self, symbol: str, tf: str, extended: bool = False) -> Optional[Path]:
        """Newest-stamp file for symbol+tf, or None."""
        files = self.list(symbol, tf, extended)
        if not files:
            return None
        return max(files, key=lambda p: _FNAME.match(p.name)["stamp"])

    def read(self, symbol: str, tf: str, extended: bool = False) -> BarSeries:
        p = self.latest(symbol, tf, extended)
        if p is None:
            raise FileNotFoundError(
                f"no cached bars for {symbol} {tf} under {self.dir} "
                "(run `ewave fetch-data` or scripts/mcp_export.py)")
        return self.read_path(p)

    @staticmethod
    def read_path(path) -> BarSeries:
        with open(path) as f:
            return BarSeries.from_dict(json.load(f))

    def write(self, series: BarSeries, stamp: Optional[str] = None,
              extended: bool = False) -> Path:
        self.dir.mkdir(parents=True, exist_ok=True)
        p = self.path_for(series.symbol, series.interval, stamp, extended)
        with open(p, "w") as f:
            json.dump(series.to_dict(), f)
        return p

    def merge_write(self, series: BarSeries, stamp: Optional[str] = None,
                    extended: bool = False) -> Path:
        """Fold `series` into the existing file for its symbol+tf (if any):
        dedupe on t — and for daily/weekly bars ALSO by calendar day, since
        different sources anchor the same day at different clock times (a raw-t
        merge would double-count the overlap). New bars win."""
        existing = self.latest(series.symbol, series.interval, extended)
        if existing is not None:
            old = self.read_path(existing)
            old_rows = old.tuples()
            iv = series.interval.lower()
            if iv.endswith("_eh"):
                iv = iv[:-3]
            if iv in ("1d", "1w"):
                new_days = {self._ny_date(r[0]) for r in series.tuples()}
                old_rows = [r for r in old_rows
                            if self._ny_date(r[0]) not in new_days]
            merged = BarSeries.from_rows(
                series.symbol, series.interval, series.asof,
                old_rows + series.tuples(),
                source=series.source or old.source,
                adjustment=series.adjustment or old.adjustment,
                session=series.session or old.session)
            series = merged
        return self.write(series, stamp, extended)

    @staticmethod
    def _ny_date(t):
        from datetime import datetime, timedelta, timezone
        try:
            from zoneinfo import ZoneInfo
            tz = ZoneInfo("America/New_York")
        except Exception:
            tz = timezone(timedelta(hours=-4))
        return datetime.fromtimestamp(t, tz).date()
