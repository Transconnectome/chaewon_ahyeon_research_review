# True Asymmetric Encoder-Decoder MAE for DIVER-2 iEEG (`code/asymmetric_mae`)

> **작성 목적**: **차지욱 교수님**께서 지적하신 핵심 구조적 쟁점(`"현행 DIVER MAE는 He et al. (2022) 비대칭 인코더-디코더 MAE가 아니라 단일 인코더 마스크 패치 예측기(SimMIM/BERT식)이다"`)을 **안채원 선생님**과 **이아현 선생님**께서 KISTI 한강 클러스터(`DIVER-2/diver_pretrain` 및 `imindbench`)에서 원본 저장소 수정 없이 즉시 실증 실험하실 수 있도록 구현 및 검증한 드롭인(drop-in) 모듈입니다.

---

## 1. 왜 단일 인코더 패치 예측을 비대칭 MAE로 분리해야 하는가?

기존 `DIVER_iEEG_FINAL_model` (`MultiHeadPrependPatchMaskedModel`)은 이름은 `MAEMultiHead_onlypatchwise`이지만 실제 코드(`src/models/diver.py`)상 다음 두 가지 병목을 갖습니다:

1. **마스킹 토큰의 인코더 유입**: 50% 마스킹된 패치를 0으로 치환(`masked_x[mask == 1] = 0`)한 뒤 **메인 인코더 전체 층에 그대로 통과**시킵니다. 이로 인해 연산량을 낭비할 뿐 아니라 학습 시점(50% 0-패치 혼합)과 하류 평가 시점(`use_mask=False`, 100% 실제 신호) 사이에 분포 불일치가 발생합니다.
2. **디코더 부재로 인한 상위 층 파형 복원 강제**: 별도 디코더 없이 인코더 최상위 층 출력(`org_x_position_features`)에 선형 헤드(`heads['org']`: 시간 파형 + 다중스케일 STFT 진폭 + FFT 진폭)를 직접 연결합니다. 그 결과 Small(12-layer) 모델의 **Layer 12가 고수준 신경 상태 추상화 대신 $1/f$ 저주파 파형 보간기에 묶여 1/1024 조건에서 `-0.0050` 표상 붕괴**를 일으키는 직접적 원인이 됩니다.

본 모듈의 `AsymmetricMultiHeadMAEModel`은 **He et al. (CVPR 2022)**의 비대칭 설계를 DIVER의 3D 전극 좌표 및 Moirai 채널-시간 어텐션 위에 정확히 이식합니다:

- **Zero-Leakage Visible-Only Encoder**: 마스킹된 패치를 `self.embedding` 진입 전에 게이팅(`x_patched * (1 - mask)`)하여 `timewise_reduced_stcpe` 이웃 누수를 원천 차단(`max diff == 0.0` 검증 완료)하고, 메인 Moirai 인코더에는 **레지스터 토큰 + 가시(unmasked) 패치(`25%` 또는 `50%`)만 물리적으로 추출(`torch.gather`)**하여 입력합니다. 이때 원래의 채널 인덱스(`var_id`)와 시간 인덱스(`time_id`)를 함께 전달하므로 `BinaryAttentionBias`와 `RotaryProjection(RoPE)`이 오차 없이 작동합니다.
- **Lightweight Asymmetric Moirai Decoder**: 인코더가 출력한 가시 잠재벡터만 `d_model -> decoder_d_model(256)`로 투영한 뒤, 마스킹 위치에 학습 가능한 `[MASK]` 토큰(`decoder_mask_token`)과 순수 메타데이터 기반 **3D MNI 전극 좌표 + 모달리티 임베딩**을 더하여 얕은 **2-layer Moirai 디코더**에서 파형·STFT·FFT 복원을 전담시킵니다.
- **Zero-Edit `imindbench` 완벽 호환**: 하류 평가(`use_mask=False`) 시 디코더는 완전히 우회되며(추가 연산 `0`), `--export_eval_compat_ckpt` 옵션이 생성하는 `last_imindbench_compat.pt` 체크포인트는 기존 `imindbench` (`litmus_stack.sh` / `run_suite.py`)에서 **단 한 줄의 코드 수정 없이 `strict=True`로 즉시 로드 및 평가**됩니다.

---

## 2. 핵심 알고리즘 의사코드 (25-Line Core Pseudocode)

