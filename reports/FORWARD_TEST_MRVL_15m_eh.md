# Forward test (ghost-feeding) — MRVL 15m_eh

_Simulated real time: at each of 228 candles (2026-06-08 23:00 → 2026-06-12 15:45) the LIVE forecast is built from the prior 400 candles only, then the next 32 candles are ghost-fed to resolve it. Causal; not advice._

## Summary
- **STALE/unusable forecasts: 49** of 228 (21%) — the target was already on the wrong side of price because the count's confirmed pivot lags (intraday lag). These are EXCLUDED, not counted as instant wins.
- Usable forecasts resolved: **47** (HIT 12 / INVALIDATED 35); OPEN 132; no-forecast 0.
- **Target-hit rate among USABLE forecasts: 26%.**
- Next-candle directional accuracy: **49%** of 228 (coin-flip = 50%).
- Snapshots (forecast vs realized): `charts/png/forward/mrvl_15m_eh_step_1.png`, `charts/png/forward/mrvl_15m_eh_step_2.png`, `charts/png/forward/mrvl_15m_eh_step_3.png`, `charts/png/forward/mrvl_15m_eh_step_4.png`, `charts/png/forward/mrvl_15m_eh_step_5.png`, `charts/png/forward/mrvl_15m_eh_step_6.png`

## Live forecast log (every 8th candle)
| time | price | forecast | conf | target | invalid | outcome |
|---|---|---|---|---|---|---|
| 06-08 23:00 | 287.29 | new impulse (up) | 39% | 312.42 | 253.00 | OPEN |
| 06-09 09:00 | 301.98 | new impulse (up) | 39% | 327.11 | 253.00 | INVALIDATED (28) |
| 06-09 11:00 | 299.01 | new impulse (up) | 39% | 324.14 | 253.00 | INVALIDATED (20) |
| 06-09 13:00 | 299.63 | new impulse (up) | 39% | 324.76 | 253.00 | INVALIDATED (12) |
| 06-09 15:00 | 268.28 | new impulse (down) | 38% | 132.25 | 304.96 | OPEN |
| 06-09 17:00 | 255.38 | new impulse (down) | 38% | 119.35 | 304.96 | OPEN |
| 06-09 19:00 | 260.24 | new impulse (up) | 38% | 267.52 | 244.00 | HIT (4) |
| 06-09 21:00 | 269.00 | new impulse (up) | 38% | 276.28 | 244.00 | OPEN |
| 06-09 23:00 | 263.30 | new impulse (up) | 37% | 270.58 | 244.00 | HIT (27) |
| 06-10 09:00 | 255.20 | new impulse (down) | 56% | 181.11 | 244.00 | stale |
| 06-10 11:00 | 257.00 | new impulse (down) | 56% | 181.11 | 244.00 | stale |
| 06-10 13:00 | 260.86 | new impulse (up) | 50% | 314.38 | 253.00 | INVALIDATED (25) |
| 06-10 15:00 | 257.02 | new impulse (down) | 39% | 120.99 | 304.96 | OPEN |
| 06-10 17:00 | 255.88 | corrective A-B-C (up) | 63% | 304.02 | 339.60 | stale |
| 06-10 19:00 | 255.50 | corrective A-B-C (up) | 63% | 304.02 | 339.60 | stale |
| 06-10 21:00 | 247.00 | corrective A-B-C (up) | 63% | 304.02 | 339.60 | stale |
| 06-10 23:00 | 242.00 | corrective A-B-C (up) | 63% | 304.02 | 339.60 | stale |
| 06-11 09:00 | 259.49 | new impulse (up) | 50% | 298.40 | 242.00 | OPEN |
| 06-11 11:00 | 260.25 | new impulse (down) | 45% | 124.22 | 304.96 | OPEN |
| 06-11 13:00 | 265.12 | new impulse (up) | 50% | 304.03 | 242.00 | OPEN |
| 06-11 15:00 | 262.82 | new impulse (up) | 33% | 294.94 | 253.00 | OPEN |
| 06-11 17:00 | 263.05 | new impulse (up) | 50% | 281.88 | 242.00 | HIT (11) |
| 06-11 19:00 | 277.65 | new impulse (up) | 49% | 296.48 | 242.00 | OPEN |
| 06-11 21:00 | 276.50 | new impulse (up) | 49% | 295.33 | 242.00 | OPEN |
| 06-11 23:00 | 279.90 | new impulse (up) | 50% | 298.73 | 242.00 | OPEN |
| 06-12 09:00 | 276.45 | new impulse (up) | 50% | 295.28 | 242.00 | OPEN |
| 06-12 11:00 | 275.55 | new impulse (up) | 50% | 294.38 | 242.00 | OPEN |
| 06-12 13:00 | 273.06 | new impulse (up) | 50% | 291.89 | 242.00 | OPEN |
| 06-12 15:00 | 284.88 | new impulse (up) | 50% | 303.71 | 242.00 | OPEN |
