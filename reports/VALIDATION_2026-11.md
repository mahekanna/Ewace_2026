# Validation Report — wavelib on live daily data

_Regenerated 2026-11-06 by `scripts/run_validation.py` on the `2026-11` daily snapshots in `data/live/`. Analysis tooling only — not investment advice._

## AVGO — Broadcom · NASDAQ:AVGO
- **4340 daily bars** through 2026-11-05, last close $291.53
- Macro count (full history): primary **WXY** @ Cycle, **honest confidence 44%** (covers 83%); alternates: ZIGZAG 32%, FLAT 27% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (366.56, 415.61); live confluence **1/7**; EWF swing-sequence: 25 (INCOMPLETE)
- **Forecast next**: new impulse (down) → targets [], invalidation 495.0 (confidence 32%)
- NeoWave: 9 motive(:5) / 51 corrective(:3) monowaves; terminal check: overlap present (terminal/diagonal)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=1 hit_rate=100%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 1)
- Chart: `charts/avgo_analysis_2026-11.html`

---

## MRVL — Marvell · NASDAQ:MRVL
- **4489 daily bars** through 2026-11-05, last close $133.55
- Macro count (full history): primary **DIAGONAL** @ Primary, **honest confidence 34%** (covers 50%); alternates: FLAT 45%, WXY 43% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (163.98, 227.34); live confluence **0/7**; EWF swing-sequence: 60 (INCOMPLETE)
- **Forecast next**: new impulse (down) → targets [1.000x (equal legs) 200.6, 1.618x (Blue Box top) 138.4], invalidation 301.27 (confidence 63%)
- NeoWave: 22 motive(:5) / 64 corrective(:3) monowaves; terminal check: overlap present (terminal/diagonal)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 0)
- Chart: `charts/mrvl_analysis_2026-11.html`

---

### How to reproduce

```
python3 scripts/run_validation.py --tag 2026-11
python3 -m unittest discover -s tests
```
