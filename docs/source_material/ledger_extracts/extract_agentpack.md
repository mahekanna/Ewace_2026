# Extract — ElliottWave_Automation_Agent_Prompt_Pack

Paths in SOURCE are relative to `ElliottWave_Automation_Agent_Prompt_Pack/` (inner pack root).

### [VALIDATION] no-lookahead-core-rule
- RULE: No module may use future candles to make a decision at the current candle. Applies to pivot confirmation, wave labeling, Fibonacci target validation, pattern confirmation, Ichimoku filtering, backtest entry and exit, and chart annotations marked as historically known.
- TYPE: hard
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§1. No-Lookahead Rule)

### [VALIDATION] pivot-time-vs-confirmation-time
- RULE: If a future bar is required to confirm a pivot, output must record `pivot_time = actual swing timestamp` and `confirmation_time = timestamp when enough future movement made the pivot knowable`. A backtest may only act from `confirmation_time`, never from `pivot_time`.
- TYPE: hard
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§1. No-Lookahead Rule)

### [SCOPE] no-auto-trading-v1
- RULE: The project must not place live orders, connect to broker trading endpoints, or generate executable order instructions in early phases. Allowed output: Manual TradingView plan, Pattern candidate, Invalidation level, Confirmation condition, Risk note. Forbidden output: "Place buy order now", "Sell short now", "Auto-submit bracket order".
- TYPE: scope
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§2. No Auto-Trading in Version 1)

### [DATA] data-contract-first
- RULE: Every downstream module must consume a normalized OHLCV bar schema. No module should call Alpaca directly except the data engine.
- TYPE: process
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§3. Data Contract First)

### [PROCESS-METHOD] pivots-before-waves
- RULE: No wave count is valid unless it comes from a stable pivot table.
- TYPE: process
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§4. Pivots Before Waves)

### [PROCESS-METHOD] monowaves-before-patterns
- RULE: Pattern validators must operate on mono-wave objects, not raw candles.
- TYPE: process
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§5. Mono-Waves Before Patterns)

### [VALIDATION] rule-engine-explainable-schema
- RULE: Every rule check must return an object with fields `rule_id` (string), `status` (PASS | FAIL | WARNING | UNKNOWN), `confidence` (0.0), `details` (human-readable reason), and `evidence` ({}).
- TYPE: validation
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§6. Rule Engine Must Be Explainable)

### [PROCESS-METHOD] pattern-detection-candidate-based
- RULE: The system should not say "This is definitely wave 3." It should say e.g. "Candidate impulse count with confidence 0.72. Wave 2 retracement passes. Wave 4 overlap warning. Confirmation pending."
- TYPE: process
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§7. Pattern Detection Is Candidate-Based)
- NOTES: Detection is probabilistic/candidate-based, never definitive certainty.

### [PROCESS-METHOD] source-docs-reference-only
- RULE: The model must not scrape all source markdowns during every task. Source documents can be used only when a task explicitly asks for a rule extraction or clarification.
- TYPE: process
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§8. Source Docs Are Reference Only)

### [SCOPE] no-ml-until-labeled-data
- RULE: Do not add ML/DL models until the rule-based engine produces labeled examples and quality checks.
- TYPE: scope
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§9. No ML Until Labeled Data Exists)

### [PROCESS-METHOD] every-module-needs-tests
- RULE: No implementation is complete without tests. Minimum required: unit tests, edge case tests, no-lookahead tests where relevant, small fixture data, expected output examples.
- TYPE: process
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§10. Every Module Needs Tests)

### [PROCESS-METHOD] no-casual-architecture-rewrite
- RULE: Agents may not restructure the repository unless the task explicitly allows it.
- TYPE: process
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§11. Do Not Rewrite Architecture Casually)

### [PROCESS-METHOD] tradingview-output-human-readable
- RULE: Final output should help a trader manually apply the system in TradingView: mark pivots, draw trendline, watch invalidation, confirm with condition.
- TYPE: process
- SOURCE: 01_SHARED_SYSTEM_RULES.md (§12. Manual TradingView Output Must Stay Human-Readable)

### [AUTOMATION-SPEC] critical-guardrail-no-trade-signal
- RULE: No agent may produce a trade signal unless a later approved Trade Engine exists. Until that phase the system only produces: Pattern candidates, Rule pass/fail/warning status, Invalidation levels, Confirmation conditions, TradingView manual annotation instructions.
- TYPE: scope
- SOURCE: 00_AGENT_OPERATING_MODEL.md (§The Critical Guardrail)

