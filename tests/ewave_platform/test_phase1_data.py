"""Phase 1 acceptance: models round-trip, store, validation, resample, adapters, MCP bridge."""
import json
import os
import tempfile
import unittest
from unittest import mock

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

from ewave.data.adapters import AdapterUnavailable, get_adapter
from ewave.data.adapters.mcp_bridge import normalize
from ewave.data.models import Bar, BarSeries
from ewave.data.resample import resample
from ewave.data.store import Store, slugify
from ewave.data.validate import in_rth_ny, validate_file, validate_series

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIVE = os.path.join(REPO, "data", "live")
FIX = os.path.join(REPO, "tests", "fixtures")


class TestModels(unittest.TestCase):
    def test_roundtrip_legacy_file_byte_stable(self):
        path = os.path.join(LIVE, "avgo_1d_2026-06.json")
        with open(path) as f:
            original = f.read()
        series = BarSeries.from_dict(json.loads(original))
        self.assertEqual(json.dumps(series.to_dict()), json.dumps(json.loads(original)))

    def test_tuples_bridge(self):
        s = BarSeries("AVGO", "1d", "2026-06-13", [Bar(1, 2.0, 3.0, 1.5, 2.5, 100)])
        self.assertEqual(s.tuples(), [(1, 2.0, 3.0, 1.5, 2.5, 100)])

    def test_from_rows_sorts_and_dedupes_last_wins(self):
        rows = [(20, 1, 2, 0.5, 1.5, 10), (10, 1, 1, 1, 1, 5),
                (20, 9, 9, 9, 9, 99)]  # duplicate t=20, later row wins
        s = BarSeries.from_rows("X", "1d", "2026-01-01", rows)
        self.assertEqual([b.t for b in s.bars], [10, 20])
        self.assertEqual(s.bars[1].o, 9)

    def test_optional_meta_serialized_only_when_set(self):
        s = BarSeries("X", "1d", "2026-01-01", [Bar(1, 1, 1, 1, 1)])
        self.assertNotIn("source", s.to_dict())
        s.source = "csv"
        self.assertEqual(s.to_dict()["source"], "csv")


class TestStore(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("ALPACA:AVGO"), "avgo")
        self.assertEqual(slugify("NASDAQ:BRK.B"), "brkb")

    def test_latest_picks_newest_stamp_and_merge(self):
        with tempfile.TemporaryDirectory() as d:
            store = Store(d)
            old = BarSeries.from_rows("AVGO", "1d", "2026-05-31",
                                      [(100, 1, 2, 0.5, 1.5, 10), (200, 1, 2, 0.5, 1.6, 11)])
            store.write(old, stamp="2026-05")
            new = BarSeries.from_rows("AVGO", "1d", "2026-06-13",
                                      [(200, 9, 9, 9, 9, 99), (300, 1, 2, 0.5, 1.7, 12)])
            p = store.merge_write(new, stamp="2026-06")
            self.assertTrue(p.name.endswith("2026-06.json"))
            self.assertEqual(store.latest("AVGO", "1d"), p)
            merged = store.read("AVGO", "1d")
            self.assertEqual([b.t for b in merged.bars], [100, 200, 300])
            self.assertEqual(merged.bars[1].o, 9)  # new bar won the t=200 slot

    def test_real_store_lists_files(self):
        store = Store(LIVE)
        self.assertGreater(len(store.list()), 50)
        self.assertTrue(store.latest("AVGO", "15m"))
        # extended-hours variant is a distinct series
        eh = store.list(symbol="AVGO", tf="15m", extended=True)
        self.assertEqual(len(eh), 1)


