"""Tests for the src/ewave platform. Bootstrap `src/` onto sys.path so the
suite runs on a bare checkout (no pip install) — mirrors the wavelib shim's
bootstrap, per docs/ARCHITECTURE.md D2."""
import os
import sys

_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
