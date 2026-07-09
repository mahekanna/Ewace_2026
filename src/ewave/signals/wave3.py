"""
wave3.py  —  the actual Elliott trade: enter wave 3 on confirmation.
====================================================================
The forecast in `forecast.py` projects the leg AFTER a completed structure — it
never trades waves 3 or 5 (the high-probability legs). This module implements the
professional setup instead:

  1. find an INCOMPLETE impulse: wave 1 (a directional leg) + wave 2 (a 38.2-78.6%
     pullback that does NOT exceed wave 1's origin — Elliott hard rule R1);
  2. ENTRY = the break of the wave-1 extreme (price reclaiming it CONFIRMS wave 3
     has begun — wave 3 must exceed wave 1);
  3. STOP  = just beyond the wave-2 extreme (a structural, count-voiding stop);
  4. TARGETS = Fibonacci EXTENSIONS of wave 1 from the wave-2 extreme
     (1.618x / 2.618x — the canonical wave-3 projections).

Because the stop is ~half of wave 1 and the target is ~1.6x of it, the setup is
naturally asymmetric (R:R ~2+), unlike the next-leg projection (R:R<1). It also
fires SELECTIVELY — only on the confirmation break — not every candle.

Optionally gated by EWO momentum (a real wave 3 expands momentum). CAUSAL: uses
only bars up to the entry candle. Pure stdlib.
"""
from __future__ import annotations
from dataclasses import dataclass

from ..pivots.percentage_reversal import zigzag_causal
from ..patterns.tree import momentum_lookup


@dataclass
class Wave3Signal:
    direction: str          # "long" | "short"
    entry_t: float
    entry: float            # the wave-1 extreme broken on this candle (fill level)
    stop: float             # just beyond the wave-2 extreme (structural)
    targets: list           # [(label, price), ...] wave-3 Fib extensions of wave 1
    reward_risk: float      # to the first target
    w1: tuple               # (origin_price, wave1_extreme) for context
    w2: float               # wave-2 extreme (the pullback low/high)
    retr: float             # wave-2 retracement fraction of wave 1
    ewo: float              # EWO at entry (momentum into wave 3)
    note: str = ""
    strands: int = 0        # confluence strands satisfied (Table D gate)
    t2: float = 0.0         # second target (2.618x W1)
    w1_bars: int = 0        # wave-1 duration in bars (for the S&B time budget)
    setup_confirmed_t: float = 0.0   # when the W2 pivot became knowable (lag metric)


def wave3_signal(bars, *, pct: float = 0.02, retr_lo: float = 0.382,
                 retr_hi: float = 0.786, min_w1_frac: float = 0.01,
                 buf: float = 0.001, use_momentum: bool = True):
    """Return a Wave3Signal iff the CURRENT (last) candle confirms a wave-3 entry
    (price just broke the wave-1 extreme out of a valid wave-1/wave-2 structure),
    else None. Causal."""
    if len(bars) < 50:
        return None
    piv = [p for p in zigzag_causal(bars, pct=pct) if p.confirmed_t is not None]
    if len(piv) < 3:
        return None
    a, b, c = piv[-3], piv[-2], piv[-1]          # a->b = wave 1, b->c = wave 2
    price = bars[-1][4]
    prev = bars[-2][4]
    t_now = bars[-1][0]
    w1_up = b.price > a.price
    w1_len = abs(b.price - a.price)
    if w1_len <= 0 or w1_len / max(a.price, 1e-9) < min_w1_frac:
        return None
    mom = momentum_lookup(bars) if use_momentum else None
    e = mom(t_now) if mom else None

    # ---- LONG: wave 1 up, wave 2 down (pullback), break ABOVE wave-1 high ----
    if w1_up and c.price < b.price:
        retr = (b.price - c.price) / w1_len
        if not (retr_lo <= retr <= retr_hi):
            return None
        if c.price <= a.price:                   # R1: wave 2 cannot exceed wave-1 origin
            return None
        w1_high, w2_low = b.price, c.price
        if not (prev <= w1_high < price):        # confirmation break happened THIS candle
            return None
        if use_momentum and (e is None or e <= 0):   # momentum must be expanding up
            return None
        entry, stop = w1_high, w2_low * (1 - buf)
        risk = entry - stop
        if risk <= 0:
            return None
        t1, t2 = w2_low + 1.618 * w1_len, w2_low + 2.618 * w1_len
        return Wave3Signal("long", t_now, round(entry, 4), round(stop, 4),
                           [("1.618x W1", round(t1, 2)), ("2.618x W1", round(t2, 2))],
                           round((t1 - entry) / risk, 2), (a.price, b.price), w2_low,
                           round(retr, 3), e if e is not None else 0.0,
                           "wave-3 long: broke wave-1 high after a valid wave-2 pullback",
                           setup_confirmed_t=c.confirmed_t or 0.0)

    # ---- SHORT: wave 1 down, wave 2 up, break BELOW wave-1 low ----
    if (not w1_up) and c.price > b.price:
        retr = (c.price - b.price) / w1_len
        if not (retr_lo <= retr <= retr_hi):
            return None
        if c.price >= a.price:
            return None
        w1_low, w2_high = b.price, c.price
        if not (prev >= w1_low > price):
            return None
        if use_momentum and (e is None or e >= 0):
            return None
        entry, stop = w1_low, w2_high * (1 + buf)
        risk = stop - entry
        if risk <= 0:
            return None
        t1, t2 = w2_high - 1.618 * w1_len, w2_high - 2.618 * w1_len
        return Wave3Signal("short", t_now, round(entry, 4), round(stop, 4),
                           [("1.618x W1", round(t1, 2)), ("2.618x W1", round(t2, 2))],
                           round((entry - t1) / risk, 2), (a.price, b.price), w2_high,
                           round(retr, 3), e if e is not None else 0.0,
                           "wave-3 short: broke wave-1 low after a valid wave-2 pullback",
                           setup_confirmed_t=c.confirmed_t or 0.0)
    return None


