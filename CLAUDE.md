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
│   ├── confluence.py      reversal-confidence scoring (momentum/volume/structure)
│   ├── forecast.py        next-wave projection from a count (targets / void / time window)
│   ├── count_history.py   causal replay: count HELD at every bar + per-adoption forecasts graded
│   └── brief.py           plain-language read: stance, trigger, void, deadline, reliability, what to do
├── data/
│   ├── fetch.py           load_bars() (stdlib) + yfinance fetch/refresh of snapshots & fixtures
│   ├── avgo.py            WEEKLY / DAILY / H4 / H1 / FRESH_4H_VOL (auto-generated)
│   ├── mrvl.py            same arrays + hand-curated MACRO_PIVOTS (preserved on regen)
│   └── live/              <slug>_<tf>_<YYYY-MM>.json snapshots (2026-06 baseline, 2026-11 fresh)
├── examples/              01 validate · 02 confluence · 03 zigzag pipeline
└── charts/                hand-built SVG/HTML charts + index.html dashboard
```

## How to run / verify
```bash
python3 wavelib/rules.py            # self-test (AVGO impulse + terminal + MRVL audit + channels)
python3 wavelib/toolkit.py          # self-test
cd examples && python3 02_confluence_score.py
python3 -m unittest discover -s tests            # full suite
python3 scripts/run_validation.py --tag 2026-11 --symbols AVGO MRVL   # daily (1d) stack on fresh data
python3 scripts/count_history.py AVGO MRVL --tag 2026-11                # bar-by-bar count continuation + graded next-wave forecasts
python3 scripts/brief.py AVGO MRVL                                       # plain-language read (reports/BRIEF_<tag>.md)
```
All examples must run clean. To refresh data: `pip install yfinance` (optional extra),
then `python3 data/fetch.py AVGO MRVL --fixtures` (see DOCUMENTATION §5). Do not
overwrite the `2026-06` snapshots — they are the recorded forward-test baseline. If you touch `rules.py` Pivot/Wave, re-check
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

## Current market state baked into data (Nov 5 2026 close, via data/fetch.py)
- AVGO $291.53 — gapped below the old $301 2-4 line and the $358–410 (IV) zone cited
  in README/examples (those are the June-2026 session findings, kept as history).
  300-bar read: FLAT A@495.00 (Jun 3 ATH) → B@356.43 (Jul 2) → C@432.73 (Aug 10), 38%;
  brief stance CONFIRMED BIAS down (break of 356.43 on Oct 26), void above 432.73.
- MRVL $133.55 — far below the old $229–266 ((4)) zone; 300-bar read IMPULSE 1-5 ending
  $329.88 (Jun 18), 37%; brief stance PLAYED OUT (price past every projected level).
- Honest replay scorecard (nearest-target hit rate of next-wave projections, graded causally):
  AVGO 23%, MRVL 31% — the forecaster is a bias, not an edge. Enforcing structural
  correctness (Nov 2026 wavetree fixes) made counts *right* but not more *predictive*.
- Reports: `reports/VALIDATION_2026-11.md`, `reports/COUNT_HISTORY_2026-11.md`,
  `reports/BRIEF_2026-11.md`. June baseline: `reports/VALIDATION_2026-06.md`.

## Not in scope
Trade execution / sizing / advice. This is analysis tooling only.
