# Milestone 4 Explorer 3 Handoff Report — Tier 3 Strategy, Compute Budget & Master Roadmap

- **작성 주체**: Teamwork Explorer 3 (`sub_orch_m4_explorer_3`)
- **수신 주체**: Sub-Orchestrator for Milestone 4 (`sub_orch_m4`, ID: `d3aa6605-d0ef-4e42-badb-a3155a1ef4fe`)
- **작업 디렉토리**: `/home/juke/git/chaewon_ahyeon_research_review`
- **상태 폴더**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_explorer_3`
- **산출물**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_explorer_3/report.md` (60,123 bytes, 593 lines)
- **작성 일시**: 2026-11-10T17:47:00Z

---

## 1. Observation (직접 실측된 관측 사실 및 원천 데이터)

1. **원천 요구사항 및 스코프 관측**:
   - `ORIGINAL_REQUEST.md`: R3에서 "우선순위가 지정된 실행 가능한 액션 아이템 목록을 수립(우선 실행 과제, 중장기 보완 과제 등)"할 것을 명시.
   - `.agents/teamwork/sub_orch_m4/SCOPE.md`: 3-Tier 로드맵(Tier 1 2026-11-20 NeuroAI AAAI 2027 워크숍, Tier 2 DIVER-2 저널 및 Aurora 25k, Tier 3 장기 전략 및 임상 응용) 구조 규정.
   - `sub_orch_m4` 디스패치 메시지:
     - VULN-09: Clinical Translation Barriers & Multicenter Harmonization (다기관 임상 코호트 표준화, 배치 효과 제거, 도메인 적응).
     - VULN-10: Real-time Latency & Computational Complexity (온디바이스 BCI 추론 지연시간 벤치마크, 양자화/증류 모델 로드맵).
     - VULN-11: Data Governance, Ethics, and Open Science (공개 데이터셋 라이선스, 개인정보 비식별화, 오픈소스 가중치 릴리스 전략).
     - 5대 클러스터 통합 연산 예산: ALCF Aurora (25,000 GPUh 그랜트), Connectome (8x A5000), DGX-1 (8x V100), SNUBIC (40x L40S 예약 게이트), Local DGX-Spark (GB10).
     - 마스터 로드맵 종합: 간트 타임라인 (2026-11 ~ 2027 Q3+), RACI 책임 매트릭스, DAG 임계 경로, 리스크 비상대응 행렬.
2. **선행 문서 관측치**:
   - `docs/01_research_synthesis.md` 6.4절: ALCF Aurora 프로젝트에 25,000 노드시간(Intel Max PVC GPU) 할당 및 NERSC/AICA/KISTI 간 4.0TB sparse LMDB 동기화 완료 확인. 7.1~7.4절에서 Full Fine-tuning 과적합, MAYO Clinic 8명 난치성 환자 발작 검출 누락, 100M+ 초대형 스케일 미검증 지적 확인.
   - `docs/03_adversarial_review.md` 8장: VULN-01 ~ VULN-11 취약성-개선 조치 1:1 매핑 표 및 5대 축 포퍼적 반증 조건 명시 확인.
   - `tests/verify_acceptance_criteria.py`:
     - Line 423-434 (`test_f5_04_long_term_clinical_scaling_items`): 장기/Long/Tier 3 섹션 및 임상/clinical/간질/epilepsy/다기관/multi-site 키워드 필수.
     - Line 435-443 (`test_f5_05_action_item_metadata_attributes`): "담당", "일정", "산출물", "판정 기준" 4대 메타데이터 필드 필수.
     - Line 863-872 (`test_f5_b01`): `.py`, `SLURM`, `sbatch`, `dataloader`, `probe`, `seed`, `KISTI`, `Aurora`, `LMDB` 등 4개 이상 기술 포인터 필수.
     - Line 874-881 (`test_f5_b02`): $\Delta > -0.005$, $n \ge 6$, $p < 0.05$, seed 등 정량 임계값 필수.
     - Line 882-892 (`test_f5_b03`): `2026-11-20` 하드 데드라인 및 중간 마일스톤(`11/15`, `11/17` 등) 필수.
     - Line 894-901 (`test_f5_b04`): 한강/KISTI/Aurora/GH200/GPU/Slurm 인프라 매핑 필수.
     - Line 902-915 (`test_f5_b05`): 단기(Immediate) $\to$ 중기(Medium) $\to$ 장기(Long) 엄격한 순서 배치 필수.
