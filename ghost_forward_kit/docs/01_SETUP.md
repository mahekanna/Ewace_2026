# 01 — Setup

## Requirements
- **Python 3.9+** (uses `zoneinfo` for DST-correct RTH filtering; falls back to EDT if absent).
- **No third-party packages.** The whole kit is stdlib. There is nothing to `pip install`.
- Optional: market-data access only if you use the bundled fetchers
  (`fetch_alpaca_rest.py` needs Alpaca keys). You can also bring bars from anywhere.

## Install
Copy the `ghost_forward_kit/` folder into your project. That's it.
```bash
cp -r ghost_forward_kit /path/to/your/project/
cd /path/to/your/project/ghost_forward_kit
python3 ghost_forward.py --help
```

## Layout you'll create
The kit reads/writes plain files; a typical layout:
```
your_project/
├── ghost_forward_kit/        the kit (this folder)
├── data/live/                your bars JSON files  (docs/02)
├── reports/                  generated GHOST_TEST_*.md
└── forecasters/              your forecaster .py files  (docs/03)
```
Paths are arguments, so you can put things wherever you like.

## Sanity check (run the bundled example)
You need one bars JSON to test against. If you don't have data yet, jump to
`docs/02_FETCH_DATA.md`, or make a tiny synthetic file:
```bash
python3 - <<'PY'
import json, math, random
random.seed(1)
bars=[]; t=1_700_000_000; p=100.0
for i in range(1200):
    p *= 1 + random.uniform(-0.01, 0.011)          # mild upward drift + noise
    o=p*(1+random.uniform(-.003,.003)); c=p
    h=max(o,c)*(1+abs(random.uniform(0,.004))); l=min(o,c)*(1-abs(random.uniform(0,.004)))
    bars.append({"t":t,"o":round(o,2),"h":round(h,2),"l":round(l,2),"c":round(c,2),"v":1000})
    t+=900
json.dump({"symbol":"SYN","interval":"15m","asof":"2026-01-01","bars":bars}, open("data/live/syn_15m.json","w"))
print("wrote data/live/syn_15m.json", len(bars), "bars")
PY

python3 ghost_forward.py --data data/live/syn_15m.json \
        --forecaster forecasters/example_naive.py:forecast --roll 300 --resolve 24
```
If that prints a Summary block and writes a `GHOST_TEST_*.md`, you're ready.
Next: **`02_FETCH_DATA.md`**.