### [AUTOMATION-SPEC] core-development-flow
- RULE: Development flow: (1) Source documents remain reference only; (2) Engineering specs define the buildable rules; (3) Agents implement one module at a time; (4) Every task must have tests; (5) No module can skip the phase order.
- TYPE: process
- SOURCE: 00_AGENT_OPERATING_MODEL.md (§Core Development Flow)

### [AUTOMATION-SPEC] pipeline-build-order
- RULE: The automation pipeline must be built in this order: Bars → Clean Data → Pivots → Mono-waves → Rule Validators → Pattern Candidates → Scores → Chart Output → Backtest. No agent should jump directly to buy/sell signals or full discretionary NeoWave prediction.
- TYPE: process
- SOURCE: README.md (§Non-Negotiable Principle); also MASTER_CLAUDE_CODE_START_PROMPT.md
- NOTES: One agent + one task card per coding session.

### [AUTOMATION-SPEC] one-session-one-role
- RULE: One session should have: one agent role, one task card, one allowed file list, one definition of done, one test requirement. Do not combine multiple agents in one coding request.
- TYPE: process
- SOURCE: 00_AGENT_OPERATING_MODEL.md (§Session Rule)

### [AUTOMATION-SPEC] agent-recommended-order
- RULE: Recommended agent execution order: A00 → A01 → A02 → A03 → A04 → A05 → A06 → A08 → A07 → A10 → A11 → A12 → A13 → A14 → A15 → A16. When in doubt choose the narrowest agent that can complete the task.
- TYPE: process
- SOURCE: 02_AGENT_REGISTRY.md (§Recommended Order, §Agent Selection Rule)
- NOTES: Note A08 (corrective: zigzag/flat) precedes A07 (impulse). Label impulse (A07) only after A04/A05/A06 exist.

### [DATA] data-contract-fields
- RULE: Normalized OHLCV data contract raw fields: timestamp, open, high, low, close, volume, optional vwap, symbol, timeframe, session_type, source. Define required columns, dtypes, timezone policy. session_type values: regular, extended, full. source value: alpaca.
- TYPE: data
- SOURCE: tasks/TASK_001_DATA_CONTRACT.md (§Input Contract, §Implementation Requirements)

### [DATA] data-contract-validation-tests
- RULE: Schema validation must pass on valid sample, fail on missing required columns, and reject invalid session_type.
- TYPE: validation
- SOURCE: tasks/TASK_001_DATA_CONTRACT.md (§Tests Required)

### [DATA] alpaca-adapter-isolation
- RULE: Alpaca MCP code must be isolated behind an adapter; downstream modules must not call Alpaca directly. Data engine supports an extended_hours flag; return only contract columns; raise clear errors for bad inputs.
- TYPE: data
- SOURCE: tasks/TASK_002_ALPACA_DATA_ENGINE.md (§Implementation Requirements); QG_01_DATA_ENGINE.md
- NOTES: Alpaca MCP has ~10 years historical data including extended hours (DATA_ENGINE_READY_PROMPT.md).

### [DATA] parquet-cache-deterministic-paths
- RULE: Local parquet cache must use deterministic cache paths including symbol/timeframe/session in the path, validate schema after load, and allow force refresh. Cache key fields: symbol, timeframe, start, end, session mode.
- TYPE: data
- SOURCE: tasks/TASK_003_PARQUET_CACHE.md (§Input Contract, §Implementation Requirements)

### [DATA] data-quality-checks
- RULE: Data quality validation must check missing bars, duplicate bars, OHLC relationships validity, and session tags; must not silently repair data without reporting. Block if extended-hours and regular-hours data are mixed silently or missing/duplicate bars are ignored.
- TYPE: validation
- SOURCE: agents/A03_Data_Quality_Agent.md; QG_01_DATA_ENGINE.md
- NOTES: Acceptance: no duplicate timestamps, OHLC values valid, session type valid, missing data reported.

### [DATA] data-fetch-timeframes
- RULE: Exit criteria for data engine: one symbol can be fetched for daily, hourly, 15m, and 5m; extended-hours mode is explicitly controlled; tests prove schema consistency.
- TYPE: data
- SOURCE: 05_PHASED_DEVELOPMENT_PLAN.md (§Phase 1 — Alpaca Data Engine)