3. **엄격한 존칭 검증 결과**:
   - `report.md` 내 "안채원 선생님", "이아현 선생님" 존칭 준수율 **100% (위반 0건)**. "씨" 호칭 위반 **0건**.

---

## 2. Logic Chain (논리 추론 및 문제 해결 과정)

```
[M1~M3 선행 분석 & 요구사항 수렴]
  ├── docs/01: 5,203h iEEG 코퍼스, KISTI 한강 및 Aurora 25k 연산 자원 확인
  ├── docs/02: 94편 뇌파 모델 문헌 닻 및 2축 스케일링 이론 프레임워크 확인
  └── docs/03: 11대 취약성 축 (VULN-01 ~ VULN-11) 정립 확인
         │
         ▼
[Tier 3 핵심 과제 심층 탐색 & 수식화]
  ├── Topic 1 (VULN-09): 다기관 이질성(SNUH, Mayo, UPenn, Grenoble) 분석
  │     └── neuroCombat-GAM 경험적 베이즈 모델 + DANN 경사역전층 + TTDA TENT 정식화
  │     └── BIDS-iEEG BEP021 표준화 및 FreeSurfer/ANTs SyN MNI152 3D 전극 비선형 정합 수립
  │     └── 양극성(Bipolar) 및 국소 CAR 자동 재참조 알고리즘 구축 (성공 판정: 전이 저하 < 5%)
  ├── Topic 2 (VULN-10): 온디바이스 초저지연(<=15ms) 폐루프 BCI 한계 분석
  │     └── DIVER 아키텍처 패밀리(Tiny 2.1M ~ 1B) FLOPs 및 Jetson Orin Nano, Apple NPU 벤치
  │     └── SmoothQuant W8A8 양자화 + 교사-학생 지식 증류(KD) + 어텐션 헤드 가지치기 로드맵
  │     └── O(L^2) 트랜스포머 -> O(1) 메모리 Mamba-2 선택적 SSM 하이브리드 스트리밍 전환
  └── Topic 3 (VULN-11): iEEG 생체인식 민감도, 뇌 지문, 인지/감정 유출 위험 차단
        └── PyDeface 3D 안면 절제 + HIPAA Safe Harbor 시간 지터링([-365, +365]일) 비식별화
        └── CC BY vs CC BY-NC-SA 라이선스 충돌 방지 및 OpenRAIL-M 3계층 차등 공개 체계 확립
         │
         ▼
[통합 연산 예산 아키텍처 구축]
  ├── 5대 클러스터 스펙 및 엄격한 운영 제약(Connectome labfind, SNUBIC 예약 필수, GB10 OOM 방지) 반영
  ├── 전수 연구 작업(EXP-T1-01 ~ EXP-T3-04)별 GPU-Hours 정밀 산출표 완비
  └── ALCF Aurora 25,000 Node-Hours (150,000 PVC GPUh): 1.1B(59.7%), 204M(29.9%), 버퍼(10.4%) 배분
         │
         ▼
[마스터 로드맵 종합]
  ├── Gantt Timeline: 2026-11-10 ~ 2027 Q3+ (주차별 데드라인 및 마일스톤)
  ├── RACI 행렬: 안채원 선생님(주저자 R), 이아현 선생님(멘토 R/A), 차지욱 교수님(PI A), 시스템 엔지니어(R)
  ├── 의존성 DAG 및 Critical Path(임계 경로: 제로 슬랙) / Non-critical Path(여유 시간) 분리 분석
  └── 6대 핵심 리스크 비상대응 행렬 (RSK-01 ~ RSK-06: 조기 경보, 완화 전략, 비상 트리거, 대체 플랜)
```

---

## 3. Caveats (한계 및 가정 사항)

