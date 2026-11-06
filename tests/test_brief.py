"""Tests for wavelib/brief.py — the plain-language read."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.avgo import DAILY                                               # noqa: E402
from wavelib.brief import (decision_brief, brief_markdown, brief_html,     # noqa: E402
                           glossary_html, glossary_markdown, _reliability_phrase)

STANCES = {"NO READ", "WAIT FOR CONFIRMATION", "CONFIRMED BIAS", "PLAYED OUT", "STAND ASIDE"}


class BriefOnRealBars(unittest.TestCase):
    def test_brief_is_complete_and_plain(self):
        b = decision_brief("AVGO", DAILY)
        self.assertIn(b.stance, STANCES)
        self.assertTrue(b.bottom_line.endswith(".") or b.bottom_line.endswith("!"))
        titles = [t for t, _ in b.sections]
        self.assertEqual(titles[0], "Where we are")
        self.assertEqual(titles[-1], "What to do")
        if b.stance != "NO READ":
            self.assertIn("What confirms it / what kills it", titles)
            lv = b.levels
            self.assertTrue(lv["trigger"] > 0 and lv["void"] > 0 and lv["stop"] > 0)
            self.assertIn(b.direction, ("up", "down"))
            self.assertRegex(lv["deadline"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertIn("$", b.bottom_line)

    def test_no_read_on_flat_series(self):
        flat = [(1_700_000_000 + i * 86400, 100, 100.5, 99.5, 100, 1) for i in range(120)]
        b = decision_brief("X", flat)
        self.assertEqual(b.stance, "NO READ")
        self.assertIn("Nothing to act on", b.bottom_line)

    def test_reliability_uses_scorecard(self):
        sc = {"IMPULSE": {"n": 10, "decided": 10, "HIT": 6, "HIT_FULL": 1, "INVALIDATED": 3,
                          "EXPIRED": 0, "OPEN": 0, "hit_rate": 0.7, "full_rate": 0.1,
                          "inval_rate": 0.3, "median_bars_to_t1": 12}}
        b = decision_brief("AVGO", DAILY, scorecard=sc)
        sec = dict(b.sections).get("How reliable is this kind of call")
        if b.pattern == "IMPULSE":
            self.assertIn("70%", sec[0])
        else:
            self.assertIn("no track record", sec[0].lower())

    def test_markdown_and_html(self):
        b = decision_brief("AVGO", DAILY)
        md = brief_markdown(b)
        self.assertIn("**Stance:", md)
        self.assertIn("**What to do**", md)
        html = brief_html(b)
        self.assertIn("class='card brief'", html)
        self.assertIn(b.stance, html)
        self.assertIn("Void (invalidation)", glossary_html())
        self.assertIn("### Glossary", glossary_markdown())


class ReliabilityPhrase(unittest.TestCase):
    def test_tiers(self):
        self.assertIn("no track record", _reliability_phrase(None))
        row = {"decided": 30, "hit_rate": 0.6, "HIT": 15, "HIT_FULL": 3, "inval_rate": 0.3,
               "median_bars_to_t1": 9, "pattern": "IMPULSE"}
        self.assertIn("decent", _reliability_phrase(row))
        row.update(hit_rate=0.4)
        self.assertIn("coin flip", _reliability_phrase(row))
        row.update(hit_rate=0.2)
        self.assertIn("weak", _reliability_phrase(row))


if __name__ == "__main__":
    unittest.main()
