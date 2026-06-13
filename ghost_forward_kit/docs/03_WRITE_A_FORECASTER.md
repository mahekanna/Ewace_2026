# 03 — Write a forecaster

A forecaster is one function:
```python
def forecast(bars) -> Forecast | None
```
- `bars` is a list of `(t, o, h, l, c, v)` tuples, **oldest → newest**, ending at "now".
  The harness hands you the most recent `--roll` bars at each step.
- Return a **`Forecast`** (or an equivalent dict), or **`None`** when you have no clean read.
- **Be causal.** Use only `bars`. Never read ahead, never use a global "latest price",
  never fit parameters on the whole series. The harness guarantees `bars` stops at the
  decision candle — keep it that way.

## The Forecast object
```python
from gf import Forecast
Forecast(
    direction,      # "up" | "down"  — which way you expect the NEXT move
    target,         # price you expect it to reach (the reward side)
    invalidation,   # price that proves you wrong (the risk side / stop)
    confidence=0.5, # 0..1, optional — only used by the diagnostic buckets
    kind="",        # optional label to group calls in the diagnostic (e.g. "wave-3")
)
```
For `direction="up"` the harness expects `invalidation < price < target`; for `"down"`,
`target < price < invalidation`. If that ordering is wrong at decision time the call is
marked **STALE** (unusable) — see `05_METHODOLOGY.md`.

You may also return a plain dict (zero kit dependency), handy when your model lives in
another package:
```python
return {"direction": "up", "target": 105.0, "invalidation": 98.0,
        "confidence": 0.6, "kind": "breakout"}
```

## Worked example (the bundled baseline)
`forecasters/example_naive.py` — SMA-momentum with ATR-sized target/stop:
```python
from gf import Forecast, sma, atr
FAST, SLOW, LOOKBACK = 10, 40, 60

def forecast(bars):
    if len(bars) < max(SLOW, LOOKBACK):
        return None
    closes = [b[4] for b in bars]
    price = closes[-1]
    a = atr(bars, 14) or price * 0.01
    fast, slow = sma(closes, FAST), sma(closes, SLOW)
    conf = max(0.0, min(1.0, abs(fast - slow) / a)) if a else 0.5
    if fast >= slow:
        return Forecast("up", price + 1.5 * a, price - 1.0 * a, confidence=conf, kind="sma-momo")
    return Forecast("down", price - 1.5 * a, price + 1.0 * a, confidence=conf, kind="sma-momo")
```
Expect it to score ~50% next-candle. A baseline that *isn't* better than this is the
signal you want to catch.

## Adapting an existing engine
If you already have a model, wrap it — don't rewrite it. See
`forecasters/wavelib_adapter.py`, which maps this repo's Elliott/NeoWave
`forecast_waves()` output onto `Forecast` in ~5 lines. The pattern:
```python
def forecast(bars):
    out = my_model.predict(bars)            # your call, on the given bars only
    if out is None:
        return None
    return Forecast(direction=out.dir, target=out.tgt, invalidation=out.stop,
                    confidence=out.conf, kind=out.label)
```

## `kind` and `confidence` are your microscope
- Set **`kind`** to the setup type (e.g. `"wave-3"`, `"breakout"`, `"mean-revert"`). The
  diagnostic reports accuracy per kind — that's how you find which setups carry the edge.
- Set **`confidence`** honestly. The diagnostic checks whether high-confidence calls are
  actually better; if they're not, your confidence is noise (a real, common finding).

Next: **`04_RUN_GHOST_TEST.md`**.