### [CONFIRMATION-LINES] pivot-output-contract
- RULE: Pivot table output fields: pivot_time, confirmation_time, price, type (HIGH/LOW), source_index, confirmation_index. A pivot may occur at one timestamp but the system may only know it later at confirmation_time; backtests must never act before confirmation_time.
- TYPE: validation
- SOURCE: tasks/TASK_004_PIVOT_ENGINE.md (§Output Contract); PIVOT_ENGINE_READY_PROMPT.md; QG_02_PIVOT_ENGINE.md

### [PROCESS-METHOD] pivot-detection-percentage-reversal
- RULE: Implement percentage-reversal pivot detection with a minimum bar distance between pivots; percentage reversal mode must be deterministic; enforce minimum bar distance; return empty result safely if insufficient data. Inputs: normalized OHLCV bars, reversal_pct, min_bars_between_pivots. Optional ATR/fractal modes later.
- TYPE: indicator
- SOURCE: tasks/TASK_004_PIVOT_ENGINE.md (§Input Contract, §Implementation Requirements); A04_Pivot_Engine_Agent.md
- NOTES: Pivot detector must not change wave labels directly (QG_02).

### [PROCESS-METHOD] monowave-output-contract
- RULE: Mono-wave built one per consecutive pivot pair. Output fields: start_time, end_time, start_price, end_price, direction, price_length, time_length, slope, retracement_vs_previous, extension_vs_previous. First wave prior-ratio fields are null. Output deterministic. Validate alternating pivot types when possible.
- TYPE: process
- SOURCE: tasks/TASK_005_MONOWAVE_ENGINE.md (§Output Contract, §Implementation Requirements); MONOWAVE_READY_PROMPT.md

### [FIB] fibonacci-key-ratios
- RULE: Fibonacci utilities must implement and test retracement/extension/equality/time ratios covering 61.8%, 100%, 138.2%, 161.8%, and 261.8%.
- TYPE: fib
- SOURCE: tasks/TASK_006_FIBONACCI_METRICS.md (§Why This Task Exists, §Tests Required); A06_Fibonacci_Rules_Agent.md; 05_PHASED_DEVELOPMENT_PLAN.md (§Phase 4)
- NOTES: Acceptance checklist enumerates 61.8/100/138.2/161.8/261.8 tested.

### [FIB] fibonacci-safe-division-tolerance
- RULE: Fibonacci implementation must use safe division (handle zero length / division-by-zero), implement tolerance bands, return PASS/FAIL/WARNING/UNKNOWN, include an evidence dictionary, and document ratio formulas.
- TYPE: fib
- SOURCE: tasks/TASK_006_FIBONACCI_METRICS.md (§Implementation Requirements); QG_03_MONOWAVE_AND_RULES.md

### [IMPULSE] impulse-5-wave-structure
- RULE: Validate a 5-wave impulse candidate: check 5-wave directional structure. Output includes impulse rule checks, extension hints, invalidation, confirmation condition.
- TYPE: setup
- SOURCE: tasks/TASK_009_IMPULSE_VALIDATOR.md (§Implementation Requirements, §Output Contract)

### [IMPULSE] impulse-wave2-retrace-le-61.8
- RULE: Check wave 2 retracement <= 61.8% (preferred rule from project notes).
- TYPE: fib
- SOURCE: tasks/TASK_009_IMPULSE_VALIDATOR.md (§Implementation Requirements)

### [IMPULSE] impulse-wave3-not-shortest
- RULE: Check wave 3 is not the shortest (among waves 1, 3, 5).
- TYPE: hard
- SOURCE: tasks/TASK_009_IMPULSE_VALIDATOR.md (§Implementation Requirements); A07_Impulse_Pattern_Agent.md

### [IMPULSE] impulse-wave4-overlap-terminal-exception
- RULE: Check wave 4 overlap rule with a terminal exception placeholder (terminal/diagonal impulse handled separately; if unimplemented, mark as explicit UNKNOWN/WARNING placeholder).
- TYPE: hard
- SOURCE: tasks/TASK_009_IMPULSE_VALIDATOR.md (§Implementation Requirements, §Forbidden Changes); A07

### [IMPULSE] impulse-alternation-soft-rule
- RULE: Check alternation as a soft rule (between wave 2 and wave 4).
- TYPE: guideline
- SOURCE: tasks/TASK_009_IMPULSE_VALIDATOR.md (§Implementation Requirements)

