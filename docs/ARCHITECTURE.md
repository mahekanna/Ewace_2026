# ARCHITECTURE — the `ewave` platform

_The repo is being restructured from the `wavelib` research base into a full
automation platform under `src/ewave`, per docs/FULL_AUTOMATION_ROADMAP.md.
`wavelib` remains importable as a thin shim so existing tests, scripts, and the
two-session workflow (docs/COLLAB_RUNBOOK.md) keep working._

## Pipeline

```
MCP export / yfinance / FMP / Alpaca / CSV
        ↓
ewave.data          contract-JSON store (data/live/) · validation · resampling
        ↓
ewave.pivots        CAUSAL detectors (pct-reversal, ATR, fractal) — pivot_t vs confirmed_t
        ↓
ewave.monowaves     confirmed pivots → objective segments (+ NeoWave :5/:3 labels)
        ↓
ewave.rules         Elliott + NeoWave validators → RuleResult(PASS/FAIL/WARN/NA/REF/UNKNOWN)
        ↓
ewave.patterns      candidates (automation path = primary; wave tree = context)
        ↓
ewave.signals       wave-3 confirmation entry (flagship) + confluence gate → Signal objects
        ↓
ewave.validation    ghost-forward replay (snapshot freeze → outcome labeling) · PSR/DSR/CPCV
        ↓
ewave.backtest      causal-entry backtest · fills/slippage · metrics · trials registry
        ↓
ewave.risk          approval: sizing, loss limits, exposure, cooldown, kill switch
        ↓
ewave.execution     paper broker (simulated fills, JSONL ledgers) · live = gates only, fails closed
        ↓
ewave.reporting     markdown/TradingView notes/SVG+HTML charts → outputs/
```

Cross-cutting: `ewave.config` (JSON-first configs/), `ewave.cli` (`ewave` command,
thin argparse), `ewave.features.indicators` (one shared RSI/EMA/MACD/ATR copy),
`ewave.signals.cycle_seam` (typed seam for the future chakra_quant Hurst/FLD
"when" layer — 7th confluence strand; neither repo imports the other).

## Decision log

| # | Decision |
|---|---|
| D1 | src-layout, setuptools, console script `ewave = ewave.cli:main` |
| D2 | `wavelib/` = re-export shim over `ewave.*` with a `src/` path bootstrap, so a bare checkout works without pip install |
| D3 | JSON configs canonical; PyYAML optional (`ewave[yaml]`) |
| D4 | `Status` keeps PASS/FAIL/WARN/NA/REF and gains UNKNOWN (= insufficient confirmed data). REF = human-discretion/reference-only — REF outputs never gate automation |
| D5 | `patterns.candidates` (RuleResult-native, causal) is the primary candidate path; `patterns.tree` (wavetree) provides context/confidence components only, never a gate |
| D6 | Flagship signal = wave-3 confirmation entry, profile-parameterized (configs/profiles.json spans the proven crude skeleton ↔ rule-faithful strict). The disproven next-leg forecast direction is REF-only |
| D7 | `ewave.rules.result` is the single owner of Pivot/Wave/Status/RuleResult; toolkit's divergent duplicates are gone in ewave (legacy names still resolve via the shim) |
| D8 | Non-causal zigzag quarantined in `ewave.pivots.repainting` (plotting only) + import-graph test |
| D9 | `data/live/` contract JSON stays the canonical store; JSONL replaces parquet everywhere |
| D10 | Live trading: gate checks only; fails closed with the failing gate named; no broker order code ships |

## Separation of concerns (do not blur)

Detection says *what structure may be forming*. Signals say *there is a
setup*. Risk says *whether and how big*. Execution says *what happened to the
order*. Validation says *whether any of it was visible and useful in real
time*. Reporting renders; it never decides. A wave label alone never trades —
confluence strands are independent by design.

## Data contract

`data/live/<slug>_<tf>_<stamp>.json`:
`{"symbol", "interval", "asof", "bars": [{"t","o","h","l","c","v"}, ...]}` —
`t` unix seconds UTC, strictly ascending, split-adjusted. Engine-internal bar
form is the tuple `(t,o,h,l,c[,v])`; `ewave.data.models.BarSeries.tuples()`
bridges the two. In this cloud sandbox market-data hosts are proxy-blocked:
bars arrive via MCP finance tools normalized by `scripts/mcp_export.py`
(`ewave.data.adapters.mcp_bridge`); on user machines the yfinance/FMP/Alpaca
adapters fetch directly.

## Empirical ground truth (why the defaults are what they are)

- Next-leg forecast direction: NO edge on a year-long causal replay
  (docs/FORWARD_GHOST_TEST_FINDINGS.md) → REF-only.
- Wave-3 confirmation entry: positive expectancy, +0.17..+0.44R across 4
  symbols (docs/WAVE3_RESULT.md) → flagship, `experimental` profile.
- Rule-faithful strict variant: higher per-trade R (+0.73..+1.12R) but 3–7
  trades/yr (docs/RULESET.md §G-H) → `sow_neowave_strict` profile; the open
  research track sweeps the space between, selected by DSR not raw expectancy.
