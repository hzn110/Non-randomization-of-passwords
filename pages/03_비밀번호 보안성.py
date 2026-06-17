import os
import math
import re
import time
from collections import Counter

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="인간의 비밀번호 선택은 정보보안에 어떤 영향을 주는가?",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 다크/라이트 모드 상태
# =====================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# =====================================================
# 다크/라이트 CSS 변수 정의 (메인 페이지와 동일)
# =====================================================

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
    q_grad     = "linear-gradient(135deg,#e8e0ff 0%,#f9c6ff 100%)"
    info_bg    = "rgba(100,170,255,0.10)"
    info_br    = "rgba(100,170,255,0.25)"
    success_bg = "rgba(90,255,160,0.08)"
    success_br = "rgba(90,255,160,0.25)"
    warn_bg    = "rgba(255,210,90,0.08)"
    warn_br    = "rgba(255,210,90,0.28)"
    err_bg     = "rgba(255,90,90,0.10)"
    err_br     = "rgba(255,90,90,0.28)"
    input_bg   = "rgba(255,255,255,0.05)"
    input_br   = "rgba(200,180,255,0.20)"
    divider_c  = "rgba(200,180,255,0.12)"
    section_icon_bg = "rgba(200,180,255,0.10)"
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
    q_grad     = "linear-gradient(135deg,#3b3bb0 0%,#db2777 100%)"
    info_bg    = "rgba(80,120,220,0.07)"
    info_br    = "rgba(80,120,220,0.22)"
    success_bg = "rgba(30,160,80,0.07)"
    success_br = "rgba(30,160,80,0.22)"
    warn_bg    = "rgba(200,150,0,0.07)"
    warn_br    = "rgba(200,150,0,0.25)"
    err_bg     = "rgba(200,50,50,0.07)"
    err_br     = "rgba(200,50,50,0.25)"
    input_bg   = "rgba(255,255,255,0.60)"
    input_br   = "rgba(100,100,200,0.22)"
    divider_c  = "rgba(100,100,200,0.12)"
    section_icon_bg = "rgba(100,100,220,0.09)"

# =====================================================
# CSS 주입 (메인 페이지와 동일 구조)
# =====================================================

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
    font-size: 2.9rem;
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
    font-size: 1.05rem;
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
    transform: translateY(-3px);
    box-shadow:
        0 14px 36px {shadow_hov},
        inset 0 1px 0 rgba(255,255,255,0.28),
        inset 0 -1px 0 rgba(255,255,255,0.08);
}}

.glass-flat {{
    position: relative;
    background: {glass_bg};
    backdrop-filter: blur(40px) saturate(180%) brightness(1.08);
    -webkit-backdrop-filter: blur(40px) saturate(180%) brightness(1.08);
    border: 1px solid {border};
    border-radius: 28px;
    padding: 30px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px {shadow}, inset 0 1px 0 rgba(255,255,255,0.14);
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
    font-size: 0.90rem;
    letter-spacing: 0.02em;
}}

/* 섹션 헤더 */
.section-header {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 2.2rem 0 1.1rem 0;
}}

.section-icon {{
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: {section_icon_bg};
    border: 1px solid {border};
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}}

.section-title-text {{
    font-size: 1.50rem;
    font-weight: 700;
    color: {text_main};
    letter-spacing: -0.01em;
}}

/* 인라인 알림 박스 */
.info-box {{
    background: {info_bg};
    border: 1px solid {info_br};
    border-radius: 16px;
    padding: 18px 22px;
    color: {text_sub};
    font-size: 0.93rem;
    line-height: 1.75;
    margin-bottom: 18px;
}}

.success-box {{
    background: {success_bg};
    border: 1px solid {success_br};
    border-radius: 16px;
    padding: 18px 22px;
    color: {text_sub};
    font-size: 0.93rem;
    line-height: 1.80;
    margin-bottom: 18px;
}}

.warn-box {{
    background: {warn_bg};
    border: 1px solid {warn_br};
    border-radius: 16px;
    padding: 18px 22px;
    color: {text_sub};
    font-size: 0.93rem;
    line-height: 1.75;
    margin-bottom: 18px;
}}

.err-box {{
    background: {err_bg};
    border: 1px solid {err_br};
    border-radius: 16px;
    padding: 18px 22px;
    color: {text_sub};
    font-size: 0.93rem;
    line-height: 1.75;
    margin-bottom: 18px;
}}

