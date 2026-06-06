# Validation Report — wavelib on live daily data

_Regenerated 2026-06-06 by `scripts/run_validation.py` on TradingView/tvremix daily snapshots in `data/live/` (price data as of 2026-06-05 close). Analysis tooling only — not investment advice._

## AVGO — Broadcom · NASDAQ:AVGO
- **4234 daily bars**, last close $385.73
- Macro wave-tree count (full history): top **ZIGZAG**, depth 2, **honest confidence 28%** (covers 37%; 8 roots) — multi-year counts are inherently ambiguous
- Recent best count: **CORRECTION**; reversal zone (358, 410); live confluence **2/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=1 reversals=1 invalidations=0 hit_rate=100%
- Chart: `charts/avgo_analysis.html`

---

## MRVL — Marvell · NASDAQ:MRVL
- **5000 daily bars**, last close $263.47
- Macro wave-tree count (full history): top **TRIANGLE**, depth 5, **honest confidence 33%** (covers 46%; 11 roots) — multi-year counts are inherently ambiguous
- Recent best count: **CORRECTION**; reversal zone (229, 266); live confluence **2/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=0 reversals=0 invalidations=0 hit_rate=0%
- Chart: `charts/mrvl_analysis.html`

---

## NVDA — Nvidia · NASDAQ:NVDA
- **5000 daily bars**, last close $205.10
- Macro wave-tree count (full history): top **FLAT**, depth 4, **honest confidence 17%** (covers 57%; 11 roots) — multi-year counts are inherently ambiguous
- Recent best count: **CORRECTION**; reversal zone (143.89, 179.27); live confluence **0/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=6 reversals=1 invalidations=5 hit_rate=17%
- Chart: `charts/nvda_analysis.html`

---

## AMD — AMD · NASDAQ:AMD
- **5000 daily bars**, last close $466.38
- Macro wave-tree count (full history): top **FLAT**, depth 4, **honest confidence 8%** (covers 15%; 34 roots) — multi-year counts are inherently ambiguous
- Recent best count: **CORRECTION**; reversal zone (256.0, 366.92); live confluence **1/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=2 reversals=1 invalidations=1 hit_rate=50%
- Chart: `charts/amd_analysis.html`

---

## TSM — TSMC · NYSE:TSM
- **5000 daily bars**, last close $415.17
- Macro wave-tree count (full history): top **ZIGZAG**, depth 2, **honest confidence 34%** (covers 47%; 5 roots) — multi-year counts are inherently ambiguous
- Recent best count: **CORRECTION**; reversal zone (254.93, 329.48); live confluence **0/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=0 reversals=0 invalidations=0 hit_rate=0%
- Chart: `charts/tsm_analysis.html`

---

## MU — Micron · NASDAQ:MU
- **5000 daily bars**, last close $864.01
- Macro wave-tree count (full history): top **ZIGZAG**, depth 4, **honest confidence 22%** (covers 46%; 8 roots) — multi-year counts are inherently ambiguous
- Recent best count: **CORRECTION**; reversal zone (454.14, 696.69); live confluence **1/7**
- Causal backtest (last 300 bars, score≥4, +5% target): signals=0 reversals=0 invalidations=0 hit_rate=0%
- Chart: `charts/mu_analysis.html`

---

### How to reproduce

```
python3 scripts/run_validation.py
python3 -m unittest discover -s tests
```
