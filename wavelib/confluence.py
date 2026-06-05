"""
confluence_score.py
===================
Reversal-confidence scoring that sits ON TOP of the Elliott/NeoWave engine.

Core idea: a wave label tells you where a reversal is *allowed*; it does NOT
tell you one is *happening*. Confirmation requires INDEPENDENT evidence that
fails separately. This module computes each strand and returns a stacked score.

Strands (each +1 if confirming a reversal at the tested swing):
  1. Fib/structure zone        — is price in a projected reversal zone?
  2. Momentum divergence       — price new extreme, RSI does not (RSI14)
  3. MACD turn                 — histogram flips toward the reversal
  4. Volume signature          — capitulation spike at the extreme
  5. Channel break             — break of the counter-trend (decline/advance) channel
  6. CHoCH (structure)         — first higher-high (up) / lower-low (down) vs the swing
  7. (external) cycle window   — caller supplies Hurst/FLD timing (+1) if aligned

Bars are (t,o,h,l,c,v). Pure stdlib.
"""
from __future__ import annotations
from dataclasses import dataclass, field


# --------------------------------------------------------------------------- #
# indicators
# --------------------------------------------------------------------------- #
def rsi(closes, n=14):
    if len(closes) <= n:
        return [None] * len(closes)
    g = [max(closes[i] - closes[i-1], 0) for i in range(1, len(closes))]
    l = [max(closes[i-1] - closes[i], 0) for i in range(1, len(closes))]
    ag, al = sum(g[:n]) / n, sum(l[:n]) / n
    out = [None] * n
    for i in range(n, len(g) + 1):
        if i > n:
            ag = (ag * (n-1) + g[i-1]) / n
            al = (al * (n-1) + l[i-1]) / n
        out.append(100 - 100 / (1 + (ag / al if al else 999)))
    return out


def ema(vals, n):
    k = 2 / (n + 1)
    out, e = [], vals[0]
    for v in vals:
        e = v * k + e * (1 - k)
        out.append(e)
    return out


def macd(closes, fast=12, slow=26, sig=9):
    ef, es = ema(closes, fast), ema(closes, slow)
    line = [a - b for a, b in zip(ef, es)]
    signal = ema(line, sig)
    hist = [a - b for a, b in zip(line, signal)]
    return line, signal, hist


# --------------------------------------------------------------------------- #
# strands
# --------------------------------------------------------------------------- #
@dataclass
class Strand:
    name: str
    confirm: bool
    detail: str


def in_zone(price, zone) -> Strand:
    lo, hi = zone
    c = lo <= price <= hi
    return Strand("Fib/structure zone", c,
                  f"price {price:.1f} {'INSIDE' if c else 'outside'} {lo:.0f}-{hi:.0f}")


def momentum_divergence(lows, closes, lookback=10, bullish=True) -> Strand:
    """Bullish: price lower-low but RSI higher-low (or vice-versa)."""
    r = rsi(closes)
    seg_lo = lows[-lookback:]
    seg_r = r[-lookback:]
    if any(x is None for x in seg_r):
        return Strand("Momentum divergence", False, "insufficient RSI history")
    i_now = len(seg_lo) - 1
    i_prev = seg_lo.index(min(seg_lo[:-1])) if len(seg_lo) > 1 else 0
    if bullish:
        price_ll = seg_lo[i_now] <= seg_lo[i_prev]
        rsi_hl = seg_r[i_now] > seg_r[i_prev]
        c = price_ll and rsi_hl
    else:
        price_hh = seg_lo[i_now] >= seg_lo[i_prev]
        rsi_lh = seg_r[i_now] < seg_r[i_prev]
        c = price_hh and rsi_lh
    return Strand("Momentum divergence", c,
                  f"RSI now {seg_r[i_now]:.0f} vs prior {seg_r[i_prev]:.0f} "
                  f"({'bullish div ✓' if c else 'none'})")


def macd_turn(closes, bullish=True) -> Strand:
    _, _, h = macd(closes)
    if len(h) < 3:
        return Strand("MACD turn", False, "insufficient history")
    turning = (h[-1] > h[-2] > h[-3]) if bullish else (h[-1] < h[-2] < h[-3])
    return Strand("MACD turn", turning,
                  f"hist {h[-3]:.2f}->{h[-2]:.2f}->{h[-1]:.2f} "
                  f"({'turning up' if turning and bullish else 'turning dn' if turning else 'flat/against'})")