/* 결과 메트릭 카드 */
.metric-glass {{
    background: {glass_bg};
    border: 1px solid {border};
    border-radius: 20px;
    padding: 20px 18px;
    text-align: center;
    box-shadow: 0 4px 16px {shadow};
}}

.metric-val {{
    font-size: 1.9rem;
    font-weight: 800;
    background: {num_grad};
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    word-break: break-all;
}}

.metric-lbl {{
    margin-top: 6px;
    font-size: 0.82rem;
    color: {text_sub};
    font-weight: 500;
    letter-spacing: 0.03em;
}}

/* 구분선 */
.glass-divider {{
    border: none;
    border-top: 1px solid {divider_c};
    margin: 2rem 0;
}}

/* 핵심 질문 */
.conclusion-box {{
    text-align: center;
    padding: 55px 30px;
    margin-top: 10px;
    font-size: 1.0rem;
    line-height: 2;
    color: {text_sub};
}}

.conclusion-box h2 {{
    font-size: 1.65rem;
    margin-bottom: 1rem;
    background: {q_grad};
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: 800;
}}

/* 딕셔너리 용어 */
.term-title {{
    font-weight: 700;
    font-size: 0.98rem;
    color: {text_main};
    margin-bottom: 8px;
}}

.term-body {{
    color: {text_sub};
    font-size: 0.88rem;
    line-height: 1.75;
}}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 데이터 불러오기
# =====================================================

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


# =====================================================
# 분석 함수
# =====================================================

def get_macrostate(password):
    macro = ""
    for ch in password:
        if ch.isupper():   macro += "U"
        elif ch.islower(): macro += "L"
        elif ch.isdigit(): macro += "d"
        else:              macro += "s"
    return macro


def charset_size(password):
    size = 0
    if any(c.islower() for c in password):  size += 26
    if any(c.isupper() for c in password):  size += 26
    if any(c.isdigit() for c in password):  size += 10
    if any(not c.isalnum() for c in password): size += 32
    return max(size, 1)


def theoretical_entropy(password):
    if not password: return 0.0
    return len(password) * math.log2(charset_size(password))


RUNS     = "0123456789abcdefghijklmnopqrstuvwxyz"
RUNS_REV = RUNS[::-1]
KEYBOARD_PATTERNS = ["qwerty", "qwer", "asdf", "asdfgh", "zxcv", "1qaz", "zaq1"]


def detect_pattern_count(password):
    lower = password.lower()
    count = 0
    for seq in (RUNS, RUNS_REV):
        for i in range(len(seq) - 2):
            if seq[i:i+3] in lower:
                count += 1
                break
    if any(p in lower for p in KEYBOARD_PATTERNS):
        count += 1
    if re.search(r"(.)\1{2,}", password):
        count += 1
    return count


def effective_entropy(password):
    penalty = detect_pattern_count(password) * 10
    return max(theoretical_entropy(password) - penalty, 0)


def entropy_grade(bits):
    if bits < 20:   return "낮음",     "🔴"
    elif bits < 40: return "보통",     "🟡"
    else:           return "높음",     "🟢"


def estimate_crack_seconds(password, guesses_per_second=1_000_000):
    combos = charset_size(password) ** max(len(password), 1)
    return combos / guesses_per_second / 2


def format_seconds(seconds):
    if seconds < 1:
        return "1초 미만"
    units = [
        ("년",  60*60*24*365),
        ("일",  60*60*24),
        ("시간",60*60),
        ("분",  60),
        ("초",  1),
    ]
    for name, unit in units:
        if seconds >= unit:
            value = seconds / unit
            if value > 1e12:
                return f"{value:.2e} {name} 이상"
            return f"약 {value:,.1f}{name}"
    return "1초 미만"


def risk_label(pct):
    if pct is None:  return "데이터 없음",  "⚪"
    if pct <= 1:     return "매우 위험",    "🔴"
    elif pct <= 10:  return "위험",         "🟠"
    elif pct <= 50:  return "보통",         "🟡"
    else:            return "비교적 안전",  "🟢"


# =====================================================
# 사이드바
# =====================================================