### [CONFIRMATION-LINES] impulse-2-4-line-confirmation
- RULE: Check the 2-4 line confirmation condition (trendline across wave 2 and wave 4 ends) as a confirmation condition, not an instant signal.
- TYPE: setup
- SOURCE: tasks/TASK_009_IMPULSE_VALIDATOR.md (§Implementation Requirements); A07_Impulse_Pattern_Agent.md (§Scope: 2-4 confirmation condition)

### [IMPULSE] impulse-validator-tests
- RULE: Impulse validator tests: valid impulse, wave 3 shortest failure, wave 4 overlap failure/warning, wave 2 deep retracement, 2-4 confirmation condition timing.
- TYPE: validation
- SOURCE: tasks/TASK_009_IMPULSE_VALIDATOR.md (§Tests Required)

### [ZIGZAG] zigzag-abc-structure
- RULE: Zigzag validator input is a 3 mono-wave candidate sequence A-B-C. Check the A-B-C direction sequence. (Zigzag = 5-3-5 approximation.)
- TYPE: setup
- SOURCE: tasks/TASK_007_ZIGZAG_VALIDATOR.md (§Input Contract, §Implementation Requirements); A08_Corrective_Pattern_Agent.md (§Zigzag 5-3-5 approximation)

### [ZIGZAG] zigzag-B-le-61.8-of-A
- RULE: Check B <= 61.8% of A as the preferred zigzag rule.
- TYPE: fib
- SOURCE: tasks/TASK_007_ZIGZAG_VALIDATOR.md (§Implementation Requirements)
- NOTES: B above 61.8 fails or warns based on spec.

### [ZIGZAG] zigzag-C-beyond-A
- RULE: Check C moves beyond A end; compute C vs A ratio.
- TYPE: setup
- SOURCE: tasks/TASK_007_ZIGZAG_VALIDATOR.md (§Implementation Requirements)
- NOTES: C not beyond A fails.

### [CONFIRMATION-LINES] zigzag-0-B-trendline-confirmation
- RULE: Record the 0-B trendline confirmation as a condition, not an instant signal.
- TYPE: setup
- SOURCE: tasks/TASK_007_ZIGZAG_VALIDATOR.md (§Implementation Requirements); A08 (§0-B confirmation)

### [FLAT] flat-3-3-5-structure
- RULE: Flat validator input is a 3 mono-wave candidate sequence A-B-C; check 3-wave corrective candidate. (Flat = 3-3-5 approximation.)
- TYPE: setup
- SOURCE: tasks/TASK_008_FLAT_VALIDATOR.md (§Input Contract, §Implementation Requirements); A08 (§Flat 3-3-5 approximation)

### [FLAT] flat-B-gt-61.8-of-A
- RULE: Check B > 61.8% of A for a flat.
- TYPE: fib
- SOURCE: tasks/TASK_008_FLAT_VALIDATOR.md (§Implementation Requirements)
- NOTES: B below 61.8 = failure test. This threshold distinguishes flat (B>61.8%) from zigzag (B<=61.8%).

### [FLAT] flat-subtype-classifications
- RULE: Support regular/irregular/running failure hints as classifications; check C relationship to A; record 0-B confirmation condition.
- TYPE: setup
- SOURCE: tasks/TASK_008_FLAT_VALIDATOR.md (§Implementation Requirements)
- NOTES: Tests: regular flat, irregular flat, running flat warning, B below 61.8 failure.

### [TRIANGLE] triangle-baseline-and-alternate-lines
- RULE: Triangle rules use a B-D baseline and A-C/C-E alternate line logic. Advanced corrective warnings included.
- TYPE: setup
- SOURCE: agents/A09_Triangle_Diametric_Agent.md (§Scope)

### [DIAMETRIC] diametric-7-leg-structure
- RULE: Diametric is a 7-leg structure. Validate diametric plus neutral/extracting triangle candidates.
- TYPE: setup
- SOURCE: agents/A09_Triangle_Diametric_Agent.md (§Mission, §Scope)
- NOTES: Advanced correctives run only after basic validators exist; unknown cases marked UNKNOWN; do not overfit diagrams; confirmation rules explicit.

