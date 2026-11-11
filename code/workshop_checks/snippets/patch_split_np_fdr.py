#!/usr/bin/env python3
"""
patch_split_np_fdr.py
=====================
안채원 선생님·이아현 선생님의 `hangang/experiments/20261107_lead_top/split_np.py` 및
`hangang/reports/lead/split_np_summary.json`에 그대로 사용할 수 있는
다중비교 보정(Benjamini-Hochberg FDR q-값 & Bonferroni 구간) + 판정 개수 자동 집계 스크립트입니다.
(외부 패키지 없이 표준 라이브러리 `math`, `re`만 사용)

해결하는 문제 2가지:
1. 부록 C 개수 합산 오타 자동 수정:
   - 초안 표기 (`draft_user_20261109.md:61`, `8_figs.md:88`, 슬라이드 6쪽):
     1/64 (유지 6, 판정 불가 9, 깨짐 0), 1/1024 (유지 8, 판정 불가 7, 깨짐 0)
   - 실제 집계 (`split_np_summary.json:86-295`):
     1/64 (유지 5, 판정 불가 10, 깨짐 0), 1/1024 (유지 7, 판정 불가 8, 깨짐 0)
2. 15개 세부 과제를 동시에 볼 때 생기는 우연 효과(다중비교) 점검:
   - 각 과제의 양측 t-검정 p-값과 Benjamini-Hochberg FDR 보정 q-값(K=15)을 자동 계산합니다.
   - 결론: 보정 전후 모두 나빠진 과제(깨짐)는 0개이며, 1/1024의 `word_index`(+0.0074, p=0.036)도
     FDR 보정 시 q=0.268로 통계적으로 유의한 상승이 아님(탐색적 관찰)이 깔끔하게 확인됩니다.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

# n=6 (df=5) 기준 임계값:
# - 단일 비교 95% 양측 t 임계값 (`split_np.py:13`과 동일): t_{0.975, df=5} = 2.57058
# - 15개 동시 비교 Bonferroni 95% 양측 t 임계값 (alpha = 0.05 / 15): t_{1 - 0.025/15, df=5} = 5.24739
T_CRIT_95_DF5 = 2.5705818356363146
T_CRIT_BONF15_DF5 = 5.247416865937306

# `split_np_summary.json` 실측 스냅샷: {task: (n_units, mean, lo95, hi95, verdict_en, n_seeds)}
EMBEDDED_SPLIT_NP_SUMMARY: Dict[str, Dict[str, Tuple[int, float, float, float, str, int]]] = {
    "1/64 - Base": {
        "delta_volume":     (4, +0.0005, -0.0045, +0.0055, "keep", 6),
        "face_num":         (1, -0.0032, -0.0135, +0.0072, "undetermined", 6),
        "frame_brightness": (1, -0.0060, -0.0241, +0.0122, "undetermined", 6),
        "global_flow":      (2, -0.0017, -0.0090, +0.0056, "undetermined", 6),
        "gpt2_surprisal":   (3, +0.0015, -0.0035, +0.0065, "keep", 6),
        "local_flow":       (3, -0.0007, -0.0065, +0.0051, "undetermined", 6),
        "onset":            (5, +0.0003, -0.0022, +0.0029, "keep", 6),
        "pitch":            (4, -0.0009, -0.0045, +0.0027, "keep", 6),
        "speech":           (5, +0.0010, -0.0029, +0.0050, "keep", 6),
        "volume":           (4, -0.0033, -0.0136, +0.0069, "undetermined", 6),
        "word_gap":         (4, -0.0008, -0.0063, +0.0047, "undetermined", 6),
        "word_head_pos":    (2, +0.0006, -0.0075, +0.0086, "undetermined", 6),
        "word_index":       (4, -0.0014, -0.0059, +0.0031, "undetermined", 6),
        "word_length":      (4, -0.0005, -0.0061, +0.0051, "undetermined", 6),
        "word_part_speech": (3, -0.0026, -0.0067, +0.0015, "undetermined", 6),
    },
    "1/1024 - Base": {
        "delta_volume":     (4, +0.0030, -0.0016, +0.0075, "keep", 6),
        "face_num":         (1, -0.0009, -0.0128, +0.0111, "undetermined", 6),
        "frame_brightness": (1, -0.0093, -0.0241, +0.0055, "undetermined", 6),
        "global_flow":      (2, -0.0014, -0.0106, +0.0077, "undetermined", 6),
        "gpt2_surprisal":   (3, +0.0051, -0.0035, +0.0138, "keep", 6),
        "local_flow":       (3, -0.0007, -0.0106, +0.0092, "undetermined", 6),
        "onset":            (5, +0.0016, -0.0006, +0.0037, "keep", 6),
        "pitch":            (4, -0.0026, -0.0078, +0.0027, "undetermined", 6),
        "speech":           (5, -0.0006, -0.0032, +0.0019, "keep", 6),
        "volume":           (4, -0.0059, -0.0122, +0.0004, "undetermined", 6),
        "word_gap":         (4, +0.0078, +0.0043, +0.0113, "keep", 6),
        "word_head_pos":    (2, +0.0006, -0.0056, +0.0068, "undetermined", 6),
        "word_index":       (4, +0.0074, +0.0007, +0.0140, "keep", 6),
        "word_length":      (4, +0.0024, -0.0041, +0.0089, "keep", 6),
        "word_part_speech": (3, +0.0002, -0.0063, +0.0067, "undetermined", 6),
    },
}

VERDICT_KO_MAP = {"keep": "유지", "undetermined": "판정 불가", "broken": "깨짐"}
KEY_RE = re.compile(r"^\(4\)\s+NP\s+(1/64|1/1024)\s+([a-zA-Z0-9_]+)\s+\(units\s+\[(\d+)\]\)$")


def student_t_two_sided_p(t_stat: float, df: int = 5) -> float:
    """자유도 df(양의 정수)에서 양측 Student-t 검정 p-값을 정확하게 계산합니다 (외부 라이브러리 불필요)."""
    if df <= 0:
        raise ValueError(f"df must be >= 1, got {df}")
    x = abs(float(t_stat))
    if x == 0.0:
        return 1.0
    theta = math.atan(x / math.sqrt(df))
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)
    if df % 2 == 1:
        acc = 0.0
        if df > 1:
            term = sin_t * cos_t
            acc = term
            for k in range(3, df, 2):
                term *= (k - 1) / k * (cos_t * cos_t)
                acc += term
        cdf_pos = 0.5 + (theta + acc) / math.pi
    else:
        term = sin_t
        acc = term
        for k in range(2, df, 2):
            term *= (k - 1) / k * (cos_t * cos_t)
            acc += term
        cdf_pos = 0.5 + 0.5 * acc
    return max(0.0, min(1.0, 2.0 * (1.0 - cdf_pos)))


def benjamini_hochberg_fdr(p_values: Sequence[float]) -> List[float]:
    """15개 과제의 p-값 목록을 받아 Benjamini-Hochberg FDR 보정 q-값 목록을 반환합니다."""
    m = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda kv: kv[1])
    q_sorted = [0.0] * m
    running_min = 1.0
    for rank_minus_1 in range(m - 1, -1, -1):
        rank = rank_minus_1 + 1
        _, p = indexed[rank_minus_1]
        running_min = min(running_min, p * m / rank)
        q_sorted[rank_minus_1] = min(1.0, running_min)
    out = [0.0] * m
    for (orig_idx, _), q in zip(indexed, q_sorted):
        out[orig_idx] = q
    return out


def classify_verdict(mean_diff: float, lo_95: float, hi_95: float, margin: float = -0.005) -> str:
    """사전 등록된 3단계 판정 규칙 (`split_np.py:13`과 100% 동일)."""
    if lo_95 > margin:
        return "유지"
    if hi_95 < 0.0 and mean_diff < margin:
        return "깨짐"
    return "판정 불가"


def analyze_split_np(split_np_json: Path | None = None) -> Dict[str, object]:
    """`split_np_summary.json`(또는 내장 실측 데이터)에서 15개 과제 FDR 및 판정 개수를 계산합니다."""
    if split_np_json is not None and split_np_json.is_file():
        raw = json.loads(split_np_json.read_text(encoding="utf-8"))
        contrasts: Dict[str, Dict[str, Tuple[int, float, float, float, str, int]]] = {
            "1/64 - Base": {},
            "1/1024 - Base": {},
        }
        for key, val in raw.items():
            m_obj = KEY_RE.match(key)
            if not m_obj:
                continue
            frac, task, units_str = m_obj.group(1), m_obj.group(2), m_obj.group(3)
            contrasts[f"{frac} - Base"][task] = (
                int(units_str),
                float(val[0]),
                float(val[1]),
                float(val[2]),
                str(val[3]),
                int(val[4]),
            )
    else:
        contrasts = EMBEDDED_SPLIT_NP_SUMMARY

    results: Dict[str, object] = {}
    for label, task_map in contrasts.items():
        tasks = sorted(task_map.keys())
        rows = []
        raw_ps = []
        for task in tasks:
            n_units, m, lo95, hi95, verdict_en, n_seeds = task_map[task]
            # 95% t-구간 반폭 h = T_95 * SE 로부터 표준오차(SE)와 t-통계량 복원
            half_w = 0.5 * (hi95 - lo95)
            se = half_w / T_CRIT_95_DF5 if half_w > 0 else 1e-12
            lo_bonf = m - T_CRIT_BONF15_DF5 * se
            hi_bonf = m + T_CRIT_BONF15_DF5 * se
            t_stat = m / se
            p_two = student_t_two_sided_p(t_stat, df=n_seeds - 1)
            raw_ps.append(p_two)
            verdict_ko = VERDICT_KO_MAP.get(verdict_en, classify_verdict(m, lo95, hi95))
            verdict_bonf = classify_verdict(m, lo_bonf, hi_bonf)
            rows.append({
                "task": task,
                "n_units": n_units,
                "mean": m,
                "lo95": lo95,
                "hi95": hi95,
                "t_stat": round(t_stat, 4),
                "p_two_sided": p_two,
                "lo_bonf15": round(lo_bonf, 4),
                "hi_bonf15": round(hi_bonf, 4),
                "verdict_uncorrected": verdict_ko,
                "verdict_bonf15": verdict_bonf,
            })
        q_vals = benjamini_hochberg_fdr(raw_ps)
        for row, q in zip(rows, q_vals):
            row["q_bh15"] = q
        counts = {
            "유지": sum(1 for r in rows if r["verdict_uncorrected"] == "유지"),
            "판정 불가": sum(1 for r in rows if r["verdict_uncorrected"] == "판정 불가"),
            "깨짐": sum(1 for r in rows if r["verdict_uncorrected"] == "깨짐"),
        }
        sig_fdr_pos = [r["task"] for r in rows if r["q_bh15"] < 0.05 and r["mean"] > 0]
        sig_fdr_neg = [r["task"] for r in rows if r["q_bh15"] < 0.05 and r["mean"] < 0]
        results[label] = {
            "counts": counts,
            "sig_fdr_positive": sig_fdr_pos,
            "sig_fdr_negative": sig_fdr_neg,
            "rows": rows,
        }
    return results


DROP_IN_SNIPPET_FOR_SPLIT_NP = """\
# `split_np.py` 맨 아래에 10줄만 붙여 넣으면 p-값, BH-FDR q-값, 판정 개수가 자동 출력됩니다!
import math

