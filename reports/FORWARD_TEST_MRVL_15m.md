# Forward test (ghost-feeding) — MRVL 15m

_Simulated real time: at each of 9345 candles (2025-01-03 15:00 → 2026-06-11 18:15) the LIVE forecast is built from the prior 400 candles only, then the next 32 candles are ghost-fed to resolve it. Causal; not advice._

## Summary
- **STALE/unusable forecasts: 2500** of 9345 (27%) — the target was already on the wrong side of price because the count's confirmed pivot lags (intraday lag). These are EXCLUDED, not counted as instant wins.
- Usable forecasts resolved: **1718** (HIT 755 / INVALIDATED 963); OPEN 5022; no-forecast 105.
- **Target-hit rate among USABLE forecasts: 44%.**
- Next-candle directional accuracy: **51%** of 9240 (coin-flip = 50%).
- Snapshots (forecast vs realized): `charts/png/forward/mrvl_15m_step_1.png`, `charts/png/forward/mrvl_15m_step_2.png`, `charts/png/forward/mrvl_15m_step_3.png`, `charts/png/forward/mrvl_15m_step_4.png`, `charts/png/forward/mrvl_15m_step_5.png`, `charts/png/forward/mrvl_15m_step_6.png`

## Live forecast log (every 77th candle)
| time | price | forecast | conf | target | invalid | outcome |
|---|---|---|---|---|---|---|
| 01-03 15:00 | 115.78 | new impulse (up) | 63% | 123.41 | 109.78 | HIT (22) |
| 01-08 14:45 | 117.08 | new impulse (down) | 32% | 78.55 | 124.50 | OPEN |
| 01-14 14:30 | 116.13 | new impulse (up) | 58% | 124.43 | 111.07 | OPEN |
| 01-17 14:15 | 119.96 | new impulse (up) | 58% | 128.26 | 111.07 | OPEN |
| 01-23 14:00 | 123.35 | (no clean count) | - | - | - | - |
| 01-28 13:45 | 103.33 | new impulse (up) | 44% | 120.78 | 99.52 | OPEN |
| 01-31 13:30 | 111.78 | new impulse (up) | 53% | 129.23 | 99.52 | OPEN |
| 02-04 19:45 | 109.46 | new impulse (up) | 43% | 115.38 | 105.69 | HIT (11) |
| 02-07 19:30 | 111.19 | new impulse (up) | 51% | 117.44 | 105.69 | OPEN |
| 02-12 19:15 | 105.99 | new impulse (up) | 51% | 112.23 | 105.69 | INVALIDATED (3) |
| 02-18 19:00 | 107.36 | new impulse (up) | 29% | 111.78 | 100.22 | HIT (8) |
| 02-21 18:45 | 103.28 | new impulse (down) | 33% | 71.13 | 112.50 | OPEN |
| 02-26 18:30 | 94.57 | new impulse (up) | 65% | 107.41 | 91.73 | INVALIDATED (12) |
| 03-03 18:15 | 88.49 | corrective A-B-C (up) | 72% | 99.07 | 113.23 | stale |
| 03-06 18:00 | 73.78 | corrective A-B-C (up) | 61% | 80.39 | 112.50 | stale |
| 03-11 17:45 | 66.70 | new impulse (up) | 49% | 83.97 | 63.65 | OPEN |
| 03-14 17:30 | 68.99 | new impulse (up) | 50% | 86.26 | 63.65 | OPEN |
| 03-19 17:15 | 69.21 | new impulse (up) | 45% | 86.48 | 63.65 | OPEN |
| 03-24 17:00 | 72.41 | corrective A-B-C (up) | 50% | 75.04 | 91.59 | stale |
| 03-27 16:45 | 63.95 | new impulse (down) | 22% | 51.39 | 73.23 | OPEN |
| 04-01 16:30 | 61.45 | new impulse (up) | 58% | 70.10 | 59.24 | OPEN |
| 04-04 16:15 | 49.28 | corrective A-B-C (up) | 59% | 52.86 | 73.23 | stale |
| 04-09 16:00 | 51.08 | corrective A-B-C (up) | 67% | 52.77 | 73.23 | stale |
| 04-14 15:45 | 51.72 | corrective A-B-C (up) | 85% | 50.84 | 73.23 | stale |
| 04-17 15:30 | 51.48 | corrective A-B-C (up) | 85% | 51.08 | 66.87 | stale |
| 04-23 15:15 | 53.94 | new impulse (up) | 44% | 62.10 | 48.09 | OPEN |
| 04-28 15:00 | 58.16 | new impulse (up) | 40% | 66.33 | 48.09 | OPEN |
| 05-01 14:45 | 61.34 | new impulse (down) | 52% | 53.37 | 55.86 | stale |
| 05-06 14:30 | 61.07 | new impulse (down) | 52% | 41.25 | 63.43 | OPEN |
| 05-09 14:15 | 59.48 | new impulse (up) | 38% | 63.17 | 53.77 | HIT (23) |
| 05-14 14:00 | 65.79 | new impulse (up) | 27% | 71.76 | 53.77 | OPEN |
| 05-19 13:45 | 62.45 | new impulse (down) | 58% | 27.72 | 67.04 | OPEN |
| 05-22 13:30 | 60.65 | new impulse (up) | 51% | 65.12 | 59.80 | OPEN |
| 05-27 19:45 | 63.81 | new impulse (up) | 58% | 68.58 | 59.32 | OPEN |
| 05-30 19:30 | 59.74 | new impulse (down) | 57% | 38.09 | 67.59 | OPEN |
| 06-04 19:15 | 66.57 | new impulse (up) | 57% | 72.12 | 58.61 | OPEN |
| 06-09 19:00 | 69.58 | new impulse (up) | 58% | 75.13 | 58.61 | OPEN |
| 06-12 18:45 | 69.53 | new impulse (down) | 57% | 36.48 | 71.23 | OPEN |
| 06-17 18:30 | 70.25 | new impulse (up) | 53% | 75.10 | 66.97 | HIT (6) |
| 06-23 18:15 | 70.28 | new impulse (up) | 27% | 75.13 | 66.97 | HIT (32) |
| 06-26 18:00 | 79.88 | new impulse (up) | 57% | 85.11 | 69.18 | OPEN |
| 07-01 17:45 | 76.73 | new impulse (down) | 58% | 45.47 | 81.12 | OPEN |
| 07-07 17:30 | 72.13 | new impulse (down) | 65% | 67.53 | 79.09 | OPEN |
| 07-10 17:15 | 73.38 | new impulse (down) | 65% | 68.78 | 79.09 | OPEN |
| 07-15 17:00 | 72.66 | new impulse (up) | 35% | 77.98 | 70.48 | INVALIDATED (12) |
| 07-18 16:45 | 74.16 | corrective A-B-C (up) | 69% | 73.51 | 81.12 | stale |
| 07-23 16:30 | 73.25 | new impulse (up) | 45% | 78.88 | 70.30 | OPEN |
| 07-28 16:15 | 75.12 | new impulse (up) | 58% | 80.75 | 70.30 | OPEN |
| 07-31 16:00 | 81.81 | new impulse (down) | 35% | 42.62 | 85.27 | OPEN |
| 08-05 15:45 | 75.79 | new impulse (down) | 39% | 68.91 | 73.42 | stale |
| 08-08 15:30 | 76.51 | new impulse (up) | 46% | 82.49 | 78.00 | stale |
| 08-13 15:15 | 79.32 | new impulse (up) | 38% | 81.88 | 74.84 | OPEN |
| 08-18 15:00 | 76.00 | new impulse (down) | 33% | 60.08 | 80.06 | OPEN |
| 08-21 14:45 | 71.28 | new impulse (up) | 40% | 78.40 | 68.54 | OPEN |
| 08-26 14:30 | 74.07 | new impulse (up) | 65% | 77.96 | 68.54 | OPEN |
| 08-29 14:15 | 64.55 | new impulse (up) | 58% | 79.99 | 78.08 | stale |
| 09-04 14:00 | 62.16 | new impulse (up) | 56% | 72.22 | 61.81 | OPEN |
| 09-09 13:45 | 65.81 | new impulse (up) | 58% | 76.10 | 61.44 | OPEN |
| 09-12 13:30 | 66.86 | new impulse (up) | 37% | 69.46 | 61.44 | OPEN |
| 09-16 19:45 | 68.83 | new impulse (up) | 37% | 71.43 | 61.44 | HIT (4) |
| 09-19 19:30 | 73.95 | new impulse (up) | 37% | 76.55 | 61.44 | OPEN |
| 09-24 19:15 | 80.53 | (no clean count) | - | - | - | - |
| 09-29 19:00 | 82.81 | new impulse (up) | 49% | 88.94 | 76.32 | OPEN |
| 10-02 18:45 | 86.56 | new impulse (up) | 24% | 87.09 | 81.35 | HIT (11) |
| 10-07 18:30 | 86.78 | new impulse (down) | 60% | 61.80 | 90.89 | INVALIDATED (15) |
| 10-10 18:15 | 87.75 | corrective A-B-C (down) | 94% | 85.76 | 76.32 | stale |
| 10-15 18:00 | 88.38 | new impulse (down) | 43% | 81.86 | 89.87 | INVALIDATED (8) |
| 10-20 17:45 | 86.11 | new impulse (down) | 33% | 70.82 | 91.20 | OPEN |
| 10-23 17:30 | 83.34 | new impulse (up) | 29% | 90.84 | 79.06 | OPEN |
| 10-28 17:15 | 88.75 | new impulse (up) | 52% | 95.43 | 79.06 | OPEN |
| 10-31 17:00 | 91.94 | new impulse (down) | 39% | 43.48 | 97.57 | INVALIDATED (14) |
| 11-05 16:45 | 93.14 | new impulse (up) | 46% | 99.67 | 87.00 | HIT (13) |
| 11-10 16:30 | 92.75 | new impulse (up) | 33% | 102.11 | 85.11 | OPEN |
| 11-13 16:15 | 86.96 | new impulse (up) | 26% | 101.04 | 94.47 | stale |
| 11-18 16:00 | 79.73 | new impulse (up) | 25% | 95.21 | 89.00 | stale |
| 11-21 15:45 | 75.39 | new impulse (up) | 37% | 88.15 | 84.53 | stale |
| 11-26 15:30 | 86.65 | corrective A-B-C (up) | 53% | 84.16 | 100.25 | stale |
| 12-02 15:15 | 92.86 | new impulse (up) | 26% | 99.33 | 88.30 | HIT (19) |
| 12-05 15:00 | 99.75 | corrective A-B-C (down) | 85% | 95.84 | 73.62 | stale |
| 12-10 14:45 | 91.69 | corrective A-B-C (down) | 85% | 95.84 | 73.62 | stale |
| 12-15 14:30 | 85.02 | corrective A-B-C (down) | 85% | 95.84 | 73.62 | stale |
| 12-18 14:15 | 84.50 | new impulse (up) | 18% | 96.96 | 88.62 | stale |
| 12-23 14:00 | 84.35 | corrective A-B-C (up) | 59% | 86.73 | 102.77 | stale |
| 12-29 14:15 | 85.30 | new impulse (up) | 52% | 91.48 | 81.77 | OPEN |
| 01-02 14:00 | 86.83 | new impulse (up) | 62% | 93.01 | 81.77 | HIT (27) |
| 01-07 13:45 | 86.90 | new impulse (down) | 55% | 70.98 | 94.20 | OPEN |
| 01-12 13:30 | 82.15 | new impulse (up) | 46% | 94.77 | 88.12 | stale |
| 01-14 19:45 | 79.52 | new impulse (up) | 46% | 94.77 | 88.12 | stale |
| 01-20 19:30 | 79.61 | new impulse (up) | 64% | 85.20 | 78.57 | HIT (32) |
| 01-23 19:15 | 80.20 | new impulse (up) | 57% | 90.82 | 85.35 | stale |
| 01-28 19:00 | 83.39 | new impulse (up) | 36% | 90.11 | 79.43 | INVALIDATED (12) |
| 02-02 18:45 | 78.74 | new impulse (down) | 35% | 62.92 | 85.47 | OPEN |
| 02-05 18:30 | 73.98 | new impulse (up) | 65% | 79.38 | 70.69 | HIT (17) |
| 02-10 18:15 | 82.46 | new impulse (up) | 58% | 91.60 | 70.69 | OPEN |
| 02-13 18:00 | 79.61 | corrective A-B-C (up) | 44% | 76.19 | 85.47 | stale |
| 02-19 18:00 | 78.72 | new impulse (up) | 58% | 83.21 | 76.51 | OPEN |
| 02-24 17:45 | 79.30 | new impulse (down) | 46% | 73.67 | 80.40 | INVALIDATED (15) |
| 02-27 17:30 | 79.79 | new impulse (up) | 44% | 82.42 | 77.15 | HIT (25) |
| 03-04 17:15 | 78.79 | new impulse (up) | 29% | 83.71 | 76.07 | INVALIDATED (28) |
| 03-09 17:00 | 89.97 | new impulse (up) | 56% | 95.66 | 84.20 | OPEN |
| 03-12 16:45 | 88.99 | new impulse (down) | 52% | 60.58 | 95.05 | OPEN |
| 03-17 16:30 | 91.15 | new impulse (down) | 65% | 83.42 | 86.82 | stale |
| 03-20 16:15 | 89.55 | new impulse (up) | 29% | 95.68 | 85.13 | OPEN |
| 03-25 16:00 | 97.53 | new impulse (up) | 29% | 100.05 | 85.13 | HIT (16) |
| 03-30 15:45 | 90.10 | new impulse (down) | 43% | 84.68 | 96.50 | INVALIDATED (17) |
| 04-02 15:30 | 106.47 | new impulse (down) | 65% | 94.44 | 101.13 | stale |
| 04-08 15:15 | 113.89 | corrective A-B-C (down) | 50% | 101.40 | 85.13 | stale |
| 04-13 15:00 | 131.60 | new impulse (up) | 29% | 136.36 | 106.00 | HIT (20) |
| 04-16 14:45 | 132.28 | new impulse (down) | 52% | 48.01 | 138.19 | INVALIDATED (27) |
| 04-21 14:30 | 151.91 | new impulse (down) | 43% | 69.72 | 128.42 | stale |
| 04-24 14:15 | 162.28 | corrective A-B-C (down) | 85% | 128.09 | 101.13 | stale |
| 04-29 14:00 | 151.74 | new impulse (up) | 38% | 166.56 | 146.85 | OPEN |
| 05-04 13:45 | 166.01 | new impulse (up) | 38% | 180.84 | 146.85 | OPEN |
| 05-07 13:30 | 164.26 | new impulse (down) | 43% | 88.47 | 175.80 | OPEN |
| 05-11 19:45 | 170.85 | new impulse (up) | 38% | 181.51 | 158.55 | INVALIDATED (13) |
| 05-14 19:30 | 183.81 | new impulse (down) | 64% | 136.71 | 192.15 | OPEN |
| 05-19 19:15 | 177.12 | new impulse (up) | 65% | 184.17 | 164.74 | HIT (3) |
| 05-22 19:00 | 195.25 | corrective A-B-C (down) | 45% | 181.05 | 157.96 | stale |
| 05-28 18:45 | 202.83 | corrective A-B-C (down) | 45% | 202.03 | 157.96 | stale |
| 06-02 18:30 | 282.21 | corrective A-B-C (down) | 36% | 183.42 | 157.96 | stale |
| 06-05 18:15 | 275.02 | new impulse (up) | 49% | 306.38 | 277.56 | stale |
| 06-10 18:00 | 261.01 | corrective A-B-C (down) | 60% | 222.41 | 194.70 | stale |
