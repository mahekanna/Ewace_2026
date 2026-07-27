"""
wavelib.wavetree — LEGACY SHIM over ewave.patterns.tree
(docs/ARCHITECTURE.md D2). The recursive multi-degree wave-tree engine moved
verbatim (plus the new `tree_context` platform adapter). The full module
namespace — including test-visible internals — is mirrored, so every
historical name resolves to the same object.
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

import ewave.patterns.tree as _tree                               # noqa: E402

globals().update({k: v for k, v in vars(_tree).items()
                  if not (k.startswith("__") and k.endswith("__"))})
del _tree