with st.sidebar:
    # 다크/라이트 토글
    label = "☀️ 라이트 모드" if dark else "🌙 다크 모드"
    if st.button(label, key="mode_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.divider()

    st.markdown(f'<div style="font-size:1.05rem;font-weight:700;color:{text_main};margin-bottom:12px;">📚 정보보안 용어 사전</div>', unsafe_allow_html=True)

    with st.expander("엔트로피 (Entropy)"):
        st.markdown(f"""
        <div class="term-body">
        비밀번호가 얼마나 예측하기 어려운지를 비트(bit) 단위로 나타낸 값이다.<br><br>
        엔트로피가 높을수록 무차별 대입 공격에 더 많은 시도가 필요하다.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("사전 공격 (Dictionary Attack)"):
        st.markdown(f"""
        <div class="term-body">
        실제 사람들이 자주 쓰는 비밀번호 목록(사전)을 우선적으로 시도하는 공격 방식이다.<br><br>
        인간의 선택이 특정 패턴에 몰려 있을수록 이 공격은 매우 효율적으로 작동한다.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("브루트포스 (Brute Force)"):
        st.markdown(f"""
        <div class="term-body">
        가능한 모든 조합을 처음부터 끝까지 전부 시도해보는 공격 방식이다.<br><br>
        엔트로피가 높을수록 시간이 기하급수적으로 늘어난다.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Zipf의 법칙"):
        st.markdown(f"""
        <div class="term-body">
        소수의 항목이 전체 빈도의 대부분을 차지하고, 나머지는 매우 낮은 빈도로 분포하는 멱법칙 형태이다.<br><br>
        비밀번호의 구조(거시상태) 분포 역시 이와 유사한 형태를 보인다.
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# Hero
# =====================================================

st.markdown(f"""
<div class="hero">
  <div class="hero-badge">INFORMATION SECURITY × STATISTICAL PHYSICS</div>
  <div class="hero-title">🛡️ 인간의 비밀번호 선택은<br>정보보안에 어떤 영향을 주는가?</div>
  <div class="hero-subtitle">앞선 통계물리학적 분석 결과를 실제 정보보안 관점으로 연결한다</div>
</div>
""", unsafe_allow_html=True)

# 목표 카드
st.markdown(f"""
<div class="glass-flat">
  <div style="color:{text_sub};font-size:0.95rem;line-height:1.9;">
    <span style="font-weight:700;color:{text_main};">🎯 이 페이지의 목표</span><br><br>
    1, 2페이지에서 우리는 인간의 비밀번호 선택이 완전히 무작위가 아니라
    특정 구조(거시상태)에 몰려 있음을 확인했다.<br><br>
    이 페이지에서는 그 <strong>비무작위성이 실제 공격(사전 공격, 브루트포스)에 어떤 영향을 주는지</strong>를
    직접 체험해본다.
  </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# SECTION 0 — 패턴은 왜 위험한가?
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">0️⃣</div>
  <div class="section-title-text">패턴은 왜 위험한가? — 상태 분포와 Zipf의 법칙</div>
</div>
""", unsafe_allow_html=True)

if DATA_OK:
    macro_counts = df["macrostate"].value_counts().reset_index()
    macro_counts.columns = ["macrostate", "count"]
    macro_counts["rank"] = range(1, len(macro_counts) + 1)

    top_n   = 200
    plot_df = macro_counts.head(top_n)

    fig = px.line(
        plot_df, x="rank", y="count", log_x=True, log_y=True,
        title="거시상태(구조) 빈도 분포 — Rank vs Frequency (log-log)"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font_color   =text_sub,
        title_font_color=text_main,
    )
    fig.update_traces(line_color="#c4b5ff" if dark else "#7c3aed")

    st.markdown('<div class="glass-flat">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    total        = macro_counts["count"].sum()
    top10_ratio  = macro_counts.head(10)["count"].sum() / total * 100

    st.markdown(f"""
    <div class="glass-flat" style="color:{text_sub};line-height:1.85;font-size:0.95rem;">
      상위 <strong style="color:{text_main};">10개</strong> 구조(거시상태)가 전체 비밀번호의 약
      <strong style="color:{text_main};">{top10_ratio:.1f}%</strong>를 차지한다.<br><br>
      로그-로그 그래프에서 거의 직선에 가까운 형태 — 이것은 Zipf의 법칙처럼
      <strong style="color:{text_main};">소수의 패턴이 압도적인 빈도</strong>를 차지한다는 뜻이다.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("💡 이게 왜 사전 공격으로 이어질까?"):
        st.markdown(f"""
        <div class="info-box">
          만약 인간의 선택이 진짜 무작위였다면 모든 구조는 거의 비슷한 빈도로 나타나야 한다.<br><br>
          하지만 실제로는 일부 구조에 빈도가 집중되어 있다.<br><br>
          공격자는 이 사실을 알고 있기 때문에, 가능한 모든 조합을 시도하기 전에
          <strong>'자주 등장하는 구조 / 자주 등장하는 비밀번호'</strong>부터 먼저 시도한다.<br><br>
          이것이 바로 <strong>사전 공격(Dictionary Attack)</strong>이다.
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="warn-box">⚠️ 비교용 데이터셋(rockyou_rigorous_behavioral_physics_v2.csv)을 불러오지 못해 이 섹션은 표시할 수 없습니다.</div>
    """, unsafe_allow_html=True)


# =====================================================
# SECTION 1 — 비밀번호 강도 측정기
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">1️⃣</div>
  <div class="section-title-text">비밀번호 강도 측정기</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="color:{text_sub};font-size:0.93rem;margin-bottom:14px;">
비밀번호를 입력하면 길이, 엔트로피, 예상 크래킹 시간을 계산한다.
</div>
""", unsafe_allow_html=True)

pw1 = st.text_input("분석할 비밀번호를 입력하세요", type="password", key="pw1")

if pw1:
    ent        = effective_entropy(pw1)
    crack_sec  = estimate_crack_seconds(pw1)
    grade, emoji = entropy_grade(ent)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-glass">
          <div class="metric-val">{len(pw1)}자</div>
          <div class="metric-lbl">비밀번호 길이</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-glass">
          <div class="metric-val">{ent:.1f} bits</div>
          <div class="metric-lbl">실질 엔트로피</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-glass">
          <div class="metric-val" style="font-size:1.3rem;">{format_seconds(crack_sec)}</div>
          <div class="metric-lbl">예상 크래킹 시간</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="glass-flat" style="margin-top:14px;text-align:center;font-size:1.1rem;font-weight:700;color:{text_main};">
      엔트로피 등급: {emoji} {grade}
    </div>
    """, unsafe_allow_html=True)

    with st.expander("💡 '실질 엔트로피'란?"):
        st.markdown(f"""
        <div class="info-box">
          이론적 엔트로피는 '어떤 문자 종류를 썼는가'만 본다.<br><br>
          하지만 1234, qwerty처럼 자주 쓰는 패턴이 포함되면 실제 추측 난이도는 이론값보다 훨씬 낮아진다.<br><br>
          이 페이지에서는 그런 패턴이 발견될 때마다 엔트로피에서 일정 비트를 감점하여 <strong>'실질 엔트로피'</strong>를 계산한다.
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="info-box">👆 비밀번호를 입력하면 분석 결과가 표시됩니다.</div>
    """, unsafe_allow_html=True)


# =====================================================
# SECTION 2 — 실제 데이터와 비교
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">2️⃣</div>
  <div class="section-title-text">실제 데이터와 비교</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="color:{text_sub};font-size:0.93rem;margin-bottom:14px;">
입력한 비밀번호의 <strong style="color:{text_main};">구조(거시상태)</strong>가
실제 유출 데이터에서 얼마나 자주 등장하는 구조인지 비교한다.<br>
<span style="color:{text_hint};">예) abc123 → lllddd 구조 → 상위 1% 패턴 → 매우 위험</span>
</div>
""", unsafe_allow_html=True)

pw2 = st.text_input("비교할 비밀번호를 입력하세요 (기본값: abc123)", value="abc123", key="pw2")

if pw2 and DATA_OK:
    macro2       = get_macrostate(pw2)
    macro_counts2 = df["macrostate"].value_counts().reset_index()
    macro_counts2.columns = ["macrostate", "count"]
    macro_counts2["rank"] = range(1, len(macro_counts2) + 1)
    total_unique = len(macro_counts2)
    match        = macro_counts2[macro_counts2["macrostate"] == macro2]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-glass">
          <div class="metric-val" style="font-size:1.2rem;word-break:break-all;">{macro2}</div>
          <div class="metric-lbl">구조 (Macrostate)</div>
        </div>
        """, unsafe_allow_html=True)

    if not match.empty:
        rank  = int(match["rank"].iloc[0])
        pct   = rank / total_unique * 100
        ratio = match["count"].iloc[0] / df.shape[0] * 100

        with col2:
            st.markdown(f"""
            <div class="metric-glass">
              <div class="metric-val">상위 {pct:.1f}%</div>
              <div class="metric-lbl">패턴 순위</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-glass">
              <div class="metric-val">{ratio:.4f}%</div>
              <div class="metric-lbl">데이터 내 비율</div>
            </div>
            """, unsafe_allow_html=True)

        label, emoji = risk_label(pct)
        st.markdown(f"""
        <div class="glass-flat" style="margin-top:14px;text-align:center;font-size:1.1rem;font-weight:700;color:{text_main};">
          위험도: {emoji} {label}
        </div>
        """, unsafe_allow_html=True)

        if pct <= 1:
            st.markdown(f'<div class="err-box">이 구조는 데이터셋에서 <strong>가장 흔한 패턴 상위 1%</strong> 안에 속한다. 사전 공격의 1순위 후보다.</div>', unsafe_allow_html=True)
        elif pct <= 10:
            st.markdown(f'<div class="warn-box">이 구조는 비교적 흔한 패턴이다. 사전 공격 목록에 포함될 가능성이 높다.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-box">이 구조는 비교적 드문 패턴이다.</div>', unsafe_allow_html=True)
    else:
        with col2:
            st.markdown(f'<div class="metric-glass"><div class="metric-val">데이터 없음</div><div class="metric-lbl">패턴 순위</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-glass"><div class="metric-val">0%</div><div class="metric-lbl">데이터 내 비율</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="success-box" style="margin-top:14px;">이 구조는 분석 데이터셋에서 발견되지 않은, 비교적 드문 구조다.</div>', unsafe_allow_html=True)

elif pw2 and not DATA_OK:
    st.markdown(f'<div class="warn-box">⚠️ 비교용 데이터셋을 불러오지 못해 이 섹션은 표시할 수 없습니다.</div>', unsafe_allow_html=True)


# =====================================================
# SECTION 3 — 엔트로피 비교
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">3️⃣</div>
  <div class="section-title-text">엔트로피 비교</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="color:{text_sub};font-size:0.93rem;margin-bottom:14px;">
같은 길이라도 어떤 패턴을 쓰느냐에 따라 실질 엔트로피가 크게 달라진다.
</div>
""", unsafe_allow_html=True)

sample_pw = ["123456", "abc123", "qwerty123", "X7!kP2#z"]
rows = []
for p in sample_pw:
    bits  = effective_entropy(p)
    grade, emoji = entropy_grade(bits)
    rows.append({"비밀번호": p, "실질 엔트로피 (bits)": round(bits, 1), "등급": f"{emoji} {grade}"})

entropy_df = pd.DataFrame(rows)

col1, col2 = st.columns([1, 1.4])

with col1:
    st.markdown('<div class="glass-flat">', unsafe_allow_html=True)
    st.dataframe(entropy_df, hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    color_map = {"🔴 낮음": "#ff5a5a", "🟡 보통": "#ffd25a", "🟢 높음": "#5affa0"}
    fig2 = px.bar(
        entropy_df,
        x="비밀번호",
        y="실질 엔트로피 (bits)",
        color="등급",
        color_discrete_map=color_map,
        title="실질 엔트로피 비교"
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font_color   =text_sub,
        title_font_color=text_main,
    )
    st.markdown('<div class="glass-flat">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="glass-flat" style="color:{text_sub};line-height:1.85;font-size:0.94rem;">
  <code>123456</code>과 <code>abc123</code>은 문자 종류만 보면 나쁘지 않아 보이지만,
  연속된 숫자/알파벳 패턴이 그대로 엔트로피를 깎아먹는다.<br><br>
  반면 <code>X7!kP2#z</code>는 길이는 비슷해도 대문자·소문자·숫자·특수문자가 불규칙하게 섞여 있어
  패턴 감점이 거의 없다.
</div>
""", unsafe_allow_html=True)


# =====================================================
# SECTION 4 — 가상 브루트포스 시뮬레이터
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">4️⃣</div>
  <div class="section-title-text">가상 브루트포스 시뮬레이터</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="color:{text_sub};font-size:0.93rem;margin-bottom:14px;">
  초당 약 100만 번 시도가 가능한 컴퓨터를 가정했을 때,
  <code>123456</code>과 <code>X7!kP2#z</code>를 전수조사하는 데 걸리는 시간을 비교해본다.
</div>
""", unsafe_allow_html=True)

weak_pw   = "123456"
strong_pw = "X7!kP2#z"
weak_time   = estimate_crack_seconds(weak_pw)
strong_time = estimate_crack_seconds(strong_pw)

if st.button("🚀 브루트포스 시뮬레이션 실행"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f'<div style="font-size:1.1rem;font-weight:700;color:{text_main};margin-bottom:10px;"><code>{weak_pw}</code></div>', unsafe_allow_html=True)
        bar1 = st.progress(0)
        for i in range(0, 101, 20):
            bar1.progress(i)
            time.sleep(0.04)
        st.markdown(f'<div class="err-box">🔓 크랙 완료! 예상 소요 시간: <strong>{format_seconds(weak_time)}</strong></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div style="font-size:1.1rem;font-weight:700;color:{text_main};margin-bottom:10px;"><code>{strong_pw}</code></div>', unsafe_allow_html=True)
        bar2 = st.progress(0)
        for i in range(0, 101, 4):
            bar2.progress(i)
            time.sleep(0.04)
        st.markdown(f'<div class="success-box">🔒 같은 속도로는 예상 소요 시간: <strong>{format_seconds(strong_time)}</strong></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="glass-flat" style="color:{text_sub};line-height:1.85;font-size:0.94rem;margin-top:6px;">
      같은 길이의 비밀번호라도,<br><br>
      <code>{weak_pw}</code>는 사람이 자주 쓰는 연속 숫자 패턴이라 <strong>{format_seconds(weak_time)}</strong> 만에 뚫리지만,<br>
      <code>{strong_pw}</code>는 문자 구성이 불규칙해서 <strong>{format_seconds(strong_time)}</strong>가 걸린다.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f'<div style="color:{text_hint};font-size:0.86rem;">버튼을 누르면 두 비밀번호의 전수조사 과정을 시뮬레이션합니다.</div>', unsafe_allow_html=True)


# =====================================================
# 정보보안 결론
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">📌</div>
  <div class="section-title-text">정보보안 결론</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
conclusions = [
    ("🧩", "인간은 랜덤하지 않다", "기억하기 쉬운 패턴에 반복적으로 집중한다."),
    ("📉", "엔트로피 감소", "이 현상은 실질 엔트로피 감소로 정량화할 수 있다."),
    ("⚔️", "사전 공격의 원리", "공격자는 이 비무작위성을 이용해 사전 공격을 수행한다."),
    ("🔐", "역발상 설계", "강한 비밀번호는 인간의 직관을 의도적으로 거스르는 방향으로 만들어야 한다."),
]

for i, (icon, title, desc) in enumerate(conclusions):
    col = col1 if i % 2 == 0 else col2
    with col:
        st.markdown(f"""
        <div class="glass" style="padding:24px;">
          <div style="font-size:1.6rem;margin-bottom:8px;">{icon}</div>
          <div style="font-size:1.0rem;font-weight:700;color:{text_main};margin-bottom:6px;">{title}</div>
          <div style="font-size:0.88rem;color:{text_sub};line-height:1.65;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# 최종 탐구 결론
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="glass-flat conclusion-box">
  <h2>🧠 최종 탐구 결론</h2>
  통계물리학적으로 인간의 비밀번호 선택은<br>
  높은 엔트로피 상태가 아니라 <strong>특정 패턴에 집중된 낮은 엔트로피 상태</strong>를 보인다.<br><br>
  이러한 비무작위성은 정보보안 측면에서 예측 가능성을 증가시키며,<br>
  결과적으로 비밀번호 크래킹 성공률을 높이는 원인이 된다.<br><br>
  따라서 안전한 비밀번호 설계를 위해서는<br>
  <strong>인간의 자연스러운 선택 경향을 의도적으로 피해야 한다.</strong>
</div>
""", unsafe_allow_html=True)
