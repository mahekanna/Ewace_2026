# FULL AUTOMATION ROADMAP

_Restructuring Ewace_2026 into the `ewave` platform: data → causal pivots →
mono-waves → rules → candidates → signals → ghost-forward → backtest → risk →
paper trading, with live gates prepared but disabled. TradingView is optional
verification, not the destination. The validated `wavelib` engine is ported,
not rewritten; `wavelib` stays importable as a shim throughout._

## Engineering phases

Each phase ends with the full test suite green and is committed on
`claude/elliot-wave-tool-plan-lbhwlm`.

| Phase | Content | Acceptance |
|---|---|---|
| **0** ✅ | pyproject + `src/ewave` skeleton + `ewave` CLI stub + configs/*.json + policy docs + outputs/ | `pip install -e .` works; `ewave --help`; existing tests pass; CI green incl. bare-checkout run |
| **1** | Data layer: Bar/BarSeries models, contract-JSON store over `data/live/`, validation, stdlib resampling, adapters (contract, CSV, Alpaca REST, FMP REST, yfinance-guarded), MCP bridge + `scripts/mcp_export.py`; CLI fetch-data / validate-data / resample | validate-data passes on all cached files; round-trip stable; bridge converts fixture FMP/yf/TV dumps |
| **2** | Causal pivots (`percentage_reversal`, `atr_reversal`, `fractal`) + repainting quarantine; mono-wave builder (+ NeoWave :5/:3 labels); F2 dedup; wavelib shim live | old tests green via shim; `ewave pivots` prints pivot_t vs confirmed_t; visibility + quarantine tests |
| **3** | rules split (result/elliott/corrections/triangles/diagonals/neowave/fib) + `Status.UNKNOWN`; patterns (candidates primary, tree context); profiles loader | strict profile reproduces `wave3_signal_strict` trades on AVGO/MRVL fixtures |
| **4** | Signal engine: Signal model (lifecycle candidate→confirmed→entered→exited\|invalidated\|expired), `generate(bars, profile)`, confluence port, trade_plan (REF-only forecast), JSONL store; CLI scan | scan emits signals with signal_time/visible_bars_until; preset-equivalence tests |
| **5** | Ghost-forward: kit → `ewave.validation.ghost_forward` + stability/repaint/late-signal + MFE/MAE metrics + profile forecasters; CLI ghost-forward | reproduces the documented crude-wave3 replay profile; snapshot-freeze test |
| **6** | Backtest: causal replay + confirmation-gated entries + fills/slippage + metrics (PF, expectancy, DSR) + trials auto-log; CLI backtest | expectancy matches docs/WAVE3_RESULT.md; entry ≥ signal_time invariants |
| **7** | Risk engine + paper broker + order state machine + replay-paper loop + live gates (fail closed); CLI paper-trade | replay-paper runs on cached AVGO; kill-switch halts mid-run; live fails closed in all permutations |
| **8** | Batch scanner, markdown/TradingView reporters, chart reuse, README/CLAUDE/RUNBOOK updates, end-to-end chain | fetch→validate→scan→ghost-forward→backtest→paper-trade(--replay)→report clean on cached AVGO/MRVL |

## Research track (parallel; starts after Phase 5; never blocks engineering)

**Find the rule-faithful wave-3 operating point with enough trades.** The crude
skeleton is proven (+0.17..+0.44R, ~80–120 trades/yr/symbol); the strict
RULESET §H version has higher per-trade R but 3–7 trades/yr. Sweep the
`sow_neowave_soft` knobs (min_confluence_strands ∈ {2,3}, min_rr ∈ {1.5, 2.0},
retracement band, S&B time on/off, zigzag_pct) via `ewave ghost-forward` +
`ewave backtest`; log every run to `registry/trials.jsonl`; select by **DSR +
MinTRL**, never raw expectancy. Target: ≥30 trades/yr/symbol with per-trade R
materially above crude. Deliverable: `docs/research/OPERATING_POINT.md`; the
winner ships as a named profile.

## Deferred (not in this build)

Real chakra_quant Hurst/FLD wiring into the cycle seam (the typed `CycleSignal`
slot stays external-input-only) · a live broker executor (see
LIVE_TRADING_SAFETY_POLICY.md) · ML of any kind (needs labeled datasets +
baseline rule performance first) · dashboard UI (engine first).
