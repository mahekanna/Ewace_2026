# OPERATING POINT — the wave-3 sweep result (research track)

_2026-07-09. Deliverable of the research track in docs/FULL_AUTOMATION_ROADMAP.md.
Method: `scripts/sweep_wave3.py` — 36 pre-committed configs × 12 semis (~70k
15m bars, ~10.7 pooled symbol-years), causal one-position-at-a-time backtests
(`ewave.backtest.engine`), costs on (2 bps + $0.005/sh), every config logged
to registry/trials.jsonl. Selection rule stated BEFORE results were read:
among configs with **≥30 pooled trades/yr/symbol**, rank by **DSR**,
tie-break MinTRL. Analysis only — not advice._

## TL;DR

1. **The crude wave-3 edge is confirmed at 12-symbol breadth**: pooled
   +0.30R over 606 trades (PF 1.61, 56.7 trades/yr/sym, MinTRL 54 ≪ 606,
   family-DSR 0.999). The 2-symbol result in WAVE3_RESULT.md was not an
   AVGO/MRVL artifact.
2. **No gated config meets the ≥30 trades/yr/symbol bar** — the sweep's
   pre-committed selection produces **no `sow_neowave_v1` profile**. The
   frequency ceiling of the gated family is ~24/yr/sym.
3. **The decomposition is the real finding**: an ablation run shows the
   rule-faithful **management** (C-1/E-5 scale-out: 50% at T1, stop→breakeven,
   run to T2; S&B time budget instead of a fixed 96-bar stop; E-10 entry
   window) accounts for most of the per-trade improvement —
   **+0.49R at 25.3 trades/yr/sym with NO confluence/R:R/pattern gates at
   all**. The Table-D strands gate then buys further per-trade quality
   almost linearly in frequency: ~+0.05R per strand level at roughly −⅓
   frequency each.

| operating point | n (pooled) | trades/yr/sym | exp (R) | PF | MinTRL |
|---|---|---|---|---|---|
| baseline: crude skeleton (single target, 96-bar stop) | 606 | **56.7** | +0.30 | 1.61 | 54 |
| **ablation: rule-faithful management only** (no gates) | 270 | 25.3 | **+0.49** | 2.69 | ~15 |
| best gated: strands≥1, R:R≥1, wide band | 254 | 23.8 | +0.51 | 2.76 | 15 |
| strands≥2, R:R≥1 | 181 | 16.9 | +0.60 | 3.23 | 12 |
| strict-like corner (strands≥3, R:R≥2, pattern-ID) | 46 | 4.3 | +0.62 | 2.72 | 15 |

## The full grid (36 configs; costs netted)

All grid rows use scale-out management + S&B time budget + E-10 window
(sb_time=3×W1, entry window 2×W2, pct 0.02, W2 retrace ≥38.2%).

| config (strands / R:R / pattern-ID / W2 band) | n | /yr/sym | exp R | PF | Sharpe | MinTRL | DSR_family |
|---|---|---|---|---|---|---|---|
| s1 rr1.0 pid golden | 165 | 15.4 | 0.576 | 2.74 | 0.41 | 15.0 | 1.000 |
| s1 rr1.0 pid wide | 165 | 15.4 | 0.576 | 2.74 | 0.41 | 15.0 | 1.000 |
| s1 rr1.0 nopid golden | 252 | 23.6 | 0.507 | 2.71 | 0.40 | 15.6 | 1.000 |
| **s1 rr1.0 nopid wide** | **254** | **23.8** | **0.513** | **2.76** | **0.41** | **15.1** | **1.000** |
| s1 rr1.5 pid golden | 165 | 15.4 | 0.576 | 2.74 | 0.41 | 15.0 | 1.000 |
| s1 rr1.5 pid wide | 165 | 15.4 | 0.576 | 2.74 | 0.41 | 15.0 | 1.000 |
| s1 rr1.5 nopid golden | 180 | 16.9 | 0.560 | 2.73 | 0.40 | 15.1 | 1.000 |
| s1 rr1.5 nopid wide | 180 | 16.9 | 0.560 | 2.73 | 0.40 | 15.1 | 1.000 |
| s1 rr2.0 (all 4 variants identical) | 120 | 11.2 | 0.486 | 2.31 | 0.33 | 21.0 | 0.997 |
| s2 rr1.0 pid golden/wide | 122 | 11.4 | 0.646 | 3.07 | 0.45 | 12.5 | 1.000 |
| s2 rr1.0 nopid golden | 179 | 16.8 | 0.598 | 3.22 | 0.47 | 11.9 | 1.000 |
| s2 rr1.0 nopid wide | 181 | 16.9 | 0.596 | 3.23 | 0.47 | 11.9 | 1.000 |
| s2 rr1.5 pid golden/wide | 122 | 11.4 | 0.646 | 3.07 | 0.45 | 12.5 | 1.000 |
| s2 rr1.5 nopid golden/wide | 133 | 12.5 | 0.617 | 2.99 | 0.44 | 13.0 | 1.000 |
| s2 rr2.0 (all 4) | 84 | 7.9 | 0.631 | 2.85 | 0.42 | 13.9 | 0.999 |
| s3 rr1.0 pid golden/wide | 63 | 5.9 | 0.593 | 2.77 | 0.40 | 14.7 | 0.996 |
| s3 rr1.0 nopid golden | 90 | 8.4 | 0.584 | 2.92 | 0.43 | 13.5 | 1.000 |
| s3 rr1.0 nopid wide | 92 | 8.6 | 0.582 | 2.96 | 0.43 | 13.3 | 1.000 |
| s3 rr1.5 pid golden/wide | 63 | 5.9 | 0.593 | 2.77 | 0.40 | 14.7 | 0.996 |
| s3 rr1.5 nopid golden/wide | 67 | 6.3 | 0.579 | 2.73 | 0.40 | 15.1 | 0.996 |
| s3 rr2.0 (all 4) | 46 | 4.3 | 0.617 | 2.72 | 0.39 | 15.1 | 0.986 |