# --------------------------------------------------------------------------- #
# RULE-FAITHFUL wave-3 entry (docs/RULESET.md §H). Adds the documented pieces the
# crude signal skipped: PATTERN IDENTIFICATION (W1 must carry a NeoWave :5 motive
# structure label — doc 02 §2.1), the CONFLUENCE GATE (>=N independent strands via
# score_reversal — doc 04 Table D: a label alone never trades), the R:R gate
# (>=2:1 — E-2), and the E-10 entry-trigger time window (the break must fire within
# ~the wave-2 duration). Long-only first; short mirrors.
# --------------------------------------------------------------------------- #
_MOTIVE_LABELS = (":5", ":L5", ":s5")
_CORR_LABELS = (":3", ":c3", ":sL3", ":F3", ":L3")


def wave3_signal_strict(bars, *, conf_min: int = 3, min_rr: float = 2.0,
                        retr_lo: float = 0.382, retr_hi: float = 0.618,
                        deep_hi: float = 0.764, pct: float = 0.02,
                        buf: float = 0.001, use_momentum: bool = True,
                        require_pattern_id: bool = True,
                        entry_window_w2_mult: int = 2,
                        min_w1_frac: float = 0.01,
                        use_ichimoku: bool = False):
    """Rule-faithful wave-3 long entry, or None. Reuses the documented rule
    components (NeoWave structure label, score_reversal confluence, Fib targets,
    S&B time). Causal."""
    if len(bars) < 60:
        return None
    from ..rules import label_monowaves
    from .confluence import score_reversal
    piv = [p for p in zigzag_causal(bars, pct=pct) if p.confirmed_t is not None]
    if len(piv) < 4:
        return None
    a, b, c = piv[-3], piv[-2], piv[-1]                  # a->b = W1, b->c = W2
    price, prev, t_now = bars[-1][4], bars[-2][4], bars[-1][0]
    if not (b.price > a.price and c.price < b.price):    # long setup only (mirror later)
        return None
    w1_len = b.price - a.price
    if w1_len <= 0 or w1_len / max(a.price, 1e-9) < min_w1_frac:
        return None
    # --- PATTERN ID: W1 (wave a->b) must carry a NeoWave :5-family MOTIVE label ---
    w1_label = ":?"
    if require_pattern_id:
        lab = label_monowaves(piv)                       # [(Wave, label), ...]
        if len(lab) < 2:
            return None
        w1_label = lab[-2][1]                             # label of the a->b wave
        if not any(w1_label.startswith(m) for m in _MOTIVE_LABELS):
            return None
    # --- W2 corrective: golden zone (.382-.618), deep allowed to .764; holds R1 ---
    retr = (b.price - c.price) / w1_len
    if not (retr_lo <= retr <= deep_hi) or c.price <= a.price:
        return None
    w1_high, w2_low = b.price, c.price
    # --- E-10 entry-trigger window: the break must fire within ~ W2's duration ---
    if entry_window_w2_mult:
        w2_bars = sum(1 for x in bars if b.t <= x[0] <= c.t)
        if sum(1 for x in bars if x[0] > c.t) > entry_window_w2_mult * max(w2_bars, 1):
            return None
    # --- CONFIRMATION: break + close above W1 high on THIS candle ---
    if not (prev <= w1_high < price):
        return None
    e = momentum_lookup(bars)(t_now) if use_momentum else 0.0
    if use_momentum and (e is None or e <= 0):           # momentum expanding (W3 personality)
        return None
    # --- CONFLUENCE GATE (Table D): >= conf_min independent strands ---
    rep = score_reversal("w3", bars[-250:], (w2_low, w1_high), bullish=True,
                         use_ichimoku=use_ichimoku)
    if rep.score < conf_min:
        return None
    entry, stop = w1_high, w2_low * (1 - buf)
    risk = entry - stop
    if risk <= 0:
        return None
    t1, t2 = w2_low + 1.618 * w1_len, w2_low + 2.618 * w1_len
    rr = (t1 - entry) / risk
    if rr < min_rr:                                       # E-2 minimum reward:risk
        return None
    w1_bars = sum(1 for x in bars if a.t <= x[0] <= b.t)
    return Wave3Signal("long", t_now, round(entry, 4), round(stop, 4),
                       [("1.618x W1", round(t1, 2)), ("2.618x W1", round(t2, 2))],
                       round(rr, 2), (a.price, b.price), w2_low, round(retr, 3),
                       e if e is not None else 0.0,
                       f"rule-faithful W3: W1={w1_label.split('(')[0]} motive, "
                       f"W2 {retr:.0%} retrace, confluence {rep.score}/7 strands, R:R {rr:.1f}",
                       strands=rep.score, t2=round(t2, 2), w1_bars=w1_bars,
                       setup_confirmed_t=c.confirmed_t or 0.0)


