"""
features.indicators — the ONE shared copy of the causal indicators
(rsi/ema/macd moved verbatim from wavelib/confluence.py; sma/atr from the
ghost-forward kit). Every value at index i uses data[0..i] only.
"""
from __future__ import annotations


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


def sma(vals, n):
    """Simple moving average of the trailing n values (last value)."""
    return sum(vals[-n:]) / min(len(vals), n) if vals else 0.0


def atr(bars, n=14):
    """Average true range over the last n bars of (t,o,h,l,c[,v]) tuples."""
    if len(bars) < 2:
        return 0.0
    trs = []
    for i in range(1, len(bars)):
        h, l, pc = bars[i][2], bars[i][3], bars[i - 1][4]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    return sum(trs[-n:]) / min(len(trs), n)


def ichimoku(bars, tenkan_n=9, kijun_n=26, senkou_b_n=52, displacement=26):
    """Ichimoku Cloud (SOW: 'NeoWave with Ichimoku Cloud' — the method's
    confirmation overlay; RULESET §I scope + audit G6).

    Returns a dict of lists aligned to `bars` (None until enough history):
      tenkan, kijun            — conversion/base lines at each bar
      senkou_a, senkou_b       — the CLOUD AT bar i (i.e. the spans computed
                                 `displacement` bars EARLIER and projected
                                 forward onto i). CAUSAL by construction: the
                                 cloud overhead at bar i uses data up to
                                 i - displacement only.
    Chikou (the lagging close plot) is deliberately NOT returned: it plots the
    close BACKWARD in time and cannot inform a causal decision at bar i.
    bars = (t,o,h,l,c[,v]) tuples.
    """
    n = len(bars)
    highs = [b[2] for b in bars]
    lows = [b[3] for b in bars]

    def mid(period, i):
        if i + 1 < period:
            return None
        return (max(highs[i + 1 - period:i + 1]) + min(lows[i + 1 - period:i + 1])) / 2

    tenkan = [mid(tenkan_n, i) for i in range(n)]
    kijun = [mid(kijun_n, i) for i in range(n)]
    senkou_a = [None] * n
    senkou_b = [None] * n
    for i in range(n):
        j = i - displacement                      # span computed j, seen at i
        if j >= 0 and tenkan[j] is not None and kijun[j] is not None:
            senkou_a[i] = (tenkan[j] + kijun[j]) / 2
        sb = mid(senkou_b_n, j) if j >= 0 else None
        senkou_b[i] = sb
    return {"tenkan": tenkan, "kijun": kijun,
            "senkou_a": senkou_a, "senkou_b": senkou_b}
