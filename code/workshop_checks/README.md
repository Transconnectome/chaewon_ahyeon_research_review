# 11/20 NeuroAI 워크숍 초안 검증 및 복붙 해결 스크립트 패키지 (`code/workshop_checks`)

**안채원 선생님**과 **이아현 선생님**, 그리고 지도교수 **차지욱 교수님**께서 추가 GPU 실험 없이 CPU에서 1초 만에 모든 통계·수치 점검을 재현하고, 논문 본문과 부록에 바로 복사해 넣을 수 있도록 구성한 실행형 도구 모음입니다.

> 자세한 쉬운 말 해설과 논문 문장 전·후(`Before -> After`) 수정본은 [../../docs/06_student_friendly_guide_and_solutions.md](../../docs/06_student_friendly_guide_and_solutions.md) 문서를 먼저 읽어 주세요.

---

## 1. 한 줄 실행 방법 (GPU 불필요, 1초 소요)

저장소 루트(`/home/juke/git/chaewon_ahyeon_research_review`)에서 아래 명령 한 줄만 실행하면 5가지 점검이 모두 돌아가고 부록 C 완성 표가 생성됩니다:

```bash
CUDA_VISIBLE_DEVICES="" python3 code/workshop_checks/run_all_checks.py --write-outputs
```

---

## 2. 파일 구성 및 각 스크립트가 해결하는 문제

| 파일 경로 | 용도 및 한 줄 요약 |
|---|---|
| [run_all_checks.py](run_all_checks.py) | 5대 점검 통합 실행기 (`outputs/` 폴더에 복붙용 마크다운 표와 JSON 리포트 자동 저장) |
| [snippets/patch_split_np_fdr.py](snippets/patch_split_np_fdr.py) | `split_np.py`에 바로 붙이는 다중비교(BH-FDR $q$-값) 계산기 + 부록 C 개수 오타(`6/9 -> 5/10`, `8/7 -> 7/8`) 자동 정정 |
| [snippets/fix_newsubj_eval_scale.py](snippets/fix_newsubj_eval_scale.py) | `newsubj_cell.py`의 새 환자 손실(`0.2791`)이 높았던 진짜 이유(`/ 2.0` 전압 스케일링 누락 + 1초 창) 검증 및 1줄 패치 |
| [snippets/check_n2_subject_balance.py](snippets/check_n2_subject_balance.py) | `subjfix46` $N=2$ 실험의 통제 항목 검증 및 환자별 기록 50:50 균등 배분 함수(`cap_per_subject_equally`) 예시 |
| [snippets/check_pr_pc90_and_layers.py](snippets/check_pr_pc90_and_layers.py) | `PR`(`5.01 -> 5.42`) vs `90% 주성분 개수 PC90`(`54.7 -> 28.1`) 구분 데모 및 1층(`rd1`) vs 12층(`rdall`) 요약표 |
| [snippets/reproduce_diver2_bugs.py](snippets/reproduce_diver2_bugs.py) | 투고 후 고칠 `DIVER-2` 버그 2건(`RoPE bfloat16` 위치 충돌 829/6,001 & 복셀 좌표 `r_hat = 1.91`) 1초 재현 데모 |
| [outputs/appendix_c_neuroprobe_15tasks_fdr.md](outputs/appendix_c_neuroprobe_15tasks_fdr.md) | 워크숍 논문 부록 C에 그대로 붙여 넣을 수 있는 Neuroprobe 15개 과제 완성 표 |
| [outputs/verification_report.json](outputs/verification_report.json) | 5대 점검 수치 자동 검증 결과 JSON |
