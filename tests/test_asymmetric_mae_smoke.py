"""Unit test suite for Asymmetric MAE under tests/ for E2E pytest execution."""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

os.environ["CUDA_VISIBLE_DEVICES"] = ""

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DIVER_PRETRAIN_ROOT = Path("/home/juke/git/DIVER-2/diver_pretrain")
ASYM_DIR = WORKSPACE_ROOT / "code" / "asymmetric_mae"

if str(DIVER_PRETRAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(DIVER_PRETRAIN_ROOT))
if str(ASYM_DIR) not in sys.path:
    sys.path.insert(0, str(ASYM_DIR))

# Load module explicitly to avoid circular import caused by matching file names
_target_file = ASYM_DIR / "test_asymmetric_mae_smoke.py"
_spec = importlib.util.spec_from_file_location("asym_smoke_mod", str(_target_file))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

# Expose test class to pytest and unittest runners
AsymmetricMAESmokeTests = _mod.AsymmetricMAESmokeTests
_make_data_info = _mod._make_data_info

__all__ = ["AsymmetricMAESmokeTests", "_make_data_info"]

if __name__ == "__main__":
    import unittest
    unittest.main(verbosity=2)
