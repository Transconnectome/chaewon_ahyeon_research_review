#!/usr/bin/env python3
"""Zero-edit CLI launcher for True Asymmetric Encoder-Decoder MAE on DIVER-2.

Usage (Single GPU or torchrun DDP — identical flags to `pretrain_main.py`)
--------------------------------------------------------------------------
  export DIVER_PRETRAIN_ROOT=/path/to/DIVER-2/diver_pretrain

  torchrun --standalone --nproc_per_node=4 \
    /path/to/chaewon_ahyeon_research_review/code/asymmetric_mae/run_asym_mae_wrapper.py \
    --dataset_dir /path/to/ieeg_lmdb \
    --output_dir /path/to/runs/asym_mae_mask75_s42 \
    --model_config DIVER_iEEG_ASYM_MAE_model \
    --width 512 --depth 12 \
    --ssl_method MAEMultiHead_onlypatchwise \
    --input_was_resampled_and_padded_3sec True \
    --optimizer muon --lr 1e-3 --muon_lr 0.005 \
    --batch_size 64 --epochs 20 --seed 42 \
    --export_eval_compat_ckpt

Standalone checkpoint conversion (for an existing `last.pt` or `best.pt`)
-------------------------------------------------------------------------
  python3 run_asym_mae_wrapper.py --convert_only /path/to/runs/asym_mae_mask75_s42/last.pt
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _resolve_diver_pretrain_root() -> Path:
    env_root = os.environ.get("DIVER_PRETRAIN_ROOT", "").strip()
    candidates = []
    if env_root:
        candidates.append(Path(env_root).expanduser().resolve())
    candidates.extend(
        [
            Path.cwd().resolve(),
            Path("/home/juke/git/DIVER-2/diver_pretrain"),
        ]
    )
    for cand in candidates:
        if (cand / "pretrain_main.py").is_file() and (cand / "src" / "models" / "diver.py").is_file():
            return cand
    raise FileNotFoundError(
        "Could not locate `DIVER-2/diver_pretrain` (expected `pretrain_main.py`). "
        "Set `export DIVER_PRETRAIN_ROOT=/path/to/DIVER-2/diver_pretrain` or `cd` into `diver_pretrain`."
    )


def main() -> None:
    diver_root = _resolve_diver_pretrain_root()
    this_dir = Path(__file__).resolve().parent
    for p in (str(this_dir), str(diver_root)):
        if p not in sys.path:
            sys.path.insert(0, p)

    from asymmetric_mae import export_imindbench_compat_checkpoint, register_with_diver2

    register_with_diver2()

    argv = list(sys.argv[1:])

    # Mode 1: Standalone checkpoint converter (`--convert_only /path/to/ckpt.pt`)
    if "--convert_only" in argv:
        idx = argv.index("--convert_only")
        if idx + 1 >= len(argv):
            raise SystemExit("Usage: run_asym_mae_wrapper.py --convert_only /path/to/last.pt")
        ckpt_path = argv[idx + 1]
        dst = export_imindbench_compat_checkpoint(ckpt_path)
        print(f"[AsymMAE] Exported strict=True imindbench-compatible checkpoint: {dst}", flush=True)
        return

    # Mode 2: Full DIVER-2 pretraining (`pretrain_main.py` drop-in)
    export_compat = False
    if "--export_eval_compat_ckpt" in argv:
        export_compat = True
        argv.remove("--export_eval_compat_ckpt")

    import pretrain_main

    args = pretrain_main.build_parser().parse_args(argv)
    args.process_start = pretrain_main._PROCESS_START
    pretrain_main.run(args)

    rank = int(os.environ.get("RANK", "0"))
    if export_compat and rank == 0:
        out_dir = Path(args.output_dir)
        for name in ("last.pt", "best.pt"):
            src = out_dir / name
            if src.is_file():
                dst = export_imindbench_compat_checkpoint(str(src))
                print(f"[AsymMAE] Exported strict=True imindbench-compatible checkpoint: {dst}", flush=True)


if __name__ == "__main__":
    main()
