# CLAUDE.md — context for Claude Code

This file orients an AI coding agent working in this repo. Read it first.

## What this is
A pure-stdlib Python research base for **Elliott Wave + NeoWave** structural analysis
and **reversal-confluence scoring**, built around AVGO and MRVL but symbol-agnostic.

This repo (**Ewace_2026**) is the *base* for the Elliott Wave / NeoWave research
project. It owns the **"where"** layer — where a reversal is structurally permitted.

## Relationship to `chakra_quant` (sibling repo — future integration)
`chakra_quant` is a separate, mature codebase that owns the **"when"** layer:
JM Hurst time cycles, FLD (Future Line of Demarcation), VTL, Gann S9, and the
sliding-window/causal cycle machinery (see its `src/fld/` package and D-013
causal-only rules). It is **not a dependency today** and must not be imported.

The integration seam already exists here: `score_reversal(..., cycle_aligned=...)`
reserves the **7th confluence strand** for an external Hurst/FLD cycle-timing signal.
Once the Elliott/NeoWave concepts in this repo are validated, the plan is to feed
`chakra_quant`'s cycle model into that slot so "where" (this repo) meets "when"
(chakra_quant). Until that research lands, the 7th strand stays an external boolean
input — keep this repo dependency-free and the seam clean.

## Project layout
```
avgo_mrvl_wave_research/
├── README.md              overview + the session's findings/levels
├── DOCUMENTATION.md       full technical docs (architecture, API, theory, extension)
├── CLAUDE.md              this file
├── requirements.txt       core = stdlib only; optional extras listed
├── wavelib/               the package
│   ├── __init__.py        public API re-exports
│   ├── rules.py           Elliott + NeoWave validators, channeling, engines (canonical Pivot/Wave)
│   ├── toolkit.py         ZigZag, Fibonacci, terminal/wave-5 projection
│   └── confluence.py      reversal-confidence scoring (momentum/volume/structure)
├── data/
│   ├── avgo.py            WEEKLY / H4 / H1 / FRESH_4H_VOL arrays
│   └── mrvl.py            FRESH_4H_VOL / MACRO_PIVOTS
├── examples/              01 validate · 02 confluence · 03 zigzag pipeline
└── charts/                hand-built SVG/HTML charts + index.html dashboard
```

## How to run / verify
```bash
python3 wavelib/rules.py            # self-test (AVGO impulse + terminal + MRVL audit + channels)
python3 wavelib/toolkit.py          # self-test
cd examples && python3 02_confluence_score.py
```
All three examples must run clean. If you touch `rules.py` Pivot/Wave, re-check
`toolkit.py` (it imports them in package context, falls back to local defs standalone).

## Conventions
- Bars are tuples: `(t,o,h,l,c)` generally; `(t,o,h,l,c,v)` where volume is needed
  (confluence). `t` is unix seconds.
- Rule outputs are `RuleResult(rule, status, detail)` with `Status` ∈ PASS/FAIL/WARN/NA/REF.
  A count is INVALID iff any **hard-rule** FAIL (guidelines are WARN, never invalidate).
- `REF` = a rule that needs human/visual discretion, intentionally not auto-decided.
- Keep it dependency-free unless the user opts into extras in `requirements.txt`.

## Design intent (don't violate)
- **Separation of concerns**: structure (rules) ≠ measurement (toolkit) ≠ confirmation
  (confluence). A reversal must be confirmed by independent strands, not the label alone.
- **Honesty over confidence**: surface WARN/REF and stretched/irregular structures
  rather than forcing a clean label. The terminal-retrace timing rule is a *bias*, not
  a precise target (it over-projected on AVGO — see DOCUMENTATION §9).

## Roadmap status (see docs/research/ for the full spec + audit)

Deep research in `docs/research/00_index.md..04_*.md` drove a 5-phase build
(Phases 0–4) — all implemented and tested (90 unit tests in `tests/`):

1. ✅ `label_and_validate(bars)` — multi-scale auto-segmentation → ranked candidate
   counts (`wavelib/automation.py`). Removes hand-picking.
2. 🔲 Hurst/FLD/PSK cycle into the 7th slot — **typed seam only** so far:
   `CycleSignal` (`wavelib/cycle_seam.py`) + `score_reversal(..., cycle_signal=...)`.
   Real wiring to `chakra_quant` is deferred until this engine is validated.
3. ✅ Confirmation strands hardened (`wavelib/confluence.py`): swing-pivot RSI
   divergence, BOS-vs-CHoCH, structural channel break, ≥50-bar guard.
4. ✅ Auto **degree** assignment (Neely bottom-up) — `assign_degrees_neely`
   (`automation.py`); `label_monowaves`/`group_polywaves` in `rules.py`. Degree
   stays the central subjectivity (degree_confidence="HEURISTIC").
5. ✅ Causal backtest harness — `wavelib/backtest.py` (`backtest_reversals`,
   walk-forward, hit-rate/profit-factor; no look-ahead).
6. ✅ `render_chart(waves, projections)` — stdlib SVG emitter (`wavelib/charting.py`).

Still open: F2 (de-dup `similarity_and_balance`/`project_wave5`/terminal-window
across `rules.py`/`toolkit.py`); deeper Neely sub-type labels (`:F3`/`:c3`/…);
the real cycle-model integration (item 2).

## Current market state baked into data
Live snapshots are suffixed by month (`data/live/<sym>_<tf>_<YYYY-MM>.json`);
`scripts/merge_live.py` folds a fresh pull into the prior month's history.
Readers pick the newest snapshot present — see `SNAPSHOTS` in `scripts/wave_report.py`.

**AVGO — 2026-08-14 snapshot ($395.29), all TFs.** Primary five read COMPLETE at
$495.00 (2026-06-03); live structure is the correction off that high. A $495→$356.43,
B $356.43→$432.73 (55% of A), C down opening. Confluence for a bullish reversal:
1/7 weekly, 1/7 daily, 3/7 4H, 2/7 1H, 2/7 15M. Invalidation $495.00; count fails
below $138.10. Full write-up: `reports/AVGO_LIVE_2026-08-14.md`.

_Fixed 2026-08-14 — intrabar pivot ordering._ Both ZigZags used to visit the
extreme in the trend's direction first and test the reversal threshold against
that just-updated extreme, so a bar wide enough to do both emitted a low and a
high pivot at one timestamp in reverse order (it inverted the AVGO 1H/15M last
leg). `_intrabar_order` (`toolkit.py`) now infers the path from open/close —
down bar → o-h-l-c, up bar → o-l-h-c — and both ZigZags walk the extremes in
that order. Bars shorter than (t,o,h,l,c) fall back to the old behaviour.
Guarded by `tests/test_intrabar_order.py`. Higher-TF primary counts were
unaffected; ranked alternates shifted slightly.

_Still open:_ the ZigZag seed prices its first pivot at bar 0's **close** rather
than an extreme, so every series opens with a slightly synthetic pivot.

**MRVL — Jun 5 2026 snapshot ($263.47)** — in $229–266 ((4)) zone, blow-off off
$324, confluence 1/7. Not refreshed in the 2026-08 pull.

## Not in scope
Trade execution / sizing / advice. This is analysis tooling only.
