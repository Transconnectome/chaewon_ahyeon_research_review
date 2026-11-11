"""True Asymmetric Encoder-Decoder Masked Autoencoder (MAE) for DIVER-2 iEEG/EEG.

Why this module exists
----------------------
Stock `DIVER_iEEG_FINAL_model` (`MultiHeadPrependPatchMaskedModel` in
`src/models/diver.py`) is named `MAEMultiHead_onlypatchwise`, but architecturally
it is a **BERT/SimMIM-style encoder-only masked patch predictor**:
  1. Masked patches are zeroed in-place (`masked_x[mask == 1] = 0`) and still fed
     into the main Transformer encoder alongside visible patches.
  2. There is NO separate decoder: `heads['org']` (`multi_linear_heads`) sits
     directly on top of the final encoder layer (`org_x_position_features`),
     forcing the deepest encoder layers (e.g. Layer 12 in Small) to specialize in
     low-level waveform + STFT/FFT reconstruction rather than abstract neural
     state representations (causing the `-0.0050` Layer-12 collapse at 1/1024).

`AsymmetricMultiHeadMAEModel` implements **He et al. (CVPR 2022) Asymmetric MAE**
natively on top of DIVER's 3D-coordinate + Moirai channel-time backbone:
  1. **Zero-Leakage Visible-Only Encoder**: Masked patches are zeroed before
     `self.embedding` (preventing `timewise_reduced_stcpe` neighbor leakage) and
     **physically dropped** before `self.encoder`. Only register tokens + the
     `K_vis = round((1 - mask_ratio) * C * N)` unmasked patches enter the main
     Moirai encoder, carrying their exact `(var_id, time_id)` for BinaryAttentionBias
     and Rotary Position Embedding (RoPE).
  2. **Lightweight Asymmetric Moirai Decoder**: Encoder visible latents are
     projected (`d_model -> decoder_d_model`, default 256), combined with a
     learnable `[MASK]` token (`decoder_mask_token`, 3-D so `Muon` routes it to
     AdamW) at masked `(c, n)` positions plus 3D electrode coordinate + modality
     positional embeddings (`PositionalEncoding3D` + `ChannelType/SubType`), and
     decoded by a shallow 2-layer Moirai Transformer decoder before `heads['org']`.
  3. **100% Drop-In Compatibility**:
     - Trainer & Loss: Works unchanged with `--ssl_method MAEMultiHead_onlypatchwise`
       and `--optimizer muon` or `adamw` (100% of trainable params receive
       gradients every step -> DDP `find_unused_parameters=False` safe).
     - Downstream Evaluation (`imindbench` / `run_suite.py`): When `use_mask=False`,
       the decoder is completely bypassed (0 extra FLOPs) and standard encoder
       features (`org_x_position_features`, `n_position_features`, plus
       `DIVER_ENCODER_TRUNC=1` for `rd1` vs `rdall`) are returned identically.
"""

from __future__ import annotations

import copy
from functools import partial
from typing import Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.profiler import record_function

from config.cfg import Config, EmbeddingParams, HeadParams
from src.layers.Embed import (
    AddEmbedding,
    ChannelSubTypeEmbedding,
    ChannelTypeEmbedding,
    CombinedEmbedding,
    ConcateEmbedding,
    PositionalEncoding3D,
)
from src.layers.Original_Moirai_bias import BinaryAttentionBias
from src.layers.Original_Moirai_projection import QueryKeyProjection, RotaryProjection
from src.utils.norms import RMSNorm
from src.layers.masking import real_data_token_mask
from src.models.Original_Moirai_encoder import (
    TransformerEncoder as OriginalMoiraiTransformerEncoder,
)
from src.models.components import create_head
from src.models.diver import MultiHeadPrependPatchMaskedModel
from src.SSL.SSL_methods import getMultiMultiheadDict_fromDummy


