#!/usr/bin/env python3
"""
check_pr_pc90_and_layers.py
===========================
안채원 선생님·이아현 선생님의 유효 차원(`effdim2_summary.json`)과
읽는 층 비교(`small46_summary.json`, `d2rdall_summary.json`)를 점검하는 스크립트입니다.

핵심 발견 2가지:
1. 초안(`draft_user_20261109.md:98, 111`)의 지표 이름 혼동 정정:
   - 초안에 `"학습 후 PR이 줄었다(55 -> 28)"`, `"PR 기준으로 입력 15.3 -> 미학습 [?] -> 학습 후 4~6"`이라고 적혀 있는데,
   - 실제 `effdim2_summary.json`을 보면 **`54.7 -> 28.1`로 줄어든 것은 `PR`이 아니라 `90% 분산을 설명하는 주성분 개수(PC90_z)`**입니다!
   - 반면 풀링된 `PR(pooled.pr_z)`은 **학습 안 한 모델(`scratch`)도 이미 `5.01 ± 1.47`**이고, 전체 학습 후(`Base`)도 `5.42 ± 0.42`로 거의 같습니다.
     (뇌파 자체가 1/f 저주파 큰 기둥 몇 개가 분산을 지배하기 때문에, `PR`은 큰 기둥 5개만 보고 `PC90`은 잔가지 축이 정리되는 것을 보여줍니다!
     또한 `15.28`은 251차원 주파수 스펙트럼 `input_spec`의 PR이라서 512차원 임베딩과 한 화살표로 이으면 차원 공간이 다릅니다.)
2. 1층(`rd1`) vs 마지막 층(`rdall`) 결과 해석:
   - `1/64 (81시간, 295회 반복)`: 2층 Base와 12층 Small 모두 **마지막 층까지 완벽히 유지**(`Small rdall -0.0006`, 유지)!
   - `1/1024 (5시간, 4,704회 반복)`: 1층(`rd1`)은 유지(`+0.0003`)되지만 **12층(`rdall`)은 `-0.0050 [-0.0072, -0.0028]`로 6개 시드 전원 하락(깨짐)**!
   - 이유: 현재 DIVER는 별도 디코더가 없어 마지막 12층이 바로 파형 복원 시험을 치릅니다. 613개 클립을 4,704번 반복하면
     12층이 그 613개 파형을 외워버리기 때문(`train_loss 0.080` vs `Base 0.096`)이며, 1층은 사람마다 공통인 기본 시간-주파수 필터만 뽑아 안 망가집니다.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple

import numpy as np


EMBEDDED_EFFDIM2_GROUPS = {
    "input_spec_251d": {"pr_z": [15.28, 0.0], "pc90_z": [121.60, 0.0]},
    "scratch": {"pr_z": [5.01, 1.47], "pc90_z": [54.73, 10.33], "sketch_pr_z": [136.84, 21.75]},
    "R1024":   {"pr_z": [7.35, 1.67], "pc90_z": [49.23, 4.71],  "sketch_pr_z": [102.56, 8.35]},
    "R256":    {"pr_z": [5.82, 0.62], "pc90_z": [33.08, 3.01],  "sketch_pr_z": [91.67, 5.59]},
    "R1.5625": {"pr_z": [5.81, 0.47], "pc90_z": [30.15, 2.88],  "sketch_pr_z": [86.34, 2.45]},
    "Base":    {"pr_z": [5.42, 0.42], "pc90_z": [28.05, 1.59],  "sketch_pr_z": [86.32, 1.43]},
    "F1.5625": {"pr_z": [10.68, 0.85], "pc90_z": [37.93, 1.43], "sketch_pr_z": [97.62, 16.39]},
}

EMBEDDED_READOUT_LAYERS = {
    "Base_d2_9.4M": {
        "1/64_rd1":   [-0.0004, -0.0019, +0.0012, "유지"],
        "1/64_rdall": [-0.0000, -0.0020, +0.0019, "유지"],
        "1/1024_rd1":   [+0.0006, -0.0012, +0.0024, "유지"],
        "1/1024_rdall": [-0.0029, -0.0063, +0.0005, "판정 불가"],
    },
    "Small_d12_51.4M": {
        "1/64_rd1":   [-0.0004, -0.0026, +0.0017, "유지"],
        "1/64_rdall": [-0.0006, -0.0021, +0.0008, "유지"],
        "1/1024_rd1":   [+0.0003, -0.0014, +0.0021, "유지"],
        "1/1024_rdall": [-0.0050, -0.0072, -0.0028, "깨짐"],
    },
}


def compute_pr_and_pc90(features: np.ndarray, standardize: bool = True) -> Tuple[float, int]:
    """
    `effdim2/one.py`와 100% 동일한 유효 차원(PR) 및 90% 주성분 개수(PC90) 계산 함수입니다.
    features: (N_samples, D_features) 2차원 배열
    """
    x = np.asarray(features, dtype=np.float64)
    if standardize:
        sd = x.std(axis=0)  # 각 뉴런(열)의 표준편차
        keep = sd > 1e-12
        x = (x[:, keep] - x[:, keep].mean(axis=0)) / sd[keep]
    else:
        x = x - x.mean(axis=0)

    # 공분산 행렬의 고유값(각 주성분 축이 가진 분산 크기)을 큰 순서대로 정렬
    eigvals = np.clip(np.linalg.eigvalsh(np.cov(x, rowvar=False)), 0.0, None)[::-1]
    total_var = float(eigvals.sum())
    # 1) Participation Ratio (PR): 큰 고유값 몇 개가 지배하면 작아짐 (제곱합 분모 때문)
    pr = float((total_var ** 2) / (eigvals ** 2).sum())
    # 2) PC90: 누적 분산 비율이 90%를 넘는 데 필요한 주성분 개수 (작은 잡음 축까지 얼마나 남아 있는지 민감하게 포착)
    cum_ratio = np.cumsum(eigvals) / total_var
    pc90 = int(np.searchsorted(cum_ratio, 0.90) + 1)
    return pr, pc90


def audit_effdim_and_layers(hangang_dir: Path | None = None) -> Dict[str, object]:
    """`effdim2_summary.json`, `small46_summary.json`, `d2rdall_summary.json` 수치를 검증합니다."""
    groups = dict(EMBEDDED_EFFDIM2_GROUPS)
    layers = dict(EMBEDDED_READOUT_LAYERS)

    if hangang_dir is not None:
        eff2_p = hangang_dir / "reports/lead/effdim2_summary.json"
        sm46_p = hangang_dir / "reports/lead/small46_summary.json"
        d2rd_p = hangang_dir / "reports/lead/d2rdall_summary.json"
        if eff2_p.is_file():
            eff2 = json.loads(eff2_p.read_text(encoding="utf-8"))
            spec = eff2["per_model"]["Base_s1"]["input_spec"]
            groups["input_spec_251d"] = {"pr_z": [round(spec["pr_z"], 2), 0.0], "pc90_z": [round(spec["pc90_z"], 2), 0.0]}
            for g in ("scratch", "R1024", "R256", "R1.5625", "Base", "F1.5625"):
                gd = eff2["groups"][g]
                groups[g] = {
                    "pr_z": [round(gd["pooled.pr_z"][0], 2), round(gd["pooled.pr_z"][1], 2)],
                    "pc90_z": [round(gd["pooled.pc90_z"][0], 2), round(gd["pooled.pc90_z"][1], 2)],
                    "sketch_pr_z": [round(gd["sketch.pr_z"][0], 2), round(gd["sketch.pr_z"][1], 2)],
                }
        if sm46_p.is_file() and d2rd_p.is_file():
            sm46 = json.loads(sm46_p.read_text(encoding="utf-8"))
            d2rd = json.loads(d2rd_p.read_text(encoding="utf-8"))
            layers["Base_d2_9.4M"] = {
                "1/64_rd1": d2rd["R1.5625 - Base rule3 | rd1 (first block)"][:4],
                "1/64_rdall": d2rd["R1.5625 - Base rule3 | rdall (last block)"][:4],
                "1/1024_rd1": d2rd["R0.09765625 - Base rule3 | rd1 (first block)"][:4],
                "1/1024_rdall": d2rd["R0.09765625 - Base rule3 | rdall (last block)"][:4],
            }
            layers["Small_d12_51.4M"] = {
                "1/64_rd1": sm46["rd1 R1.5625 - Base rule3"][:4],
                "1/64_rdall": sm46["rdall R1.5625 - Base rule3"][:4],
                "1/1024_rd1": sm46["rd1 R0.09765625 - Base rule3"][:4],
                "1/1024_rdall": sm46["rdall R0.09765625 - Base rule3"][:4],
            }

    # 직관 확인용 합성 예제: 큰 축 5개는 그대로 두고 나머지 507개 작은 잡음 축만 줄였을 때 PR vs PC90 변화 시연
    rng = np.random.default_rng(42)
    head = rng.normal(size=(1000, 5)) * np.array([6.0, 5.0, 4.5, 4.0, 3.5])
    noisy_tail = rng.normal(size=(1000, 75)) * 0.85
    clean_tail = rng.normal(size=(1000, 75)) * 0.35
    toy_before = compute_pr_and_pc90(np.hstack([head, noisy_tail]), standardize=False)
    toy_after = compute_pr_and_pc90(np.hstack([head, clean_tail]), standardize=False)

    return {
        "effdim2_groups": groups,
        "readout_layers": layers,
        "toy_demo_noise_cleanup": {
            "before_cleanup_pr_pc90": [round(toy_before[0], 2), toy_before[1]],
            "after_cleanup_pr_pc90": [round(toy_after[0], 2), toy_after[1]],
        },
    }


if __name__ == "__main__":
    res = audit_effdim_and_layers(Path("/home/juke/git/chaewon-intern-2026fall/hangang"))
    print("=== [점검 4A] 유효 차원: 왜 'PR'이 아니라 '90% 주성분 개수(PC90)'가 55 -> 28로 줄었나? ===")
    for name, vals in res["effdim2_groups"].items():
        print(f"  {name:<16}: pooled PR_z = {vals['pr_z'][0]:5.2f} ± {vals['pr_z'][1]:4.2f} | "
              f"pooled PC90_z = {vals['pc90_z'][0]:6.2f} ± {vals['pc90_z'][1]:5.2f}")
    print("\n=== [점검 4B] 읽는 층 비교 (n=6 시드): 1/64는 전 층 유지, 1/1024는 마지막 층만 붕괴 ===")
    for model_name, conds in res["readout_layers"].items():
        for cond, (m, lo, hi, v) in conds.items():
            print(f"  {model_name:<16} | {cond:<12}: Δ = {m:+.4f} [{lo:+.4f}, {hi:+.4f}] -> {v}")