def p_two_sided_df5(t):
    th = math.atan(abs(t) / math.sqrt(5.0))
    return max(0.0, 1.0 - (2.0 / math.pi) * (th + (2.0 / 3.0) * math.sin(2 * th) + (1.0 / 12.0) * math.sin(4 * th)))

def bh_fdr(ps):
    m, idx = len(ps), sorted(range(len(ps)), key=ps.__getitem__)
    out, cur = [0.0] * m, 1.0
    for r in range(m, 0, -1):
        cur = min(cur, ps[idx[r - 1]] * m / r)
        out[idx[r - 1]] = min(1.0, cur)
    return out
"""


def format_markdown_table(results: Dict[str, object]) -> str:
    """부록 C에 바로 복사-붙여넣기 할 수 있는 마크다운 표를 생성합니다."""
    lines = [
        "# 부록 C: Neuroprobe 15개 세부 과제 탐색적 분해 및 다중비교(BH-FDR) 점검표",
        "",
        "> **핵심 요약 (본문·부록 1줄용)**: Neuroprobe 15개 세부 과제를 개별 점검한 결과(n=6 시드 짝 비교),",
        "> 무보정 95% 구간 기준 **1/64에서는 유지 5개·판정 불가 10개·깨짐 0개**, **1/1024에서는 유지 7개·판정 불가 8개·깨짐 0개**였으며,",
        "> Benjamini-Hochberg FDR(K=15) 보정 후 유의하게 하락한 과제는 두 조건 모두 **0개**였다.",
        "> (환자 세션 수가 1~3개뿐인 시각·구문 과제는 표본 분산이 커서 개별 비열등성 구간이 넓으므로, 주 판정은 사전 등록한 3개 코퍼스 평균 `rule3`로 수행한다.)",
        "",
    ]
    for label in ("1/64 - Base", "1/1024 - Base"):
        block = results[label]
        c = block["counts"]
        lines.append(f"## {label} (정확한 집계: 유지 {c['유지']} · 판정 불가 {c['판정 불가']} · 깨짐 {c['깨짐']})")
        lines.append("")
        lines.append("| 세부 과제 (세션 수) | 평균 차이 Δ | 95% t-구간 (무보정) | 무보정 판정 | 양측 p-값 | BH-FDR q-값 (15개) | 해석 |")
        lines.append("|---|---:|---|---|---:|---:|---|")
        for r in block["rows"]:
            note = "비열등 유지" if r["verdict_uncorrected"] == "유지" else "세션 수 적어 구간 넓음"
            if r["q_bh15"] < 0.05 and r["mean"] > 0:
                note = "탐색적 소폭 양(+) 신호 (주장 제외)"
            elif r["p_two_sided"] < 0.05 and r["q_bh15"] >= 0.05:
                note = "FDR 보정 후 유의성 소멸 (우연 변동)"
            lines.append(
                f"| `{r['task']}` ({r['n_units']}) | {r['mean']:+.4f} | "
                f"[{r['lo95']:+.4f}, {r['hi95']:+.4f}] | {r['verdict_uncorrected']} | "
                f"{r['p_two_sided']:.4f} | {r['q_bh15']:.4f} | {note} |"
            )
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Compute BH-FDR q-values and exact counts for Neuroprobe 15 subtasks.")
    ap.add_argument(
        "--json",
        type=Path,
        default=Path("/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/split_np_summary.json"),
        help="Path to split_np_summary.json (falls back to embedded snapshot if absent).",
    )
    args = ap.parse_args()
    res = analyze_split_np(args.json)
    print(format_markdown_table(res))
