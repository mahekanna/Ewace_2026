# CLAUDE.md — context for Claude Code

This file orients an AI coding agent working in this repo. Read it first.

## What this is
**Ewace_2026** is an Elliott Wave + NeoWave **full-automation platform**
(`ewave`): causal detection → rule validation → signals → ghost-forward
validation → backtest → risk → paper trading, with live-trading gates that
fail closed. Built around AVGO/MRVL research but symbol-agnostic. Pure-stdlib
core; optional extras only behind import guards.

It owns the **"where"** layer — where a reversal/entry is structurally
permitted. The sibling repo `chakra_quant` owns the **"when"** layer (Hurst/FLD
cycles); the only seam is the typed `CycleSignal`
(`ewave.signals.cycle_seam`) feeding the 7th confluence strand. Neither repo
imports the other — keep it that way.

## Layout
```
pyproject.toml            pip install -e . ; console script `ewave`
configs/*.json            app/data/watchlists/profiles/risk/execution (JSON canonical)
src/ewave/                THE platform (see docs/ARCHITECTURE.md for the full map)
  data/                   contract-JSON store over data/live/ + adapters + MCP bridge
  pivots/                 CAUSAL detectors (confirmed_t contract); repainting.py = plotting only
  monowaves/ rules/ patterns/   objective segments; validators (RuleResult); candidates+tree
  signals/                wave-3 generate(bars, profile) [flagship], confluence, Signal+JSONL store
  validation/             ghost_forward/ (snapshot freeze) + stats.py (PSR/DSR/CPCV)
  backtest/ risk/ execution/ scanner/ reporting/
wavelib/                  LEGACY SHIMS over ewave (same objects; don't add code here)
tests/                    unittest; tests/ewave_platform/ = platform acceptance per phase
data/live/                contract JSON bars (~25 symbols); COLLAB_RUNBOOK data contract
ghost_forward_kit/        portable kit; gf.py shims ewave.validation.ghost_forward.core
docs/                     ARCHITECTURE, NO_LOOKAHEAD_POLICY, RULESET, roadmap, research/
outputs/ registry/        run artifacts; trials.jsonl = DSR trial registry (append-only)
```

## How to run / verify
```bash
python3 -m unittest discover -s tests -p "test_*.py"   # full suite (bare checkout works)
pip install -e . && ewave --help
ewave validate-data --all
ewave scan --watchlist default --tf 1h --profile experimental
ewave ghost-forward --symbols AVGO --tf 15m --profile experimental --horizon 96
ewave backtest --symbols AVGO,MRVL --tf 15m --profile experimental
ewave paper-trade --replay --watchlist default --tf 15m --days 120
ewave report --date today
```
CI additionally runs the wavelib module self-tests + examples/ on py3.9/3.11/3.12.

## Non-negotiables
- **No lookahead** (docs/NO_LOOKAHEAD_POLICY.md): pivots usable only from
  `confirmed_t`; cursor-slice replay; snapshot-freeze before outcome labeling;
  every new detector/signal ships its own no-lookahead test. The non-causal
  zigzag lives quarantined in `ewave.pivots.repainting` (an import-graph test
  enforces no signal-path module touches it).
- **Separation of concerns**: detection ≠ signal ≠ risk ≠ execution ≠
  reporting. A label alone never trades (confluence strands are independent).
- **Honesty over confidence**: `Status.UNKNOWN` when data is insufficient;
  REF = human-discretion output that must never gate automation; every
  backtest logs a trial to registry/trials.jsonl; select edges by **DSR +
  MinTRL**, never raw expectancy.
- **Live trading fails closed**: gates only, no live executor ships
  (docs/LIVE_TRADING_SAFETY_POLICY.md).
- **wavelib is frozen**: it's a shim layer. New code goes in src/ewave; legacy
  names must keep resolving (tests enforce identity).

## Empirical ground truth (do not regress)
- The next-leg forecast DIRECTION has **no edge** (coin-flip over a year-long
  causal replay, docs/FORWARD_GHOST_TEST_FINDINGS.md) → REF-only, never an
  entry gate.
- The **wave-3 confirmation entry is the validated signal**
  (docs/WAVE3_RESULT.md): crude profile = +0.167R/79 trades AVGO, +0.314R/119
  MRVL (year, 15m) — `tests/ewave_platform/test_phase6_backtest.py` pins these
  anchors. Strict RULESET-§H profile: higher per-trade R, 3–7 trades/yr.
- Open research (docs/FULL_AUTOMATION_ROADMAP.md): sweep `sow_neowave_soft`
  knobs in configs/profiles.json via ghost-forward+backtest for an operating
  point with ≥30 trades/yr/symbol and DSR-supported edge.

## Data
Contract: `data/live/<slug>_<tf>_<stamp>.json` = `{"symbol","interval","asof",
"bars":[{t,o,h,l,c,v}]}`, t unix seconds UTC ascending, split-adjusted.
In the cloud sandbox market-data hosts are proxy-blocked: fetch via the MCP
finance tools and normalize with `scripts/mcp_export.py` (see
docs/COLLAB_RUNBOOK.md). On machines with access: `ewave fetch-data --adapter
alpaca|fmp|yfinance` (keys via .env, see .env.example).

## Not in scope
Trade execution advice / sizing recommendations; a live broker executor; ML
(needs labeled datasets + baseline rule performance first).