class TestValidate(unittest.TestCase):
    def _series(self, rows):
        return BarSeries("X", "1d", "2026-01-01",
                         [Bar(*r) for r in rows])

    def test_all_live_files_valid(self):
        store = Store(LIVE)
        bad = []
        for p in store.list():
            rep = validate_file(p)
            if not rep.ok:
                bad.append(rep.summary())
        self.assertEqual(bad, [], "\n".join(bad))

    def test_catches_duplicates_descending_ohlc_negv_and_ms(self):
        base = 1700000000
        rep = validate_series(self._series([(base, 1, 2, 0.5, 1.5, 10),
                                            (base, 1, 2, 0.5, 1.5, 10)]))
        self.assertIn("duplicate", " ".join(rep.errors))
        rep = validate_series(self._series([(base + 86400, 1, 2, 0.5, 1.5, 10),
                                            (base, 1, 2, 0.5, 1.5, 10)]))
        self.assertIn("descending", " ".join(rep.errors))
        rep = validate_series(self._series([(base, 5, 4, 1, 4.5, 10)]))  # h < o
        self.assertIn("OHLC", " ".join(rep.errors))
        rep = validate_series(self._series([(base, 1, 2, 0.5, 1.5, -1)]))
        self.assertIn("negative volume", " ".join(rep.errors))
        rep = validate_series(self._series([(base * 1000, 1, 2, 0.5, 1.5, 1)]))
        self.assertIn("unit bug", " ".join(rep.errors))

    def test_empty_is_invalid_not_silent(self):
        rep = validate_series(BarSeries("X", "1d", "2026-01-01", []))
        self.assertFalse(rep.ok)

    def test_in_rth_ny(self):
        # 2026-06-12 13:30 UTC = 09:30 EDT (in), 20:00 UTC = 16:00 EDT (out)
        self.assertTrue(in_rth_ny(1781271000))
        self.assertFalse(in_rth_ny(1781294400))


