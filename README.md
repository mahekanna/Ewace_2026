# ewave — Elliott Wave / NeoWave Full-Automation Platform

*Causal detection → rule validation → signals → ghost-forward validation →
backtest → risk → paper trading. Live-trading gates fail closed. Pure-stdlib
core. Analysis tooling only — not investment advice.*

## Quickstart

```bash
python3 -m unittest discover -s tests -p "test_*.py"   # full suite, no install needed
pip install -e .                                       # console script `ewave`

ewave validate-data --all                              # check the cached bar store
ewave scan --watchlist default --tf 15m --profile experimental
ewave ghost-forward --symbols AVGO --tf 15m --profile experimental --horizon 96
ewave backtest --symbols AVGO,MRVL --tf 15m --profile experimental
ewave paper-trade --replay --watchlist default --tf 15m --days 120
ewave report --date today
```

## The five-minute tour

- **Pipeline & decisions:** docs/ARCHITECTURE.md · **phases/roadmap:**
  docs/FULL_AUTOMATION_ROADMAP.md · **the one policy that rules them all:**
  docs/NO_LOOKAHEAD_POLICY.md
- **Rule spec:** docs/RULESET.md (every knob cites Elliott/NeoWave doctrine);
  profiles in configs/profiles.json span the validated crude wave-3 entry
  (`experimental`, +0.17..+0.31R/year on AVGO/MRVL 15m — reproduced by the
  test suite) to the rule-faithful strict variant (RULESET §H).
- **Honesty machinery:** ghost-forward snapshot-freeze validation
  (ewave.validation.ghost_forward), DSR/PSR/MinTRL stats + append-only trials
  registry (registry/trials.jsonl) — edges are judged by DSR, never raw
  expectancy. The next-leg forecast direction is retained REF-only: a year of
  causal replay showed it has no edge (docs/FORWARD_GHOST_TEST_FINDINGS.md).
- **Data:** contract JSON in data/live/ (~25 symbols); adapters for
  Alpaca/FMP/yfinance/CSV + an MCP-export bridge for sandboxes
  (scripts/mcp_export.py, docs/COLLAB_RUNBOOK.md).
- **Safety:** risk engine (sizing, loss limits, exposure caps, cooldown, kill
  switch) gates every order; the live executor refuses to start — and even
  fully-gated raises — by design (docs/LIVE_TRADING_SAFETY_POLICY.md).
- Legacy `wavelib` imports keep working (thin shims over ewave).

---

# Research bundle — AVGO + MRVL session analysis (historical)
*Built across the session on live TVremix data. Updated through Fri Jun 5 2026.*
*Analysis and tooling only — not investment advice.*

---

## 1. The methodology stack (in the order it should run)

A wave label says **where** a turn is *allowed*; it does not say **whether** one is happening. So the engine is layered, each layer failing independently:

1. **Channels first** (NeoWave construction order) — 2-4 trendline, 1-3 upper channel, throw-over vs fell-short.
2. **Elliott structure** — 3 hard rules + guidelines; corrective-pattern classification.
3. **NeoWave overlays** — Similarity & Balance (price *and* time), retracement logic, terminal impulsions, complex-correction zoo.
4. **Fibonacci** — wave relationships, retrace/extension target zones.
5. **Reversal confluence** — momentum divergence, MACD, volume climax, CHoCH/structure, channel break, (external) Hurst/FLD cycle timing. Only act when the *score* crosses a threshold AND the label permits.

---

## 2. AVGO — summary

**Macro count (weekly):** Primary **(I)** $41.51→$251.88, **(II)** →$138.10 (54% retrace), **(III)** $138.10→$495.00.
Two independent Fib projections landed within ~$1 of the $495 top (wave ⑤ = 1.61× ①; (III) = 1.70× (I)).

**Top mechanism (4h):** ending diagonal / NeoWave **terminal impulsion** ($290→429→394→442→405→495) — *expanding/irregular* (honest caveat: non-textbook).

**Channels:** 2-4 line ~**$301** (unbroken at $385 → completion not yet channel-confirmed); wave ⑤ **fell short** of the $560 upper channel → weak/truncated fifth.

