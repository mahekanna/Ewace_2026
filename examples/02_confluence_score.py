"""
Example 02 — Reversal-confluence scoring on live data.
cd examples && python3 02_confluence_score.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wavelib import score_reversal, classify_swing_sequence
from data.avgo import FRESH_4H_VOL as AVGO
from data.mrvl import FRESH_4H_VOL as MRVL

# AVGO: testing the $358-410 (IV) zone for a BULLISH reversal
print(score_reversal("AVGO", AVGO, zone=(358, 410), bullish=True))
print("  swing off top:", classify_swing_sequence([495.0, 403.01, 426.45, 385.60]))

# MRVL: testing the $229-266 ((4)) zone for a BULLISH reversal
print(score_reversal("MRVL", MRVL, zone=(229, 266), bullish=True))
print("  swing off top:", classify_swing_sequence([324.16, 277.56, 321.46, 261.42]))

print("""
NOTE: feed 50+ bars for the RSI/divergence strand to activate (needs >14 bars).
A 7th strand (Hurst/FLD cycle window) is left as an external input — pass
cycle_aligned=True to score_reversal(...) when your cycle model confirms timing.
""")
