# DASHBOARD_ARCHITECTURE.md — self-hosted scanner portal + analysis agent

> **Purpose of this document.** A complete, hand-off-ready plan for a **local
> Claude session** (one that has this repo checked out AND access to your local
> data lake) to build the end-to-end system: an automated multi-cadence scanner
> over your full symbol universe, a self-hosted web portal that lists the ranked
> opportunities, and a **project-trained analysis agent** that writes the
> trader-facing analysis for each flagged stock on demand.
>
> This session runs in a cloud sandbox with **no access to your data lake**, so
> it writes the spec; the local session executes it. Everything here is grounded
> in the existing `src/ewave` codebase — module names, function signatures, and
> data contracts below are real, not aspirational.

---

## 0. The one-paragraph summary

The Elliott/NeoWave engine (`src/ewave`) already turns bars into **frozen,
causal trade signals** with entry/stop/targets/R:R (`ewave.scanner.batch.scan`
→ `Signal`). This project adds three things around it, all on the local host:
(1) a **scheduler** that runs the scan across your whole lake universe at four
cadences (15m / 1h / 1d / 1w) and writes ranked result files; (2) a **FastAPI +
web portal** that serves those results as a sortable dashboard and, per symbol,
an analysis page (honest visual + trade plan + backtest history); (3) a
**headless `wave-analyst` Claude agent** that *narrates the engine's
deterministic output* into plain language for the flagged symbols — it never
invents or overrides a signal. The engine decides; the agent explains.

---

## 1. Non-negotiable design principles (carry these into every component)

These come straight from `CLAUDE.md` and the trust work already done. The portal
is worthless if it quietly re-introduces the dishonesty we removed.

1. **The engine decides, the agent explains.** Opportunities come ONLY from the
   deterministic rule engine (`wave3.generate` / `scanner.batch.scan`). The
   `wave-analyst` agent is a *translator*: it reads the engine's output and
   writes prose. It may not add, remove, re-rank, or override a signal. Every
   claim on a page must trace to a rule check, a `Signal` field, or a backtest
   number.
2. **Honesty over confidence.** Show `Status.UNKNOWN` when data is thin. The
   honest-label discipline (`html_report.py`: number a wave count ONLY when a
   rule-clean 5-wave impulse exists, else show swings) MUST be preserved in the
   portal charts. A symbol with no validated structure is shown as such.
3. **No lookahead.** The portal only ever reads causal, confirmed data
   (`confirmed_t` discipline, `docs/NO_LOOKAHEAD_POLICY.md`). Intraday refresh
   uses the last CLOSED bar, never the forming one.
4. **Live trading fails closed.** The portal is **decision support, not an
   executor.** No order-placement path ships. Risk/sizing stays out
   (`docs/LIVE_TRADING_SAFETY_POLICY.md`). Buttons that look like "trade" must
   not exist.
5. **Universe honesty gate.** The +0.24R edge is validated on **12 liquid semis
   at 1h** (`docs/research/HOURLY_TRACK.md`). Any symbol outside that set is an
   *extrapolation*. The portal must visibly badge a symbol's signal as
   `VALIDATED` (in the backtested set) vs `UNVALIDATED — extrapolated` until a
   re-validation run covers it (see §7).

---

## 2. System architecture (five layers)

