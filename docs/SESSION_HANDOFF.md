# SESSION HANDOFF — Elliott/NeoWave engine rebuild + forward testing

_Last updated 2026-06-13. Read this first to resume; everything below is committed
on branch `claude/ewave-2026-base-repo-ZRYzS`._

## Where we are
The wave engine was rebuilt to apply EW/NeoWave the way professionals do, then
validated with **ghost-feeding forward testing** (not just backtests).

### Engine rebuild — DONE (5 phases, 173 tests green)
Driven by `docs/research/audit/00_MISTAKES_AND_FIXES.md` (located bugs) +
`docs/research/practitioner/00_PRO_APPLICATION_SPEC.md` (how pros apply it):
1. **Log measurement** — `Wave.log_length`; all Fib/ratio comparisons in log space.
2. **Momentum gate** — EWO (5/35) gates wave-3 identity (`wavetree.momentum_lookup`,
   `_momentum_multiplier`).
3. **Top-down anchoring** — `wavetree.top_down_count` finds the best full-range
   5-wave partition → AVGO/MRVL now read **IMPULSE @ Cycle, 100% coverage** (was
   "ZIGZAG @ Minuette"). Calendar-based degree; confidence haircut + 0.85 cap.
4. **Projection** — Fibonacci EXTENSIONS + confluence CLUSTER (`toolkit.fib_cluster`)
   + NeoWave TIME window `[N/3,3N]` in `forecast.forecast_from_count`.
5. **Trading discipline** — `forecast.trade_plan` carries confluence target, R:R,
   alternate flip-price, confluence gate.

### Validation — the honest findings
- **Backtest re-test (rebuilt engine, 1W+1D):** counts fixed, but **no predictive
  edge** — direction skill still ~coin-flip / worse than buy-and-hold; the powered
  "positive" BOS rows are drift + barrier-asymmetry, not skill. See
  `reports/FORECAST_BACKTEST_2026-06.md` (hand-written verdict) and
  `reports/FORECAST_BACKTEST_prerebuild.md` (before).
- **Forward test (ghost-feeding, AVGO 15m)** — `scripts/forward_test.py`. Exposed a
  real flaw backtests hid: forecasts anchored to the lagging confirmed pivot were
  **stale ~51%** of the time intraday. **Fixed** by re-anchoring projections to
  current price (`forecast_from_count`, ZIGZAG/FLAT/TRIANGLE branches) → **stale
  51%→6%**, honest target-hit **57%**, next-candle direction 55%. R:R<1 so not yet a
  proven edge. Report: `reports/FORWARD_TEST_AVGO_15m.md`; snapshots:
  `charts/png/forward/`.

## The standing conclusion
Applying the tools professionally made the **counts correct** (real analysis-quality
gain) but did **not** produce a tradeable directional edge on the evidence so far.
Forward testing is the right validation method and is now usable.

## Open / next steps
1. **Alpaca data** — BLOCKED in the cloud env two ways: (a) no Alpaca MCP injected
   here, (b) `data.alpaca.markets` not in the network egress allowlist ("Host not in
   allowlist"). To use it: add the Alpaca MCP **and** allowlist the hosts in THIS
   web environment's settings, then start a fresh session. tvremix is the only
   market-data MCP available otherwise.
2. **Improve R:R** — targets currently sit closer than the structural stop (R:R<1),
   which caps the forward-test edge. Make targets structure-based nearer parity.
3. **Add the confluence/momentum gate to forward entries**, then re-ghost-feed.
4. **Truly live forward loop** — once data is live: forecast → wait for the next
   real candle → self-evaluate (can schedule with send_later/Monitor).
5. **Multi-symbol, longer-window forward test** for a real sample (current = 2 weeks,
   1 symbol).

## How to run
```
python3 -m unittest discover -s tests          # 173 tests
python3 scripts/wave_report.py AVGO MRVL       # detailed counts
python3 scripts/wave_charts.py avgo mrvl       # PNG charts (charts/png/)
python3 scripts/forward_test.py avgo 15m       # ghost-feeding forward test
```
matplotlib is a non-stdlib extra used only by the chart scripts (core `wavelib`
stays stdlib).
