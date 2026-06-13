# Ghost Forward-Testing Kit

A small, **portable, stdlib-only** harness for **causal ghost-feeding forward tests** of
any price forecaster. Drop it into any project: point it at OHLCV bars and a
`forecast(bars) -> Forecast` function, and it walks the series candle-by-candle —
building each forecast from *prior bars only*, then ghost-feeding the next candles to
see whether the call played out. It reports STALE / HIT / INVALIDATED / OPEN, target-hit
rate, and next-candle direction, plus a diagnostic that exposes *why* a signal has (no)
edge.

> Why "ghost feeding"? A normal backtest pools stats and hides the moment of decision.
> This simulates real time: at each candle it makes a live call, then reveals the future
> one bar at a time. It catches failures backtests miss (e.g. a projection that is already
> stale the instant it's made).

## File map
```
ghost_forward_kit/
├── README.md                     ← you are here
├── gf.py                         core: bars contract, Forecast, the causal walk, classifier
├── ghost_forward.py              run a forward test → Markdown report
├── ghost_diag.py                 break a forecaster down by type & confidence (the "why")
├── fetch_alpaca_rest.py          get bars from Alpaca REST (needs keys) → contract JSON
├── build_from_dumps.py           merge Alpaca-MCP get_stock_bars dumps → contract JSON
├── forecasters/
│   ├── example_naive.py          a trivial baseline (shows the contract; ~coin-flip)
│   └── wavelib_adapter.py        example: wrap an existing engine into the contract
└── docs/
    ├── 01_SETUP.md
    ├── 02_FETCH_DATA.md          three ways to get bars into the contract
    ├── 03_WRITE_A_FORECASTER.md  the contract + a worked example
    ├── 04_RUN_GHOST_TEST.md      run it, read the report, run the diagnostic
    └── 05_METHODOLOGY.md         the method, outcome definitions, pitfalls
```

## 60-second quickstart
```bash
# 1. you need a bars JSON (see docs/02). Example shape:
#    {"symbol":"X","interval":"15m","asof":"2026-06-13",
#     "bars":[{"t":1733412600,"o":1,"h":2,"l":0.5,"c":1.5,"v":100}, ...]}

# 2. run the built-in baseline forecaster on it
python3 ghost_forward.py --data path/to/bars.json \
        --forecaster forecasters/example_naive.py:forecast

# 3. see WHY (by-type / by-confidence breakdown)
python3 ghost_diag.py --data path/to/bars.json \
        --forecaster forecasters/example_naive.py:forecast

# 4. swap in YOUR model: copy forecasters/example_naive.py, keep the signature,
#    put your logic inside, and pass --forecaster yourfile.py:forecast
```

## The two contracts you must satisfy
1. **Bars JSON** — `{"symbol","interval","asof","bars":[{t,o,h,l,c,v}]}`, `t` = unix seconds
   UTC, ascending. Any data source works (see `docs/02_FETCH_DATA.md`).
2. **Forecaster** — `forecast(bars) -> Forecast | None`, **causal** (use only the bars given).
   Return a `Forecast(direction, target, invalidation, confidence=, kind=)` or an equivalent
   dict. See `docs/03_WRITE_A_FORECASTER.md`.

Everything is pure Python stdlib — no install step. See `docs/01_SETUP.md`.