```
                    ┌───────────────────────────────────────────────┐
                    │                LOCAL HOST                      │
                    │                                                │
  your data lake ──▶│  ① DATA LAYER                                  │
  (OHLCV files/db)  │     ewave.data.store.Store                    │
                    │     via EWAVE_STORE_DIR  ─or─ LakeAdapter      │
                    │     universe.py  (list all symbols×tf in lake) │
                    │                    │                           │
                    │                    ▼                           │
                    │  ② SCAN ENGINE (reuse, unchanged)              │
                    │     scanner.batch.scan(symbols, tf, profile)  │
                    │     → List[Signal]  → SignalStore (frozen)     │
                    │                    │                           │
                    │                    ▼                           │
                    │  ③ RANK + PERSIST                              │
                    │     rank.py → scan_results/<tf>_<run>.json    │
                    │     (composite score; per-symbol edge weight)  │
                    │                    │                           │
                    │         ┌──────────┴──────────┐                │
                    │         ▼                     ▼                │
                    │  ④ ANALYSIS AGENT       ⑤ WEB PORTAL           │
                    │   wave-analyst (Claude)   FastAPI + frontend  │
                    │   narrates each hit  ───▶  /api/scan/latest   │
                    │   → analysis/<sym>.json    /api/symbol/{sym}  │
                    │                            Dashboard → detail  │
                    │                                                │
                    │  ⑥ SCHEDULER: cron/systemd/APScheduler         │
                    │     15m ▸ 1h ▸ 1d ▸ 1w  each: refresh→scan→    │
                    │     rank→analyse(hits)→publish artifacts       │
                    └───────────────────────────────────────────────┘
                                     │
                                     ▼
                          you: open portal, pick a stock,
                          read the engine's read + agent's analysis
```

### Layer ① — Data (the ONLY integration you must write)

The engine reads bars through `ewave.data.store.Store`, which resolves its
directory in this order (see `src/ewave/data/store.py`):

1. `EWAVE_STORE_DIR` environment variable, else
2. `./data/live`, else a parent's `data/live`.

Files use the contract name `**<slug>_<tf>_<stamp>.json**` where
`slug = lowercase bare ticker`, `tf ∈ {15m,1h,1d,1w}`, `stamp = YYYY-MM`, and
the body is `{"symbol","interval","asof","bars":[{t,o,h,l,c,v}]}`, `t` = unix
seconds UTC ascending, split-adjusted.

**Two integration options — pick based on your lake's shape:**

- **(A) Point-and-go (recommended if your lake is/near contract-JSON).** Set
  `EWAVE_STORE_DIR=/path/to/lake` and run a one-time normalizer that writes lake
  data into the contract filenames. Zero engine changes.
- **(B) `LakeAdapter` (if your lake is a DB / parquet / different schema).**
  Write `src/ewave/data/adapters/lake.py` implementing the existing adapter
  interface (see `data/adapters/` for the contract adapter as the template):
  `read(symbol, tf) -> BarSeries`. Then a thin `LakeStore(Store)` subclass whose
  `read()` calls the adapter. Keep it behind an import guard so the pure-stdlib
  core still works without the lake.

**`universe.py` (new, `src/ewave/scanner/universe.py`):** enumerate every
`(symbol, tf)` available in the lake. `Store.list()` already returns all
contract files sorted by `(slug, tf, stamp)` — for option (A) the universe is
`{parse(f) for f in store.list()}`. For option (B), query the lake directly.
Expose `universe(tf) -> list[str]` and `all_symbols() -> list[str]`.

### Layer ② — Scan engine (reuse verbatim, no changes)

`ewave.scanner.batch.scan(symbols, tf, profile_name, store, signal_store)`
already:
- reads cached bars per symbol,
- runs `wave3.generate(bars, profile, symbol, tf)` (the validated wave-3
  confirmation signal),
- attaches `tree_context` (macro count confidence),
- **freezes** any signals to `SignalStore` (`outputs/signals/<day>.jsonl`,
  append-only) and writes `latest_signals.{json,csv}`,
- returns `{"profile","timeframe","symbols_scanned","signals":[Signal...],
  "errors":[...]}`.

The scheduler calls this once per (cadence-tf, profile). **Profiles available**
(`configs/profiles.json`): `experimental` (crude, more trades), `sow_neowave_soft`,
`sow_neowave_strict` (RULESET §H, few high-quality trades), `classic_elliott`.
Default the dashboard to `experimental` for coverage and let the user filter to
`strict` for high-conviction only.

### Layer ③ — Rank + persist

New: `src/ewave/scanner/rank.py`. Input: the `scan()` result's `signals`.
Output: `outputs/scan_results/<tf>_<runstamp>.json` — a ranked, portal-ready
list. Each row is the `Signal.to_dict()` PLUS derived display fields:

