# Extracted rules ledger — project-bundle specs + standalone plan/spec docs

Path shorthand used in SOURCE lines:
- `BX/` = /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle_extract/ElliottWave_Automation_Project_Bundle/ElliottWave_Automation_Project_Bundle/
- `SM/` = /tmp/claude-0/-home-user-Ewace-2026/1a8fcd1b-2017-5973-a7a6-ec0799e5d962/scratchpad/bundle/ElliottWave_All_Conversation_Files_Bundle/02_standalone_markdown_files/

### [AUTOMATION-SPEC] bundle pipeline order
- RULE: The system pipeline is: Bars → Pivots → Mono-waves → Rule validators → Pattern candidates → Ghost-forward validation → TradingView notes.
- TYPE: process
- SOURCE: BX/README.md (§What is included)
- NOTES: v0.1 engineering base built around Alpaca MCP data source, TradingView manual workflow, and Ghost Forward Validation.

### [SCOPE] bundle is not an auto-trading bot
- RULE: The bundle "is **not** an auto-trading bot"; it is a disciplined project scaffold so Codex/Claude can refine one module at a time without getting confused by the full Elliott Wave document library.
- TYPE: scope
- SOURCE: BX/README.md (§intro)

### [DATA] CSV column contract (canonical or abbreviated)
- RULE: CSV columns can be either canonical `timestamp,open,high,low,close,volume` or common API abbreviations `t,o,h,l,c,v`.
- TYPE: hard
- SOURCE: BX/README.md (§Validate a CSV)
- NOTES: Validated via `ewauto validate-csv path/to/TSLA_1D.csv --symbol TSLA --timeframe 1D`.

### [VALIDATION] ghost-forward CSV run defaults
- RULE: Ghost-forward validation on CSV uses `ewauto ghost-forward-csv ... --reversal-pct 3.0 --warmup-bars 100 --horizon-bars 50`; outputs `outputs/reports/<SYMBOL>_<TF>_ghost_forward_signals.csv` and `outputs/reports/<SYMBOL>_<TF>_ghost_forward_outcomes.csv`.
- TYPE: validation
- SOURCE: BX/README.md (§Run ghost-forward validation on CSV)
- NOTES: Example parameters: reversal 3.0%, 100 warmup bars, 50-bar outcome horizon.

### [VALIDATION] most important rule — pivot candle vs signal candle
- RULE: Never confuse the pivot candle with the signal candle: "Pivot happened at index 100. Pivot confirmed at index 105. Signal can start at 105 only, not 100."
- TYPE: hard
- SOURCE: BX/README.md (§Most important rule)
- NOTES: "The whole project is built around this no-lookahead principle."

### [PROCESS-METHOD] one Codex task prompt at a time
- RULE: Do not ask Codex to build everything at once; use one task prompt at a time from prompts/ and docs/codex/, starting with prompts/001_CODEX_CONNECT_ALPACA_MCP.md, then proceed through docs/roadmap/PHASED_BUILD_ROADMAP.md.
- TYPE: process
- SOURCE: BX/README.md (§Recommended Codex workflow)

### [AUTOMATION-SPEC] architecture pipeline stages
- RULE: Pipeline: Alpaca MCP / CSV / Data Lake → Data Adapter → Canonical Bar Schema → Parquet Cache → Pivot Detector → Mono-wave Builder → Rule Validators → Pattern Candidate Scanner → Ghost Forward Replay → Outcome Labeling → TradingView Manual Notes / Reports.
- TYPE: process
- SOURCE: BX/docs/ARCHITECTURE.md (§Pipeline)

### [AUTOMATION-SPEC] package map (ewauto)
- RULE: Package layout: ewauto/data (schema.py, cache.py, sessions.py, adapters/{base,csv_adapter,alpaca_mcp_adapter}.py), ewauto/pivots (models.py, percent_reversal.py, fractal.py), ewauto/waves/monowave.py, ewauto/rules ({result,fibonacci,impulse,corrective}.py), ewauto/patterns/candidates.py, ewauto/validation/ghost_forward ({snapshot,replay_engine,outcome_labeler,metrics}.py), ewauto/charts/tradingview_notes.py.
- TYPE: setup
- SOURCE: BX/docs/ARCHITECTURE.md (§Package map)

### [VALIDATION] design principle 1 — no lookahead
- RULE: "No lookahead: every pivot and signal must have a confirmation index."
- TYPE: hard
- SOURCE: BX/docs/ARCHITECTURE.md (§Design principles)

### [SCOPE] design principle 2 — detection is not trading
- RULE: "Detection is not trading: wave candidates are research objects, not orders."
- TYPE: scope
- SOURCE: BX/docs/ARCHITECTURE.md (§Design principles)

### [AUTOMATION-SPEC] design principle 3 — explicit rule statuses
- RULE: "Rules are explicit: every rule returns PASS, FAIL, WARN, or UNKNOWN."
- TYPE: hard
- SOURCE: BX/docs/ARCHITECTURE.md (§Design principles)

### [PROCESS-METHOD] design principles 4–5 — one pattern at a time, limited context
- RULE: "One pattern at a time: do not implement all NeoWave patterns in one task." and "Codex gets limited context: each coding task should load only relevant specs and files."
- TYPE: process
- SOURCE: BX/docs/ARCHITECTURE.md (§Design principles)

