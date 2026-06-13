# 02 — Get bars into the contract

Everything downstream reads one shape. Produce it however you like.

## The bars contract
```json
{
  "symbol": "ALPACA:AVGO",
  "interval": "15m",
  "asof": "2026-06-13",
  "bars": [
    {"t": 1733412600, "o": 384.1, "h": 385.0, "l": 383.2, "c": 384.7, "v": 12000},
    {"t": 1733413500, "o": 384.7, "h": 386.1, "l": 384.5, "c": 385.9, "v": 9800}
  ]
}
```
Rules: `t` = **unix seconds UTC**, bars **strictly ascending**, no duplicate `t`.
Prefer **split-adjusted** prices (a continuous series). For intraday, decide up front
whether you keep **extended hours** or **regular session only** (RTH) — see "Sessions".

You have three ways to fill it:

## A) Alpaca REST (you have keys + network)
```bash
export APCA_API_KEY_ID=...  APCA_API_SECRET_KEY=...
python3 fetch_alpaca_rest.py AVGO 15m 1h 1d --rth --feed iex --out ../data/live
```
- `--rth` keeps only the US regular session (recommended for intraday).
- `--feed iex` (free) or `sip` (paid, all exchanges).
- Paginates up to `--limit` bars (default 10000), split-adjusted.

## B) Alpaca MCP (no keys, tool-based) — windowed pulls + merge
If you can only reach Alpaca through the MCP `get_stock_bars` tool, it caps each call
at ~690 bars and has no page-token argument, so you fetch a **year in windows** and
merge. Each large MCP result is auto-saved to disk; `build_from_dumps.py` collects them.

1. Call the tool once per window. Fixed params: `timeframe="15Min"`, `adjustment="split"`,
   `feed="sip"`, `limit=690`, `sort="desc"`, and a moving `start`/`end`. Use **30-day spans
   stepping 13 days** so every call returns a full 690 bars (and so saves to disk) with
   overlap (dedupe handles it). ~42 windows ≈ 1 year. (Tip: have an agent fire the windows.)
2. Merge everything into the contract (auto-detects 15m vs 1h/1d by bar spacing):
   ```bash
   python3 build_from_dumps.py AVGO 15m --dumps /root/.claude/projects --out ../data/live
   ```
   It writes `avgo_15m_*.json` (RTH) and `avgo_15m_eh_*.json` (extended hours), and prints
   counts, the date range, and a `gaps>4d` check. If a gap shows, fetch a window centred on
   it and re-run.

## C) Any other source
Convert whatever you have (CSV, another API, a DataFrame) to the JSON above. Minimal CSV→JSON:
```python
import csv, json, datetime as dt
rows=[]
for r in csv.DictReader(open("ohlcv.csv")):           # columns: time,open,high,low,close,volume
    t=int(dt.datetime.fromisoformat(r["time"]).replace(tzinfo=dt.timezone.utc).timestamp())
    rows.append({"t":t,"o":float(r["open"]),"h":float(r["high"]),
                 "l":float(r["low"]),"c":float(r["close"]),"v":float(r.get("volume",0))})
rows.sort(key=lambda x:x["t"])
json.dump({"symbol":"MYSYM","interval":"15m","asof":"2026-06-13","bars":rows},
          open("data/live/mysym_15m.json","w"))
```

## Sessions (RTH vs extended hours) — pick deliberately
Intraday feeds often include pre/post-market bars (~64/day for US equities vs ~26 RTH).
Mixing them changes bar **density**, which silently changes any constant tuned in *bars*
(like a rolling window). For comparability and to match most backtest tooling, **use RTH
for intraday** unless you specifically want overnight behaviour. Both fetchers above can
emit RTH (`--rth`, or the `_eh` vs non-`_eh` files from `build_from_dumps.py`).

## Freshness & sanity
The harness checks ascending order at load. Before trusting results, confirm: the last bar
is recent, prices are split-adjusted/continuous, and there are no large gaps. `build_from_dumps.py`
prints a gap check; for other sources, eyeball first/last `t` and bar count.

Next: **`03_WRITE_A_FORECASTER.md`**.