```python
# Input: raw iEEG x [B, C, T], 3D electrode metadata info (xyz MNI, modality)
x_patched = patcher(x)                                 # [B, C, N, P=500]
ids_keep, mask = sample_visible(B, C, N, ratio=0.75)   # K_vis = round(0.25 * C * N)

# 1) Gate BEFORE STCPE embedding -> 0.0 neighbor signal leakage from masked patches
emb_grid  = embedding(x_patched * (1 - mask), info)    # [B, C, N, D_enc=512]
full_grid = token_manager.prepend_registers(emb_grid)  # [B, 1+C, 1+N, D_enc]

# 2) Visible-Only Main Moirai Encoder (4x fewer patch tokens, ~10-16x cheaper attention)
x_vis, var_vis, time_vis = gather_registers_and_visible(full_grid, ids_keep)
z_enc = main_moirai_encoder(x_vis, var_id=var_vis, time_id=time_vis)  # 12 layers, D=512
z_vis = extract_visible_latents(z_enc)                 # [B, K_vis, D_enc]

# 3) Lightweight Asymmetric Moirai Decoder (absorbs waveform + STFT + FFT reconstruction)
dec_tokens = mask_token.expand(B, C * N, D_dec)        # [B, C*N, D_dec=256]
dec_tokens.scatter_(dim=1, index=ids_keep, src=enc_to_dec(z_vis))
dec_grid   = dec_pos_embed_3d_xyz(dec_tokens.view(B, C, N, D_dec), info)
dec_out    = shallow_moirai_decoder(dec_grid)          # ONLY 2 layers, D=256

# 4) Multi-domain SSL loss ONLY on masked patches; at eval (use_mask=False), skip step 3-4!
y_pred = multi_linear_heads(dec_out)                   # time + multiscale STFT + FFT
loss   = masked_mse(y_pred, targets(x_patched), mask)
```

---

## 3. 파일 구성

| 파일 | 설명 |
|---|---|
| [asymmetric_mae.py](asymmetric_mae.py) | `AsymmetricMultiHeadMAEModel`, `register_with_diver2()`, `export_imindbench_compat_checkpoint()` 본체 구현 |
| [run_asym_mae_wrapper.py](run_asym_mae_wrapper.py) | `DIVER-2/diver_pretrain` 무수정 드롭인 실행기 (`torchrun` DDP 및 `--export_eval_compat_ckpt` 지원) |
| [test_asymmetric_mae_smoke.py](test_asymmetric_mae_smoke.py) | 7대 핵심 불변량 단위·통합 검증 스위트 (토큰 드롭 비율, 누수 0.0 검증, Muon/DDP 역전파, 패딩 배치, `rd1`/`rdall` 추론 동치, `strict=True` 체크포인트 변환, CLI E2E 학습·변환) |

---

## 4. 즉시 실행 가이드 (Quickstart for 안채원 선생님)

### Step 1: 5초 무결성 스모크 테스트 (CPU에서도 즉시 확인 가능)
```bash
export DIVER_PRETRAIN_ROOT=/path/to/DIVER-2/diver_pretrain
python3 code/asymmetric_mae/test_asymmetric_mae_smoke.py
```

### Step 2: KISTI 한강 클러스터 사전학습 실행 (`DIVER-2` 원본 코드 수정 불필요)
기존 `pretrain_main.py` 호출 자리만 `run_asym_mae_wrapper.py`로 바꾸고 `--model_config`와 `--export_eval_compat_ckpt`만 지정하시면 됩니다:

```bash
export DIVER_PRETRAIN_ROOT=/path/to/DIVER-2/diver_pretrain

# 조건 A: He et al. 표준 75% 마스킹 비대칭 MAE (권장 주력 모델)
torchrun --standalone --nproc_per_node=4 \
  /path/to/chaewon_ahyeon_research_review/code/asymmetric_mae/run_asym_mae_wrapper.py \
  --dataset_dir /path/to/ieeg_lmdb \
  --output_dir /path/to/runs/asym_mae_m75_small_d12_1_64_s42 \
  --model_config DIVER_iEEG_ASYM_MAE_model \
  --width 512 --depth 12 \
  --ssl_method MAEMultiHead_onlypatchwise \
  --input_was_resampled_and_padded_3sec True \
  --optimizer muon --lr 1e-3 --muon_lr 0.005 \
  --batch_size 64 --epochs 20 --seed 42 \
  --export_eval_compat_ckpt

# 조건 B: 마스킹 비율 통제 대조군 (기존 DIVER와 동일한 50% 마스킹 + 비대칭 디코더만 분리)
#   -> --model_config DIVER_iEEG_ASYM_MAE_mask50_model 로 변경
```

