# Forward test (ghost-feeding) — AVGO 15m_eh

_Simulated real time: at each of 228 candles (2026-06-08 23:00 → 2026-06-12 15:45) the LIVE forecast is built from the prior 400 candles only, then the next 32 candles are ghost-fed to resolve it. Causal; not advice._

## Summary
- **STALE/unusable forecasts: 196** of 228 (86%) — the target was already on the wrong side of price because the count's confirmed pivot lags (intraday lag). These are EXCLUDED, not counted as instant wins.
- Usable forecasts resolved: **0** (HIT 0 / INVALIDATED 0); OPEN 32; no-forecast 0.
- **Target-hit rate among USABLE forecasts: 0%.**
- Next-candle directional accuracy: **45%** of 228 (coin-flip = 50%).
- Snapshots (forecast vs realized): `charts/png/forward/avgo_15m_eh_step_1.png`, `charts/png/forward/avgo_15m_eh_step_2.png`, `charts/png/forward/avgo_15m_eh_step_3.png`, `charts/png/forward/avgo_15m_eh_step_4.png`, `charts/png/forward/avgo_15m_eh_step_5.png`, `charts/png/forward/avgo_15m_eh_step_6.png`

## Live forecast log (every 8th candle)
| time | price | forecast | conf | target | invalid | outcome |
|---|---|---|---|---|---|---|
| 06-08 23:00 | 396.88 | corrective A-B-C (up) | 36% | 429.62 | 499.12 | stale |
| 06-09 09:00 | 401.80 | corrective A-B-C (up) | 36% | 429.62 | 499.12 | stale |
| 06-09 11:00 | 401.06 | corrective A-B-C (up) | 36% | 429.62 | 499.12 | stale |
| 06-09 13:00 | 403.87 | corrective A-B-C (up) | 36% | 429.62 | 499.12 | stale |
| 06-09 15:00 | 387.98 | corrective A-B-C (up) | 36% | 429.62 | 499.12 | stale |
| 06-09 17:00 | 379.88 | corrective A-B-C (up) | 40% | 433.34 | 499.12 | stale |
| 06-09 19:00 | 389.74 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-09 21:00 | 390.85 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-09 23:00 | 388.50 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-10 09:00 | 382.50 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-10 11:00 | 383.56 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-10 13:00 | 386.19 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-10 15:00 | 372.06 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-10 17:00 | 373.12 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-10 19:00 | 372.82 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-10 21:00 | 371.79 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-10 23:00 | 366.17 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-11 09:00 | 376.50 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
| 06-11 11:00 | 374.70 | corrective A-B-C (up) | 40% | 433.26 | 499.00 | stale |
| 06-11 13:00 | 371.99 | corrective A-B-C (up) | 40% | 432.62 | 496.44 | stale |
| 06-11 15:00 | 375.92 | corrective A-B-C (up) | 40% | 432.56 | 496.16 | stale |
| 06-11 17:00 | 376.26 | new impulse (down) | 44% | 305.02 | 410.21 | OPEN |
| 06-11 19:00 | 385.61 | new impulse (down) | 46% | 314.37 | 410.21 | OPEN |
| 06-11 21:00 | 384.10 | new impulse (down) | 46% | 312.86 | 410.21 | OPEN |
| 06-11 23:00 | 384.53 | new impulse (down) | 46% | 313.29 | 410.21 | OPEN |
| 06-12 09:00 | 387.25 | corrective A-B-C (up) | 40% | 391.42 | 479.23 | stale |
| 06-12 11:00 | 387.62 | corrective A-B-C (up) | 47% | 391.42 | 479.23 | stale |
| 06-12 13:00 | 383.56 | corrective A-B-C (up) | 47% | 391.42 | 479.23 | stale |
| 06-12 15:00 | 382.70 | corrective A-B-C (up) | 47% | 391.42 | 479.23 | stale |
