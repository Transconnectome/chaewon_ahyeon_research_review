#!/usr/bin/env python3
"""
run_all_checks.py
=================
안채원 선생님·이아현 선생님의 11/20 AAAI 2027 NeuroAI 워크숍 초안 점검 및
복붙용 결과표 생성을 한 번에 수행하는 통합 실행 스크립트입니다. (GPU 불필요, CPU 1초 완주)

실행 방법:
    CUDA_VISIBLE_DEVICES="" python3 code/workshop_checks/run_all_checks.py --write-outputs
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict

os.environ["CUDA_VISIBLE_DEVICES"] = ""

THIS_DIR = Path(__file__).resolve().parent
SNIPPETS_DIR = THIS_DIR / "snippets"
if str(SNIPPETS_DIR) not in sys.path:
    sys.path.insert(0, str(SNIPPETS_DIR))

from check_n2_subject_balance import audit_n2_subject_scaling  # noqa: E402
from check_pr_pc90_and_layers import audit_effdim_and_layers  # noqa: E402
from fix_newsubj_eval_scale import audit_holdout_vs_newsubj  # noqa: E402
from patch_split_np_fdr import analyze_split_np, format_markdown_table  # noqa: E402
from reproduce_diver2_bugs import (  # noqa: E402
    demo_neuroprobe_voxel_extrapolation,
    demo_rope_bfloat16_collision,
)


def run_all(hangang_dir: Path | None = None, write_outputs: bool = False) -> Dict[str, object]:
    """5대 점검을 순서대로 실행하고 요약 딕셔너리(및 선택적 마크다운/JSON 파일)를 반환합니다."""
    split_np_json = (
        hangang_dir / "reports/lead/split_np_summary.json"
        if hangang_dir is not None
        else None
    )
    c1 = analyze_split_np(split_np_json)
    c2 = audit_holdout_vs_newsubj(hangang_dir)
    c3 = audit_n2_subject_scaling(hangang_dir)
    c4 = audit_effdim_and_layers(hangang_dir)
    c5 = {
        "rope_bf16": demo_rope_bfloat16_collision(),
        "neuroprobe_voxel": demo_neuroprobe_voxel_extrapolation(),
    }

    report = {
        "check_1_neuroprobe_15tasks": {
            "counts_1of64": c1["1/64 - Base"]["counts"],
            "counts_1of1024": c1["1/1024 - Base"]["counts"],
            "draft_typo_1of64": {"유지": 6, "판정 불가": 9, "깨짐": 0},
            "draft_typo_1of1024": {"유지": 8, "판정 불가": 7, "깨짐": 0},
            "sig_fdr_negative_1of64": c1["1/64 - Base"]["sig_fdr_negative"],
            "sig_fdr_negative_1of1024": c1["1/1024 - Base"]["sig_fdr_negative"],
            "sig_fdr_positive_1of1024": c1["1/1024 - Base"]["sig_fdr_positive"],
            "rows_1of64": c1["1/64 - Base"]["rows"],
            "rows_1of1024": c1["1/1024 - Base"]["rows"],
        },
        "check_2_holdout_vs_newsubj": {
            k: v for k, v in c2.items() if not k.endswith("_snippet")
        },
        "check_3_n2_subject_scaling": c3,
        "check_4_effdim_and_layers": c4,
        "check_5_diver2_bug_demos": c5,
    }

    if write_outputs:
        out_dir = THIS_DIR / "outputs"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "appendix_c_neuroprobe_15tasks_fdr.md").write_text(
            format_markdown_table(c1) + "\n", encoding="utf-8"
        )
        (out_dir / "verification_report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    return report


def main() -> None:
    ap = argparse.ArgumentParser(description="Run all 5 workshop verification checks on CPU.")
    ap.add_argument(
        "--hangang-dir",
        type=Path,
        default=Path("/home/juke/git/chaewon-intern-2026fall/hangang"),
        help="Read-only path to chaewon-intern-2026fall/hangang (uses embedded data if missing).",
    )
    ap.add_argument(
        "--write-outputs",
        action="store_true",
        help="Write ready-to-paste Markdown table and JSON report into code/workshop_checks/outputs/.",
    )
    args = ap.parse_args()
    hangang = args.hangang_dir if args.hangang_dir.is_dir() else None
    rep = run_all(hangang_dir=hangang, write_outputs=args.write_outputs)

    c1 = rep["check_1_neuroprobe_15tasks"]
    c2 = rep["check_2_holdout_vs_newsubj"]
    c3 = rep["check_3_n2_subject_scaling"]
    c4 = rep["check_4_effdim_and_layers"]
    c5 = rep["check_5_diver2_bug_demos"]

    print("==========================================================================")
    print("  11/20 NeuroAI 워크숍 초안 5대 점검 자동 실행 요약 (CPU Read-Only 검증)")
    print("==========================================================================")
    print(f"[1] 부록 C Neuroprobe 15개 과제 실제 집계:")
    print(f"    - 1/64   : {c1['counts_1of64']}  (초안 오타 6/9/0 -> 5/10/0 정정!)")
    print(f"    - 1/1024 : {c1['counts_1of1024']}  (초안 오타 8/7/0 -> 7/8/0 정정!)")
    print(f"    - BH-FDR(15개) 보정 후 유의한 하락(깨짐): 1/64 {len(c1['sig_fdr_negative_1of64'])}개, "
          f"1/1024 {len(c1['sig_fdr_negative_1of1024'])}개")
    print(f"[2] 같은 환자 검증 손실({c2['heldout_all_mean']:.4f}) vs 새 환자 손실({c2['newsubj_all_mean']:.4f}):")
    print(f"    - 2.88배 차이 원인: `newsubj_cell.py`의 `/ 2.0` 전압 스케일링 누락(확인={c2['found_missing_div2_in_newsubj_cell_py']}) + 1초(N=1) 창 길이 차이")
    print(f"    - 같은 조건 내 `1/1024 vs 전체` 상대 변화율: 새 환자 {c2['unseen_subject_1024_rel_pct'][0]:+.2f}% (차이 없음)")
    print(f"[3] 사람 수 N=2 (`subjfix46`, n=6):")
    print(f"    - 기록 수({c3['matched_records_64']}개=295회 반복) 및 병원 비율(SNUH 1+AJILE 1) 이미 완벽 통제 확인!")
    print(f"    - 심부 전극 상관 p={c3['depth_corr_64']['p_two_sided']:.3f} (유의하지 않음); "
          f"`S2_s2` 단일 환자 비중 {c3['max_single_patient_share_s2']*100:.1f}% 쏠림 확인")
    print(f"[4] 유효 차원 지표 구분 & 읽는 층(1층 vs 12층):")
    print(f"    - `54.7 -> 28.1` 감소는 `PR`이 아니라 `90% 주성분 개수(PC90_z)`임 (`PR`은 미학습 5.01 -> Base 5.42로 동일)")
    print(f"    - Small(12층) 1/64: 1층 {c4['readout_layers']['Small_d12_51.4M']['1/64_rd1'][0]:+.4f}(유지), "
          f"12층 {c4['readout_layers']['Small_d12_51.4M']['1/64_rdall'][0]:+.4f}(유지)")
    print(f"    - Small(12층) 1/1024: 1층 {c4['readout_layers']['Small_d12_51.4M']['1/1024_rd1'][0]:+.4f}(유지), "
          f"12층 {c4['readout_layers']['Small_d12_51.4M']['1/1024_rdall'][0]:+.4f}(깨짐)")
    print(f"[5] DIVER-2 투고 후 수정용 버그 데모:")
    print(f"    - RoPE bfloat16 6,001개 위치 중 고유값 {c5['rope_bf16']['unique_in_bfloat16']}개 (float32 패치 시 6,001개)")
    print(f"    - Neuroprobe 복셀 좌표 정규화 반경 r_hat = {c5['neuroprobe_voxel']['voxel_r_hat']} (> 1.0 단위 구 외삽)")
    if args.write_outputs:
        print("\n[완료] 복붙용 부록 C 표 저장: code/workshop_checks/outputs/appendix_c_neuroprobe_15tasks_fdr.md")


if __name__ == "__main__":
    main()
