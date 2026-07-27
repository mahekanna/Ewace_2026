"""Legacy containment guard (bundle packs 05/06, adapted to the approved
architecture — docs/ARCHITECTURE.md D11).

The packs' intent: production code must never depend on legacy code. In this
repo the dependency direction is inverted BY DESIGN (wavelib shims import
FROM ewave); this test enforces the invariant that makes that safe:
`src/ewave` must never import `wavelib` — the platform stands alone."""
import ast
import os
import unittest

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, "src", "ewave")


def _imports_wavelib(path: str) -> bool:
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(a.name == "wavelib" or a.name.startswith("wavelib.")
                   for a in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if node.level == 0 and (mod == "wavelib" or mod.startswith("wavelib.")):
                return True
    return False


class TestNoLegacyImports(unittest.TestCase):
    def test_src_ewave_never_imports_wavelib(self):
        offenders = []
        for root, _dirs, files in os.walk(SRC):
            for fn in files:
                if fn.endswith(".py") and _imports_wavelib(os.path.join(root, fn)):
                    offenders.append(os.path.relpath(os.path.join(root, fn), REPO))
        self.assertEqual(offenders, [],
                         "production code depends on the legacy namespace: "
                         + ", ".join(offenders))

    def test_wavelib_is_a_pure_shim_layer(self):
        """Every wavelib module must import from ewave (the shim direction) —
        no residual implementation drifts back into the legacy tree."""
        wl = os.path.join(REPO, "wavelib")
        for fn in sorted(os.listdir(wl)):
            if not fn.endswith(".py"):
                continue
            with open(os.path.join(wl, fn)) as f:
                text = f.read()
            self.assertIn("ewave", text,
                          f"wavelib/{fn} does not reference ewave — "
                          "implementation may have drifted back into legacy")


if __name__ == "__main__":
    unittest.main()
