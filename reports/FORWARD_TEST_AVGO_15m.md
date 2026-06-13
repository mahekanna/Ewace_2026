# Forward test (ghost-feeding) — AVGO 15m

_Simulated real time: at each of 228 candles (2026-05-22 13:30 → 2026-06-04 18:15) the LIVE forecast is built from the prior 400 candles only, then the next 32 candles are ghost-fed to resolve it. Causal; not advice._

## Summary
- **STALE/unusable forecasts: 13** of 228 (6%) — the target was already on the wrong side of price because the count's confirmed pivot lags (intraday lag). These are EXCLUDED, not counted as instant wins.
- Usable forecasts resolved: **86** (HIT 49 / INVALIDATED 37); OPEN 129; no-forecast 0.
- **Target-hit rate among USABLE forecasts: 57%.**
- Next-candle directional accuracy: **55%** of 228 (coin-flip = 50%).
- Snapshots (forecast vs realized): `charts/png/forward/avgo_15m_step_1.png`, `charts/png/forward/avgo_15m_step_2.png`, `charts/png/forward/avgo_15m_step_3.png`, `charts/png/forward/avgo_15m_step_4.png`, `charts/png/forward/avgo_15m_step_5.png`, `charts/png/forward/avgo_15m_step_6.png`

## Live forecast log (every 8th candle)
| time | price | forecast | conf | target | invalid | outcome |
|---|---|---|---|---|---|---|
| 05-22 13:30 | 419.23 | new impulse (up) | 50% | 441.78 | 405.87 | OPEN |
| 05-22 15:30 | 413.94 | new impulse (up) | 50% | 436.49 | 405.87 | OPEN |
| 05-22 17:30 | 413.19 | new impulse (up) | 50% | 435.74 | 405.87 | OPEN |
| 05-22 19:30 | 411.82 | new impulse (up) | 50% | 434.37 | 405.87 | HIT (5) |
| 05-26 15:00 | 427.80 | new impulse (up) | 38% | 460.89 | 405.87 | OPEN |
| 05-26 17:00 | 423.02 | new impulse (up) | 38% | 456.11 | 405.87 | OPEN |
| 05-26 19:00 | 423.31 | new impulse (up) | 38% | 456.40 | 405.87 | OPEN |
| 05-27 14:30 | 420.00 | new impulse (up) | 38% | 453.09 | 405.87 | OPEN |
| 05-27 16:30 | 420.69 | new impulse (up) | 38% | 453.79 | 405.87 | OPEN |
| 05-27 18:30 | 420.68 | new impulse (up) | 38% | 453.77 | 405.87 | OPEN |
| 05-28 14:00 | 422.02 | new impulse (up) | 38% | 455.12 | 405.87 | OPEN |
| 05-28 16:00 | 425.22 | new impulse (up) | 38% | 447.77 | 405.87 | HIT (17) |
| 05-28 18:00 | 428.79 | new impulse (up) | 57% | 451.34 | 405.87 | OPEN |
| 05-29 13:30 | 445.68 | new impulse (up) | 57% | 468.23 | 405.87 | OPEN |
| 05-29 15:30 | 439.00 | new impulse (up) | 57% | 461.55 | 405.87 | HIT (28) |
| 05-29 17:30 | 434.98 | new impulse (up) | 57% | 457.53 | 405.87 | HIT (14) |
| 05-29 19:30 | 440.18 | new impulse (up) | 57% | 462.73 | 405.87 | HIT (12) |
| 06-01 15:00 | 456.11 | new impulse (up) | 57% | 478.66 | 405.87 | HIT (20) |
| 06-01 17:00 | 461.69 | new impulse (up) | 57% | 503.14 | 405.87 | OPEN |
| 06-01 19:00 | 461.89 | new impulse (up) | 57% | 503.34 | 405.87 | OPEN |
| 06-02 14:30 | 480.47 | new impulse (up) | 58% | 521.92 | 405.87 | OPEN |
| 06-02 16:30 | 483.06 | new impulse (up) | 57% | 524.51 | 405.87 | OPEN |
| 06-02 18:30 | 471.85 | new impulse (up) | 55% | 513.30 | 405.87 | INVALIDATED (32) |
| 06-03 14:00 | 481.90 | new impulse (up) | 54% | 523.35 | 405.87 | INVALIDATED (24) |
| 06-03 16:00 | 483.97 | new impulse (up) | 56% | 525.42 | 405.87 | INVALIDATED (16) |
| 06-03 18:00 | 486.50 | new impulse (up) | 40% | 503.68 | 414.02 | INVALIDATED (8) |
| 06-04 13:30 | 403.79 | new impulse (up) | 40% | 431.20 | 414.02 | stale |
| 06-04 15:30 | 412.98 | new impulse (up) | 40% | 431.20 | 414.02 | stale |
| 06-04 17:30 | 422.46 | new impulse (up) | 56% | 479.31 | 403.01 | INVALIDATED (10) |
