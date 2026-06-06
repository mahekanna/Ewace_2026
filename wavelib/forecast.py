"""
forecast.py  —  project the NEXT wave(s) from the current count.
================================================================
Everything else in wavelib *labels* completed structure; this module *forecasts*.
Given the anchored primary count, it projects what comes next — the expected
direction, Fibonacci target zone(s), and the invalidation level — with the same
honest (often low) confidence as the count it is built on.

CAUSAL: built from confirmed pivots only; targets are projections, not promises.
Pure stdlib.
"""
from __future__ import annotations
from dataclasses import dataclass

from .toolkit import fib_retrace
from .rules import triangle_thrust
from .wavetree import wave_counts
from .automation import swing_sequence


@dataclass
class WaveForecast:
    as_of_price: float
    pattern: str                 # the current (just-completed) structure
    next_wave: str               # what is expected next
    direction: str               # "up" | "down"
    targets: list                # [(label, price), ...] projected zone
    invalidation: float          # level that voids this forecast
    confidence: float            # inherited from the count — honest, often low
    sequence_status: str         # EWF swing-sequence overlay
    rationale: str

    def __str__(self):
        t = "; ".join(f"{lab} ${p:,.2f}" for lab, p in self.targets)
        return (f"Next: {self.next_wave} | targets: {t} | invalidation ${self.invalidation:,.2f} "
                f"| confidence {self.confidence:.0%} ({self.sequence_status})\n  {self.rationale}")


def forecast_from_count(pc, price, sequence_status="INCOMPLETE") -> "WaveForecast":
    """Project the next wave from an AnchoredCount `pc`. The next wave OPPOSES the
    last completed leg and is anchored at the MOST RECENT pivot, with bounded
    Fibonacci targets (clamped to sane values), so projections stay local to the
    current price rather than exploding off the whole structure's range."""
    legs = [n for _lab, n in pc.labels]
    if not legs:
        return None
    first, last = legs[0], legs[-1]
    struct_up = last.end.price > first.start.price
    last_up = last.end.price > last.start.price
    direction = "down" if last_up else "up"          # next move opposes the last leg
    sgn = 1 if direction == "up" else -1
    anchor = last.end.price                           # most recent confirmed pivot
    pat = pc.pattern
    seq_note = ("swing-sequence INCOMPLETE — the current leg may extend first"
                if sequence_status == "INCOMPLETE" else f"swing-sequence {sequence_status}")

    if pat in ("IMPULSE", "DIAGONAL"):
        hi, lo = (last.end.price, first.start.price) if struct_up else (first.start.price, last.end.price)
        retr = fib_retrace(hi, lo)                    # bounded within the structure
        targets = [(f"{r:.3f} retrace", retr[r]) for r in (0.382, 0.5, 0.618)]
        invalid = first.start.price
        nxt = f"corrective A-B-C ({direction})"
        why = (f"5-wave {pat.lower()} complete; a 3-wave correction retracing "
               "~38.2-61.8% of it is expected before the trend resumes.")
    elif pat in ("ZIGZAG", "FLAT", "WXY", "CORRECTION"):
        ll = last.length                              # project off the LAST leg (local)
        targets = [("0.618x last leg", anchor + sgn * 0.618 * ll),
                   ("1.000x last leg", anchor + sgn * 1.000 * ll),
                   ("1.618x last leg", anchor + sgn * 1.618 * ll)]
        invalid = anchor                              # a break past the last pivot voids it
        nxt = f"new impulse ({direction})"
        why = ("3-wave correction appears complete; trend resumption is expected, "
               "projected as Fibonacci multiples of the last leg from the recent pivot.")
    elif pat == "TRIANGLE":
        widest = max(l.length for l in legs)
        direction = "up" if struct_up else "down"
        sgn = 1 if direction == "up" else -1
        th = triangle_thrust(widest, anchor, sgn)
        targets = [("thrust min (0.75x)", th["min"]), ("thrust max (1.25x)", th["max"])]
        invalid = first.start.price
        nxt = f"post-triangle thrust ({direction})"
        why = (f"triangle complete; a thrust of ~75-125% of the widest leg "
               f"({widest:.2f}) is expected.")
    else:
        return None

    # clamp to sane prices (drop non-positive / absurd projections)
    targets = [(lab, round(p, 2)) for lab, p in targets if 0 < p < price * 3]
    # honesty: if price has run far past the last CONFIRMED pivot, a big unconfirmed
    # leg is in progress and the confirmed-structure forecast lags reality.
    gap = abs(price - anchor) / price if price else 0.0
    caveat = ""
    if gap > 0.15:
        caveat = (f" CAVEAT: price (${price:,.2f}) is {gap:.0%} past the last confirmed "
                  f"pivot (${anchor:,.2f}) — a large unconfirmed leg is in progress, so "
                  "this forecast assumes the confirmed count and likely lags; let the "
                  "current leg confirm first.")
    return WaveForecast(price, pat, nxt, direction, targets, round(invalid, 2),
                        pc.confidence, sequence_status, why + " " + seq_note + caveat)


def forecast_waves(bars, scales=(0.03, 0.05, 0.08), window: int = 300) -> "WaveForecast":
    """Forecast the next wave(s) from the RECENT structure (last `window` bars at
    FINE scales, so the count's legs are a local sub-move near the current price —
    not the whole multi-month range). Returns a WaveForecast or None. Confidence
    is the count's honest confidence — treat targets as a zone, not a prediction."""
    recent = bars[-window:] if len(bars) > window else bars
    counts = wave_counts(recent, scales, max_alternates=0)
    if not counts:
        return None
    seq = swing_sequence(bars=recent, pct=0.10)
    return forecast_from_count(counts[0], recent[-1][4], seq["status"])