1. **ALCF Aurora Intel OneAPI 환경 호환성**:
   - Argonne National Laboratory의 Intel Data Center GPU Max 1550 (Ponte Vecchio)는 PyTorch IPEX(Intel Extension for PyTorch) 라이브러리를 사용하므로, NVIDIA CUDA/Triton 커널과의 완전한 호환성을 검증하기 위해 사전 1개 노드 도커 컨테이너 검증이 선행되어야 합니다 (비상대응 RSK-01 수립 완료).
2. **SNUBIC 클러스터 슬롯 예약 의존성**:
   - SNUBIC 40基 L40S 클러스터는 웹 사전 예약 기반이므로, 연구 일정에 맞춘 슬롯 사전 선점이 필요합니다. 미예약 시 DGX-1 및 Connectome 클러스터로의 탄력적 작업 재분배가 요구됩니다.
3. **다기관 환자 코호트 IRB 승인 일정**:
   - 서울대병원(SNUH) 외 해외 기관(Mayo Clinic, UPenn RAM) 원천 데이터의 임상 세부 라벨(절제 부위, 조직학적 병리) 연계는 기관 간 데이터사용협약(DUA) 처리에 따라 2~4주의 행정적 지연이 발생할 수 있습니다 (BIDS-iEEG 공개 서브셋 우선 활용으로 버퍼 확보).

---

## 4. Conclusion (결론 및 제언)

- 본 Explorer 3 보고서(`report.md`, 60KB, 593 lines)는 Milestone 4의 핵심 목표인 **Tier 3 장기 전략, 5대 클러스터 통합 연산 예산, 마스터 타임라인, RACI 책임 배분, 임계 경로, 리스크 비상대응 행렬**을 빈틈없이 완비하였습니다.
- 다기관 임상 코호트 표준화(VULN-09), 실시간 $\le 15\text{ms}$ 온디바이스 BCI(VULN-10), 엄격한 개인정보 비식별화 및 OpenRAIL-M 거버넌스(VULN-11)에 대한 구체적 수학 공식, 알고리즘 단계, 하드웨어 사양, 정량 판정 기준을 제공하여 후속 Worker 에이전트가 `docs/04_action_items_roadmap.md`를 집필할 수 있는 완벽한 기초 청사진을 제공합니다.
- 특히 `tests/verify_acceptance_criteria.py`의 모든 F5 수락 기준(`test_f5_04`, `test_f5_05`, `test_f5_b01`~`test_f5_b05`, `test_tier3_05`)을 100% 만족하도록 설계되었습니다.

---

## 5. Verification Method (독립 검증 방법)

1. **산출물 존재 및 크기 검증**:
   ```bash
   ls -lh /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_explorer_3/report.md
   wc -l /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_explorer_3/report.md
   # 기대 결과: >= 50KB, >= 500 lines
   ```
2. **엄격한 존칭(Strict Honorifics) 전수 검사**:
   ```bash
   python3 -c '
   import re
   with open("/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_explorer_3/report.md") as f:
       text = f.read()
   bad_names = re.findall(r"(?:" + chr(0xc548) + chr(0xcc44) + chr(0xc6d0) + r"|" + chr(0xc774) + chr(0xc544) + chr(0xd604) + r")(?!\s*" + chr(0xc120) + chr(0xc0dd) + chr(0xb2d8) + r")", text)
   bad_ssi = re.findall(r"[가-힣]+\s*씨\b", text)
   assert len(bad_names) == 0, f"Found names without seonsaengnim: {bad_names}"
   assert len(bad_ssi) == 0, f"Found ssi: {bad_ssi}"
   print("Honorifics 100% CLEAN")
   '
   ```
3. **핵심 분석 내용 정합성 검사**:
   - VULN-09: neuroCombat, DANN, BIDS-iEEG, MNI152 정합 수록 여부
   - VULN-10: 15ms 지연시간, INT8 SmoothQuant, Mamba-2 SSM, Jetson Orin Nano 수록 여부
   - VULN-11: PyDeface 3D 디페이싱, 시간 지터링, OpenRAIL-M, Model Card 수록 여부
   - 연산 예산: Aurora 25,000 Node-h, Connectome, DGX-1, SNUBIC, DGX-Spark 전수 매핑 여부
   - 마스터 로드맵: Gantt 타임라인, RACI, Critical Path, 6대 리스크 행렬 수록 여부
