# Forward test (ghost-feeding) — AVGO 15m

_Simulated real time: at each of 9344 candles (2025-01-03 16:00 → 2026-06-11 18:15) the LIVE forecast is built from the prior 400 candles only, then the next 32 candles are ghost-fed to resolve it. Causal; not advice._

## Summary
- **STALE/unusable forecasts: 1500** of 9344 (16%) — the target was already on the wrong side of price because the count's confirmed pivot lags (intraday lag). These are EXCLUDED, not counted as instant wins.
- Usable forecasts resolved: **1367** (HIT 558 / INVALIDATED 809); OPEN 5377; no-forecast 1100.
- **Target-hit rate among USABLE forecasts: 41%.**
- Next-candle directional accuracy: **50%** of 8244 (coin-flip = 50%).
- Snapshots (forecast vs realized): `charts/png/forward/avgo_15m_step_1.png`, `charts/png/forward/avgo_15m_step_2.png`, `charts/png/forward/avgo_15m_step_3.png`, `charts/png/forward/avgo_15m_step_4.png`, `charts/png/forward/avgo_15m_step_5.png`, `charts/png/forward/avgo_15m_step_6.png`

## Live forecast log (every 77th candle)
| time | price | forecast | conf | target | invalid | outcome |
|---|---|---|---|---|---|---|
| 01-03 16:00 | 231.60 | new impulse (down) | 61% | 146.83 | 247.47 | OPEN |
| 01-08 15:45 | 229.12 | new impulse (up) | 35% | 247.26 | 241.75 | stale |
| 01-14 15:30 | 227.69 | new impulse (up) | 39% | 236.55 | 218.05 | OPEN |
| 01-17 15:15 | 233.81 | new impulse (up) | 40% | 248.46 | 218.05 | OPEN |
| 01-23 15:00 | 238.51 | new impulse (up) | 57% | 253.16 | 218.05 | OPEN |
| 01-28 14:45 | 202.70 | new impulse (up) | 46% | 234.63 | 210.42 | stale |
| 01-31 14:30 | 217.18 | new impulse (up) | 48% | 226.51 | 198.89 | HIT (8) |
| 02-05 14:15 | 233.80 | new impulse (up) | 65% | 249.70 | 212.80 | OPEN |
| 02-10 14:00 | 228.26 | corrective A-B-C (down) | 36% | 213.30 | 198.89 | stale |
| 02-13 13:45 | 235.27 | new impulse (up) | 65% | 250.41 | 224.60 | OPEN |
| 02-19 13:30 | 226.29 | new impulse (down) | 52% | 211.19 | 237.89 | OPEN |
| 02-21 19:45 | 217.96 | new impulse (down) | 57% | 202.86 | 237.89 | OPEN |
| 02-26 19:30 | 210.70 | new impulse (up) | 47% | 233.55 | 200.92 | INVALIDATED (28) |
| 03-03 19:15 | 190.30 | new impulse (up) | 65% | 221.18 | 205.08 | stale |
| 03-06 19:00 | 180.59 | corrective A-B-C (up) | 85% | 192.19 | 236.95 | stale |
| 03-11 18:45 | 194.42 | corrective A-B-C (up) | 85% | 195.75 | 229.46 | stale |
| 03-14 18:30 | 194.92 | corrective A-B-C (up) | 85% | 194.61 | 223.50 | stale |
| 03-19 18:15 | 194.30 | new impulse (up) | 49% | 210.66 | 180.43 | OPEN |
| 03-24 18:00 | 191.95 | new impulse (up) | 26% | 200.71 | 198.27 | stale |
| 03-27 17:45 | 171.72 | new impulse (down) | 26% | 127.97 | 198.27 | OPEN |
| 04-01 17:30 | 167.46 | new impulse (up) | 53% | 190.73 | 160.62 | OPEN |
| 04-04 17:15 | 142.45 | new impulse (up) | 63% | 163.62 | 139.17 | INVALIDATED (11) |
| 04-09 17:00 | 163.38 | corrective A-B-C (up) | 85% | 151.89 | 198.27 | stale |
| 04-14 16:45 | 176.62 | corrective A-B-C (up) | 85% | 151.60 | 195.58 | stale |
| 04-17 16:30 | 171.67 | corrective A-B-C (down) | 44% | 162.01 | 138.10 | stale |
| 04-23 16:15 | 178.03 | corrective A-B-C (down) | 44% | 162.01 | 138.10 | stale |
| 04-28 16:00 | 188.05 | corrective A-B-C (down) | 39% | 162.01 | 138.10 | stale |
| 05-01 15:45 | 197.79 | new impulse (up) | 51% | 212.86 | 161.61 | OPEN |
| 05-06 15:30 | 200.37 | new impulse (up) | 65% | 217.00 | 161.61 | OPEN |
| 05-09 15:15 | 207.98 | new impulse (up) | 56% | 215.86 | 195.94 | HIT (19) |
| 05-14 15:00 | 232.85 | new impulse (down) | 45% | 148.97 | 205.68 | stale |
| 05-19 14:45 | 228.54 | new impulse (down) | 54% | 125.55 | 235.28 | OPEN |
| 05-22 14:30 | 231.56 | new impulse (up) | 58% | 247.11 | 221.60 | OPEN |
| 05-28 14:15 | 235.18 | new impulse (down) | 57% | 218.25 | 236.50 | INVALIDATED (7) |
| 06-02 14:00 | 247.90 | new impulse (down) | 38% | 219.57 | 236.50 | stale |
| 06-05 13:45 | 261.22 | new impulse (up) | 52% | 270.26 | 234.90 | OPEN |
| 06-10 13:30 | 244.59 | new impulse (down) | 53% | 164.67 | 265.43 | OPEN |
| 06-12 19:45 | 256.13 | new impulse (up) | 52% | 271.16 | 241.11 | OPEN |
| 06-17 19:30 | 251.25 | new impulse (up) | 52% | 266.28 | 241.11 | OPEN |
| 06-23 19:15 | 253.80 | new impulse (up) | 39% | 264.90 | 244.17 | HIT (3) |
| 06-26 19:00 | 269.99 | new impulse (up) | 39% | 281.09 | 244.17 | OPEN |
| 07-01 18:45 | 263.96 | (no clean count) | - | - | - | - |
| 07-07 18:30 | 273.77 | new impulse (up) | 49% | 290.87 | 262.66 | OPEN |
| 07-10 18:15 | 275.09 | new impulse (up) | 57% | 292.19 | 262.66 | OPEN |
| 07-15 18:00 | 281.95 | new impulse (up) | 35% | 291.34 | 269.58 | OPEN |
| 07-18 17:45 | 283.60 | new impulse (up) | 52% | 292.98 | 269.58 | OPEN |
| 07-23 17:30 | 279.00 | (no clean count) | - | - | - | - |
| 07-28 17:15 | 293.62 | new impulse (up) | 56% | 313.54 | 273.00 | OPEN |
| 07-31 17:00 | 295.65 | (no clean count) | - | - | - | - |
| 08-05 16:45 | 293.50 | new impulse (up) | 56% | 309.15 | 281.61 | OPEN |
| 08-08 16:30 | 303.66 | new impulse (up) | 56% | 319.32 | 281.61 | OPEN |
| 08-13 16:15 | 308.91 | (no clean count) | - | - | - | - |
| 08-18 16:00 | 302.55 | (no clean count) | - | - | - | - |
| 08-21 15:45 | 288.43 | (no clean count) | - | - | - | - |
| 08-26 15:30 | 298.04 | (no clean count) | - | - | - | - |
| 08-29 15:15 | 296.35 | (no clean count) | - | - | - | - |
| 09-04 15:00 | 304.47 | new impulse (up) | 56% | 331.54 | 287.17 | HIT (20) |
| 09-09 14:45 | 341.00 | new impulse (up) | 44% | 369.39 | 331.42 | HIT (24) |
| 09-12 14:30 | 359.69 | new impulse (up) | 46% | 383.07 | 335.83 | OPEN |
| 09-17 14:15 | 349.15 | new impulse (down) | 37% | 248.62 | 374.23 | OPEN |
| 09-22 14:00 | 343.10 | new impulse (down) | 37% | 242.56 | 374.23 | OPEN |
| 09-25 13:45 | 329.30 | new impulse (down) | 37% | 228.76 | 374.23 | OPEN |
| 09-30 13:30 | 328.62 | new impulse (up) | 46% | 357.63 | 327.30 | INVALIDATED (1) |
| 10-02 19:45 | 338.20 | new impulse (up) | 56% | 351.59 | 324.50 | OPEN |
| 10-07 19:30 | 335.79 | new impulse (up) | 55% | 349.18 | 324.50 | OPEN |
| 10-10 19:15 | 326.32 | new impulse (down) | 35% | 263.44 | 350.60 | INVALIDATED (3) |
| 10-15 19:00 | 352.78 | new impulse (up) | 39% | 363.33 | 339.65 | OPEN |
| 10-20 18:45 | 349.33 | new impulse (down) | 58% | 287.58 | 363.24 | OPEN |
| 10-23 18:30 | 344.76 | new impulse (down) | 46% | 283.01 | 363.24 | OPEN |
| 10-28 18:15 | 371.94 | new impulse (up) | 39% | 403.44 | 335.51 | OPEN |
| 10-31 18:00 | 369.62 | new impulse (down) | 35% | 236.18 | 386.48 | OPEN |
| 11-05 17:45 | 361.74 | new impulse (up) | 22% | 369.06 | 350.09 | OPEN |
| 11-10 17:30 | 357.52 | new impulse (up) | 57% | 387.93 | 337.27 | OPEN |
| 11-13 17:15 | 338.98 | new impulse (up) | 41% | 356.04 | 337.27 | INVALIDATED (3) |
| 11-18 17:00 | 345.47 | new impulse (up) | 61% | 365.76 | 329.06 | OPEN |
| 11-21 16:45 | 343.53 | new impulse (down) | 34% | 237.32 | 376.08 | OPEN |
| 11-26 16:30 | 394.53 | new impulse (up) | 29% | 420.94 | 371.75 | OPEN |
| 12-02 16:15 | 382.16 | new impulse (down) | 62% | 296.81 | 404.35 | OPEN |
| 12-05 16:00 | 385.70 | new impulse (up) | 29% | 413.36 | 370.65 | OPEN |
| 12-10 15:45 | 400.96 | new impulse (up) | 46% | 428.63 | 370.65 | OPEN |
| 12-15 15:30 | 345.57 | new impulse (down) | 43% | 239.28 | 411.25 | OPEN |
| 12-18 15:15 | 327.79 | new impulse (up) | 56% | 383.30 | 321.42 | OPEN |
| 12-23 15:00 | 339.45 | new impulse (up) | 53% | 394.96 | 321.42 | OPEN |
| 12-29 14:45 | 347.07 | (no clean count) | - | - | - | - |
| 01-02 14:30 | 358.28 | (no clean count) | - | - | - | - |
| 01-07 14:15 | 341.71 | new impulse (down) | 45% | 320.92 | 355.03 | OPEN |
| 01-12 14:00 | 340.36 | new impulse (up) | 49% | 362.17 | 330.50 | OPEN |
| 01-15 13:45 | 349.50 | new impulse (up) | 49% | 361.86 | 334.42 | OPEN |
| 01-21 13:30 | 333.33 | new impulse (up) | 36% | 360.29 | 353.23 | stale |
| 01-23 19:45 | 319.17 | new impulse (up) | 36% | 360.29 | 353.23 | stale |
| 01-28 19:30 | 330.10 | new impulse (up) | 35% | 353.17 | 314.11 | OPEN |
| 02-02 19:15 | 333.48 | new impulse (up) | 51% | 355.87 | 320.28 | INVALIDATED (10) |
| 02-05 19:00 | 317.02 | new impulse (up) | 43% | 335.50 | 309.00 | OPEN |
| 02-10 18:45 | 342.95 | new impulse (up) | 32% | 352.08 | 309.00 | OPEN |
| 02-13 18:30 | 327.48 | new impulse (up) | 32% | 354.43 | 295.30 | OPEN |
| 02-19 18:15 | 335.76 | new impulse (up) | 39% | 358.03 | 316.31 | OPEN |
| 02-24 18:00 | 324.87 | new impulse (up) | 39% | 350.00 | 340.11 | stale |
| 02-27 17:45 | 318.60 | new impulse (down) | 28% | 262.42 | 335.91 | OPEN |
| 03-04 17:30 | 320.29 | new impulse (up) | 63% | 338.03 | 307.20 | OPEN |
| 03-09 17:15 | 341.78 | new impulse (up) | 38% | 364.38 | 323.61 | OPEN |
| 03-12 17:00 | 338.09 | new impulse (down) | 35% | 260.78 | 353.14 | OPEN |
| 03-17 16:45 | 320.37 | new impulse (down) | 56% | 243.06 | 353.14 | OPEN |
| 03-20 16:30 | 317.46 | (no clean count) | - | - | - | - |
| 03-25 16:15 | 319.60 | new impulse (up) | 53% | 347.18 | 308.51 | OPEN |
| 03-30 16:00 | 294.93 | new impulse (up) | 40% | 320.72 | 309.92 | stale |
| 04-02 15:45 | 312.69 | new impulse (up) | 65% | 335.26 | 289.96 | OPEN |
| 04-08 15:30 | 349.04 | new impulse (up) | 58% | 371.61 | 289.96 | OPEN |
| 04-13 15:15 | 374.03 | new impulse (up) | 36% | 385.39 | 301.75 | OPEN |
| 04-16 15:00 | 398.62 | new impulse (up) | 35% | 409.98 | 301.75 | OPEN |
| 04-21 14:45 | 398.84 | new impulse (up) | 50% | 410.20 | 301.75 | HIT (24) |
| 04-24 14:30 | 415.60 | (no clean count) | - | - | - | - |
| 04-29 14:15 | 401.39 | (no clean count) | - | - | - | - |
| 05-04 14:00 | 420.53 | (no clean count) | - | - | - | - |
| 05-07 13:45 | 417.00 | (no clean count) | - | - | - | - |
| 05-12 13:30 | 427.08 | new impulse (up) | 54% | 462.73 | 406.30 | INVALIDATED (27) |
| 05-14 19:45 | 439.69 | new impulse (up) | 39% | 474.00 | 404.80 | OPEN |
| 05-19 19:30 | 411.26 | new impulse (down) | 49% | 312.93 | 442.36 | OPEN |
| 05-22 19:15 | 412.40 | new impulse (up) | 50% | 434.96 | 405.86 | HIT (7) |
| 05-28 19:00 | 428.12 | new impulse (up) | 57% | 450.68 | 405.86 | HIT (30) |
| 06-02 18:45 | 473.40 | new impulse (up) | 55% | 514.86 | 405.86 | INVALIDATED (31) |
| 06-05 18:30 | 389.04 | new impulse (down) | 46% | 362.38 | 426.48 | OPEN |
| 06-10 18:15 | 378.25 | corrective A-B-C (up) | 39% | 395.20 | 495.00 | stale |