### [TERMINAL] terminal-impulse-separated
- RULE: Terminal impulse is a separate pattern (Phase 5 order position 5) handled after basic impulse; the terminal exception to the wave-4 overlap rule must be separated and not folded into the normal impulse validator.
- TYPE: setup
- SOURCE: 05_PHASED_DEVELOPMENT_PLAN.md (§Phase 5); A07_Impulse_Pattern_Agent.md (Acceptance: terminal exception separated)

### [COMPLEX-X] pattern-validator-order
- RULE: Pattern validators are built one pattern at a time in order: 1 Zigzag, 2 Flat, 3 Impulse, 4 Triangle, 5 Terminal impulse, 6 Diametric, 7 Complex correction, 8 Neutral / Extracting triangle. Each pattern is a separate module with unit tests and returns a candidate score and invalidation.
- TYPE: process
- SOURCE: 05_PHASED_DEVELOPMENT_PLAN.md (§Phase 5 — Pattern Validators)

### [VALIDATION] pattern-candidate-output-schema
- RULE: Each pattern validator returns a PatternCandidate with: pattern_type, direction, rule_results, confidence, invalidation_level (if available), confirmation_condition (if available), notes. Every rule returns PASS/FAIL/WARNING/UNKNOWN with details and evidence. Add valid and invalid fixture tests.
- TYPE: validation
- SOURCE: prompts/PATTERN_VALIDATOR_READY_PROMPT.md; QG_04_PATTERN_VALIDATORS.md
- NOTES: Block if code claims certainty without confidence, or if zigzag/flat/impulse logic is mixed into one large function, or trade signals generated before trade engine approval.

### [ICHIMOKU] ichimoku-line-periods
- RULE: Ichimoku calculations: Tenkan 9, Kijun 26, Senkou A/B, and Chikou (calculated carefully without lookahead misuse).
- TYPE: indicator
- SOURCE: tasks/TASK_010_ICHIMOKU_FILTER.md (§Implementation Requirements); A10_Ichimoku_Filter_Agent.md

### [ICHIMOKU] ichimoku-filter-status-values
- RULE: Ichimoku output = indicator columns plus a filter status: supportive, neutral, conflicting, unknown. Ichimoku is context only, not a signal by itself; must not become a standalone trade system and must not override wave invalidations.
- TYPE: indicator
- SOURCE: tasks/TASK_010_ICHIMOKU_FILTER.md (§Output Contract); A10_Ichimoku_Filter_Agent.md
- NOTES: Source uses Ichimoku as context for support/resistance, trend direction, and momentum. No-lookahead Chikou/cloud test required; filter remains optional.

### [INDICATORS] pattern-scoring-weights
- RULE: Pattern scoring uses deterministic weights: PASS adds score; FAIL reduces score strongly; WARNING reduces score mildly; UNKNOWN neutral or small penalty (UNKNOWN does not equal fail). Output = ranked candidates with score, confidence band, and explanation. Warnings reduce confidence.
- TYPE: indicator
- SOURCE: tasks/TASK_011_PATTERN_SCORING.md (§Implementation Requirements); A11_Pattern_Scoring_Agent.md
- NOTES: Scoring must be transparent/explainable, no black-box ML. Tests: deterministic, warning penalty, fail penalty, ranking.

### [SETUP-TRADE] chart-annotation-output
- RULE: Chart annotation must annotate pivots and candidate labels with confidence, draw invalidation/confirmation lines when available, generate manual TradingView steps, and clearly separate confirmed vs pending. No future-known labels shown as real-time.
- TYPE: setup
- SOURCE: tasks/TASK_012_CHART_ANNOTATION.md (§Implementation Requirements); A12_Chart_Annotation_Agent.md
- NOTES: TradingView note must contain symbol/timeframe/pivots/invalidation/confirmation.

### [RISK] backtest-confirmation-time-only
- RULE: Backtest must act only after confirmation_time; support long-only initially; record entry/exit/invalidation reason; keep trade log auditable. Input: bars and candidate events with confirmation_time, invalidation, optional target zone.
- TYPE: risk
- SOURCE: tasks/TASK_013_BACKTEST_SKELETON.md (§Implementation Requirements, §Input Contract); A13_Backtest_Agent.md; QG_05_BACKTEST.md