# --------------------------------------------------------------------------- #
# Profile-driven entry point (docs/ARCHITECTURE.md D6): one generator, the
# crude<->strict spread expressed entirely as configs/profiles.json knobs. The
# 'experimental' profile routes to the exact crude function (+0.17..+0.44R,
# docs/WAVE3_RESULT.md); gated profiles route to the rule-faithful strict
# function with the profile's knobs — preset equivalence by construction.
# --------------------------------------------------------------------------- #
def generate(bars, profile, symbol: str = "", timeframe: str = ""):
    """Run the wave-3 confirmation entry under `profile` (rules.profiles.Profile)
    on the CURRENT (last) candle. Returns [Signal] (0 or 1); causal."""
    from .models import from_wave3
    kw = profile.wave3_kwargs()
    gated = (kw["require_pattern_id"] or kw["conf_min"] > 0 or kw["min_rr"] > 0
             or kw["entry_window_w2_mult"] > 0)
    if gated:
        sig = wave3_signal_strict(
            bars, conf_min=kw["conf_min"], min_rr=kw["min_rr"],
            retr_lo=kw["retr_lo"], retr_hi=kw["retr_hi"],
            deep_hi=kw["deep_hi"] if kw["deep_hi"] is not None else kw["retr_hi"],
            pct=kw["pct"], buf=kw["buf"], use_momentum=kw["use_momentum"],
            require_pattern_id=kw["require_pattern_id"],
            entry_window_w2_mult=kw["entry_window_w2_mult"],
            min_w1_frac=kw["min_w1_frac"],
            use_ichimoku=kw.get("use_ichimoku", False))
    else:
        sig = wave3_signal(
            bars, pct=kw["pct"], retr_lo=kw["retr_lo"], retr_hi=kw["retr_hi"],
            min_w1_frac=kw["min_w1_frac"], buf=kw["buf"],
            use_momentum=kw["use_momentum"])
    if sig is None:
        return []
    return [from_wave3(sig, profile=profile, symbol=symbol, timeframe=timeframe)]
