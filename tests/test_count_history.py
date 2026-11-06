"""Tests for wavelib/count_history.py — causal replay of the held count."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.avgo import DAILY                                   # noqa: E402
from wavelib.count_history import (count_history, history_markdown,  # noqa: E402
                                   render_count_history_page, _transition, CountSegment)

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
