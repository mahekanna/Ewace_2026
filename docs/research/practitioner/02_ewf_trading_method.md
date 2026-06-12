# 02 — EWF Trading Method: Blue Box, Sequences, and Next-Wave Prediction

**Document type:** Practitioner methodology reference — trading rules layer  
**Date:** 2026-06-12  
**Prior context:** `docs/research/deep/09_ewf_theory_patterns.md` (theory harvest) and
`docs/research/deep/10_ewf_method_tools.md` (tools/indicators). This document goes
deeper on the *trading mechanics* — setup identification, entry/stop/target, scaling,
and next-wave prediction logic.  
**Retrieval note:** elliottwave-forecast.com returns HTTP 403 to automated fetches.
All content is derived from Google-indexed page snippets, third-party write-ups,
Forex Factory threads, and public blog syndication. Rules stated verbatim where
text was unambiguous in search output; paraphrased otherwise. Confidence is HIGH
for published numerical rules (snippets quote the live page text); MEDIUM for
procedural sequences assembled from multiple example articles.

---

## 1. Overview: EWF's Trading System in One Paragraph

EWF (elliottwave-forecast.com) runs a subscription service serving ~78 markets.
Their analytical system layers five components: (1) classical Elliott Wave rules and
pattern taxonomy (3 unbreakable rules + corrective/impulsive hierarchy); (2) a
**swing-sequence counting framework** (3/7/11 corrective vs 5/9/13 impulsive) that
treats sequence completion/incompletion as the primary trading edge; (3) the
**Blue Box** — a price zone spanning the 100%–161.8% Fibonacci extension of the
first corrective leg, drawn inside every 3-, 7-, or 11-swing corrective sequence;
(4) the **Right Side tag** — a color-coded directional stamp (Green=bullish,
Red=bearish, Black=unclear) that filters which side of any Blue Box to trade; and
(5) RSI divergence + market correlation as structural confirmation. The phrase
"react, don't predict" captures their stance: they *pre-draw* the Blue Box zone
algorithmically, then wait for price to *enter* it before taking action. They do
not forecast whether price will enter the box — only what to do if it does.

