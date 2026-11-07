# Wave-3 entry — forward test on refreshed data (snapshot 2026-11)

_Generated 2026-11-07 by `scripts/forward_wave3.py ... --tag 2026-11`. Causal ghost-feed of
`wave3_signal` (confirmation break of wave-1 after a valid wave-2; stop = wave-2 extreme;
target 1.618× wave-1; EWO-gated) and `wave3_signal_strict` (+ NeoWave :5 pattern-ID on W1,
≥3 confluence strands, R:R ≥ 2, S&B time budget, scale-out). Expectancy in R. Not advice._

## 1. Data actually available (step 1 of the plan)

| series | source | span | bars | note |
|---|---|---|---|---|
| 15m | Yahoo via `data/fetch.py` | **2026-08-14 → 2026-11-06** | 1,560 | Yahoo caps 15m at 60 days |
| 1h | Yahoo | **2023-12-11 → 2026-11-06** | 5,077 | 730-day cap; regular session, 7 bars/day |
| 15m (June baseline) | Alpaca | 2024-12-11 → 2026-06-12 | 9,776 | stamps 1h early on EST dates (DST slip) |

- The **15m gap 2026-06-13 → 2026-08-13 cannot be filled** from free sources. Alpaca is
  reachable from this session (answers 401 without keys); with `APCA_API_KEY_ID` /
  `APCA_API_SECRET_KEY` set, `python3 scripts/alpaca_fetch.py AVGO MRVL 15m --tag 2026-11`
  gives the continuous history (10k bars ≈ 15 months of 15m).
- Do not splice June (Alpaca) and November (Yahoo) 15m bars by timestamp without correcting
  the June winter offset (08:30 vs 09:30 first bar).
- The 1h series is the useful long sample: two years on one consistent grid.

## 2. Results

| symbol · tf · mode | trades | expectancy | win | median R:R | breakeven win | P(win ≥ obs ‖ chance) |
|---|---:|---:|---:|---:|---:|---:|
| AVGO 15m normal | 9 | **+0.94 R** | 78% | 1.82 | 35% | 0.012 (n<20) |
| AVGO 15m strict | 0 | — | — | — | — | no signal in 60 days |
| **AVGO 1h normal** | **64** | **+0.30 R** | 50% | 1.69 | 37% | **0.024** |
| AVGO 1h strict | 2 | +1.48 R | 100% | 2.69 | 27% | n<20 |
| MRVL 15m normal | 18 | +0.21 R | 44% | 1.98 | 34% | 0.230 (n<20) |
| MRVL 15m strict | 2 | +0.18 R | 50% | 2.33 | 30% | n<20 |
| **MRVL 1h normal** | **87** | **+0.35 R** | 49% | 1.83 | 35% | **0.005** |
| MRVL 1h strict | 3 | +0.57 R | 67% | 2.72 | 27% | n<20 |

"Breakeven win" = 1/(1+R:R); the last column is the one-sided binomial probability of
seeing at least the observed number of winners if the true win rate were the breakeven
rate (no edge). Only the 1h runs have enough trades to test; both are below 0.05.

## 3. The June baseline, re-run after the ZigZag look-ahead fix

Yesterday's audit (`docs/RULESET.md` §I) removed an intrabar look-ahead from the causal
ZigZag: a bar that set a new extreme could also confirm the reversal of that extreme using
its own range. `wave3_signal` builds on that ZigZag, so the baseline moved:

| AVGO 15m 2024-12 → 2026-06 | before (as pasted) | now |
|---|---:|---:|
| normal: trades / expectancy / win | 79 / +0.17 R / 47% | **59 / +0.26 R / 51%** (p = 0.008) |
| strict: trades / expectancy | 3 / +1.12 R | **4 / +1.19 R** |

Twenty of the original 79 trades existed only because of same-bar confirmation; removing
them raised expectancy. The old numbers should not be quoted any more.

## 4. Read

- **Normal signal, 1h, two years, two symbols: +0.30 R and +0.35 R over 64 and 87 trades,
  win rates 13–14 points above breakeven, p = 0.02 and 0.005.** That is the first result in
  this project with a sample large enough to call it more than noise — on two symbols in
  the same sector over the same period, so it is still one regime, not a universe.
- **Strict signal: 2–4 trades everywhere.** Its expectancy looks better but is untestable.
  The filters (≥3 strands, R:R ≥ 2) are doing what they were meant to and the cost is that
  nothing fires. It needs multi-symbol, multi-year data before it can be judged.
- **15m on 60 days is anecdote** (9 and 18 trades); AVGO's +0.94 R is 8 shorts into a crash.
- Still unverified: out-of-sample across symbols/sectors; cost/slippage (none applied here);
  whether the EWO gate or the structure is carrying the edge (ablation).

## 5. Reproduce

```
python3 data/fetch.py AVGO MRVL --tf 15m 1h            # Yahoo: 60d of 15m, 730d of 1h
python3 scripts/forward_wave3.py avgo 1h 96 0.02 --tag 2026-11
python3 scripts/forward_wave3.py mrvl 1h 96 0.02 strict --tag 2026-11
python3 scripts/forward_wave3.py avgo 15m 96 0.02        # June baseline (2026-06)
```
