# TEST session — Alpaca data + ghost forward-test results (AVGO/MRVL, 1-year 15m)

_Run 2026-06-13 by the Alpaca-enabled TEST session (see `docs/COLLAB_RUNBOOK.md`).
Causal ghost-feeding forward test; analysis only, not advice._

## Data source
- **Alpaca via MCP** (server `Alpacamn`), `feed=sip`, `adjustment=split`.
- **REST unavailable here:** `data.alpaca.markets` → `403 Host not in allowlist`, and
  `APCA_API_KEY_ID/SECRET` unset, so `scripts/alpaca_fetch.py` can't run. Pulled via the
  MCP `get_stock_bars` tool and wrote the contract JSON directly.
- The MCP caps each response at **~690 bars** (no page-token arg), so the year was
  assembled from **42 windowed pulls per symbol** (30-day spans, 13-day step, `limit=690`),
  run by two background agents, then merged/deduped by timestamp. 1h is **resampled from
  the EH 15m** bars. All files verified: unix-sec UTC, strictly ascending, deduped,
  OHLC-valid, **no gaps > 4 days**.

## Files (all `ALPACA:…`, split-adjusted, asof 2026-06-13, fresh through 2026-06-12)
| file | bars | range | session |
|---|---|---|---|
| `avgo_15m` | 9,776 | 2024-12-11 → 2026-06-12 | **RTH (canonical)** |
| `avgo_15m_eh` | 23,799 | 2024-12-11 → 2026-06-12 | raw + extended hours |
| `avgo_1h` | 6,004 | 2024-12-11 → 2026-06-12 | resampled from EH 15m |
| `avgo_1d` | 1,380 | 2020-12-14 → 2026-06-12 | daily |
| `mrvl_15m` | 9,777 | 2024-12-10 → 2026-06-12 | **RTH (canonical)** |
| `mrvl_15m_eh` | 23,335 | 2024-12-10 → 2026-06-12 | raw + extended hours |
| `mrvl_1h` | 6,003 | 2024-12-10 → 2026-06-12 | resampled from EH 15m |
| `mrvl_1d` | 1,380 | 2020-12-14 → 2026-06-12 | daily |

Canonical `15m` is RTH-filtered (13:30–20:00 UTC) to match the RTH-tuned engine/baseline;
`15m_eh` is the raw Alpaca source (incl. ~64 bars/day extended hours).

## Year-long ghost forward test (`forward_test.py <sym> <tf> 100000` — walks the whole year)
`FORWARD` was widened (optional 3rd CLI arg; default 260 unchanged) so the test forecasts
across **all ~376 trading days** instead of only the most recent ~260 candles. ROLL=400
lookback / RESOLVE=32 horizon unchanged.

| run | candles | STALE | usable (HIT/INVAL) | TARGET-HIT (usable) | next-candle DIR |
|---|---|---|---|---|---|
| **AVGO 15m (RTH)** | 9,344 | 16% (1500) | 1367 (558/809) | **41%** | **50%** of 8,244 |
| **MRVL 15m (RTH)** | 9,345 | 27% (2500) | 1718 (755/963) | **44%** | **51%** of 9,240 |
| AVGO 15m_eh | 23,367 | 9% (2079) | 1147 (439/708) | 38% | 51% of 10,653 |
| MRVL 15m_eh | 22,903 | 18% (4100) | 2041 (891/1150) | 44% | 51% of 16,803 |

For contrast, the same engine on the prior **30-day** windows (a sharp June reversal):
STALE 45–86%, target-hit 0–26%, dir 45–50%.

## Honest read (now on a large, multi-regime sample)
- **No directional edge — robustly.** Next-candle direction is **50–51%** in every run,
  over 8,000–17,000 observations. That is a coin flip on a sample large enough to trust.
- **Targets miss more than they hit.** Target-hit among usable forecasts is **38–44%**, and
  INVALIDATED outnumbers HIT in all four runs (e.g. AVGO RTH 558 vs 809). Net negative skew;
  the closer-than-stop targets (R:R < 1, per `SESSION_HANDOFF`) don't rescue it.
- **The 30-day "all-stale" scare was regime, not the data.** Over a full year STALE falls to
  **9–27%** (vs 45–86% in the late-May→June reversal window). The engine produces usable
  forecasts most of the time; the earlier spike was the fast reversal lagging the confirmed
  pivot, not a data/feed problem. RTH vs EH stale stays inconsistent across symbols, so
  session structure is a second-order effect.
- **Bottom line:** large-sample forward testing confirms `SESSION_HANDOFF`'s standing
  conclusion — applying the tools professionally yields correct *counts* but **no tradeable
  directional edge** on this evidence.

## Caveats / notes for DEV
- `avgo_1d/mrvl_1d` still span 2020→2026 (1,380 bars) from the earlier pull — not re-fetched
  this round (MCP 690/call cap; extend via more windows or REST for deeper daily history).
- `15m_eh` runs carry many `no-forecast`/`OPEN` candles (thin overnight bars) — expect lower
  resolved counts there despite more total candles.
- `alpaca_fetch.py` applies no session filter, so a live REST pull lands EH bars in the `15m`
  slot; to reproduce the RTH numbers above, filter to RTH or scale ROLL/FORWARD with density.