```jsonc
{
  "run": {"tf": "1h", "profile": "experimental", "asof": 1753600000,
          "universe": 512, "hits": 7, "generated": "2026-07-27T21:05:00Z"},
  "signals": [
    {
      // --- straight from Signal.to_dict() ---
      "symbol": "MU", "timeframe": "1h", "direction": "long",
      "entry_price": 118.4, "stop_price": 112.9,
      "targets": [["1.618x W1", 131.2]], "reward_risk": 2.1,
      "confluence_strands": 3, "tree_confidence": 0.52,
      "stability_score": null, "setup_confirmed_t": 1753500000,
      "signal_time": 1753560000, "invalidation_level": 112.9,
      // --- derived by rank.py ---
      "rank_score": 0.78,           // composite (see formula)
      "edge_class": "VALIDATED",    // VALIDATED | UNVALIDATED (see §7)
      "hist_expectancy_r": 0.31,    // this symbol's backtest R (if any)
      "count_ok": false,            // honest-label gate for the chart
      "analysis_ref": "analysis/mu_1h_<run>.json"  // filled by layer ④
    }
  ]
}
```

**Composite `rank_score`** (transparent, tunable — document the weights in the
file header so nothing is a black box):

```
rank_score =  0.35 * confluence_strands / max_strands
            + 0.25 * clamp(reward_risk / 3, 0, 1)
            + 0.20 * (tree_confidence or 0)
            + 0.20 * edge_weight       # 1.0 if VALIDATED & hist R>0, else 0.3
```

Sorting is by `rank_score` desc; `edge_class=UNVALIDATED` rows sink and are
visibly badged. `hist_expectancy_r` is looked up per symbol from
`registry/trials.jsonl` (the append-only DSR trial registry) — if the symbol was
never backtested, it's `null` and `edge_class=UNVALIDATED`.

### Layer ④ — Analysis agent (`wave-analyst`)

A **headless Claude agent** invoked by the scheduler ONLY for symbols that
produced a signal this run (not the whole universe — cost control). Definition
lives at `.claude/agents/wave-analyst.md` (drafted in this repo — see that file).

Contract:
- **Input** (assembled by `src/ewave/agent/analysis_brief.py`, new): a JSON brief
  = the ranked `Signal` row + the per-symbol rule-check results
  (`patterns.candidates.label_and_validate` / `rules.*` outputs) + the honest
  chart data (`html_report.analyze_symbol` returns `count_ok`, `count_note`,
  pivots, targets, zone, and the six analysis cards) + the symbol's backtest
  stats from `registry/trials.jsonl` + recent journal rows
  (`reporting.journal.build_records`).
- **Output**: `outputs/analysis/<slug>_<tf>_<run>.json`:
  `{"verdict","setup","levels","why","caveats","confidence_label","provenance"}`
  — plain-language, every field traceable. Rendered as the "Analyst read" card
  on the detail page.
- **Hard rule**: the agent gets the engine output as GROUND TRUTH and may only
  summarize/explain it. It cannot emit a BUY/SELL it wasn't handed, cannot
  invent levels, cannot upgrade confidence. See the agent def for the full
  guardrail prompt.

**Two invocation modes** (build both; the portal offers "on-demand"):
- **Batch (scheduler):** after each scan, generate analyses for the top-N hits
  so the dashboard is warm.
- **On-demand (portal):** when you open a symbol whose analysis is stale/missing,
  the backend enqueues a `wave-analyst` run and streams the result. Cache by
  `(symbol, tf, run)` so repeat views are free.

Use the Claude Agent SDK / `claude` CLI in headless mode from Python
(`subprocess` or the SDK). Keep the API key in the local env, never in the repo.

### Layer ⑤ — Web portal (FastAPI backend + frontend)

**Backend** (`web/app.py`, FastAPI):

