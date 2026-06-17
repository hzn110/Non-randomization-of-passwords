# 🔐 인간이 만든 비밀번호는 정말 랜덤할까?

> **Statistical Physics × Information Security**  
> 실제 유출 비밀번호 데이터로 살펴보는 인간 선택의 패턴

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://statistical-pw-mechanics.streamlit.app)

---

## 📌 프로젝트 소개

우리는 비밀번호를 만들 때 스스로는 무작위라고 생각한다.

하지만 실제 비밀번호 데이터는 인간이 반복적으로 특정 규칙을 사용한다는 사실을 보여준다.

본 프로젝트는 실제 유출 비밀번호 데이터(RockYou)를 활용하여 인간의 선택 행동을 **통계물리학**적으로 분석하고, 그 결과를 **정보보안** 관점에서 해석하는 것을 목표로 한다.

---

## 🧠 핵심 연구 질문

> 인간이 만든 비밀번호는 정말 랜덤할까?  
> 그리고 그 비무작위성은 정보보안에 어떤 영향을 미칠까?

---

## 📊 데이터

| 항목 | 내용 |
|------|------|
| 분석 대상 비밀번호 | 1,400만 개+ |
| 데이터 출처 | RockYou 유출 데이터셋 |
| 분석 지표 | Shannon Entropy, Order Parameter, Macrostate, Human Bias Score 등 |
| 발견된 패턴 | 100개+ |

---

## 🗂️ 페이지 구성

### `main.py` — 홈
- 프로젝트 소개 및 연구 진행 과정 개요
- Apple Liquid Glass 스타일 UI
- 다크/라이트 모드 전환 기능

---

### `pages/00_비밀번호 생성의 원리` — ① 생성 과정 분석
**인간은 어떻게 비밀번호를 만드는가?**

통계역학적 관점에서 분석한 비밀번호 생성 과정

- 미시상태(Microstate) / 거시상태(Macrostate) 개념 적용
- Human Bias Score 분포 시각화
- Shannon Entropy 분포 분석
- 타이핑 이동 거리(Keyboard Path Length) 분석
- Order Parameter를 통한 질서 측정
- Empirical State Density 분석
- **결론**: 비밀번호 생성은 자기조직화(Self-Organization)의 통계역학적 현상

---

### `pages/01_비밀번호의 규칙성` — ② 규칙성 검증
**인간의 비밀번호에는 정말 규칙성이 존재하는가?**

- 인터랙티브 해커 시뮬레이션 (비밀번호 예측 퀴즈)
- 거시상태(Macrostate) 구조 반복성 검증
- Zipf 법칙 — 소수의 비밀번호가 압도적 빈도를 차지함을 로그-로그 그래프로 확인
- Bigram 분석 — 가장 자주 등장하는 2자 조합 시각화
- 랜덤 세계 vs 실제 데이터 Shannon Entropy 분포 비교
- 가상 사전 공격 시뮬레이션

---

### `pages/02_비번 보안` — ③ 정보보안 분석
**인간의 비밀번호 선택은 정보보안에 어떤 영향을 주는가?**

- 거시상태 분포와 Zipf 법칙이 사전 공격으로 이어지는 원리 설명
- **분석1** 비밀번호 강도 측정기 — 길이, 실질 엔트로피, 예상 크래킹 시간
- **분석2** 실제 데이터와 비교 — 입력 비밀번호의 구조가 상위 몇 % 패턴인지 확인
- **분석3** 엔트로피 비교 표 (`123456` vs `abc123` vs `qwerty123` vs `X7!kP2#z`)
- **분석4** 가상 브루트포스 시뮬레이터 — 클릭 한 번으로 크래킹 시간 체감
- 정보보안 결론 및 최종 탐구 결론

---

### `pages/03_비번 평가` — ④ 비밀번호 안전도 측정
**내 비밀번호는 얼마나 흔할까?**

입력한 비밀번호의 희귀도(Rarity)와 보안성(Security)을 분석

- **1️⃣ 기본 구조 분석** — 길이, 문자 종류 수, Shannon Entropy, Order Parameter, Macrostate
- **2️⃣ 희귀도 분석** — `common_passwords.csv` 흔한 비밀번호 여부 확인, 동일 구조 비율 및 Surprisal 계산
- **3️⃣ 보안성 분석** — Human Bias Score 패턴 탐지, 이론적 전수조사 시간 추정
- **4️⃣ 종합 점수** — 희귀도 점수 / 보안 점수 게이지 시각화
- **5️⃣ 개선 제안** — 분석 결과 기반 맞춤 보안 가이드

> 🔒 입력된 비밀번호는 서버에 저장되거나 전송되지 않으며, 브라우저 내에서만 분석됩니다.

---

## 🛠️ 기술 스택

| 분류 | 사용 기술 |
|------|-----------|
| Frontend / App | Streamlit |
| 데이터 처리 | Pandas, NumPy |
| 시각화 | Plotly Express, Plotly Graph Objects |
| 통계 분석 | Python 표준 라이브러리 (math, collections, re) |
| 배포 | Streamlit Community Cloud |
| 버전 관리 | GitHub |

---

## 📁 파일 구조

```
Non-randomization-of-passwords/
│
├── main.py                          # 홈 페이지
│
├── pages/
│   ├── 00_비밀번호 생성의 원리      # ① 생성 과정 분석
│   ├── 01_비밀번호의 규칙성         # ② 규칙성 검증
│   ├── 02_비번 보안                 # ③ 정보보안 분석
│   └── 03_비번 평가                 # ④ 비밀번호 안전도 측정
│
├── rockyou_rigorous_behavioral_physics_v2.csv   # 분석용 데이터셋
├── common_passwords.csv                          # 흔한 비밀번호 목록
├── requirements.txt
└── README.md
```

---

## ⚙️ 로컬 실행

```bash
# 1. 저장소 클론
git clone https://github.com/hzn110/Non-randomization-of-passwords.git
cd Non-randomization-of-passwords

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 앱 실행
streamlit run main.py
```

---

## 📚 핵심 개념 정리

| 개념 | 설명 |
|------|------|
| **미시상태 (Microstate)** | 비밀번호 하나하나 (`abc123`, `qwerty` 등) |
| **거시상태 (Macrostate)** | 문자 구조만 남긴 형태 (`LLLddd`, `Ulllllllddds` 등) |
| **Shannon Entropy** | 비밀번호의 무작위성 정도 (bits) |
| **Order Parameter** | 문자 종류 편중도 (0=균형, 1=완전 편중) |
| **Human Bias Score** | 인간 행동 패턴 개수 (연속 숫자, 키보드 패턴 등) |
| **Zipf 법칙** | 소수 패턴이 전체 빈도의 대부분을 차지하는 멱법칙 분포 |
| **자기조직화** | 규칙 없이도 집단 전체에서 질서가 나타나는 현상 |
| **Surprisal** | 특정 구조의 희귀도 (-log₂(확률), bits) |

---

## 🔗 바로가기

- 🌐 **라이브 앱**: [statistical-pw-mechanics.streamlit.app](https://statistical-pw-mechanics.streamlit.app)
- 📂 **GitHub**: [hzn110/Non-randomization-of-passwords](https://github.com/hzn110/Non-randomization-of-passwords)
