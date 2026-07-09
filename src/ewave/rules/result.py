"""
rules.result — THE canonical data model: Pivot, Wave, Degree, Status, RuleResult.
=================================================================================
Single source of truth (docs/ARCHITECTURE.md D7): every ewave module and the
legacy `wavelib` shim import these classes from here — the historical
rules.py/toolkit.py duplication (roadmap item F2) ends at this module.

This module imports nothing from the rest of ewave (import-graph root).

Causality contract (docs/NO_LOOKAHEAD_POLICY.md): `Pivot.t` is when the price
extreme printed; `Pivot.confirmed_t` is the first bar at which the pivot is
KNOWABLE. Signal logic may use a pivot only from `confirmed_t`; `None` means
provisional (still forming).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

PHI = 1.6180339887
INV_PHI = 0.6180339887


class Degree(Enum):
    """
    Elliott wave degree hierarchy (Frost & Prechter), largest -> smallest.

    Numeric values rank the degrees (higher = larger degree), so degrees compare
    by `.value`. The field is OPTIONAL metadata on Pivot/Wave: `degree is None`
    means "not yet assigned" — the bottom-up Neely constructor populates it.
    See docs/research/01_elliott_wave.md §2.5.
    """
    GRAND_SUPERCYCLE = 9
    SUPERCYCLE = 8
    CYCLE = 7
    PRIMARY = 6
    INTERMEDIATE = 5
    MINOR = 4
    MINUTE = 3
    MINUETTE = 2
    SUBMINUETTE = 1

    @property
    def abbr(self) -> str:
        """Short notation label for the degree."""
        return {
            "GRAND_SUPERCYCLE": "GSC", "SUPERCYCLE": "SC", "CYCLE": "C",
            "PRIMARY": "P", "INTERMEDIATE": "I", "MINOR": "Mn",
            "MINUTE": "mn", "MINUETTE": "mu", "SUBMINUETTE": "smu",
        }[self.name]

    def finer(self) -> Optional["Degree"]:
        """The next-smaller degree, or None at SUBMINUETTE."""
        return Degree(self.value - 1) if self.value > 1 else None

    def coarser(self) -> Optional["Degree"]:
        """The next-larger degree, or None at GRAND_SUPERCYCLE."""
        return Degree(self.value + 1) if self.value < 9 else None


@dataclass
class Pivot:
    t: float
    price: float
    kind: str  # "H" or "L"
    # confirmed_t: bar time at which this pivot's reversal was CONFIRMED (causal
    # discipline — a pivot is only "known" once price reverses past the threshold).
    # None => provisional / still forming (e.g. the final extreme of a series).
    confirmed_t: Optional[float] = None
    degree: Optional["Degree"] = None  # optional wave-degree annotation
    # provenance (ewauto SPEC parity): which detector produced this pivot and
    # with what parameters — e.g. source="pct_reversal", meta={"pct": 0.03}.
    # Defaults keep positional construction and equality of legacy code intact.
    source: str = ""
    meta: Optional[dict] = None

    @property
    def date(self) -> str:
        return datetime.fromtimestamp(self.t, tz=timezone.utc).strftime("%Y-%m-%d")

    @property
    def confirmed(self) -> bool:
        return self.confirmed_t is not None

    # uploads-vocabulary aliases (pivot_time / confirmed_time)
    @property
    def pivot_time(self) -> float:
        return self.t

    @property
    def confirmed_time(self) -> Optional[float]:
        return self.confirmed_t


@dataclass
class Wave:
    start: Pivot
    end: Pivot
    label: str = ""
    degree: Optional["Degree"] = None  # optional wave-degree annotation

    @property
    def length(self) -> float: return abs(self.end.price - self.start.price)

    @property
    def log_length(self) -> float:
        """Wave magnitude in LOG price — the correct measure for Fibonacci/ratio
        comparisons on any instrument spanning >2x (Neely, neowave.com QA #38).
        For small moves log_length ≈ the relative move, so it is safe to use
        everywhere. Falls back to linear if prices are non-positive."""
        s, e = self.start.price, self.end.price
        if s > 0 and e > 0:
            return abs(math.log(e / s))
        return abs(e - s)

    @property
    def signed(self) -> float: return self.end.price - self.start.price

    @property
    def days(self) -> float: return (self.end.t - self.start.t) / 86400.0

    @property
    def up(self) -> bool: return self.end.price > self.start.price

    def retr(self, other: "Wave") -> float:
        return self.length / other.length if other.length else float("nan")
    retrace_of = retr


class Status(Enum):
    """PASS/FAIL = computed verdicts. WARN = guideline miss (never invalidates).
    NA = rule not applicable (arity/precondition). REF = reference-only /
    human-discretion output — must never gate an automated decision.
    UNKNOWN = insufficient confirmed data to decide (never a silent PASS)."""
    PASS = "PASS"; FAIL = "FAIL"; WARN = "WARN"; NA = "N/A"; REF = "REF"
    UNKNOWN = "UNKNOWN"


@dataclass
class RuleResult:
    rule: str
    status: Status
    detail: str
    def __str__(self): return f"[{self.status.value:4}] {self.rule}: {self.detail}"


def _ok(c) -> Status:
    return Status.PASS if c else Status.FAIL


def _within(a, b, lo, hi) -> bool:
    """Is a/b inside [lo, hi]? (generic ratio-band helper used across validators)"""
    r = a / b if b else float("nan")
    return lo <= r <= hi


def _group_similar(vals, lo=1 / 3, hi=3.0) -> bool:
    """Adjacent values all within the lo..hi ratio band (S&B group test)."""
    return all(_within(vals[i], vals[i + 1], lo, hi)
               for i in range(len(vals) - 1)) if len(vals) > 1 else True
