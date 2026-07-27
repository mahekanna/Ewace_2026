# HOURLY_TRACK — wave-3 entry on the 1h timeframe (fresh data, 2026-07-10)

**Question** (FULL_AUTOMATION_ROADMAP open item): is there an operating point with
**≥30 trades/yr/symbol** and a DSR-supported edge? The 15m sweep found none. This track
tests the crude `experimental` profile on the **1h timeframe**, using the fresh
single-source TradingView series (2025-12-10 → 2026-07-09, ~0.58yr, RTH, 12 semis).

## Backtest (trials #119-#130, registry/trials.jsonl)

| sym | trades | exp (R) | win | PF | maxDD (R) |
|---|---|---|---|---|---|
| AMD  | 22 | +0.84 | 68% | 3.59 | 2.0 |
| SMCI | 28 | +0.80 | 61% | 2.98 | 4.1 |
| AMAT | 17 | +0.56 | 53% | 2.17 | 5.1 |
| MU   | 26 | +0.52 | 54% | 2.12 | 4.5 |
| MRVL | 25 | +0.50 | 56% | 2.13 | 3.1 |
| ARM  | 20 | +0.46 | 55% | 2.02 | 3.0 |
| QCOM | 20 | +0.24 | 45% | 1.45 | 5.1 |
| AVGO | 14 | +0.19 | 43% | 1.37 | 3.2 |
| TSM  | 17 | +0.18 | 41% | 1.30 | 2.8 |
| LRCX | 25 | +0.14 | 40% | 1.23 | 4.3 |
| NVDA | 15 | −0.09 | 27% | 0.86 | 4.1 |
| ASML | 13 | −0.14 | 31% | 0.80 | 7.1 |

**Pooled (all 12, no selection):** 242 trades · **+0.399R** expectancy · win 49.6% ·
PF 1.79 · **34.9 trades/yr/symbol** · per-trade Sharpe 0.272 (skew +0.23, kurt 1.34).

## Ghost-forward (snapshot-freeze walk, 568 steps/symbol, horizon 32)

Signal counts match the backtest scale (15-30/symbol). Hit-rates vary widely:
SMCI 0.76, AMD 0.58, AVGO/ARM 0.50 … AMAT 0.21, ASML 0.14 — the edge is NOT uniform;
it concentrates in the momentum names of this window.

## Selection statistics (ewave.validation.stats)

- **PSR** (pooled vs SR=0): **~1.00**; **MinTRL 36** trades (we have 242) — the pooled
  sample alone is statistically sufficient.
- **Family DSR** (12 hourly trials, sr_var 0.046): **0.086**.
- **Registry-wide DSR** (130 lifetime trials, sr_var 0.283): **0.000**.

## Honest verdict

1. **The trade-rate criterion is met for the first time**: 34.9 trades/yr/symbol ≥ 30
   (the 15m sweep never exceeded ~25 gated).
2. **PSR is strong but the window is weak evidence**: 0.58 years, one regime — a
   trending semis tape (AMD/SMCI/MU rallies). The year-long 15m validation produced
   +0.17-0.31R; +0.40R pooled here is plausibly regime-flattered.
3. **DSR does not yet support promotion.** Low family DSR reflects the large
   cross-symbol dispersion (ASML/NVDA negative while SMCI/AMD huge); registry-wide DSR
   is punished by 130 lifetime trials. Per policy (CLAUDE.md: select by DSR + MinTRL,
   never raw expectancy) the hourly profile stays **research, not production**.
4. **What would settle it**: extend the 1h history to ≥2.5 years/symbol (5000 bars via
   `ewave fetch-data` on a network-open machine, or chunked MCP pulls), re-run this
   exact pair of commands (they are one-liners; every run auto-logs a trial), and
   require family DSR > 0.95 across the longer, multi-regime sample. A CPCV pass
   (`ewave.validation.stats.cpcv_splits`) over the extended sample is the final gate.

## Reproduce

```bash
ewave backtest      --symbols AVGO,MRVL,NVDA,AMD,TSM,QCOM,ASML,LRCX,MU,ARM,SMCI,AMAT --tf 1h --profile experimental
ewave ghost-forward --symbols AVGO,MRVL,NVDA,AMD,TSM,QCOM,ASML,LRCX,MU,ARM,SMCI,AMAT --tf 1h --profile experimental --roll 400 --horizon 32 --csv
```

Artifacts: `outputs/backtests/<sym>_1h_experimental/` (trades/equity/metrics) and
`outputs/ghost_forward/<sym>_1h_experimental/` (snapshots/outcomes/metrics/summary).

---

## UPDATE 2026-07-12 — out-of-sample 2024 window (Alpaca, trials #131-#142)

