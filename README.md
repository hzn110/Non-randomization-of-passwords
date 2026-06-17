# 🔐 인간이 만든 비밀번호는 정말 랜덤할까?

> 실제 유출 비밀번호 데이터 1,400만 건으로 인간 선택의 패턴을 통계물리학과 정보보안 관점에서 분석하는 프로젝트

🔗 **배포 링크 (Streamlit)**: [statistical-pw-mechanics.streamlit.app](https://statistical-pw-mechanics.streamlit.app/)  
📊 **데이터 출처 1**: [Kaggle — RockYou Password Dataset](https://www.kaggle.com/datasets/wjburns/common-password-list-rockyoutxt)  
📊 **데이터 출처 2**: [Kaggle — 10,000 Most Common Passwords](https://www.kaggle.com/datasets/shivamb/10000-most-common-passwords)

---

## 1. 우리가 발견한 문제

매일 수십 개의 서비스에서 비밀번호를 만들면서, 우리는 스스로 무작위를 선택한다고 생각합니다.  
그런데 정말 그럴까요? 아니면 *우리가 편하다고 느끼는 패턴을 반복*하고 있는 건 아닐까요?

우리 팀은 이 익숙한 착각이 **실제 데이터로 뒷받침되는지** 궁금했습니다. 그래서 다음과 같이 문제를 정의했습니다.

> **"인간이 만든 비밀번호는 정말 랜덤할까?  
> 그리고 그 비무작위성은 정보보안에 어떤 영향을 미칠까?"**

막연한 느낌("다들 비슷하게 만들더라")을 **검증 가능한 질문**으로 바꾼 것이 이 프로젝트의 출발점입니다.

---

## 2. 사용한 데이터

이 프로젝트는 두 개의 Kaggle 데이터셋을 목적에 맞게 나누어 활용했습니다.

### 📂 데이터셋 1 — RockYou Password Dataset (주 분석용)

| 항목 | 내용 |
| --- | --- |
| 출처 | Kaggle — RockYou Password Dataset |
| 원본 링크 | [kaggle.com/datasets/wjburns/common-password-list-rockyoutxt](https://www.kaggle.com/datasets/wjburns/common-password-list-rockyoutxt) |
| 데이터 규모 | 약 1,400만 건의 실제 유출 비밀번호 |
| 배경 | 2009년 소셜 게임 플랫폼 RockYou의 해킹 사고로 유출된 사용자 비밀번호 |
| 활용 목적 | 통계물리학적 패턴 분석, 거시상태 분포, 엔트로피 계산 |
| 파생 변수 | 길이 / 거시상태(Macrostate) / 섀넌 엔트로피 / 문자 종류 포함 여부 플래그 |

> ⚠️ 원본 데이터에는 인코딩 오류 및 특수문자 혼입 행이 포함되어 있어,  
> 코드에서 전처리(`strip`, `encoding='latin-1'`, 결측치 제거)를 거쳐 분석에 활용했습니다.

### 📂 데이터셋 2 — 10,000 Most Common Passwords (흔한 비밀번호 비교용)

| 항목 | 내용 |
| --- | --- |
| 출처 | Kaggle — 10,000 Most Common Passwords |
| 원본 링크 | [kaggle.com/datasets/shivamb/10000-most-common-passwords](https://www.kaggle.com/datasets/shivamb/10000-most-common-passwords) |
| 데이터 규모 | 전 세계에서 가장 자주 사용되는 비밀번호 상위 10,000건 |
| 배경 | 다양한 유출 데이터를 종합해 선별된 공통 취약 비밀번호 목록 |
| 활용 목적 | 비밀번호 안전도 측정 페이지에서 "흔한 비밀번호 여부" 즉시 판정 |
| 파일명 | `common_passwords.csv` |

---

## 3. 분석 방법

두 가지 학문적 관점에서 교차 분석했습니다.

**1. 통계물리학적 분석**
- 비밀번호를 문자 종류 패턴으로 추상화한 **거시상태(Macrostate)** 개념 적용
- 엔트로피 분포 및 질서변수(Order Parameter) 계산으로 비무작위성을 정량화
- 거시상태 빈도 분포에서 **Zipf의 법칙** 성립 여부 확인 (log-log 그래프)

**2. 정보보안적 분석**
- 연속 숫자·키보드 패턴·반복 문자 등 **Human Bias Score** 산출
- 이론적 엔트로피 대비 패턴 감점을 반영한 **실질 엔트로피** 계산
- 브루트포스 예상 크래킹 시간 및 사전 공격 취약도 평가

사이드바에서 직접 비밀번호를 입력해 실제 데이터와 비교하고, 자신의 비밀번호 안전도를 측정해볼 수 있습니다.

---

## 4. 페이지 구성

| 페이지 | 내용 |
| --- | --- |
| 🏠 홈 | 프로젝트 소개 및 연구 질문 |
| 1️⃣ 비밀번호 생성의 원리 | 길이·문자 구성·엔트로피 분포 분석 |
| 2️⃣ 비밀번호의 규칙성 | 연속 숫자, 키보드 배열, 날짜 패턴 등 인간 행동 패턴 검증 |
| 3️⃣ 비밀번호와 정보보안 | 발견된 패턴이 사전 공격·브루트포스에 미치는 영향 분석 |
| 4️⃣ 비밀번호 안전도 측정 | 사용자 비밀번호의 희귀도(Rarity)와 보안성(Security) 평가 |

---

## 5. 우리가 내린 결론

> 통계물리학적으로 인간의 비밀번호 선택은 높은 엔트로피 상태가 아니라  
> **특정 패턴에 집중된 낮은 엔트로피 상태**를 보인다.  
> 이러한 비무작위성은 정보보안 측면에서 예측 가능성을 증가시키며,  
> 결과적으로 **비밀번호 크래킹 성공률을 높이는 원인**이 된다.  
> 따라서 안전한 비밀번호 설계를 위해서는  
> 인간의 자연스러운 선택 경향을 **의도적으로 피해야 한다**.

---

## 6. AI를 비판적으로 활용한 과정

이 프로젝트는 Claude의 도움을 받아 코드를 작성했지만, **AI의 결과를 그대로 믿지 않고 검증**했습니다.

- AI가 제안한 엔트로피 계산 로직이 특수문자 집합 크기를 과소 산정하는 문제를 발견해 **직접 charset_size 함수를 수정**했습니다.
- 거시상태 분포가 Zipf 법칙을 따르는지 AI가 단정하는 대신, **실제 log-log 그래프를 그려 육안으로 검증**했습니다.
- "인간이 랜덤하지 않을 것"이라는 우리의 가설과 데이터 결과가 일치했을 때도, **p-value 등 통계적 근거를 추가로 확인**했습니다.

> 💡 **AI 제안, 인간 결정** — AI는 도구이고, 무엇을 묻고 어떻게 해석할지는 우리가 정했습니다.

---

## 7. 팀원과 역할

| 학번 | 이름 | 역할 |
| --- | --- | --- |
| 20306 | 김시우 | 데이터 수집 · 통계물리학 분석 · 시각화 |
| 20628 | 최홍란 | 정보보안 분석 · 안전도 측정 페이지 · README |

> GitHub와 공유 문서를 활용해 역할을 나누고, 분석 방향은 함께 논의하며 결정했습니다.

---

## 8. 실행 방법

```bash
pip install streamlit pandas plotly
streamlit run 홈.py
```

프로젝트 루트 디렉터리에 아래 파일이 있어야 합니다.

```
📁 프로젝트 루트
├── 홈.py
├── rockyou_rigorous_behavioral_physics_v2.csv
├── common_passwords.csv
└── pages/
    ├── 00_비밀번호 생성의 원리.py
    ├── 01_비밀번호의 규칙성.py
    ├── 02_비번 보안.py
    └── 03_비번 평가.py
```
---

🎓 데이터 1: [Kaggle — RockYou Password Dataset](https://www.kaggle.com/datasets/wjburns/common-password-list-rockyoutxt)  
🎓 데이터 2: [Kaggle — 10,000 Most Common Passwords](https://www.kaggle.com/datasets/shivamb/10000-most-common-passwords)  
🤝 함께 만든 도구: Claude,chatgpt
