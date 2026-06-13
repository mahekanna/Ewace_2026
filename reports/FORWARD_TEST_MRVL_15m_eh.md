# Forward test (ghost-feeding) — MRVL 15m_eh

_Simulated real time: at each of 22903 candles (2024-12-19 10:15 → 2026-06-12 15:45) the LIVE forecast is built from the prior 400 candles only, then the next 32 candles are ghost-fed to resolve it. Causal; not advice._

## Summary
- **STALE/unusable forecasts: 4100** of 22903 (18%) — the target was already on the wrong side of price because the count's confirmed pivot lags (intraday lag). These are EXCLUDED, not counted as instant wins.
- Usable forecasts resolved: **2041** (HIT 891 / INVALIDATED 1150); OPEN 10662; no-forecast 6100.
- **Target-hit rate among USABLE forecasts: 44%.**
- Next-candle directional accuracy: **51%** of 16803 (coin-flip = 50%).
- Snapshots (forecast vs realized): `charts/png/forward/mrvl_15m_eh_step_1.png`, `charts/png/forward/mrvl_15m_eh_step_2.png`, `charts/png/forward/mrvl_15m_eh_step_3.png`, `charts/png/forward/mrvl_15m_eh_step_4.png`, `charts/png/forward/mrvl_15m_eh_step_5.png`, `charts/png/forward/mrvl_15m_eh_step_6.png`

