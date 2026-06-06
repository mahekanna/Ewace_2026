# Validation Report — wavelib on live daily data

_Regenerated 2026-06-06 by `scripts/run_validation.py` on TradingView/tvremix daily snapshots in `data/live/` (price data as of 2026-06-05 close). Analysis tooling only — not investment advice._

## AVGO — Broadcom · NASDAQ:AVGO
- **4234 daily bars**, last close $385.73
- Macro count (full history): primary **ZIGZAG** @ Minuette, **honest confidence 28%** (covers 37%); alternates: ZIGZAG 9%, ZIGZAG 5% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (358, 410); live confluence **2/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=1 reversals=1 invalidations=0 hit_rate=100%; statistical power: UNDERPOWERED — too few events to claim edge
- Chart: `charts/avgo_analysis.html`

---

## MRVL — Marvell · NASDAQ:MRVL
- **5000 daily bars**, last close $263.47
- Macro count (full history): primary **TRIANGLE** @ Minor, **honest confidence 33%** (covers 46%); alternates: FLAT 17%, TRIANGLE 4% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (229, 266); live confluence **2/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=0 reversals=0 invalidations=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge
- Chart: `charts/mrvl_analysis.html`

---

## NVDA — Nvidia · NASDAQ:NVDA
- **5000 daily bars**, last close $205.10
- Macro count (full history): primary **FLAT** @ Minute, **honest confidence 17%** (covers 57%); alternates: FLAT 16%, ZIGZAG 10% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (143.89, 179.27); live confluence **0/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=6 reversals=1 invalidations=5 hit_rate=17%; statistical power: PSR 100%, MinTRL 3
- Chart: `charts/nvda_analysis.html`

---

## AMD — AMD · NASDAQ:AMD
- **5000 daily bars**, last close $466.38
- Macro count (full history): primary **FLAT** @ Minute, **honest confidence 8%** (covers 15%); alternates: FLAT 8%, FLAT 5% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (256.0, 366.92); live confluence **1/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=2 reversals=1 invalidations=1 hit_rate=50%; statistical power: UNDERPOWERED — too few events to claim edge
- Chart: `charts/amd_analysis.html`

---

## TSM — TSMC · NYSE:TSM
- **5000 daily bars**, last close $415.17
- Macro count (full history): primary **ZIGZAG** @ Minuette, **honest confidence 34%** (covers 47%); alternates: ZIGZAG 13%, ZIGZAG 13% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (254.93, 329.48); live confluence **0/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=0 reversals=0 invalidations=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge
- Chart: `charts/tsm_analysis.html`

---

## MU — Micron · NASDAQ:MU
- **5000 daily bars**, last close $864.01
- Macro count (full history): primary **ZIGZAG** @ Minute, **honest confidence 22%** (covers 46%); alternates: ZIGZAG 10%, FLAT 4% — multi-year counts are ambiguous
- Recent best count: **CORRECTION**; reversal zone (454.14, 696.69); live confluence **1/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=0 reversals=0 invalidations=0 hit_rate=0%; statistical power: UNDERPOWERED — too few events to claim edge
- Chart: `charts/mu_analysis.html`

---

### How to reproduce

```
python3 scripts/run_validation.py
python3 -m unittest discover -s tests
```