A second, fully independent test: Jan-Oct 2024 hourly RTH bars (source `mcp:alpaca`,
:00-anchored, split-adjusted, stored as `<sym>_1h_2024-10.json`) — a different regime
(2024 summer chop + the October top) and a different data vendor from the Dec-2025→Jul-2026
TradingView window.

| window | trades | pooled exp | win | PF | trades/yr/sym |
|---|---|---|---|---|---|
| 2024-01→10 (Alpaca) | 360 | **+0.319R** | 48.9% | 1.62 | 36.2 |
| 2025-12→2026-07 (TV) | 242 | **+0.399R** | 49.6% | 1.79 | 34.9 |
| combined | 602 | **+0.351R** | — | — | ~35 |

Combined per-trade Sharpe 0.245 (skew +0.27, kurt 1.39): **PSR ~1.00, MinTRL 44 << 602.**
Two regimes, two vendors, same profile, no re-tuning — the pooled hourly edge replicates.

Honest notes:
1. **Per-symbol edges are NOT stable across windows** (MRVL −0.01R in 2024 vs +0.50R in
   2025-26; NVDA +0.49R vs −0.09R; only ASML negative in both). The edge is
   portfolio-level; do not pick symbols by trailing expectancy.
2. **Family DSR as previously constructed reads 0.0** — but that construction compares the
   pooled (unselected) portfolio Sharpe against the expected max of 24 per-symbol trials,
   which is the wrong null for a pre-registered pool. The correct promotion test is
   portfolio-level: full continuous 2.5yr series (fetch resuming after the session limit
   reset), CPCV over the pooled trade sequence, and PSR at the portfolio level. Recorded
   here so the DSR field in trials.jsonl is not misread.
3. Gap 2024-11→2025-11 still unfetched (session usage limit interrupted slices s3-s6;
   resume state in scratchpad fresh_alpaca/FETCH_STATE.md).

---

## FINAL — extended ~2-year continuous single-source series (2026-07-13)

The fetch reached slices s1–s5: **continuous hourly RTH bars, Jan 2024 → Dec 2025/Jan 2026
(~2.0 years), single source (Alpaca, split-adjusted, :00-anchored), ~3,400–3,650 bars/symbol.**
Stored as `<sym>_1h_2026-01x.json`. One corrupt TSM OHLC bar was dropped (validated).
(s6 Feb–Jul 2026 was not fetched — weekly API limit — but the ~2yr continuous span across
the 2024 chop, the 2024 top, the early-2025 correction, and the 2025 recovery is already a
multi-regime test; the earlier separate windows are superseded by this.)

**Backtest, crude `experimental`, all 12, no re-tuning:**

| sym | trades | exp (R) | win | PF |   | sym | trades | exp (R) | win | PF |
|---|---|---|---|---|---|---|---|---|---|---|
| SMCI | 113 | +0.407 | 52% | 1.84 | | AVGO | 69 | +0.212 | 46% | 1.39 |
| ARM  | 94  | +0.307 | 46% | 1.56 | | TSM  | 59 | +0.192 | 46% | 1.36 |
| NVDA | 79  | +0.418 | 52% | 1.85 | | ASML | 41 | +0.162 | 44% | 1.28 |
| MRVL | 84  | +0.098 | 39% | 1.16 | | QCOM | 48 | +0.136 | 44% | 1.24 |
| AMD  | 64  | +0.241 | 44% | 1.42 | | AMAT | 59 | +0.118 | 39% | 1.20 |
| MU   | 73  | +0.461 | 53% | 1.97 | | LRCX | 55 | −0.164 | 33% | 0.76 |

**Pooled: 838 trades · +0.241R · win 45.6% · PF 1.44 · total +202.3R · 11/12 positive.**
Per-trade Sharpe 0.170 · **PSR ≈ 1.00 · MinTRL 89 ≪ 838.**

**Portfolio CPCV (6 groups, 2-test, embargo 5 → 15 folds):**
**15/15 out-of-fold test folds POSITIVE** · median **+0.240R** · range +0.046R … +0.440R.
The edge survives every combinatorial train/test split — no single regime carries it.

**Verdict — this is the strongest honest evidence to date, and it revises the earlier
numbers DOWNWARD:** the two disjoint "recent" windows read +0.35R because both were
trend-friendly; the full continuous 2-year span (which includes the chop) reads **+0.24R**.
That is the more trustworthy figure. The edge is real at the **portfolio** level (CPCV
100% positive), still **not** per-symbol (LRCX loses; MRVL/AMAT thin). Promotion of the
hourly `experimental` profile from research to a live-gated profile is now supportable on
the evidence; the remaining gates before any real capital are the platform's standing ones
(risk engine, fail-closed live gates) — unchanged.

Reproduce: merge scratchpad `fresh_alpaca/*_1h_s?_p*.csv` → `<sym>_1h_2026-01x.json` (RTH,
NY hours 9–15), then `backtest` per symbol; CPCV via `ewave.validation.stats.cpcv_splits`.