Full machine-readable results: `outputs/backtests/sweep_wave3.{csv,json}`;
per-symbol breakdowns in the .json.

## Statistical reading (two DSRs, both reported)

- **DSR_family** (the textbook correction for picking the best of THIS
  37-config family, variance of the family's Sharpes): >0.98 everywhere —
  within the family, these edges are not best-of-N luck; the pooled samples
  are 3–40× their MinTRL.
- **DSR_registry** (against ALL 100+ trials ever logged, mixed return
  scales): ≈0 everywhere. This bar is distorted — the registry mixes old
  %-return trial Sharpes (up to 2.96) with R-based per-trade Sharpes (~0.2–
  0.47), inflating the expected-max — but we report it because silent
  denominator-shopping is how research lies to itself.
- Caveats that keep this honest: one year of data, one market regime
  (a strong semis tape), 12 correlated symbols from one sector, fills
  assumed at the break level, `zigzag_pct` not swept. This is a **strong
  candidate**, not a proven system.

## Structure of the result

- **Bands and R:R gates barely matter**: golden vs wide W2 band changes
  almost nothing (deep W2 setups are rare); R:R≥1–1.5 seldom binds (median
  planned R:R ≈1.9); R:R≥2.0 strictly hurts (trims the best trades).
- **Pattern-ID (NeoWave :5 on W1)** cuts frequency ~35% for ~+0.05R/trade —
  a real but expensive filter.
- **Strands** are the main quality/frequency dial; s2 is the per-trade sweet
  spot (+0.60–0.65R), s3 adds nothing further.
- **Ghost-forward corroboration** (best candidate, AVGO+MRVL, horizon 96):
  86 signals, hit-rates 40%/57%, MFE/MAE 1.6/1.6 and 2.3/1.3 R — the
  signal-level shape matches the trade-level result
  (`outputs/ghost_forward/*_sw_s1_rr1_nopid_wide/`).

## Verdict & recommendation

**Per the pre-committed rule: no winner.** Nothing gated reaches 30
trades/yr/symbol, so no new profile ships as a validated default and
`experimental` remains the frequency workhorse.

**What the sweep actually taught us:** the biggest under-exploited edge is
not more gates — it is the rule-faithful **exit/management logic**. The
management-only configuration (+0.49R, 25.3/yr/sym, PF 2.7, n=270) nearly
doubles per-trade expectancy over the crude skeleton while keeping 45% of
its frequency, and needs no confluence machinery at all.

**Recommended next experiments (in order):**
1. Sweep `zigzag_pct` (0.015/0.025/0.03) under management-only — a finer
   pivot scale may recover frequency toward the 30+ bar at similar quality.
2. Relax the E-10 window (3×W2) under management-only — isolate how much
   frequency the entry window costs vs the longer holds.
3. Out-of-sector validation (the cached indices/defensives at 1d, or fresh
   15m pulls for non-semis) — break the single-sector correlation caveat.
4. A regime split (first vs second half-year) on the management-only config.

## Reproduce

```bash
python3 scripts/sweep_wave3.py                    # full grid (~4 min)
python3 scripts/sweep_wave3.py --symbols avgo,mrvl --quick
```

Data note: AVGO 15m was refreshed through 2026-07-09 via the MCP bridge
(tvremix → scripts/mcp_export.py, RTH-filtered); the other 11 symbols use the
2026-06 cache (MRVL/NVDA/AMD refresh deferred — marginal for a ~1-yr sample).
