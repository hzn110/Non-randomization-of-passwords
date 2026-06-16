import streamlit as st

st.set_page_config(
    page_title="인간이 만든 비밀번호는 정말 랜덤할까?",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================
# CSS (Apple Liquid Glass)
# ======================
st.markdown("""
<style>

/* 전체 배경 - 은은한 그라데이션 + 블러 처리된 컬러 오브 */
.stApp{
    background:
        radial-gradient(circle at 15% 20%, rgba(120,160,255,0.35) 0%, transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(255,120,200,0.30) 0%, transparent 45%),
        radial-gradient(circle at 50% 90%, rgba(120,255,210,0.25) 0%, transparent 50%),
        linear-gradient(160deg, #0b0c10 0%, #14151c 50%, #0b0c10 100%);
    background-attachment: fixed;
}

.block-container{
    padding-top:2rem;
    max-width:1200px;
}

/* 사이드바 숨김 느낌 정리 */
section[data-testid="stSidebar"]{
    display:none;
}

/* ---------- Hero ---------- */
.hero{
    text-align:center;
    padding:5rem 1rem 2rem 1rem;
}

.hero-badge{
    display:inline-block;
    padding:6px 18px;
    border-radius:999px;
    background:rgba(255,255,255,0.06);
    border:1px solid rgba(255,255,255,0.14);
    backdrop-filter: blur(20px);
    color:rgba(255,255,255,0.75);
    font-size:0.85rem;
    letter-spacing:0.05em;
    margin-bottom:1.2rem;
}

.hero-title{
    font-size:3.4rem;
    font-weight:800;
    line-height:1.25;
    letter-spacing:-0.02em;
    background:linear-gradient(135deg, #ffffff 0%, #b9c2ff 50%, #ffd1ef 100%);
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
}

.hero-subtitle{
    margin-top:18px;
    color:rgba(255,255,255,0.55);
    font-size:1.15rem;
    font-weight:500;
    letter-spacing:0.04em;
}

/* ---------- Liquid Glass 공통 카드 ---------- */
.glass{
    position:relative;
    background:linear-gradient(135deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.03) 100%);
    backdrop-filter: blur(28px) saturate(180%);
    -webkit-backdrop-filter: blur(28px) saturate(180%);
    border:1px solid rgba(255,255,255,0.14);
    border-radius:28px;
    padding:32px;
    margin-bottom:22px;
    box-shadow:
        0 8px 32px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.18);
    transition: all 0.35s ease;
}

.glass:hover{
    background:linear-gradient(135deg, rgba(255,255,255,0.16) 0%, rgba(255,255,255,0.05) 100%);
    border-color:rgba(255,255,255,0.28);
    transform: translateY(-4px);
    box-shadow:
        0 16px 40px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.25);
}

/* 통계 숫자 카드 */
.stat-card{
    text-align:center;
    padding:28px 10px;
}

.big-number{
    font-size:2.6rem;
    font-weight:800;
    background:linear-gradient(135deg, #ffffff 0%, #aab6ff 100%);
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
}

.big-label{
    margin-top:6px;
    color:rgba(255,255,255,0.55);
    font-size:0.95rem;
    letter-spacing:0.03em;
}

/* 섹션 타이틀 */
.section-title{
    font-size:1.6rem;
    font-weight:700;
    color:rgba(255,255,255,0.92);
    margin: 2.4rem 0 1.2rem 0;
    letter-spacing:-0.01em;
}

/* 카드 내부 텍스트 */
.card-icon{
    font-size:2rem;
    margin-bottom:10px;
}

.card-title{
    font-size:1.25rem;
    font-weight:700;
    color:rgba(255,255,255,0.95);
}

.card-desc{
    color:rgba(255,255,255,0.55);
    margin-top:10px;
    font-size:0.95rem;
    line-height:1.6;
    min-height:78px;
}

/* 핵심 질문 박스 */
.question{
    text-align:center;
    padding:60px 30px;
    margin-top:30px;
    font-size:1.05rem;
    line-height:2;
    color:rgba(255,255,255,0.85);
}

.question h2{
    font-size:1.8rem;
    margin-bottom:1.2rem;
    background:linear-gradient(135deg, #ffffff 0%, #ffd1ef 100%);
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
}

</style>
""", unsafe_allow_html=True)

# ======================
# Hero
# ======================
st.markdown("""
<div class="hero">

<div class="hero-badge">STATISTICAL PHYSICS × INFORMATION SECURITY</div>

<div class="hero-title">
🔐 인간이 만든 비밀번호는<br>
정말 랜덤할까?
</div>

<div class="hero-subtitle">
실제 유출 비밀번호 데이터로 살펴보는 인간 선택의 패턴
</div>

</div>
""", unsafe_allow_html=True)

# ======================
# 통계 카드
# ======================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass stat-card">
    <div class="big-number">1400만+</div>
    <div class="big-label">분석 대상 비밀번호</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass stat-card">
    <div class="big-number">100+</div>
    <div class="big-label">발견된 패턴</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass stat-card">
    <div class="big-number">2</div>
    <div class="big-label">융합 학문 분야</div>
    </div>
    """, unsafe_allow_html=True)

# ======================
# 프로젝트 소개
# ======================
st.markdown('<div class="section-title">프로젝트 소개</div>', unsafe_allow_html=True)

st.markdown("""
<div class="glass">
우리는 비밀번호를 만들 때 스스로는 무작위라고 생각한다.<br><br>
하지만 실제 비밀번호 데이터는 인간이 반복적으로 특정 규칙을 사용한다는 사실을 보여준다.<br><br>
본 프로젝트는 실제 유출 비밀번호 데이터를 활용하여 인간의 선택 행동을 통계물리학적으로 분석하고,
그 결과를 정보보안 관점에서 해석하는 것을 목표로 한다.
</div>
""", unsafe_allow_html=True)

# ======================
# 연구 진행 과정 (페이지 1~4 소개 및 이동)
# ======================
st.markdown('<div class="section-title">연구 진행 과정</div>', unsafe_allow_html=True)

pages_info = [
    {
        "icon": "📊",
        "title": "① 생성 과정 분석",
        "desc": "비밀번호 길이, 문자 구성, 엔트로피를 분석하여 인간이 비밀번호를 만드는 과정을 탐구한다.",
        "path": "pages/00_비밀번호 생성의 원리.py",
        "label": "생성 과정 분석으로 이동"
    },
    {
        "icon": "🔁",
        "title": "② 규칙성 검증",
        "desc": "연속 숫자, 키보드 배열, 날짜 패턴 등을 통해 인간 선택의 보편성을 검증한다.",
        "path": "pages/01_비밀번호의 규칙성.py",
        "label": "규칙성 검증으로 이동"
    },
    {
        "icon": "🛡️",
        "title": "③ 정보보안 분석",
        "desc": "발견된 규칙성이 실제 공격 환경에서 어떤 위험을 만드는지 분석한다.",
        "path": "pages/02_비번 보안.py",
        "label": "정보보안 분석으로 이동"
    },
    {
        "icon": "🔑",
        "title": "④ 비밀번호 안전도 측정",
        "desc": "사용자가 입력한 비밀번호의 희귀도와 안전도를 평가한다.",
        "path": "pages/03_비번 평가.py",
        "label": "비밀번호 안전도 측정으로 이동"
    },
]

row1 = st.columns(2)
row2 = st.columns(2)
cols = row1 + row2

for col, info in zip(cols, pages_info):
    with col:
        st.markdown(f"""
        <div class="glass">
        <div class="card-icon">{info['icon']}</div>
        <div class="card-title">{info['title']}</div>
        <div class="card-desc">{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(info["path"], label=f"**{info['label']} →**")

# ======================
# 핵심 연구 질문
# ======================
st.markdown("""
<div class="glass question">

<h2>🧠 핵심 연구 질문</h2>

인간이 만든 비밀번호는 정말 랜덤할까?<br>
그리고 그 비무작위성은 정보보안에 어떤 영향을 미칠까?

</div>
""", unsafe_allow_html=True)