### [RISK] backtest-metrics
- RULE: Backtest must calculate win rate, expectancy, max drawdown, and profit factor; metrics must be reproducible.
- TYPE: risk
- SOURCE: tasks/TASK_013_BACKTEST_SKELETON.md (§Implementation Requirements); 05_PHASED_DEVELOPMENT_PLAN.md (§Phase 7); QG_05_BACKTEST.md

### [RISK] backtest-no-overoptimization
- RULE: Do not optimize parameters / do not over-optimize; block if parameters are over-optimized without separation of train/test. Backtest must not use future-confirmed pivots as if known earlier.
- TYPE: risk
- SOURCE: tasks/TASK_013_BACKTEST_SKELETON.md (§Forbidden Changes); A13; QG_05_BACKTEST.md

### [VALIDATION] backtest-tests-required
- RULE: Backtest tests: cannot enter before confirmation_time, invalidation exit test, metrics calculation test, empty candidate test.
- TYPE: validation
- SOURCE: tasks/TASK_013_BACKTEST_SKELETON.md (§Tests Required)

### [VALIDATION] no-lookahead-audit-scope
- RULE: No-lookahead audit inspects timestamp usage, pivot confirmation logic, backtest event timing, and Ichimoku shifting; writes failing tests for leakage. Required tests: global no-lookahead test, pivot confirmation audit test, backtest action timing test. Must not approve code with unresolved leakage.
- TYPE: validation
- SOURCE: tasks/TASK_014_NO_LOOKAHEAD_AUDIT.md (§Implementation Requirements, §Tests Required); A14_No_Lookahead_QA_Agent.md
- NOTES: Acceptance: every timestamp has meaning; backtest cannot act before confirmation; future columns not used.

### [VALIDATION] qg00-repository-bootstrap
- RULE: Repository bootstrap passes only if folder structure exists, tests can be discovered, shared rules exist, no feature logic was prematurely implemented, LLM workflow rules exist. Block if repo contains mixed wave/trading/backtest code before data contract, or no test framework.
- TYPE: validation
- SOURCE: quality_gates/QG_00_REPOSITORY_BOOTSTRAP.md

### [VALIDATION] qg02-pivot-engine-gate
- RULE: Pivot engine passes only if pivots have pivot_time and confirmation_time, percentage reversal mode is deterministic, minimum bar distance is enforced, and no-lookahead tests exist. Block if backtest can act at pivot_time before confirmation, or pivot detector changes wave labels directly.
- TYPE: validation
- SOURCE: quality_gates/QG_02_PIVOT_ENGINE.md

### [VALIDATION] qg03-monowave-rules-gate
- RULE: Mono-wave and rule engine passes only if consecutive pivots produce mono-waves, price/time metrics are tested, Fibonacci helpers handle zero division, and RuleResult uses PASS/FAIL/WARNING/UNKNOWN. Block if patterns are detected directly from candles or rule results are not explainable.
- TYPE: validation
- SOURCE: quality_gates/QG_03_MONOWAVE_AND_RULES.md

### [VALIDATION] qg04-pattern-validators-gate
- RULE: Pattern validators pass only if each pattern is a separate module, each validator returns candidate objects and rule results, invalidation and confirmation are explicit, and tests exist for valid and invalid examples. Block if code claims certainty without confidence, zigzag/flat/impulse logic mixed into one large function, or trade signals generated before trade engine approval.
- TYPE: validation
- SOURCE: quality_gates/QG_04_PATTERN_VALIDATORS.md

### [PROCESS-METHOD] phased-development-phases
- RULE: Phases: 0 Repository and Governance; 1 Alpaca Data Engine; 2 Pivot Engine; 3 Mono-Wave Engine; 4 Rule Engine and Fibonacci Metrics; 5 Pattern Validators; 6 Chart and TradingView Manual Output; 7 Backtest Harness; 8 Dashboard and Automation Expansion; 9 ML Later (only after labels). Do not start Phase 9 until enough validated examples exist.
- TYPE: process
- SOURCE: 05_PHASED_DEVELOPMENT_PLAN.md

### [PROCESS-METHOD] context-loading-tiers
- RULE: Context tiers — Tier 1 always load: 01_SHARED_SYSTEM_RULES.md, current task card, current agent file, relevant spec. Tier 2 load only if needed: architecture file, data contract, previous handoff, related tests. Tier 3 (source docs) load rarely, only for rule clarification or documentation. Golden rule: use the smallest amount of context needed to complete the task safely.
- TYPE: process
- SOURCE: 04_CONTEXT_LOADING_POLICY.md
- NOTES: Per-phase avoid-loading table, e.g. Mono-wave avoids Ichimoku/ML/backtest; Pattern loads specific pattern spec only.