### [AUTOMATION-SPEC] bundle file inventory
- RULE: Bundle contains root (README.md, pyproject.toml, requirements.txt, configs/default.yml), 22 code files under ewauto/, 6 test files (test_schema, test_percent_pivots, test_fractal_pivots, test_monowaves, test_rules, test_ghost_forward), and 5 prompt files (001–005).
- TYPE: setup
- SOURCE: BX/docs/BUNDLE_FILE_INDEX.md (§Root/Code/Tests/Prompts)

### [DATA] data-lake independence via adapters
- RULE: "The active code should not depend directly on a specific data lake layout. Use adapters and canonical schema."
- TYPE: hard
- SOURCE: BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§intro)

### [DATA] canonical bars — required and optional columns
- RULE: Required columns: timestamp, open, high, low, close, volume. Optional columns: vwap, symbol, timeframe, session_type, source.
- TYPE: hard
- SOURCE: BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Canonical bars)

### [DATA] recommended data lake layout
- RULE: data_lake/ layout: raw/alpaca/SYMBOL/TIMEFRAME/*.json; normalized/bars/SYMBOL/SYMBOL_TIMEFRAME_full.parquet; features/pivots/ and features/monowaves/; validation/ghost_forward/.
- TYPE: setup
- SOURCE: BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Recommended data lake layout)

### [DATA] data lake rule 1 — raw data immutable
- RULE: "Raw data is immutable."
- TYPE: hard
- SOURCE: BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Rules)

### [DATA] data lake rule 2 — normalized reproducible from raw
- RULE: "Normalized bars are reproducible from raw data."
- TYPE: hard
- SOURCE: BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Rules)

### [DATA] data lake rule 3 — feature outputs carry config metadata
- RULE: "Feature outputs must include config metadata."
- TYPE: hard
- SOURCE: BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Rules)

### [VALIDATION] data lake rule 4 — snapshots carry timestamp + visible boundary
- RULE: "Ghost-forward snapshots must include signal timestamp and visible-bar boundary."
- TYPE: hard
- SOURCE: BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Rules)

### [DATA] data lake rule 5 — version historical validation results
- RULE: "Never overwrite historical validation results without versioning."
- TYPE: hard
- SOURCE: BX/docs/DATA_LAKE_INTEGRATION_GUIDE.md (§Rules)

### [VALIDATION] ghost forward validation — definition
- RULE: Ghost Forward Validation is a candle-by-candle historical replay where the engine receives only past and current bars, generates live-visible wave candidates, records every candidate state, and later evaluates the outcome using future bars only after the signal snapshot has been frozen.
- TYPE: validation
- SOURCE: BX/docs/GHOST_FORWARD_VALIDATION.md (§intro)

### [VALIDATION] ghost forward vs backtest question
- RULE: Normal backtesting asks "Did the completed historical pattern work?"; ghost-forward asks "At each historical candle, what would the engine have seen in real time?" — more appropriate for Elliott Wave and NeoWave because patterns evolve gradually.
- TYPE: validation
- SOURCE: BX/docs/GHOST_FORWARD_VALIDATION.md (§Why this matters)

### [VALIDATION] snapshot fields (bundle)
- RULE: Snapshot fields: symbol, timeframe, signal_index, signal_time, visible_bars_until, candidate_id, pattern, status, confidence, expected_direction, invalidation_level, confirmation_level, wave_ids.
- TYPE: hard
- SOURCE: BX/docs/GHOST_FORWARD_VALIDATION.md (§Snapshot fields)

### [VALIDATION] outcome fields (bundle)
- RULE: Outcome fields: max_favorable_excursion, max_adverse_excursion, hit_confirmation, hit_invalidation, bars_to_confirmation, bars_to_invalidation.
- TYPE: hard
- SOURCE: BX/docs/GHOST_FORWARD_VALIDATION.md (§Outcome fields)

### [VALIDATION] non-negotiable — never backdate ghost-forward signal
- RULE: "Ghost-forward validation must never move a signal backward to the pivot candle."
- TYPE: hard
- SOURCE: BX/docs/GHOST_FORWARD_VALIDATION.md (§Non-negotiable rule)

### [VALIDATION] no-lookahead core law
- RULE: "A module is invalid if it uses future bars to create a signal at an earlier timestamp."
- TYPE: hard
- SOURCE: BX/docs/NO_LOOKAHEAD_POLICY.md (§Core law)
- NOTES: The policy file "is mandatory for every agent and Codex task."

### [VALIDATION] pivot rule — three indices
- RULE: "Pivot index = where the swing actually occurred. Confirmed index = when the algorithm had enough evidence to know the pivot existed. Signal index = confirmed index or later." A pivot that occurs at candle 100 and is confirmed at candle 105 can only affect signals from candle 105 onward.
- TYPE: hard
- SOURCE: BX/docs/NO_LOOKAHEAD_POLICY.md (§Pivot rule)

### [VALIDATION] forbidden lookahead behaviors
- RULE: Forbidden: backdating signals to the pivot candle; using completed future structures to label real-time candidates; optimizing pivots using full-chart hindsight; generating PnL from unconfirmed pivots; treating TradingView repainting labels as valid trade-time signals.
- TYPE: hard
- SOURCE: BX/docs/NO_LOOKAHEAD_POLICY.md (§Forbidden behavior)

### [VALIDATION] required tests for every pivot detector
- RULE: Every pivot detector must pass: `confirmed_index >= pivot_index`, `confirmed_t >= pivot_t`, and a prefix-stability test.
- TYPE: validation
- SOURCE: BX/docs/NO_LOOKAHEAD_POLICY.md (§Required tests)

### [VALIDATION] required tests for every replay engine
- RULE: Every replay engine must pass: visible data at t = `bars[:t+1]`; `signal_time` = current candle time; outcome labels use future only after snapshot is frozen.
- TYPE: validation
- SOURCE: BX/docs/NO_LOOKAHEAD_POLICY.md (§Required tests)

### [SCOPE] bundle v0.1.0 status — implemented vs not implemented
- RULE: v0.1.0 scaffold, 11 tests passing at generation time. Implemented: data schema, CSV adapter, Alpaca MCP adapter interface, parquet cache, session helper, percent reversal pivots, fractal pivots, mono-wave builder, rule result model, zigzag/flat/impulse validators, pattern scanner, ghost-forward replay, outcome labeler, TradingView note generator, CLI. Not implemented: real Alpaca MCP wiring, ATR pivot detector, triangle/terminal/diametric/advanced NeoWave patterns, chart HTML output, data lake connector, dashboard, paper trading, live trading.
- TYPE: scope
- SOURCE: BX/docs/PROJECT_STATUS.md (§Implemented now / Not implemented yet)
- NOTES: Missing pieces require local environment: Alpaca MCP function names, data lake paths, repo conventions, broker/data credentials, preferred chart output.

### [PROCESS-METHOD] use bundle as active repo; legacy as reference only
- RULE: Use ElliottWave_Automation_Project_Bundle/ as the new clean base project; keep legacy/ (previous repo), research_validation/ (research decision docs), elliotwave_md_pack/ (source theory and manual TradingView notes) as references only. Do not build from the legacy repo directly.
- TYPE: process
- SOURCE: BX/docs/START_HERE.md (§Use this bundle as the active repository)

### [PROCESS-METHOD] legacy migration rule
- RULE: "Legacy idea → new spec → new test → clean implementation → accepted module".
- TYPE: process
- SOURCE: BX/docs/START_HERE.md (§Do not build from the legacy repo directly)

### [PROCESS-METHOD] first 5 steps
- RULE: 1. Create a GitHub repo from this bundle. 2. Run pytest and confirm all tests pass. 3. Connect Alpaca MCP server through ewauto/data/adapters/alpaca_mcp_adapter.py. 4. Fetch one symbol and save canonical bars. 5. Run ghost-forward validation and inspect the CSV outputs.
- TYPE: process
- SOURCE: BX/docs/START_HERE.md (§First 5 steps)

### [PROCESS-METHOD] Task 1 context restriction
- RULE: Give Codex only these files for Task 1: README.md, pyproject.toml, ewauto/data/schema.py, ewauto/data/adapters/base.py, ewauto/data/adapters/alpaca_mcp_adapter.py, ewauto/data/cache.py, tests/test_schema.py, prompts/001_CODEX_CONNECT_ALPACA_MCP.md. "Do not give it all Elliott Wave docs while connecting Alpaca. That prevents drift."
- TYPE: process
- SOURCE: BX/docs/START_HERE.md (§What Codex should see first)

### [PROCESS-METHOD] never give Codex the full theory library
- RULE: "Never give Codex the full theory library for a coding task. Use one task card, one agent role, and a small file set."
- TYPE: process
- SOURCE: BX/docs/codex/CODEX_WORKFLOW_RULES.md (§Never give Codex the full theory library)

### [PROCESS-METHOD] required prompt structure
- RULE: Every prompt must contain: Role, Task, Allowed files, Forbidden files, Input contract, Output contract, Tests required, Definition of done.
- TYPE: process
- SOURCE: BX/docs/codex/CODEX_WORKFLOW_RULES.md (§Required prompt structure)

### [PROCESS-METHOD] forbidden Codex behavior
- RULE: Forbidden: implementing trading execution without request; adding ML before labeled data exists; mixing classical Elliott and NeoWave rules without profile separation; removing confirmed_index / confirmed_t; backdating signals; rewriting unrelated modules.
- TYPE: hard
- SOURCE: BX/docs/codex/CODEX_WORKFLOW_RULES.md (§Forbidden Codex behavior)

### [PROCESS-METHOD] pull request acceptance rule
- RULE: A change is accepted only if: pytest passes; no-lookahead tests pass; module docstring explains the design; new behavior has tests; README or docs updated when interface changes.
- TYPE: process
- SOURCE: BX/docs/codex/CODEX_WORKFLOW_RULES.md (§Pull request acceptance rule)

### [PROCESS-METHOD] Phase 0 — repo setup DoD
- RULE: Phase 0 definition of done: `pip install -e '.[dev]'`, pytest passes, README commands work.
- TYPE: process
- SOURCE: BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 0)

### [DATA] Phase 1 — Alpaca MCP data connection DoD
- RULE: Fetch 10 years of bars for one symbol; normalize into canonical schema; save parquet cache; reload parquet and pass validate_bars. Files: ewauto/data/adapters/alpaca_mcp_adapter.py, ewauto/data/schema.py, ewauto/data/cache.py.
- TYPE: process
- SOURCE: BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 1)

### [VALIDATION] Phase 2 — pivot engine hardening DoD
- RULE: Goal: compare percent-reversal, fractal, and later ATR pivots. DoD: confirmed_index test passes; prefix-stability test passes; pivot CSV export exists; chart debug output exists.
- TYPE: process
- SOURCE: BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 2)

### [AUTOMATION-SPEC] Phase 3 — mono-wave and rule engine DoD
- RULE: Convert pivots to mono-waves and validate zigzag/flat/impulse candidates. DoD: wave table export; rule-result JSON export; candidate scanner returns interpretable results.
- TYPE: process
- SOURCE: BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 3)

### [VALIDATION] Phase 4 — ghost-forward validation DoD
- RULE: Prove candidates are visible in real time. DoD: ghost_forward_signals.csv; ghost_forward_outcomes.csv; summary metrics; no backdated signal timestamps.
- TYPE: process
- SOURCE: BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 4)

### [SETUP-TRADE] Phase 5 — TradingView workflow output DoD
- RULE: Produce manual chart instructions. DoD: Markdown note per candidate; invalidation / confirmation levels; wave IDs and timestamps.
- TYPE: process
- SOURCE: BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 5)

### [PROCESS-METHOD] Phase 6 — legacy salvage rule
- RULE: Migrate only proven pieces from the old repo: "Legacy idea → new spec → new tests → clean implementation". Do not copy large legacy files directly into production modules.
- TYPE: process
- SOURCE: BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 6)

### [PROCESS-METHOD] Phase 7 — advanced patterns one at a time
- RULE: Add one pattern at a time: Triangle, Terminal impulse, Diametric, Neutral triangle, Extracting triangle, Complex correction. Each pattern must include tests and ghost-forward output.
- TYPE: process
- SOURCE: BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 7)

### [DATA] Phase 8 — data lake integration timing
- RULE: Connect the package to the broader data lake only after the schema stabilizes.
- TYPE: process
- SOURCE: BX/docs/roadmap/PHASED_BUILD_ROADMAP.md (§Phase 8)

### [DATA] SPEC 001 — required column types
- RULE: Required: timestamp (UTC-aware datetime), open (float), high (float), low (float), close (float), volume (numeric >= 0). Optional: vwap, symbol, timeframe, session_type, source. Purpose: all data sources produce the same canonical OHLCV schema so the wave engine never depends on provider-specific quirks.
- TYPE: hard
- SOURCE: BX/docs/specs/SPEC_001_DATA_CONTRACT.md (§Required columns / Optional columns)

### [DATA] SPEC 001 — validation rules
- RULE: timestamp sorted ascending; timestamp unique; high >= open, close, low; low <= open, close, high; no nulls in required columns; volume >= 0. Implementation: ewauto/data/schema.py.
- TYPE: hard
- SOURCE: BX/docs/specs/SPEC_001_DATA_CONTRACT.md (§Validation rules)

### [DATA] SPEC 002 — required pivot fields
- RULE: Pivot fields: index, t, price, kind: H/L, confirmed_index, confirmed_t, source, meta. Purpose: detect swing pivots without lookahead.
- TYPE: hard
- SOURCE: BX/docs/specs/SPEC_002_PIVOT_ENGINE.md (§Required pivot fields)

### [VALIDATION] SPEC 002 — mandatory pivot invariant
- RULE: `confirmed_index >= index` and `confirmed_t >= t`.
- TYPE: hard
- SOURCE: BX/docs/specs/SPEC_002_PIVOT_ENGINE.md (§Mandatory invariant)

### [AUTOMATION-SPEC] SPEC 002 — implemented and future detectors
- RULE: Implemented: PercentReversalPivotDetector, FractalPivotDetector. Future: ATR reversal pivots, volume-confirmed pivots, multi-timeframe pivots.
- TYPE: setup
- SOURCE: BX/docs/specs/SPEC_002_PIVOT_ENGINE.md (§Implemented detectors / Future detectors)

### [AUTOMATION-SPEC] SPEC 003 — rule statuses
- RULE: Rule statuses: PASS, FAIL, WARN, UNKNOWN. Rationale: "Elliott Wave and NeoWave are not purely binary. Some rules are hard invalidations, while others are warning signs or manual-review criteria."
- TYPE: hard
- SOURCE: BX/docs/specs/SPEC_003_RULE_ENGINE.md (§Rule statuses / Why this matters)

### [AUTOMATION-SPEC] SPEC 003 — implemented and future validators
- RULE: Implemented validators: validate_zigzag, validate_flat, validate_impulse. Future validators: triangle, terminal impulse, diametric, neutral triangle, extracting triangle, complex correction.
- TYPE: setup
- SOURCE: BX/docs/specs/SPEC_003_RULE_ENGINE.md (§Implemented validators / Future validators)

### [VALIDATION] SPEC 004 — ghost forward replay process
- RULE: For candle t: visible = bars[:t+1]; pivots = detect(visible); monowaves = build(pivots confirmed by t); candidates = scan(monowaves); snapshot = freeze candidate at t. Later: label outcome using bars after t.
- TYPE: validation
- SOURCE: BX/docs/specs/SPEC_004_GHOST_FORWARD.md (§Process)

### [VALIDATION] SPEC 004 — forbidden ghost-forward behaviors
- RULE: Do not let outcome labeling affect the snapshot. Do not move signal time back to the pivot candle. Do not use full-history pivots during replay.
- TYPE: hard
- SOURCE: BX/docs/specs/SPEC_004_GHOST_FORWARD.md (§Forbidden)

### [DATA] Prompt 001 — Alpaca MCP adapter requirements
- RULE: Adapter must: return canonical bars; support extended-hours flag; support adjusted/raw behavior if exposed by MCP; preserve UTC timestamps; pass schema validation; not store secrets. Forbidden: implementing Elliott Wave logic; modifying pivot/wave/rules/pattern/ghost-forward modules; adding API keys or secrets; removing normalize_bars or validate_bars.
- TYPE: hard
- SOURCE: BX/prompts/001_CODEX_CONNECT_ALPACA_MCP.md (§Requirements / Forbidden changes)
- NOTES: DoD: pytest passes; fetch one symbol from Alpaca MCP; save parquet cache; reload parquet cache; validate_bars passes; README command snippet updated if needed.

### [VALIDATION] Prompt 002 — pivot engine hardening tests
- RULE: Required tests: `confirmed_index >= index`; `confirmed_t >= t`; prefix-stability test; `min_bars_between` respected. Forbidden: adding trading signals; adding Elliott pattern rules; removing confirmed_index or confirmed_t; backdating signal timestamps.
- TYPE: validation
- SOURCE: BX/prompts/002_CODEX_HARDEN_PIVOT_ENGINE.md (§Required tests / Forbidden changes)
- NOTES: DoD: pytest passes; pivot outputs are deterministic; pivot detector config is documented.

### [INDICATORS] Prompt 003 — ATR pivot detector requirements
- RULE: 1. ATR must be computed only from past/current bars. 2. Pivot confirmation must occur only after ATR reversal is visible. 3. Every pivot must include confirmed_index and confirmed_t. 4. Include tests for no-lookahead behavior. New file: ewauto/pivots/atr_reversal.py; do not rewrite percent_reversal.py or fractal.py; no trading logic.
- TYPE: hard
- SOURCE: BX/prompts/003_CODEX_ADD_ATR_PIVOT_DETECTOR.md (§Requirements)

### [VALIDATION] Prompt 004 — extended ghost-forward reports
- RULE: Add: ghost_forward_summary.md generator; candidate stability report; late signal rate metric; repaint-like disappearance metric. Forbidden: altering pivot confirmation semantics; adding live trading; letting outcome labels influence signal snapshots.
- TYPE: validation
- SOURCE: BX/prompts/004_CODEX_EXTEND_GHOST_FORWARD_REPORTS.md (§Requirements / Forbidden changes)
- NOTES: DoD: pytest passes; sample CSV run produces signals, outcomes, and summary markdown.

### [PROCESS-METHOD] Prompt 005 — legacy salvage process
- RULE: Process: 1. Summarize the legacy idea. 2. Identify whether it fits the new architecture. 3. Write or update a spec. 4. Add tests. 5. Implement cleanly in the new module. Acceptance: Legacy idea → new spec → new tests → clean implementation → pytest passes.
- TYPE: process
- SOURCE: BX/prompts/005_CODEX_LEGACY_SALVAGE.md (§Process / Acceptance rule)

### [PROCESS-METHOD] Prompt 005 — legacy salvage prohibitions
- RULE: Do not copy entire legacy modules blindly. Do not import from legacy code in production modules. Do not migrate symbol-specific logic. Do not migrate old forecast logic unless it passes ghost-forward validation.
- TYPE: hard
- SOURCE: BX/prompts/005_CODEX_LEGACY_SALVAGE.md (§Forbidden behavior)

### [PROCESS-METHOD] three-layer knowledge architecture
- RULE: Layer 1 — Knowledge Base (raw markdown conversions, handwritten notes, source PDFs, diagrams, rules, examples). Layer 2 — Engineering Specifications (clean, simplified, machine-readable specs derived from the knowledge base). Layer 3 — Code Implementation. "The LLM should normally work from Layer 2, not from all raw documents."
- TYPE: process
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§1 Executive Summary)
- NOTES: Risks of handing full doc set to LLM: mixing discretionary theory with engineering; building all patterns at once; hallucinating rules; combining detection/signal/backtest/auto-trading into one unstable module; losing focus.

### [PROCESS-METHOD] core build sequence
- RULE: Build in this sequence: Bars → Pivots → Mono-waves → Rule checks → Candidate patterns → Scores → Chart annotations → Backtest → Dashboard. Do NOT begin with "Detect every Elliott Wave / NeoWave pattern automatically" — too broad, will fail.
- TYPE: process
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§2 Core Development Philosophy)
- NOTES: Foundation order: 1. Clean historical data. 2. Stable pivot detection. 3. Mono-wave construction. 4. Rule validation. 5. Pattern candidates. 6. Manual TradingView interpretation.

### [SCOPE] Version 1 scope
- RULE: V1 scope: fetch Alpaca historical data; normalize OHLCV bars; support regular/extended/full session data; resample into useful timeframes; detect swing pivots; create mono-wave table; apply Elliott/NeoWave rule validators; detect limited pattern candidates; generate chart annotations; export TradingView manual notes; run simple historical validation. V1 focuses on manual TradingView support, not auto-trading.
- TYPE: scope
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§3 What Version 1 Must Do)

### [SCOPE] Version 1 non-scope
- RULE: No live order placement; no options execution; no short selling automation; no full discretionary NeoWave interpretation; no black-box ML prediction; no automatic final buy/sell recommendations in early phases; no all-pattern detection in one release; no strategy optimization before data and rules are stable.
- TYPE: scope
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§3 Version 1 Non-Scope)

### [AUTOMATION-SPEC] recommended repository structure
- RULE: Repo `elliotwave-automation/` with README.md, PROJECT_CHARTER.md, DEVELOPMENT_ROADMAP.md, LLM_WORKFLOW_RULES.md; docs_source/ (original_markdown_pack, handwritten_notes, pdf_conversions, source_images); specs/00–12 (system_scope, data_contract, bar_schema, pivot_detection, monowave, impulse_rules, corrective_rules, fibonacci_rules, ichimoku_filter, pattern_scoring, backtest, output_chart, tradingview_manual_output); src/ (data, pivots, waves, rules, patterns, scoring, backtest, charts, reports, utils); tests/ incl. test_no_lookahead.py; notebooks/; config/ (symbols.yaml, timeframes.yaml, pivot_profiles.yaml, session_profiles.yaml); outputs/ (data_cache, charts, backtests, reports, logs).
- TYPE: setup
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§4 Recommended Repository Structure)

### [PROCESS-METHOD] keep raw documents separate
- RULE: The markdown pack goes under docs_source/original_markdown_pack/. Codex/Claude should NOT read every source document for every task; every development task should point to one or two specific specs (e.g., use only specs/03_pivot_detection_spec.md + specs/01_data_contract.md; do not read or modify docs_source/, patterns/, backtest/, dashboard/).
- TYPE: process
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§5 Important Rule: Keep Raw Documents Separate)

### [PROCESS-METHOD] Phase 0 — project freeze and scope control
- RULE: Create PROJECT_CHARTER.md, DEVELOPMENT_ROADMAP.md, LLM_WORKFLOW_RULES.md, specs/00_system_scope.md. Acceptance: project scope clearly defined; non-scope clearly defined; LLM workflow rules exist; development phases locked; the project does not contain auto-trading logic yet.
- TYPE: process
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§6 Phase 0)

### [DATA] Phase 1 — bar data contract
- RULE: Every bar must normalize to: symbol (string), timestamp (timezone-aware datetime), open/high/low/close (float), volume (float), vwap (float optional), timeframe (string), session_type (regular | extended | full), source (alpaca), adjusted (true | false optional).
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 1 Data Contract)

### [DATA] Phase 1 — required data capabilities
- RULE: Fetch historical bars for one symbol; support daily, hourly, 15m, 5m, and 1m where available; support extended-hours filtering; cache data locally as parquet; validate missing candles; validate duplicate timestamps; validate timezone consistency; export sample CSV for manual inspection.
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 1 Required Capabilities)

### [DATA] session handling — regular/extended/full
- RULE: The system must explicitly support: regular = only regular market session; extended = premarket + postmarket only if separated; full = regular + extended combined. "For U.S. equities, session handling matters because Elliott Wave pivots can differ when extended-hours candles are included."
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 1 Session Handling)

### [DATA] Phase 1 — acceptance criteria
- RULE: Can fetch 10 years of daily data for a symbol; can fetch intraday data for supported periods; can store and reload parquet files; can label each bar with session_type; no duplicate timestamps; no missing schema columns; all timestamps timezone-aware; unit tests pass.
- TYPE: validation
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 1 Acceptance Criteria)

### [AUTOMATION-SPEC] Phase 2 — required pivot modes
- RULE: Start with three modes: Mode 1 percentage reversal pivots; Mode 2 ATR-based pivots; Mode 3 fractal swing pivots. For the first working version prioritize: "Percentage reversal + minimum bar distance".
- TYPE: setup
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 2 Required Pivot Modes)
- NOTES: "Elliott Wave automation depends on pivots. If the pivot engine is unstable, every wave count will be unstable."

### [DATA] Phase 2 — pivot record schema
- RULE: Pivot record: symbol, timeframe, pivot_id, pivot_time, pivot_price, pivot_type (HIGH | LOW), source_bar_index, confirmation_time, confirmation_bar_index, confirmation_lag_bars, method, parameters.
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 2 Pivot Record Schema)

### [VALIDATION] Phase 2 — pivot no-lookahead rule
- RULE: A pivot is confirmed only after enough future bars or reversal movement occurred. Store pivot_time = actual swing point time; confirmation_time = time when the system could know the pivot was confirmed. "Backtests must use `confirmation_time`, not `pivot_time`, for decisions."
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 2 No-Lookahead Rule)

### [AUTOMATION-SPEC] Phase 2 — pivot acceptance criteria
- RULE: Detects alternating HIGH and LOW pivots; does not create duplicate consecutive highs or lows; stores pivot time and confirmation time separately; supports parameter profiles; can plot pivots on a chart; no-lookahead tests pass.
- TYPE: validation
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 2 Acceptance Criteria)

### [PROCESS-METHOD] mono-wave concept — measurable unit, no labels
- RULE: "A mono-wave is the basic measurable unit of wave analysis. It is not yet an Elliott Wave label. It is only a directional segment between two confirmed pivots." Do not label a segment as Wave 1, Wave 2, Wave A, Wave B, or Wave C in this phase — first calculate facts, not opinions.
- TYPE: process
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 3 Mono-Wave Concept / Important Rule)
- NOTES: Example measurements only: "This wave is UP. It moved 8.4%. It took 27 bars. It retraced 52% of the previous wave. It extended 1.61x the previous comparable wave."

### [DATA] Phase 3 — mono-wave schema
- RULE: Mono-wave record: symbol, timeframe, wave_id, start_pivot_id, end_pivot_id, start_time, end_time, start_price, end_price, direction (UP | DOWN), price_length, time_length_bars, time_length_seconds, percent_change, slope, retracement_vs_previous, extension_vs_previous, price_ratio_vs_previous, time_ratio_vs_previous, confirmation_time.
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 3 Mono-Wave Schema)

### [AUTOMATION-SPEC] Phase 3 — mono-wave acceptance criteria
- RULE: Can convert pivot table to mono-wave table; calculates price length and time length; calculates retracement and extension ratios; does not assign Elliott labels yet; tests pass. Mono-wave table must be deterministic.
- TYPE: validation
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 3 Acceptance Criteria / DoD)

### [AUTOMATION-SPEC] Phase 4 — rule result schema
- RULE: Every rule check returns: {"rule_id": "wave_2_retrace_limit", "status": "PASS | FAIL | WARNING | UNKNOWN", "confidence": 0.0, "details": "Human-readable explanation", "measured_value": 0.618, "expected_value": "<= 0.618"}.
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 4 Rule Result Schema)
- NOTES: Why not binary only: Elliott Wave / NeoWave is interpretive — some rules mandatory, some guidelines, some context-dependent; hence PASS/FAIL/WARNING/UNKNOWN.

### [AUTOMATION-SPEC] Phase 4 — rule engine acceptance criteria
- RULE: Rule engine can run a list of validators; each validator returns structured output; pattern modules can reuse this engine; rule results can be converted into pattern score; scoring works deterministically; tests pass.
- TYPE: validation
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 4 Acceptance Criteria)

### [FIB] Fibonacci measurement definitions
- RULE: Retracement = correction length / prior impulse length. Extension = current wave length / comparison wave length. Equality = current wave approximately equal to comparison wave. Time ratio = current wave duration / comparison wave duration.
- TYPE: fib
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Required Calculations)

### [FIB] important Fibonacci ratios
- RULE: Important ratios: 0.382, 0.500, 0.618, 1.000, 1.382, 1.618, 2.000, 2.618.
- TYPE: fib
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Important Ratios)

### [FIB] impulse Fibonacci relationships
- RULE: Wave 3 often extends 1.618x or 2.618x Wave 1; extended wave should be at least 1.618x of next longest; two unextended waves tend toward equality.
- TYPE: fib
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Usage in Later Pattern Rules — Impulse)

### [FIB] zigzag Fibonacci relationships
- RULE: B should be less than 61.8% of A; C often equals A or extends 1.618x A.
- TYPE: fib
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Usage — Zigzag)

### [FIB] flat Fibonacci relationships
- RULE: B should be more than 61.8% of A; C often relates to A or A+B.
- TYPE: fib
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Usage — Flat)

### [FIB] triangle Fibonacci relationships
- RULE: Internal legs are corrective; multiple legs often retrace more than 50% of previous leg.
- TYPE: fib
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Usage — Triangle)

### [DIAMETRIC] diametric Fibonacci relationships
- RULE: G often relates to A; F often relates to B; E often relates to C.
- TYPE: fib
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Usage — Diametric)

### [FIB] Fibonacci engine acceptance criteria
- RULE: Calculates all common price ratios; calculates time ratios; supports tolerance bands; returns structured measurements; measurements reusable by pattern modules; tests pass.
- TYPE: validation
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 5 Acceptance Criteria)

### [ZIGZAG] zigzag structure rules
- RULE: A-B-C; internal structure approximation 5-3-5; B retracement: less than 61.8% of A; C should move beyond end of A; Wave B should take same or more time than A; 0-B line break confirms completion.
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 6 Zigzag Structure)
- NOTES: Candidate input = three mono-waves (A = wave 1, B = wave 2, C = wave 3). Output: Possible Zigzag, confidence score, rule results, invalidation level, confirmation line, TradingView drawing instruction.

### [ZIGZAG] zigzag module implementation checks
- RULE: 1. Evaluate three mono-waves as A-B-C. 2. Check B < 61.8% of A. 3. Check C beyond A. 4. Check time rule for B vs A. 5. Return structured rule results and score. 6. Generate manual TradingView note.
- TYPE: setup
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 6 Codex / Claude Prompt)
- NOTES: Zigzag is Pattern Module 1 — implemented first; Flat/Triangle/Impulse forbidden in that task.

### [FLAT] flat structure rules
- RULE: A-B-C; internal structure approximation 3-3-5; B retracement: more than 61.8% of A; C relates to A price-wise or A+B time-wise; 0-B line break confirms completion; Wave B should take same or more time than A.
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 7 Flat Structure)

### [FLAT] flat variants
- RULE: Variants: Regular Flat, Irregular Flat, Running Flat, C Failure Flat, Double Failure Flat. Detector must classify broad variant when possible and return warning when ambiguous.
- TYPE: guideline
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 7 Flat Variants / Acceptance Criteria)

### [IMPULSE] impulse structure rules
- RULE: 1-2-3-4-5; internal structure approximation 5-3-5-3-5; Waves 1, 3, and 5 move in impulse direction; Waves 2 and 4 correct waves 1 and 3; Wave 2 cannot retrace more than 61.8% of Wave 1; Wave 3 cannot be the shortest among 1, 3, and 5; Wave 4 should not overlap Wave 1 except terminal impulse; Wave 2 and Wave 4 should alternate; only one of 1, 3, or 5 should extend; extended wave should be at least 1.618x of the next longest.
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 8 Impulse Structure)
- NOTES: Implement impulse only after corrective modules and mono-wave engine are stable.

### [TERMINAL] terminal impulse exception flag
- RULE: Wave 4 overlap of Wave 1 is allowed only for terminal impulse; the impulse validator must mark the terminal exception separately ("Do not implement terminal impulse yet except as an exception flag").
- TYPE: guideline
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 8 Impulse Structure / Forbidden)

### [IMPULSE] impulse validator checks
- RULE: 1. Evaluate five mono-waves as 1-2-3-4-5. 2. Check Wave 2 retracement <= 61.8%. 3. Check Wave 3 is not shortest. 4. Check Wave 4 overlap rule. 5. Check extension and equality rules. 6. Return structured rule results and score.
- TYPE: setup
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 8 Codex / Claude Prompt)

### [TRIANGLE] triangle structure rules
- RULE: A-B-C-D-E; internal structure approximation 3-3-3-3-3; each segment is corrective; triangle can drift upward or downward; E should often be smallest; at least three segments should retrace more than 50% of previous segment; B-D line is the base line and should be clean; triangle is confirmed when B-D line breaks in equal or lesser time than E.
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 9 Triangle Structure)
- NOTES: Acceptance: evaluate five mono-waves as triangle candidate; produce trendline instructions; identify B-D confirmation line.

### [COMPLEX-X] advanced NeoWave pattern set and order
- RULE: Advanced patterns: Terminal Impulse, Diametric, Complex Correction, Double Combination, Triple Combination, Neutral Triangle, Extracting Triangle, Running Diametric. Implement as separate modules, not mixed into core impulse/corrective modules. Recommended order: 1. Terminal impulse 2. Diametric 3. Complex correction with X-wave 4. Neutral triangle 5. Extracting triangle 6. Double / triple combinations. Only begin after the core engine is stable.
- TYPE: process
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§Phase 10 Advanced NeoWave Patterns)

### [SETUP-TRADE] manual TradingView note template
- RULE: Early output is a manual interpretation note containing: Symbol, Timeframe, Session, Detected structure, Current candidate, Confidence (e.g., 72%), key pivots with timestamps and prices, rule results (PASS/WARNING/UNKNOWN lines), TradingView action steps (mark pivot A, mark pivot B, draw 0-B trendline, watch for break of 0-B line, add Fibonacci projection from A to B to estimate C zone, use Ichimoku only as a trend filter), and invalidation statement. "This is better than directly producing buy/sell signals."
- TYPE: setup
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§7 Manual TradingView Output Design)

### [SETUP-TRADE] invalidation discipline
- RULE: "If price violates the candidate structure before confirmation, discard the count."
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§7 Manual TradingView Output Design — Invalidation)

### [AUTOMATION-SPEC] chart output requirements per phase
- RULE: Phase 1 chart: candles only, optional session shading. Phase 2: candles + pivot markers, HIGH/LOW pivots labeled, confirmation lag visible in debug mode. Phase 3: candles + pivots + mono-wave lines, each mono-wave numbered internally as M1, M2, M3... Phase 6+: candles + pattern candidate labels, A-B-C or 1-2-3-4-5 labels, rule score box, invalidation level, confirmation trendline.
- TYPE: setup
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§8 Chart Output Requirements)

### [VALIDATION] backtest stage 1 — mechanics
- RULE: Do not backtest final trading strategies too early. Stage 1 validates mechanics: data availability, pivot confirmation lag, no-lookahead enforcement, pattern frequency, pattern completion behavior.
- TYPE: validation
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§9 Backtest Stage 1)

### [VALIDATION] backtest stage 2 — pattern implication
- RULE: Stage 2 validates pattern implication: After Zigzag completion, did price move as expected? After 0-B line break, did follow-through occur? After impulse count completion, did correction begin? After triangle breakout, did directional continuation occur?
- TYPE: validation
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§9 Backtest Stage 2)

### [RISK] backtest stage 3 — trading rules metrics
- RULE: Only after stages 1–2, test trading rules: entry trigger, stop invalidation, target zones, time stop, risk-reward, win rate, profit factor, max drawdown, expectancy.
- TYPE: risk
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§9 Backtest Stage 3)

### [VALIDATION] no-lookahead core rule + example
- RULE: "A signal, pattern, pivot, or confirmation can only be used after the bar where it becomes knowable." Example: swing high at 10:00 confirmed at 10:45 → pivot_time = 10:00, confirmation_time = 10:45; for backtesting "Do not allow any trade or pattern decision before 10:45."
- TYPE: hard
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§10 No-Lookahead Rules)
- NOTES: Required test tests/test_no_lookahead.py "must remain active throughout the project."

### [PROCESS-METHOD] LLM workflow rules and task template
- RULE: Never give the prompt "Read all documents and build the Elliott Wave automation system." Every task must include: Task name, Scope, Allowed files, Forbidden files, Input contract, Output contract, Tests required, Definition of done. Template includes: "Do not add trading logic unless explicitly requested. Do not refactor unrelated modules."
- TYPE: process
- SOURCE: SM/ElliottWave_Automation_Development_Plan.md (§11 LLM Workflow Rules)