Sources:
- [Trading Elliott Wave Charts with the Right Side Tag and Blue Boxes](https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/)
- [BlueBox Wins: What is a BlueBox Win?](https://elliottwave-forecast.com/bluebox-wins/blue-box-wins-explained/)
- [The Right Side: Only Way to Survive in the Trading World](https://elliottwave-forecast.com/trading/right-side-helps-survival-trading-world/)
- [Trading Edge through Swings Sequences](https://elliottwave-forecast.com/elliottwave/trading-edge-through-swing-sequences/)

---

## 2. Methodology: The Five Analytical Layers

### 2.1 Motive Sequence vs Corrective Sequence

EWF defines all market moves in terms of a **swing count**, where one "swing" is
a directional leg between two adjacent ZigZag pivots (alternating high-to-low or
low-to-high). The count maps onto two arithmetic series:

| Series type | Swing counts |
|---|---|
| **Impulsive / motive** | 5, 9, 13, 17, 21 … |
| **Corrective** | 3, 7, 11, 15, 19 … |

A standard 5-wave impulse contains 5 swings. A Wave 3 extension expands the
impulse to 9 swings. A double extension (waves 3 and 5) gives 13 swings. A simple
ABC zigzag = 3 swings; a WXY double-three = 7 swings; a WXYXZ triple-three = 11
swings.

**The trading edge:** If the visible swing count is one of the impulsive numbers
(5, 9, 13…), the trend is incomplete and an extension is expected. If the count
is one of the corrective numbers (3, 7, 11…), the correction is complete and the
prior trend should resume.

> "If analysts discover the number of swings on the chart is one of the numbers in
> the motive sequence, they can expect the current trend to extend further."

Sources:
- [Elliott Wave Structures & Swing Sequence](https://elliottwave-forecast.com/elliott-wave-structures-and-swing-sequence/)
- [Trading Edge through Swings Sequences](https://elliottwave-forecast.com/elliottwave/trading-edge-through-swing-sequences/)
- [Trading Right Side using Elliott Wave Theory, Cycles and Sequences](https://elliottwave-forecast.com/trading-right-side-using-elliott-wave-theory-cycles-and-sequences/)

---

### 2.2 The Right Side Tag System

The Right Side tag is a directional bias overlay derived from the higher-degree
swing sequence. It is displayed on every EWF chart:

| Stamp color | Meaning | Trading rule |
|---|---|---|
| **Green** | Bullish Sequence — incomplete motive sequence upward | Buy dips only |
| **Red** | Bearish Sequence — incomplete motive sequence downward | Sell rallies only |
| **Black** | Unclear / choppy | Do not trade |

> "When the chart shows the right side is higher in green, traders should only buy
> the dips and not try to sell pullbacks. Conversely, when the chart shows the right
> side is lower in red, traders should only attempt to sell rallies."

The Right Side is derived from the larger-degree sequence: if the daily chart is in
a Bullish Sequence, the 4H chart Blue Box entries should be longs. The Right Side
can flip when price breaks the higher-degree invalidation level for that timeframe.

**Multi-timeframe stacking:** Each timeframe carries its own Right Side tag and its
own invalidation level. A trade only has the highest conviction when the Right Side
tags align top-down (Weekly → Daily → 4H).

Sources:
- [Trading Elliott Wave Charts with the Right Side Tag and Blue Boxes](https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/)
- [The Right Side in Elliott Wave](https://elliottwave-forecast.com/elliottwave/right-side-elliott-wave/)
- [Trading Right Side using EWT, Cycles and Sequences](https://elliottwave-forecast.com/trading-right-side-using-elliott-wave-theory-cycles-and-sequences/)

---

### 2.3 The Blue Box: High-Frequency Inflection Zone

The Blue Box is EWF's primary mechanical entry tool. It is drawn as a price band
and is not a support/resistance zone from prior price action — it is a
**Fibonacci-extension projection** from the current corrective swing structure.

#### 2.3.1 Conceptual definition

> "Blue Boxes are High-Frequency and High Probability / Low Risk areas based in a
> relationship of sequences, cycles and calculated using extensions."

> "Both buyers and sellers agree in the blue box in the direction of the next move
> for at least 3 waves." (Hence the label "no enemy areas.")

Claimed reaction rate: ~85% of the time price entering a Blue Box produces at
least a 3-wave bounce. No independent audit of this statistic is published.

#### 2.3.2 Blue Box construction — step-by-step

The following procedure is assembled from multiple worked examples. The same
calculation applies to bullish and bearish Blue Boxes (direction reversed).

**For a BULLISH Blue Box (corrective pullback in a bullish sequence):**

1. **Identify the dominant uptrend** — confirm a Green Bullish Sequence stamp
   (incomplete impulsive count at higher degree means trend is up).
2. **Identify the corrective structure** — confirm the pullback is a 3-, 7-, or
   11-swing corrective sequence (NOT a 5/9/13 impulsive one).
3. **Identify the anchor swings:**
   - **Swing A / Wave W**: the *first* directional leg of the correction
     (downward in a bullish correction). Anchor: from the swing high at the
     start of the correction (call it point O) down to the first corrective low
     (call it point A).
   - **Swing B / Wave X**: the retracement bounce from A back toward O.
     End of swing B is point B (a swing high below O).
   - For a 3-swing ABC: O → A → B sets up the extension. Extension direction is
     down from B, measuring 100%–161.8% of the distance O→A.
   - For a 7-swing WXY: the same measurement applies off the W leg with the
     X connector rebound as the starting point for the Y extension.
4. **Compute the Blue Box boundaries:**
   - **Lower boundary (= entry zone top):** 100% extension of Swing A measured
     from the end of Swing B.
     `BB_lower = B_price - 1.000 × |A_price - O_price|` (for a bullish box)
   - **Upper boundary (= invalidation):** 161.8% extension of Swing A from B.
     `BB_upper = B_price - 1.618 × |A_price - O_price|`
   - The Blue Box is the price band `[BB_upper, BB_lower]` (the box spans from
     the 100% to the 161.8% extension, with 100% at the top and 161.8% at
     the bottom for a bullish box).
5. **Draw on chart** as a shaded rectangle between `BB_lower` and `BB_upper`.

**Equal Legs relationship:** The 100% extension point is precisely the *Equal
Legs* level (where C=A in an ABC, or Y=W in a WXY). EWF uses "Equal Legs" and
the lower Blue Box boundary as synonyms.

> "Equal legs occurs where the magnitude of swing A is equal to swing C (A=C)
> with B as the correction."

**Why 161.8% is the outer boundary / invalidation:**

> "If the third swing extends only to 100% of the first swing, then it's an ABC
> zigzag. If the third swing extends to at least 161.8% of the first swing, then
> the odds increase that we are in an impulsive structure."

A C wave (or Y wave) extending beyond 161.8% of A (or W) is no longer behaving
like a corrective wave — it is transitioning into a Wave 3 of an impulse. This
structural rule is why 161.8% is the stop/invalidation anchor.

Sources:
- [BlueBox Wins: What is a BlueBox Win?](https://elliottwave-forecast.com/bluebox-wins/blue-box-wins-explained/)
- [Equal Legs: What does it mean?](https://elliottwave-forecast.com/elliottwave/equal-legs/)
- [Did you know what the meaning of term Equal Legs is?](https://elliottwave-forecast.com/elliottwave/equal-legs-elliotts-wave-theory/)
- [Why Double Three WXY is A Better Structure to Trade Than Zigzag ABC](https://elliottwave-forecast.com/elliottwave/why-double-three-wxy-is-a-better-structure-to-trade-than-zigzag-abc/)
- [S&P 500 E-Mini (ES_F) Elliott Wave: Blue Box Buy Setup Explained](https://elliottwave-forecast.com/stock-market/sp-500-e-mini-es_f-elliott-wave-blue-box/)

---

### 2.4 ABC vs WXY in the Context of Blue Box Setup Selection

EWF prefers WXY (double three) over ABC (zigzag) as the label for the corrective
structure that contains the Blue Box. The reason is structural risk reduction:

- In a **WXY**, the first leg (W) subdivides into **3 waves**. This means it
  structurally cannot be confused with a Wave 1 impulse (which would need 5
  sub-waves). Buying at the Y extension target (100% of W) carries lower risk
  that the decline is actually a Wave 3.
- In an **ABC** zigzag, the first leg (A) subdivides into **5 waves** —
  identical to a Wave 1 impulse. There is always ambiguity: is the 5-wave A a
  corrective A, or the beginning of a new impulsive Wave 1/3? Buying at C's
  100% extension risks buying into a continuing impulse.

> "WXY is a better corrective pattern to trade than ABC, as the pattern reduces
> the risk that the correction will become an impulse."

**Practical rule:** EWF analysts first check the internal count of the first
leg. If it has 3 sub-waves → label WXY, use the Blue Box. If it has 5 sub-waves →
label ABC (or possibly the start of an impulse) — the Blue Box is still valid but
the ambiguity risk is noted.

**Fibonacci targets within WXY:**
- Wave Y typically ends at 100%–123.6% of Wave W. The Blue Box spans 100%–161.8%.
- Wave Y extending to exactly 100% = Equal Legs = the center of the highest-
  probability zone.
- Wave Y at 123.6% still within the box — common landing zone for normal
  double-three corrections.
- Beyond 161.8% = structural invalidation (correction becoming impulse).

Sources:
- [Why Double Three WXY is A Better Structure to Trade Than Zigzag ABC](https://elliottwave-forecast.com/elliottwave/why-double-three-wxy-is-a-better-structure-to-trade-than-zigzag-abc/)
- [ABC and WXY: difference between both structure](https://elliottwave-forecast.com/elliottwave/difference-wxy-abc-structure/)
- [WXY and ABC Elliott Wave Structure: Key Differences](https://elliottwave-forecast.com/video-blog/wxy-elliottwave-structure/)

---

### 2.5 RSI Divergence as Structural Confirmation

EWF uses RSI (14-period by default) not as an overbought/oversold filter but as a
**structural validator** — a near-rule rather than a guideline.

**Core RSI rules:**
1. A valid 5-wave impulse must end with **RSI divergence** at Wave 5: price makes
   a new high while RSI makes a *lower* high vs. Wave 3. Absence of divergence
   means the move is likely not complete.
2. A valid corrective structure should end **without RSI divergence**. If RSI is
   diverging at what looks like the end of a correction, the structure may actually
   be an impulse (Wave 5 of an impulse in the opposite direction).
3. Each impulsive sub-division (wave 1, 3, 5) should carry **internal RSI
   divergence** in its own internals (at the (v) of 1, (v) of 3, and wave 5 level).
4. **Incomplete 7-swing test:** If a structure looks like a completed 5-wave
   impulse but shows no RSI divergence, it is likely still in an incomplete
   7-swing corrective. RSI divergence presence confirms impulse completion;
   absence suggests continuation.

> "RSI divergence is used to check if an instrument is in wave 5, and also to
> check if the structure is an incomplete 7 swing structure. Impulse structures
> should end with RSI divergence and corrective structures should end without
> RSI divergence."

**At Blue Box entries:** RSI divergence on the corrective sequence's final leg
(Wave C or Wave Y) is a *positive* confirmation of a legitimate corrective end —
it signals the correction itself is showing internal exhaustion, supporting the
bounce thesis.

Sources:
- [How Momentum Indicator (RSI) is Used with Elliott Wave](https://elliottwave-forecast.com/elliottwave/how-momentum-indicator-is-used-with-elliott-wave/)
- [Elliott Wave Analysis with MACD, RSI and Fibonacci Divergence](https://elliottwave-forecast.com/trading/elliott-wave-divergence-macd-rsi-fibonacci/)
- [Using RSI to Identify Elliott Waves](https://elliottwave-forecast.com/trading/using-relative-strength-index-identify-elliott-waves/)

---

### 2.6 Market Correlation and the Proprietary Pivot System

EWF describes a two-part objectivity layer:

1. **Market Correlation ("Elliott Wave 2.0"):** When a market has an ambiguous
   wave count, find a correlated market with a clear structure and use that
   structure as a template. This "contrarian instrument" technique reduces
   relabeling frequency.
   - First-dimension correlation: two instruments moving in the same direction.
   - Second-dimension correlation: two instruments moving in opposite directions
     but with structurally correlated swings in time.

2. **Proprietary Pivot System:** Combines RSI + CCI + Stochastic RSI to
   independently confirm whether a cycle/wave has ended. The exact algorithm
   is proprietary and not publicly specified. It functions as a second filter on
   top of wave labeling — if the pivot system says a cycle has not ended, EWF
   will not declare the wave complete even if the price structure looks complete.

Sources:
- [Elliott Wave Theory 2.0: Market Correlation secrets for better Forecasting](https://elliottwave-forecast.com/elliottwave/new-elliott-wave-theory-market-correlation-and-rsi-in-elliott-wave/)
- [Using Market Correlation and RSI in the new EWF theory](https://elliottwave-forecast.com/elliottwave/the-new-elliott-wave-theory-using-market-correlation-and-rsi-in-elliott-wave/)

---

## 3. Enumerated Rules

### Part A — Setup / Identification Rules

**A1. Sequence-type classification**  
Count all alternating pivot swings from a clear structural origin. If the count
is in the series {5, 9, 13, 17, 21…}, classify the move as a *motive (impulsive)
sequence* — trend is incomplete, extension expected. If the count is in the series
{3, 7, 11, 15, 19…}, classify as a *corrective sequence* — correction is complete
or nearing completion, trend resumption expected.

Source: [Elliott Wave Structures & Swing Sequence](https://elliottwave-forecast.com/elliott-wave-structures-and-swing-sequence/)

---

**A2. Right Side determination**  
Before drawing a Blue Box on any timeframe, check the higher-degree Right Side
tag. A Green (Bullish) stamp is required for a long Blue Box setup; a Red
(Bearish) stamp is required for a short Blue Box setup. A Black stamp = no trade.
The Right Side is invalid (and must be rechecked) if price closes through the
higher-degree invalidation level associated with the stamp.

Source: [Trading Elliott Wave Charts with the Right Side Tag and Blue Boxes](https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/)

---

**A3. Blue Box placement — corrective sequence confirmed**  
A Blue Box is only drawn when the current counter-trend move is confirmed as a 3-,
7-, or 11-swing *corrective* sequence. A 5-, 9-, or 13-swing counter-trend move
is a *motive* sequence in the opposite direction and does NOT get a Blue Box in
the original trend's direction.

Source: [BlueBox Wins: What is a BlueBox Win?](https://elliottwave-forecast.com/bluebox-wins/blue-box-wins-explained/)

---

**A4. Blue Box construction — Fibonacci anchor**  
Given anchor swings O (start of correction), A (first corrective leg end), B (end
of retracement against A):
- Blue Box lower boundary = B ± (100% × |A−O|) (the Equal Legs level)
- Blue Box upper boundary = B ± (161.8% × |A−O|) (the structural invalidation level)
- Direction of ± is the same as the direction of the A leg (i.e., further in the
  corrective direction from B).

For a **WXY**, "A" = the end of Wave W; "O" = the start of Wave W; "B" = the end
of Wave X. The Blue Box marks where Wave Y should end.  
For an **ABC**, "A" = the end of Wave A; "O" = the start of Wave A; "B" = the end
of Wave B. The Blue Box marks where Wave C should end.

Source: [Why Double Three WXY is A Better Structure to Trade Than Zigzag ABC](https://elliottwave-forecast.com/elliottwave/why-double-three-wxy-is-a-better-structure-to-trade-than-zigzag-abc/)

---

**A5. WXY vs ABC preference rule**  
When the first corrective leg has **3 internal sub-waves** → label the structure
WXY. Buy at the Y extension Blue Box. Risk that the correction becomes a new
impulse is reduced because a 3-wave W cannot be mistaken for a Wave 1.  
When the first corrective leg has **5 internal sub-waves** → label ABC. The Blue
Box is still computed the same way, but note that the ambiguity risk (A could be
Wave 1 of a new impulse) is higher. In strong impulsive contexts, avoid trading
the Blue Box against the prevailing larger trend when labeled ABC.

Source: [Why Double Three WXY is A Better Structure to Trade Than Zigzag ABC](https://elliottwave-forecast.com/elliottwave/why-double-three-wxy-is-a-better-structure-to-trade-than-zigzag-abc/)

---

**A6. Sequence completion signal — the "7 swings = done" rule**  
When a corrective swing count reaches 7 (a complete WXY double-three), the
correction is considered structurally complete. If price is simultaneously near
the 100% extension (Blue Box lower boundary), the probability that correction is
over and trend resumes is highest. The signal is the *combination* of: count = 7,
price = in Blue Box, Right Side = aligned.

Source: [Elliott Wave Structures & Swing Sequence](https://elliottwave-forecast.com/elliott-wave-structures-and-swing-sequence/)

---

**A7. Incomplete 5-swing corrective = extension coming**  
If a corrective count stands at 5 swings (neither in the corrective series
{3,7,11} nor the impulsive series {5,9,13} in a way that fits the structural
context), treat the move as an *incomplete corrective* — the 6th swing (bounce)
will likely fail and the 7th swing (final corrective leg) will reach the Blue Box.
The 5-swing state is a warning: do not buy yet. Wait for the 6th swing to complete
before entering at the 7th swing zone.

Source: [Trading Edge through Swings Sequences](https://elliottwave-forecast.com/elliottwave/trading-edge-through-swing-sequences/)

---

**A8. RSI divergence at corrective end — positive confirmation**  
When price enters the Blue Box AND the final corrective leg (C or Y) shows RSI
divergence on the sub-wave level (price lower, RSI higher for a bullish setup),
this is a positive confirmation that the correction is exhausting. The absence of
divergence does not disqualify the setup but lowers conviction.

Source: [How Momentum Indicator (RSI) is Used with Elliott Wave](https://elliottwave-forecast.com/elliottwave/how-momentum-indicator-is-used-with-elliott-wave/)

---

**A9. Motive sequence incomplete = buy the corrective pullback**  
When the higher-degree move shows an *incomplete* impulsive swing count (e.g.,
5 swings up in what needs to reach 9), any 3- or 7-swing corrective pullback is
a setup, not a reversal. EWF stamps the chart Bullish Sequence and waits for the
corrective count to reach 3 or 7 (with Blue Box confluence) before entering long.

Source: [Trading Edge through Swings Sequences](https://elliottwave-forecast.com/elliottwave/trading-edge-through-swing-sequences/)

---

### Part B — Trade Rules (Entry / Stop / Target / Scaling)

**B1. Entry — touch the Blue Box, react before committing**  
EWF's stance is explicitly "react, don't predict." They do not enter before price
reaches the Blue Box. The first entry trigger is **price touching the 100%
extension level** (the Equal Legs / lower Blue Box boundary). Some analysts wait
for a 1-bar or 1-candle reaction off the Blue Box before entering (a small bounce
indicating buyers/sellers appearing), but the Box itself is the permissible entry
zone. Entering outside the Blue Box (before price reaches it) is not part of
their protocol.

> "Blue Boxes are the areas that traders can attempt to enter the market in the
> direction of the right side stamp."

Source: [Trading Elliott Wave Charts with the Right Side Tag and Blue Boxes](https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/)

---

**B2. Entry — position sizing rule**  
Maximum risk per trade = **2% of capital**. Stop placement determines position
size: `size = (2% × account) / (entry − stop)`. This is stated explicitly and
consistently across multiple EWF articles.

Source: [S&P 500 ETF SPY Elliott Wave Trading Setup Explained](https://elliottwave-forecast.com/stock-market/sp-500-etf-spy-elliott-wave-setup/)

---

**B3. Stop loss — beyond 161.8% extension (outer Blue Box boundary)**  
The stop loss is placed **below the 161.8% Fibonacci extension** (the outer / far
boundary of the Blue Box). In a bullish setup:
`stop = B_price - (1.618 × |A_price - O_price|)`
This is the structural invalidation level: if C or Y extends beyond 161.8% of A
or W, the correction is no longer corrective — it has become an impulse in the
opposite direction and the prior trend thesis is invalid.

> "Breaking below the 1.618 Fibonacci extension level would invalidate the trade."

Source: [BlueBox Wins: What is a BlueBox Win?](https://elliottwave-forecast.com/bluebox-wins/blue-box-wins-explained/)

---

**B4. Risk-free trigger — move stop to breakeven at 50% of connector**  
After entering in the Blue Box, the first management milestone is when price
bounces back 50% of the *connector wave* (Wave X in a WXY, or Wave B in an ABC —
the corrective rally within the structure). At this point:
- Take **partial profits** on a portion of the position.
- Move stop on the remaining position to **breakeven** (= the original entry price).

> "Once price reaches the 50% Fibonacci retracement against the red X connector,
> positions are made risk-free and partial profits are booked."

The position now carries zero capital risk. The remaining portion is held for the
larger target.

Sources:
- [S&P 500 ETF SPY Elliott Wave Trading Setup Explained](https://elliottwave-forecast.com/stock-market/sp-500-etf-spy-elliott-wave-setup/)
- [AMD Delivers 25%+ Rally Off Our Blue Box Entry](https://elliottwave-forecast.com/stock-market/amd-delivers-25-rally-off-our-blue-box-entry/)

---

**B5. Primary target — previous swing high / start of the correction**  
The minimum expected reaction from a Blue Box reaction is **3 waves back toward
the origin of the correction** (point O, the high that started the corrective
pullback). EWF states that in a Bullish Sequence, the Blue Box should produce "at
least a 3-wave bounce" back toward the previous high or a new high. The first
structural target is the high immediately preceding the corrective move.

Source: [BlueBox Wins: What is a BlueBox Win?](https://elliottwave-forecast.com/bluebox-wins/blue-box-wins-explained/)

---

**B6. Extended targets — next motive wave projections**  
If the Blue Box reaction is part of an ongoing impulsive sequence (e.g., the
correction is wave 4 of an impulse, and the Blue Box entry catches the wave 5
launch), the subsequent targets are:
- **Wave 5 = Wave 1** (equal legs) — first target
- **Wave 5 at 61.8% of combined Wave 1+3** (measured from Wave 4 low) — alternative
- **1.236–1.618× extension of Wave 4's range, measured from Wave 3 high** — extended

> "One way to forecast a fifth wave target with Elliott Wave is from the 61.8%
> extension area of the first & third waves combined measured against the high of
> the fourth wave."

For a Wave 3 launch (Blue Box at Wave 2):
- First target: 161.8% × Wave 1 (typical Wave 3)
- Extended: 261.8% × Wave 1 (strong Wave 3)

Sources:
- [Fifth Wave Trading: Elliott Wave Target Strategies That Work](https://elliottwave-forecast.com/elliottwave/elliott-wave-fifth-wave-target/)
- [Elliott Wave Theory – Most Powerful Move: Wave 3/C](https://elliottwave-forecast.com/elliottwave/elliott-wave-powerful-move-wave3/)

---

**B7. Timeframe guidance — avoid intraday; use 4H/Daily/Weekly**  
EWF explicitly states:

> "Elliott Wave theory is extremely hard to use for intraday trades, and much
> better accuracy is found by changing trades from 1–3 days to 5–60 days."

Preferred analysis and entry timeframes: 4H, Daily, Weekly. Top-down order:
Weekly sets the Right Side → Daily confirms the sequence count → 4H or 1H used
for Blue Box entry timing.

Source: [How to Trade Forex with Elliott Wave: The Complete Guide](https://elliottwave-forecast.com/elliottwave/how-to-trade-forex-with-elliott-wave/)

---

**B8. "Black stamp" — no trade, no Blue Box**  
When the Right Side tag is Black (unclear/choppy), EWF publishes no Blue Box and
no trade signal. Choppy/sideways structures do not fit the corrective sequence
framework and carrying positions into them degrades expected value.

Source: [Trading Elliott Wave Charts with the Right Side Tag and Blue Boxes](https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/)

---

**B9. Maximum position addition rule (scaling in)**  
EWF does not explicitly publish a scale-in protocol. However, their risk management
framework (2% max risk per trade, stop below 161.8%) implies that adding to a
position before the stop-to-breakeven trigger (rule B4) would increase capital at
risk beyond 2%. In practice, their examples show single-entry trades at the Blue
Box top (100% level) with no mention of scaling in within the box before the
risk-free trigger is reached.

---

### Part C — Next-Wave Projection Rules

**C1. "At least 3 waves from the Blue Box" — the minimum forecast**  
After a Blue Box reaction, EWF's minimum forecast is a **3-wave bounce** (or
decline, for a bearish box) back toward the origin of the corrective move. This
3-wave minimum is the basis for the "Blue Box win" claim — even if the bounce
stalls before the prior high, a 3-wave reaction is sufficient to produce a
profitable trade (given the B4 partial profit at 50% of connector).

> "Traders need to decide the exact level to buy, but we present the area where
> we believe the pair has a high chance of at least turning higher in 3 waves."

Source: [EURUSD Trading Setup Explained: Buying the Dip at the Blue Box Zone](https://elliottwave-forecast.com/forex/eurusd-trading-setup-buying-blue-box-2/)

---

**C2. Next-wave direction = Right Side direction (always)**  
The direction of the next wave from a Blue Box is always in the direction of the
Right Side stamp. There is no "counter-trend Blue Box" in EWF's published
framework. If the Right Side is Green (bullish), the next expected move is upward.
The Blue Box defines *where* to catch the turn; the Right Side defines *which way*
to trade from that turn.

Source: [Trading Elliott Wave Charts with the Right Side Tag and Blue Boxes](https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/)

---

**C3. Completed corrective sequence → motive continuation**  
When the corrective swing count reaches exactly 3, 7, or 11 AND price is in the
Blue Box (100%–161.8% extension zone), the forecast is that the prior trend will
resume. The motive continuation is labeled as the next impulsive sequence:
- If the correction was a Wave 2 pullback → next move is Wave 3 (strongest,
  targets 161.8%+ of Wave 1 from Wave 2's low).
- If the correction was a Wave 4 → next move is Wave 5 (moderating momentum,
  targets equal to Wave 1 or 61.8% of Wave 1+3).
- If the correction was a Wave B / Wave X → next move is Wave C / Wave Y of the
  same corrective structure (counter-trend continuation, not a new trend move).

Source: [Elliott Wave Structures & Swing Sequence](https://elliottwave-forecast.com/elliott-wave-structures-and-swing-sequence/)

---

**C4. Incomplete motive sequence → buy the next corrective dip (extension forecast)**  
If the motive swing count is at 5 (and internal structure confirms the 5 swings
are impulsive), the forecast is that the trend will extend to 9 swings. After a
3-swing corrective pullback (from the 5th swing top), EWF enters long for the
expected 7th swing up (which, with a subsequent 8th-swing pullback and 9th-swing
top, completes the 9-count). The "incomplete motive sequence" is itself a
next-wave prediction: direction = same as prior trend, with one more motive leg
to come.

Source: [Trading Edge through Swings Sequences](https://elliottwave-forecast.com/elliottwave/trading-edge-through-swing-sequences/)

---

**C5. After 13-swing / 9-swing motive completion → forecast a larger correction**  
When an impulsive sequence completes at 9 or 13 swings (all motive sequence
numbers have been consumed), EWF no longer buys dips in the prior trend
direction — the Right Side stamp is reassessed and may switch from Green to Black
or Red. The forecast becomes: "a larger-degree correction is now expected" (a
3-, 7-, or 11-swing counter-trend move, with the first Blue Box appearing in the
opposite direction). This is the "calling the right side" transition — from buying
dips to selling rallies (or standing aside until the new Right Side is clear).

Source: [The Right Side in Elliott Wave](https://elliottwave-forecast.com/elliottwave/right-side-elliott-wave/)

---

**C6. RSI confirmation of the next-wave direction**  
After a Blue Box reaction, if price makes a new high (in the trend direction) AND
RSI also makes a new high (no divergence yet), this confirms the move is in a Wave
3 or early in the motive continuation — the trend is strong and has further to go.
If price makes a new high but RSI makes a *lower* high (divergence), the move is
likely in a Wave 5 / near completion — reduce position size on new entries and
look for the next corrective setup to form.

Source: [How Momentum Indicator (RSI) is Used with Elliott Wave](https://elliottwave-forecast.com/elliottwave/how-momentum-indicator-is-used-with-elliott-wave/)

---

**C7. Invalidation → Right Side flip**  
If price closes beyond the outer Blue Box boundary (the 161.8% level), the setup
is invalidated AND the Right Side is reassessed. A confirmed break of the 161.8%
extension signals the correction has become an impulse in the opposite direction.
EWF will then:
1. Exit the invalidated trade (stop triggered at 161.8%).
2. Reassess the wave count from the last clear structural anchor.
3. If the new count shows an impulsive sequence in the opposite direction, the
   Right Side may flip (Green → Red or vice versa).
4. Wait for the new sequence to either complete (3, 7, 11 swings) or show an
   incomplete count requiring an extension — then redraw the Blue Box in the new
   direction if applicable.

Sources:
- [Silver Elliott Wave View: Bearish Sequence and Invalidation](https://elliottwave-forecast.com/news/silver-elliott-wave-view-bearish-sequence-invalidation/)
- [Trading Elliott Wave Charts with the Right Side Tag and Blue Boxes](https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/)

---

**C8. Running / expanded corrective variants and their forecast implications**

*Running Flat:* Wave C ends without reaching Wave A's extreme. Signal: the
underlying trend is extremely strong. Forecast: the trend will resume with unusual
velocity (the "failed correction" consumed less price depth, leaving more energy
in the trend). The Blue Box in a running flat is narrower — Wave C's 100%
extension of A will be shallower, so the box sits closer to the Wave B high.

*Expanded Flat:* Wave B exceeds Wave A's origin; Wave C extends beyond Wave A's
extreme but still stays within the 100%–161.8% extension. Standard Blue Box
applies. The extra extension in Wave B (and hence Wave C) means the box sits
further away from current price than a regular flat — deeper retracement but
still structurally bounded.

*Running Triangle as Wave B or Wave X:* Wave B makes a new extreme above the
triangle's origin (looks like a new impulse breakout). EWF warns this is the most
common misidentification trap. If the subsequent legs (C, D, E) converge rather
than diverge, it is a running triangle — the post-triangle thrust is the next
wave in the dominant direction. Forecast: thrust equals the widest portion of the
triangle, projected from Wave E.

Sources:
- [Three Types of Elliott Wave Flat Corrections](https://elliottwave-forecast.com/elliottwave/three-types-of-elliott-wave-flats-2/)
- [Running Triangle and how they are different to regular Triangles](https://elliottwave-forecast.com/elliottwave/running-triangle-and-how-they-are-different-to-regular-triangles/)

---

## 4. Summary of the Complete EWF Trade Checklist

The following is a condensed, ordered checklist assembling rules A1–A9, B1–B9,
and C1–C8 into a practical workflow:

```
PRE-TRADE SETUP (IDENTIFICATION)
 [ ] A1  Count swing sequence from last clear anchor: result in {3,7,11}? → corrective
 [ ] A2  Right Side tag on this timeframe + one TF higher: both Green (long) or Red (short)?
 [ ] A3  Confirm current move is corrective, not a new motive sequence in opposite direction
 [ ] A5  Check internal sub-wave count of first corrective leg: 3 sub-waves → WXY (preferred)
 [ ] A4  Compute Blue Box: lower = 100% ext, upper = 161.8% ext of first corrective leg
 [ ] A8  Check if final corrective leg shows RSI divergence (positive confirmation, not required)

ENTRY
 [ ] B1  Wait for price to TOUCH the 100% extension level (do not pre-enter)
 [ ] B2  Compute position size: risk ≤ 2% of capital; stop = below 161.8% extension

STOP LOSS
 [ ] B3  Place stop beyond 161.8% extension (structural invalidation)

TRADE MANAGEMENT AFTER ENTRY
 [ ] B4  At 50% retracement of connector (X or B wave): take partial profit, move stop to BE
 [ ] B5  First target: previous swing high (origin of the correction)
 [ ] B6  Extended target: 161.8% × wave 1 from wave 2 low (if entering at wave 2), or
              61.8% of wave 1+3 from wave 4 low (if entering at wave 4), or
              previous high + next motive wave projection

NEXT-WAVE PREDICTION
 [ ] C2  Direction = Right Side stamp direction (no counter-trend Blue Box entries)
 [ ] C3  Corrective count complete (3/7/11) → forecast motive continuation
 [ ] C4  Motive count incomplete at 5/9 → forecast extension; buy next corrective dip
 [ ] C5  Motive count complete (9/13) → reassess Right Side; may flip direction
 [ ] C6  RSI at new extreme with NO divergence → Wave 3 still running, more upside
         RSI divergence → Wave 5 near end, reduce new long entries
 [ ] C7  Invalidation (close beyond 161.8%) → stop out, reassess Right Side, redraw

```

---

## 5. Gap Analysis — What Our Engine Needs to Build or Change

The Ewace_2026 engine (`wavelib/`) currently implements: ZigZag pivot detection
(`toolkit.py`), wave validation (rules.py), confluence scoring (`confluence.py`),
auto-labeling (`automation.py`), and a causal backtest harness (`backtest.py`).

The prior research docs (`10_ewf_method_tools.md §3`) mapped EWF concepts to
implementation layers. Below is an updated, more granular gap assessment
specifically from the trading/prediction rules above:

### 5.1 Gaps that require NEW code

| Gap | Rule | Location | Priority |
|---|---|---|---|
| **Blue Box zone computation** | A4, B3, B4 | `toolkit.py`: add `blue_box_zone(O, A, B)` | HIGH |
| **Swing sequence counter** | A1, A6, A7, C3–C5 | `automation.py`: `count_swing_sequence(pivots)` returning count + {impulsive, corrective, incomplete} | HIGH |
| **Right Side directional bias** | A2, C2, C5 | `automation.py`: `directional_bias(wave_count, degree_hierarchy)` returning {bullish, bearish, unclear} | HIGH |
| **Connector 50% retracement trigger** | B4 | `toolkit.py`: given entry + connector wave, compute risk-free trigger level | MEDIUM |
| **Incomplete-5-swing warning** | A7 | `automation.py`: flag corrective swings at count=5 as "incomplete, expect extension" | MEDIUM |
| **Wave-label-specific RSI divergence** | A8, C6 | `confluence.py`: make existing RSI divergence strand wave-label-aware (check divergence at labeled W5 vs W3, not arbitrary swings) | MEDIUM |
| **WXY vs ABC discriminator gate** | A5 | `rules.py`: surface `"first_leg_internal=3 → WXY (preferred)" vs "first_leg_internal=5 → ABC (ambiguous)"` in RuleResult.detail | LOW |

### 5.2 Gaps that require MODIFYING existing code

| Gap | Rule | Location | Notes |
|---|---|---|---|
| **Equal Legs as named output** | A4, B5 | `toolkit.py`: rename / surface 100% extension as `equal_legs_level` in Fibonacci output | trivial |
| **WXY Fibonacci validation bounds** | A5 | `rules.py` double-three validator: validate Y ends within 100%–161.8% of W (not just vague "corrective extent") | existing validator needs tighter bounds |
| **X wave retracement check** | (A5 context) | `rules.py` WXY validator: enforce X retraces 50%–85.4% of W | add numeric check |
| **Running flat detection** | C8 | `rules.py` flat validator: add `is_running_flat` flag when C does not reach A's extreme | currently surface as WARN |
| **Running triangle detection** | C8, A3 | `rules.py` triangle validator: add `is_running_triangle` flag when B exceeds triangle origin | add flag |

### 5.3 Gaps that require DESIGN DECISIONS (not just code)

1. **Pivot quality vs Blue Box accuracy.** The Blue Box is only as good as the
   ZigZag pivot detector that identifies swings O, A, B. Our current ZigZag uses
   a parameterized threshold. A poorly calibrated threshold will misidentify
   swing anchors, producing Blue Boxes at wrong levels. Any implementation must
   expose the pivot threshold as a validated parameter, not a hardcoded constant.

2. **Degree selection for swing count.** Swing-sequence counting is degree-
   sensitive: a 7-swing WXY at the 4H degree may be a single swing at the daily
   degree. The engine needs to count at the *trading degree* (typically the degree
   at which the Right Side stamp is applied). This requires the multi-scale
   `label_and_validate()` output to carry an explicit degree annotation before
   swing counting is run.

3. **Right Side persistence and flip logic.** Implementing the Right Side flip
   (C7: 161.8% break → reassess) requires a stateful observer across bars, not
   just a single-bar computation. This is a new stateful component distinct from
   the existing per-structure validators.

4. **"3 pushes" and "three RSI divergences" granularity.** EWF's rule that each
   impulsive sub-division must carry internal RSI divergence (3 divergences in a
   5-wave impulse) requires accessing the sub-wave structure at one degree below
   the trading degree. Our `automation.py` does multi-scale labeling but does not
   yet pass sub-wave detail to `confluence.py`. A new data path from the sub-wave
   count to the RSI divergence scorer is needed.

5. **Corrective-ends-without-divergence gate.** This is the inverse of rule A8.
   Currently `confluence.py` treats RSI divergence as a positive signal at any
   swing. For EWF compliance, the gate needs to be context-aware: divergence at
   a corrective terminal is positive; absence of divergence at an impulsive
   terminal (Wave 5) is negative (should demote confidence of impulse completion).

### 5.4 Genuinely proprietary gaps (cannot replicate from public information)

- **Proprietary pivot system (RSI + CCI + Stochastic RSI cycle-end detector):**
  The exact algorithm is not published. Partial substitute: use our existing
  `confluence.py` momentum strands as a proxy.
- **Distribution system:** Not publicly specified. No implementation path.
- **Market correlation / currency ranking:** Qualitatively described; no
  quantitative specification available publicly.
- **85% Blue Box success rate:** No methodology for this statistic is public.
  Our own backtest harness (`wavelib/backtest.py`) should be used to measure
  actual hit rate of the `blue_box_zone()` function on historical AVGO/MRVL data
  before any claims are made about expected win rate.

---

## 6. "React, Don't Predict" — Practical Stance

The phrase "react, don't predict" is EWF's core epistemological claim. In practice
it means:

- The Blue Box is drawn *in advance* based on the corrective count and Fibonacci
  extensions — this is the prediction layer (stating WHERE the correction should
  end).
- Whether price actually enters the Blue Box is not predicted — it may or may not.
- The trade is only triggered if/when price enters the box — this is the react
  layer.
- If price never enters the box (correction ends shallower), no trade is taken.
- If price passes through the box without reacting (161.8% breach), the count is
  wrong and the trade is stopped out (or not entered if the breach happens without
  a touch first).

This is mechanically equivalent to a limit-order-at-a-computed-level approach:
compute the level, post a limit, manage the trade if filled, move on if not.

For our engine: the `blue_box_zone()` output functions as a zone-of-interest flag
in the confluence scorer — `price_in_blue_box = True/False` — not as a fill
trigger. The actual execution layer is out of scope for Ewace_2026.

---

## 7. Sources (Complete)

All URLs are confirmed as indexed public pages on elliottwave-forecast.com or
syndicated third-party content. Direct WebFetch returned HTTP 403 for all EWF
URLs; content derived from Google-indexed snippets, search-result excerpts, and
third-party republication.

- [Trading Elliott Wave Charts with the Right Side Tag and Blue Boxes](https://elliottwave-forecast.com/elliottwave/trading-elliott-wave-chart-right-side-tag/)
- [BlueBox Wins: What is a BlueBox Win?](https://elliottwave-forecast.com/bluebox-wins/blue-box-wins-explained/)
- [The Right Side: Only Way to Survive in the Trading World](https://elliottwave-forecast.com/trading/right-side-helps-survival-trading-world/)
- [Trading Edge through Swings Sequences](https://elliottwave-forecast.com/elliottwave/trading-edge-through-swing-sequences/)
- [Elliott Wave Structures & Swing Sequence](https://elliottwave-forecast.com/elliott-wave-structures-and-swing-sequence/)
- [Trading Right Side using Elliott Wave Theory, Cycles and Sequences](https://elliottwave-forecast.com/trading-right-side-using-elliott-wave-theory-cycles-and-sequences/)
- [Why Double Three WXY is A Better Structure to Trade Than Zigzag ABC](https://elliottwave-forecast.com/elliottwave/why-double-three-wxy-is-a-better-structure-to-trade-than-zigzag-abc/)
- [ABC and WXY: difference between both structure](https://elliottwave-forecast.com/elliottwave/difference-wxy-abc-structure/)
- [WXY and ABC Elliott Wave Structure: Key Differences](https://elliottwave-forecast.com/video-blog/wxy-elliottwave-structure/)
- [Equal Legs: What does it mean?](https://elliottwave-forecast.com/elliottwave/equal-legs/)
- [Did you know what the meaning of term Equal Legs is?](https://elliottwave-forecast.com/elliottwave/equal-legs-elliotts-wave-theory/)
- [S&P 500 E-Mini (ES_F) Elliott Wave: Blue Box Buy Setup Explained](https://elliottwave-forecast.com/stock-market/sp-500-e-mini-es_f-elliott-wave-blue-box/)
- [How Momentum Indicator (RSI) is Used with Elliott Wave](https://elliottwave-forecast.com/elliottwave/how-momentum-indicator-is-used-with-elliott-wave/)
- [Elliott Wave Analysis with MACD, RSI and Fibonacci Divergence](https://elliottwave-forecast.com/trading/elliott-wave-divergence-macd-rsi-fibonacci/)
- [Using RSI to Identify Elliott Waves](https://elliottwave-forecast.com/trading/using-relative-strength-index-identify-elliott-waves/)
- [S&P 500 ETF SPY Elliott Wave Trading Setup Explained](https://elliottwave-forecast.com/stock-market/sp-500-etf-spy-elliott-wave-setup/)
- [AMD Delivers 25%+ Rally Off Our Blue Box Entry](https://elliottwave-forecast.com/stock-market/amd-delivers-25-rally-off-our-blue-box-entry/)
- [How to Trade Forex with Elliott Wave: The Complete Guide](https://elliottwave-forecast.com/elliottwave/how-to-trade-forex-with-elliott-wave/)
- [Fifth Wave Trading: Elliott Wave Target Strategies That Work](https://elliottwave-forecast.com/elliottwave/elliott-wave-fifth-wave-target/)
- [Elliott Wave Theory – Most Powerful Move: Wave 3/C](https://elliottwave-forecast.com/elliottwave/elliott-wave-powerful-move-wave3/)
- [EURUSD Trading Setup Explained: Buying the Dip at the Blue Box Zone](https://elliottwave-forecast.com/forex/eurusd-trading-setup-buying-blue-box-2/)
- [Silver Elliott Wave View: Bearish Sequence and Invalidation](https://elliottwave-forecast.com/news/silver-elliott-wave-view-bearish-sequence-invalidation/)
- [Three Types of Elliott Wave Flat Corrections](https://elliottwave-forecast.com/elliottwave/three-types-of-elliott-wave-flats-2/)
- [Running Triangle and how they are different to regular Triangles](https://elliottwave-forecast.com/elliottwave/running-triangle-and-how-they-are-different-to-regular-triangles/)
- [Elliott Wave Theory 2.0: Market Correlation secrets for better Forecasting](https://elliottwave-forecast.com/elliottwave/new-elliott-wave-theory-market-correlation-and-rsi-in-elliott-wave/)
- [Using Market Correlation and RSI in the new EWF theory](https://elliottwave-forecast.com/elliottwave/the-new-elliott-wave-theory-using-market-correlation-and-rsi-in-elliott-wave/)
- [The Right Side in Elliott Wave](https://elliottwave-forecast.com/elliottwave/right-side-elliott-wave/)
- [CHF/JPY posts perfect rally from Elliott Wave blue box area - FXStreet](https://www.fxstreet.com/analysis/chf-jpy-posts-perfect-rally-from-elliott-wave-blue-box-area-202510311217)
- [Elliottwave-Forecast.com Official Thread - Forex Factory](https://www.forexfactory.com/thread/528784-elliottwave-forecastcom-official-thread-w-analysis-blogs)

---

*Document generated 2026-06-12. Source: 20+ targeted web searches against
`elliottwave-forecast.com` public content plus third-party syndication.
Direct page access blocked (HTTP 403). Members-only video library inaccessible.
No commitment from Ewace_2026 to implement any EWF concept without passing
the engine's own validation gates (backtest hit rate, causal compliance,
separation-of-concerns architecture).*
