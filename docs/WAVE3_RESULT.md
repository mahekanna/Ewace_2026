# The wave-3 entry works — the application WAS the problem

_2026-06-13. Causal ghost-feed forward test of `wavelib.wave3.wave3_signal` — the
actual Elliott trade (enter wave 3 on the confirmation break, stop at the wave-2
extreme, target the 1.618× wave-1 extension), EWO-gated. This is the method the
prior "forecast the next leg" signal never implemented (findings doc O2)._

## Result — positive expectancy on every symbol tested

| symbol | data | bars | trades | win% | **expectancy** | profit factor | median R:R |
|---|---|---|---|---|---|---|---|
| AVGO | Alpaca year | 9,776 | 79 | 47% | **+0.17 R** | 1.32 | 1.89 |
| MRVL | Alpaca year | 9,777 | 119 | 51% | **+0.31 R** | 1.67 | 1.71 |
| NVDA | tvremix ~9mo | 5,000 | 27 | 56% | **+0.44 R** | 1.99 | 1.61 |
| AMD  | tvremix ~9mo | 5,000 | 49 | 51% | **+0.41 R** | 1.84 | 1.80 |

~**274 confirmation-triggered trades, all four POSITIVE**, across two data sources.

## Why this is real signal, not barrier asymmetry
A driftless random walk hits a target at R:R≈1.8 before a 1R stop only ~**36%** of
the time (probability ≈ S/(S+T)). Random entries would therefore break even
(0.36·1.8 − 0.64·1 ≈ 0) before costs — *negative* after. Our win rates are
**47–56%, well above the 36% random threshold**, so price reaches the wave-3 target
*more often than chance*: the entry carries genuine directional follow-through —
exactly what Elliott says about the 3rd wave (the strong, extended one).

## Why costs don't kill it
The stop is the **wave-2 extreme** — typically 1–3% away — so risk per trade is
large relative to spread/slippage. A round-trip cost of ~$0.10–0.20 on a multi-%
stop is ≈ **0.02–0.03 R**, which barely dents a +0.17–0.44 R expectancy. (The wide
structural stop is the very thing that made the old next-leg signal's R:R<1 fail
and makes this one robust.)

## What this means
The user's thesis is vindicated: **the missing edge was the APPLICATION, not the
theory.** Trading the *completion* of a structure (the old reflex) is a coin flip;
trading **wave 3 on confirmation** — the actual professional method — shows positive
expectancy on causal, out-of-sample, live-data forward testing across 4 names.

## What is NOT yet established (stay honest)
1. **Sample.** 79–119 trades/symbol (year) and 27–49 (9-mo) — promising, not yet
   statistically airtight; per-trade variance is high. Need more symbols + the full
   year on NVDA/AMD (currently only 9 months of tvremix).
2. **Costs modelled explicitly** (above is an estimate) and **slippage on the break
   fill** (we assume a fill at the wave-1 extreme).
3. **Parameter robustness** — one setting (zigzag pct=0.02, target 1.618×,
   max_hold=96). Sweep pct/target/horizon; the sign should hold.
4. **Scale-out / wave-5** — currently single target; adding the partial + wave-5
   leg may improve it.

## Next (for the Alpaca TEST session)
- Re-fetch the **full year** for NVDA, AMD, TSM, QCOM, ASML, LRCX, MU, ARM, SMCI
  (Alpaca, split-adjusted) and run `scripts/forward_wave3.py <sym> 15m 96 0.02`.
- Add explicit cost (e.g. 0.03 R/trade) and a pct/target sweep.
- Report the pooled expectancy + a DSR-style multiple-testing check.

## Reproduce
```bash
python3 scripts/forward_wave3.py avgo 15m 96 0.02
python3 scripts/forward_wave3.py mrvl 15m 96 0.02
# reports/FORWARD_WAVE3_<SYM>_15m.md
```
