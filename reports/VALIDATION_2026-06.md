# Validation Report — wavelib on live daily data

_Regenerated 2026-06-06 by `scripts/run_validation.py` on TradingView/tvremix daily snapshots in `data/live/` (price data as of 2026-06-05 close). Analysis tooling only — not investment advice._

## AVGO — Broadcom · NASDAQ:AVGO
- **4234 daily bars**, last close $385.73
- Macro count (full history): primary **ZIGZAG** @ Minuette, **honest confidence 28%** (covers 37%); alternates: ZIGZAG 8%, ZIGZAG 5% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (358, 410); live confluence **2/7**; EWF swing-sequence: 22 (INCOMPLETE)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=1 hit_rate=100%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 1)
- Chart: `charts/avgo_analysis.html`

---

## MRVL — Marvell · NASDAQ:MRVL
- **5000 daily bars**, last close $263.47
- Macro count (full history): primary **TRIANGLE** @ Minor, **honest confidence 33%** (covers 46%); alternates: FLAT 26%, TRIANGLE 4% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (229, 266); live confluence **2/7**; EWF swing-sequence: 53 (INCOMPLETE)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 0)
- Chart: `charts/mrvl_analysis.html`

---

## NVDA — Nvidia · NASDAQ:NVDA
- **5000 daily bars**, last close $205.10
- Macro count (full history): primary **ZIGZAG** @ Minute, **honest confidence 24%** (covers 43%); alternates: FLAT 6%, ZIGZAG 4% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (143.89, 179.27); live confluence **0/7**; EWF swing-sequence: 22 (INCOMPLETE)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=6 hit_rate=100%; statistical power: PSR 100%; CPCV 5th-pctile OOS profit-factor inf (15 folds)
- Chart: `charts/nvda_analysis.html`

---

## AMD — AMD · NASDAQ:AMD
- **5000 daily bars**, last close $466.38
- Macro count (full history): primary **FLAT** @ Minute, **honest confidence 9%** (covers 16%); alternates: FLAT 8%, TRIANGLE 4% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (256.0, 366.92); live confluence **1/7**; EWF swing-sequence: 42 (INCOMPLETE)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=2 hit_rate=50%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 2)
- Chart: `charts/amd_analysis.html`

---

## TSM — TSMC · NYSE:TSM
- **5000 daily bars**, last close $415.17
- Macro count (full history): primary **ZIGZAG** @ Minuette, **honest confidence 34%** (covers 47%); alternates: FLAT 23%, ZIGZAG 15% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (254.93, 329.48); live confluence **0/7**; EWF swing-sequence: 9 (MOTIVE-COMPLETE)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 0)
- Chart: `charts/tsm_analysis.html`

---

## MU — Micron · NASDAQ:MU
- **5000 daily bars**, last close $864.01
- Macro count (full history): primary **ZIGZAG** @ Minute, **honest confidence 33%** (covers 69%); alternates: FLAT 12%, FLAT 4% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (454.14, 696.69); live confluence **1/7**; EWF swing-sequence: 47 (INCOMPLETE)
- Causal backtest (last 300 bars, score≥4, +5% target): decided events=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge; CPCV needs ≥6 events (have 0)
- Chart: `charts/mu_analysis.html`

---

### How to reproduce

```
python3 scripts/run_validation.py
python3 -m unittest discover -s tests
```