### Step 3: 하류 벤치마크(`imindbench`) 무수정 평가 (`rdall` vs `rd1`)
`--export_eval_compat_ckpt` 플래그가 `last_imindbench_compat.pt` (및 `best_imindbench_compat.pt`)를 자동 생성하므로 기존 `imindbench` 평가 스크립트에 그대로 넣으시면 됩니다:

```bash
# 최상위 층(Layer 12, rdall) 평가: 기존 단일 인코더에서 -0.0050 붕괴가 일어났던 핵심 검증 지점
DIVER_ENCODER_TRUNC="" bash litmus_stack.sh full \
  /path/to/runs/asym_mae_m75_small_d12_1_64_s42/last_imindbench_compat.pt control

# 얕은 층(Layer 1, rd1) 평가: 층별 읽기 분기(Layer Readout Divergence) 해소 여부 비교
DIVER_ENCODER_TRUNC="1" bash litmus_stack.sh full \
  /path/to/runs/asym_mae_m75_small_d12_1_64_s42/last_imindbench_compat.pt control
```

---

## 5. 사전 등록 최소 결정 실험 설계 (Minimal Decisive 3×3 Grid)

**안채원 선생님**께서 가장 적은 GPU 시간(Small `d12` 기준 KISTI 한강 약 15~25 GPU-h)으로 명확한 인과 결론을 얻으실 수 있는 핵심 비교표입니다:

| 아키텍처 조건 (`--model_config`) | 마스킹 비율 | 디코더 분리 여부 | 데이터 축 (`Full` / `1/64` / `1/1024`) | 핵심 판정 지표 (`Small d12`) |
|---|---|---|---|---|
| `DIVER_iEEG_FINAL_model` (기존 기준선) | 50% (0-치환 인코더 유입) | 없음 (단일 인코더) | `100%`, `1/64`, `1/1024` | `1/1024`에서 `rdall`(L12) `-0.0050` 붕괴 및 시간 스케일링 정체(`slope ≈ 0`) 재현 |
| `DIVER_iEEG_ASYM_MAE_mask50_model` | 50% (가시 토큰만 인코더 입력) | 2-layer Moirai (`d=256`) | `100%`, `1/64`, `1/1024` | **순수 디코더 분리 효과 검증**: 마스킹률을 50%로 고정했을 때 L12 표상 붕괴가 사라지는가? |
| `DIVER_iEEG_ASYM_MAE_model` (주력) | 75% (가시 25%만 인코더 입력) | 2-layer Moirai (`d=256`) | `100%`, `1/64`, `1/1024` | **진정한 비대칭 MAE 효과 검증**: (1) `rdall >= rd1` 역전 여부, (2) `100% > 1/64 > 1/1024` 양(+)의 시간 스케일링 기울기 출현 여부 |

### 칼 포퍼 반증 및 의사결정 규칙 (Pre-registered Decision Rule)
1. **가설 지지 (아키텍처 병목 가설 입증)**: `DIVER_iEEG_ASYM_MAE_model`에서 Small `d12`의 `rdall`(Layer 12) 점수가 `rd1`(Layer 1) 이상으로 회복되고 `100%` 대비 `1/1024` 격차가 벌어지면, 기존 `"시간 무관 포화(A Little iEEG Goes a Long Way)"` 현상의 상당 부분이 **단일 인코더 패치 복원기의 조기 포화 아티팩트**였음을 세계 최초로 규명하는 강력한 방법론+스케일링 논문이 됩니다.
2. **가설 기각 (신호 본질적 포화 재확증)**: 비대칭 인코더-디코더 분리(50% 및 75% 드롭) 후에도 `1/64`와 `100%`의 `rdall` 및 하류 점수가 여전히 비열등(`|Δ| < 0.002`)하다면, **이아현 선생님**과 **안채원 선생님**의 `"Subjects over Hours"` 결론은 **"단일 인코더 한계를 제거한 진정한 He et al. 비대칭 MAE에서도 불변하는 침습적 뇌신호의 근본 법칙"**으로 방어력이 한 단계 격상됩니다. 어떤 결과가 나오든 Win-Win입니다.
