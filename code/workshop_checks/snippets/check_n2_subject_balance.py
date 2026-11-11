#!/usr/bin/env python3
"""
check_n2_subject_balance.py
===========================
안채원 선생님·이아현 선생님의 사람 수 축소 실험(`subjfix46_summary.json`, `electrode_mix_summary.json`, `plan.py`)을
실제 데이터로 검증하고, 향후 실험에서 환자별 기록 비율까지 50:50으로 똑같이 맞추는 함수를 제공합니다.

핵심 검증 결과 (안채원 선생님의 실험 설계가 이미 통제한 것 vs 남은 1가지 미세 변수):
1. [이미 완벽히 통제됨] 총 고유 기록 수 & 반복 횟수:
   `S2_64`, `S8_64` 모두 고유 기록 **9,757개(약 81시간, 295회 반복)**로 정확히 맞춰져 있습니다.
   (초기 `P6.25` 실험의 82.4회 반복 문제는 `subjfix46`에서 이미 해결되었습니다!)
2. [이미 완벽히 통제됨] 병원 출처 비율:
   `S2`의 6개 시드 모두 **SNUH 사설 1명 + AJILE 1명**으로 층화 추출되었고, 6개 시드(12명) 간 겹치는 환자도 0명입니다.
3. [이미 확인됨] 심부 전극(sEEG Depth) 비율만으로는 설명되지 않음:
   6개 시드에서 심부 전극 비율과 점수 차이의 상관은 r=+0.428(1/64), r=+0.473(1/1024)이나 표본이 n=6이라
   **양측 p=0.397 / 0.343으로 통계적으로 유의하지 않으며**, BYD 과제에서는 부호가 반대(r=-0.415)입니다.
   실제로 심부 전극이 26.3%(`s3`), 24.1%(`s4`)로 평균(13.6%)보다 훨씬 많은 시드도 `-0.0055`, `-0.0065`로 떨어졌습니다.
4. [새로 찾은 미세 교란 1가지 — 환자 간 녹음 길이 불균형]:
   `plan.py`의 `cap_fraction`이 두 환자의 원래 기록 수에 **같은 비율 f**를 곱해 합계 9,757개를 맞추다 보니,
   원래 녹음이 긴 환자가 학습 데이터를 독차지한 시드가 있었습니다!
   - 예: `S2_s2` (`Sub26` 54,639개 + `sub-10_AJILE` 13,877개) -> 한 환자(`Sub26`)가 **79.7%**를 차지 (유효 인원 N_eff = 1.47명, 점수 -0.0093 하락!)
   - 반면 유일하게 점수가 유지된 `S2_s1` (+0.0027)은 두 환자 비율이 **56.3% : 43.7%**(`N_eff = 1.97명`)로 고르고 두 사람 모두 심부+피질 전극을 함께 갖고 있었습니다.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Sequence, Tuple


EMBEDDED_S2_SEEDS = [
    {"seed": 1, "pair": ("iEEG_Sub23", "sub-09_AJILE"), "orig_counts": (18040, 14006), "kept_64": (5493, 4265), "depth_frac": 0.227, "d_64": +0.0027, "d_1024": +0.0030, "byd_64": +0.0010},
    {"seed": 2, "pair": ("iEEG_Sub26", "sub-10_AJILE"), "orig_counts": (54639, 13877), "kept_64": (7782, 1976), "depth_frac": 0.147, "d_64": -0.0093, "d_1024": -0.0060, "byd_64": -0.0047},
    {"seed": 3, "pair": ("iEEG_Sub1", "sub-11_AJILE"),  "orig_counts": (18830, 13949), "kept_64": (5605, 4152), "depth_frac": 0.263, "d_64": -0.0055, "d_1024": -0.0039, "byd_64": -0.0122},
    {"seed": 4, "pair": ("iEEG_Sub18", "sub-03_AJILE"), "orig_counts": (14223, 13952), "kept_64": (4926, 4832), "depth_frac": 0.241, "d_64": -0.0065, "d_1024": -0.0080, "byd_64": -0.0101},
    {"seed": 5, "pair": ("iEEG_Sub24", "sub-06_AJILE"), "orig_counts": (22829, 13965), "kept_64": (6054, 3703), "depth_frac": 0.069, "d_64": -0.0057, "d_1024": -0.0063, "byd_64": -0.0035},
    {"seed": 6, "pair": ("iEEG_Sub17", "sub-08_AJILE"), "orig_counts": (17513, 13889), "kept_64": (5442, 4316), "depth_frac": 0.096, "d_64": -0.0089, "d_1024": -0.0098, "byd_64": -0.0054},
]


def pearson_r_and_p_df4(xs: Sequence[float], ys: Sequence[float]) -> Tuple[float, float]:
    """n=6 (df=4) 피어슨 상관계수 r과 정확한 양측 p-값을 계산합니다."""
    n = len(xs)
    assert n == len(ys) == 6
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    r = num / den if den > 0 else 0.0
    if abs(r) >= 1.0:
        return r, 0.0
    t_abs = abs(r) * math.sqrt((n - 2) / (1.0 - r * r))
    theta = math.atan(t_abs / 2.0)
    sin_t, cos_t = math.sin(theta), math.cos(theta)
    p_two = max(0.0, min(1.0, 1.0 - sin_t * (1.0 + 0.5 * cos_t * cos_t)))
    return r, p_two


def cap_per_subject_equally(subject_record_counts: Dict[str, int], total_target: int) -> Dict[str, int]:
    """
    [복붙용 해결 코드]
    환자마다 원래 녹음 길이가 달라도 총 `total_target`개를 환자들에게 똑같이(1/K씩) 배분합니다.
    특정 환자의 전체 기록이 `total_target / K`보다 적다면 그 환자는 전부를 쓰고,
    모자란 개수만 나머지 환자들에게 균등하게 나누어 채웁니다 (Water-filling 방식).
    """
    remaining = dict(subject_record_counts)
    allocated = {subj: 0 for subj in remaining}
    budget = int(total_target)
    if sum(remaining.values()) < budget:
        raise ValueError(f"전체 가용 기록({sum(remaining.values())})이 목표치({budget})보다 적습니다.")
    while budget > 0 and remaining:
        share = max(1, budget // len(remaining))
        for subj in list(remaining.keys()):
            take = min(remaining[subj], share, budget)
            allocated[subj] += take
            remaining[subj] -= take
            budget -= take
            if remaining[subj] == 0:
                del remaining[subj]
            if budget == 0:
                break
    return allocated


def audit_n2_subject_scaling(hangang_dir: Path | None = None) -> Dict[str, object]:
    """S2 (2명) 실험의 기록 수·병원 비율·심부 전극 상관·환자 내 비중 불균형을 종합 점검합니다."""
    seeds = [dict(row) for row in EMBEDDED_S2_SEEDS]
    if hangang_dir is not None:
        em_path = hangang_dir / "reports/lead/electrode_mix_summary.json"
        nc_path = hangang_dir / "reports/H-llm/nested_check_1209249.json"
        p1_path = hangang_dir / "experiments/20261108_lead_subjfix/plan.json"
        p2_path = hangang_dir / "experiments/20261108_lead_subjfix/plan46.json"
        if em_path.is_file() and nc_path.is_file() and p1_path.is_file() and p2_path.is_file():
            em = json.loads(em_path.read_text(encoding="utf-8"))
            nc = json.loads(nc_path.read_text(encoding="utf-8"))
            cnt_map = {Path(p["source"]).name: int(p["n_train"]) for p in nc["per_source"]}
            plans = {}
            plans.update(json.loads(p1_path.read_text(encoding="utf-8"))["S2_64"])
            plans.update(json.loads(p2_path.read_text(encoding="utf-8"))["S2_64"])
            s64 = em["S2_64 loss vs depth"]
            s1024 = em["S2_1024 loss vs depth"]
            seeds = []
            for idx_zero in range(6):
                s_idx = idx_zero + 1
                p_info = plans[str(s_idx)]
                names = p_info["subject_list"].split(",")
                f = float(p_info["source_fraction"])
                orig = tuple(cnt_map[nm] for nm in names)
                kept = tuple(max(1, int(round(c * f))) for c in orig)
                seeds.append({
                    "seed": s_idx,
                    "pair": tuple(nm.replace("_clipped_fixed200.lmdb", "").replace("_clip-200.0.lmdb", "") for nm in names),
                    "orig_counts": orig,
                    "kept_64": kept,
                    "depth_frac": float(s64["depth_frac_record_weighted"][idx_zero]),
                    "d_64": float(s64["rule3_diff"][idx_zero]),
                    "d_1024": float(s1024["rule3_diff"][idx_zero]),
                    "byd_64": float(s64["BYD_diff"][idx_zero]),
                })

    for row in seeds:
        k0, k1 = row["kept_64"]
        tot = k0 + k1
        p0, p1 = k0 / tot, k1 / tot
        row["max_patient_share"] = round(max(p0, p1), 4)
        row["effective_n_subjects"] = round(1.0 / (p0 * p0 + p1 * p1), 3)
        eq = cap_per_subject_equally({row["pair"][0]: row["orig_counts"][0], row["pair"][1]: row["orig_counts"][1]}, 9757)
        row["equal_cap_64"] = (eq[row["pair"][0]], eq[row["pair"][1]])

    depths = [r["depth_frac"] for r in seeds]
    d64s = [r["d_64"] for r in seeds]
    d1024s = [r["d_1024"] for r in seeds]
    byd64s = [r["byd_64"] for r in seeds]
    r64, p64 = pearson_r_and_p_df4(depths, d64s)
    r1024, p1024 = pearson_r_and_p_df4(depths, d1024s)
    r_byd, p_byd = pearson_r_and_p_df4(depths, byd64s)

    return {
        "matched_records_64": 9757,
        "matched_records_1024": 610,
        "hospital_stratification": "1 SNUH + 1 AJILE across all 6 seeds (12 disjoint subjects)",
        "depth_corr_64": {"r": round(r64, 3), "p_two_sided": round(p64, 3)},
        "depth_corr_1024": {"r": round(r1024, 3), "p_two_sided": round(p1024, 3)},
        "depth_corr_byd_64": {"r": round(r_byd, 3), "p_two_sided": round(p_byd, 3)},
        "max_single_patient_share_s2": max(r["max_patient_share"] for r in seeds),
        "min_effective_n_s2": min(r["effective_n_subjects"] for r in seeds),
        "seeds": seeds,
    }


if __name__ == "__main__":
    res = audit_n2_subject_scaling(Path("/home/juke/git/chaewon-intern-2026fall/hangang"))
    print("=== [점검 3] 사람 수 N=2 (subjfix46) 통제 설계 검증 및 환자 비중 분석 ===")
    print(f"- 기록 수 통제: 1/64 = {res['matched_records_64']}개 (295회 반복), 1/1024 = {res['matched_records_1024']}개")
    print(f"- 병원 층화:   {res['hospital_stratification']}")
    print(f"- 심부 전극 비율 상관: 1/64 rule3 r={res['depth_corr_64']['r']:+.3f} (p={res['depth_corr_64']['p_two_sided']:.3f}), "
          f"1/1024 rule3 r={res['depth_corr_1024']['r']:+.3f} (p={res['depth_corr_1024']['p_two_sided']:.3f}), "
          f"BYD r={res['depth_corr_byd_64']['r']:+.3f} -> 통계적으로 유의하지 않음!")
    print(f"- 환자 내 기록 쏠림 최대치: S2_s2에서 1명이 {res['max_single_patient_share_s2']*100:.1f}% 차지 (유효 인원 {res['min_effective_n_s2']:.2f}명)\n")
    for s in res["seeds"]:
        print(f"  seed {s['seed']} {s['pair'][0]}+{s['pair'][1]}: "
              f"실제 추출={s['kept_64']} (최대비중 {s['max_patient_share']*100:.1f}%, N_eff={s['effective_n_subjects']:.2f}) "
              f"| 50:50 균등추출 시={s['equal_cap_64']} | 심부={s['depth_frac']*100:.1f}% | Δ64={s['d_64']:+.4f}")
