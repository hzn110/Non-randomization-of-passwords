import streamlit as st

st.set_page_config(
    page_title="인간이 만든 비밀번호는 정말 랜덤할까?",
    page_icon="🔐",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.hero {
    text-align: center;
    padding: 3rem 1rem;
}

.hero h1 {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.hero p {
    font-size: 1.2rem;
    color: #888;
}

.card {
    background-color: #262730;
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 20px;
    height: 100%;
}

.card-title {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 10px;
}

.card-text {
    color: #CCCCCC;
}

.question-box {
    background: linear-gradient(135deg,#1f2937,#111827);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    margin-top: 40px;
}

.question-box h2 {
    font-size: 2rem;
}

.question-box p {
    font-size: 1.2rem;
}

.footer {
    text-align:center;
    margin-top:50px;
    color:gray;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================
st.markdown("""
<div class='hero'>
    <h1>🔐 인간이 만든 비밀번호는 정말 랜덤할까?</h1>
    <p>Statistical Physics × Information Security</p>
</div>
""", unsafe_allow_html=True)

# =========================
# 통계 카드
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "분석 대상 비밀번호",
        "1,400만+"
    )

with col2:
    st.metric(
        "발견된 패턴",
        "100+"
    )

with col3:
    st.metric(
        "연구 분야",
        "2개"
    )

st.divider()

# =========================
# 프로젝트 소개
# =========================
st.header("📖 프로젝트 소개")

st.write("""
우리는 비밀번호를 만들 때 스스로는 '무작위'라고 생각한다.

하지만 실제 비밀번호 데이터는 다른 이야기를 보여준다.

사람들은 특정 숫자, 단어, 키보드 배열과 같은
반복적인 패턴을 사용하는 경향이 있으며,
이러한 경향은 공격자가 비밀번호를 예측하는 데 활용될 수 있다.

본 프로젝트는 실제 유출 비밀번호 데이터를 활용하여
인간의 비밀번호 선택 행동을 통계물리학적으로 분석하고,
그 결과를 정보보안 관점에서 해석하는 것을 목표로 한다.
""")

st.divider()

# =========================
# 연구 목적
# =========================
st.header("🎯 연구 목적")

col1, col2 = st.columns(2)

with col1:
    st.info("""
### 통계물리학

- 비밀번호 분포 분석
- 엔트로피 계산
- 확률 분포 탐색
- 인간 선택 행동 모델링
""")

with col2:
    st.warning("""
### 정보보안

- 비밀번호 강도 평가
- 사전 공격 분석
- 브루트포스 공격 분석
- 보안 취약성 탐구
""")

st.divider()

# =========================
# 페이지 소개
# =========================
st.header("🧭 연구 진행 과정")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="card">
    <div class="card-title">① 비밀번호 생성 과정 분석</div>
    <div class="card-text">
    • 길이 분포 분석<br>
    • 문자 구성 분석<br>
    • 엔트로피 분석<br>
    • 통계물리학적 해석
    </div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="card">
    <div class="card-title">② 규칙성 검증</div>
    <div class="card-text">
    • 연속 숫자 패턴<br>
    • 키보드 패턴<br>
    • 날짜 패턴<br>
    • Zipf 법칙 분석
    </div>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
<div class="card">
    <div class="card-title">③ 정보보안 분석</div>
    <div class="card-text">
    • Dictionary Attack<br>
    • Brute Force Attack<br>
    • 비밀번호 강도 분석<br>
    • 보안적 의미 해석
    </div>
</div>
""", unsafe_allow_html=True)

with col4:
    st.markdown("""
<div class="card">
    <div class="card-title">④ 비밀번호 안전도 측정</div>
    <div class="card-text">
    • 희귀도 분석<br>
    • 엔트로피 계산<br>
    • 패턴 탐지<br>
    • 예상 크래킹 시간 측정
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# 핵심 질문
# =========================
st.markdown("""
<div class="question-box">
    <h2>🧠 핵심 연구 질문</h2>
    <p>
    인간이 만든 비밀번호는 정말 랜덤할까?<br><br>
    만약 랜덤하지 않다면,<br>
    그 규칙성은 정보보안에 어떤 영향을 미칠까?
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# 데이터셋
# =========================
st.divider()

st.header("📊 사용 데이터")

col1, col2 = st.columns(2)

with col1:
    st.success("""
### Common Passwords Dataset

일반적으로 많이 사용되는 비밀번호 데이터
""")

with col2:
    st.success("""
### RockYou Dataset

실제 유출된 대규모 비밀번호 데이터
""")

# =========================
# Footer
# =========================
st.markdown("""
<div class="footer">
통계물리학 × 정보보안 융합 탐구 프로젝트
</div>
""", unsafe_allow_html=True)
