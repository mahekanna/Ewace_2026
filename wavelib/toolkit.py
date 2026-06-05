"""
neowave_toolkit.py
==================
A compact, dependency-free toolkit for applying classic Elliott Wave and
selected NeoWave (Glenn Neely) construction rules to OHLC price data.

Implements the machinery used to analyse AVGO / MRVL:
  - ZigZag pivot detection (percentage-reversal, intrabar extremes)
  - Fibonacci wave-relationship helpers
  - Rule of Similarity & Balance (price AND time, 1/3 .. 3x band)
  - Retracement-logic wave identification (NeoWave depth tables)
  - Terminal-impulsion detection (3-3-3-3-3, wave-4/1 overlap)
  - Terminal full-retrace TIME projection
  - Fifth-wave projection with truncation flag

Bars are tuples/lists of (t, o, h, l, c) with t in unix seconds.
No third-party dependencies (pure stdlib). Python 3.9+.

Author: built with Claude. Educational use; not investment advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal, Optional

PHI = 1.6180339887

# --------------------------------------------------------------------------- #
# Data structures — share the canonical Pivot/Wave from rules.py when used as
# a package; fall back to local definitions for standalone execution.
# --------------------------------------------------------------------------- #
try:
    from .rules import Pivot, Wave           # package context (one canonical class)
except Exception:                            # standalone: define locally
    @dataclass
    class Pivot:
        t: float
        price: float
        kind: Literal["H", "L"]
        @property
        def date(self) -> str:
            return datetime.fromtimestamp(self.t, tz=timezone.utc).strftime("%Y-%m-%d")

    @dataclass
    class Wave:
        start: Pivot
        end: Pivot
        label: str = ""
        @property
        def length(self): return abs(self.end.price - self.start.price)
        @property
        def signed(self): return self.end.price - self.start.price
        @property
        def days(self): return (self.end.t - self.start.t) / 86400.0
        @property
        def up(self): return self.end.price > self.start.price
        def retr(self, other): return self.length / other.length if other.length else float("nan")
        retrace_of = retr


# --------------------------------------------------------------------------- #
# 1. ZigZag pivot detection
# --------------------------------------------------------------------------- #
def zigzag(bars, pct: float = 0.10) -> list[Pivot]:
    """
    Percentage-reversal ZigZag on intrabar highs/lows.

    bars : iterable of (t, o, h, l, c)
    pct  : reversal threshold (0.10 = 10%)
    returns alternating H/L pivots (the wave skeleton).
    """
    bars = list(bars)
    if not bars:
        return []
    piv: list[Pivot] = []
    trend = 0                                  # +1 up, -1 down, 0 unseeded
    et, ep = bars[0][0], bars[0][4]            # extreme time / price
    for t, o, h, l, c in bars:
        if trend > 0:                          # tracking a high
            if h > ep:
                et, ep = t, h
            if l < ep * (1 - pct):
                piv.append(Pivot(et, ep, "H"))
                trend, et, ep = -1, t, l
        elif trend < 0:                        # tracking a low
            if l < ep:
                et, ep = t, l
            if h > ep * (1 + pct):
                piv.append(Pivot(et, ep, "L"))
                trend, et, ep = 1, t, h
        else:                                  # seed (avoid dual-branch corruption)
            if h > ep * (1 + pct):
                piv.append(Pivot(et, ep, "L")); trend, et, ep = 1, t, h
            elif l < ep * (1 - pct):
                piv.append(Pivot(et, ep, "H")); trend, et, ep = -1, t, l
            else:
                if h > ep: et, ep = t, h
                if l < bars[0][3]: pass
    piv.append(Pivot(et, ep, "H" if trend > 0 else "L"))
    # collapse consecutive same-kind pivots, keep the more extreme
    out: list[Pivot] = []
    for p in piv:
        if out and out[-1].kind == p.kind:
            if (p.kind == "H" and p.price > out[-1].price) or \
               (p.kind == "L" and p.price < out[-1].price):
                out[-1] = p
        else:
            out.append(p)
    return out


def pivots_to_waves(pivots: list[Pivot], labels: Optional[list[str]] = None) -> list[Wave]:
    waves = [Wave(pivots[i], pivots[i + 1]) for i in range(len(pivots) - 1)]
    if labels:
        for w, lab in zip(waves, labels):
            w.label = lab
    return waves


# --------------------------------------------------------------------------- #
# 2. Fibonacci helpers
# --------------------------------------------------------------------------- #
def fib_extension(w1_len: float, base: float, ratios=(1.0, 1.618, 2.0, 2.618, 3.0, 3.618)) -> dict:
    """Project upward fib extensions of `w1_len` added to `base`."""
    return {r: round(base + r * w1_len, 2) for r in ratios}


def fib_retrace(high: float, low: float, ratios=(0.236, 0.382, 0.5, 0.618, 0.786)) -> dict:
    rng = high - low
    return {r: round(high - r * rng, 2) for r in ratios}


def wave_ratio(a: Wave, b: Wave) -> float:
    return a.length / b.length if b.length else float("nan")


# --------------------------------------------------------------------------- #
# 3. NeoWave — Rule of Similarity & Balance
# --------------------------------------------------------------------------- #
@dataclass
class SBResult:
    price_ratio: float
    time_ratio: float
    price_ok: bool
    time_ok: bool
    note: str

    @property
    def passes(self) -> bool:
        return self.price_ok and self.time_ok


def similarity_and_balance(a: Wave, b: Wave, lo: float = 1 / 3, hi: float = 3.0) -> SBResult:
    """
    NeoWave: two adjacent corrective waves (e.g. 2 vs 4) must relate in BOTH
    price and time within roughly lo..hi (default 1/3 .. 3x).
    """
    pr = a.length / b.length if b.length else float("nan")
    tr = a.days / b.days if b.days else float("nan")
    pok = lo <= pr <= hi
    tok = lo <= tr <= hi
    note = "balanced" if (pok and tok) else (
        "time out of band" if pok else "price out of band" if tok else "both out of band")
    return SBResult(round(pr, 3), round(tr, 3), pok, tok, note)


# --------------------------------------------------------------------------- #
# 4. NeoWave — retracement logic (depth -> implied wave identity)
# --------------------------------------------------------------------------- #
def retracement_logic(retrace_pct: float) -> str:
    """
    Given how deeply the CURRENT move retraces the PRIOR leg, infer what the
    prior leg likely was (Neely's depth heuristics).
    retrace_pct is a fraction (0.30 = 30%).
    """
    if retrace_pct < 0.382:
        return "prior leg = an extended 3rd; you are likely in a 4th wave"
    if retrace_pct < 0.618:
        return "prior leg = a 1st or 5th; current move = 2nd/4th (normal)"
    if retrace_pct <= 1.0:
        return "deep: prior leg = a-wave or 1st; current = 2nd / B / X (sharp)"
    return "retrace > 100% -> NOT a retracement; trend change or larger structure"


# --------------------------------------------------------------------------- #
# 5. NeoWave — terminal-impulsion detection + retrace timing
# --------------------------------------------------------------------------- #
def is_terminal(legs: list[Wave]) -> tuple[bool, str]:
    """
    Detect a terminal impulsion (NeoWave) / ending diagonal (classic).
    Expects 5 legs. Key test: wave 4 OVERLAPS wave 1's territory.
    """
    if len(legs) != 5:
        return False, f"need 5 legs, got {len(legs)}"
    w1, w2, w3, w4, w5 = legs
    up = w1.up
    w1_end = w1.end.price
    w4_end = w4.end.price
    overlap = (w4_end < w1_end) if up else (w4_end > w1_end)
    if not overlap:
        return False, "no wave4/wave1 overlap -> impulse, not terminal"
    highs = [w1.end.price, w3.end.price, w5.end.price] if up else \
            [w1.start.price]  # simplified
    contracting = (w5.length < w3.length < w1.length)
    shape = "contracting (textbook)" if contracting else "expanding/irregular (rarer)"
    return True, f"terminal: wave4 overlaps wave1; trendlines {shape}"


def terminal_retrace_projection(build_days: float, top_t: float,
                                origin_price: float,
                                frac=(0.25, 0.33, 0.5)) -> dict:
    """
    NeoWave: a terminal is fully retraced to its ORIGIN in ~1/4..1/2 the time
    it took to build. Returns target completion dates for each fraction.
    """
    out = {"origin_price": origin_price, "build_days": round(build_days, 1), "windows": {}}
    for f in frac:
        done_t = top_t + build_days * f * 86400
        out["windows"][f] = {
            "days_after_top": round(build_days * f, 1),
            "approx_date": datetime.fromtimestamp(done_t, tz=timezone.utc).strftime("%Y-%m-%d"),
        }
    return out


# --------------------------------------------------------------------------- #
# 6. Fifth-wave projection + truncation flag
# --------------------------------------------------------------------------- #
def project_wave5(w1_len: float, w3_len: float, w4_low: float,
                  prior_high: float) -> dict:
    """
    Project wave-5 targets and flag truncation risk.
      equality : w5 = w1
      ext      : w5 = 0.618 * w3
    Truncation risk if the equality target barely exceeds prior_high.
    """
    eq = round(w4_low + w1_len, 2)
    ext = round(w4_low + 0.618 * w3_len, 2)
    truncation = eq < prior_high * 1.03            # <3% above old high
    return {
        "w5_equality(w1)": eq,
        "w5_0.618xw3": ext,
        "prior_high": prior_high,
        "truncation_risk": truncation,
        "note": ("TRUNCATION RISK: w5 barely clears the prior high"
                 if truncation else "healthy new-high projection"),
    }


# --------------------------------------------------------------------------- #
# Demo / self-test on AVGO + MRVL pivots
# --------------------------------------------------------------------------- #
def _demo():
    def P(d, price, kind):
        t = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()
        return Pivot(t, price, kind)

    print("=" * 60, "\nAVGO\n", "=" * 60, sep="")
    avgo = [P("2022-10-13", 41.51, "L"), P("2024-12-16", 251.88, "H"),
            P("2025-04-07", 138.10, "L"), P("2026-06-03", 495.00, "H")]
    w = pivots_to_waves(avgo, ["(I)", "(II)", "(III)"])
    wI, wII, wIII = w
    print("wave (III)/(I) ratio:", round(wave_ratio(wIII, wI), 2))
    # terminal of wave 5 (4h legs)
    term = [Wave(P("2026-03-30", 289.96, "L"), P("2026-04-21", 429.31, "H")),
            Wave(P("2026-04-21", 429.31, "H"), P("2026-04-23", 394.66, "L")),
            Wave(P("2026-04-23", 394.66, "L"), P("2026-05-14", 442.36, "H")),
            Wave(P("2026-05-14", 442.36, "H"), P("2026-05-19", 405.87, "L")),
            Wave(P("2026-05-19", 405.87, "L"), P("2026-06-03", 495.00, "H"))]
    ok, why = is_terminal(term)
    print("terminal?", ok, "->", why)
    build = (term[-1].end.t - term[0].start.t) / 86400
    proj = terminal_retrace_projection(build, term[-1].end.t, 289.96)
    print("retrace-to-$290 windows:", {f: v["approx_date"] for f, v in proj["windows"].items()})
    print("wave5 (deep IV@290):",
          project_wave5(wI.length, wIII.length, 289.96, 495.00))

    print("\n" + "=" * 60, "\nMRVL\n", "=" * 60, sep="")
    mrvl = [P("2022-12-30", 33.75, "L"), P("2025-01-21", 127.48, "H"),
            P("2025-04-07", 47.09, "L"), P("2025-12-04", 102.77, "H"),
            P("2026-02-09", 76.07, "L"), P("2026-06-03", 324.20, "H")]
    mw = pivots_to_waves(mrvl, ["(I)", "(II)", "((1))", "((2))", "((3))"])
    print("(II) retrace of (I): {:.1%}".format(mw[1].retrace_of(mw[0])),
          "->", retracement_logic(mw[1].retrace_of(mw[0])))
    print("((3))/((1)) ratio:", round(wave_ratio(mw[4], mw[2]), 1),
          "(extended 3rd; S&B-stretched)")
    sb = similarity_and_balance(mw[1], mw[3])   # (II) vs ((2)) illustrative
    print("S&B (II vs ((2))): price", sb.price_ratio, "time", sb.time_ratio, "->", sb.note)
    print("(( 3 )) extension targets:",
          fib_extension(mw[0].length, mw[2].start.price, (3.0, 3.382, 3.618, 4.0)))


if __name__ == "__main__":
    _demo()
