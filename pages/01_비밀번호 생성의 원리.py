import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
import os

st.set_page_config(
    page_title="인간은 어떻게 비밀번호를 만드는가?",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# 다크/라이트 모드 상태 (메인과 공유)
# ======================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# ======================
# 다크/라이트 CSS 변수 (메인과 동일)
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
    chart_bg  = "rgba(0,0,0,0)"
    chart_paper = "rgba(0,0,0,0)"
    chart_font  = "rgba(220,210,255,0.80)"
    bar_color   = "#a78bfa"
    bar_color2  = "#f9a8d4"
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
    chart_bg  = "rgba(0,0,0,0)"
    chart_paper = "rgba(0,0,0,0)"
    chart_font  = "rgba(60,60,100,0.80)"
    bar_color   = "#7c3aed"
    bar_color2  = "#db2777"

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
section[data-testid="stSidebar"] * {{ color: {text_main} !important; }}
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p {{ color: {text_main} !important; opacity:1 !important; }}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {{
    color: {text_main} !important; background: transparent; border-radius: 10px; transition: background 0.2s;
}}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {{ background: {badge_bg} !important; }}

.glass {{
    position: relative;
    background: {glass_bg};
    backdrop-filter: blur(40px) saturate(180%) brightness(1.08);
    -webkit-backdrop-filter: blur(40px) saturate(180%) brightness(1.08);
    border: 1px solid {border};
    border-radius: 28px;
    padding: 30px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px {shadow}, inset 0 1px 0 rgba(255,255,255,0.18), inset 0 -1px 0 rgba(255,255,255,0.04);
    transition: all 0.32s cubic-bezier(.4,0,.2,1);
}}
.glass:hover {{
    background: {glass_hov};
    border-color: {border_hov};
    transform: translateY(-3px);
    box-shadow: 0 14px 36px {shadow_hov}, inset 0 1px 0 rgba(255,255,255,0.28);
}}
.page-hero {{
    text-align: center;
    padding: 2.8rem 1rem 1.4rem 1rem;
}}
.page-badge {{
    display: inline-block;
    padding: 5px 18px;
    border-radius: 999px;
    background: {badge_bg};
    border: 1px solid {border};
    color: {text_sub};
    font-size: 0.8rem;
    letter-spacing: 0.06em;
    font-weight: 600;
    margin-bottom: 1rem;
}}
.page-title {{
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.25;
    letter-spacing: -0.02em;
    background: {title_grad};
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}
.page-subtitle {{
    margin-top: 14px;
    color: {text_sub};
    font-size: 1.05rem;
    font-weight: 500;
}}
.section-title {{
    font-size: 1.4rem;
    font-weight: 700;
    color: {text_main};
    margin: 2rem 0 0.8rem 0;
    letter-spacing: -0.01em;
}}
.stat-row {{
    text-align: center;
    padding: 20px 10px;
}}
.big-number {{
    font-size: 2.2rem;
    font-weight: 800;
    background: {num_grad};
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}
.big-label {{
    margin-top: 5px;
    color: {text_sub};
    font-size: 0.88rem;
}}
.body-text {{
    color: {text_sub};
    line-height: 1.85;
    font-size: 0.97rem;
}}
.conclusion-box {{
    background: {glass_bg};
    backdrop-filter: blur(40px) saturate(180%);
    -webkit-backdrop-filter: blur(40px) saturate(180%);
    border: 1px solid {border};
    border-radius: 28px;
    padding: 40px 36px;
    margin-top: 24px;
    text-align: center;
    color: {text_sub};
    line-height: 2;
    font-size: 1rem;
    box-shadow: 0 4px 24px {shadow}, inset 0 1px 0 rgba(255,255,255,0.18);
}}
.conclusion-title {{
    font-size: 1.6rem;
    font-weight: 800;
    margin-bottom: 1rem;
    background: {title_grad};
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}
</style>
""", unsafe_allow_html=True)

# ======================
# 사이드바 — 모드 토글 + 용어 사전
# ======================
with st.sidebar:
    label = "☀️ 라이트 모드" if dark else "🌙 다크 모드"
    if st.button(label, key="mode_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    st.divider()
    st.markdown(f"**📚 용어 사전**")
    with st.expander("미시상태 (Microstate)"):
        st.write("비밀번호 하나하나를 개별 미시상태로 본다.\n\n예) abc123, qwerty, password")
    with st.expander("거시상태 (Macrostate)"):
        st.write("문자 구조만 남긴 형태.\n\nPassword123! → Ulllllllddds\n\n같은 구조를 가진 비밀번호는 같은 거시상태.")
    with st.expander("엔트로피 (Entropy)"):
        st.write("얼마나 다양하고 예측하기 어려운지를 나타낸다.\n\n높을수록 무작위, 낮을수록 특정 패턴에 집중.")
    with st.expander("질서변수 (Order Parameter)"):
        st.write("특정 상태에 얼마나 집중되어 있는지.\n\n0 = 완전 무질서, 1 = 완전 질서")
    with st.expander("자기조직화 (Self-Organization)"):
        st.write("누가 규칙을 만든 것이 아닌데도\n\n집단 전체에서 자연스럽게 질서가 나타나는 현상.")

# ======================
# 데이터 로드
# ======================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "rockyou_rigorous_behavioral_physics_v2.csv")
    return pd.read_csv(path)

try:
    df = load_data()
    DATA_OK = True
except Exception:
    df = None
    DATA_OK = False

AVG_BIAS    = 0.159
AVG_ENTROPY = 2.678
AVG_ORDER   = 0.716

def apply_chart_theme(fig):
    fig.update_layout(
        paper_bgcolor=chart_paper,
        plot_bgcolor=chart_bg,
        font_color=chart_font,
        font_family="-apple-system, BlinkMacSystemFont, sans-serif",
        margin=dict(t=40, b=20, l=10, r=10),
    )
    fig.update_xaxes(gridcolor=border, zerolinecolor=border)
    fig.update_yaxes(gridcolor=border, zerolinecolor=border)
    return fig

# ======================
# Hero
# ======================
st.markdown(f"""
<div class="page-hero">
    <div class="page-badge">① 생성 과정 분석</div>
    <div class="page-title">인간은 어떻게<br>비밀번호를 만드는가?</div>
    <div class="page-subtitle">통계역학적 관점에서 분석한 인간의 비밀번호 생성 과정</div>
</div>
""", unsafe_allow_html=True)

# 탐구 질문
st.markdown(f"""
<div class="glass" style="text-align:center; padding:28px 30px;">
    <div style="color:{text_hint}; font-size:0.82rem; letter-spacing:0.06em; font-weight:600; margin-bottom:10px;">🎯 탐구 질문</div>
    <div style="color:{text_main}; font-size:1.1rem; font-weight:600; line-height:1.8;">
        인간은 랜덤한 비밀번호를 만든다고 생각한다.<br>
        그런데 정말 그럴까?
    </div>
</div>
""", unsafe_allow_html=True)


# ======================
# SECTION 1 — 작은 편향은 어떤 결과를 만들까?
# ======================
st.markdown(f'<div class="section-title">2️⃣ 작은 편향은 어떤 결과를 만들까?</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="glass">
    <div class="body-text">
    편향 강도를 조절해보자.<br>
    편향이 조금만 생겨도 상태 분포가 얼마나 빠르게 쏠리는지 확인할 수 있다.
    </div>
</div>
""", unsafe_allow_html=True)

bias_strength = st.slider("인간의 편향 강도", 0, 100, 20, key="bias_slider")
states = np.arange(20)
weights = np.exp(bias_strength / 25 * np.linspace(0, 1, 20))
weights /= weights.sum()

sim_df = pd.DataFrame({"상태 번호": states, "선택 확률": weights})
fig = px.bar(sim_df, x="상태 번호", y="선택 확률",
             color_discrete_sequence=[bar_color], title="상태 분포 — 편향 강도에 따른 변화")
fig = apply_chart_theme(fig)
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
<div class="glass">
    <div class="body-text">
    편향 강도 <strong>{bias_strength}%</strong> — 
    편향이 커질수록 특정 상태가 선택될 확률이 집중된다.<br>
    완전히 랜덤하면 모든 막대가 같은 높이여야 한다.
    </div>
</div>
""", unsafe_allow_html=True)

# ======================
# SECTION 2 — 사람이 많아지면?
# ======================
st.markdown(f'<div class="section-title">3️⃣ 사람이 많아지면 무슨 일이 일어날까?</div>', unsafe_allow_html=True)

population = st.slider("비밀번호를 만드는 사람 수", 1, 100000, 5000, step=1000, key="pop_slider")

samples = np.random.choice(states, size=population, p=weights)
freq = pd.Series(samples).value_counts()
concentration = freq.max() / population

fig = px.histogram(x=samples, nbins=20, color_discrete_sequence=[bar_color2],
                   title=f"집단 선택 결과 — {population:,}명의 선택 분포")
fig = apply_chart_theme(fig)
fig.update_layout(xaxis_title="상태 번호", yaxis_title="선택 횟수")
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="glass stat-row">
        <div class="big-number">{concentration:.3f}</div>
        <div class="big-label">집중도 (최고 빈도 / 전체)</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="glass stat-row">
        <div class="big-number">{population:,}</div>
        <div class="big-label">시뮬레이션 인원</div>
    </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class="glass">
    <div class="body-text">
    한 사람은 랜덤하게 선택할 수 있다.<br>
    하지만 사람이 많아질수록 특정 상태에 선택이 집중된다.<br><br>
    이것이 통계역학에서 말하는 <strong>거시적 질서의 출현</strong>이다.
    </div>
</div>
""", unsafe_allow_html=True)

# ======================
# SECTION 3 — 질서변수 관찰
# ======================
st.markdown(f'<div class="section-title">4️⃣ 질서변수(Order Parameter)를 관찰해보자</div>', unsafe_allow_html=True)

order = concentration
fig = go.Figure()
fig.add_bar(x=["현재 시뮬레이션", "실제 데이터 (RockYou)"],
            y=[order, AVG_ORDER],
            marker_color=[bar_color, bar_color2],
            text=[f"{order:.3f}", f"{AVG_ORDER}"],
            textposition="outside")
fig = apply_chart_theme(fig)
fig.update_layout(title="Order Parameter 비교", yaxis_title="Order Parameter", yaxis_range=[0, 1.1])
st.plotly_chart(fig, use_container_width=True)

if order > 0.5:
    status_text = f"질서 상태가 형성되었다. (Order Parameter = {order:.3f})<br>집단은 더 이상 랜덤하지 않다."
    status_color = "rgba(120,255,180,0.30)"
else:
    status_text = f"아직 무질서 상태에 가깝다. (Order Parameter = {order:.3f})<br>편향 강도를 높이면 질서 상태로 전환된다."
    status_color = "rgba(255,200,100,0.25)"

st.markdown(f"""
<div class="glass" style="border-color:{status_color};">
    <div class="body-text">{status_text}</div>
</div>
""", unsafe_allow_html=True)

# ======================
# SECTION 4 — 발견 요약 (실제 데이터)
# ======================
st.markdown(f'<div class="section-title">5️⃣ 실제 데이터에서 무엇을 발견했을까?</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
findings = [
    ("편향 존재", f"평균 편향 {AVG_BIAS}"),
    ("상태 집중", "상위 10개 구조가\n대다수 차지"),
    ("질서 형성", f"Order Parameter\n평균 {AVG_ORDER}"),
    ("자기조직화", "규칙 없이\n패턴 반복"),
]
icons = ["🎯", "📌", "🔮", "🌀"]
for col, (title, desc), icon in zip([col1, col2, col3, col4], findings, icons):
    with col:
        st.markdown(f"""
        <div class="glass stat-row">
            <div style="font-size:1.8rem; margin-bottom:8px;">{icon}</div>
            <div style="font-size:1rem; font-weight:700; color:{text_main};">{title}</div>
            <div class="big-label" style="margin-top:6px; white-space:pre-line;">{desc}</div>
        </div>""", unsafe_allow_html=True)

if DATA_OK:
    st.markdown(f'<div class="section-title" style="margin-top:1.5rem;">📈 실제 Shannon Entropy 분포</div>', unsafe_allow_html=True)
    fig = px.histogram(df, x="shannon_entropy", nbins=50,
                       color_discrete_sequence=[bar_color],
                       title="RockYou 데이터셋 Shannon Entropy 분포")
    fig = apply_chart_theme(fig)
    fig.update_layout(xaxis_title="Shannon Entropy (bits)", yaxis_title="비밀번호 수")
    st.plotly_chart(fig, use_container_width=True)

# ======================
# 결론
# ======================
st.markdown(f"""
<div class="conclusion-box">
    <div class="conclusion-title">📌 결론</div>
    실제 데이터의 평균 질서변수는 <strong>{AVG_ORDER}</strong> 이다.<br><br>
    이는 사람들의 비밀번호가 완전히 랜덤하게 생성되지 않는다는 의미이다.<br><br>
    개인의 작은 편향은 집단 수준에서 증폭되고,<br>
    결국 특정 구조가 반복적으로 선택된다.<br><br>
    즉, 비밀번호 생성은 통계역학에서 말하는<br>
    <strong>자기조직화(Self-Organization)</strong>의 한 예로 볼 수 있다.<br><br>
    <span style="color:{text_hint}; font-size:0.9rem;">➡ 다음 페이지에서는 실제 데이터에서 어떤 규칙성이 발견되는지 검증한다.</span>
</div>
""", unsafe_allow_html=True)
