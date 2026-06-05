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

## Highest-value TODOs (the user wants to research these)
1. `label_and_validate(bars)` — auto-segment ZigZag → candidate impulses/corrections →
   validate at multiple degrees → return best-scoring count. (Removes hand-picking legs.)
2. Wire a **Hurst/FLD/PSK cycle** model into the reserved 7th confluence slot
   (`score_reversal(..., cycle_aligned=...)`). User has prior cycle toolkits.
3. Feed 50–100 bars to confluence so the RSI/divergence strand activates.
4. Auto **degree** assignment (Neely monowave→polywave→multiwave) — the biggest open
   subjectivity; currently degree is assumed, only internal consistency is checked.
5. Backtest harness: replay bars, score reversals, measure score≥4 hit-rate.
6. `render_chart(waves, projections)` to emit the SVG charts programmatically.

## Current market state baked into data (Jun 5 2026)
- AVGO $385.74 — in $358–410 (IV) zone, A-B-C corrective, 2-4 line $301 unbroken,
  invalidation $251.88, confluence 1/7.
- MRVL $263.47 — in $229–266 ((4)) zone, blow-off off $324, confluence 1/7.

## Not in scope
Trade execution / sizing / advice. This is analysis tooling only.
