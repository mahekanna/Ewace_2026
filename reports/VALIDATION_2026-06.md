# Validation Report — wavelib on live daily data

_Regenerated 2026-06-06 by `scripts/run_validation.py` on TradingView/tvremix daily snapshots in `data/live/` (price data as of 2026-06-05 close). Analysis tooling only — not investment advice._

## AVGO — Broadcom · NASDAQ:AVGO
- **4234 daily bars**, last close $385.73
- Macro count (full history): primary **ZIGZAG** @ Minuette, **honest confidence 28%** (covers 37%); alternates: FLAT 9%, WXY 6% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (358, 410); live confluence **2/7**; EWF swing-sequence: 22 (INCOMPLETE)
- **Forecast next**: new impulse (up) → targets [0.618x last leg 365.6, 1.000x last leg 386.5, 1.618x last leg 420.3], invalidation 331.8 (confidence 26%)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=1 hit_rate=100%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 1)
- Chart: `charts/avgo_analysis.html`

---

## MRVL — Marvell · NASDAQ:MRVL
- **5000 daily bars**, last close $263.47
- Macro count (full history): primary **TRIANGLE** @ Minor, **honest confidence 33%** (covers 46%); alternates: FLAT 26%, TRIANGLE 5% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (229, 266); live confluence **2/7**; EWF swing-sequence: 53 (INCOMPLETE)
- **Forecast next**: new impulse (down) → targets [0.618x last leg 90.6, 1.000x last leg 77.4, 1.618x last leg 56.1], invalidation 111.89 (confidence 26%)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 0)
- Chart: `charts/mrvl_analysis.html`

---

## NVDA — Nvidia · NASDAQ:NVDA
- **5000 daily bars**, last close $205.10
- Macro count (full history): primary **WXY** @ Minute, **honest confidence 18%** (covers 43%); alternates: FLAT 16%, WXY 5% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (143.89, 179.27); live confluence **0/7**; EWF swing-sequence: 22 (INCOMPLETE)
- **Forecast next**: new impulse (down) → targets [0.618x last leg 190.2, 1.000x last leg 173.7, 1.618x last leg 147.0], invalidation 216.82 (confidence 48%)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=6 hit_rate=100%; statistical power: PSR 100%; CPCV 5th-pctile OOS profit-factor inf (15 folds)
- Chart: `charts/nvda_analysis.html`

---

## AMD — AMD · NASDAQ:AMD
- **5000 daily bars**, last close $466.38
- Macro count (full history): primary **FLAT** @ Minute, **honest confidence 9%** (covers 16%); alternates: FLAT 8%, WXY 5% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (256.0, 366.92); live confluence **1/7**; EWF swing-sequence: 42 (INCOMPLETE)
- **Forecast next**: new impulse (down) → targets [0.618x last leg 255.2, 1.000x last leg 221.3, 1.618x last leg 166.5], invalidation 310 (confidence 34%)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=2 hit_rate=50%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 2)
- Chart: `charts/amd_analysis.html`

---

## TSM — TSMC · NYSE:TSM
- **5000 daily bars**, last close $415.17
- Macro count (full history): primary **FLAT** @ Minute, **honest confidence 54%** (covers 100%); alternates: FLAT 22%, WXY 20% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (254.93, 329.48); live confluence **0/7**; EWF swing-sequence: 9 (MOTIVE-COMPLETE)
- **Forecast next**: new impulse (down) → targets [0.618x last leg 410.6, 1.000x last leg 386.1, 1.618x last leg 346.5], invalidation 450.16 (confidence 36%)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 0)
- Chart: `charts/tsm_analysis.html`

---

## MU — Micron · NASDAQ:MU
- **5000 daily bars**, last close $864.01
- Macro count (full history): primary **WXY** @ Minor, **honest confidence 45%** (covers 74%); alternates: FLAT 13%, WXY 4% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (454.14, 696.69); live confluence **1/7**; EWF swing-sequence: 47 (INCOMPLETE)
- **Forecast next**: new impulse (down) → targets [0.618x last leg 133.6, 1.000x last leg 103.4, 1.618x last leg 54.5], invalidation 182.39 (confidence 30%)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 0)
- Chart: `charts/mu_analysis.html`

---

### How to reproduce

```
python3 scripts/run_validation.py
python3 -m unittest discover -s tests
```