## Live forecast log (every 190th candle)
| time | price | forecast | conf | target | invalid | outcome |
|---|---|---|---|---|---|---|
| 12-19 10:15 | 107.33 | new impulse (up) | 46% | 123.60 | 119.13 | stale |
| 12-24 11:00 | 114.62 | new impulse (down) | 44% | 102.91 | 110.38 | stale |
| 12-30 18:00 | 113.02 | (no clean count) | - | - | - | - |
| 01-06 09:15 | 120.14 | (no clean count) | - | - | - | - |
| 01-10 13:30 | 116.63 | (no clean count) | - | - | - | - |
| 01-15 19:15 | 116.34 | new impulse (up) | 65% | 125.39 | 110.50 | OPEN |
| 01-21 20:30 | 124.28 | (no clean count) | - | - | - | - |
| 01-24 23:15 | 124.00 | new impulse (up) | 51% | 128.93 | 121.73 | INVALIDATED (7) |
| 01-29 22:45 | 111.34 | new impulse (up) | 52% | 120.12 | 103.11 | OPEN |
| 02-03 23:00 | 115.22 | new impulse (up) | 51% | 130.55 | 99.52 | OPEN |
| 02-07 00:00 | 122.96 | new impulse (up) | 55% | 129.19 | 105.69 | OPEN |
| 02-12 00:00 | 109.15 | (no clean count) | - | - | - | - |
| 02-18 09:15 | 107.45 | (no clean count) | - | - | - | - |
| 02-21 15:30 | 107.26 | (no clean count) | - | - | - | - |
| 02-26 17:45 | 94.62 | (no clean count) | - | - | - | - |
| 03-03 18:00 | 88.66 | new impulse (up) | 47% | 97.65 | 93.97 | stale |
| 03-06 17:45 | 74.21 | new impulse (up) | 45% | 85.16 | 74.38 | stale |
| 03-11 16:30 | 66.54 | new impulse (up) | 50% | 76.71 | 63.65 | OPEN |
| 03-14 16:45 | 69.18 | corrective A-B-C (up) | 78% | 71.02 | 78.40 | stale |
| 03-19 18:00 | 69.79 | new impulse (up) | 36% | 74.25 | 67.65 | OPEN |
| 03-24 20:15 | 72.76 | new impulse (up) | 58% | 75.13 | 68.44 | OPEN |
| 03-27 22:45 | 64.83 | (no clean count) | - | - | - | - |
| 04-02 08:30 | 62.40 | (no clean count) | - | - | - | - |
| 04-07 09:45 | 46.71 | corrective A-B-C (up) | 44% | 56.94 | 65.44 | stale |
| 04-10 09:30 | 58.81 | corrective A-B-C (up) | 80% | 48.48 | 64.95 | stale |
| 04-15 09:00 | 52.71 | corrective A-B-C (down) | 40% | 52.56 | 44.00 | stale |
| 04-21 11:00 | 50.83 | corrective A-B-C (up) | 36% | 54.17 | 61.50 | stale |
| 04-24 11:30 | 53.84 | new impulse (down) | 42% | 33.26 | 55.95 | INVALIDATED (8) |
| 04-29 12:45 | 58.45 | new impulse (up) | 57% | 60.97 | 52.84 | OPEN |
| 05-02 13:30 | 62.91 | new impulse (up) | 51% | 67.33 | 55.86 | OPEN |
| 05-07 14:45 | 54.57 | new impulse (down) | 26% | 50.61 | 59.00 | OPEN |
| 05-12 14:15 | 63.91 | new impulse (up) | 25% | 66.58 | 62.20 | OPEN |
| 05-15 14:45 | 64.46 | new impulse (up) | 58% | 67.13 | 62.20 | OPEN |
| 05-20 15:30 | 60.65 | (no clean count) | - | - | - | - |
| 05-23 16:45 | 60.38 | new impulse (up) | 50% | 64.86 | 58.50 | OPEN |
| 05-29 16:30 | 64.04 | new impulse (down) | 35% | 39.03 | 69.22 | OPEN |
| 06-03 17:00 | 63.09 | new impulse (up) | 37% | 66.96 | 58.61 | OPEN |
| 06-06 16:30 | 69.39 | new impulse (up) | 64% | 70.99 | 63.22 | OPEN |
| 06-11 16:30 | 68.84 | (no clean count) | - | - | - | - |
| 06-16 16:45 | 70.59 | new impulse (up) | 35% | 73.23 | 66.80 | OPEN |
| 06-20 16:30 | 74.30 | corrective A-B-C (down) | 79% | 71.44 | 66.80 | stale |
| 06-25 16:00 | 75.02 | new impulse (up) | 51% | 80.05 | 69.18 | OPEN |
| 06-30 15:30 | 77.13 | new impulse (up) | 56% | 82.48 | 76.41 | OPEN |
| 07-03 15:45 | 75.02 | new impulse (down) | 47% | 70.42 | 79.09 | OPEN |
| 07-09 18:45 | 72.50 | (no clean count) | - | - | - | - |
| 07-14 18:45 | 72.72 | (no clean count) | - | - | - | - |
| 07-17 18:45 | 72.41 | new impulse (up) | 51% | 76.51 | 68.00 | OPEN |
| 07-22 19:00 | 72.34 | (no clean count) | - | - | - | - |
| 07-25 19:45 | 74.22 | (no clean count) | - | - | - | - |
| 07-30 19:45 | 81.77 | (no clean count) | - | - | - | - |
| 08-04 19:30 | 76.71 | new impulse (up) | 40% | 83.18 | 73.52 | OPEN |
| 08-07 20:30 | 75.85 | new impulse (up) | 50% | 79.10 | 73.98 | OPEN |
| 08-12 22:15 | 77.80 | new impulse (up) | 58% | 83.67 | 74.84 | OPEN |
| 08-18 08:30 | 76.32 | (no clean count) | - | - | - | - |
| 08-21 10:45 | 71.22 | (no clean count) | - | - | - | - |
| 08-26 12:45 | 73.01 | (no clean count) | - | - | - | - |
| 08-29 13:15 | 64.52 | new impulse (up) | 51% | 70.48 | 65.42 | stale |
| 09-04 12:45 | 62.51 | new impulse (up) | 62% | 67.50 | 60.88 | OPEN |
| 09-09 12:15 | 65.87 | new impulse (up) | 61% | 68.66 | 61.44 | OPEN |
| 09-12 12:00 | 67.70 | (no clean count) | - | - | - | - |
| 09-17 12:45 | 68.58 | (no clean count) | - | - | - | - |
| 09-22 12:45 | 73.41 | (no clean count) | - | - | - | - |
| 09-25 13:15 | 77.99 | (no clean count) | - | - | - | - |
| 09-30 13:15 | 81.70 | new impulse (down) | 51% | 58.74 | 85.09 | OPEN |
| 10-03 12:45 | 86.20 | new impulse (up) | 51% | 89.48 | 81.03 | OPEN |
| 10-08 13:30 | 88.94 | (no clean count) | - | - | - | - |
| 10-13 13:30 | 88.33 | new impulse (up) | 56% | 95.51 | 83.14 | OPEN |
| 10-16 14:15 | 90.23 | new impulse (up) | 64% | 94.01 | 85.33 | OPEN |
| 10-21 16:00 | 84.71 | new impulse (up) | 57% | 91.12 | 88.95 | stale |
| 10-24 17:15 | 85.57 | new impulse (up) | 38% | 91.68 | 79.06 | OPEN |
| 10-29 19:00 | 90.38 | (no clean count) | - | - | - | - |
| 11-03 22:00 | 90.69 | new impulse (up) | 52% | 97.86 | 91.16 | stale |
| 11-06 23:00 | 93.51 | new impulse (up) | 38% | 103.68 | 85.55 | OPEN |
| 11-12 00:45 | 89.99 | new impulse (up) | 58% | 101.79 | 85.11 | OPEN |
| 11-17 11:15 | 86.75 | new impulse (up) | 58% | 93.63 | 83.33 | INVALIDATED (30) |
| 11-20 11:45 | 83.81 | new impulse (up) | 65% | 90.74 | 77.78 | INVALIDATED (27) |
| 11-25 13:45 | 82.59 | new impulse (up) | 58% | 90.10 | 73.62 | OPEN |
| 12-01 20:15 | 91.91 | new impulse (up) | 45% | 98.38 | 88.30 | OPEN |
| 12-04 20:15 | 97.66 | new impulse (down) | 32% | 79.39 | 102.77 | OPEN |
| 12-09 20:15 | 88.18 | new impulse (down) | 37% | 84.03 | 98.66 | OPEN |
| 12-12 21:30 | 84.53 | new impulse (up) | 65% | 99.45 | 92.85 | stale |
| 12-17 22:30 | 82.27 | (no clean count) | - | - | - | - |
| 12-22 23:45 | 84.99 | new impulse (up) | 50% | 91.84 | 81.18 | OPEN |
| 12-29 17:00 | 84.92 | (no clean count) | - | - | - | - |
| 01-02 21:45 | 89.37 | (no clean count) | - | - | - | - |
| 01-07 21:45 | 84.72 | new impulse (up) | 57% | 94.95 | 88.71 | stale |
| 01-12 21:45 | 82.97 | new impulse (up) | 57% | 94.95 | 88.71 | stale |
| 01-15 23:00 | 80.74 | (no clean count) | - | - | - | - |
| 01-21 23:30 | 83.30 | new impulse (up) | 57% | 90.55 | 77.11 | OPEN |
| 01-26 23:15 | 81.77 | new impulse (up) | 58% | 88.50 | 79.43 | OPEN |
| 01-29 23:30 | 81.34 | new impulse (up) | 52% | 85.77 | 78.30 | OPEN |
| 02-04 00:15 | 75.00 | new impulse (up) | 45% | 79.21 | 72.79 | OPEN |
| 02-09 09:15 | 80.13 | new impulse (up) | 51% | 83.53 | 73.86 | OPEN |
| 02-12 14:30 | 80.01 | new impulse (down) | 63% | 65.04 | 83.78 | OPEN |
| 02-18 18:15 | 80.28 | new impulse (up) | 35% | 87.09 | 76.51 | OPEN |
| 02-24 09:45 | 78.19 | (no clean count) | - | - | - | - |
| 02-27 13:30 | 79.00 | (no clean count) | - | - | - | - |
| 03-04 13:00 | 78.71 | new impulse (down) | 35% | 73.01 | 82.82 | OPEN |
| 03-09 11:30 | 87.41 | new impulse (down) | 58% | 59.08 | 93.40 | OPEN |
| 03-12 11:45 | 89.75 | corrective A-B-C (down) | 82% | 88.25 | 75.24 | stale |
| 03-17 13:00 | 92.28 | new impulse (up) | 58% | 97.37 | 86.82 | OPEN |
| 03-20 14:15 | 88.27 | new impulse (up) | 49% | 93.41 | 85.13 | OPEN |
| 03-25 14:30 | 96.69 | new impulse (up) | 40% | 100.63 | 85.62 | OPEN |
| 03-30 14:30 | 89.54 | new impulse (up) | 46% | 99.86 | 96.50 | stale |
| 04-02 14:00 | 104.47 | new impulse (down) | 45% | 96.95 | 106.44 | INVALIDATED (2) |
| 04-08 13:30 | 111.93 | corrective A-B-C (down) | 48% | 101.52 | 86.58 | stale |
| 04-13 13:00 | 132.65 | new impulse (up) | 45% | 138.40 | 110.45 | OPEN |
| 04-16 12:30 | 133.75 | new impulse (up) | 57% | 143.97 | 130.00 | INVALIDATED (4) |
| 04-21 12:00 | 151.25 | new impulse (up) | 56% | 162.35 | 128.42 | OPEN |
| 04-24 11:30 | 172.78 | new impulse (up) | 34% | 178.65 | 143.93 | OPEN |
| 04-29 11:00 | 157.23 | new impulse (up) | 64% | 168.01 | 146.00 | OPEN |
| 05-04 10:45 | 166.00 | new impulse (up) | 64% | 176.78 | 146.00 | OPEN |
| 05-07 10:15 | 170.66 | new impulse (up) | 51% | 182.93 | 165.00 | INVALIDATED (13) |
| 05-12 09:45 | 167.43 | new impulse (down) | 25% | 136.62 | 174.16 | OPEN |
| 05-15 09:15 | 173.31 | corrective A-B-C (down) | 81% | 176.19 | 157.96 | stale |
| 05-20 08:45 | 184.77 | corrective A-B-C (down) | 81% | 176.19 | 157.96 | stale |
| 05-26 08:15 | 203.88 | corrective A-B-C (down) | 67% | 181.36 | 162.64 | stale |
| 05-28 23:45 | 203.20 | corrective A-B-C (down) | 70% | 198.91 | 182.73 | stale |
| 06-02 23:15 | 316.00 | new impulse (up) | 39% | 355.03 | 219.98 | OPEN |
| 06-05 22:45 | 273.44 | new impulse (up) | 39% | 287.11 | 253.00 | HIT (17) |
| 06-10 22:15 | 245.10 | corrective A-B-C (up) | 63% | 304.02 | 339.60 | stale |
