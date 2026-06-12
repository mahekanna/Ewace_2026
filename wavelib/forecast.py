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

from .toolkit import fib_retrace, fib_cluster
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
    cluster: list = None         # [(price, n_overlaps), ...] Fibonacci confluence zones
    time_lo_days: float = 0.0    # NeoWave Similarity & Balance: next wave in [N/3, 3N]
    time_hi_days: float = 0.0
    time_note: str = ""

    def __str__(self):
        t = "; ".join(f"{lab} ${p:,.2f}" for lab, p in self.targets)
        cl = ""
        if self.cluster:
            top = self.cluster[0]
            cl = f"\n  confluence: ${top[0]:,.2f} ({top[1]} projections overlap)"
        tm = f"\n  {self.time_note}" if self.time_note else ""
        return (f"Next: {self.next_wave} | targets: {t} | invalidation ${self.invalidation:,.2f} "
                f"| confidence {self.confidence:.0%} ({self.sequence_status})\n  {self.rationale}"
                + cl + tm)


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
    last_days = (last.end.t - last.start.t) / 86400.0
    seq_note = ("swing-sequence INCOMPLETE — the current leg may extend first"
                if sequence_status == "INCOMPLETE" else f"swing-sequence {sequence_status}")
    proj = []                                         # ALL independent projections -> cluster

    if pat in ("IMPULSE", "DIAGONAL"):
        # 5-wave move complete -> a 3-wave CORRECTION retraces it (retracement targets)
        hi, lo = (last.end.price, first.start.price) if struct_up else (first.start.price, last.end.price)
        retr = fib_retrace(hi, lo, ratios=(0.236, 0.382, 0.5, 0.618, 0.786))
        targets = [(f"{r:.3f} retrace", retr[r]) for r in (0.382, 0.5, 0.618)]
        proj = list(retr.values())
        if len(legs) >= 4:                            # wave-4 low is the classic A-B-C magnet
            proj.append(legs[3].end.price)
        invalid = first.start.price
        nxt = f"corrective A-B-C ({direction})"
        why = (f"5-wave {pat.lower()} complete; a 3-wave correction retracing "
               "~38.2-61.8% of it is expected before the trend resumes.")
    elif pat in ("ZIGZAG", "FLAT", "WXY", "CORRECTION"):
        # 3-wave correction complete -> a new impulse; project Fibonacci EXTENSIONS of
        # the last leg, incl. the EWF Blue Box (100%-161.8% equal-legs reaction zone).
        ll = last.length
        ext = {r: anchor + sgn * r * ll for r in (0.618, 1.0, 1.272, 1.618, 2.618)}
        targets = [("1.000x (equal legs)", ext[1.0]), ("1.618x (Blue Box top)", ext[1.618]),
                   ("2.618x extension", ext[2.618])]
        proj = list(ext.values())
        invalid = anchor                              # a break past the last pivot voids it
        nxt = f"new impulse ({direction})"
        why = ("3-wave correction appears complete; trend resumption is expected, "
               "projected as Fibonacci EXTENSIONS of the last leg (Blue Box = 1.0-1.618x).")
    elif pat == "TRIANGLE":
        widest = max(l.length for l in legs)
        direction = "up" if struct_up else "down"
        sgn = 1 if direction == "up" else -1
        th = triangle_thrust(widest, anchor, sgn)
        targets = [("thrust min (0.75x)", th["min"]), ("thrust max (1.25x)", th["max"])]
        proj = [th["min"], th["max"], anchor + sgn * widest]
        invalid = first.start.price
        nxt = f"post-triangle thrust ({direction})"
        why = (f"triangle complete; a thrust of ~75-125% of the widest leg "
               f"({widest:.2f}) is expected.")
    else:
        return None

    # clamp to sane prices: a single next-wave target shouldn't be a tiny fraction of
    # or a huge multiple of current price (those come from projecting a macro-degree
    # leg locally). Keep [0.3x, 3x].
    lo_c, hi_c = price * 0.3, price * 3
    targets = [(lab, round(p, 2)) for lab, p in targets if lo_c < p < hi_c]
    # Fibonacci CONFLUENCE: where independent projections overlap is the real target
    cluster = fib_cluster([p for p in proj if lo_c < p < hi_c], tol=0.02)
    cluster = [c for c in cluster if c[1] >= 2] or cluster[:1]
    # NeoWave time projection (Similarity & Balance on TIME): the next same-degree
    # wave should complete in [N/3, 3N] bars where N = the last wave's duration.
    t_lo, t_hi = last_days / 3.0, last_days * 3.0
    time_note = (f"time: next wave likely completes in ~{t_lo:.0f}-{t_hi:.0f} days "
                 f"(NeoWave S&B vs the {last_days:.0f}-day prior wave)")
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
                        pc.confidence, sequence_status, why + " " + seq_note + caveat,
                        cluster=cluster, time_lo_days=round(t_lo, 1),
                        time_hi_days=round(t_hi, 1), time_note=time_note)


def forecast_waves(bars, window: int = None) -> "WaveForecast":
    """Forecast the next wave from the engine's PRIMARY (top-down) count — the same
    count shown on the chart — so the forecast is coherent with the labelled
    structure rather than a separate recent-window read. Pass `window` to forecast
    from only the last N bars (e.g. for intraday). Returns a WaveForecast or None;
    confidence is the count's honest (often low) number — treat targets as a zone."""
    data = bars if (window is None or len(bars) <= window) else bars[-window:]
    counts = wave_counts(data, max_alternates=0)      # top-down primary
    if not counts:
        return None
    seq = swing_sequence(bars=data, pct=0.10)
    return forecast_from_count(counts[0], data[-1][4], seq["status"])


