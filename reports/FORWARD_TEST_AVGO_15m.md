# Forward test (ghost-feeding) — AVGO 15m

_Simulated real time: at each of 134 candles (2026-06-04 17:30 → 2026-06-11 18:15) the LIVE forecast is built from the prior 400 candles only, then the next 32 candles are ghost-fed to resolve it. Causal; not advice._

## Summary
- **STALE/unusable forecasts: 80** of 134 (60%) — the target was already on the wrong side of price because the count's confirmed pivot lags (intraday lag). These are EXCLUDED, not counted as instant wins.
- Usable forecasts resolved: **19** (HIT 3 / INVALIDATED 16); OPEN 35; no-forecast 0.
- **Target-hit rate among USABLE forecasts: 16%.**
- Next-candle directional accuracy: **49%** of 134 (coin-flip = 50%).
- Snapshots (forecast vs realized): `charts/png/forward/avgo_15m_step_1.png`, `charts/png/forward/avgo_15m_step_2.png`, `charts/png/forward/avgo_15m_step_3.png`, `charts/png/forward/avgo_15m_step_4.png`, `charts/png/forward/avgo_15m_step_5.png`, `charts/png/forward/avgo_15m_step_6.png`

## Live forecast log (every 8th candle)
| time | price | forecast | conf | target | invalid | outcome |
|---|---|---|---|---|---|---|
| 06-04 17:30 | 422.43 | new impulse (up) | 56% | 479.27 | 403.01 | INVALIDATED (10) |
| 06-04 19:30 | 422.05 | new impulse (up) | 56% | 478.90 | 403.01 | INVALIDATED (2) |
| 06-05 15:00 | 398.46 | new impulse (down) | 46% | 371.80 | 426.48 | OPEN |
| 06-05 17:00 | 394.50 | new impulse (down) | 46% | 367.84 | 426.48 | OPEN |
| 06-05 19:00 | 387.29 | new impulse (down) | 46% | 360.63 | 426.48 | OPEN |
| 06-08 14:30 | 396.42 | new impulse (down) | 46% | 369.76 | 426.48 | OPEN |
| 06-08 16:30 | 394.71 | new impulse (up) | 46% | 468.83 | 426.48 | stale |
| 06-08 18:30 | 394.82 | new impulse (up) | 46% | 468.83 | 426.48 | stale |
| 06-09 14:00 | 395.00 | new impulse (up) | 46% | 420.27 | 385.59 | INVALIDATED (5) |
| 06-09 16:00 | 375.96 | new impulse (up) | 42% | 422.93 | 407.87 | stale |
| 06-09 18:00 | 385.57 | new impulse (up) | 65% | 413.84 | 393.39 | stale |
| 06-10 13:30 | 378.82 | corrective A-B-C (up) | 39% | 395.20 | 495.00 | stale |
| 06-10 15:30 | 376.05 | corrective A-B-C (up) | 39% | 395.20 | 495.00 | stale |
| 06-10 17:30 | 374.45 | corrective A-B-C (up) | 39% | 395.20 | 495.00 | stale |
| 06-10 19:30 | 373.21 | corrective A-B-C (up) | 39% | 395.20 | 495.00 | stale |
| 06-11 15:00 | 375.92 | corrective A-B-C (up) | 39% | 395.20 | 495.00 | stale |
| 06-11 17:00 | 376.26 | corrective A-B-C (up) | 39% | 395.20 | 495.00 | stale |
