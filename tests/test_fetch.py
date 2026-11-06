"""
Tests for data/fetch.py — the stdlib half only (loading, resampling, fixture
formatting). No network: the yfinance-backed fetch is exercised manually via
`python3 data/fetch.py`.
"""
import ast
import datetime as dt
import json
import os
import sys
import tempfile
import unittest
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import fetch  # noqa: E402

NY = ZoneInfo("America/New_York")


def _t(y, m, d, hh=0, mm=0):
    return int(dt.datetime(y, m, d, hh, mm, tzinfo=NY).timestamp())


def _hourly_session(y, m, d, base=100.0):
    """Seven 1h bars 09:30..15:30 ET: o,h,l,c = base+k, base+k+2, base+k-1, base+k+1; v=10."""
    out = []
    for k in range(7):
        t = _t(y, m, d, 9, 30) + k * 3600
        out.append((t, base + k, base + k + 2, base + k - 1, base + k + 1, 10))
    return out


class Resample4h(unittest.TestCase):
    def test_two_session_aligned_buckets_per_day(self):
        h1 = _hourly_session(2026, 11, 3) + _hourly_session(2026, 11, 4, base=200.0)
        h4 = fetch.resample_4h(h1)
        self.assertEqual(len(h4), 4)
        stamps = [dt.datetime.fromtimestamp(b[0], NY).strftime("%d %H:%M") for b in h4]
        self.assertEqual(stamps, ["03 09:30", "03 13:30", "04 09:30", "04 13:30"])
        # first bucket = bars k=0..3 (09:30,10:30,11:30,12:30)
        t, o, h, l, c, v = h4[0]
        self.assertEqual((o, h, l, c, v), (100.0, 105.0, 99.0, 104.0, 40))
        # second bucket = bars k=4..6 (13:30,14:30,15:30)
        t, o, h, l, c, v = h4[1]
        self.assertEqual((o, h, l, c, v), (104.0, 108.0, 103.0, 107.0, 30))

    def test_preserves_order_and_tuple_shape(self):
        h4 = fetch.resample_4h(_hourly_session(2026, 11, 3))
        self.assertTrue(all(len(b) == 6 for b in h4))
        self.assertEqual([b[0] for b in h4], sorted(b[0] for b in h4))


class ResampleWeekly(unittest.TestCase):
    def test_monday_stamp_and_aggregation(self):
        # Mon 2026-10-26 .. Fri 2026-10-30, then Mon 2026-11-02 .. Thu 2026-11-05
        days = [(2026, 10, 26), (2026, 10, 27), (2026, 10, 28), (2026, 10, 29), (2026, 10, 30),
                (2026, 11, 2), (2026, 11, 3), (2026, 11, 4), (2026, 11, 5)]
        d1 = [(_t(*d), 10.0 + i, 12.0 + i, 9.0 + i, 11.0 + i, 1) for i, d in enumerate(days)]
        w = fetch.resample_weekly(d1)
        self.assertEqual(len(w), 2)
        self.assertEqual([dt.datetime.fromtimestamp(b[0], NY).strftime("%a %Y-%m-%d") for b in w],
                         ["Mon 2026-10-26", "Mon 2026-11-02"])
        t, o, h, l, c, v = w[0]
        self.assertEqual((o, h, l, c, v), (10.0, 16.0, 9.0, 15.0, 5))
        t, o, h, l, c, v = w[1]
        self.assertEqual((o, h, l, c, v), (15.0, 20.0, 14.0, 19.0, 4))

    def test_thursday_anchored_input_still_yields_monday_weeks(self):
        """A Thu-Wed source alignment (Yahoo's MRVL weekly) must not leak through."""
        days = [(2026, 10, 29), (2026, 10, 30), (2026, 11, 2), (2026, 11, 3), (2026, 11, 4)]
        d1 = [(_t(*d), 1.0, 2.0, 0.5, 1.5, 1) for d in days]
        w = fetch.resample_weekly(d1)
        self.assertEqual([dt.datetime.fromtimestamp(b[0], NY).weekday() for b in w], [0, 0])
        self.assertEqual([b[5] for b in w], [2, 3])


