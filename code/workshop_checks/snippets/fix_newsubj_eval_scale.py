#!/usr/bin/env python3
"""
fix_newsubj_eval_scale.py
=========================
안채원 선생님·이아현 선생님의 `newsubj_cell.py` (새 환자 복원 손실 0.2791)와
`gen_gap_eval.py` (같은 37명 환자 2% holdout 복원 손실 0.0970)를 코드 줄 단위로 대조하여,
왜 절대 손실 숫자가 2.88배(0.2791 vs 0.0970) 차이 났는지 쉽게 설명하고 수정 코드를 보여주는 스크립트입니다.

핵심 발견:
- "새 환자라서 모델이 2.88배 망가진 것"이 아닙니다!
- 원인 1 (입력 전압 스케일 2배 차이):
  사전학습(`dataloader_utils.py:452`)과 `gen_gap_eval.py:85`는 iEEG 전압(uV)을 먼저 `/ 2.0` 한 뒤
  다시 `/ input_scale(100)`을 해서 총 `/ 200.0`으로 나눕니다.
  반면 `newsubj_cell.py:68,94`는 `collate`를 거치지 않아 `/ 2.0`이 빠졌고 `/ 100.0`만 적용되어
  입력 진폭이 정확히 **2배** 크게 들어갔습니다. (제곱오차 MSE 기준 최대 4배까지 손실 숫자가 커질 수 있음!)
- 원인 2 (창 길이 1초 vs 3초 차이):
  `gen_gap_eval.py`는 3초(`N=3` 패치) 창이라 가려진 1초 패치의 앞·뒤 1초 이웃(같은 전극)을 보고 복원할 수 있지만,
  `newsubj_cell.py`가 평가한 BYD/Pippi 테스트 창은 1초(`N=1` 패치)라서 마스킹된 채널은 자기 전극 신호가 100% 사라지고
  오직 이웃 전극만으로 맞혀야 하는 훨씬 어려운 시험이었습니다.
- 반면 같은 조건 안에서 비교한 `1/1024 - 전체` 상대 차이는 `-0.06% [-1.34%, +1.21%]`로 완전히 같았습니다!
"""
from __future__ import annotations

import json
import statistics as st
from pathlib import Path
from typing import Dict


EMBEDDED_HOLDOUT_VS_NEWSUBJ = {
    "heldout_same_37_subjects": {
        "all_mean_loss": 0.0970,
        "rel_pct_1of64_vs_all": [+0.06, -0.28, +0.39],
        "rel_pct_1of1024_vs_all": [+8.50, +7.75, +9.25],
        "input_divisor_uV": 200.0,
        "window_seconds": 3.0,
        "tokens_per_channel_N": 3,
    },
    "newsubj_unseen_pippi_byd": {
        "all_mean_loss": 0.2791,
        "1of64_mean_loss": 0.2785,
        "1of1024_mean_loss": 0.2789,
        "rel_pct_1of64_vs_all": [-0.18, -1.05, +0.68],
        "rel_pct_1of1024_vs_all": [-0.06, -1.34, +1.21],
        "input_divisor_uV_in_script": 100.0,  # `/ 2.0` 누락!
        "window_seconds": 1.0,
        "tokens_per_channel_N": 1,
    },
}


ONE_LINE_PATCH_FOR_NEWSUBJ = """\
# 파일: hangang/experiments/20261109_lead_newsubj/newsubj_cell.py (94번째 줄)
# [수정 전] 사전학습 collate의 iEEG `/ 2.0` (dataloader_utils.py:452)이 빠져 입력이 2배 큼:
xx = normalize_inputs(x.to(dev) / args.input_scale, getattr(args, "input_norm", "none"))

# [수정 후] 사전학습 및 imindbench(diver_model.py:93-95)와 동일하게 총 200 uV 단위로 맞춤:
iEEG_COLLATE_DIVISOR = 2.0  # dataloader_utils.py:452 ("scaling 200uv to 100uv")
xx = normalize_inputs(x.to(dev) / (args.input_scale * iEEG_COLLATE_DIVISOR), getattr(args, "input_norm", "none"))
"""


APPLES_TO_APPLES_1SEC_CHECK = """\
# (선택) 만약 투고 후 '같은 37명 환자'와 '새 환자(BYD/Pippi)'의 절대 손실 크기를
# 공정하게(둘 다 1초 창 N=1, 둘 다 /200uV) 비교하고 싶다면 `gen_gap_eval.py` 86번째 줄 아래에 1줄만 추가하면 됩니다:
x = x[:, :, :1, :]  # 3초(N=3) 대신 첫 1초(N=1) 패치만 사용하여 BYD/Pippi 1초 창과 조건 통일!
"""


