# NO-LOOKAHEAD POLICY

_The single most important engineering policy in this repo. Every detection,
signal, validation, and backtest module must satisfy it; every reviewer should
check against it first. It codifies discipline that already exists in the
engine (and caught real bugs — see §5)._

## 1. The rule

**No code path that produces a decision at bar `t` may read any bar after `t`.**

A price extreme happens at one time; it becomes *knowable* only later. The two
timestamps are different fields and must never be conflated:

| field | meaning |
|---|---|
| `Pivot.t` (pivot_time) | when the price extreme printed |
| `Pivot.confirmed_t` (confirmed_time) | the first bar at which the pivot is knowable (reversal threshold crossed / n_right bars elapsed) |

- A pivot is **usable only from `confirmed_t`**, never from `t`.
- A pivot with `confirmed_t is None` is **provisional** (the still-open final
  extreme of `zigzag_causal`) and must not enter signal logic.
- A mono-wave is visible only at its **end pivot's** `confirmed_t`.
- Every signal carries `signal_time` = the timestamp of the bar that made it
  visible, and is evaluated from `signal_time` forward only.

## 2. Forbidden

- Back-dating an entry to `pivot_time` when the pivot confirmed later.
- Using final/completed wave labels during historical replay.
- Using future max/min prices (or a completed pattern's shape) to place a
  signal at an earlier timestamp.
- Centered/two-sided filters, `shift(-n)`-style transforms, or "repainting"
  detectors in any signal path. The non-causal `zigzag()` (which back-dates
  pivots to the extreme) is quarantined as `ewave.pivots.repainting` —
  **plotting only**; an import-graph test enforces that no signal, scanner,
  patterns, backtest, or execution module imports it.
- Labeling an outcome before the signal snapshot is frozen (persisted).

## 3. The two approved causal patterns

**Cursor-slice replay** (backtests, ghost-forward): advance a cursor `t`, hand
the engine only `bars[lo : t+1]`, act on the result, then reveal the future one
bar at a time for outcome resolution. Canonical implementations:
`ewave.backtest.replay` (`_replay`) and `ewave.validation.ghost_forward.core`
(`iter_steps`).

**Confirmation-gated entry** (signals): a setup may be described early, but the
entry exists only on the bar where the trigger actually printed (e.g. the
wave-3 entry fires only on the candle that closes beyond the wave-1 extreme),
and the fill is simulated at/after that bar — never at the setup's origin.

**Snapshot-freeze** (validation): persist the signal/candidate exactly as seen
at `t` *before* any future bar is inspected; outcome labeling (MFE/MAE,
target/invalidation hits, stability, repaint) runs strictly on the frozen rows.

## 4. How we test it

- **The monkeypatch proof**: wrap the labeler/generator and record the last-bar
  timestamp of every slice it receives; assert the sequence equals the cursor
  timestamps exactly (`tests/test_phase4_automation.py::TestNoLookAhead`; being
  generalized into a reusable helper in `tests/ewave/`).
- **Visibility tests**: no pivot usable before `confirmed_t`; last zigzag pivot
  provisional; fractal pivots confirmed `n_right` bars late
  (`tests/test_foundations.py`).
- **Invariant tests**: every backtest trade has `entry_time >= signal_time`;
  the ghost-forward outcome labeler refuses unfrozen snapshots.
- Every new detector, signal, or validation feature must ship with its own
  no-lookahead test. "It looks causal" is not evidence.

## 5. Why we are strict (history)

- Forward ghost-testing exposed that projections anchored to the *lagging
  confirmed pivot* were stale ~51% of the time intraday — a flaw ordinary
  backtests hid (docs/SESSION_HANDOFF.md).
- A year-long causal replay showed the next-leg forecast direction is a
  coin-flip (50–51%) despite plausible-looking backtests
  (docs/FORWARD_GHOST_TEST_FINDINGS.md). Its direction logic is therefore kept
  only as a **REF** (reference/discretion) annotation — `Status.REF` marks
  outputs that must never gate an automated decision.
- The wave-3 confirmation entry earned its flagship status the same way: it
  survived the causal replay with positive expectancy (docs/WAVE3_RESULT.md).

Honesty over confidence: when data is insufficient, return `Status.UNKNOWN` —
never a silent PASS.
