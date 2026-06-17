import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import time
from collections import Counter

st.set_page_config(
    page_title="인간의 비밀번호에는 규칙성이 존재하는가?",
    page_icon="🔁",
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
# CSS 변수 (메인과 동일)
# ======================
if dark:
    bg_main    = "radial-gradient(circle at 20% 25%, rgba(160,130,255,0.22) 0%, transparent 50%), radial-gradient(circle at 80% 12%, rgba(220,130,255,0.18) 0%, transparent 50%), radial-gradient(circle at 50% 88%, rgba(100,170,255,0.16) 0%, transparent 55%), linear-gradient(160deg, rgba(18,14,48,0.92) 0%, rgba(22,14,52,0.88) 50%, rgba(16,12,42,0.92) 100%)"
    glass_bg   = "linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(200,180,255,0.03) 100%)"
    glass_hov  = "linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(200,180,255,0.07) 100%)"
    border     = "rgba(200,180,255,0.15)"
    border_hov = "rgba(220,200,255,0.32)"
    text_main  = "rgba(255,255,255,0.95)"
    text_sub   = "rgba(220,210,255,0.60)"
    text_hint  = "rgba(180,170,255,0.35)"
    badge_bg   = "rgba(200,180,255,0.07)"
    shadow     = "rgba(60,30,120,0.18)"
    shadow_hov = "rgba(80,40,160,0.28)"
    sidebar_bg = "rgba(18,12,45,0.50)"
    sidebar_br = "rgba(200,180,255,0.10)"
    title_grad = "linear-gradient(135deg,#e8e0ff 0%,#c4b5ff 50%,#f9c6ff 100%)"
    num_grad   = "linear-gradient(135deg,#ffffff 0%,#c4b5ff 100%)"
    chart_font = "rgba(220,210,255,0.80)"
    bar_color  = "#a78bfa"
    bar_color2 = "#f9a8d4"
    bar_color3 = "#6ee7b7"
    success_border = "rgba(110,231,183,0.35)"
    danger_border  = "rgba(255,120,120,0.35)"
    warn_border    = "rgba(255,200,100,0.30)"
else:
    bg_main    = "radial-gradient(circle at 15% 20%, rgba(100,140,255,0.12) 0%, transparent 45%), radial-gradient(circle at 85% 15%, rgba(255,100,180,0.10) 0%, transparent 45%), radial-gradient(circle at 50% 90%, rgba(80,220,180,0.10) 0%, transparent 50%), linear-gradient(160deg,#f0f2ff 0%,#faf5ff 50%,#f0f8ff 100%)"
    glass_bg   = "linear-gradient(135deg, rgba(255,255,255,0.72) 0%, rgba(255,255,255,0.45) 100%)"
    glass_hov  = "linear-gradient(135deg, rgba(255,255,255,0.90) 0%, rgba(255,255,255,0.65) 100%)"
    border     = "rgba(120,120,180,0.18)"
    border_hov = "rgba(100,100,220,0.38)"
    text_main  = "rgba(30,30,60,0.95)"
    text_sub   = "rgba(60,60,100,0.65)"
    text_hint  = "rgba(100,100,160,0.55)"
    badge_bg   = "rgba(100,100,220,0.09)"
    shadow     = "rgba(100,100,200,0.10)"
    shadow_hov = "rgba(100,100,200,0.22)"
    sidebar_bg = "rgba(255,255,255,0.55)"
    sidebar_br = "rgba(180,180,220,0.20)"
    title_grad = "linear-gradient(135deg,#3b3bb0 0%,#7c3aed 50%,#db2777 100%)"
    num_grad   = "linear-gradient(135deg,#3b3bb0 0%,#6366f1 100%)"
    chart_font = "rgba(60,60,100,0.80)"
    bar_color  = "#7c3aed"
    bar_color2 = "#db2777"
    bar_color3 = "#059669"
    success_border = "rgba(5,150,105,0.35)"
    danger_border  = "rgba(220,38,38,0.30)"
    warn_border    = "rgba(180,130,0,0.25)"

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
    color: {text_main} !important; background: transparent;
    border-radius: 10px; transition: background 0.2s;
}}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {{
    background: {badge_bg} !important;
}}
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
.body-text {{
    color: {text_sub};
    line-height: 1.85;
    font-size: 0.97rem;
}}
.rank-card {{
    text-align: center;
    padding: 18px 10px;
}}
.rank-num {{
    font-size: 0.78rem;
    color: {text_hint};
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 6px;
}}
.rank-pw {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {text_main};
    font-family: 'SF Mono', 'Fira Code', monospace;
}}
.attack-line {{
    padding: 10px 16px;
    border-radius: 12px;
    background: {badge_bg};
    border: 1px solid {border};
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 0.9rem;
    color: {text_main};
    margin-bottom: 8px;
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
# 사이드바
# ======================
with st.sidebar:
    label = "☀️ 라이트 모드" if dark else "🌙 다크 모드"
    if st.button(label, key="mode_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    st.divider()
    st.markdown(f"**📚 용어 사전**")
    with st.expander("거시상태 (Macrostate)"):
        st.write("문자 구조만 남긴 형태.\n\n예) password123 → llllllllddd\n\n같은 구조끼리는 같은 거시상태.")
    with st.expander("Zipf 법칙"):
        st.write("소수의 항목이 전체 빈도의 대부분을 차지하는 멱법칙 분포.\n\n비밀번호에서도 동일하게 나타난다.")
    with st.expander("Bigram"):
        st.write("비밀번호에서 연속된 두 문자 쌍.\n\npassword → pa, as, ss, sw, wo, or, rd")
    with st.expander("사전 공격 (Dictionary Attack)"):
        st.write("자주 쓰이는 비밀번호 목록(사전)을 우선 시도하는 공격.\n\n인간의 패턴 집중이 이 공격을 효과적으로 만든다.")

# ======================
# 데이터 로드
# [수정 3] 오류 내용을 보여주도록 변경 → 디버깅이 쉬워짐
# ======================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "rockyou_rigorous_behavioral_physics_v2 (1).csv")
    return pd.read_csv(path)

try:
    df = load_data()
    DATA_OK = True
    DATA_ERR = None  # [수정 3] 오류 메시지 저장용 변수
except Exception as e:
    df = None
    DATA_OK = False
    DATA_ERR = str(e)  # [수정 3] 실제 예외 내용을 보관

def apply_chart_theme(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=chart_font,
        font_family="-apple-system, BlinkMacSystemFont, sans-serif",
        margin=dict(t=44, b=20, l=10, r=10),
    )
    fig.update_xaxes(gridcolor=border, zerolinecolor=border)
    fig.update_yaxes(gridcolor=border, zerolinecolor=border)
    return fig

# ======================
# Hero
# ======================
st.markdown(f"""
<div class="page-hero">
    <div class="page-badge">② 규칙성 검증</div>
    <div class="page-title">인간의 비밀번호에는<br>정말 규칙성이 존재하는가?</div>
    <div class="page-subtitle">당신이 공격자라면 비밀번호를 예측할 수 있을까?</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="glass" style="text-align:center; padding:28px 30px;">
    <div style="color:{text_hint}; font-size:0.82rem; letter-spacing:0.06em; font-weight:600; margin-bottom:10px;">🎯 탐구 질문</div>
    <div style="color:{text_main}; font-size:1.05rem; font-weight:600; line-height:1.8;">
        페이지1에서 인간이 특정 방향으로 비밀번호를 선택한다는 사실을 발견했다.<br>
        이번에는 실제 데이터가 정말 예측 가능한 패턴을 가지는지 검증해보자.
    </div>
</div>
""", unsafe_allow_html=True)

# ======================
# SECTION 1 — 해커 퀴즈
# ======================
st.markdown(f'<div class="section-title">1️⃣ 당신은 해커가 될 수 있을까?</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="glass">
    <div class="body-text">
    세 가지 비밀번호 중 <strong>가장 보안이 취약한 것</strong>을 골라보자.<br>
    실제 유출 데이터에서는 어떤 패턴이 압도적으로 많이 등장할까?
    </div>
</div>
""", unsafe_allow_html=True)

answer = st.radio(
    "가장 보안이 취약할 것 같은 비밀번호를 선택하세요",
    ["password123", "T7@zK91!", "xM#4L!qp"],
    horizontal=True
)

if st.button("🔍 정답 확인", key="quiz_btn"):
    if answer == "password123":
        st.markdown(f"""
        <div class="glass" style="border-color:{success_border};">
            <div style="font-size:1.1rem; font-weight:700; color:{text_main}; margin-bottom:8px;">✅ 정답!</div>
            <div class="body-text">
            실제 데이터 속에서 사람들은 <strong>기억하기 쉬운 패턴</strong>을 압도적으로 많이 사용합니다.<br>
            <code>password123</code>은 흔한 단어 + 연속 숫자 구조로, 사전 공격의 1순위 대상입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="glass" style="border-color:{danger_border};">
            <div style="font-size:1.1rem; font-weight:700; color:{text_main}; margin-bottom:8px;">❌ 오답</div>
            <div class="body-text">
            실제 사용자는 생각보다 훨씬 단순한 비밀번호를 선택합니다.<br>
            정답은 <code>password123</code> — 가장 흔하고 예측하기 쉬운 패턴입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ======================
# SECTION 2 — 거시상태 구조 반복성
# ======================
st.markdown(f'<div class="section-title">2️⃣ 사람들은 정말 비슷한 구조를 사용할까?</div>', unsafe_allow_html=True)

if DATA_OK:
    sample_df = df[["microstate", "macrostate"]].sample(15, random_state=42)
    st.markdown(f"""
    <div class="glass">
        <div class="body-text" style="margin-bottom:14px;">
        무작위로 뽑은 15개의 비밀번호와 그 구조(거시상태)다.<br>
        서로 다른 비밀번호인데 구조가 반복되는 것을 찾아보자.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(
        sample_df.rename(columns={"microstate": "비밀번호", "macrostate": "구조 (Macrostate)"}),
        use_container_width=True, hide_index=True
    )

    if st.button("📊 공통 구조 분포 보기", key="macro_btn"):
        top_macro = df["macrostate"].value_counts().head(15).reset_index()
        top_macro.columns = ["구조 (Macrostate)", "등장 횟수"]
        fig = px.bar(top_macro, x="구조 (Macrostate)", y="등장 횟수",
                     color_discrete_sequence=[bar_color],
                     title="가장 많이 사용되는 비밀번호 구조 Top 15")
        fig = apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

        total = len(df)
        top3_ratio = df["macrostate"].value_counts().head(3).sum() / total * 100
        st.markdown(f"""
        <div class="glass" style="border-color:{success_border};">
            <div class="body-text">
            상위 3개 구조만으로 전체의 <strong>{top3_ratio:.1f}%</strong>를 차지한다.<br>
            인간은 매우 다양한 비밀번호를 만드는 것 같지만, 실제로는 <strong>일부 구조를 반복적으로</strong> 사용한다.
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    # [수정 3] 단순 경고 → 실제 오류 내용까지 표시
    st.markdown(f"""
    <div class="glass">
        <div class="body-text">⚠️ 데이터셋을 불러오지 못했습니다.<br>
        <code>{DATA_ERR}</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ======================
# SECTION 3 — 인기 순위 + Zipf 법칙
# ======================
st.markdown(f'<div class="section-title">3️⃣ 비밀번호에도 인기 순위가 존재할까?</div>', unsafe_allow_html=True)

if DATA_OK:
    top_pw = df["microstate"].value_counts().head(10)
    cols_rank = st.columns(5)
    for i, (pw, count) in enumerate(top_pw.items()):
        with cols_rank[i % 5]:
            st.markdown(f"""
            <div class="glass rank-card">
                <div class="rank-num">{i+1}위</div>
                <div class="rank-pw">{pw}</div>
                <div style="font-size:0.78rem; color:{text_hint}; margin-top:4px;">{count:,}회</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-title" style="margin-top:1.5rem;">📉 Zipf 법칙 — 순위 vs 빈도</div>', unsafe_allow_html=True)

    zipf_df = df["microstate"].value_counts().reset_index()
    zipf_df.columns = ["password", "count"]
    zipf_df["rank"] = np.arange(1, len(zipf_df) + 1)

    fig = px.scatter(
        zipf_df.head(5000), x="rank", y="count",
        log_x=True, log_y=True,
        color_discrete_sequence=[bar_color],
        title="Zipf Law — 비밀번호 순위 vs 빈도 (log-log)",
        labels={"rank": "순위 (log)", "count": "등장 횟수 (log)"}
    )
    fig = apply_chart_theme(fig)
    fig.update_traces(marker=dict(size=3, opacity=0.6))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="glass" style="border-color:{success_border};">
        <div class="body-text">
        로그-로그 그래프에서 <strong>직선에 가까운 패턴</strong>이 나타난다 → <strong>Zipf 법칙(멱법칙)</strong> 확인.<br>
        소수의 비밀번호가 엄청난 빈도를 차지하고, 나머지는 길게 늘어진 꼬리 분포를 보인다.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ======================
# SECTION 4 — Bigram 분석
# ======================
st.markdown(f'<div class="section-title">4️⃣ 사람들은 어떤 문자 조합을 좋아할까?</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="glass">
    <div class="body-text">
    비밀번호에서 가장 자주 등장하는 <strong>연속 두 문자 조합(Bigram)</strong>은 무엇일까?<br>
    직관적으로 예측해보고 실제 데이터와 비교해보자.
    </div>
</div>
""", unsafe_allow_html=True)

guess = st.radio(
    "가장 많이 등장할 것 같은 문자 조합은?",
    ["pa", "zx", "kr", "jq"], horizontal=True
)

if st.button("📊 Bigram 결과 보기", key="bigram_btn"):
    is_correct = guess == "pa"
    result_border = success_border if is_correct else danger_border
    result_icon = "✅" if is_correct else "❌"
    result_text = "정답!" if is_correct else f"아쉽게도 정답은 <strong>pa</strong> 입니다."

    st.markdown(f"""
    <div class="glass" style="border-color:{result_border};">
        <div style="font-size:1rem; font-weight:700; color:{text_main}; margin-bottom:8px;">{result_icon} {result_text}</div>
        <div class="body-text">
        <code>password</code>, <code>pass123</code>, <code>password1</code> 등의 영향으로 <strong>pa</strong>가 압도적 1위입니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # [수정 4] bigram_sequence 컬럼 유무에 따라 안내 메시지 분기
    if DATA_OK and "bigram_sequence" in df.columns:
        counter = Counter()
        for item in df["bigram_sequence"].dropna():
            counter.update(str(item).split("|"))
        top_bigram = pd.DataFrame(counter.most_common(15), columns=["Bigram", "등장 횟수"])
        fig = px.bar(top_bigram, x="Bigram", y="등장 횟수",
                     color_discrete_sequence=[bar_color2],
                     title="가장 자주 등장하는 문자 조합 Top 15")
        fig = apply_chart_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # [수정 4] 그래프를 못 그리는 이유를 사용자에게 알려줌
        reason = "데이터셋을 불러오지 못했습니다." if not DATA_OK else "데이터에 'bigram_sequence' 컬럼이 없습니다."
        st.markdown(f"""
        <div class="glass">
            <div class="body-text">ℹ️ Bigram 분포 그래프를 표시할 수 없습니다. ({reason})</div>
        </div>
        """, unsafe_allow_html=True)

# ======================
# SECTION 5 — 랜덤 세계 vs 실제
# [수정 1] np.random.seed 고정 → 슬라이더 값이 같으면 결과도 동일하게 재현
# ======================
st.markdown(f'<div class="section-title">5️⃣ 완전히 랜덤한 세계와 비교해보자</div>', unsafe_allow_html=True)

randomness = st.slider("랜덤성 강도", 0, 100, 50, key="rand_slider")

col1, col2 = st.columns(2)

# [수정 1] 슬라이더 값을 시드로 사용해 재현성 확보
rng = np.random.default_rng(seed=randomness)
sim = rng.normal(50, max(3, randomness / 5), 1000)

fig1 = px.histogram(x=sim, nbins=30, color_discrete_sequence=[bar_color],
                    title=f"가상의 랜덤 세계 (랜덤성 {randomness}%)",
                    labels={"x": "값", "y": "빈도"})
fig1 = apply_chart_theme(fig1)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

if DATA_OK:
    fig2 = px.histogram(df, x="shannon_entropy", nbins=40,
                        color_discrete_sequence=[bar_color2],
                        title="실제 데이터 Shannon Entropy 분포",
                        labels={"shannon_entropy": "Shannon Entropy (bits)", "count": "빈도"})
    fig2 = apply_chart_theme(fig2)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

st.markdown(f"""
<div class="glass" style="border-color:{success_border};">
    <div class="body-text">
    완전히 랜덤한 세계라면 분포가 균등하거나 정규분포에 가까워야 한다.<br>
    하지만 실제 비밀번호의 엔트로피 분포는 <strong>특정 구간에 집중</strong>되어 있다.<br>
    이는 인간의 선택이 랜덤하지 않다는 직접적 증거다.
    </div>
</div>
""", unsafe_allow_html=True)

# ======================
# SECTION 6 — 상태공간의 함정
# [수정 2] 근거 없는 '* 15' 제거 → 실제 데이터 기반 고유 패턴 수 사용
# ======================
st.markdown(f'<div class="section-title">6️⃣ 상태공간의 함정</div>', unsafe_allow_html=True)

possible = st.slider("이론적으로 가능한 비밀번호 수", 100, 1_000_000, 100_000, step=1000, key="state_slider")

# [수정 2] 실제 데이터의 고유 거시상태(구조) 개수를 '집중 상태'의 근거로 사용
# 데이터가 없으면 안전하게 보수적인 추정치(가능 수의 일정 비율)를 사용
if DATA_OK and "macrostate" in df.columns:
    used = int(df["macrostate"].nunique())          # 실제로 사람들이 사용한 고유 구조 수
    used_basis = "실제 데이터의 고유 구조(거시상태) 개수"
else:
    used = max(1, int(possible * 0.001))            # 데이터 없을 때 보수적 추정 (0.1%)
    used_basis = "데이터 부재로 인한 추정치(가능 수의 0.1%)"

# possible보다 used가 클 수 없도록 상한 처리
used = min(used, possible)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="glass" style="text-align:center; padding:24px;">
        <div style="font-size:2rem; font-weight:800; background:{num_grad}; -webkit-background-clip:text; background-clip:text; color:transparent;">{possible:,}</div>
        <div style="color:{text_sub}; font-size:0.9rem; margin-top:6px;">이론적으로 가능한 상태</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="glass" style="text-align:center; padding:24px;">
        <div style="font-size:2rem; font-weight:800; background:{num_grad}; -webkit-background-clip:text; background-clip:text; color:transparent;">{used:,}</div>
        <div style="color:{text_sub}; font-size:0.9rem; margin-top:6px;">실제 집중 상태</div>
    </div>""", unsafe_allow_html=True)

ratio = used / possible * 100
st.markdown(f"""
<div class="glass" style="border-color:{warn_border};">
    <div class="body-text">
    가능한 조합은 <strong>{possible:,}개</strong>이지만, 사람들은 전체의 약 <strong>{ratio:.2f}%</strong>에 해당하는 <strong>{used:,}개</strong> 패턴에만 집중한다.<br>
    공격자 입장에서는 탐색 공간이 기하급수적으로 줄어드는 셈이다.<br>
    <span style="color:{text_hint}; font-size:0.85rem;">※ 집중 상태 산출 근거: {used_basis}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ======================
# SECTION 7 — 사전 공격 시뮬레이션
# ======================
st.markdown(f'<div class="section-title">7️⃣ 실제 공격 시뮬레이션</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="glass">
    <div class="body-text">
    해커는 가능한 모든 비밀번호를 시도하지 않는다.<br>
    인간이 자주 선택하는 패턴부터 우선 시도한다.<br>
    버튼을 눌러 사전 공격 과정을 시뮬레이션해보자.
    </div>
</div>
""", unsafe_allow_html=True)

candidates = ["123456", "password", "qwerty", "welcome", "admin", "password123"]

if st.button("🚨 공격 시작", key="attack_btn"):
    progress = st.progress(0)
    result_container = st.empty()
    tried = []
    for i, pw in enumerate(candidates):
        time.sleep(0.4)
        tried.append(pw)
        progress.progress((i + 1) / len(candidates))
        lines = "".join([f'<div class="attack-line">시도 {j+1} → <strong>{p}</strong></div>' for j, p in enumerate(tried)])
        result_container.markdown(f'<div style="margin-top:8px;">{lines}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="glass" style="border-color:{success_border}; margin-top:12px;">
        <div style="font-size:1.1rem; font-weight:700; color:{text_main}; margin-bottom:8px;">💥 공격 성공</div>
        <div class="body-text">
        단 <strong>{len(candidates)}번</strong>의 시도만으로 크래킹 완료.<br>
        해커는 모든 조합을 시도하는 것이 아니라, <strong>인간의 패턴을 이용한 확률 기반 탐색</strong>을 수행한다.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ======================
# 결론
# ======================
st.markdown(f"""
<div class="conclusion-box">
    <div class="conclusion-title">📌 최종 결론</div>
    사람은 랜덤하다고 생각하며 비밀번호를 만든다.<br><br>
    그러나 실제 데이터는<br>
    <strong>반복되는 구조</strong> · <strong>반복되는 문자 조합</strong> · <strong>반복되는 길이</strong> · <strong>반복되는 인기 비밀번호</strong><br>
    를 보여준다.<br><br>
    해커는 모든 비밀번호를 시도하지 않는다.<br>
    인간이 가장 먼저 선택할 것 같은 비밀번호부터 시도하고, 그것이 <strong>실제로 매우 잘 통한다.</strong><br><br>
    <span style="color:{text_hint}; font-size:0.9rem;">➡ 다음 페이지에서는 이러한 규칙성이 왜 보안상 위험한지 구체적으로 분석한다.</span>
</div>
""", unsafe_allow_html=True)
