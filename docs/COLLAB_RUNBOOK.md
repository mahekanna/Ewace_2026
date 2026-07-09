# Two-session workflow — develop here, test in the Alpaca session

Branch for everything: **`claude/ewave-2026-base-repo-ZRYzS`**. GitHub is the shared
state, so neither session loses context.

```
  ┌─────────────────────────┐   git push    ┌──────────────────────────────┐
  │ DEV session (this env)  │ ────────────▶ │  GitHub  (the branch)        │
  │ • tvremix data only     │ ◀──────────── │                              │
  │ • writes engine + tests │   git pull    └──────────────────────────────┘
  │ • forward-test on       │                         ▲   │
  │   whatever data exists  │            git pull /   │   │  git push
  └─────────────────────────┘            push results │   ▼
                                          ┌──────────────────────────────────┐
                                          │ TEST session (Alpaca-enabled)    │
                                          │ • Alpaca reachable + allowlisted │
                                          │ • fetches LIVE bars              │
                                          │ • runs forward_test, pushes back │
                                          └──────────────────────────────────┘
```

## TEST session — exact steps (the Alpaca-enabled session)

```bash
git checkout claude/ewave-2026-base-repo-ZRYzS && git pull

# 1) make sure Alpaca keys are set (env), then pull live bars in OUR format:
export APCA_API_KEY_ID=...   APCA_API_SECRET_KEY=...
python3 scripts/alpaca_fetch.py AVGO 15m 1h 1d
python3 scripts/alpaca_fetch.py MRVL 15m 1h 1d
#   -> writes data/live/<sym>_<tf>_2026-06.json (split-adjusted, up to 10k bars)
#   If you have SIP data:  ... AVGO 15m --feed sip

# 2) run the ghost-feeding forward test on the fresh data:
python3 scripts/forward_test.py avgo 15m
python3 scripts/forward_test.py mrvl 15m

# 3) push the data + results back so the dev session can read them:
git add data/live/ reports/FORWARD_TEST_*.md charts/png/forward/
git commit -m "test: fresh Alpaca data + forward-test results"
git push origin claude/ewave-2026-base-repo-ZRYzS
```

If the Alpaca MCP is the only way you have data (no REST keys), use the MCP's
get-bars tool and save the result into `data/live/<sym>_<tf>_2026-06.json` in the
shape below — that's all the dev tools need.

## DEV session — exact steps (here)

```bash
git pull origin claude/ewave-2026-base-repo-ZRYzS   # pick up fresh data + results
# ... improve the engine (wavelib/), commit, push ...
git push origin claude/ewave-2026-base-repo-ZRYzS
```

## The data contract (must match exactly)

`data/live/<slug>_<tf>_2026-06.json` where `<slug>` = lowercase ticker, `<tf>` ∈
`{15m,1h,4h,1d,1w}`:

```json
{
  "symbol": "ALPACA:AVGO",
  "interval": "15m",
  "asof": "2026-06-13",
  "bars": [ {"t": 1733412600, "o": 384.1, "h": 385.0, "l": 383.2, "c": 384.7, "v": 12000}, ... ]
}
```
- `t` = **unix seconds (UTC)**, bars **ascending** by time.
- Prices **split-adjusted** (Alpaca `adjustment=split`) — keeps a continuous series.

## Division of labour
- **DEV (here):** engine (`wavelib/`), tests, scripts, analysis on existing data.
  Cannot reach Alpaca (firewall + no MCP) — so never depends on live data landing.
- **TEST (Alpaca session):** fetch live bars, run `forward_test.py` / future live
  loop, push data + reports. Doesn't need to touch engine code.
- **Bridge:** the branch. Pull before you start, push when you finish, small commits.

## Open next steps (see docs/SESSION_HANDOFF.md)
1. Improve R:R (targets nearer parity with the structural stop) — caps the edge now.
2. Add the confluence/momentum gate to forward entries, then re-ghost-feed.
3. Truly LIVE loop in the test session: forecast → wait for next real candle →
   self-evaluate → append to a running forward-test ledger, push.
4. Multi-symbol, longer-window forward test for a real sample.

---

## Platform update (2026-07): the `ewave` CLI supersedes the ad-hoc scripts

Everything above still works — the data contract and branch workflow are
unchanged. The platform now also provides first-class commands:

```bash
pip install -e .                                   # or run bare: wavelib bootstraps src/

# TEST session (network + keys):
ewave fetch-data --adapter alpaca --symbols AVGO,MRVL --tf 15m    # same contract JSON
ewave validate-data --all

# Sandbox sessions (market hosts proxy-blocked): fetch via MCP finance tools,
# save the raw payload, then normalize into the store:
python3 scripts/mcp_export.py --format fmp|yf|tv|alpaca-mcp \
        --symbol AVGO --tf 1h payload.json          # -> data/live/avgo_1h_<YYYY-MM>.json

# then anywhere:
ewave scan --watchlist default --tf 15m --profile experimental
ewave ghost-forward --symbols AVGO --tf 15m --profile experimental --horizon 96
ewave backtest --symbols AVGO,MRVL --tf 15m --profile experimental
ewave paper-trade --replay --watchlist default --tf 15m --days 120
```

Profiles live in `configs/profiles.json` (experimental = the validated crude
wave-3 entry; sow_neowave_strict = RULESET §H; sow_neowave_soft = the research
sweep's starting point). Every backtest logs a trial to registry/trials.jsonl —
commit it with your results.