| Endpoint | Returns |
|---|---|
| `GET /api/scan/latest?tf=1h&profile=experimental` | latest `scan_results/<tf>_*.json` (ranked rows) |
| `GET /api/scan/history?tf=1h&limit=30` | recent runs (for a "new since last run" diff) |
| `GET /api/symbol/{sym}?tf=1h` | analysis JSON + chart data + trade plan + backtest stats + journal rows |
| `GET /api/symbol/{sym}/chart?tf=1h` | `html_report.analyze_symbol()` payload (honest pivots/targets/zone) |
| `POST /api/symbol/{sym}/analyse` | trigger an on-demand `wave-analyst` run; returns job id |
| `GET /api/backtest/{sym}` | that symbol's trials from `registry/trials.jsonl` |
| `GET /api/health` | data freshness per cadence, last run times, universe size |

**Frontend** (React or server-rendered — your call; React if you want live
sorting/filtering):

- **Dashboard page** (`/`): four cadence tabs (Intraday 15m · Hourly 1h · Daily
  1d · Weekly 1w). Each shows the ranked opportunity table: Symbol · Dir · Entry ·
  Stop · Targets · R:R · Confluence · Rank · Edge badge (`VALIDATED` green /
  `UNVALIDATED` amber). Sortable columns; filter by profile, direction, edge
  class, min R:R. A "new this run" highlight. Empty state is explicit: "No
  structural setups on 512 symbols this run — sit out." (silence is a feature).
- **Symbol detail page** (`/symbol/MU?tf=1h`): reuse the existing honest visual
  (embed `html_report` output or re-render from `/chart`), the trade-plan card
  (entry/stop/targets/R:R/invalidation), the **Analyst read** card (from
  `wave-analyst`), the confluence-strand breakdown, the backtest stats for this
  symbol (expectancy, win rate, trade count, DSR), and the journal history
  (past signals + outcomes). Header badge = edge class + "decision support, not
  advice, not an order."

### Layer ⑥ — Scheduler

Four independent jobs. Each runs: **refresh lake slice → scan universe(tf) →
rank → analyse top-N hits → write artifacts**.

| Track | tf | Trigger | Notes |
|---|---|---|---|
| Intraday | 15m | every 15 min during RTH | heaviest; last CLOSED bar only |
| Hourly | 1h | every hour during RTH | the validated timeframe — primary |
| Daily | 1d | once after US close (~21:30 UTC) | next-session watchlist |
| Weekly | 1w | Fri after close | position-trading cadence |

Implementation: `cron` / `systemd timers` (robust, survives reboot) or
APScheduler inside a long-running worker. Each job is
`python -m ewave_portal.jobs.run --tf 1h --profile experimental`. Make jobs
idempotent (keyed by run stamp) and log to `registry/logs/`.

---

## 3. Repository / directory layout to create (on local)

```
src/ewave/scanner/universe.py        # enumerate lake symbols×tf         (NEW)
src/ewave/scanner/rank.py            # composite ranking → scan_results  (NEW)
src/ewave/data/adapters/lake.py      # ONLY if lake ≠ contract-JSON      (NEW, opt)
src/ewave/agent/analysis_brief.py    # assemble the agent input brief    (NEW)
src/ewave/agent/wave_analyst.py      # headless-Claude invocation wrapper(NEW)
.claude/agents/wave-analyst.md       # the trained analysis agent def    (DRAFTED HERE)
web/app.py                           # FastAPI backend                   (NEW)
web/frontend/                        # React (or Jinja templates)        (NEW)
ewave_portal/jobs/run.py             # one scheduler job                 (NEW)
deploy/systemd/ or deploy/cron/      # the four timers                   (NEW)
outputs/scan_results/<tf>_<run>.json # ranked results (served)           (RUNTIME)
outputs/analysis/<slug>_<tf>_<run>.json # agent narratives (served)      (RUNTIME)
```

Reused unchanged: `ewave.scanner.batch`, `ewave.signals.wave3`,
`ewave.signals.models.Signal`, `ewave.signals.store.SignalStore`,
`ewave.reporting.html_report`, `ewave.reporting.journal`,
`ewave.patterns.*`, `ewave.rules.*`, `registry/trials.jsonl`.

---

## 4. Build phases (each ends with a concrete acceptance check)

**Phase A — Data seam.** Wire the lake. Acceptance:
`EWAVE_STORE_DIR=<lake> python -c "from ewave.scanner.universe import all_symbols; print(len(all_symbols()))"` prints your real symbol count; `ewave validate-data --all` passes on a sample.

