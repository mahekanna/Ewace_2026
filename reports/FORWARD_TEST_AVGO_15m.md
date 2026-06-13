# Forward test (ghost-feeding) — AVGO 15m

_Simulated real time: at each of 228 candles (2026-05-22 13:30 → 2026-06-04 18:15) the LIVE forecast is built from the prior 400 candles only, then the next 32 candles are ghost-fed to resolve it. Causal; not advice._

## Summary
- **STALE/unusable forecasts: 117** of 228 (51%) — the target was already on the wrong side of price because the count's confirmed pivot lags (intraday lag). These are EXCLUDED, not counted as instant wins.
- Usable forecasts resolved: **63** (HIT 56 / INVALIDATED 7); OPEN 48; no-forecast 0.
- **Target-hit rate among USABLE forecasts: 89%.**
- Next-candle directional accuracy: **55%** of 228 (coin-flip = 50%).
- Snapshots (forecast vs realized): `charts/png/forward/avgo_15m_step_1.png`, `charts/png/forward/avgo_15m_step_2.png`, `charts/png/forward/avgo_15m_step_3.png`, `charts/png/forward/avgo_15m_step_4.png`, `charts/png/forward/avgo_15m_step_5.png`, `charts/png/forward/avgo_15m_step_6.png`

## Live forecast log (every 8th candle)
| time | price | forecast | conf | target | invalid | outcome |
|---|---|---|---|---|---|---|
| 05-22 13:30 | 419.23 | new impulse (up) | 50% | 428.42 | 405.87 | HIT (27) |
| 05-22 15:30 | 413.94 | new impulse (up) | 50% | 428.42 | 405.87 | HIT (19) |
| 05-22 17:30 | 413.19 | new impulse (up) | 50% | 428.42 | 405.87 | HIT (11) |
| 05-22 19:30 | 411.82 | new impulse (up) | 50% | 428.42 | 405.87 | HIT (3) |
| 05-26 15:00 | 427.80 | new impulse (up) | 38% | 438.96 | 405.87 | OPEN |
| 05-26 17:00 | 423.02 | new impulse (up) | 38% | 438.96 | 405.87 | OPEN |
| 05-26 19:00 | 423.31 | new impulse (up) | 38% | 438.96 | 405.87 | OPEN |
| 05-27 14:30 | 420.00 | new impulse (up) | 38% | 438.96 | 405.87 | OPEN |
| 05-27 16:30 | 420.69 | new impulse (up) | 38% | 438.96 | 405.87 | OPEN |
| 05-27 18:30 | 420.68 | new impulse (up) | 38% | 438.96 | 405.87 | HIT (32) |
| 05-28 14:00 | 422.02 | new impulse (up) | 38% | 438.96 | 405.87 | HIT (24) |
| 05-28 16:00 | 425.22 | new impulse (up) | 38% | 428.42 | 405.87 | HIT (6) |
| 05-28 18:00 | 428.79 | new impulse (up) | 57% | 428.42 | 405.87 | stale |
| 05-29 13:30 | 445.68 | new impulse (up) | 57% | 428.42 | 405.87 | stale |
| 05-29 15:30 | 439.00 | new impulse (up) | 57% | 428.42 | 405.87 | stale |
| 05-29 17:30 | 434.98 | new impulse (up) | 57% | 428.42 | 405.87 | stale |
| 05-29 19:30 | 440.18 | new impulse (up) | 57% | 428.42 | 405.87 | stale |
| 06-01 15:00 | 456.11 | new impulse (up) | 57% | 428.42 | 405.87 | stale |
| 06-01 17:00 | 461.69 | new impulse (up) | 57% | 428.42 | 405.87 | stale |
| 06-01 19:00 | 461.89 | new impulse (up) | 57% | 428.42 | 405.87 | stale |
| 06-02 14:30 | 480.47 | new impulse (up) | 58% | 428.42 | 405.87 | stale |
| 06-02 16:30 | 483.06 | new impulse (up) | 57% | 428.42 | 405.87 | stale |
| 06-02 18:30 | 471.85 | new impulse (up) | 55% | 428.42 | 405.87 | stale |
| 06-03 14:00 | 481.90 | new impulse (up) | 54% | 428.42 | 405.87 | stale |
| 06-03 16:00 | 483.97 | new impulse (up) | 56% | 428.42 | 405.87 | stale |
| 06-03 18:00 | 486.50 | new impulse (up) | 40% | 431.20 | 414.02 | stale |
| 06-04 13:30 | 403.79 | new impulse (up) | 40% | 431.20 | 414.02 | stale |
| 06-04 15:30 | 412.98 | new impulse (up) | 40% | 431.20 | 414.02 | stale |
| 06-04 17:30 | 422.46 | new impulse (up) | 56% | 459.86 | 403.01 | INVALIDATED (10) |
