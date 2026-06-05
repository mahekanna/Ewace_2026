"""
Example 03 — Full pipeline: raw OHLC -> ZigZag pivots -> waves -> validation.
cd examples && python3 03_zigzag_pipeline.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
from wavelib import zigzag, pivots_to_waves, validate_impulse, report
from data.avgo import FRESH_4H_VOL

# zigzag wants (t,o,h,l,c); FRESH_4H_VOL is (t,o,h,l,c,v) -> drop volume
bars = [(t, o, h, l, c) for (t, o, h, l, c, v) in FRESH_4H_VOL]
pivots = zigzag(bars, pct=0.045)

print("ZigZag pivots (4.5% reversal):")
for p in pivots:
    d = datetime.fromtimestamp(p.t, tz=timezone.utc).strftime("%Y-%m-%d")
    print(f"  {d}  {p.kind}  {p.price:.2f}")

# If we get 6 pivots (5 legs) we can validate as an impulse
if len(pivots) >= 6:
    waves = pivots_to_waves(pivots[-6:])
    print(report(validate_impulse(waves), "Last 5 legs validated as impulse"))
else:
    print(f"\n{len(pivots)} pivots -> not a clean 5-leg impulse; "
          "widen the window or adjust pct.")
