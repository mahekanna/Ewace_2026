# Validation Report — wavelib on live daily data

_Regenerated 2026-11-06 by `scripts/run_validation.py` on the `2026-11` daily snapshots in `data/live/`. Analysis tooling only — not investment advice._

## AVGO — Broadcom · NASDAQ:AVGO
- **4340 daily bars** through 2026-11-05, last close $291.53
- Macro count (full history): primary **IMPULSE** @ Cycle, **honest confidence 29%** (covers 100%); alternates: ZIGZAG 24%, WXY 10% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (366.56, 415.61); live confluence **1/7**; EWF swing-sequence: 25 (INCOMPLETE)
- **Forecast next**: corrective A-B-C (down) → targets [0.382 retrace 306.9, 0.500 retrace 248.8, 0.618 retrace 190.7], invalidation 2.64 (confidence 29%)
- NeoWave: 11 motive(:5) / 68 corrective(:3) monowaves; terminal check: overlap present (terminal/diagonal)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=1 hit_rate=100%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 1)
- Chart: `charts/avgo_analysis_2026-11.html`

---

## MRVL — Marvell · NASDAQ:MRVL
- **4489 daily bars** through 2026-11-05, last close $133.55
- Macro count (full history): primary **WXY** @ Primary, **honest confidence 18%** (covers 37%); alternates: WXY 12%, WXY 4% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (163.98, 227.34); live confluence **0/7**; EWF swing-sequence: 69 (INCOMPLETE)
- **Forecast next**: new impulse (down) → targets [], invalidation 301.27 (confidence 18%)
- NeoWave: 36 motive(:5) / 102 corrective(:3) monowaves; terminal check: overlap present (terminal/diagonal)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 0)
- Chart: `charts/mrvl_analysis_2026-11.html`

---

### How to reproduce

```
python3 scripts/run_validation.py --tag 2026-11
python3 -m unittest discover -s tests
```
