# Forward test (ghost-feeding) — MRVL 15m

_Simulated real time: at each of 127 candles (2026-06-04 19:15 → 2026-06-11 18:15) the LIVE forecast is built from the prior 400 candles only, then the next 32 candles are ghost-fed to resolve it. Causal; not advice._

## Summary
- **STALE/unusable forecasts: 57** of 127 (45%) — the target was already on the wrong side of price because the count's confirmed pivot lags (intraday lag). These are EXCLUDED, not counted as instant wins.
- Usable forecasts resolved: **22** (HIT 0 / INVALIDATED 22); OPEN 48; no-forecast 0.
- **Target-hit rate among USABLE forecasts: 0%.**
- Next-candle directional accuracy: **50%** of 127 (coin-flip = 50%).
- Snapshots (forecast vs realized): `charts/png/forward/mrvl_15m_step_1.png`, `charts/png/forward/mrvl_15m_step_2.png`, `charts/png/forward/mrvl_15m_step_3.png`, `charts/png/forward/mrvl_15m_step_4.png`, `charts/png/forward/mrvl_15m_step_5.png`, `charts/png/forward/mrvl_15m_step_6.png`

## Live forecast log (every 8th candle)
| time | price | forecast | conf | target | invalid | outcome |
|---|---|---|---|---|---|---|
| 06-04 19:15 | 319.85 | new impulse (up) | 51% | 348.67 | 277.56 | INVALIDATED (22) |
| 06-05 14:45 | 295.85 | new impulse (up) | 51% | 324.67 | 277.56 | INVALIDATED (14) |
| 06-05 16:45 | 284.51 | new impulse (up) | 50% | 313.33 | 277.56 | INVALIDATED (6) |
| 06-05 18:45 | 278.37 | new impulse (down) | 58% | 163.34 | 321.50 | OPEN |
| 06-08 14:15 | 294.34 | new impulse (down) | 43% | 179.31 | 321.50 | OPEN |
| 06-08 16:15 | 298.44 | new impulse (down) | 43% | 183.41 | 321.50 | OPEN |
| 06-08 18:15 | 300.52 | new impulse (down) | 43% | 185.49 | 321.50 | OPEN |
| 06-09 13:45 | 282.36 | new impulse (down) | 43% | 167.32 | 321.50 | OPEN |
| 06-09 15:45 | 254.63 | new impulse (down) | 37% | 140.56 | 304.96 | OPEN |
| 06-09 17:45 | 257.60 | corrective A-B-C (down) | 60% | 222.41 | 194.70 | stale |
| 06-09 19:45 | 266.88 | corrective A-B-C (down) | 60% | 222.41 | 194.70 | stale |
| 06-10 15:15 | 257.72 | corrective A-B-C (down) | 60% | 222.41 | 194.70 | stale |
| 06-10 17:15 | 256.75 | corrective A-B-C (down) | 60% | 222.41 | 194.70 | stale |
| 06-10 19:15 | 254.58 | corrective A-B-C (down) | 60% | 222.41 | 194.70 | stale |
| 06-11 14:45 | 260.81 | new impulse (down) | 37% | 146.74 | 304.96 | OPEN |
| 06-11 16:45 | 263.41 | corrective A-B-C (down) | 60% | 222.41 | 194.70 | stale |
