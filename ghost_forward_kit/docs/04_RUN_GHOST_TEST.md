# 04 — Run the test and read the results

## Run the forward test
```bash
python3 ghost_forward.py --data ../data/live/avgo_15m_2026-06.json \
        --forecaster forecasters/wavelib_adapter.py:forecast \
        --roll 400 --forward all --resolve 32 --out ../reports/GHOST_TEST_AVGO_15m.md
```
| flag | meaning | default |
|---|---|---|
| `--data` | bars JSON (contract from doc 02) | – |
| `--forecaster` | `file.py:func` or `dotted.module:func` (doc 03) | – |
| `--roll` | bars of history handed to the forecaster each step | 400 |
| `--forward` | how many recent candles to test, or `all` for the whole series | all |
| `--resolve` | ghost-feed horizon (bars) to resolve each call | 32 |
| `--out` | report path | `GHOST_TEST_<data>.md` |

It prints the Summary and writes a Markdown report with a sampled forecast log.

## Read the summary
```
- STALE/unusable: 1500 of 9344 (16%)        ← calls discarded as degenerate (see below)
- Usable resolved: 1367 (HIT 558 / INVALIDATED 809); OPEN 5377; no-forecast 1100
- Target-hit among usable: 41%              ← of resolved calls, how many hit target first
- Next-candle directional accuracy: 50% of 8244   ← the cleanest edge signal; 50% = none
```
- **Next-candle direction** is the least forgiving, least gameable number. **~50% = no
  directional edge**, full stop. Treat this as the headline.
- **Target-hit among usable** depends on how far you place target vs stop (your R:R). A high
  hit-rate with target ≪ stop is not an edge. Read it next to direction.
- **STALE** = the call was unusable the instant it was made (target/invalidation already on
  the wrong side of price). High stale ⇒ your anchor lags price (often in fast moves).
- **OPEN** = neither target nor stop reached within `--resolve`. Lots of OPEN ⇒ targets too
  far for the horizon (raise `--resolve` or pull targets in).

## Run the diagnostic — *why*
```bash
python3 ghost_diag.py --data ../data/live/avgo_15m_2026-06.json \
        --forecaster forecasters/wavelib_adapter.py:forecast --roll 400 --resolve 32
```
It prints three things that locate the problem:
1. **By `kind`** — count, %up, next-candle accuracy, HIT/INVAL/stale/OPEN per setup type.
   (e.g. it revealed one branch that was *100% stale* — pure dead weight.)
2. **Trend-agreement split** — next-candle accuracy when the call *agrees* vs *disagrees*
   with the recent trend. If both ≈ 50%, the **direction carries no information** (it's a
   mechanical reflex, not a prediction).
3. **By confidence bucket** + **median bars-to-resolution**. If accuracy is flat across
   confidence buckets, the model can't tell its good calls from its bad ones. If INVALIDATED
   resolves faster than HIT, your stop is tighter than your target (negative skew).

## What "good" looks like
- Next-candle direction **clearly > 50%** (e.g. 54–60%) and **stable across regimes**.
- The edge **concentrated in a `kind`** you can name and gate on.
- **Confidence monotonic** with accuracy (higher conf → better).
- Target-hit > 50% **with R:R ≥ 1** (target at least as far as the stop).

If you don't see these, the diagnostic tells you where to fix the *signal* — not the data.

## Validate the harness on your project
Wrap your existing model (doc 03) and confirm the kit reproduces your own backtest's
direction number. In this repo, `wavelib_adapter.py` reproduces the project's forward test
exactly — that's your proof the harness is faithful before you trust new experiments.

Next: **`05_METHODOLOGY.md`**.
