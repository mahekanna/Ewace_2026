# Forward test (ghost-feeding) — AVGO 15m_eh

_Simulated real time: at each of 23367 candles (2024-12-19 12:45 → 2026-06-12 15:45) the LIVE forecast is built from the prior 400 candles only, then the next 32 candles are ghost-fed to resolve it. Causal; not advice._

## Summary
- **STALE/unusable forecasts: 2079** of 23367 (9%) — the target was already on the wrong side of price because the count's confirmed pivot lags (intraday lag). These are EXCLUDED, not counted as instant wins.
- Usable forecasts resolved: **1147** (HIT 439 / INVALIDATED 708); OPEN 7427; no-forecast 12714.
- **Target-hit rate among USABLE forecasts: 38%.**
- Next-candle directional accuracy: **51%** of 10653 (coin-flip = 50%).
- Snapshots (forecast vs realized): `charts/png/forward/avgo_15m_eh_step_1.png`, `charts/png/forward/avgo_15m_eh_step_2.png`, `charts/png/forward/avgo_15m_eh_step_3.png`, `charts/png/forward/avgo_15m_eh_step_4.png`, `charts/png/forward/avgo_15m_eh_step_5.png`, `charts/png/forward/avgo_15m_eh_step_6.png`

## Live forecast log (every 194th candle)
| time | price | forecast | conf | target | invalid | outcome |
|---|---|---|---|---|---|---|
| 12-19 12:45 | 226.15 | new impulse (up) | 25% | 238.97 | 230.81 | stale |
| 12-24 13:15 | 238.60 | new impulse (down) | 38% | 215.00 | 228.70 | stale |
| 12-30 16:45 | 235.88 | new impulse (down) | 50% | 161.72 | 247.47 | OPEN |
| 01-03 17:15 | 232.94 | (no clean count) | - | - | - | - |
| 01-08 17:45 | 228.50 | (no clean count) | - | - | - | - |
| 01-14 18:45 | 226.29 | (no clean count) | - | - | - | - |
| 01-17 20:00 | 236.57 | new impulse (up) | 50% | 244.95 | 228.24 | OPEN |
| 01-23 20:30 | 238.24 | (no clean count) | - | - | - | - |
| 01-28 21:15 | 207.05 | new impulse (up) | 50% | 228.13 | 198.89 | OPEN |
| 01-31 21:45 | 220.96 | new impulse (up) | 51% | 235.07 | 202.77 | OPEN |
| 02-05 22:15 | 235.00 | new impulse (up) | 26% | 245.05 | 222.43 | OPEN |
| 02-10 23:15 | 234.20 | new impulse (up) | 38% | 250.00 | 224.02 | OPEN |
| 02-14 00:45 | 234.95 | (no clean count) | - | - | - | - |
| 02-20 09:30 | 226.42 | (no clean count) | - | - | - | - |
| 02-25 10:45 | 205.61 | (no clean count) | - | - | - | - |
| 02-28 11:15 | 199.47 | (no clean count) | - | - | - | - |
| 03-05 12:15 | 190.88 | new impulse (up) | 43% | 206.08 | 180.48 | OPEN |
| 03-10 11:45 | 189.59 | new impulse (up) | 45% | 207.77 | 181.56 | INVALIDATED (21) |
| 03-13 12:15 | 192.78 | new impulse (up) | 39% | 211.90 | 180.04 | OPEN |
| 03-18 12:45 | 190.13 | new impulse (up) | 57% | 204.88 | 187.00 | INVALIDATED (19) |
| 03-21 13:30 | 187.83 | new impulse (up) | 45% | 195.77 | 186.90 | OPEN |
| 03-26 14:45 | 183.05 | (no clean count) | - | - | - | - |
| 03-31 15:15 | 163.72 | (no clean count) | - | - | - | - |
| 04-03 16:15 | 159.59 | (no clean count) | - | - | - | - |
| 04-08 16:45 | 160.72 | new impulse (down) | 35% | 116.92 | 143.49 | stale |
| 04-11 17:30 | 179.50 | corrective A-B-C (down) | 30% | 160.64 | 132.62 | stale |
| 04-16 18:45 | 168.11 | new impulse (down) | 39% | 113.97 | 187.08 | OPEN |
| 04-22 19:30 | 168.35 | new impulse (up) | 61% | 178.90 | 161.61 | OPEN |
| 04-25 20:00 | 192.50 | new impulse (up) | 52% | 198.51 | 173.02 | OPEN |
| 04-30 20:45 | 196.75 | new impulse (up) | 57% | 204.48 | 184.02 | OPEN |
| 05-05 22:30 | 200.80 | (no clean count) | - | - | - | - |
| 05-09 08:00 | 208.30 | (no clean count) | - | - | - | - |
| 05-14 08:30 | 231.77 | (no clean count) | - | - | - | - |
| 05-19 10:15 | 221.75 | (no clean count) | - | - | - | - |
| 05-22 12:15 | 227.20 | (no clean count) | - | - | - | - |
| 05-28 14:00 | 236.24 | (no clean count) | - | - | - | - |
| 06-02 15:15 | 247.01 | new impulse (up) | 58% | 262.95 | 234.90 | OPEN |
| 06-05 15:45 | 264.12 | (no clean count) | - | - | - | - |
| 06-10 16:15 | 245.36 | new impulse (up) | 35% | 257.82 | 248.88 | stale |
| 06-13 17:15 | 250.81 | new impulse (up) | 45% | 267.73 | 241.11 | OPEN |
| 06-18 18:00 | 251.75 | (no clean count) | - | - | - | - |
| 06-24 20:00 | 263.54 | (no clean count) | - | - | - | - |
| 06-27 21:00 | 271.30 | (no clean count) | - | - | - | - |
| 07-02 22:15 | 269.30 | (no clean count) | - | - | - | - |
| 07-09 13:00 | 271.88 | (no clean count) | - | - | - | - |
| 07-14 14:45 | 274.57 | (no clean count) | - | - | - | - |
| 07-17 17:15 | 287.58 | (no clean count) | - | - | - | - |
| 07-22 20:15 | 278.02 | (no clean count) | - | - | - | - |
| 07-25 21:45 | 290.74 | (no clean count) | - | - | - | - |
| 07-30 23:45 | 302.31 | (no clean count) | - | - | - | - |
| 08-05 08:15 | 298.35 | new impulse (up) | 58% | 308.47 | 281.61 | OPEN |
| 08-08 09:45 | 306.55 | new impulse (up) | 58% | 316.67 | 281.61 | OPEN |
| 08-13 13:00 | 315.73 | (no clean count) | - | - | - | - |
| 08-18 17:45 | 304.14 | (no clean count) | - | - | - | - |
| 08-21 21:15 | 289.87 | (no clean count) | - | - | - | - |
| 08-27 08:15 | 298.16 | (no clean count) | - | - | - | - |
| 09-02 11:00 | 292.58 | (no clean count) | - | - | - | - |
| 09-05 11:30 | 339.79 | new impulse (up) | 57% | 352.59 | 298.00 | HIT (7) |
| 09-10 12:00 | 345.23 | new impulse (down) | 38% | 319.39 | 354.17 | INVALIDATED (6) |
| 09-15 13:15 | 359.82 | new impulse (down) | 56% | 259.29 | 374.23 | OPEN |
| 09-18 14:00 | 348.47 | (no clean count) | - | - | - | - |
| 09-23 15:15 | 343.80 | (no clean count) | - | - | - | - |
| 09-26 16:30 | 334.36 | (no clean count) | - | - | - | - |
| 10-01 17:45 | 335.83 | new impulse (up) | 39% | 349.22 | 324.50 | OPEN |
| 10-06 18:15 | 337.44 | new impulse (up) | 55% | 364.05 | 324.58 | OPEN |
| 10-09 19:30 | 345.26 | new impulse (up) | 57% | 359.46 | 326.58 | OPEN |
| 10-14 20:15 | 343.51 | new impulse (down) | 55% | 264.68 | 363.98 | OPEN |
| 10-17 21:00 | 349.95 | new impulse (down) | 37% | 288.20 | 363.24 | OPEN |
| 10-22 23:15 | 341.44 | (no clean count) | - | - | - | - |
| 10-28 09:00 | 364.19 | (no clean count) | - | - | - | - |
| 10-31 09:30 | 376.33 | (no clean count) | - | - | - | - |
| 11-05 11:30 | 349.60 | (no clean count) | - | - | - | - |
| 11-10 12:00 | 358.23 | new impulse (up) | 62% | 389.58 | 337.27 | OPEN |
| 11-13 12:30 | 353.85 | (no clean count) | - | - | - | - |
| 11-18 13:15 | 343.00 | (no clean count) | - | - | - | - |
| 11-21 13:45 | 349.16 | new impulse (down) | 34% | 242.95 | 376.08 | OPEN |
| 11-26 14:15 | 385.47 | new impulse (up) | 58% | 412.45 | 371.75 | OPEN |
| 12-02 17:45 | 381.34 | new impulse (down) | 61% | 295.99 | 404.35 | OPEN |
| 12-05 18:30 | 388.84 | (no clean count) | - | - | - | - |
| 12-10 19:00 | 407.32 | (no clean count) | - | - | - | - |
| 12-15 19:30 | 340.18 | new impulse (up) | 52% | 408.07 | 382.00 | stale |
| 12-18 20:00 | 328.75 | new impulse (up) | 32% | 392.26 | 321.42 | OPEN |
| 12-23 20:30 | 348.35 | (no clean count) | - | - | - | - |
| 12-30 00:00 | 348.12 | (no clean count) | - | - | - | - |
| 01-03 00:45 | 347.58 | (no clean count) | - | - | - | - |
| 01-08 09:15 | 341.12 | new impulse (up) | 40% | 362.87 | 335.88 | INVALIDATED (21) |
| 01-13 09:45 | 351.27 | new impulse (up) | 40% | 373.08 | 330.50 | OPEN |
| 01-16 10:15 | 346.57 | (no clean count) | - | - | - | - |
| 01-22 10:45 | 335.14 | (no clean count) | - | - | - | - |
| 01-27 11:15 | 327.91 | (no clean count) | - | - | - | - |
| 01-30 11:45 | 331.06 | (no clean count) | - | - | - | - |
| 02-04 12:15 | 319.10 | new impulse (down) | 48% | 298.41 | 338.90 | HIT (21) |
| 02-09 12:45 | 329.87 | new impulse (up) | 52% | 355.07 | 304.35 | OPEN |
| 02-12 13:15 | 343.49 | new impulse (down) | 51% | 275.92 | 352.34 | OPEN |
| 02-18 13:45 | 329.69 | (no clean count) | - | - | - | - |
| 02-23 14:15 | 332.25 | (no clean count) | - | - | - | - |
| 02-26 14:45 | 316.40 | (no clean count) | - | - | - | - |
| 03-03 15:15 | 309.30 | new impulse (up) | 58% | 333.66 | 324.00 | stale |
| 03-06 15:45 | 336.60 | new impulse (up) | 39% | 364.67 | 317.53 | OPEN |
| 03-11 15:15 | 341.39 | new impulse (up) | 58% | 370.09 | 318.25 | OPEN |
| 03-16 15:45 | 327.47 | (no clean count) | - | - | - | - |
| 03-19 16:15 | 318.95 | (no clean count) | - | - | - | - |
| 03-24 16:45 | 317.72 | new impulse (up) | 39% | 330.99 | 303.09 | OPEN |
| 03-27 17:15 | 299.66 | (no clean count) | - | - | - | - |
| 04-01 17:45 | 313.36 | (no clean count) | - | - | - | - |
| 04-07 18:15 | 331.11 | new impulse (up) | 50% | 342.47 | 301.75 | HIT (18) |
| 04-10 18:45 | 373.54 | (no clean count) | - | - | - | - |
| 04-15 19:15 | 394.80 | (no clean count) | - | - | - | - |
| 04-20 19:45 | 399.84 | (no clean count) | - | - | - | - |
| 04-23 20:30 | 421.20 | (no clean count) | - | - | - | - |
| 04-28 21:00 | 399.55 | (no clean count) | - | - | - | - |
| 05-01 21:30 | 420.10 | new impulse (up) | 38% | 438.31 | 394.65 | OPEN |
| 05-06 22:00 | 424.00 | (no clean count) | - | - | - | - |
| 05-11 22:45 | 429.00 | (no clean count) | - | - | - | - |
| 05-14 23:15 | 441.08 | new impulse (up) | 50% | 475.39 | 404.80 | OPEN |
| 05-19 23:45 | 411.99 | (no clean count) | - | - | - | - |
| 05-26 08:15 | 416.99 | (no clean count) | - | - | - | - |
| 05-29 08:45 | 431.68 | (no clean count) | - | - | - | - |
| 06-03 09:15 | 496.19 | new impulse (up) | 55% | 537.23 | 458.82 | OPEN |
| 06-08 09:45 | 392.32 | corrective A-B-C (up) | 67% | 427.73 | 499.12 | stale |
| 06-11 10:15 | 376.20 | corrective A-B-C (up) | 40% | 433.30 | 499.12 | stale |
