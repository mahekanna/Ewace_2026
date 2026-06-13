# TEST session — fresh Alpaca data + forward-test results (AVGO/MRVL)

_Run 2026-06-13 by the Alpaca-enabled TEST session (see `docs/COLLAB_RUNBOOK.md`).
Causal ghost-feeding forward test; analysis only, not advice._

## Data source
- **Alpaca via MCP** (server `Alpacamn`), `feed=sip`, `adjustment=split`.
- **REST path was NOT available** here: `data.alpaca.markets` returns
  `403 Host not in allowlist` (egress firewall) and `APCA_API_KEY_ID/SECRET` are
  unset — so `scripts/alpaca_fetch.py` could not run. Used the MCP `get_stock_bars`
  tool and wrote the contract JSON directly (per the runbook's MCP-only path).
- **MCP caps each response at ~690 bars** and exposes no page-token argument, so
  history was assembled from multiple `start`/`end`-windowed pulls. 1h aggregates
  to only ~172 bars/page from the endpoint, so **1h here is resampled from the EH
  15m bars** (a 1h bar = the hour's 15m OHLCV). All files verified: timestamps are
  unix-seconds UTC, strictly ascending, deduped, OHLC-valid, prices > 0.

## Files written (all `ALPACA:…`, split-adjusted, asof 2026-06-13, fresh — last bar 2026-06-12)
| file | bars | range (UTC) | session |
|---|---|---|---|
| `avgo_15m_2026-06.json` | 566 | 05-13 → 06-12 19:45 | **RTH only (canonical)** |
| `avgo_15m_eh_2026-06.json` | 1380 | 05-13 → 06-12 23:45 | raw incl. extended hours |
| `avgo_1h_2026-06.json` | 345 | 05-13 → 06-12 23:00 | resampled from EH 15m |
| `avgo_1d_2026-06.json` | 1380 | 2020-12-14 → 2026-06-12 | daily |
| `mrvl_15m_2026-06.json` | 559 | 05-13 → 06-12 19:45 | **RTH only (canonical)** |
| `mrvl_15m_eh_2026-06.json` | 1373 | 05-13 → 06-12 23:45 | raw incl. extended hours |
| `mrvl_1h_2026-06.json` | 344 | 05-13 → 06-12 23:00 | resampled from EH 15m |
| `mrvl_1d_2026-06.json` | 1380 | 2020-12-14 → 2026-06-12 | daily |

Why two 15m variants: Alpaca SIP 15m natively includes **extended hours** (~64
bars/day) whereas the engine + the prior baseline were tuned on **RTH** (~26
bars/day). The canonical `15m` is RTH-filtered (13:30–20:00 UTC) to stay comparable
to the baseline + the RTH-tuned `forward_test.py`; `15m_eh` is the raw source (what
`alpaca_fetch.py` would also produce, since it applies no session filter).

## Forward-test results (`scripts/forward_test.py`, ROLL=400 / FORWARD=260 / RESOLVE=32)
| run | window | candles | STALE | usable (HIT/INVAL) | TARGET-HIT (usable) | next-candle DIR |
|---|---|---|---|---|---|---|
| **AVGO 15m (RTH)** | 06-04 17:30 → 06-11 18:15 | 134 | **60%** (80) | 19 (3/16) | **16%** | **49%** |
| **MRVL 15m (RTH)** | 06-04 19:15 → 06-11 18:15 | 127 | **45%** (57) | 22 (0/22) | **0%** | **50%** |
| AVGO 15m_eh | 06-08 23:00 → 06-12 15:45 | 228 | 86% (196) | 0 (0/0) | n/a (0 usable) | 45% |
| MRVL 15m_eh | 06-08 23:00 → 06-12 15:45 | 228 | 21% (49) | 47 (12/35) | 26% | 49% |

Baseline for contrast (prior tvremix RTH window 05-22 → 06-04, an uptrend):
228 candles, STALE **6%**, usable 86, TARGET-HIT **57%**, DIR **55%**.

## Honest read of the numbers
- **The driver is the market regime, not the data source.** The fresh window
  (Jun 4–12) is a sharp **reversal + high-vol chop**: AVGO 479→386 (−19% in two
  sessions) then 372–397; MRVL 316→263 then 253–291. Trend-projection forecasts
  anchored to the last *confirmed* pivot lag badly when price reverses fast, so
  STALE rises (45–86%) and "up" targets get invalidated. The calm-uptrend baseline
  showed 6% stale / 57% hit on the *same engine* — the difference is the tape.
- **Extended hours is a secondary, inconsistent effect.** If EH density were the
  main cause, EH would always be worse than RTH; instead AVGO is worse on EH (86 vs
  60) but MRVL is *better* on EH (21 vs 45). So EH ≠ the explanation; regime is.
- **No directional edge on this evidence.** Next-candle direction is 45–50%
  (coin-flip or worse) across all four runs; target-hit is 0–26% among usable
  forecasts. This is consistent with `docs/SESSION_HANDOFF.md`'s standing
  conclusion (correct counts, no tradeable edge).
- **Small usable samples** (AVGO 19, MRVL 22 on RTH) — low statistical weight; a
  longer, multi-regime window is needed before drawing edge conclusions.

## Caveats / things that looked off
- **History reduced vs the prior tvremix files** (MCP 690-bar/call cap): 1d
  1380 bars from 2020 (was ~4234 from 2009); 1h 345 bars / ~1 month (was ~5000).
  Daily/15m are split-adjusted & continuous (no split artifact), but high-degree
  daily/1h counts may shift on the shorter history — extend via more windowed MCP
  pulls or REST (10k bars) when the host is allowlisted.
- `*_1w` weekly files were left as the prior tvremix data (1w not requested).
- **Pipeline note for DEV:** `alpaca_fetch.py` has no session filter, so live REST
  pulls will land EH bars (~64/day) into the `15m` slot and reproduce the high-stale
  `15m_eh` behavior. Either add an RTH filter to the fetch, or make the forward-test
  ROLL/FORWARD/RESOLVE scale with bar density, before comparing to the RTH baseline.
