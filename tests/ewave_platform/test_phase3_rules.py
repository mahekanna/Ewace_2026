"""Phase 3 acceptance: rules split parity, patterns move, profiles loader."""
import json
import os
import unittest

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

import ewave.rules as R
from ewave.rules.profiles import Profile, get_profile, load_profiles
from ewave.rules.result import Pivot, Status, Wave

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CFG = os.path.join(REPO, "configs")


def _bars(symbol="avgo", tf="1d", n=500):
    with open(os.path.join(REPO, "data", "live", f"{symbol}_{tf}_2026-06.json")) as f:
        d = json.load(f)
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0)
            for b in d["bars"]][-n:]


class TestRulesSplitParity(unittest.TestCase):
    """The split modules must behave identically to the legacy monolith
    (which now shims them — identity, not just equality)."""

    def test_shim_identity(self):
        import wavelib.rules as WR
        for name in ("elliott_hard_rules", "classify_correction",
                     "similarity_and_balance", "label_monowaves",
                     "validate_impulse", "confirm_completion", "is_terminal"):
            self.assertIs(getattr(WR, name), getattr(R, name), name)

    def test_engine_on_real_candidates(self):
        from ewave.patterns.candidates import label_and_validate
        cands = label_and_validate(_bars())
        self.assertGreater(len(cands), 0)
        for c in cands:
            self.assertEqual(c.hard_fails,
                             sum(1 for r in c.results if r.status is Status.FAIL))

    def test_wavetree_shim_and_context(self):
        import wavelib.wavetree as WT
        from ewave.patterns import tree
        self.assertIs(WT.wave_counts, tree.wave_counts)
        ctx = tree.tree_context(_bars())
        self.assertIn("tree_confidence", ctx)
        self.assertIn("alternates", ctx)
        # D5: context only — a float summary + strings, nothing gate-like
        self.assertIsInstance(ctx["primary"], str)

    def test_tree_context_degrades_on_empty_data(self):
        from ewave.patterns.tree import tree_context
        ctx = tree_context([])
        self.assertIsNone(ctx["tree_confidence"])
        self.assertEqual(ctx["alternates"], [])


class TestProfiles(unittest.TestCase):
    def test_four_shipped_profiles_load(self):
        profs = load_profiles(CFG)
        self.assertEqual(set(profs), {"experimental", "sow_neowave_soft",
                                      "sow_neowave_strict", "classic_elliott"})
        for p in profs.values():
            self.assertIsInstance(p, Profile)

    def test_strict_encodes_ruleset_h(self):
        s = get_profile("sow_neowave_strict", CFG)
        self.assertTrue(s.require_pattern_id)      # W1 must be :5 motive
        self.assertEqual(s.min_confluence_strands, 3)  # Table D
        self.assertEqual(s.min_rr, 2.0)            # E-2
        self.assertEqual(s.retr_hi, 0.618)         # golden zone
        self.assertEqual(s.deep_hi, 0.764)
        self.assertEqual(s.sb_time_budget_w1_mult, 3)  # S&B, not fixed bars
        self.assertEqual(s.time_stop_bars, 0)

    def test_experimental_matches_crude_wave3_defaults(self):
        """The crude preset must mirror wavelib.wave3.wave3_signal's defaults
        (the +0.17..+0.44R configuration) exactly."""
        e = get_profile("experimental", CFG)
        kw = e.wave3_kwargs()
        self.assertEqual(kw["pct"], 0.02)
        self.assertEqual((kw["retr_lo"], kw["retr_hi"]), (0.382, 0.786))
        self.assertEqual(kw["min_w1_frac"], 0.01)
        self.assertEqual(kw["buf"], 0.001)
        self.assertTrue(kw["use_momentum"])
        self.assertFalse(kw["require_pattern_id"])
        self.assertEqual(kw["conf_min"], 0)
        self.assertEqual(kw["min_rr"], 0.0)

    def test_unknown_profile_and_unknown_knob_raise(self):
        from ewave.config import ConfigError
        with self.assertRaises(ConfigError):
            get_profile("nope", CFG)
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "profiles.json"), "w") as f:
                json.dump({"bad": {"not_a_knob": 1}}, f)
            with self.assertRaises(ConfigError):
                load_profiles(d)


class TestStatusUnknown(unittest.TestCase):
    def test_unknown_member_present_and_distinct(self):
        self.assertEqual(Status.UNKNOWN.value, "UNKNOWN")
        self.assertEqual(len({Status.PASS, Status.FAIL, Status.WARN,
                              Status.NA, Status.REF, Status.UNKNOWN}), 6)

    def test_report_verdict_unaffected_by_unknown(self):
        from ewave.rules import report
        from ewave.rules.result import RuleResult
        txt = report([RuleResult("x", Status.UNKNOWN, "insufficient data")], "t")
        self.assertIn("VALID", txt)  # UNKNOWN is not a hard FAIL


if __name__ == "__main__":
    unittest.main()
