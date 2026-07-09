# PAPER TRADING POLICY

Paper trading is the mandatory proving ground between validated signals and any
live order. It exercises the *entire* loop — scanner → signal → risk approval →
order → simulated fill → position → report — with zero market impact.

## Rules

1. **Paper before live, always.** The live executor refuses to start without a
   paper-trading performance report on disk (docs/LIVE_TRADING_SAFETY_POLICY.md).
2. **Same code path as live.** The paper broker implements the same
   `BrokerInterface` and order state machine (`pending → submitted → accepted →
   partially_filled → filled | cancelled | rejected | expired | failed`) that a
   live executor would. No shortcuts that a real broker wouldn't allow.
3. **No order without risk approval.** Every order carries the RiskEngine
   approval (size, risk amount) or it is not placed. Bypassing the risk engine
   is a bug, not a feature.
4. **Honest fills.** Market orders fill at the *next* bar's open (never the
   signal bar's close); limit/stop orders fill only when the level actually
   trades intra-bar; slippage and commission from configs/execution.json are
   always applied.
5. **Signals are frozen before outcomes.** Orders reference persisted signal
   ids (outputs/signals/*.jsonl); a fill can never retroactively edit the
   signal that caused it.
6. **Kill switch honored.** The presence of `outputs/KILL_SWITCH` halts new
   orders immediately; the loop flattens per config and stops.
7. **Everything is a ledger.** Orders, fills, and positions append to JSONL
   under outputs/paper_trading/; a daily markdown report summarizes signals
   seen, orders placed/rejected, open positions, P&L, and drawdown. Ledgers
   are append-only history — do not rewrite them.

## Two bar sources, one loop

- `ewave paper-trade --replay` — deterministic replay over cached contract
  JSON (works offline / in the sandbox; used by tests).
- live-poll mode — polls a data adapter for new bars on the user's machine.

The trading logic is identical in both; only the bar source differs.

## Exit criteria toward live readiness

A paper campaign supports live-readiness only if: it ran the current engine
version; covered ≥ the MinTRL implied by its Sharpe (ewave.validation.stats);
its DSR is positive after accounting for the trials registry; and its
max-drawdown and rejection rates are within the risk config. Until then, live
gates stay closed — see docs/LIVE_TRADING_SAFETY_POLICY.md.
