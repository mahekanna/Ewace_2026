# LIVE TRADING SAFETY POLICY

**Live trading is disabled by design.** This repo ships live *infrastructure
gates*, not a live executor: even with every gate green, the shipped
`ewave.execution.live` raises `NotImplementedError` instead of routing an
order. Enabling real orders is a deliberate future step that requires writing
and reviewing a live executor — it can never happen by flipping a flag.

## Fail-closed gates

`ewave.execution.guard` evaluates all gates and names the first failure; the
live path raises `LiveTradingDisabled` unless **all** of the following hold:

1. `EWAVE_ENABLE_LIVE=true` in the environment (never set in committed files).
2. `configs/execution.json` → `"mode": "live"`.
3. `configs/risk.json` → `"live_enabled": true`.
4. A paper-trading performance report exists under `outputs/paper_trading/`
   (see docs/PAPER_TRADING_POLICY.md exit criteria).
5. No kill-switch file (`outputs/KILL_SWITCH`) present.
6. Risk limits configured: max daily loss, max position exposure, max open
   positions are all set and non-zero.

Missing any one → refuse to start, log the failing gate, exit non-zero.

## Standing controls (apply to any future live executor)

- **Kill switch**: creating `outputs/KILL_SWITCH` (manually or by the risk
  engine on a daily-loss breach) halts new orders immediately and flattens per
  config. It is checked every cycle, not just at startup.
- **Risk engine is unbypassable**: no order without a fresh `RiskEngine`
  approval; approvals are logged with the order.
- **No credentials in the repo**: keys come from the environment only
  (`.env.example` documents the names, never values).
- **Cooldown after loss**, per-symbol and portfolio exposure caps, and
  daily/weekly loss limits per `configs/risk.json`.
- **Audit trail**: every order, rejection, fill, and gate evaluation is
  appended to outputs/logs/ — reconstructable after the fact.

## Tests

`tests/ewave/` must prove: live fails closed for every single missing gate,
for all-gates-missing, and — crucially — that all-gates-green still refuses to
trade (`NotImplementedError`). A change that weakens any of these tests is a
policy violation, not a refactor.
