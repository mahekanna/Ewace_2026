"""Tests for wavelib/count_history.py — causal replay of the held count."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.avgo import DAILY                                   # noqa: E402
from wavelib.count_history import (count_history, history_markdown,  # noqa: E402
                                   render_count_history_page, _transition, CountSegment,
                                   grade_forecasts, forecast_scorecard, scorecard_markdown,
                                   ledger_markdown)

BARS = DAILY[-320:]                                           # small, fast replay


class Replay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = count_history(BARS, symbol="AVGO", window=200, stride=5, min_history=60)

    def test_steps_cover_history_and_end_on_last_bar(self):
        idx = [s.i for s in self.h.snapshots]
        self.assertEqual(idx[0], 60)
        self.assertEqual(idx[-1], len(BARS))
        self.assertEqual(idx, sorted(set(idx)))
        self.assertEqual(self.h.snapshots[-1].t, BARS[-1][0])
        self.assertEqual(self.h.snapshots[-1].close, BARS[-1][4])

    def test_causal_no_lookahead(self):
        """A snapshot at step i must be identical whether or not later bars exist."""
        s = self.h.snapshots[len(self.h.snapshots) // 2]
        h2 = count_history(BARS[:s.i], symbol="AVGO", window=200, stride=5, min_history=60)
        s2 = h2.snapshots[-1]
        self.assertEqual(s2.i, s.i)
        a1 = self.h.anchored[s.anchored].signature if s.anchored is not None else None
        a2 = h2.anchored[s2.anchored].signature if s2.anchored is not None else None
        self.assertEqual(a1, a2)
        r1 = self.h.recent[s.recent].signature if s.recent is not None else None
        r2 = h2.recent[s2.recent].signature if s2.recent is not None else None
        self.assertEqual(r1, r2)
        for seg in self.h.anchored + self.h.recent:
            for _lab, t0, _p0, t1, _p1 in seg.legs:
                self.assertLessEqual(t1, seg.end_t, "a leg can never end after the bar it was labelled on")
                self.assertLessEqual(t0, t1)

    def test_segments_are_contiguous_and_signature_changes(self):
        for segs in (self.h.anchored, self.h.recent):
            self.assertTrue(segs)
            self.assertEqual(sum(s.n_bars for s in segs), len(self.h.snapshots))
            for a, b in zip(segs, segs[1:]):
                self.assertLess(a.end_t, b.start_t)
                self.assertNotEqual(a.signature, b.signature)
            self.assertEqual(segs[0].transition, "START")
            self.assertTrue(all(s.transition in
                                {"START", "NEW", "LOST", "RELABEL", "EXTEND", "SHIFT"} for s in segs))

    def test_snapshot_refs_resolve(self):
        for s in self.h.snapshots:
            if s.anchored is not None:
                seg = self.h.anchored[s.anchored]
                self.assertTrue(seg.start_t <= s.t <= seg.end_t)
                self.assertNotEqual(seg.pattern, "NONE")
            if s.recent is not None:
                seg = self.h.recent[s.recent]
                self.assertTrue(seg.start_t <= s.t <= seg.end_t)
                self.assertIn(seg.pattern, {"IMPULSE", "CORRECTION", "DIAGONAL"})

    def test_markdown_and_page(self):
        md = history_markdown(self.h, "anchored")
        self.assertIn("| held from | to | bars | transition |", md)
        self.assertIn("segments; transitions:", md)
        html = render_count_history_page(self.h, desc="test")
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn('"window":200', html)
        self.assertIn('"snaps":[[60,', html)
        self.assertNotIn("__DATA__", html)


class Forecasts(unittest.TestCase):
    @staticmethod
    def _seg(**f):
        base = {"t": 0, "price": 100.0, "dir": "up", "next": "x", "pattern": "ZIGZAG",
                "targets": [["a", 110.0]], "t1": 110.0, "t_far": 120.0, "cluster": None,
                "inv": 90.0, "conf": 0.5, "anchor_t": 0, "anchor_p": 100.0, "leg_days": 10,
                "time_lo": 3.3, "time_hi": 30.0, "why": ""}
        base.update(f)
        return CountSegment("anchored", base["pattern"], 0, 0, 1, [], forecast=base)

    @staticmethod
    def _bars(path):
        """path: list of (day, high, low)."""
        return [(d * 86400, 0, h, l, (h + l) / 2, 1) for d, h, l in path]

    def test_hit_then_full(self):
        s = self._seg()
        grade_forecasts(self._bars([(1, 105, 95), (2, 111, 100), (3, 115, 105), (4, 121, 110)]), [s])
        self.assertEqual(s.forecast["outcome"], "HIT_FULL")
        self.assertEqual(s.forecast["bars_to_t1"], 2)
        self.assertEqual(s.forecast["resolved_t"], 4 * 86400)
        self.assertAlmostEqual(s.forecast["mfe"], 0.21)

    def test_invalidated_before_t1(self):
        s = self._seg()
        grade_forecasts(self._bars([(1, 105, 95), (2, 100, 89), (3, 130, 100)]), [s])
        self.assertEqual(s.forecast["outcome"], "INVALIDATED")
        self.assertEqual(s.forecast["resolved_t"], 2 * 86400)

    def test_hit_then_void_touch_is_still_hit(self):
        s = self._seg()
        grade_forecasts(self._bars([(1, 111, 100), (2, 100, 80)]), [s])
        self.assertEqual(s.forecast["outcome"], "HIT")

    def test_expired_and_open(self):
        s = self._seg()
        grade_forecasts(self._bars([(d, 105, 95) for d in range(1, 40)]), [s])
        self.assertEqual(s.forecast["outcome"], "EXPIRED")
        s2 = self._seg()
        grade_forecasts(self._bars([(d, 105, 95) for d in range(1, 5)]), [s2])
        self.assertEqual(s2.forecast["outcome"], "OPEN")

    def test_void_level_beyond_the_target_impulse_case(self):
        """Completed up-impulse -> expect a DOWN correction; the void level is the
        wave-1 origin BELOW the targets. It must not count as touched merely because
        price is above it."""
        s = self._seg(dir="down", t1=90.0, t_far=80.0, inv=50.0)
        grade_forecasts(self._bars([(1, 105, 95), (2, 100, 89), (3, 95, 79)]), [s])
        self.assertEqual(s.forecast["outcome"], "HIT_FULL")
        s2 = self._seg(dir="down", t1=90.0, t_far=80.0, inv=50.0)
        grade_forecasts(self._bars([(1, 105, 95), (2, 100, 49)]), [s2])
        self.assertEqual(s2.forecast["outcome"], "INVALIDATED")

    def test_down_direction(self):
        s = self._seg(dir="down", t1=90.0, t_far=80.0, inv=110.0)
        grade_forecasts(self._bars([(1, 105, 95), (2, 100, 89)]), [s])
        self.assertEqual(s.forecast["outcome"], "HIT")

    def test_scorecard(self):
        segs = [self._seg(), self._seg(), self._seg(pattern="IMPULSE"), CountSegment("anchored", "NONE", 0, 0, 1, [])]
        grade_forecasts(self._bars([(1, 111, 100), (2, 115, 112)]), segs)
        sc = forecast_scorecard(segs)
        self.assertEqual(sc["ALL"]["n"], 3)
        self.assertEqual(sc["ZIGZAG"]["n"], 2)
        self.assertEqual(sc["ALL"]["hit_rate"], 1.0)
        self.assertEqual(sc["ALL"]["median_bars_to_t1"], 1)

    def test_replay_carries_graded_forecasts(self):
        h = count_history(BARS, symbol="AVGO", window=200, stride=5, min_history=60)
        fs = [s.forecast for s in h.anchored if s.forecast]
        self.assertTrue(fs)
        for f in fs:
            self.assertIn(f["outcome"], {"HIT", "HIT_FULL", "INVALIDATED", "EXPIRED", "OPEN"})
            self.assertLessEqual(f["anchor_t"], f["t"], "projection anchor must be a visible pivot")
            if f["resolved_t"]:
                self.assertGreater(f["resolved_t"], f["t"], "outcome must come from LATER bars")
        self.assertIn("| from pattern |", scorecard_markdown(h))
        self.assertIn("forecast ledger", ledger_markdown(h))
        html = render_count_history_page(h)
        self.assertIn('"score":', html)


class Transitions(unittest.TestCase):
    def seg(self, pattern, origin_t, ends=(10,)):
        legs = [(str(k + 1), origin_t if k == 0 else ends[k - 1], 1.0, e, 2.0) for k, e in enumerate(ends)]
        return CountSegment("anchored", pattern, 0, 0, 1, legs)

    def test_rules(self):
        self.assertEqual(_transition(None, self.seg("IMPULSE", 1)), "START")
        self.assertEqual(_transition(self.seg("NONE", 1), self.seg("IMPULSE", 1)), "NEW")
        self.assertEqual(_transition(self.seg("IMPULSE", 1), CountSegment("anchored", "NONE", 0, 0, 1, [])), "LOST")
        self.assertEqual(_transition(self.seg("IMPULSE", 1), self.seg("ZIGZAG", 1)), "RELABEL")
        self.assertEqual(_transition(self.seg("IMPULSE", 1, (10,)), self.seg("IMPULSE", 1, (10, 20))), "EXTEND")
        self.assertEqual(_transition(self.seg("IMPULSE", 1), self.seg("IMPULSE", 5)), "SHIFT")


if __name__ == "__main__":
    unittest.main()
