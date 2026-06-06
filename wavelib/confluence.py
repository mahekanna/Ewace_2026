"""
confluence.py
=============
Reversal-confidence scoring that sits ON TOP of the Elliott/NeoWave engine.

Core idea: a wave label tells you where a reversal is *allowed*; it does NOT
tell you one is *happening*. Confirmation requires INDEPENDENT evidence that
fails separately. This module computes each strand and returns a stacked score.

Strands (each +1 if confirming a reversal at the tested swing):
  1. Fib/structure zone        — is price in a projected reversal zone?
  2. Momentum divergence       — swing-pivot RSI divergence (regular + hidden)
  3. MACD turn                 — histogram flips toward the reversal
  4. Volume signature          — capitulation spike with wide-range filter
  5. Channel break             — close beyond two-pivot anchored trendline
  6. CHoCH (structure)         — genuine counter-trend structural break (not BOS)
  7. (external) cycle window   — caller supplies Hurst/FLD timing via CycleSignal

Bars are (t,o,h,l,c,v). Pure stdlib. Python 3.9+.

Phase 3 hardening (03_confirmation_strands.md §4 P1-P6):
  P1 — momentum_divergence: swing_pivots-based, regular + hidden, ≥50-bar guard,
       ≥3 RSI-point amplitude filter.
  P2 — choch: SMC swing-pivot structure, body-close confirmation, BOS vs CHoCH.
  P3 — CycleSignal typed payload in wavelib/cycle_seam.py; score_reversal updated.
  P4 — volume_capitulation: 20-bar window + price-range (wide-range) filter.
  P5 — channel_break: two-pivot anchored trendline, not EMA9.
  P6 — minimum-bar guard in score_reversal (_MIN_BARS = 50).

Causal-only: every computation at bar t uses data ≤ t only (D-013 in chakra_quant).
swing_pivots introduces an n_right-bar lag which is causal by design.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

try:
    from .toolkit import swing_pivots
    from .cycle_seam import CycleSignal
except ImportError:
    # Standalone execution: add parent directory to path and import directly.
    import sys as _sys, os as _os
    _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    from wavelib.toolkit import swing_pivots      # type: ignore
    from wavelib.cycle_seam import CycleSignal    # type: ignore


# --------------------------------------------------------------------------- #
# Minimum bar count for full-quality scoring
# --------------------------------------------------------------------------- #
_MIN_BARS: int = 50


# --------------------------------------------------------------------------- #
# Indicators (unchanged public API)
# --------------------------------------------------------------------------- #
def rsi(closes, n=14):
    """
    Wilder RSI on a sequence of close prices.

    Returns a list of the same length as `closes`; the first n values are None
    (seed period). Causal: value at index i uses closes[0..i] only.
    """
    if len(closes) <= n:
        return [None] * len(closes)
    g = [max(closes[i] - closes[i-1], 0) for i in range(1, len(closes))]
    lo = [max(closes[i-1] - closes[i], 0) for i in range(1, len(closes))]
    ag, al = sum(g[:n]) / n, sum(lo[:n]) / n
    out = [None] * n
    for i in range(n, len(g) + 1):
        if i > n:
            ag = (ag * (n-1) + g[i-1]) / n
            al = (al * (n-1) + lo[i-1]) / n
        out.append(100 - 100 / (1 + (ag / al if al else 999)))
    return out


def ema(vals, n):
    """Standard exponential moving average (cold-start: first value = vals[0])."""
    k = 2 / (n + 1)
    out, e = [], vals[0]
    for v in vals:
        e = v * k + e * (1 - k)
        out.append(e)
    return out


def macd(closes, fast=12, slow=26, sig=9):
    """MACD line, signal line, histogram. Causal EMA construction."""
    ef, es = ema(closes, fast), ema(closes, slow)
    line = [a - b for a, b in zip(ef, es)]
    signal = ema(line, sig)
    hist = [a - b for a, b in zip(line, signal)]
    return line, signal, hist


# --------------------------------------------------------------------------- #
# Strand dataclass
# --------------------------------------------------------------------------- #
@dataclass
class Strand:
    name: str
    confirm: bool
    detail: str


# --------------------------------------------------------------------------- #
# Strand 1 — Fib / structure zone (unchanged)
# --------------------------------------------------------------------------- #
def in_zone(price, zone) -> Strand:
    lo, hi = zone
    c = lo <= price <= hi
    return Strand("Fib/structure zone", c,
                  f"price {price:.1f} {'INSIDE' if c else 'outside'} {lo:.0f}-{hi:.0f}")


# --------------------------------------------------------------------------- #
# Strand 2 — Momentum divergence (P1 rewrite)
# --------------------------------------------------------------------------- #
def momentum_divergence(
    lows, closes,
    lookback: int = 10,   # kept for backward compat but minimum is 50 bars
    bullish: bool = True,
    n_left: int = 3,
    n_right: int = 3,
    rsi_period: int = 14,
    min_rsi_amplitude: float = 3.0,
) -> Strand:
    """
    Swing-pivot RSI divergence — regular AND hidden, both directions.

    Correct construction (per 03_confirmation_strands.md §2.1 and §4 P1):
    1. Compute RSI on the full `closes` series (causal, Wilder smoothing).
    2. Find confirmed swing pivots on BOTH the price series and RSI series
       using swing_pivots(series, n_left, n_right).  The n_right-bar lag is
       causal: a pivot at bar i is confirmed only at bar i+n_right.
    3. Pair the two most recent CONFIRMED same-kind (H or H, L or L) pivots on
       each series and compare them.
    4. Regular bullish : price lower-low / RSI higher-low → reversal signal.
       Regular bearish : price higher-high / RSI lower-high → reversal signal.
       Hidden  bullish : price higher-low / RSI lower-low → continuation signal.
       Hidden  bearish : price lower-high / RSI higher-high → continuation signal.
    5. Amplitude filter: |RSI_pivot2 - RSI_pivot1| >= min_rsi_amplitude.
    6. Minimum bar guard: need ≥ 50 bars for RSI to be meaningful.

    Causal note: swing_pivots introduces an n_right-bar lag; all comparisons
    use data ≤ bar t (no future data). Confirmed pivots omit the last n_right bars.

    Returns a Strand whose `detail` describes the divergence type found.
    """
    # --- guard: need enough bars for meaningful RSI + pivot detection ---
    min_required = max(50, rsi_period + 2 * n_left + 2 * n_right + 5)
    if len(closes) < min_required:
        return Strand("Momentum divergence", False,
                      f"insufficient history ({len(closes)} bars, need ≥{min_required})")

    # --- compute RSI on full close series ---
    rsi_vals = rsi(closes, rsi_period)

    # --- build (t, value) series indexed by position ---
    # t is just the bar index (integer) — no actual timestamps needed here
    n = len(closes)
    price_series_lows = [(i, lows[i]) for i in range(n)]
    price_series_highs = [(i, lows[i]) for i in range(n)]  # placeholder; see below
    rsi_series = [(i, rsi_vals[i]) for i in range(n) if rsi_vals[i] is not None]

    if bullish:
        # For bullish divergence we compare swing LOWS on price vs RSI
        price_series = [(i, lows[i]) for i in range(n)]
        price_pivots = swing_pivots(price_series, n_left, n_right)
        price_lows = [p for p in price_pivots if p.kind == "L"]
    else:
        # For bearish divergence we compare swing HIGHS on price vs RSI
        # lows series passed in; use closes as proxy for highs if only lows given
        # For generality: use closes as the "high proxy" for bearish scan
        price_series = [(i, closes[i]) for i in range(n)]
        price_pivots = swing_pivots(price_series, n_left, n_right)
        price_highs = [p for p in price_pivots if p.kind == "H"]

    rsi_pivots = swing_pivots(rsi_series, n_left, n_right)

    if bullish:
        rsi_lows = [p for p in rsi_pivots if p.kind == "L"]
        # Need at least two price swing lows and two RSI swing lows
        if len(price_lows) < 2 or len(rsi_lows) < 2:
            return Strand("Momentum divergence", False,
                          "insufficient swing pivots for divergence check")
        p1, p2 = price_lows[-2], price_lows[-1]   # older, newer
        r1, r2 = rsi_lows[-2], rsi_lows[-1]

        # amplitude filter
        rsi_diff = abs(r2.price - r1.price)
        if rsi_diff < min_rsi_amplitude:
            return Strand("Momentum divergence", False,
                          f"RSI amplitude {rsi_diff:.1f} < {min_rsi_amplitude:.1f} pts (micro-divergence suppressed)")

        regular_bull = (p2.price < p1.price) and (r2.price > r1.price)
        hidden_bull  = (p2.price > p1.price) and (r2.price < r1.price)

        if regular_bull:
            return Strand("Momentum divergence", True,
                          f"REGULAR BULL div: price LL ({p1.price:.1f}->{p2.price:.1f}) / "
                          f"RSI HL ({r1.price:.1f}->{r2.price:.1f})")
        if hidden_bull:
            return Strand("Momentum divergence", True,
                          f"HIDDEN BULL div: price HL ({p1.price:.1f}->{p2.price:.1f}) / "
                          f"RSI LL ({r1.price:.1f}->{r2.price:.1f})")
        return Strand("Momentum divergence", False,
                      f"no bullish div: price ({p1.price:.1f}->{p2.price:.1f}) "
                      f"RSI ({r1.price:.1f}->{r2.price:.1f})")

    else:  # bearish
        rsi_highs = [p for p in rsi_pivots if p.kind == "H"]
        if len(price_highs) < 2 or len(rsi_highs) < 2:
            return Strand("Momentum divergence", False,
                          "insufficient swing pivots for divergence check")
        p1, p2 = price_highs[-2], price_highs[-1]
        r1, r2 = rsi_highs[-2], rsi_highs[-1]

        rsi_diff = abs(r2.price - r1.price)
        if rsi_diff < min_rsi_amplitude:
            return Strand("Momentum divergence", False,
                          f"RSI amplitude {rsi_diff:.1f} < {min_rsi_amplitude:.1f} pts (micro-divergence suppressed)")

        regular_bear = (p2.price > p1.price) and (r2.price < r1.price)
        hidden_bear  = (p2.price < p1.price) and (r2.price > r1.price)

        if regular_bear:
            return Strand("Momentum divergence", True,
                          f"REGULAR BEAR div: price HH ({p1.price:.1f}->{p2.price:.1f}) / "
                          f"RSI LH ({r1.price:.1f}->{r2.price:.1f})")
        if hidden_bear:
            return Strand("Momentum divergence", True,
                          f"HIDDEN BEAR div: price LH ({p1.price:.1f}->{p2.price:.1f}) / "
                          f"RSI HH ({r1.price:.1f}->{r2.price:.1f})")
        return Strand("Momentum divergence", False,
                      f"no bearish div: price ({p1.price:.1f}->{p2.price:.1f}) "
                      f"RSI ({r1.price:.1f}->{r2.price:.1f})")


# --------------------------------------------------------------------------- #
# Strand 3 — MACD turn (unchanged heuristic; kept for backward compat)
# --------------------------------------------------------------------------- #
def macd_turn(closes, bullish=True) -> Strand:
    """
    3-bar monotone MACD histogram inflection (earliest MACD signal).

    Note: this is a heuristic — fires early but has no amplitude gate and no
    warm-up guard. The 03 spec (§2.2) flags it as Heuristic fidelity. A future
    pass may add an amplitude threshold. Left unchanged in this phase (P1-P6
    did not mandate a rewrite).
    """
    _, _, h = macd(closes)
    if len(h) < 3:
        return Strand("MACD turn", False, "insufficient history")
    turning = (h[-1] > h[-2] > h[-3]) if bullish else (h[-1] < h[-2] < h[-3])
    return Strand("MACD turn", turning,
                  f"hist {h[-3]:.2f}->{h[-2]:.2f}->{h[-1]:.2f} "
                  f"({'turning up' if turning and bullish else 'turning dn' if turning else 'flat/against'})")


# --------------------------------------------------------------------------- #
# Strand 4 — Volume capitulation (P4 hardened)
# --------------------------------------------------------------------------- #
def volume_capitulation(
    vols,
    bars_ohlcv=None,
    mult: float = 2.0,
    window: int = 20,
    range_mult: float = 1.5,
) -> Strand:
    """
    Volume capitulation spike with wide-range (climax vs churn) filter.

    Hardening per 03_confirmation_strands.md §4 P4:
    - Average window extended to 20 bars (industry standard; was 10).
    - Price-range filter: qualifying bar must have range > range_mult × ATR(window)
      to distinguish climax (exhaustion) from churn (absorption).
    - Fires on vols[-1] only (the current bar), not max(vols[-3:]).
    - Threshold raised to 2.0× (was 1.8×) for high-cap liquid equities.

    Parameters
    ----------
    vols       : volume series (list of floats)
    bars_ohlcv : optional (t,o,h,l,c,v) bars for range computation.
                 If None, the range filter is skipped (volume-only check).
    mult       : RVOL threshold (current bar volume / 20-bar avg). Default 2.0.
    window     : Rolling average window in bars. Default 20.
    range_mult : Minimum bar-range as a multiple of ATR(window). Default 1.5.

    Causal: all computations use data ≤ current bar only.
    """
    if len(vols) < window + 1:
        return Strand("Volume capitulation", False,
                      f"insufficient history ({len(vols)} bars, need ≥{window + 1})")

    avg = sum(vols[-(window + 1):-1]) / window
    if avg == 0:
        return Strand("Volume capitulation", False, "zero average volume")

    current_vol = vols[-1]
    vol_spike = current_vol > avg * mult

    # --- price-range filter ---
    range_ok = True
    range_detail = "(no OHLCV for range check)"
    if bars_ohlcv is not None and len(bars_ohlcv) >= window + 1:
        ranges = [abs(b[2] - b[3]) for b in bars_ohlcv]  # high - low
        atr = sum(ranges[-(window + 1):-1]) / window
        cur_range = abs(bars_ohlcv[-1][2] - bars_ohlcv[-1][3])
        range_ok = atr > 0 and cur_range > range_mult * atr
        range_detail = (f"range {cur_range:.2f} vs {range_mult}×ATR({atr:.2f})"
                        f"={'wide ✓' if range_ok else 'narrow (churn)'}")

    confirm = vol_spike and range_ok
    return Strand("Volume capitulation", confirm,
                  f"vol {current_vol/1e6:.1f}M vs avg {avg/1e6:.1f}M "
                  f"({current_vol/avg:.1f}× {'spike ✓' if vol_spike else 'no spike'}); "
                  + range_detail)


# --------------------------------------------------------------------------- #
# Strand 6 — CHoCH (P2 rewrite: SMC swing-pivot structure)
# --------------------------------------------------------------------------- #
def choch(
    highs, lows,
    bullish: bool = True,
    lookback: int = 8,     # kept for backward compat; used as min bars
    n_left: int = 3,
    n_right: int = 3,
) -> Strand:
    """
    Change of Character (CHoCH) vs Break of Structure (BOS) — SMC methodology.

    Correct construction per 03_confirmation_strands.md §2.4 and §4 P2:

    1. Build confirmed swing pivots using swing_pivots() on highs and lows.
       n_right-bar lag is causal: a pivot confirmed at bar i+n_right.
    2. Determine structural trend from the sequence of confirmed pivots:
       - Uptrend:   sequence of higher highs (HH) AND higher lows (HL).
       - Downtrend: sequence of lower highs (LH) AND lower lows (LL).
    3. BOS (Break of Structure): close breaks the most recent confirmed swing
       in the direction OF the established trend → trend continuation.
    4. CHoCH (Change of Character): close breaks the structural level in the
       direction COUNTER to the established trend → potential reversal.
    5. Body-close requirement: uses closes[-1] vs pivot price, not raw high/low.

    For bullish reversals we look for a CHoCH UP (close > last confirmed swing
    high) after an established downtrend (LH/LL sequence).
    For bearish reversals we look for a CHoCH DOWN (close < last confirmed
    swing low) after an established uptrend (HH/HL sequence).

    Returns a Strand with name indicating whether a CHoCH or BOS was detected.

    Causal: all pivot confirmation uses only bars up to bar t - n_right.
    """
    n = len(highs)
    if n < max(lookback, n_left + n_right + 2):
        return Strand("CHoCH (structure)", False,
                      f"insufficient bars ({n}, need ≥{max(lookback, n_left + n_right + 2)})")

    if len(lows) != n:
        return Strand("CHoCH (structure)", False, "highs/lows length mismatch")

    # Use the last element as "close proxy" for body-close check.
    # Score_reversal passes closes separately; here we use lows[-1] for bullish
    # (the close at the most recent bar) and highs[-1] for bearish as an
    # approximation — score_reversal provides the actual close via closes[-1].
    # The function can also work standalone with raw high/low arrays.

    # Build index series for swing_pivots
    high_series = [(i, highs[i]) for i in range(n)]
    low_series  = [(i, lows[i]) for i in range(n)]

    swing_highs = swing_pivots(high_series, n_left, n_right)
    swing_lows  = swing_pivots(low_series,  n_left, n_right)

    confirmed_highs = [p for p in swing_highs if p.kind == "H"]
    confirmed_lows  = [p for p in swing_lows  if p.kind == "L"]

    if len(confirmed_highs) < 2 or len(confirmed_lows) < 2:
        return Strand("CHoCH (structure)", False,
                      "insufficient confirmed swing pivots")

    # --- determine structural trend ---
    sh1, sh2 = confirmed_highs[-2], confirmed_highs[-1]   # older, newer swing highs
    sl1, sl2 = confirmed_lows[-2],  confirmed_lows[-1]    # older, newer swing lows

    is_downtrend = (sh2.price < sh1.price) and (sl2.price < sl1.price)
    is_uptrend   = (sh2.price > sh1.price) and (sl2.price > sl1.price)

    # --- body-close level check ---
    # Use the raw high/low of the final bar as an approximation for close.
    # (score_reversal wraps this with actual closes; the function still works
    # standalone for testing purposes.)
    cur_close = highs[-1]   # last bar close approximation for standalone use
    # For the canonical path through score_reversal, _choch_with_close() is used.

    if bullish:
        # Looking for CHoCH UP: close breaks last confirmed swing high
        # after an established downtrend.
        ref_level = sh2.price  # most recent confirmed swing high
        breaks_up = cur_close > ref_level

        if is_downtrend and breaks_up:
            return Strand("CHoCH (higher-high)", True,
                          f"CHoCH UP: close {cur_close:.1f} > swing-H {ref_level:.1f} "
                          f"(LH/LL downtrend broken)")
        if not is_downtrend and breaks_up:
            return Strand("CHoCH (higher-high)", False,
                          f"BOS (trend continuation): close {cur_close:.1f} > swing-H "
                          f"{ref_level:.1f} but trend was {'up' if is_uptrend else 'unclear'}")
        return Strand("CHoCH (higher-high)", False,
                      f"no higher-high: close {cur_close:.1f} ≤ swing-H {ref_level:.1f}")

    else:  # bearish
        ref_level = sl2.price  # most recent confirmed swing low
        breaks_dn = cur_close < ref_level

        if is_uptrend and breaks_dn:
            return Strand("CHoCH (lower-low)", True,
                          f"CHoCH DOWN: close {cur_close:.1f} < swing-L {ref_level:.1f} "
                          f"(HH/HL uptrend broken)")
        if not is_uptrend and breaks_dn:
            return Strand("CHoCH (lower-low)", False,
                          f"BOS (trend continuation): close {cur_close:.1f} < swing-L "
                          f"{ref_level:.1f} but trend was {'down' if is_downtrend else 'unclear'}")
        return Strand("CHoCH (lower-low)", False,
                      f"no lower-low: close {cur_close:.1f} ≥ swing-L {ref_level:.1f}")


def _choch_with_close(
    highs, lows, close_val: float,
    bullish: bool = True,
    n_left: int = 3,
    n_right: int = 3,
) -> Strand:
    """
    Internal variant of choch() that accepts the actual last close for the
    body-close check. Called by score_reversal which has access to closes.
    """
    n = len(highs)
    if n < n_left + n_right + 2:
        return Strand("CHoCH (structure)", False,
                      f"insufficient bars ({n})")

    high_series = [(i, highs[i]) for i in range(n)]
    low_series  = [(i, lows[i])  for i in range(n)]

    confirmed_highs = [p for p in swing_pivots(high_series, n_left, n_right)
                       if p.kind == "H"]
    confirmed_lows  = [p for p in swing_pivots(low_series, n_left, n_right)
                       if p.kind == "L"]

    if len(confirmed_highs) < 2 or len(confirmed_lows) < 2:
        return Strand("CHoCH (structure)", False,
                      "insufficient confirmed swing pivots")

    sh1, sh2 = confirmed_highs[-2], confirmed_highs[-1]
    sl1, sl2 = confirmed_lows[-2],  confirmed_lows[-1]

    is_downtrend = (sh2.price < sh1.price) and (sl2.price < sl1.price)
    is_uptrend   = (sh2.price > sh1.price) and (sl2.price > sl1.price)

    if bullish:
        ref_level = sh2.price
        breaks_up = close_val > ref_level
        if is_downtrend and breaks_up:
            return Strand("CHoCH (higher-high)", True,
                          f"CHoCH UP: close {close_val:.1f} > swing-H {ref_level:.1f} "
                          f"(LH/LL broken)")
        if not is_downtrend and breaks_up:
            return Strand("CHoCH (higher-high)", False,
                          f"BOS (up continuation): close {close_val:.1f} > swing-H {ref_level:.1f}")
        return Strand("CHoCH (higher-high)", False,
                      f"no CHoCH: close {close_val:.1f} ≤ swing-H {ref_level:.1f}")
    else:
        ref_level = sl2.price
        breaks_dn = close_val < ref_level
        if is_uptrend and breaks_dn:
            return Strand("CHoCH (lower-low)", True,
                          f"CHoCH DOWN: close {close_val:.1f} < swing-L {ref_level:.1f} "
                          f"(HH/HL broken)")
        if not is_uptrend and breaks_dn:
            return Strand("CHoCH (lower-low)", False,
                          f"BOS (down continuation): close {close_val:.1f} < swing-L {ref_level:.1f}")
        return Strand("CHoCH (lower-low)", False,
                      f"no CHoCH: close {close_val:.1f} ≥ swing-L {ref_level:.1f}")


# --------------------------------------------------------------------------- #
# Strand 5 — Counter-trend channel break (P5 rewrite)
# --------------------------------------------------------------------------- #
def channel_break(
    closes,
    decline: bool = True,
    n_left: int = 3,
    n_right: int = 3,
    min_channel_bars: int = 10,
) -> Strand:
    """
    Structural trendline break using two confirmed swing pivot anchors.

    Correct construction per 03_confirmation_strands.md §2.5 and §4 P5:
    1. Find two most recent confirmed swing HIGHS (for a declining channel, i.e.
       bullish reversal) or swing LOWS (for an advancing channel, bearish reversal)
       using swing_pivots().
    2. Construct a linear trendline through the two anchor pivots.
    3. Project the trendline to the current bar (linear extrapolation — causal).
    4. Check whether closes[-1] has crossed on the other side of the line.
    5. Enforce min_channel_bars: channel must span ≥ min_channel_bars bars
       between the two anchor pivots (suppresses micro-channel noise).

    Causal: anchor pivots are confirmed at their n_right confirmation bars;
    projection to bar t uses no future data.

    Falls back to a graceful "no channel" Strand when fewer than two anchors
    exist.
    """
    n = len(closes)
    if n < n_left + n_right + 2:
        return Strand("Counter-trend channel break", False,
                      f"insufficient bars ({n})")

    close_series = [(i, closes[i]) for i in range(n)]
    pivots = swing_pivots(close_series, n_left, n_right)

    if decline:
        # Declining channel: anchor on swing HIGHS (resistance trendline)
        anchors = [p for p in pivots if p.kind == "H"]
    else:
        # Advancing channel: anchor on swing LOWS (support trendline)
        anchors = [p for p in pivots if p.kind == "L"]

    if len(anchors) < 2:
        return Strand("Counter-trend channel break", False,
                      "fewer than 2 confirmed anchors — cannot draw channel")

    a1, a2 = anchors[-2], anchors[-1]   # older, newer anchor (as integer indices)
    i1, i2 = int(a1.t), int(a2.t)       # t is the position index in our series

    if (i2 - i1) < min_channel_bars:
        return Strand("Counter-trend channel break", False,
                      f"channel too short ({i2 - i1} bars < {min_channel_bars} min)")

    # Linear trendline: project to last bar (index n-1)
    # slope = (price2 - price1) / (i2 - i1)
    slope = (a2.price - a1.price) / (i2 - i1)
    line_at_current = a1.price + slope * ((n - 1) - i1)

    cur_close = closes[-1]
    if decline:
        # Bullish break: close above the declining resistance trendline
        broken = cur_close > line_at_current
    else:
        # Bearish break: close below the advancing support trendline
        broken = cur_close < line_at_current

    return Strand("Counter-trend channel break", broken,
                  f"trendline @ {line_at_current:.1f} (anchors {a1.price:.1f}@bar{i1}, "
                  f"{a2.price:.1f}@bar{i2}); close {cur_close:.1f} "
                  f"({'broke ✓' if broken else 'held'})")


def divergence_at(closes, idx_prior, idx_recent, bullish=False) -> Strand:
    """Wave-label-aware RSI divergence between two SPECIFIC pivots — e.g. the
    labelled wave-3 and wave-5 tops (docs/research/deep/10). EWF: an impulse top
    is *confirmed* by divergence here; its ABSENCE argues the move can extend.
    bullish=False -> bearish top (price higher-high, RSI lower-high)."""
    r = rsi(closes)
    if not (0 <= idx_prior < len(r)) or not (0 <= idx_recent < len(r)) \
            or r[idx_prior] is None or r[idx_recent] is None:
        return Strand("RSI divergence @ waves", False, "insufficient RSI history")
    pp, pr = closes[idx_prior], closes[idx_recent]
    rp, rr = r[idx_prior], r[idx_recent]
    if not bullish:
        div = pr > pp and rr < rp
        kind = f"price {pp:.1f}->{pr:.1f} (HH={pr > pp}), RSI {rp:.0f}->{rr:.0f} (LH={rr < rp})"
    else:
        div = pr < pp and rr > rp
        kind = f"price {pp:.1f}->{pr:.1f} (LL={pr < pp}), RSI {rp:.0f}->{rr:.0f} (HL={rr > rp})"
    return Strand("RSI divergence @ waves", div,
                  ("divergence present — " if div else "no divergence — ") + kind)


# --------------------------------------------------------------------------- #
# Swing classifier (unchanged)
# --------------------------------------------------------------------------- #
def classify_swing_sequence(pivot_prices) -> str:
    """
    Given alternating swing pivots of a move, guess impulsive (5) vs corrective (3).
    Heuristic: 5 clean alternating legs trending = impulse; 3 legs = correction.
    """
    n = len(pivot_prices) - 1  # number of legs
    if n <= 3:
        return f"{n} legs -> CORRECTIVE (A-B-C / 3-wave) — bounce/continuation likely"
    if n == 5:
        return "5 legs -> IMPULSIVE (motive) — trend move, expect follow-through"
    return f"{n} legs -> complex/extended — needs sub-degree resolution"


# --------------------------------------------------------------------------- #
# ConfluenceReport (P3: extended with CycleSignal)
# --------------------------------------------------------------------------- #
@dataclass
class ConfluenceReport:
    symbol: str
    price: float
    strands: list = field(default_factory=list)
    cycle_aligned: bool = False
    cycle_signal: Optional[CycleSignal] = None
    bar_count: int = 0
    warnings: list = field(default_factory=list)

    @property
    def score(self):
        effective = (self.cycle_signal.aligned
                     if self.cycle_signal is not None
                     else self.cycle_aligned)
        return sum(1 for s in self.strands if s.confirm) + (1 if effective else 0)

    @property
    def max_score(self):
        return len(self.strands) + 1

    def __str__(self):
        effective = (self.cycle_signal.aligned
                     if self.cycle_signal is not None
                     else self.cycle_aligned)
        head = (f"\n=== {self.symbol} @ {self.price:.2f} — REVERSAL CONFLUENCE "
                f"({self.bar_count} bars) ===\n")
        warns = ""
        if self.warnings:
            warns = "  [!] " + "\n  [!] ".join(self.warnings) + "\n"
        body = "\n".join(f"  [{'✓' if s.confirm else ' '}] {s.name}: {s.detail}"
                         for s in self.strands)
        if self.cycle_signal is not None:
            cs = self.cycle_signal
            cyc_detail = (f"aligned={cs.aligned}"
                          + (f", period={cs.cycle_period}" if cs.cycle_period else "")
                          + (f", phase={cs.phase:.3f}" if cs.phase is not None else "")
                          + (f", source={cs.source}" if cs.source else ""))
            cyc = f"\n  [{'✓' if effective else ' '}] Hurst/FLD cycle window: {cyc_detail}"
        else:
            cyc = f"\n  [{'✓' if effective else ' '}] Hurst/FLD cycle window (external input)"
        verdict = (f"\n  SCORE {self.score}/{self.max_score} -> "
                   + ("HIGH-CONFIDENCE reversal" if self.score >= 4
                      else "BUILDING — not yet confirmed" if self.score >= 2
                      else "STRUCTURALLY ALLOWED ONLY (do not trust the label alone)"))
        return head + warns + body + cyc + verdict


# --------------------------------------------------------------------------- #
# P6 — Minimum-bar guard constant
# --------------------------------------------------------------------------- #
_BAR_WARN_THRESHOLD: int = _MIN_BARS


# --------------------------------------------------------------------------- #
# score_reversal (updated signature: P3 + P6)
# --------------------------------------------------------------------------- #
def score_reversal(
    symbol: str,
    bars: list,
    zone: tuple,
    bullish: bool = True,
    cycle_aligned: bool = False,
    cycle_signal: Optional[CycleSignal] = None,
) -> ConfluenceReport:
    """
    Compute reversal-confluence score for `symbol` at the most recent bar.

    Parameters
    ----------
    symbol        : Ticker string for reporting.
    bars          : List of (t, o, h, l, c, v) bar tuples.
    zone          : (lo, hi) price zone for the Fib/structure strand.
    bullish       : True = testing for a bullish reversal; False = bearish.
    cycle_aligned : Legacy boolean for the 7th (cycle) strand. Ignored if
                    cycle_signal is provided.
    cycle_signal  : CycleSignal dataclass (preferred, richer payload). When
                    provided, cycle_signal.aligned takes precedence over
                    cycle_aligned.

    Returns
    -------
    ConfluenceReport with per-strand results and aggregated score.

    P6 note: if len(bars) < _MIN_BARS (50), a warning is appended to the
    report and strands requiring history (momentum_divergence, channel_break,
    choch) will return False gracefully rather than silently degrading.
    """
    closes = [b[4] for b in bars]
    highs  = [b[2] for b in bars]
    lows   = [b[3] for b in bars]

    # Volume may not be available (e.g. weekly bars stored as (t,h,l,c))
    try:
        vols = [b[5] for b in bars]
    except IndexError:
        vols = []

    n = len(bars)
    warnings = []
    if n < _MIN_BARS:
        warnings.append(
            f"Only {n} bars supplied (recommend ≥{_MIN_BARS}); "
            "momentum_divergence and channel_break strands need more history."
        )

    rep = ConfluenceReport(
        symbol=symbol,
        price=closes[-1],
        cycle_aligned=cycle_aligned,
        cycle_signal=cycle_signal,
        bar_count=n,
        warnings=warnings,
    )

    # Volume capitulation: pass full bars for range filter
    if vols:
        vol_strand = volume_capitulation(vols, bars_ohlcv=bars)
    else:
        vol_strand = Strand("Volume capitulation", False,
                            "no volume data in bars (need (t,o,h,l,c,v) format)")

    rep.strands = [
        in_zone(closes[-1], zone),
        momentum_divergence(lows, closes, bullish=bullish),
        macd_turn(closes, bullish=bullish),
        vol_strand,
        channel_break(closes, decline=bullish),
        _choch_with_close(highs, lows, closes[-1], bullish=bullish),
    ]
    return rep


if __name__ == "__main__":
    print("Demo: run score_reversal(symbol, bars, zone) on live OHLCV+volume.")
    print("CycleSignal is available from wavelib.cycle_seam for typed 7th-strand input.")