class SnapshotLoading(unittest.TestCase):
    def setUp(self):
        self._live = fetch.LIVE
        self.tmp = tempfile.TemporaryDirectory()
        fetch.LIVE = self.tmp.name
        bars = [{"t": 2, "o": 1, "h": 2, "l": 0.5, "c": 1.5, "v": 7},
                {"t": 1, "o": 1, "h": 2, "l": 0.5, "c": 1.5}]           # unsorted, one missing v
        for tag in ("2026-06", "2026-11"):
            with open(os.path.join(self.tmp.name, f"avgo_1d_{tag}.json"), "w") as fh:
                json.dump({"symbol": "YF:AVGO", "interval": "1d", "asof": tag, "bars": bars}, fh)
        # a variant file that must NOT be treated as a tag
        with open(os.path.join(self.tmp.name, "avgo_1d_eh_2026-06.json"), "w") as fh:
            json.dump({"bars": []}, fh)

    def tearDown(self):
        fetch.LIVE = self._live
        self.tmp.cleanup()

    def test_available_and_latest_tag(self):
        self.assertEqual(fetch.available_tags("NASDAQ:AVGO", "1d"), ["2026-06", "2026-11"])
        self.assertEqual(fetch.latest_tag("avgo", "1d"), "2026-11")
        self.assertIsNone(fetch.latest_tag("avgo", "1w"))

    def test_load_bars_sorted_tuples_and_meta(self):
        bars, meta = fetch.load_bars("AVGO", "1d", with_meta=True)
        self.assertEqual(bars, [(1, 1, 2, 0.5, 1.5, 0), (2, 1, 2, 0.5, 1.5, 7)])
        self.assertEqual(meta["tag"], "2026-11")
        self.assertEqual(meta["n"], 2)
        self.assertEqual(fetch.load_bars("AVGO", "1d", tag="2026-06")[0][0], 1)

    def test_missing_snapshot_errors(self):
        with self.assertRaises(FileNotFoundError):
            fetch.load_bars("MRVL", "1d")
        with self.assertRaises(FileNotFoundError):
            fetch.load_bars("AVGO", "1d", tag="1999-01")
        with self.assertRaises(ValueError):
            fetch.load_bars("AVGO", "2h")

    def test_write_snapshot_roundtrip(self):
        bars = [(10, 1.0, 2.0, 0.5, 1.5, 3), (20, 1.5, 2.5, 1.0, 2.0, 4)]
        p = fetch.write_snapshot("MRVL", "4h", bars, tag="2026-11")
        self.assertEqual(os.path.basename(p), "mrvl_4h_2026-11.json")
        self.assertEqual(fetch.load_bars("MRVL", "4h"), bars)
        with open(p) as fh:
            d = json.load(fh)
        self.assertEqual(d["symbol"], "YF:MRVL")
        self.assertEqual(d["interval"], "4h")
        self.assertEqual(set(d["bars"][0]), {"t", "o", "h", "l", "c", "v"})


class FixtureFormatting(unittest.TestCase):
    def test_fmt_array_is_valid_python_and_roundtrips(self):
        rows = [(i, 1.5 + i, 2.5 + i, 0.5 + i, 2.0 + i, 100 + i) for i in range(40)]
        src = fetch._fmt_array("DAILY", rows)
        ns = {}
        exec(src, ns)
        self.assertEqual(ns["DAILY"], rows)
        self.assertTrue(all(len(ln) <= 120 for ln in src.splitlines()))

    def test_build_fixture_arrays_shapes(self):
        daily = [(_t(2026, 1, 5) + i * 86400, 1.0, 2.0, 0.5, 1.5, 1) for i in range(10)]
        weekly = fetch.resample_weekly(daily)
        h1 = _hourly_session(2026, 11, 3) + _hourly_session(2026, 11, 4)
        arr = fetch.build_fixture_arrays(daily, weekly, h1)
        self.assertEqual(set(arr), {"WEEKLY", "DAILY", "H4", "H1", "FRESH_4H_VOL"})
        self.assertTrue(all(len(b) == 4 for b in arr["WEEKLY"]))
        self.assertTrue(all(len(b) == 6 for b in arr["DAILY"]))
        self.assertTrue(all(len(b) == 4 for b in arr["H4"]))
        self.assertTrue(all(len(b) == 5 for b in arr["H1"]))
        self.assertTrue(all(len(b) == 6 for b in arr["FRESH_4H_VOL"]))
        self.assertEqual(len(arr["H4"]), 4)

    def test_curated_tail_marker_and_legacy(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.py")
            with open(p, "w") as fh:
                fh.write("X = [1]\n\n" + fetch._CURATED_MARKER + "\n# note\nMACRO_PIVOTS = [1]\n")
            self.assertEqual(fetch._curated_tail(p), "# note\nMACRO_PIVOTS = [1]\n")
            with open(p, "w") as fh:            # legacy layout (no marker)
                fh.write('"""doc"""\nX = [1]\n\n# (date, price, kind)\nMACRO_PIVOTS = [2]\n')
            self.assertEqual(fetch._curated_tail(p), "# (date, price, kind)\nMACRO_PIVOTS = [2]\n")
            with open(p, "w") as fh:
                fh.write("X = [1]\n")
            self.assertEqual(fetch._curated_tail(p), "")
        self.assertEqual(fetch._curated_tail(os.path.join(d, "missing.py")), "")


class CommittedFixtures(unittest.TestCase):
    """The regenerated data/avgo.py + data/mrvl.py keep the documented tuple shapes."""

    def test_shapes(self):
        from data import avgo, mrvl
        for m in (avgo, mrvl):
            self.assertTrue(all(len(b) == 4 for b in m.WEEKLY))
            self.assertTrue(all(len(b) == 6 for b in m.DAILY))
            self.assertTrue(all(len(b) == 4 for b in m.H4))
            self.assertTrue(all(len(b) == 5 for b in m.H1))
            self.assertTrue(all(len(b) == 6 for b in m.FRESH_4H_VOL))
            for arr in (m.WEEKLY, m.DAILY, m.H4, m.H1, m.FRESH_4H_VOL):
                ts = [b[0] for b in arr]
                self.assertEqual(ts, sorted(set(ts)), "bars must be ascending, unique")
            self.assertGreater(len(m.FRESH_4H_VOL), 50, "RSI/MACD strands need >50 bars")
        self.assertTrue(isinstance(mrvl.MACRO_PIVOTS, list) and mrvl.MACRO_PIVOTS)


if __name__ == "__main__":
    unittest.main()