**Phase B — Universe scan + rank.** `universe.py` + `rank.py`. Acceptance:
`python -m ewave_portal.jobs.run --tf 1h` writes a `scan_results/1h_*.json` whose
rows are sorted by `rank_score` and carry correct `edge_class` badges;
cross-check counts against a manual `ewave scan`.

**Phase C — Web portal (read-only).** FastAPI + dashboard + detail, served from
the JSON artifacts. Acceptance: open `/`, see the four cadence tabs and ranked
tables; click a symbol → detail page shows the honest chart + trade plan +
backtest stats. No analyst card yet.

**Phase D — Analysis agent.** `.claude/agents/wave-analyst.md` +
`analysis_brief.py` + `wave_analyst.py` + on-demand endpoint. Acceptance: opening
a flagged symbol renders an "Analyst read" whose every level/number matches the
engine's `Signal`; feed it a symbol with NO signal → it must refuse to
manufacture one ("no structural setup — nothing to analyse").

**Phase E — Scheduler.** Four timers. Acceptance: leave it running a full
session; dashboard auto-refreshes per cadence; `/api/health` shows fresh
timestamps; logs in `registry/logs/`.

**Phase F — Universe re-validation (the honesty gate).** Before trusting signals
on the wider universe, run `ewave backtest` + `ewave ghost-forward` across it and
extend `registry/trials.jsonl`; promote symbols to `edge_class=VALIDATED` only
where DSR + MinTRL support it. Acceptance: `docs/research/UNIVERSE_VALIDATION.md`
records which symbols earned VALIDATED and which stay extrapolated.

---

## 5. Data-flow contract (so components stay decoupled)

```
lake ──Store/LakeAdapter──▶ bars(sym,tf)
bars ──wave3.generate────▶ Signal[]  ──SignalStore.append──▶ frozen ledger
Signal[] ──rank.py───────▶ scan_results/<tf>_<run>.json   (portal reads this)
hit rows ──analysis_brief─▶ brief.json ──wave-analyst────▶ analysis/<sym>.json
FastAPI ──serves────────▶ scan_results + analysis + html_report chart payload
scheduler ──drives────────▶ the whole chain per cadence
```

Every arrow is a file or a function call that already exists or is specified
above. No component reaches past its neighbor.

---

## 6. The analysis agent, in one screen (full def in `.claude/agents/wave-analyst.md`)

- **Identity:** a NeoWave/Elliott desk analyst that reads THIS project's engine
  output and explains it. Grounded on `docs/RULESET.md`, `docs/RULE_COVERAGE.md`,
  `docs/WAVE3_RESULT.md`, `docs/research/SOW_METHOD.md`,
  `docs/research/HOURLY_TRACK.md`.
- **Gets:** the engine brief (signal + rule results + honest chart + backtest +
  journal). **Emits:** verdict, setup, levels, why, caveats, confidence label.
- **Must:** cite the rule/strand/backtest behind every claim; say UNKNOWN when
  thin; state the edge class honestly; repeat "decision support, not an order."
- **Must NOT:** invent a signal, change a level, upgrade confidence, give sizing
  advice, or reference the forming (unconfirmed) bar.

---

## 7. Honest caveats to surface in the product (not hide in docs)

1. **Validated ≠ everywhere.** Only the backtested set carries the +0.24R
   evidence. Everything else is badged UNVALIDATED until Phase F covers it.
2. **The edge is portfolio-level and modest.** Win rate ~46%, PF ~1.44. Some
   symbols lose individually. The product must not imply per-trade certainty.
3. **Silence is the common output.** Most symbols, most runs → no signal. The
   dashboard's empty state is the honest default, not an error.
4. **Decision support only.** No executor, no sizing, live gates stay closed.

---

## 8. Kickoff prompt for the local session

Copy-paste into the local Claude session (it must have the repo + lake):
see **`docs/LOCAL_SESSION_HANDOFF.md`** in this repo for the ready-to-paste
brief and the ordered task list.
