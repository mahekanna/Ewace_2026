"""Phase 8 acceptance: reporters, TV notes, daily report, charting shims."""
import os
import tempfile
import unittest

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

from ewave.reporting.markdown import daily_report, scan_report
from ewave.reporting.tradingview import note, notes_markdown
from ewave.signals.models import Signal, SignalStatus


def _sig(**kw):
    base = dict(symbol="AVGO", timeframe="15m", signal_time=1_750_000_000,
                pattern_type="wave3_impulse", direction="long",
                entry_trigger="break_close_beyond_w1_extreme",
                entry_price=100.0, stop_price=95.0,
                targets=[("1.618x W1", 110.0), ("2.618x W1", 120.0)],
                invalidation_level=95.0, source_profile="experimental",
                confluence_strands=3, reward_risk=2.0)
    base.update(kw)
    return Signal(**base)


class TestTradingViewNotes(unittest.TestCase):
    def test_note_has_levels_and_no_blind_commands(self):
        text = note(_sig())
        for needle in ("Invalidation level: 95.0", "1.618x W1 110.0",
                       "Manual TradingView steps", "never trades"):
            self.assertIn(needle, text)
        for forbidden in ("BUY NOW", "SELL NOW"):
            self.assertNotIn(forbidden, text.upper().replace("\n", " ")
                             .replace("DO NOT ENTER", ""))

    def test_forming_candidate_carries_warning(self):
        text = note(_sig(status=SignalStatus.CANDIDATE))
        self.assertIn("WARNING", text)
        self.assertNotIn("WARNING", note(_sig()))

    def test_notes_markdown_wraps_blocks(self):
        md = notes_markdown([_sig(), _sig(symbol="MRVL")])
        self.assertEqual(md.count("```"), 4)
        self.assertIn("_No signals._", notes_markdown([]))


class TestReports(unittest.TestCase):
    def test_scan_report_written(self):
        with tempfile.TemporaryDirectory() as d:
            p = scan_report({"profile": "experimental", "timeframe": "15m",
                             "symbols_scanned": 2, "signals": [_sig()],
                             "errors": ["MRVL: no data"]}, out_dir=d)
            text = p.read_text()
            self.assertIn("AVGO", text)
            self.assertIn("MRVL: no data", text)

    def test_scan_report_empty_is_explained(self):
        with tempfile.TemporaryDirectory() as d:
            p = scan_report({"profile": "x", "timeframe": "1h",
                             "symbols_scanned": 1, "signals": [],
                             "errors": []}, out_dir=d)
            self.assertIn("fires selectively", p.read_text().replace("\n", " "))

    def test_daily_report_aggregates_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "signals"))
            with open(os.path.join(d, "signals", "2026-07-09.jsonl"), "w") as f:
                import json
                f.write(json.dumps(_sig().to_dict()) + "\n")
            text = daily_report("2026-07-09", outputs_dir=d)
            self.assertIn("Signals frozen today: 1", text)
            self.assertIn("DSR + MinTRL", text)

    def test_daily_report_empty_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            text = daily_report("2026-07-09", outputs_dir=d)
            self.assertIn("Signals frozen today: 0", text)


class TestChartingShims(unittest.TestCase):
    def test_shims_identity(self):
        import wavelib.charting as WC
        import wavelib.report_chart as WRC
        from ewave.reporting import charting, html_report
        self.assertIs(WC.render_chart, charting.render_chart)
        self.assertIs(WRC.analyze_symbol, html_report.analyze_symbol)
        self.assertIs(WRC.render_analysis_page, html_report.render_analysis_page)


if __name__ == "__main__":
    unittest.main()