class TestResample(unittest.TestCase):
    def test_15m_to_1h_session_anchored(self):
        # NY session open 09:30 EDT = 13:30 UTC on 2026-06-12
        t0 = 1781271000
        bars = [(t0 + i * 900, 100 + i, 101 + i, 99 + i, 100.5 + i, 10)
                for i in range(8)]  # 13:30..15:15 UTC
        out = resample(bars, "15m", "1h", calendar="America/New_York")
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0][0], t0)              # bucket anchored at 09:30
        self.assertEqual(out[0][1], 100)             # first open
        self.assertEqual(out[0][2], 104)             # max high of 4 bars
        self.assertEqual(out[0][4], 103.5)           # last close
        self.assertEqual(out[0][5], 40)              # summed volume
        self.assertEqual(out[1][0], t0 + 4 * 900)

    def test_1d_to_1w_iso_monday(self):
        # Mon 2026-06-08 .. Fri 2026-06-12 then Mon 2026-06-15 (UTC days)
        import calendar as _cal
        from datetime import date

        def ts(d):
            return _cal.timegm(d.timetuple())
        days = [date(2026, 6, 8), date(2026, 6, 9), date(2026, 6, 10),
                date(2026, 6, 11), date(2026, 6, 12), date(2026, 6, 15)]
        bars = [(ts(d), 1 + i, 2 + i, 0.5 + i, 1.5 + i, 1) for i, d in enumerate(days)]
        out = resample(bars, "1d", "1w")
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0][5], 5)   # first ISO week has 5 bars
        self.assertEqual(out[0][4], 5.5)  # Friday close

    def test_upsample_rejected(self):
        with self.assertRaises(ValueError):
            resample([], "1d", "15m")

    def test_real_data_15m_to_1d_closes_match_cached_daily(self):
        """Cross-source oracle: daily closes built from RTH 15m bars must match
        the independently cached 1d series for the same NY dates."""
        from datetime import datetime, timezone, timedelta
        try:
            from zoneinfo import ZoneInfo
            ny = ZoneInfo("America/New_York")
        except Exception:
            ny = timezone(timedelta(hours=-4))

        def ny_date(t):
            return datetime.fromtimestamp(t, ny).date()
        store = Store(LIVE)
        src = store.read("AVGO", "15m").tuples()
        out = resample(src, "15m", "1d", calendar="America/New_York")
        ref = {ny_date(b.t): b.c for b in store.read("AVGO", "1d").bars}
        common = [(b[4], ref[ny_date(b[0])]) for b in out if ny_date(b[0]) in ref]
        self.assertGreater(len(common), 100)
        diffs = sorted(abs(got - want) / max(abs(want), 1e-9) for got, want in common)
        # a bucketing bug (shifted dates) would blow both of these out; residual
        # spread is IEX-15m vs consolidated-1d feed disagreement (median ~0.04%)
        self.assertLess(diffs[len(diffs) // 2], 0.002,
                        f"median daily-close diff {diffs[len(diffs)//2]:.4%}")
        within = sum(1 for x in diffs if x <= 0.025)
        self.assertGreater(within / len(diffs), 0.95,
                           f"only {within}/{len(diffs)} daily closes within 2.5%")


class TestAdapters(unittest.TestCase):
    def test_contract_adapter_reads_cache(self):
        a = get_adapter("contract", base_dir=LIVE)
        s = a.fetch("AVGO", "1d")
        self.assertGreater(len(s), 100)

    def test_csv_adapter(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write("time,open,high,low,close,volume\n")
            f.write("2026-06-12T13:30:00Z,384.2,385.4,383.9,385.0,150000\n")
            f.write("1749735900,385.0,386.3,384.6,386.1,180000\n")
            path = f.name
        try:
            s = get_adapter("csv").fetch("AVGO", "15m", path=path)
            self.assertEqual(len(s), 2)
            self.assertEqual(s.bars[1].c, 385.0)  # ISO row is later than unix row
        finally:
            os.unlink(path)

    def test_alpaca_requires_keys(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(AdapterUnavailable):
                get_adapter("alpaca").fetch("AVGO", "15m")

    def test_alpaca_parses_mocked_response(self):
        payload = {"bars": [{"t": "2026-06-12T13:30:00Z", "o": 384.2, "h": 385.4,
                             "l": 383.9, "c": 385.0, "v": 150000}],
                   "next_page_token": None}

        class _Resp:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            @staticmethod
            def read():
                return json.dumps(payload).encode()
        import ewave.data.adapters.alpaca_rest as ar
        with mock.patch.object(ar.urllib.request, "urlopen", return_value=_Resp()):
            a = ar.AlpacaRest(key="k", secret="s")
            s = a.fetch("AVGO", "15m")
        self.assertEqual(len(s), 1)
        self.assertEqual(s.symbol, "ALPACA:AVGO")
        self.assertEqual(s.bars[0].t, 1781271000)  # 2026-06-12T13:30:00Z

    def test_fmp_requires_key(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(AdapterUnavailable):
                get_adapter("fmp").fetch("AVGO", "1d")

    def test_yfinance_unavailable_without_package(self):
        import builtins
        real_import = builtins.__import__

        def deny_yf(name, *a, **k):
            if name == "yfinance":
                raise ImportError("nope")
            return real_import(name, *a, **k)
        with mock.patch.object(builtins, "__import__", side_effect=deny_yf):
            with self.assertRaises(AdapterUnavailable):
                get_adapter("yfinance").fetch("AVGO", "1d")


class TestMcpBridge(unittest.TestCase):
    def _fix(self, name):
        with open(os.path.join(FIX, name)) as f:
            return json.load(f)

    def test_fmp_chart_ny_time_and_reorder(self):
        s = normalize(self._fix("mcp_fmp_chart.json"), "fmp", "AVGO", "1h")
        self.assertEqual(len(s), 3)
        ts = [b.t for b in s.bars]
        self.assertEqual(ts, sorted(ts))
        # 2026-06-12 13:00 America/New_York (EDT) = 17:00 UTC
        self.assertEqual(s.bars[0].t, 1781283600)

    def test_yfinance_history(self):
        s = normalize(self._fix("mcp_yf_history.json"), "yf", "AVGO", "1d")
        self.assertEqual(len(s), 3)
        self.assertEqual(s.bars[-1].c, 386.9)

    def test_tvremix_ohlcv(self):
        s = normalize(self._fix("mcp_tv_ohlcv.json"), "tv", "NASDAQ:AVGO", "15m")
        self.assertEqual(len(s), 3)
        self.assertEqual(s.symbol, "AVGO")
        self.assertEqual(s.bars[0].t, 1749735000)

    def test_alpaca_mcp_dump(self):
        s = normalize(self._fix("mcp_alpaca_bars.json"), "alpaca-mcp", "AVGO", "15m")
        self.assertEqual(len(s), 3)

    def test_unparseable_payload_raises(self):
        with self.assertRaises(ValueError):
            normalize({"garbage": True}, "tv", "AVGO", "15m")


if __name__ == "__main__":
    unittest.main()
