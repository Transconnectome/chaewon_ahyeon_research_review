"""End-to-end CPU verification suite for `AsymmetricMultiHeadMAEModel` against live DIVER-2."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from types import SimpleNamespace
import unittest
import warnings

os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Strict CPU-only verification

DIVER_PRETRAIN_ROOT = Path("/home/juke/git/DIVER-2/diver_pretrain")
THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(DIVER_PRETRAIN_ROOT))
sys.path.insert(0, str(THIS_DIR))

import numpy as np
import torch

from asymmetric_mae import register_with_diver2
from config.cfg import Experiments
from pretrain_trainer import MuonWithAuxAdam, PretrainTrainer, build_ssl_method
import src.models.diver as diver_mod


def _make_data_info(batch_size: int, channels: int, n_patches: int = 3, padded: bool = False):
    rng = np.random.default_rng(42)
    infos = []
    for b in range(batch_size):
        xyz = rng.uniform(-60.0, 60.0, size=(channels, 3)).astype(np.float32)
        subtypes = ["depth" if c % 2 == 0 else "grid" for c in range(channels)]
        info = {
            "modality": "iEEG",
            "channel_types": ["iEEG"] * channels,
            "channel_subtypes": subtypes,
            "coord_subtype": subtypes,
            "xyz_id": xyz,
        }
        if padded:
            valid = np.ones((channels, n_patches, 500), dtype=bool)
            if b == 1:
                valid[-2:, :, :] = False    # Last 2 channels padded
                valid[:, -1, :] = False     # Last 1s time patch padded
            info["input_was_resampled_and_padded"] = True
            info["valid"] = valid
        else:
            info["input_was_resampled_and_padded"] = False
        infos.append(info)
    return infos


class AsymmetricMAESmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.simplefilter("ignore")
        register_with_diver2()

    def test_1_encoder_token_dropping_ratio_3s_and_30s(self):
        """Verify masked patches are physically removed before `model.encoder.encoder`."""
        cfg75 = Experiments.DIVER_iEEG_ASYM_MAE_model(d_model=128, e_layers=2, patch_size=500)
        model75 = diver_mod.build_model(cfg75).eval()

        captured_shapes = []
        handle = model75.encoder.encoder.register_forward_pre_hook(
            lambda _mod, args: captured_shapes.append(tuple(args[0].shape))
        )
        try:
            # Case A: 3s window (C=8, N=3 -> full aug grid = 9*4 = 36; registers = 1+8+3 = 12; patches = 24 -> K_vis = 6 -> L_enc = 18)
            x_3s = torch.randn(2, 8, 1500)
            info_3s = _make_data_info(2, 8, n_patches=3)
            model75(x_3s, data_info_list=info_3s, use_mask=True)
            self.assertEqual(captured_shapes[-1], (2, 12 + 6, 128))

            # Case B: 30s window (C=16, N=30 -> full aug grid = 17*31 = 527; registers = 47; patches = 480 -> K_vis = 120 -> L_enc = 167 vs 527!)
            x_30s = torch.randn(2, 16, 15000)
            info_30s = _make_data_info(2, 16, n_patches=30)
            model75(x_30s, data_info_list=info_30s, use_mask=True)
            self.assertEqual(captured_shapes[-1], (2, 47 + 120, 128))
            flop_ratio = (527 ** 2) / (167 ** 2)
            self.assertGreater(flop_ratio, 9.9)  # ~10x quadratic attention speedup on 30s!
        finally:
            handle.remove()

    def test_2_zero_masked_signal_leakage_into_encoder(self):
        """Prove mathematically that perturbing masked patches has 0.0 effect on encoder latents."""
        cfg = Experiments.DIVER_iEEG_ASYM_MAE_mask50_model(d_model=128, e_layers=2, patch_size=500)
        model = diver_mod.build_model(cfg).eval()

        x = torch.randn(2, 6, 3, 500)
        info = _make_data_info(2, 6, n_patches=3)

        torch.manual_seed(777)
        out_clean = model(x, data_info_list=info, use_mask=True, return_encoder_output=True)
        mask = out_clean["mask"]  # [2, 6, 3], 1.0 where masked

        # Inject a massive +500.0 shock strictly on masked patches
        x_shocked = x.clone()
        x_shocked[mask == 1] += 500.0

        torch.manual_seed(777)
        out_shocked = model(x_shocked, data_info_list=info, use_mask=True, return_encoder_output=True)

        self.assertTrue(torch.equal(mask, out_shocked["mask"]))
        max_enc_diff = (out_clean["encoder_output"] - out_shocked["encoder_output"]).abs().max().item()
        self.assertEqual(max_enc_diff, 0.0)

    def test_3_ssl_loss_backward_ddp_safety_and_muon_routing(self):
        """Verify 100% trainable params get gradients (DDP safe) and Muon/AdamW split works."""
        cfg = Experiments.DIVER_iEEG_ASYM_MAE_model(d_model=128, e_layers=4, patch_size=500)
        model = diver_mod.build_model(cfg).train()

        params_ns = SimpleNamespace(
            cl_weight=1.0,
            cl_temperature=0.5,
            weight_decay=1e-4,
            no_decay_norm_bias=True,
        )
        ssl = build_ssl_method(
            "MAEMultiHead_onlypatchwise",
            model,
            params_ns,
            loss_configs=cfg.basemodel.params["patchwise_ssl_configs"],
        )

        # Verify PretrainTrainer._split_muon_params routes decoder_mask_token to AdamW (aux_no_decay)
        muon_params, aux_decay, aux_no_decay = PretrainTrainer._split_muon_params(
            model, params_ns
        )
        muon_ids = {id(p) for p in muon_params}
        aux_ids = {id(p) for p in aux_decay + aux_no_decay}
        self.assertNotIn(id(model.decoder_mask_token), muon_ids)
        self.assertIn(id(model.decoder_mask_token), aux_ids)
        self.assertIn(id(model.enc_to_dec.weight), muon_ids)

        opt = MuonWithAuxAdam(
            [
                {"params": muon_params, "weight_decay": 1e-4, "use_muon": True, "lr": 0.01},
                {"params": aux_decay, "weight_decay": 1e-4, "use_muon": False, "lr": 1e-3},
                {"params": aux_no_decay, "weight_decay": 0.0, "use_muon": False, "lr": 1e-3},
            ],
            lr=1e-3,
            muon_lr=0.01,
        )

        x = torch.randn(2, 6, 1500)
        info = _make_data_info(2, 6, n_patches=3)

        losses = []
        for step in range(3):
            opt.zero_grad()
            loss = ssl.compute_loss(x, data_info_list=info)
            self.assertTrue(torch.isfinite(loss), f"Non-finite loss at step {step}")
            loss.backward()

            if step == 0:
                unused = [
                    name
                    for name, p in model.named_parameters()
                    if p.requires_grad and (p.grad is None or not torch.isfinite(p.grad).all())
                ]
                self.assertEqual(
                    unused,
                    [],
                    f"DDP find_unused_parameters=False hazard! Unused/NaN params: {unused}",
                )
            opt.step()
            losses.append(loss.item())

        self.assertLess(losses[-1], losses[0], f"Loss did not decrease over 3 steps: {losses}")

    def test_4_padded_batch_handling(self):
        """Verify padded heterogeneous batches run cleanly without NaN or mask leakage."""
        cfg = Experiments.DIVER_iEEG_ASYM_MAE_model(d_model=128, e_layers=2, patch_size=500)
        model = diver_mod.build_model(cfg).train()
        ssl = build_ssl_method(
            "MAEMultiHead_onlypatchwise",
            model,
            SimpleNamespace(cl_weight=1.0, cl_temperature=0.5),
            loss_configs=cfg.basemodel.params["patchwise_ssl_configs"],
        )

        x = torch.randn(2, 8, 1500)
        info = _make_data_info(2, 8, n_patches=3, padded=True)
        loss = ssl.compute_loss(x, data_info_list=info)
        self.assertTrue(torch.isfinite(loss))
        loss.backward()

    def test_5_imindbench_inference_parity_and_trunc(self):
        """Verify `use_mask=False` skips decoder and matches stock DIVER `rd1` & `rdall` shapes."""
        stock_cfg = Experiments.DIVER_iEEG_FINAL_model(d_model=128, e_layers=4, patch_size=500)
        asym_cfg = Experiments.DIVER_iEEG_ASYM_MAE_model(d_model=128, e_layers=4, patch_size=500)
        stock_m = diver_mod.build_model(stock_cfg).eval()
        asym_m = diver_mod.build_model(asym_cfg).eval()

        decoder_calls = []
        handle = asym_m.decoder.register_forward_pre_hook(lambda *_: decoder_calls.append(1))
        x = torch.randn(2, 6, 1500)
        info = _make_data_info(2, 6, n_patches=3)

        try:
            for trunc_val in ("", "1"):
                os.environ["DIVER_ENCODER_TRUNC"] = trunc_val
                s_out = stock_m(x, data_info_list=info, use_mask=False)
                a_out = asym_m(x, data_info_list=info, use_mask=False)
                self.assertEqual(
                    s_out["token_manager_output"]["org_x_position_features"].shape,
                    a_out["token_manager_output"]["org_x_position_features"].shape,
                )
                self.assertEqual(
                    s_out["token_manager_output"]["n_position_features"].shape,
                    a_out["token_manager_output"]["n_position_features"].shape,
                )
            self.assertEqual(decoder_calls, [], "Decoder must NEVER run when use_mask=False!")
        finally:
            os.environ.pop("DIVER_ENCODER_TRUNC", None)
            handle.remove()

    def test_6_imindbench_strict_checkpoint_export_bit_exact(self):
        """Exported compat checkpoint loads into stock DIVER_iEEG_FINAL_model (strict=True) with 0.0 feature diff."""
        import tempfile
        from asymmetric_mae import export_imindbench_compat_checkpoint

        asym_cfg = Experiments.DIVER_iEEG_ASYM_MAE_model(d_model=128, e_layers=3)
        asym_model = diver_mod.build_model(asym_cfg).eval()

        with tempfile.TemporaryDirectory() as tmpdir:
            raw_ckpt = Path(tmpdir) / "last.pt"
            torch.save(
                {
                    "format_version": 3,
                    "epoch": 1,
                    "global_step": 10,
                    "best_loss": 0.123,
                    "model_state_dict": asym_model.state_dict(),
                    "ssl_method": "MAEMultiHead_onlypatchwise",
                    "metric": 0.123,
                    "args": {
                        "model_config": "DIVER_iEEG_ASYM_MAE_model",
                        "width": 128,
                        "depth": 3,
                        "input_scale": 100.0,
                    },
                },
                raw_ckpt,
            )
            compat_path = export_imindbench_compat_checkpoint(str(raw_ckpt))
            compat_ckpt = torch.load(compat_path, map_location="cpu", weights_only=False)
            self.assertEqual(compat_ckpt["args"]["model_config"], "DIVER_iEEG_FINAL_model")

            stock_cfg = Experiments.DIVER_iEEG_FINAL_model(d_model=128, e_layers=3)
            stock_model = diver_mod.build_model(stock_cfg).eval()
            stock_model.load_state_dict(compat_ckpt["model_state_dict"], strict=True)

            torch.manual_seed(77)
            x = torch.randn(2, 8, 1500)
            infos = _make_data_info(2, 8, 3)
            try:
                for trunc in ("", "1"):
                    if trunc:
                        os.environ["DIVER_ENCODER_TRUNC"] = trunc
                    else:
                        os.environ.pop("DIVER_ENCODER_TRUNC", None)
                    with torch.no_grad():
                        a_out = asym_model(x, data_info_list=infos, use_mask=False, return_encoder_output=True)
                        s_out = stock_model(x, data_info_list=infos, use_mask=False, return_encoder_output=True)
                    diff = (
                        a_out["token_manager_output"]["org_x_position_features"]
                        - s_out["token_manager_output"]["org_x_position_features"]
                    ).abs().max().item()
                    self.assertEqual(diff, 0.0, f"Feature mismatch after compat export (trunc={trunc!r}): {diff}")
            finally:
                os.environ.pop("DIVER_ENCODER_TRUNC", None)

    def test_7_cli_wrapper_end_to_end(self):
        """Run `run_asym_mae_wrapper.main()` end-to-end (PretrainTrainer.fit + compat ckpt export)."""
        import tempfile
        import types

        # Stub optional C-extensions if absent on a lightweight dev node (`--fake_data True` does not use them)
        for opt_pkg in ("blosc2", "lmdb"):
            if opt_pkg not in sys.modules:
                try:
                    __import__(opt_pkg)
                except ModuleNotFoundError:
                    sys.modules[opt_pkg] = types.ModuleType(opt_pkg)

        import run_asym_mae_wrapper

        orig_argv = list(sys.argv)
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir) / "cli_smoke"
            try:
                sys.argv = [
                    "run_asym_mae_wrapper.py",
                    "--fake_data", "True",
                    "--fake_steps", "2",
                    "--fake_channels", "8",
                    "--fake_patches", "3",
                    "--fake_patch_size", "500",
                    "--output_dir", str(out_dir),
                    "--model_config", "DIVER_iEEG_ASYM_MAE_model",
                    "--width", "128",
                    "--depth", "2",
                    "--ssl_method", "MAEMultiHead_onlypatchwise",
                    "--batch_size", "2",
                    "--epochs", "1",
                    "--num_workers", "0",
                    "--amp", "False",
                    "--export_eval_compat_ckpt",
                ]
                run_asym_mae_wrapper.main()
            finally:
                sys.argv = orig_argv

            self.assertTrue((out_dir / "last.pt").is_file(), "last.pt was not saved")
            self.assertTrue(
                (out_dir / "last_imindbench_compat.pt").is_file(),
                "last_imindbench_compat.pt was not exported",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
