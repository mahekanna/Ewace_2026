# LOCAL_SESSION_HANDOFF.md — kickoff brief for the local Claude session

This is the brief to hand a **local Claude Code session** that has (a) this repo
checked out and (b) access to your data lake. It builds the scanner portal +
analysis agent specified in `docs/DASHBOARD_ARCHITECTURE.md`. Read that document
first — it is the source of truth; this file is the execution runbook.

---

## Copy-paste kickoff prompt

> You are building the self-hosted Elliott/NeoWave scanner portal for this repo.
> The full spec is in `docs/DASHBOARD_ARCHITECTURE.md` and the analysis agent is
> pre-defined in `.claude/agents/wave-analyst.md`. Follow the spec's principles
> exactly — especially: **the deterministic engine decides opportunities, the
> `wave-analyst` agent only explains them**; the honest-label chart discipline
> must be preserved; the portal is **decision support, not an executor** (no
> order path, no sizing); and symbols outside the backtested set are badged
> `UNVALIDATED` until re-validation.
>
> My data lake is at: `______________________` (fill in). Its format is:
> `______________________` (contract-JSON files / parquet / TimescaleDB /
> other — describe schema and how to read OHLCV per symbol+timeframe).
>
> Work through Phases A–F from the spec, in order. After each phase, run its
> acceptance check and show me the result before moving on. Start with Phase A
> (wire the data seam) and confirm the universe size against my lake before
> touching anything else. Keep the existing test suite green
> (`python3 -m unittest discover -s tests -p "test_*.py"`) throughout.

---

## Before you start — three things to confirm with me

1. **Lake path + schema.** Where is the data, and how is OHLCV stored per
   `(symbol, timeframe)`? This decides Data-seam **Option A** (point
   `EWAVE_STORE_DIR` at normalized contract-JSON) vs **Option B** (write
   `src/ewave/data/adapters/lake.py`). See spec §2 ①.
2. **Frontend flavor.** React (live sort/filter, heavier) or server-rendered
   Jinja (simpler, fine for a personal portal)? Spec §2 ⑤.
3. **Claude for the agent.** Confirm the `claude` CLI / Agent SDK is installed
   locally and `ANTHROPIC_API_KEY` is in the environment (never commit it). The
   `wave-analyst` agent runs headless per flagged symbol.

---

## Ordered task list (mirrors spec §4 — each has an acceptance gate)

- [ ] **Phase A — Data seam.** Option A or B per lake shape. Add
  `src/ewave/scanner/universe.py`. ✅ when
  `EWAVE_STORE_DIR=<lake> python -c "from ewave.scanner.universe import all_symbols; print(len(all_symbols()))"`
  prints the real count and `ewave validate-data --all` passes on a sample.
- [ ] **Phase B — Universe scan + rank.** Add `src/ewave/scanner/rank.py` and
  `ewave_portal/jobs/run.py`. ✅ when `python -m ewave_portal.jobs.run --tf 1h`
  writes a ranked `outputs/scan_results/1h_*.json` matching a manual `ewave scan`.
- [ ] **Phase C — Portal (read-only).** `web/app.py` (FastAPI) + dashboard +
  detail, served from the JSON artifacts, reusing `html_report` for the honest
  chart. ✅ when the four cadence tabs render and a symbol click shows chart +
  trade plan + backtest stats.
- [ ] **Phase D — Analysis agent.** `src/ewave/agent/analysis_brief.py` +
  `src/ewave/agent/wave_analyst.py` + the on-demand endpoint, driving
  `.claude/agents/wave-analyst.md`. ✅ when a flagged symbol shows an "Analyst
  read" whose every number matches the `Signal`, AND a no-signal symbol makes the
  agent refuse to invent one.
- [ ] **Phase E — Scheduler.** Four timers (15m/1h/1d/1w) via cron/systemd. ✅
  when the portal auto-refreshes per cadence and `/api/health` shows fresh
  timestamps.
- [ ] **Phase F — Universe re-validation (honesty gate).** Run `ewave backtest` +
  `ewave ghost-forward` across the wider universe; extend `registry/trials.jsonl`;
  write `docs/research/UNIVERSE_VALIDATION.md`. ✅ when `edge_class=VALIDATED`
  is set ONLY where DSR + MinTRL support it; everything else stays badged
  extrapolated.

---

## Guardrails the local session must not cross (restate from the spec)

- No order-placement / broker-execution code. Live gates stay closed
  (`docs/LIVE_TRADING_SAFETY_POLICY.md`).
- No position-sizing or dollar-risk advice in the portal or the agent output.
- The `wave-analyst` agent may only explain engine output — never add, remove,
  re-rank, or upgrade a signal (`.claude/agents/wave-analyst.md`).
- Preserve the honest-label chart discipline (number a wave count only when a
  rule-clean 5-wave impulse exists) — do not "prettify" it into always showing a
  count.
- Keep secrets out of the repo; keep the pure-stdlib core importable without the
  lake (adapters behind import guards).
