"""
rules.engine — the aggregate validators + report renderer (moved verbatim
from wavelib/rules.py §G). A count is INVALID iff any hard-rule FAIL;
guidelines are WARN and never invalidate.
"""
from __future__ import annotations
from typing import Sequence

from .corrections import classify_complex_correction, classify_correction
from .diagonals import diagonal_rules, is_terminal
from .elliott import elliott_guidelines, elliott_hard_rules
from .neowave import retracement_logic, similarity_and_balance
from .result import RuleResult, Status, Wave

def validate_impulse(w: Sequence[Wave], diagonal: bool = False) -> list[RuleResult]:
    res = []
    if diagonal:
        res += diagonal_rules(w)
    else:
        res += elliott_hard_rules(w)
    res += elliott_guidelines(w)
    # NeoWave overlays
    if len(w) == 5:
        res.append(similarity_and_balance(w[1], w[3], context="wave2 vs wave4"))
        res.append(is_terminal(w))
    return res


def validate_correction(w: Sequence[Wave]) -> list[RuleResult]:
    res = [classify_correction(w)]
    if len(w) >= 2:
        res.append(retracement_logic(w[1].retr(w[0])))
    if len(w) == 3:
        res.append(similarity_and_balance(w[0], w[2], context="A vs C"))
    if len(w) == 5:
        for i in range(4):                                   # triangle adjacent legs
            res.append(similarity_and_balance(w[i], w[i + 1], context=f"leg{i+1} vs leg{i+2}"))
    if len(w) in (5, 7) or len(w) > 7:
        res.append(classify_complex_correction(w))
    return res


def report(results: list[RuleResult], title="") -> str:
    head = f"\n{'='*64}\n{title}\n{'='*64}" if title else ""
    body = "\n".join(str(x) for x in results)
    fails = sum(1 for x in results if x.status is Status.FAIL)
    verdict = "VALID (no hard-rule failures)" if fails == 0 else f"INVALID — {fails} hard failure(s)"
    return f"{head}\n{body}\n  -> {verdict}"
