from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


_MODULE_PATH = Path(__file__).resolve().parent / "scripts" / "repo_paths.py"
_SPEC = importlib.util.spec_from_file_location("_assistant_training_repo_paths_impl", str(_MODULE_PATH))
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError(f"unable to load repository path helper from {_MODULE_PATH}")

_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

__all__ = [name for name in dir(_MODULE) if not name.startswith("_")]

for name in __all__:
    globals()[name] = getattr(_MODULE, name)
