import streamlit as st

st.set_page_config(
    page_title="인간이 만든 비밀번호는 정말 랜덤할까?",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# 다크/라이트 모드 상태
# ======================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# ======================
# 다크/라이트 CSS 변수 정의
# ======================
if dark:
    bg_main   = "radial-gradient(circle at 20% 25%, rgba(160,130,255,0.22) 0%, transparent 50%), radial-gradient(circle at 80% 12%, rgba(220,130,255,0.18) 0%, transparent 50%), radial-gradient(circle at 50% 88%, rgba(100,170,255,0.16) 0%, transparent 55%), linear-gradient(160deg, rgba(18,14,48,0.92) 0%, rgba(22,14,52,0.88) 50%, rgba(16,12,42,0.92) 100%)"
    glass_bg  = "linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(200,180,255,0.03) 100%)"
    glass_hov = "linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(200,180,255,0.07) 100%)"
    border    = "rgba(200,180,255,0.15)"
    border_hov= "rgba(220,200,255,0.32)"
    text_main = "rgba(255,255,255,0.95)"
    text_sub  = "rgba(220,210,255,0.60)"
    text_hint = "rgba(180,170,255,0.35)"
    badge_bg  = "rgba(200,180,255,0.07)"
    shadow    = "rgba(60,30,120,0.18)"
    shadow_hov= "rgba(80,40,160,0.28)"
    sidebar_bg= "rgba(18,12,45,0.50)"
    sidebar_br= "rgba(200,180,255,0.10)"
    title_grad= "linear-gradient(135deg,#e8e0ff 0%,#c4b5ff 50%,#f9c6ff 100%)"
    num_grad  = "linear-gradient(135deg,#ffffff 0%,#c4b5ff 100%)"
    q_grad    = "linear-gradient(135deg,#e8e0ff 0%,#f9c6ff 100%)"
    arrow_col = "rgba(200,180,255,0.50)"
    arrow_hov = "#e8e0ff"
    link_bg   = "rgba(200,180,255,0.07)"
    link_hov  = "rgba(200,180,255,0.16)"
    link_text = "rgba(220,210,255,0.88)"
else:
    bg_main   = "radial-gradient(circle at 15% 20%, rgba(100,140,255,0.12) 0%, transparent 45%), radial-gradient(circle at 85% 15%, rgba(255,100,180,0.10) 0%, transparent 45%), radial-gradient(circle at 50% 90%, rgba(80,220,180,0.10) 0%, transparent 50%), linear-gradient(160deg,#f0f2ff 0%,#faf5ff 50%,#f0f8ff 100%)"
    glass_bg  = "linear-gradient(135deg, rgba(255,255,255,0.72) 0%, rgba(255,255,255,0.45) 100%)"
    glass_hov = "linear-gradient(135deg, rgba(255,255,255,0.90) 0%, rgba(255,255,255,0.65) 100%)"
    border    = "rgba(120,120,180,0.18)"
    border_hov= "rgba(100,100,220,0.38)"
    text_main = "rgba(30,30,60,0.95)"
    text_sub  = "rgba(60,60,100,0.65)"
    text_hint = "rgba(100,100,160,0.55)"
    badge_bg  = "rgba(100,100,220,0.09)"
    shadow    = "rgba(100,100,200,0.10)"
    shadow_hov= "rgba(100,100,200,0.22)"
    sidebar_bg= "rgba(255,255,255,0.55)"
    sidebar_br= "rgba(180,180,220,0.20)"
    title_grad= "linear-gradient(135deg,#3b3bb0 0%,#7c3aed 50%,#db2777 100%)"
    num_grad  = "linear-gradient(135deg,#3b3bb0 0%,#6366f1 100%)"
    q_grad    = "linear-gradient(135deg,#3b3bb0 0%,#db2777 100%)"
    arrow_col = "rgba(80,80,180,0.55)"
    arrow_hov = "#3b3bb0"
    link_bg   = "rgba(100,100,220,0.08)"
    link_hov  = "rgba(100,100,220,0.18)"
    link_text = "rgba(40,40,120,0.90)"

st.markdown(f"""
<style>

.stApp {{
    background: {bg_main};
    background-attachment: fixed;
}}

.block-container {{
    padding-top: 1.5rem;
    max-width: 1200px;
}}

section[data-testid="stSidebar"] {{
    background: {sidebar_bg};
    border-right: 1px solid {sidebar_br};
    backdrop-filter: blur(20px);
}}

/* 사이드바 텍스트 색상 (라이트모드에서 안 보이는 문제 해결) */
section[data-testid="stSidebar"] * {{
    color: {text_main} !important;
}}

section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p {{
    color: {text_main} !important;
    opacity: 1 !important;
}}

section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {{
    color: {text_main} !important;
    background: transparent;
    border-radius: 10px;
    transition: background 0.2s;
}}

section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {{
    background: {badge_bg} !important;
}}

/* ---------- Hero ---------- */
.hero {{
    text-align: center;
    padding: 4rem 1rem 1.8rem 1rem;
}}

.hero-badge {{
    display: inline-block;
    padding: 6px 20px;
    border-radius: 999px;
    background: {badge_bg};
    border: 1px solid {border};
    backdrop-filter: blur(20px);
    color: {text_sub};
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    margin-bottom: 1.2rem;
    font-weight: 600;
}}

.hero-title {{
    font-size: 3.4rem;
    font-weight: 800;
    line-height: 1.22;
    letter-spacing: -0.025em;
    background: {title_grad};
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.hero-subtitle {{
    margin-top: 18px;
    color: {text_sub};
    font-size: 1.1rem;
    font-weight: 500;
    letter-spacing: 0.03em;
}}

/* ---------- Liquid Glass 카드 ---------- */
.glass {{
    position: relative;
    background: {glass_bg};
    backdrop-filter: blur(40px) saturate(180%) brightness(1.08);
    -webkit-backdrop-filter: blur(40px) saturate(180%) brightness(1.08);
    border: 1px solid {border};
    border-radius: 28px;
    padding: 30px;
    margin-bottom: 20px;
    box-shadow:
        0 4px 24px {shadow},
        inset 0 1px 0 rgba(255,255,255,0.18),
        inset 0 -1px 0 rgba(255,255,255,0.04);
    transition: all 0.32s cubic-bezier(.4,0,.2,1);
}}

.glass:hover {{
    background: {glass_hov};
    border-color: {border_hov};
    transform: translateY(-5px);
    box-shadow:
        0 14px 36px {shadow_hov},
        inset 0 1px 0 rgba(255,255,255,0.28),
        inset 0 -1px 0 rgba(255,255,255,0.08);
}}

/* 통계 카드 */
.stat-card {{
    text-align: center;
    padding: 26px 10px;
}}

.big-number {{
    font-size: 2.5rem;
    font-weight: 800;
    background: {num_grad};
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.big-label {{
    margin-top: 6px;
    color: {text_sub};
    font-size: 0.92rem;
    letter-spacing: 0.02em;
}}

/* 섹션 타이틀 */
.section-title {{
    font-size: 1.55rem;
    font-weight: 700;
    color: {text_main};
    margin: 2.2rem 0 1rem 0;
    letter-spacing: -0.01em;
}}

/* 카드 내부 */
.card-icon {{
    font-size: 2rem;
    margin-bottom: 10px;
}}

.card-title {{
    font-size: 1.2rem;
    font-weight: 700;
    color: {text_main};
}}

.card-desc {{
    color: {text_sub};
    margin-top: 10px;
    font-size: 0.93rem;
    line-height: 1.65;
    min-height: 74px;
}}

/* 카드 링크 버튼 */
.card-link {{
    display: inline-block;
    margin-top: 16px;
    padding: 9px 20px;
    border-radius: 999px;
    background: {link_bg};
    border: 1px solid {border};
    color: {link_text} !important;
    font-size: 0.88rem;
    font-weight: 600;
    text-decoration: none !important;
    transition: all 0.22s ease;
    cursor: pointer;
}}

.card-link:hover {{
    background: {link_hov};
    border-color: {border_hov};
    transform: translateX(3px);
}}

.card-link .arrow {{
    margin-left: 5px;
    display: inline-block;
    transition: transform 0.2s ease;
}}

.card-link:hover .arrow {{
    transform: translateX(4px);
}}

/* 클릭 가능한 전체 카드 래퍼 */
a.card-wrap {{
    text-decoration: none !important;
    color: inherit;
    display: block;
    cursor: pointer;
}}

/* 핵심 질문 */
.question {{
    text-align: center;
    padding: 55px 30px;
    margin-top: 28px;
    font-size: 1.05rem;
    line-height: 2;
    color: {text_sub};
}}

.question h2 {{
    font-size: 1.75rem;
    margin-bottom: 1rem;
    background: {q_grad};
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: 800;
}}

/* Streamlit 기본 버튼 숨기기 (mode toggle 제외) */
div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] {{
    gap: 0;
}}

</style>
""", unsafe_allow_html=True)

# ======================
# 다크/라이트 모드 토글 (사이드바 상단)
# ======================
with st.sidebar:
    label = "☀️ 라이트 모드" if dark else "🌙 다크 모드"
    if st.button(label, key="mode_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    st.divider()

# ======================
# Hero
# ======================
st.markdown(f"""
<div class="hero">
<div class="hero-badge">STATISTICAL PHYSICS × INFORMATION SECURITY</div>
<div class="hero-title">🔐 인간이 만든 비밀번호는<br>정말 랜덤할까?</div>
<div class="hero-subtitle">실제 유출 비밀번호 데이터로 살펴보는 인간 선택의 패턴</div>
</div>
""", unsafe_allow_html=True)

# ======================
# 통계 카드
# ======================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="glass stat-card">
    <div class="big-number">1400만+</div>
    <div class="big-label">분석 대상 비밀번호</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass stat-card">
    <div class="big-number">100+</div>
    <div class="big-label">발견된 패턴</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass stat-card">
    <div class="big-number">2</div>
    <div class="big-label">융합 학문 분야</div>
    </div>
    """, unsafe_allow_html=True)

# ======================
# 프로젝트 소개
# ======================
st.markdown(f'<div class="section-title">프로젝트 소개</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="glass" style="color:{text_sub}; line-height:1.9;">
우리는 비밀번호를 만들 때 스스로는 무작위라고 생각한다.<br><br>
하지만 실제 비밀번호 데이터는 인간이 반복적으로 특정 규칙을 사용한다는 사실을 보여준다.<br><br>
본 프로젝트는 실제 유출 비밀번호 데이터를 활용하여 인간의 선택 행동을 통계물리학적으로 분석하고,
그 결과를 정보보안 관점에서 해석하는 것을 목표로 한다.
</div>
""", unsafe_allow_html=True)

# ======================
# 연구 진행 과정
# ======================
st.markdown(f'<div class="section-title">연구 진행 과정</div>', unsafe_allow_html=True)

pages_info = [
    {
        "icon": "📊",
        "title": "① 생성 과정 분석",
        "desc": "비밀번호 길이, 문자 구성, 엔트로피를 분석하여 인간이 비밀번호를 만드는 과정을 탐구한다.",
        "path": "pages/00_비밀번호 생성의 원리.py",
        "label": "생성 과정 분석으로 이동",
        "url": "/비밀번호_생성의_원리"
    },
    {
        "icon": "🔁",
        "title": "② 규칙성 검증",
        "desc": "연속 숫자, 키보드 배열, 날짜 패턴 등을 통해 인간 선택의 보편성을 검증한다.",
        "path": "pages/01_비밀번호의 규칙성.py",
        "label": "규칙성 검증으로 이동",
        "url": "/비밀번호의_규칙성"
    },
    {
        "icon": "🛡️",
        "title": "③ 정보보안 분석",
        "desc": "발견된 규칙성이 실제 공격 환경에서 어떤 위험을 만드는지 분석한다.",
        "path": "pages/02_비번 보안.py",
        "label": "정보보안 분석으로 이동",
        "url": "/비번_보안"
    },
    {
        "icon": "🔑",
        "title": "④ 비밀번호 안전도 측정",
        "desc": "사용자가 입력한 비밀번호의 희귀도와 안전도를 평가한다.",
        "path": "pages/03_비번 평가.py",
        "label": "비밀번호 안전도 측정으로 이동",
        "url": "/비번_평가"
    },
]

row1 = st.columns(2)
row2 = st.columns(2)
cols = row1 + row2

for col, info in zip(cols, pages_info):
    with col:
        st.markdown(f"""
        <a class="card-wrap" href="{info['url']}" target="_self">
        <div class="glass">
        <div class="card-icon">{info['icon']}</div>
        <div class="card-title">{info['title']}</div>
        <div class="card-desc">{info['desc']}</div>
        <span class="card-link">{info['label']}<span class="arrow">→</span></span>
        </div>
        </a>
        """, unsafe_allow_html=True)

# ======================
# 핵심 연구 질문
# ======================
st.markdown(f"""
<div class="glass question">
<h2>🧠 핵심 연구 질문</h2>
인간이 만든 비밀번호는 정말 랜덤할까?<br>
그리고 그 비무작위성은 정보보안에 어떤 영향을 미칠까?
</div>
""", unsafe_allow_html=True)
