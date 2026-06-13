# 05 — Methodology, outcome definitions, and pitfalls

## Why ghost feeding (vs a normal backtest)
A pooled backtest reports aggregate P&L and hides the **moment of decision**. Ghost feeding
reconstructs real time: at each candle `t` it builds the forecast from bars `≤ t` only, then
reveals the future **one bar at a time** to resolve it. This surfaces failures a backtest
launders away — most importantly forecasts that are **already wrong the instant they're
made** (STALE), and direction skill measured **out-of-sample at every step**.

## The causal walk (what the harness does)
For each step `t` from `max(roll, n-forward)` to `n-resolve`:
1. Hand the forecaster `bars[t-roll+1 .. t]` (no future).
2. Get a `Forecast(direction, target, invalidation)` or `None`.
3. Ghost-feed `bars[t+1 .. t+resolve]` and classify the first thing that happens.
4. Record next-candle direction (was `t+1`'s close up or down vs `t`).

`roll` bounds the lookback (and keeps cost linear); `forward=all` walks the whole series;
`resolve` is the horizon a call gets to play out.

## Outcome definitions
| outcome | meaning |
|---|---|
| **HIT** | target reached before invalidation, within `resolve` bars |
| **INVALIDATED** | invalidation (stop) reached first |
| **OPEN** | neither reached within the horizon |
| **STALE** | at decision time the target/invalidation were already on the wrong side of price (`up` needs `inv < price < target`); the call is degenerate and **excluded** from hit-rate so it can't be scored as a trivial instant "win" |
| **no-forecast** | the model returned `None` |

Headline metrics: **next-candle directional accuracy** (50% = no edge), **target-hit among
usable** (HIT / (HIT+INVALIDATED)), and **STALE %**.

## Pitfalls that will fool you (each one bit us — learn from it)
1. **Look-ahead leakage.** The whole point is causality. Don't let the model see future
   bars, a global "current price", or parameters fit on the full series. Keep all logic
   inside `forecast(bars)`.
2. **Sample window ≠ the conclusion.** A model tested only on a recent **reversal** month
   showed 45–86% STALE and 0–26% hit; the *same model* over a full year showed 9–27% STALE.
   The difference was the **regime**, not the model. Always test across a **long,
   multi-regime** window before concluding anything.
3. **Bar density silently breaks bar-counted constants.** `roll`/`resolve` are in *bars*.
   Extended-hours data (~64 bars/day) vs RTH (~26) changes what "400 bars" means in calendar
   time. Pick a session (doc 02) and keep it fixed.
4. **Target-hit without R:R is a mirage.** Placing the target nearer than the stop inflates
   hit-rate while losing money. Always read hit-rate next to **direction** and the
   **median bars-to-resolution** (if INVALIDATED resolves faster than HIT, your stop is
   tighter than your target).
5. **Confidence you never validated.** If `ghost_diag` shows flat accuracy across confidence
   buckets, your confidence is noise. Don't size on it until it's monotonic.
6. **STALE is a signal, not a nuisance.** A high STALE rate means your anchor (e.g. a
   confirmed pivot) lags price — the projection is built off something stale. Fix the anchor
   or re-anchor to live price.
7. **Direction that just echoes the trend.** The trend-agreement split in `ghost_diag` is the
   tell: if accuracy is ~50% whether the call agrees or disagrees with the recent trend, the
   direction is a **mechanical reflex with no information**, regardless of how sophisticated
   the labels look.

## What a real edge must clear
- Next-candle direction **clearly > 50%** and **stable across regimes** and symbols.
- Edge **localised in a nameable `kind`** you can gate on (not smeared across everything).
- **Confidence monotonic** with accuracy.
- Target-hit > 50% **at R:R ≥ 1**.
- Survives a **walk-forward** (don't tune on the same window you report).

## Honesty checklist before you believe a result
- [ ] Causal — no future, no globals, no whole-series fitting.
- [ ] Long, multi-regime window (ideally ≥ a year of the target timeframe).
- [ ] One session policy (RTH or EH), stated.
- [ ] Direction and hit-rate read **together**, with R:R and resolution speed.
- [ ] Re-checked on a second symbol / out-of-sample window.
- [ ] STALE / OPEN explained, not ignored.

A model that produces correct *structure* but coin-flip *direction* is not a trading edge —
it's an analysis tool. The kit is built to tell those two apart, honestly.