@dataclass
class TradePlan:
    """NeoWave/EWF trading-method synthesis (GAP-2, doc 11 §trading-method).

    Turns a forecast into an actionable-but-honest panel: WHICH WAY, the
    CONFIRMATION trigger to wait for (Neely never acts on the label alone), the
    protective STOP, the structural INVALIDATION, the time-gated TARGETS, and the
    bar WINDOW within which confirmation must arrive (the prior leg's build time).
    Analysis tooling only — not advice; confidence is the count's honest (often low)
    number, so a low-confidence plan is a *reason to wait*, not a signal."""
    symbol: str
    direction: str                # "long" | "short"
    entry_trigger: str            # the confirmation condition to act on
    entry_level: float            # price whose break confirms
    stop_level: float             # protective stop (beyond the last swing)
    invalidation: float           # structural void level
    targets: list                 # [(label, price), ...] next-wave target zone
    confirm_window_bars: int      # Neely time gate: confirm within prior-leg build time
    confidence: float
    rationale: str
    cluster: list = None          # Fibonacci confluence zone(s) — the primary target
    time_lo_days: float = 0.0     # NeoWave time window for the next wave
    time_hi_days: float = 0.0
    alt_flip: float = None        # the ranked ALTERNATE count's invalidation (flip price)
    confluence: int = 0           # independent confirming strands (score_reversal)
    reward_risk: float = 0.0      # R:R to the primary (confluence) target

    def __str__(self):
        t = "; ".join(f"{lab} ${p:,.2f}" for lab, p in self.targets)
        cl = f" | confluence ${self.cluster[0][0]:,.2f}" if self.cluster else ""
        return (f"{self.direction.upper()} on {self.entry_trigger} | stop ${self.stop_level:,.2f} "
                f"| invalidation ${self.invalidation:,.2f} | targets {t}{cl} "
                f"| R:R {self.reward_risk:.1f} | confluence {self.confluence} "
                f"| confirm within {self.confirm_window_bars} bars | conf {self.confidence:.0%}\n"
                f"  {self.rationale}")


def trade_plan(bars, symbol: str = "", window: int = 300) -> "TradePlan":
    """Synthesize a NeoWave trading-method plan from the recent count + forecast.

    The trade is in the direction of the forecast NEXT wave; the entry is gated on a
    CONFIRMATION break of the last confirmed pivot (NeoWave never trades the label
    alone), the stop sits just beyond the last swing, invalidation is the count's
    structural void, and the confirmation must arrive within the prior leg's bar
    count (Neely's time gate). Returns a TradePlan or None. CAUSAL: confirmed
    pivots + the forecast only."""
    recent = bars[-window:] if len(bars) > window else bars
    fc = forecast_waves(bars, window=window)
    if fc is None:
        return None
    counts = wave_counts(recent, (0.03, 0.05, 0.08), max_alternates=1)
    if not counts:
        return None
    legs = [n for _lab, n in counts[0].labels]
    if not legs:
        return None
    last = legs[-1]
    anchor = last.end.price
    direction = "long" if fc.direction == "up" else "short"
    entry_level = round(anchor, 2)
    swing_lo = min(last.start.price, last.end.price)
    swing_hi = max(last.start.price, last.end.price)
    if direction == "long":
        stop = round(swing_lo * 0.99, 2)
        trig = f"break ABOVE last pivot ${entry_level:,.2f}"
    else:
        stop = round(swing_hi * 1.01, 2)
        trig = f"break BELOW last pivot ${entry_level:,.2f}"
    # Neely time gate: confirmation should arrive within the prior leg's build time
    leg_bars = sum(1 for b in recent if last.start.t <= b[0] <= last.end.t)
    confirm_window = max(leg_bars, 1)
    # --- Phase 5 discipline: confluence target, R:R, alternate flip-price, gate ---
    price = recent[-1][4]
    tgt = fc.cluster[0][0] if fc.cluster else (fc.targets[0][1] if fc.targets else anchor)
    risk = abs(entry_level - stop) or 1e-9
    rr = round(abs(tgt - entry_level) / risk, 2)
    # the ALTERNATE count's invalidation = the price that flips the read
    alt_flip = None
    if len(counts) > 1 and counts[1].labels:
        alt_flip = round(counts[1].labels[0][1].start.price, 2)
    # independent confirmation strands at the current price (the confluence gate)
    confl = 0
    try:
        from .confluence import score_reversal
        zone = (min(swing_lo, tgt), max(swing_hi, tgt))
        confl = score_reversal(symbol or "x", recent[-250:], zone,
                               bullish=(direction == "long")).score
    except Exception:
        confl = 0
    rationale = (f"{fc.pattern} appears complete -> expect {fc.next_wave}. NeoWave method: "
                 f"act ONLY on confirmation (the pivot break, within ~{confirm_window} bars); "
                 f"risk to the structural stop; primary target = the Fibonacci confluence "
                 f"(R:R {rr}); flip the read if price breaks the alternate's invalidation. "
                 f"Confidence {fc.confidence:.0%} + confluence {confl} strands — low = wait.")
    return TradePlan(symbol or "", direction, trig, entry_level, stop,
                     fc.invalidation, fc.targets, confirm_window, fc.confidence, rationale,
                     cluster=fc.cluster, time_lo_days=fc.time_lo_days,
                     time_hi_days=fc.time_hi_days, alt_flip=alt_flip,
                     confluence=confl, reward_risk=rr)