### [SCOPE] ichimoku-not-standalone-not-override
- RULE: Ichimoku must not be used as a standalone trade system and must not override wave invalidations; it is context, not a signal by itself; must not use future cloud in backtest.
- TYPE: scope
- SOURCE: agents/A10_Ichimoku_Filter_Agent.md (§Forbidden Responsibilities, §Acceptance Checklist)

### [SCOPE] documentation-no-invented-claims
- RULE: Documentation must not change algorithms, invent performance claims, or remove limitations; a limitations section must be present; no exaggerated performance claims.
- TYPE: scope
- SOURCE: tasks/TASK_015_DOCUMENTATION_PACK.md; agents/A15_Documentation_Agent.md

## FILES READ
- 00_AGENT_OPERATING_MODEL.md
- 01_SHARED_SYSTEM_RULES.md
- 02_AGENT_REGISTRY.md
- 03_AGENT_HANDOFF_PROTOCOL.md
- 04_CONTEXT_LOADING_POLICY.md
- 05_PHASED_DEVELOPMENT_PLAN.md
- 06_PROMPT_USAGE_GUIDE.md
- FILE_INDEX.md
- README.md
- agents/A00_Project_Manager_Agent.md
- agents/A01_Architecture_Agent.md
- agents/A02_Data_Engine_Agent.md
- agents/A03_Data_Quality_Agent.md
- agents/A04_Pivot_Engine_Agent.md
- agents/A05_MonoWave_Engine_Agent.md
- agents/A06_Fibonacci_Rules_Agent.md
- agents/A07_Impulse_Pattern_Agent.md
- agents/A08_Corrective_Pattern_Agent.md
- agents/A09_Triangle_Diametric_Agent.md
- agents/A10_Ichimoku_Filter_Agent.md
- agents/A11_Pattern_Scoring_Agent.md
- agents/A12_Chart_Annotation_Agent.md
- agents/A13_Backtest_Agent.md
- agents/A14_No_Lookahead_QA_Agent.md
- agents/A15_Documentation_Agent.md
- agents/A16_Release_Guardian_Agent.md
- prompts/CODEX_TASK_PROMPT_TEMPLATE.md
- prompts/DATA_ENGINE_READY_PROMPT.md
- prompts/MASTER_CLAUDE_CODE_START_PROMPT.md
- prompts/MONOWAVE_READY_PROMPT.md
- prompts/PATTERN_VALIDATOR_READY_PROMPT.md
- prompts/PIVOT_ENGINE_READY_PROMPT.md
- quality_gates/QG_00_REPOSITORY_BOOTSTRAP.md
- quality_gates/QG_01_DATA_ENGINE.md
- quality_gates/QG_02_PIVOT_ENGINE.md
- quality_gates/QG_03_MONOWAVE_AND_RULES.md
- quality_gates/QG_04_PATTERN_VALIDATORS.md
- quality_gates/QG_05_BACKTEST.md
- tasks/TASK_000_BOOTSTRAP_REPOSITORY.md
- tasks/TASK_001_DATA_CONTRACT.md
- tasks/TASK_002_ALPACA_DATA_ENGINE.md
- tasks/TASK_003_PARQUET_CACHE.md
- tasks/TASK_004_PIVOT_ENGINE.md
- tasks/TASK_005_MONOWAVE_ENGINE.md
- tasks/TASK_006_FIBONACCI_METRICS.md
- tasks/TASK_007_ZIGZAG_VALIDATOR.md
- tasks/TASK_008_FLAT_VALIDATOR.md
- tasks/TASK_009_IMPULSE_VALIDATOR.md
- tasks/TASK_010_ICHIMOKU_FILTER.md
- tasks/TASK_011_PATTERN_SCORING.md
- tasks/TASK_012_CHART_ANNOTATION.md
- tasks/TASK_013_BACKTEST_SKELETON.md
- tasks/TASK_014_NO_LOOKAHEAD_AUDIT.md
- tasks/TASK_015_DOCUMENTATION_PACK.md
- templates/AGENT_FILE_TEMPLATE.md
- templates/HANDOFF_TEMPLATE.md
- templates/TASK_CARD_TEMPLATE.md