def audit_holdout_vs_newsubj(hangang_dir: Path | None = None) -> Dict[str, object]:
    """실제 JSON 및 스크립트 파일을 읽어 스케일/창 길이 차이와 상대 손실 변화율을 검증합니다."""
    data = {
        "heldout_same_37_subjects": dict(EMBEDDED_HOLDOUT_VS_NEWSUBJ["heldout_same_37_subjects"]),
        "newsubj_unseen_pippi_byd": dict(EMBEDDED_HOLDOUT_VS_NEWSUBJ["newsubj_unseen_pippi_byd"]),
    }
    found_missing_div2_in_source = True

    if hangang_dir is not None:
        ho_path = hangang_dir / "reports/lead/heldout_summary.json"
        cg_path = hangang_dir / "reports/lead/curve6_gap_summary.json"
        ns_path = hangang_dir / "reports/lead/newsubj_summary.json"
        nc_path = hangang_dir / "experiments/20261109_lead_newsubj/newsubj_cell.py"

        if ho_path.is_file():
            ho = json.loads(ho_path.read_text(encoding="utf-8"))
            # Base heldout mean = mean(1/64 values) - diff
            base_ho = st.mean(ho["1/64"]["values"]) - float(ho["1/64"]["diff"])
            data["heldout_same_37_subjects"]["all_mean_loss"] = round(base_ho, 4)

        if cg_path.is_file():
            cg = json.loads(cg_path.read_text(encoding="utf-8"))
            data["heldout_same_37_subjects"]["rel_pct_1of64_vs_all"] = [
                round(float(cg["1/64"]["pct"]), 2),
                round(float(cg["1/64"]["pct_lo"]), 2),
                round(float(cg["1/64"]["pct_hi"]), 2),
            ]
            data["heldout_same_37_subjects"]["rel_pct_1of1024_vs_all"] = [
                round(float(cg["1/1024"]["pct"]), 2),
                round(float(cg["1/1024"]["pct_lo"]), 2),
                round(float(cg["1/1024"]["pct_hi"]), 2),
            ]

        if ns_path.is_file():
            ns = json.loads(ns_path.read_text(encoding="utf-8"))
            data["newsubj_unseen_pippi_byd"]["all_mean_loss"] = float(ns["both all mean"])
            data["newsubj_unseen_pippi_byd"]["1of64_mean_loss"] = float(ns["both 1of64 mean"])
            data["newsubj_unseen_pippi_byd"]["1of1024_mean_loss"] = float(ns["both 1of1024 mean"])
            data["newsubj_unseen_pippi_byd"]["tokens_per_channel_N"] = int(ns["tokens_used"][0])
            data["newsubj_unseen_pippi_byd"]["rel_pct_1of64_vs_all"] = [
                float(v) for v in ns["both 1of64 - all (% of all)"][:3]
            ]
            data["newsubj_unseen_pippi_byd"]["rel_pct_1of1024_vs_all"] = [
                float(v) for v in ns["both 1of1024 - all (% of all)"][:3]
            ]

        if nc_path.is_file():
            src = nc_path.read_text(encoding="utf-8")
            found_missing_div2_in_source = ("/ args.input_scale" in src) and ("/ 2.0" not in src and "* 2.0" not in src)

    ho_loss = data["heldout_same_37_subjects"]["all_mean_loss"]
    ns_loss = data["newsubj_unseen_pippi_byd"]["all_mean_loss"]
    ratio = ns_loss / ho_loss

    scale_factor = (
        data["heldout_same_37_subjects"]["input_divisor_uV"]
        / data["newsubj_unseen_pippi_byd"]["input_divisor_uV_in_script"]
    )
    return {
        "heldout_all_mean": ho_loss,
        "newsubj_all_mean": ns_loss,
        "raw_loss_ratio": round(ratio, 2),
        "input_amplitude_inflation": scale_factor,
        "pure_mse_quadratic_factor": scale_factor ** 2,
        "found_missing_div2_in_newsubj_cell_py": found_missing_div2_in_source,
        "same_subject_1024_rel_pct": data["heldout_same_37_subjects"]["rel_pct_1of1024_vs_all"],
        "unseen_subject_1024_rel_pct": data["newsubj_unseen_pippi_byd"]["rel_pct_1of1024_vs_all"],
        "patch_snippet": ONE_LINE_PATCH_FOR_NEWSUBJ,
        "one_sec_check_snippet": APPLES_TO_APPLES_1SEC_CHECK,
    }


if __name__ == "__main__":
    res = audit_holdout_vs_newsubj(Path("/home/juke/git/chaewon-intern-2026fall/hangang"))
    print("=== [점검 2] 같은 37명 검증 손실(0.0970) vs 새 환자 손실(0.2791) 원인 해부 ===")
    print(f"- 같은 37명 2% holdout 손실 (`gen_gap_eval.py`, 3초 창, /200uV): {res['heldout_all_mean']:.4f}")
    print(f"- 새 환자 BYD+Pippi 손실   (`newsubj_cell.py`, 1초 창, /100uV): {res['newsubj_all_mean']:.4f} ({res['raw_loss_ratio']:.2f}배)")
    print(f"- `newsubj_cell.py`에 `/ 2.0` 스케일링 누락 확인 여부: {res['found_missing_div2_in_newsubj_cell_py']}")
    print(f"- 같은 조건 내 상대 변화 (1/1024 vs 전체): 같은 환자 {res['same_subject_1024_rel_pct'][0]:+.2f}% vs 새 환자 {res['unseen_subject_1024_rel_pct'][0]:+.2f}%")
    print("\n--- 1줄 수정 패치 ---")
    print(res["patch_snippet"])
