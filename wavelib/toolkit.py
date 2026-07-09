"""
wavelib.toolkit — LEGACY SHIM over the ewave platform (docs/ARCHITECTURE.md D2).
================================================================================
The implementations moved:
  zigzag_causal / zigzag_multiscale / _causal_atr -> ewave.pivots.percentage_reversal
  swing_pivots                                    -> ewave.pivots.fractal
  zigzag (NON-CAUSAL, plotting only)              -> ewave.pivots.repainting
  pivots_to_waves                                 -> ewave.pivots.models
  fib_extension/fib_retrace/fib_cluster/
  wave_ratio/blue_box_zone                        -> ewave.rules.fib
  Pivot / Wave / Degree                           -> ewave.rules.result

Every historical name still imports from here and is the SAME object as the
ewave one. The NeoWave helpers that duplicated rules.py with divergent APIs
(SBResult-returning similarity_and_balance, tuple-returning is_terminal,
str-returning retracement_logic, this module's project_wave5 variant,
terminal_retrace_projection) were the F2 debt: they are NOT part of ewave —
they live on below for legacy callers and the historical self-test only.
Prefer the RuleResult versions in wavelib.rules / ewave.rules.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

try:
    from ewave.rules.result import PHI, Degree, Pivot, Wave       # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))
    from ewave.rules.result import PHI, Degree, Pivot, Wave       # noqa: F401

from ewave.pivots.percentage_reversal import (                    # noqa: F401,E402
    causal_atr as _causal_atr, zigzag_causal, zigzag_multiscale)
from ewave.pivots.fractal import swing_pivots                     # noqa: F401,E402
from ewave.pivots.repainting import zigzag                        # noqa: F401,E402
from ewave.pivots.models import pivots_to_waves                   # noqa: F401,E402
from ewave.rules.fib import (                                     # noqa: F401,E402
    blue_box_zone, fib_cluster, fib_extension, fib_retrace, wave_ratio)


# --------------------------------------------------------------------------- #
# LEGACY-ONLY duplicates (F2). Deliberately NOT in ewave — see module docstring.
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
    """LEGACY variant returning SBResult; prefer wavelib.rules.similarity_and_balance
    (RuleResult). NeoWave: two adjacent corrective waves (e.g. 2 vs 4) must relate
    in BOTH price and time within roughly lo..hi (default 1/3 .. 3x)."""
    pr = a.length / b.length if b.length else float("nan")
    tr = a.days / b.days if b.days else float("nan")
    pok = lo <= pr <= hi
    tok = lo <= tr <= hi
    note = "balanced" if (pok and tok) else (
        "time out of band" if pok else "price out of band" if tok else "both out of band")
    return SBResult(round(pr, 3), round(tr, 3), pok, tok, note)


def retracement_logic(retrace_pct: float) -> str:
    """LEGACY variant returning a str; prefer wavelib.rules.retracement_logic."""
    if retrace_pct < 0.382:
        return "prior leg = an extended 3rd; you are likely in a 4th wave"
    if retrace_pct < 0.618:
        return "prior leg = a 1st or 5th; current move = 2nd/4th (normal)"
    if retrace_pct <= 1.0:
        return "deep: prior leg = a-wave or 1st; current = 2nd / B / X (sharp)"
    return "retrace > 100% -> NOT a retracement; trend change or larger structure"


def is_terminal(legs: list) -> tuple:
    """LEGACY variant returning (bool, str); prefer wavelib.rules.is_terminal."""
    if len(legs) != 5:
        return False, f"need 5 legs, got {len(legs)}"
    w1, w2, w3, w4, w5 = legs
    up = w1.up
    w1_end = w1.end.price
    w4_end = w4.end.price
    overlap = (w4_end < w1_end) if up else (w4_end > w1_end)
    if not overlap:
        return False, "no wave4/wave1 overlap -> impulse, not terminal"
    contracting = (w5.length < w3.length < w1.length)
    shape = "contracting (textbook)" if contracting else "expanding/irregular (rarer)"
    return True, f"terminal: wave4 overlaps wave1; trendlines {shape}"


def terminal_retrace_projection(build_days: float, top_t: float,
                                origin_price: float,
                                frac=(0.25, 0.33, 0.5)) -> dict:
    """LEGACY; prefer wavelib.rules.terminal_retrace_window. NeoWave: a terminal
    is fully retraced to its ORIGIN in ~1/4..1/2 the time it took to build."""
    out = {"origin_price": origin_price, "build_days": round(build_days, 1), "windows": {}}
    for f in frac:
        done_t = top_t + build_days * f * 86400
        out["windows"][f] = {
            "days_after_top": round(build_days * f, 1),
            "approx_date": datetime.fromtimestamp(done_t, tz=timezone.utc).strftime("%Y-%m-%d"),
        }
    return out


def project_wave5(w1_len: float, w3_len: float, w4_low: float,
                  prior_high: float) -> dict:
    """LEGACY variant (different keys); prefer wavelib.rules.project_wave5.
    Projects wave-5 targets and flags truncation risk."""
    eq = round(w4_low + w1_len, 2)
    ext = round(w4_low + 0.618 * w3_len, 2)
    ext_w1 = round(w4_low + PHI * w1_len, 2)       # extended fifth (1.618xw1)
    short = round(w4_low + 0.382 * w3_len, 2)      # short fifth (0.382xw3)
    truncation = eq < prior_high * 1.03            # <3% above old high
    return {
        "w5_equality(w1)": eq,
        "w5_0.618xw3": ext,
        "w5_1.618xw1": ext_w1,
        "w5_0.382xw3": short,
        "prior_high": prior_high,
        "truncation_risk": truncation,
        "note": ("TRUNCATION RISK: w5 barely clears the prior high"
                 if truncation else "healthy new-high projection"),
    }


# --------------------------------------------------------------------------- #
# Demo / self-test on AVGO + MRVL pivots (historical; exercised by CI)
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