def volume_capitulation(vols, mult=1.8) -> Strand:
    if len(vols) < 10:
        return Strand("Volume capitulation", False, "insufficient history")
    avg = sum(vols[-10:-1]) / 9
    spike = vols[-1] > avg * mult or max(vols[-3:]) > avg * mult
    return Strand("Volume capitulation", spike,
                  f"recent peak {max(vols[-3:])/1e6:.1f}M vs avg {avg/1e6:.1f}M "
                  f"({'spike ✓' if spike else 'no climax'})")


def choch(highs, lows, bullish=True, lookback=8) -> Strand:
    """Change of character: first higher-high (up) after lower-highs."""
    h = highs[-lookback:]
    if bullish:
        # has the latest bar taken out the prior swing high?
        recent_high = max(h[:-1])
        c = h[-1] > recent_high
        return Strand("CHoCH (higher-high)", c,
                      f"last high {h[-1]:.1f} vs prior swing {recent_high:.1f} "
                      f"({'broke up ✓' if c else 'no higher-high yet'})")
    else:
        l = lows[-lookback:]
        recent_low = min(l[:-1])
        c = l[-1] < recent_low
        return Strand("CHoCH (lower-low)", c,
                      f"last low {l[-1]:.1f} vs prior {recent_low:.1f}")


def channel_break(closes, decline=True) -> Strand:
    """Crude: is the latest close back above the short-term EMA of the down-move?"""
    e = ema(closes, 9)
    c = closes[-1] > e[-1] if decline else closes[-1] < e[-1]
    return Strand("Counter-trend channel break", c,
                  f"close {closes[-1]:.1f} vs EMA9 {e[-1]:.1f} "
                  f"({'reclaimed ✓' if c else 'still below'})")


# --------------------------------------------------------------------------- #
# swing classifier (impulse 5 vs corrective 3) — the piece promised earlier
# --------------------------------------------------------------------------- #
def classify_swing_sequence(pivot_prices) -> str:
    """
    Given alternating swing pivots of a move, guess impulsive (5) vs corrective (3).
    Heuristic: 5 clean alternating legs trending = impulse; 3 legs = correction;
    checks whether the last leg made a new extreme (impulse) or held (correction).
    """
    n = len(pivot_prices) - 1  # number of legs
    if n <= 3:
        return f"{n} legs -> CORRECTIVE (A-B-C / 3-wave) — bounce/continuation likely"
    if n == 5:
        return "5 legs -> IMPULSIVE (motive) — trend move, expect follow-through"
    return f"{n} legs -> complex/extended — needs sub-degree resolution"


# --------------------------------------------------------------------------- #
# aggregator
# --------------------------------------------------------------------------- #
@dataclass
class ConfluenceReport:
    symbol: str
    price: float
    strands: list = field(default_factory=list)
    cycle_aligned: bool = False

    @property
    def score(self):
        return sum(1 for s in self.strands if s.confirm) + (1 if self.cycle_aligned else 0)

    @property
    def max_score(self):
        return len(self.strands) + 1

    def __str__(self):
        head = f"\n=== {self.symbol} @ {self.price:.2f} — REVERSAL CONFLUENCE ===\n"
        body = "\n".join(f"  [{'✓' if s.confirm else ' '}] {s.name}: {s.detail}" for s in self.strands)
        cyc = f"\n  [{'✓' if self.cycle_aligned else ' '}] Hurst/FLD cycle window (external input)"
        verdict = (f"\n  SCORE {self.score}/{self.max_score} -> "
                   + ("HIGH-CONFIDENCE reversal" if self.score >= 4
                      else "BUILDING — not yet confirmed" if self.score >= 2
                      else "STRUCTURALLY ALLOWED ONLY (do not trust the label alone)"))
        return head + body + cyc + verdict


def score_reversal(symbol, bars, zone, bullish=True, cycle_aligned=False) -> ConfluenceReport:
    closes = [b[4] for b in bars]
    highs = [b[2] for b in bars]
    lows = [b[3] for b in bars]
    vols = [b[5] for b in bars]
    rep = ConfluenceReport(symbol, closes[-1], cycle_aligned=cycle_aligned)
    rep.strands = [
        in_zone(closes[-1], zone),
        momentum_divergence(lows, closes, bullish=bullish),
        macd_turn(closes, bullish=bullish),
        volume_capitulation(vols),
        channel_break(closes, decline=bullish),
        choch(highs, lows, bullish=bullish),
    ]
    return rep


if __name__ == "__main__":
    print("Demo: run score_reversal(symbol, bars, zone) on live OHLCV+volume.")