class AsymmetricMultiHeadMAEModel(MultiHeadPrependPatchMaskedModel):
    """He et al. (2022) Asymmetric Encoder-Decoder MAE for DIVER patch grids."""

    def __init__(self, configs: Config):
        super().__init__(configs)

        bp = configs.basemodel.params if isinstance(configs.basemodel.params, dict) else {}
        self.mask_ratio = float(bp.get("mask_ratio", 0.75))
        if not (0.0 < self.mask_ratio < 1.0):
            raise ValueError(
                f"AsymmetricMultiHeadMAEModel requires 0 < mask_ratio < 1, got {self.mask_ratio}"
            )

        enc_d_model = int(configs.encoder.params["d_model"])
        self.decoder_d_model = int(bp.get("decoder_d_model", max(128, enc_d_model // 2)))
        self.decoder_layers = int(bp.get("decoder_e_layers", 2))
        self.decoder_heads = int(bp.get("decoder_n_heads", max(1, self.decoder_d_model // 32)))
        decoder_dropout = float(bp.get("decoder_dropout", configs.encoder.params.get("dropout", 0.1)))
        use_mup = bool(getattr(configs, "use_mup", False))

        # 1. Encoder -> Decoder bottleneck projection
        self.enc_to_dec = nn.Linear(enc_d_model, self.decoder_d_model, bias=True)

        # 2. Learnable [MASK] token kept 3-D (1, 1, D_dec) so PretrainTrainer._split_muon_params
        #    routes it to AdamW (no_decay) rather than orthogonalizing a 1-vector with Muon.
        self.decoder_mask_token = nn.Parameter(torch.zeros(1, 1, self.decoder_d_model))
        nn.init.trunc_normal_(self.decoder_mask_token, std=0.02)

        # 3. Pure metadata positional embedding for decoder tokens (3D MNI xyz + modality + subtype).
        #    Reads ONLY `data_info_list` metadata on a zero tensor -> zero signal leakage.
        emb_params = configs.embedding.params
        pe_params = dict(emb_params.get("pe_params", {"emb_style": "cpe", "pe_learnable_proj": True, "temperature": 2000, "scale": 1 / 256}))
        d_chtype_dec = max(16, self.decoder_d_model // 4)
        avail_types = emb_params.get("available_ch_types", ["EEG", "iEEG"])
        avail_subtypes = emb_params.get("available_ch_subtypes", ["grid", "strip", "depth"])

        self.decoder_pos_embed = AddEmbedding(
            ConcateEmbedding(
                PositionalEncoding3D(
                    d_model=self.decoder_d_model - d_chtype_dec,
                    pe_params=pe_params,
                    emb_style=pe_params.get("emb_style", "cpe"),
                    learnable_proj=pe_params.get("pe_learnable_proj", True),
                ),
                CombinedEmbedding(
                    ChannelTypeEmbedding(avail_types, d_chtype_dec, True),
                    ChannelSubTypeEmbedding(avail_subtypes, d_chtype_dec, True),
                ),
            )
        )

        # 4. Lightweight Asymmetric Moirai Transformer Decoder (full [B, C*N, D_dec] grid)
        self.decoder = OriginalMoiraiTransformerEncoder(
            d_model=self.decoder_d_model,
            num_layers=self.decoder_layers,
            num_heads=self.decoder_heads,
            num_groups=self.decoder_heads,
            pre_norm=True,
            attn_dropout_p=decoder_dropout,
            dropout_p=decoder_dropout,
            norm_layer=RMSNorm,
            activation=nn.SiLU(),
            use_moe=False,
            use_glu=True,
            use_qk_norm=True,
            var_attn_bias_layer=partial(BinaryAttentionBias),
            time_attn_bias_layer=None,
            var_qk_proj_layer=None,
            time_qk_proj_layer=partial(
                QueryKeyProjection,
                proj_layer=RotaryProjection,
                kwargs=dict(max_len=512),
                partial_factor=None,
            ),
            shared_var_attn_bias=False,
            shared_time_qk_proj=True,
            d_ff=4 * self.decoder_d_model,
            use_bias=False,
            flash_attention=bool(configs.encoder.params.get("flash_attention", True)),
            use_mup=use_mup,
        )
        # Ensure DIVER_ENCODER_TRUNC never truncates the reconstruction decoder.
        self.decoder._diver_main_encoder = False

        # 5. Rebuild `heads['org']` (`multi_linear_heads`) to read `decoder_d_model` instead of `enc_d_model`
        patchwise_ssl_configs = bp.get("patchwise_ssl_configs")
        if patchwise_ssl_configs is not None and "org" in self.heads:
            dec_head_params = getMultiMultiheadDict_fromDummy(
                int(bp["input_token_len"]),
                self.decoder_d_model,
                patchwise_ssl_configs,
            )
            for key in dec_head_params:
                dec_head_params[key]["use_mup"] = use_mup
            dec_org_head_cfg = HeadParams(type="multi_linear_heads", params=dec_head_params)
            self.heads["org"] = create_head(dec_org_head_cfg.type, dec_org_head_cfg)

    @staticmethod
    def _is_padded_batch(data_info_list) -> bool:
        return bool(
            data_info_list is not None
            and len(data_info_list) > 0
            and isinstance(data_info_list[0], dict)
            and data_info_list[0].get("input_was_resampled_and_padded", False)
        )

    def _sample_visible_and_mask(
        self,
        B: int,
        C: int,
        N: int,
        device: torch.device,
        data_info_list=None,
        token_len: Optional[int] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor, Optional[torch.Tensor]]:
        """Per-sample uniform visible-token sampling (He et al. 2022 `random_masking`).

        Padded tokens (if any) are pushed to the end of the random ranking so the
        encoder never wastes visible capacity on zero-padded channels/timepoints.

        Returns
        -------
        ids_keep : LongTensor [B, K_vis]
            Flattened patch indices in `0 .. C*N - 1` kept for the encoder.
        mask : FloatTensor [B, C, N]
            `1.0` on masked patches, `0.0` on kept visible patches.
        real_patch_valid : Optional[BoolTensor [B, C, N]]
            Real-token mask when the batch contains padding, else `None`.
        """
        L = C * N
        noise = torch.rand(B, L, device=device)

        real_patch_valid = None
        if self._is_padded_batch(data_info_list):
            real_patch_valid = real_data_token_mask(
                data_info_list, N, device, token_len=token_len
            )  # [B, C, N] bool
            valid_flat = real_patch_valid.reshape(B, L)
            # Push invalid (padded) slots behind all real slots in argsort
            noise = noise + (~valid_flat).float() * 10.0

            # Per-sample k_vis calculation to prevent heterogeneous montage mask vanishing
            k_vis_list = []
            for b in range(B):
                v_b = int(valid_flat[b].sum().item())
                if v_b >= 2:
                    k_b = int(round((1.0 - self.mask_ratio) * v_b))
                    k_b = max(1, min(v_b - 1, k_b))
                else:
                    k_b = 1
                k_vis_list.append(k_b)
            k_vis_max = max(1, min(L - 1, max(k_vis_list))) if L >= 2 else 1

            ids_shuffle = torch.argsort(noise, dim=1)  # [B, L]
            ids_keep_list = []
            mask_flat = torch.zeros(B, L, dtype=self.precision, device=device)

            for b in range(B):
                v_b = int(valid_flat[b].sum().item())
                k_b = k_vis_list[b]
                vis_tokens = ids_shuffle[b, :k_b]
                mask_tokens = ids_shuffle[b, k_b:v_b]
                mask_flat[b].scatter_(0, mask_tokens, 1.0)

                if k_vis_max > k_b:
                    extra_needed = k_vis_max - k_b
                    extra_tokens = ids_shuffle[b, v_b:v_b + extra_needed]
                    if extra_tokens.numel() < extra_needed:
                        extra_tokens = ids_shuffle[b, :extra_needed]
                    sample_keep = torch.cat([vis_tokens, extra_tokens])
                else:
                    sample_keep = vis_tokens[:k_vis_max]

                sample_keep = torch.sort(sample_keep).values
                ids_keep_list.append(sample_keep)

            ids_keep = torch.stack(ids_keep_list, dim=0)
        else:
            ref_len = max(2, L)
            k_vis = int(round((1.0 - self.mask_ratio) * ref_len))
            k_vis = max(1, min(L - 1, k_vis)) if L >= 2 else 1

            ids_shuffle = torch.argsort(noise, dim=1)  # [B, L]
            ids_keep = torch.sort(ids_shuffle[:, :k_vis], dim=1).values  # [B, K_vis], sorted for cache locality

            mask_flat = torch.ones(B, L, dtype=self.precision, device=device)
            mask_flat.scatter_(1, ids_keep, 0.0)

        # Safety fallback: ensure at least one token is masked to prevent empty tensor NaN loss
        if mask_flat.sum() == 0.0:
            mask_flat[0, 0] = 1.0

        return ids_keep, mask_flat.view(B, C, N), real_patch_valid

    def _encode_visible_only(
        self,
        full_grid: torch.Tensor,
        ids_keep: torch.Tensor,
        C: int,
        N: int,
        data_info_list=None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Run `self.encoder` ONLY on register tokens + `K_vis` visible patch tokens.

        Parameters
        ----------
        full_grid : Tensor [B, 1+C, 1+N, D_enc]
            Output of `token_manager.prepend_x_with_tokens(emb_grid)`.
        ids_keep : LongTensor [B, K_vis]
            Kept patch indices in `0 .. C*N - 1`.

        Returns
        -------
        z_vis : Tensor [B, K_vis, D_enc]
            Encoded representations of the visible patches only.
        sparse_full_out : Tensor [B, 1+C, 1+N, D_enc]
            Encoded registers + visible patches scattered into the `(1+C, 1+N)` grid
            so `token_manager.extract_prepended_x` preserves its state invariant.
        """
        B, C_aug, N_aug, D_enc = full_grid.shape
        device = full_grid.device
        kc = C_aug - C  # 1 for vanilla_NC_prepend
        kn = N_aug - N  # 1 for vanilla_NC_prepend

        if getattr(self.encoder, "_uses_coords", False):
            self.encoder._push_coords(data_info_list, C_aug, device)

        flat_grid = full_grid.reshape(B, C_aug * N_aug, D_enc)
        var_id_full = torch.repeat_interleave(
            torch.arange(C_aug, device=device), repeats=N_aug
        ).expand(B, -1)
        time_id_full = torch.tile(
            torch.arange(N_aug, device=device), (C_aug,)
        ).expand(B, -1)

        # Register token flat positions: row < kc OR col < kn (closed-form without GPU-host sync)
        row_part = torch.arange(kc * N_aug, device=device)
        r_idx = torch.arange(kc, C_aug, device=device).unsqueeze(1)
        c_idx = torch.arange(kn, device=device).unsqueeze(0)
        col_part = (r_idx * N_aug + c_idx).reshape(-1)
        reg_flat_idx = torch.cat([row_part, col_part])
        L_reg = int(reg_flat_idx.numel())

        # Map kept patch index p in [0, C*N) -> (c + kc, n + kn) in (C_aug, N_aug)
        keep_c = (ids_keep // N) + kc
        keep_n = (ids_keep % N) + kn
        keep_aug_idx = keep_c * N_aug + keep_n  # [B, K_vis]

        ids_enc = torch.cat(
            [reg_flat_idx.unsqueeze(0).expand(B, -1), keep_aug_idx], dim=1
        )  # [B, L_reg + K_vis]

        gather_idx = ids_enc.unsqueeze(-1).expand(-1, -1, D_enc)
        x_enc = torch.gather(flat_grid, dim=1, index=gather_idx)
        var_id_enc = torch.gather(var_id_full, dim=1, index=ids_enc)
        time_id_enc = torch.gather(time_id_full, dim=1, index=ids_enc)

        attn_mask_enc = None
        if self._is_padded_batch(data_info_list):
            tok_valid_aug = real_data_token_mask(
                data_info_list, N_aug, device, n_register_c=kc, n_register_n=kn
            ).reshape(B, C_aug * N_aug)
            valid_enc = torch.gather(tok_valid_aug, dim=1, index=ids_enc)  # [B, L_enc]
            attn_mask_enc = valid_enc.unsqueeze(2) & valid_enc.unsqueeze(1)

        # Core Moirai Transformer stack over ONLY [B, L_reg + K_vis, D_enc]
        z_enc = self.encoder.encoder(
            x_enc, attn_mask_enc, time_id=time_id_enc, var_id=var_id_enc
        )

        if getattr(self.encoder, "_uses_coords", False):
            self.encoder._clear_coords()

        z_vis = z_enc[:, L_reg:, :]  # [B, K_vis, D_enc]

        sparse_flat = torch.zeros(B, C_aug * N_aug, D_enc, dtype=z_enc.dtype, device=device)
        sparse_flat.scatter_(1, gather_idx, z_enc)
        return z_vis, sparse_flat.view(B, C_aug, N_aug, D_enc)

    def _decode_all_patches(
        self,
        z_vis: torch.Tensor,
        ids_keep: torch.Tensor,
        C: int,
        N: int,
        real_patch_valid: Optional[torch.Tensor],
        data_info_list=None,
    ) -> torch.Tensor:
        """Re-insert `[MASK]` tokens + 3D/modality embeddings and run shallow Moirai decoder."""
        B, K_vis, _ = z_vis.shape
        L = C * N
        device = z_vis.device

        z_vis_dec = self.enc_to_dec(z_vis)  # [B, K_vis, D_dec]
        dec_dtype = z_vis_dec.dtype

        # Fill full [B, C*N, D_dec] with learnable [MASK] token, then overwrite visible slots
        dec_tokens = self.decoder_mask_token.to(dec_dtype).expand(B, L, -1).clone()
        scatter_idx = ids_keep.unsqueeze(-1).expand(-1, -1, self.decoder_d_model)
        dec_tokens.scatter_(1, scatter_idx, z_vis_dec)
        dec_grid = dec_tokens.view(B, C, N, self.decoder_d_model)

        # Add pure metadata 3D MNI + modality/subtype embedding (no raw signal touched)
        dec_grid = self.decoder_pos_embed(dec_grid, data_info_list=data_info_list)

        dec_seq = dec_grid.reshape(B, L, self.decoder_d_model)
        var_id_dec = torch.repeat_interleave(
            torch.arange(C, device=device), repeats=N
        ).expand(B, -1)
        time_id_dec = torch.tile(
            torch.arange(N, device=device), (C,)
        ).expand(B, -1)

        attn_mask_dec = None
        if real_patch_valid is not None:
            q_valid = real_patch_valid.reshape(B, L)
            attn_mask_dec = q_valid.unsqueeze(2) & q_valid.unsqueeze(1)

        dec_out = self.decoder(
            dec_seq, attn_mask_dec, time_id=time_id_dec, var_id=var_id_dec
        )
        return dec_out.view(B, C, N, self.decoder_d_model)

    def forward(
        self,
        x: torch.Tensor,
        data_info_list=None,
        x_mark=None,
        y_mark=None,
        use_mask: Optional[bool] = None,
        return_embedding_output: bool = False,
        return_encoder_output: bool = False,
    ):
        assert use_mask is not None, "use_mask must be specified in the forward call."

        # Inference / iMindBench linear probe (`use_mask=False`):
        # Bypass decoder completely (0 overhead) and return standard full-grid encoder features.
        if not use_mask:
            return super().forward(
                x,
                data_info_list=data_info_list,
                x_mark=x_mark,
                y_mark=y_mark,
                use_mask=False,
                return_embedding_output=return_embedding_output,
                return_encoder_output=return_encoder_output,
            )

        # Pretraining (`use_mask=True`): True Asymmetric Encoder-Decoder MAE
        x = self._transform_input_format(x)
        return_dict = {}

        with record_function("patcher"):
            x_patched = self.patcher(x)
            return_dict["x_patched"] = x_patched.clone()

        B, C, N, P = x_patched.shape
        ids_keep, mask, real_patch_valid = self._sample_visible_and_mask(
            B, C, N, x_patched.device, data_info_list=data_info_list, token_len=P
        )

        # Multiply by (1 - mask) BEFORE `self.embedding` so masked raw patches have
        # strictly zero forward value AND zero backward gradient into visible tokens
        # even when `timewise_reduced_stcpe` is present in `self.embedding`.
        keep_gate = (1.0 - mask).unsqueeze(-1).to(x_patched.dtype)
        masked_x = x_patched * keep_gate

        with record_function("embedding"):
            emb_grid = self.embedding(masked_x, data_info_list=data_info_list)
            return_dict["embedding_output"] = emb_grid.clone() if return_embedding_output else None

        with record_function("token_prepend"):
            full_grid = self.token_manager.prepend_x_with_tokens(
                emb_grid, **self.token_prepend_config
            )

        with record_function("asymmetric_encoder_visible_only"):
            z_vis, sparse_full_out = self._encode_visible_only(
                full_grid, ids_keep, C, N, data_info_list=data_info_list
            )
            return_dict["encoder_output"] = sparse_full_out.clone() if return_encoder_output else None

        with record_function("token_extract"):
            token_outputs = self.token_manager.extract_prepended_x(sparse_full_out)
            return_dict["token_manager_output"] = token_outputs

        with record_function("asymmetric_decoder"):
            dec_out = self._decode_all_patches(
                z_vis, ids_keep, C, N, real_patch_valid, data_info_list=data_info_list
            )

        return_dict["y"] = self.heads["main"](
            token_outputs[self.token_prepend_head_to_what], data_info_list=data_info_list
        )
        if "n" in self.heads:
            return_dict["y_n"] = self.heads["n"](
                token_outputs["n_position_features"], data_info_list=data_info_list
            )
        if "c" in self.heads:
            return_dict["y_c"] = self.heads["c"](
                token_outputs["c_position_features"], data_info_list=data_info_list
            )
        if "nc" in self.heads:
            return_dict["y_nc"] = self.heads["nc"](
                token_outputs["nc_position_features"], data_info_list=data_info_list
            )
        if "org" in self.heads:
            with record_function("head_org_from_decoder"):
                return_dict["y_org"] = self.heads["org"](dec_out, data_info_list=data_info_list)

        return_dict["mask"] = mask
        return return_dict


def build_diver_asym_mae_config(
    d_model: int = 512,
    e_layers: int = 12,
    mup: bool = False,
    patch_size: int = 500,
    mask_ratio: float = 0.75,
    decoder_d_model: int = 256,
    decoder_e_layers: int = 2,
) -> Config:
    """Build `DIVER_iEEG_ASYM_MAE_model` config by extending a fresh `DIVER_iEEG_FINAL_model`."""
    from config.cfg import Experiments

    # `DIVER_iEEG_FINAL_model` constructs a fresh Config object each call;
    # avoid `copy.deepcopy` because `cfg.py`'s `__getattr__` does not guard `self.params`.
    cfg = Experiments.DIVER_iEEG_FINAL_model(
        d_model=d_model, e_layers=e_layers, mup=mup, patch_size=patch_size
    )
    cfg.basemodel.type = "asymmetric_multi_head_mae"
    cfg.basemodel.params["mask_ratio"] = mask_ratio
    cfg.basemodel.params["decoder_d_model"] = decoder_d_model
    cfg.basemodel.params["decoder_e_layers"] = decoder_e_layers
    cfg.basemodel.params["decoder_n_heads"] = max(1, decoder_d_model // 32)
    return cfg


def register_with_diver2() -> None:
    """Non-invasive runtime registration into `DIVER-2/diver_pretrain` (`Experiments` + `build_model`).

    Call `register_with_diver2()` once at the top of `pretrain_main.py` (and `imindbench`
    upstream loader if evaluating custom `model_config` names) to unlock:
      - `--model_config DIVER_iEEG_ASYM_MAE_model`        (mask_ratio=0.75, dec d256 L2)
      - `--model_config DIVER_iEEG_ASYM_MAE_mask50_model` (mask_ratio=0.50, controlled match to stock)
    """
    import src.models.diver as diver_mod
    from config.cfg import Experiments
    from src.models.components import create_embedding, create_encoder, create_head

    if getattr(diver_mod, "_asym_mae_registered", False):
        return

    orig_build_model = diver_mod.build_model

    def patched_build_model(configs):
        if getattr(configs.basemodel, "type", None) == "asymmetric_multi_head_mae":
            embedding_type = getattr(configs.embedding, "type", "identity")
            encoder_type = getattr(configs.encoder, "type", "identity")
            head_type = getattr(configs.head, "type", "identity")

            model = AsymmetricMultiHeadMAEModel(configs)
            model.embedding = create_embedding(embedding_type, configs.embedding)
            model.encoder = create_encoder(encoder_type, configs.encoder)
            for enc_mod in [model.encoder] + list(model.encoder.modules()):
                if hasattr(enc_mod, "layers"):
                    enc_mod._diver_main_encoder = True
            model.head = create_head(head_type, configs.head)
            return model
        return orig_build_model(configs)

    diver_mod.build_model = patched_build_model
    diver_mod.AsymmetricMultiHeadMAEModel = AsymmetricMultiHeadMAEModel
    diver_mod._asym_mae_registered = True

    Experiments.DIVER_iEEG_ASYM_MAE_model = staticmethod(
        lambda d_model=512, e_layers=12, mup=False, patch_size=500: build_diver_asym_mae_config(
            d_model=d_model,
            e_layers=e_layers,
            mup=mup,
            patch_size=patch_size,
            mask_ratio=0.75,
            decoder_d_model=max(128, d_model // 2),
            decoder_e_layers=2,
        )
    )
    Experiments.DIVER_iEEG_ASYM_MAE_mask50_model = staticmethod(
        lambda d_model=512, e_layers=12, mup=False, patch_size=500: build_diver_asym_mae_config(
            d_model=d_model,
            e_layers=e_layers,
            mup=mup,
            patch_size=patch_size,
            mask_ratio=0.50,
            decoder_d_model=max(128, d_model // 2),
            decoder_e_layers=2,
        )
    )


def export_imindbench_compat_checkpoint(src_ckpt_path: str, dst_ckpt_path: Optional[str] = None) -> str:
    """Export an Asymmetric MAE checkpoint as a `strict=True` stock `DIVER_iEEG_FINAL_model` checkpoint.

    Why this matters:
      Downstream `imindbench` (`litmus.sh` / `run_suite.py`) runs with `use_mask=False`,
      which ONLY executes `patcher -> embedding -> token_manager -> encoder` and never
      uses the reconstruction decoder or `heads['org']`. Because `AsymmetricMultiHeadMAEModel`
      preserves 100% identical key names and tensor shapes for the encoder/embedding/register
      backbone, stripping decoder keys and restoring dummy-shaped `heads.org.*` entries lets
      stock `imindbench` evaluate the checkpoint with ZERO code edits to `imindbench` or `torch_brain`.
    """
    from pathlib import Path
    from config import cfg_model_utils
    import src.models.diver as diver_mod

    src_path = Path(src_ckpt_path).resolve()
    if dst_ckpt_path is None:
        dst_path = src_path.with_name(f"{src_path.stem}_imindbench_compat{src_path.suffix}")
    else:
        dst_path = Path(dst_ckpt_path).resolve()

    ckpt = torch.load(src_path, map_location="cpu", weights_only=False)
    saved_args = dict(ckpt.get("args", {}))

    # Strip DDP module. prefix if present
    raw_sd = ckpt["model_state_dict"]
    asym_sd = {
        (k[7:] if k.startswith("module.") else k): v
        for k, v in raw_sd.items()
    }

    # Auto-infer width from backbone state dict if missing or default
    if "encoder.encoder.norm.weight" in asym_sd:
        width = asym_sd["encoder.encoder.norm.weight"].shape[0]
    elif "width" in saved_args:
        width = saved_args["width"]
    else:
        width = 512

    # Auto-infer depth from backbone layers if missing or default
    layer_indices = [
        int(k.split("encoder.encoder.layers.")[1].split(".")[0])
        for k in asym_sd
        if "encoder.encoder.layers." in k and k.split("encoder.encoder.layers.")[1].split(".")[0].isdigit()
    ]
    if layer_indices:
        depth = max(layer_indices) + 1
    elif "depth" in saved_args:
        depth = saved_args["depth"]
    else:
        depth = 12

    stock_cfg = cfg_model_utils.get_model_config(
        "DIVER_iEEG_FINAL_model", width=width, depth=depth, mup=False
    )
    if not hasattr(stock_cfg.embedding, "stcpe_mask_padding"):
        stock_cfg.embedding.stcpe_mask_padding = True

    stock_ref = diver_mod.build_model(stock_cfg)
    stock_sd = stock_ref.state_dict()

    decoder_only_prefixes = (
        "enc_to_dec.",
        "decoder_mask_token",
        "decoder_pos_embed.",
        "decoder.",
    )
    rebuilt_sd = {}
    copied_backbone_keys = 0
    for k, ref_tensor in stock_sd.items():
        if k.startswith("heads.org."):
            # Unused during `use_mask=False` downstream probing; keep stock shape for strict=True loading.
            rebuilt_sd[k] = ref_tensor
        else:
            if k not in asym_sd:
                raise KeyError(f"Missing required backbone key in Asymmetric MAE checkpoint: {k}")
            if tuple(asym_sd[k].shape) != tuple(ref_tensor.shape):
                raise ValueError(
                    f"Backbone shape mismatch on {k}: asym={tuple(asym_sd[k].shape)} vs stock={tuple(ref_tensor.shape)}"
                )
            rebuilt_sd[k] = asym_sd[k]
            copied_backbone_keys += 1

    # Verify zero unexpected non-decoder keys were silently dropped
    for k in asym_sd:
        if not k.startswith(decoder_only_prefixes) and not k.startswith("heads.org.") and k not in rebuilt_sd:
            raise KeyError(f"Unexpected non-decoder key in Asymmetric MAE state_dict: {k}")

    # Sanity-check strict=True load right now
    stock_ref.load_state_dict(rebuilt_sd, strict=True)

    saved_args["orig_asym_model_config"] = saved_args.get("model_config", "DIVER_iEEG_ASYM_MAE_model")
    saved_args["model_config"] = "DIVER_iEEG_FINAL_model"

    compat_ckpt = {
        "format_version": ckpt.get("format_version", 3),
        "epoch": ckpt.get("epoch", 0),
        "global_step": ckpt.get("global_step", 0),
        "best_loss": ckpt.get("best_loss", float("nan")),
        "model_state_dict": rebuilt_sd,
        "ssl_method": ckpt.get("ssl_method", "MAEMultiHead_onlypatchwise"),
        "metric": ckpt.get("metric", float("nan")),
        "args": saved_args,
        "copied_backbone_keys": copied_backbone_keys,
    }
    tmp_path = dst_path.with_suffix(dst_path.suffix + ".tmp")
    torch.save(compat_ckpt, tmp_path)
    tmp_path.replace(dst_path)
    return str(dst_path)