**Current status (Jun 5):** price **$385.74** — fell $495→$385 as a clean **A-B-C (corrective)** move, landing **inside the $358–410 zone** (my chart's (IV)≈$384 projection nailed it). Confluence score **1/7** = structurally allowed, not yet confirmed.

**Levels:**
- $358–410 — shallow (IV) zone (price here now)
- $290–301 — deep target (2-4 break ≈ terminal-retrace) — **not reached**; my "$290 fast" call was too aggressive vs the shallow reality
- $540–620 — wave (V) target *if* (IV) holds shallow; **truncation risk to ~$500–510** if (IV) goes deep
- **$251.88 — hard invalidation** (weekly close below = whole impulse complete)

---

## 3. MRVL — summary

**Macro count (weekly):** **(I)** $33.75→$127.48, **(II)** →$47.09 (85.8% retrace — deep, edge-of-legal), **(III)** $47.09→$324.20 (+589%). Internal: ((1))$103, ((2))$76, ((3)) the parabola $76→$324 (4.5× extended — S&B-stretched, lower confidence).

**Top mechanism:** clean non-overlapping thrust = **extending impulse, NOT a terminal** → a *normal* correction expected, not a collapse. $324 hit ~3.0× ext of wave (I) ($328).

**Channels:** threw **over** the $223 upper line (blow-off overthrow); lower channel ~$206 (intact until broken).

**Current status (Jun 5):** price **$263.47** — pulled back from $324 as a 3-wave move into the **$229–266 ((4)) zone**. Confluence score **1/7** = allowed, not confirmed.

**Levels:**
- $360–386 (stretch $422) — still-extending upside if it turns here
- $229–266 — normal ((4)) zone (price at top of it now)
- then ((5)) to **$380–420** new highs
- first-crack trigger: 4h close < $277 (already broke intraday — watch the close)

---

## 4. The disagreement with @ArtavestPro (X)

Their count: $290 = wave 2 low, $290→$495 = wave 1, correction to **$390**, then **wave 3 to $1,000**, invalidation $289.95.
- **Agree:** $290 floor (their $289.95 = my 2-4/terminal confluence), completed five, correction-then-up.
- **Differ:** degree (they call $495 wave **1**; I called it Primary **(III)**) and target ($1,000 vs $540–620/truncation).
- **Verdict:** their degree is *legitimate* (most subjective call in Elliott). But $1,000 has **no shown Fib derivation** (a measured wave-3 from $390 lands ~$720, even 2.618× ~$925) and is bundled with a subscription pitch — treat the *number* as marketing, the *invalidation* as the useful part. **The $390 hold/fail resolves whose degree is right.**

---

## 5. File index (project layout)

| File | What it is |
|------|-----------|
| `ew_neowave_rules.py` | **Main rule engine** — Elliott hard rules + guidelines, corrective classifiers, diagonals, NeoWave S&B / proportion / retracement logic / **computed channeling** / terminals / complex-correction zoo. Run `python3 ew_neowave_rules.py`. |
| `neowave_toolkit.py` | Helper toolkit — ZigZag pivots, Fib helpers, S&B, terminal projection, wave-5 truncation. |
| `confluence_score.py` | **Reversal scorer** — RSI/MACD divergence, volume climax, CHoCH, channel break, swing classifier → stacked confidence score. |
| `avgo_4h_elliott_wave.html` | AVGO 4h chart — ending-diagonal top, (IV) target zones. |
| `avgo_wave_projection.html` | AVGO forward path — (IV)≈$384 → (V) $540–620 (the projection that hit). |
| `mrvl_elliott_wave.html` | MRVL multi-timeframe — parabolic (III) blow-off. |
| `neowave_projections_avgo_mrvl.html` | Side-by-side NeoWave projections (terminal vs extending impulse). |
| `index.html` | Dashboard linking all charts + this summary. |

---

## 6. Honest caveats carried throughout
- Elliott **degree** is the most subjective call — reasonable analysts (incl. ArtavestPro) label $495 differently; that is genuinely unresolved until $390/$300 resolves.
- AVGO's terminal is **expanding/irregular**, not textbook.
- MRVL's ((3)) is **S&B-stretched** (3.0×+) → lower-confidence count.
- The **terminal-retrace "$290 fast"** call over-projected depth/speed; the shallow $384 zone was the better read. (Recalibrate the terminal rule.)
- Confluence RSI/divergence strand needs **>14 bars** of history to activate.
- Both names currently score **1/7** — *no* confirmed reversal yet, only structural permission.
