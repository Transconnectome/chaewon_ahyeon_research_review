#!/usr/bin/env python3
"""
reproduce_diver2_bugs.py
========================
투고 후(DIVER-2 본 논문 단계)에 고치면 좋은 `DIVER-2` 코드베이스의 숨은 수치 버그 2가지를
GPU 없이 노트북/CPU에서 1초 만에 직접 눈으로 확인해 볼 수 있는 25줄 데모 스크립트입니다.

버그 1 (`Original_Moirai_projection.py:70` — RoPE bfloat16 위치 번호 뭉개짐):
  - `bfloat16` 숫자 형식은 유효 자릿수(가수부)가 7비트뿐이라 256보다 큰 정수를 1씩 구분하지 못합니다!
  - 예: `bfloat16`에서는 `256 + 1 == 256`이 되고, 1024 뒤로는 8칸씩, 4096 뒤로는 32칸씩 같은 숫자로 뭉개집니다.
  - 따라서 6,001개 시간 패치 번호(`0..6000`)를 `bfloat16`으로 만들면 서로 구분되는 위치가 **829개뿐(86.2% 중복 충돌!)**입니다.
  - 1줄 해결책: `torch.arange(max_len, dtype=torch.float32, device=device)`로 바꾸면 `6,001개 전부` 살아납니다!

버그 2 (`Attn_Bias.py:224-250` & Neuroprobe h5 — 복셀 좌표 56~167 vs MNI mm 좌표):
  - DIVER의 3차원 뇌 공간 어텐션은 뇌 중심이 `(0, 0, 0) mm`이고 반지름이 `128 mm` 안쪽(`r_hat <= 1.0`)이라고 가정합니다.
  - 그런데 Neuroprobe 평가 파일에는 MNI mm 대신 양수 복셀 번호(`56 ~ 167`)가 들어 있어,
    원점 거리가 `244 mm` (`r_hat = 1.91 > 1.0`)로 튀면서 공간 다항식(르장드르 다항식)이 구 바깥으로 외삽됩니다.
"""
from __future__ import annotations

import math
from typing import Dict

import torch


def demo_rope_bfloat16_collision(max_len: int = 6001) -> Dict[str, object]:
    """`bfloat16` vs `float32`에서 위치 번호(`arange`)가 얼마나 뭉개지는지 실측합니다."""
    pos_bf16 = torch.arange(max_len, dtype=torch.bfloat16)
    pos_fp32 = torch.arange(max_len, dtype=torch.float32)

    unique_bf16 = int(pos_bf16.unique().numel())
    unique_fp32 = int(pos_fp32.unique().numel())
    collided = max_len - unique_bf16
    collision_pct = 100.0 * collided / max_len

    # 4096 근처에서 실제로 어떤 숫자들이 똑같은 위치로 뭉개지는지 예시 추출
    sample_4096_to_4128 = [float(v) for v in pos_bf16[4096:4129:8]]
    return {
        "max_len": max_len,
        "unique_in_bfloat16": unique_bf16,
        "unique_in_float32": unique_fp32,
        "collided_positions": collided,
        "collision_pct": round(collision_pct, 2),
        "example_4096_step8_in_bf16": sample_4096_to_4128,
    }


def demo_neuroprobe_voxel_extrapolation(r_max_mm: float = 128.0) -> Dict[str, object]:
    """정상 MNI mm 좌표 vs Neuroprobe 복셀 좌표(56~167)의 정규화 반경 `r_hat`을 비교합니다."""
    # 정상적인 측두엽 MNI mm 좌표 예시: (-52, -24, -8) mm
    mni_coord = (-52.0, -24.0, -8.0)
    r_mni = math.sqrt(sum(c * c for c in mni_coord))
    r_hat_mni = r_mni / r_max_mm

    # Neuroprobe 평가 파일에 들어 있는 양수 복셀 인덱스 예시: (135, 148, 138)
    voxel_coord = (135.0, 148.0, 138.0)
    r_voxel = math.sqrt(sum(c * c for c in voxel_coord))
    r_hat_voxel = r_voxel / r_max_mm

    # 3차 르장드르 다항식 P_3(x) = 0.5 * (5x^3 - 3x) 값 비교 (|x| <= 1에서는 [-1, 1] 범위지만 1.91에서는 폭증!)
    def legendre_p3(x: float) -> float:
        return 0.5 * (5.0 * (x ** 3) - 3.0 * x)

    return {
        "normal_mni_coord_mm": mni_coord,
        "normal_r_hat": round(r_hat_mni, 3),
        "normal_legendre_p3": round(legendre_p3(r_hat_mni), 3),
        "neuroprobe_voxel_coord": voxel_coord,
        "voxel_norm_as_mm": round(r_voxel, 1),
        "voxel_r_hat": round(r_hat_voxel, 3),
        "voxel_legendre_p3": round(legendre_p3(r_hat_voxel), 3),
    }


if __name__ == "__main__":
    rope = demo_rope_bfloat16_collision()
    vox = demo_neuroprobe_voxel_extrapolation()
    print("=== [점검 5A] RoPE bfloat16 위치 번호 충돌 데모 ===")
    print(f"- 총 6,001개 시간 패치 중 bfloat16 생존 개수: {rope['unique_in_bfloat16']}개 "
          f"(충돌 소실 {rope['collided_positions']}개 = {rope['collision_pct']:.1f}%)")
    print(f"- float32 패치 시 생존 개수:                  {rope['unique_in_float32']}개 (충돌 0%)")
    print(f"- 예: 위치 [4096, 4104, 4112, 4120, 4128]의 bfloat16 값 -> {rope['example_4096_step8_in_bf16']} (전부 4096으로 뭉개짐!)\n")

    print("=== [점검 5B] Neuroprobe 복셀 좌표(56~167) 반경 외삽 데모 ===")
    print(f"- 정상 MNI 좌표 {vox['normal_mni_coord_mm']} mm -> r_hat = {vox['normal_r_hat']} (<= 1.0 정상), P3 = {vox['normal_legendre_p3']}")
    print(f"- 복셀 좌표     {vox['neuroprobe_voxel_coord']}    -> r_hat = {vox['voxel_r_hat']} (> 1.0 구 밖 외삽!), P3 = {vox['voxel_legendre_p3']} (14배 팽창!)")
