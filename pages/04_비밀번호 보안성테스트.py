import os
import re
import math
from collections import Counter

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="비밀번호 안전도 측정",
    page_icon="🔑",
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
# 테마 변수 (메인 페이지와 동일)
# =====================================================

if dark:
    bg_main     = "radial-gradient(circle at 20% 25%, rgba(160,130,255,0.22) 0%, transparent 50%), radial-gradient(circle at 80% 12%, rgba(220,130,255,0.18) 0%, transparent 50%), radial-gradient(circle at 50% 88%, rgba(100,170,255,0.16) 0%, transparent 55%), linear-gradient(160deg, rgba(18,14,48,0.92) 0%, rgba(22,14,52,0.88) 50%, rgba(16,12,42,0.92) 100%)"
    glass_bg    = "linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(200,180,255,0.03) 100%)"
    glass_hov   = "linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(200,180,255,0.07) 100%)"
    border      = "rgba(200,180,255,0.15)"
    border_hov  = "rgba(220,200,255,0.32)"
    text_main   = "rgba(255,255,255,0.95)"
    text_sub    = "rgba(220,210,255,0.60)"
    text_hint   = "rgba(180,170,255,0.35)"
    badge_bg    = "rgba(200,180,255,0.07)"
    shadow      = "rgba(60,30,120,0.18)"
    shadow_hov  = "rgba(80,40,160,0.28)"
    sidebar_bg  = "rgba(18,12,45,0.50)"
    sidebar_br  = "rgba(200,180,255,0.10)"
    title_grad  = "linear-gradient(135deg,#e8e0ff 0%,#c4b5ff 50%,#f9c6ff 100%)"
    num_grad    = "linear-gradient(135deg,#ffffff 0%,#c4b5ff 100%)"
    q_grad      = "linear-gradient(135deg,#e8e0ff 0%,#f9c6ff 100%)"
    info_bg     = "rgba(100,170,255,0.10)"
    info_br     = "rgba(100,170,255,0.25)"
    success_bg  = "rgba(90,255,160,0.08)"
    success_br  = "rgba(90,255,160,0.25)"
    warn_bg     = "rgba(255,210,90,0.08)"
    warn_br     = "rgba(255,210,90,0.28)"
    err_bg      = "rgba(255,90,90,0.10)"
    err_br      = "rgba(255,90,90,0.28)"
    divider_c   = "rgba(200,180,255,0.12)"
    section_icon_bg = "rgba(200,180,255,0.10)"
    gauge_paper = "rgba(18,14,48,0)"
    gauge_font  = "rgba(220,210,255,0.80)"
    plot_bg     = "rgba(0,0,0,0)"
else:
    bg_main     = "radial-gradient(circle at 15% 20%, rgba(100,140,255,0.12) 0%, transparent 45%), radial-gradient(circle at 85% 15%, rgba(255,100,180,0.10) 0%, transparent 45%), radial-gradient(circle at 50% 90%, rgba(80,220,180,0.10) 0%, transparent 50%), linear-gradient(160deg,#f0f2ff 0%,#faf5ff 50%,#f0f8ff 100%)"
    glass_bg    = "linear-gradient(135deg, rgba(255,255,255,0.72) 0%, rgba(255,255,255,0.45) 100%)"
    glass_hov   = "linear-gradient(135deg, rgba(255,255,255,0.90) 0%, rgba(255,255,255,0.65) 100%)"
    border      = "rgba(120,120,180,0.18)"
    border_hov  = "rgba(100,100,220,0.38)"
    text_main   = "rgba(30,30,60,0.95)"
    text_sub    = "rgba(60,60,100,0.65)"
    text_hint   = "rgba(100,100,160,0.55)"
    badge_bg    = "rgba(100,100,220,0.09)"
    shadow      = "rgba(100,100,200,0.10)"
    shadow_hov  = "rgba(100,100,200,0.22)"
    sidebar_bg  = "rgba(255,255,255,0.55)"
    sidebar_br  = "rgba(180,180,220,0.20)"
    title_grad  = "linear-gradient(135deg,#3b3bb0 0%,#7c3aed 50%,#db2777 100%)"
    num_grad    = "linear-gradient(135deg,#3b3bb0 0%,#6366f1 100%)"
    q_grad      = "linear-gradient(135deg,#3b3bb0 0%,#db2777 100%)"
    info_bg     = "rgba(80,120,220,0.07)"
    info_br     = "rgba(80,120,220,0.22)"
    success_bg  = "rgba(30,160,80,0.07)"
    success_br  = "rgba(30,160,80,0.22)"
    warn_bg     = "rgba(200,150,0,0.07)"
    warn_br     = "rgba(200,150,0,0.25)"
    err_bg      = "rgba(200,50,50,0.07)"
    err_br      = "rgba(200,50,50,0.25)"
    divider_c   = "rgba(100,100,200,0.12)"
    section_icon_bg = "rgba(100,100,220,0.09)"
    gauge_paper = "rgba(255,255,255,0)"
    gauge_font  = "rgba(50,50,100,0.80)"
    plot_bg     = "rgba(255,255,255,0)"

# =====================================================
# CSS 주입
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

/* ---------- Liquid Glass ---------- */
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
    background: {glass_bg};
    backdrop-filter: blur(40px) saturate(180%) brightness(1.08);
    -webkit-backdrop-filter: blur(40px) saturate(180%) brightness(1.08);
    border: 1px solid {border};
    border-radius: 28px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px {shadow}, inset 0 1px 0 rgba(255,255,255,0.14);
}}

/* 메트릭 카드 */
.metric-glass {{
    background: {glass_bg};
    border: 1px solid {border};
    border-radius: 20px;
    padding: 20px 14px;
    text-align: center;
    box-shadow: 0 4px 16px {shadow};
    margin-bottom: 16px;
}}

.metric-val {{
    font-size: 1.85rem;
    font-weight: 800;
    background: {num_grad};
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    word-break: break-all;
    line-height: 1.2;
}}

.metric-lbl {{
    margin-top: 6px;
    font-size: 0.80rem;
    color: {text_sub};
    font-weight: 500;
    letter-spacing: 0.03em;
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
    font-size: 1.45rem;
    font-weight: 700;
    color: {text_main};
    letter-spacing: -0.01em;
}}

/* 알림 박스 */
.info-box {{
    background: {info_bg};
    border: 1px solid {info_br};
    border-radius: 16px;
    padding: 18px 22px;
    color: {text_sub};
    font-size: 0.93rem;
    line-height: 1.75;
    margin-bottom: 16px;
}}

.success-box {{
    background: {success_bg};
    border: 1px solid {success_br};
    border-radius: 16px;
    padding: 18px 22px;
    color: {text_sub};
    font-size: 0.93rem;
    line-height: 1.80;
    margin-bottom: 16px;
}}

.warn-box {{
    background: {warn_bg};
    border: 1px solid {warn_br};
    border-radius: 16px;
    padding: 18px 22px;
    color: {text_sub};
    font-size: 0.93rem;
    line-height: 1.75;
    margin-bottom: 16px;
}}

.err-box {{
    background: {err_bg};
    border: 1px solid {err_br};
    border-radius: 16px;
    padding: 18px 22px;
    color: {text_sub};
    font-size: 0.93rem;
    line-height: 1.75;
    margin-bottom: 16px;
}}

/* 패턴 뱃지 */
.pattern-badge {{
    display: inline-block;
    padding: 5px 14px;
    border-radius: 999px;
    background: {warn_bg};
    border: 1px solid {warn_br};
    color: {text_sub};
    font-size: 0.85rem;
    margin: 4px 4px 4px 0;
    font-weight: 500;
}}

/* 구분선 */
.glass-divider {{
    border: none;
    border-top: 1px solid {divider_c};
    margin: 2rem 0;
}}

/* 매크로스테이트 코드 블록 */
.macro-block {{
    background: {badge_bg};
    border: 1px solid {border};
    border-radius: 12px;
    padding: 14px 18px;
    font-family: monospace;
    font-size: 1.0rem;
    color: {text_main};
    letter-spacing: 0.08em;
    margin: 10px 0;
    word-break: break-all;
}}

/* 개선 팁 카드 */
.tip-card {{
    background: {warn_bg};
    border: 1px solid {warn_br};
    border-left: 3px solid rgba(255,200,80,0.6);
    border-radius: 14px;
    padding: 14px 18px;
    color: {text_sub};
    font-size: 0.90rem;
    line-height: 1.65;
    margin-bottom: 10px;
}}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 데이터 로드
# =====================================================

@st.cache_data
def load_dataset():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "rockyou_rigorous_behavioral_physics_v2.csv")
    return pd.read_csv(path)

@st.cache_data
def load_common_passwords():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "common_passwords.csv")
    df = pd.read_csv(path)
    col = df.columns[0]
    return df[col].astype(str).tolist()

try:
    df = load_dataset()
    DATA_OK = True
except Exception:
    df = None
    DATA_OK = False

try:
    common_list = load_common_passwords()
    common_set  = set(common_list)
    COMMON_OK   = True
except Exception:
    common_list = []
    common_set  = set()
    COMMON_OK   = False


# =====================================================
# 분석 함수
# =====================================================

KEYBOARD_ROWS = [
    "1234567890",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
]

def _key_position(ch):
    ch = ch.lower()
    for r, row in enumerate(KEYBOARD_ROWS):
        if ch in row:
            return (r, row.index(ch))
    return None

def keyboard_path_length(password):
    total, prev = 0.0, None
    for ch in password:
        pos = _key_position(ch)
        if pos is not None and prev is not None:
            total += math.sqrt((pos[0]-prev[0])**2 + (pos[1]-prev[1])**2)
        if pos is not None:
            prev = pos
    return total

def shannon_entropy(password):
    if not password: return 0.0
    counts = Counter(password)
    n = len(password)
    return -sum((c/n)*math.log2(c/n) for c in counts.values())

def get_macrostate(password):
    macro = ""
    for ch in password:
        if ch.isupper():   macro += "U"
        elif ch.islower(): macro += "L"
        elif ch.isdigit(): macro += "d"
        else:              macro += "s"
    return macro

def order_parameter(password):
    if not password: return 0.0
    counts = {"U":0,"L":0,"d":0,"s":0}
    for ch in password:
        if ch.isupper():   counts["U"] += 1
        elif ch.islower(): counts["L"] += 1
        elif ch.isdigit(): counts["d"] += 1
        else:              counts["s"] += 1
    total = len(password)
    fractions = [c/total for c in counts.values()]
    return sum(abs(f-0.25) for f in fractions) / 2

SEQUENCES = [
    "0123456789","9876543210",
    "abcdefghijklmnopqrstuvwxyz",
]
KEYBOARD_PATTERNS = ["qwer","asdf","zxcv","qwerty","asdfgh","1qaz","zaq1"]
COMMON_WORDS = ["password","love","admin","welcome","iloveyou",
                "monkey","dragon","letmein","qwerty","123456"]

def detect_patterns(password):
    lower = password.lower()
    found = []
    for seq in SEQUENCES:
        for i in range(len(seq)-3):
            if seq[i:i+4] in lower:
                found.append("연속된 문자/숫자 (예: 1234, abcd)")
                break
    if re.search(r'(.)\1{2,}', password):
        found.append("같은 문자 반복 (예: aaa, 111)")
    if re.search(r'(19|20)\d{2}', password):
        found.append("연도 형태 포함 (예: 1999, 2024)")
    if any(p in lower for p in KEYBOARD_PATTERNS):
        found.append("키보드 인접 자판 패턴 (예: qwer, asdf)")
    if any(w in lower for w in COMMON_WORDS):
        found.append("흔히 쓰이는 단어 포함 (예: password, love)")
    return found

def human_bias_score(password):
    return len(detect_patterns(password))

def percentile_rank(series, value):
    series = series.dropna()
    if len(series) == 0: return None
    return float((series < value).mean() * 100)

def estimate_crack_time_seconds(password):
    charset = 0
    if any(c.islower() for c in password):  charset += 26
    if any(c.isupper() for c in password):  charset += 26
    if any(c.isdigit() for c in password):  charset += 10
    if any(not c.isalnum() for c in password): charset += 32
    charset = max(charset, 1)
    return charset**max(len(password),1) / 1e10 / 2

def format_seconds(seconds):
    if seconds < 1: return "1초 미만"
    units = [("년",60*60*24*365),("일",60*60*24),("시간",60*60),("분",60),("초",1)]
    for name, unit in units:
        if seconds >= unit:
            value = seconds / unit
            if value > 1e12: return f"{value:.2e} {name} 이상"
            return f"약 {value:,.1f}{name}"
    return "1초 미만"

def clamp(v, lo=0, hi=100):
    return max(lo, min(hi, v))


# =====================================================
# 사이드바
# =====================================================

with st.sidebar:
    label = "☀️ 라이트 모드" if dark else "🌙 다크 모드"
    if st.button(label, key="mode_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    st.divider()

    st.markdown(f'<div style="font-size:1.05rem;font-weight:700;color:{text_main};margin-bottom:12px;">💡 분석 지표 안내</div>', unsafe_allow_html=True)

    with st.expander("섀넌 엔트로피"):
        st.markdown(f'<div style="color:{text_sub};font-size:0.88rem;line-height:1.75;">비밀번호 내 문자의 분포를 기반으로 정보량을 측정한다. 값이 높을수록 문자 구성이 균일하게 다양하다.</div>', unsafe_allow_html=True)

    with st.expander("질서변수 (Order Parameter)"):
        st.markdown(f'<div style="color:{text_sub};font-size:0.88rem;line-height:1.75;">대·소문자·숫자·특수문자 비율이 균등(0.25씩)에서 얼마나 벗어나는지 측정한다. 0에 가까울수록 균형 잡혀 있다.</div>', unsafe_allow_html=True)

    with st.expander("거시상태 (Macrostate)"):
        st.markdown(f'<div style="color:{text_sub};font-size:0.88rem;line-height:1.75;">문자 자체가 아니라 문자 종류 패턴(U/L/d/s)으로 비밀번호 구조를 표현한다. 같은 구조가 데이터셋에 많을수록 위험하다.</div>', unsafe_allow_html=True)

    with st.expander("Human Bias Score"):
        st.markdown(f'<div style="color:{text_sub};font-size:0.88rem;line-height:1.75;">연속 숫자·키보드 패턴·반복 문자 등 인간이 자주 쓰는 습관 패턴의 개수를 센 값이다. 0에 가까울수록 좋다.</div>', unsafe_allow_html=True)


# =====================================================
# Hero
# =====================================================

st.markdown(f"""
<div class="hero">
  <div class="hero-badge">RARITY × SECURITY ANALYSIS</div>
  <div class="hero-title">🔑 비밀번호 안전도 측정</div>
  <div class="hero-subtitle">입력한 비밀번호의 희귀도(Rarity)와 보안성(Security)을 분석해보자</div>
</div>
""", unsafe_allow_html=True)

# 개인정보 안내 카드
st.markdown(f"""
<div class="info-box">
  🔒 입력하신 비밀번호는 서버에 저장되거나 전송되지 않고, 이 브라우저 화면 안에서만 분석에 사용됩니다.<br><br>
  다만 실제로 사용 중인 비밀번호 대신, <strong>테스트용으로 변형한 비밀번호</strong>를 입력하는 것을 추천합니다.
</div>
""", unsafe_allow_html=True)

password = st.text_input("분석할 비밀번호를 입력해보세요", type="password")

if not password:
    st.markdown(f'<div style="color:{text_hint};font-size:0.90rem;margin-top:8px;">👆 비밀번호를 입력하면 분석이 시작됩니다.</div>', unsafe_allow_html=True)
    st.stop()

# 사전 계산
macro    = get_macrostate(password)
n_upper  = sum(c.isupper() for c in password)
n_lower  = sum(c.islower() for c in password)
n_digit  = sum(c.isdigit() for c in password)
n_symbol = sum(not c.isalnum() for c in password)
s_ent    = shannon_entropy(password)
op       = order_parameter(password)
patterns_found = detect_patterns(password)
bias_score     = human_bias_score(password)
is_common      = password.lower() in {p.lower() for p in common_list} if COMMON_OK else False


# =====================================================
# SECTION 1 — 기본 구조 분석
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">1️⃣</div>
  <div class="section-title-text">기본 구조 분석</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

metrics = [
    (f"{len(password)}자",           "비밀번호 길이"),
    (str(sum(x>0 for x in [n_upper,n_lower,n_digit,n_symbol])), "문자 종류 수"),
    (f"{s_ent:.2f} bits",            "섀넌 엔트로피"),
    (f"{op:.2f}",                    "질서변수"),
]

for col, (val, lbl) in zip([col1,col2,col3,col4], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-glass">
          <div class="metric-val">{val}</div>
          <div class="metric-lbl">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f"""
<div class="glass-flat">
  <div style="color:{text_sub};font-size:0.88rem;margin-bottom:8px;font-weight:600;">거시상태 (Macrostate) 구조</div>
  <div class="macro-block">{macro}</div>
  <div style="color:{text_hint};font-size:0.82rem;margin-top:8px;">U = 대문자 &nbsp;·&nbsp; L = 소문자 &nbsp;·&nbsp; d = 숫자 &nbsp;·&nbsp; s = 특수문자</div>
</div>
""", unsafe_allow_html=True)

with st.expander("💡 거시상태 읽는 법"):
    st.markdown(f"""
    <div class="info-box">
      예를 들어 <code>Password123!</code>은 <code>UllllllldddsS</code> 형태의 거시상태를 가진다.<br><br>
      문자 자체는 다르더라도, 같은 구조(거시상태)를 가진 비밀번호는 실제 유출 데이터에서 매우 많이 발견된다.
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# SECTION 2 — 희귀도 분석
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">2️⃣</div>
  <div class="section-title-text">희귀도 분석 (Rarity)</div>
</div>
""", unsafe_allow_html=True)

# 흔한 비밀번호 여부
if COMMON_OK:
    if is_common:
        st.markdown(f'<div class="err-box">🚨 이 비밀번호는 실제 유출 데이터에서 자주 등장하는 <strong>흔한 비밀번호 목록에 포함</strong>되어 있습니다.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="success-box">✅ 입력한 비밀번호는 흔한 비밀번호 목록(common_passwords.csv)에서 발견되지 않았습니다.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="warn-box">⚠️ common_passwords.csv 데이터를 불러오지 못해 흔한 비밀번호 여부는 확인할 수 없습니다.</div>', unsafe_allow_html=True)

if DATA_OK:
    macro_counts = df["macrostate"].value_counts(normalize=True)
    macro_ratio  = macro_counts.get(macro, 0.0)
    macro_pct    = macro_ratio * 100

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-glass">
          <div class="metric-val" style="font-size:1.5rem;">{macro_pct:.4f}%</div>
          <div class="metric-lbl">같은 구조(macrostate)를 가진 비밀번호 비율</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if macro_pct > 0:
            surprisal = -math.log2(macro_ratio)
            st.markdown(f"""
            <div class="metric-glass">
              <div class="metric-val">{surprisal:.2f} bits</div>
              <div class="metric-lbl">구조 희귀도 (Surprisal)</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-glass">
              <div class="metric-val" style="font-size:1.1rem;">미발견</div>
              <div class="metric-lbl">구조 희귀도 (Surprisal)</div>
            </div>
            """, unsafe_allow_html=True)

    if macro_pct >= 0.5:
        st.markdown(f"""
        <div class="warn-box">
          입력한 비밀번호와 <strong>동일한 구조</strong>를 가진 비밀번호가 분석 데이터셋의
          <strong>{macro_pct:.2f}%</strong>를 차지합니다.<br><br>
          문자가 달라도 구조가 흔하면, 공격자의 패턴 기반 추측 공격에 노출될 수 있습니다.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-box">
          입력한 비밀번호와 동일한 구조를 가진 비밀번호는 데이터셋에서 <strong>{macro_pct:.4f}%</strong>로
          비교적 드문 구조입니다.
        </div>
        """, unsafe_allow_html=True)

    ent_pct = percentile_rank(df["shannon_entropy"], s_ent)
    if ent_pct is not None:
        st.markdown(f"""
        <div class="glass-flat" style="color:{text_sub};font-size:0.93rem;line-height:1.75;">
          입력한 비밀번호의 섀넌 엔트로피는 분석 데이터셋 내에서
          <strong style="color:{text_main};">상위 {100-ent_pct:.1f}%</strong> 수준입니다.<br>
          <span style="color:{text_hint};">값이 높을수록 더 무작위적인 비밀번호입니다.</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown(f'<div class="warn-box">⚠️ 비교용 데이터셋을 불러오지 못해 일부 비교 분석을 표시할 수 없습니다.</div>', unsafe_allow_html=True)


# =====================================================
# SECTION 3 — 보안성 분석
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">3️⃣</div>
  <div class="section-title-text">보안성 분석 (Security)</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="glass-flat">
      <div style="font-size:1.0rem;font-weight:700;color:{text_main};margin-bottom:14px;">🧩 발견된 인간적 패턴</div>
    """, unsafe_allow_html=True)

    if patterns_found:
        badges_html = "".join(f'<span class="pattern-badge">⚠️ {p}</span>' for p in patterns_found)
        st.markdown(badges_html, unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="success-box" style="margin-top:8px;">✅ 뚜렷한 인간 행동 패턴이 발견되지 않았습니다.</div>', unsafe_allow_html=True)

    st.markdown(f"""
      <div class="metric-glass" style="margin-top:16px;">
        <div class="metric-val">{bias_score}</div>
        <div class="metric-lbl">Human Bias Score</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    crack_seconds = estimate_crack_time_seconds(password)
    st.markdown(f"""
    <div class="glass-flat">
      <div style="font-size:1.0rem;font-weight:700;color:{text_main};margin-bottom:14px;">⏱️ 이론적 전수조사 시간</div>
    """, unsafe_allow_html=True)

    if is_common:
        st.markdown(f"""
        <div class="metric-glass">
          <div class="metric-val" style="font-size:1.3rem;">1초 미만</div>
          <div class="metric-lbl">예상 크랙 시간</div>
        </div>
        <div class="err-box" style="margin-top:12px;">이미 알려진 비밀번호 목록에 있어, 이론적 시간과 무관하게 즉시 노출될 수 있습니다.</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-glass">
          <div class="metric-val" style="font-size:1.3rem;">{format_seconds(crack_seconds)}</div>
          <div class="metric-lbl">예상 크랙 시간</div>
        </div>
        <div style="color:{text_hint};font-size:0.82rem;margin-top:10px;">초당 100억 회 시도가 가능한 오프라인 공격 가정치</div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with st.expander("💡 왜 '희귀도'와 '보안성'을 따로 볼까?"):
    st.markdown(f"""
    <div class="info-box">
      이론적인 전수조사 시간(엔트로피 기반)만 보면 안전해 보이는 비밀번호라도,<br><br>
      실제 유출 데이터에서 같은 구조나 동일한 문자열이 자주 등장한다면
      공격자는 전수조사가 아니라 <strong>패턴 기반 추측</strong>으로 훨씬 빠르게 접근할 수 있다.<br><br>
      즉, 진짜 보안성은<br>
      <strong>이론적 엔트로피 × 실제 데이터에서의 희귀도</strong><br>
      둘을 함께 봐야 한다.
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# SECTION 4 — 종합 점수
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">4️⃣</div>
  <div class="section-title-text">종합 점수</div>
</div>
""", unsafe_allow_html=True)

# 점수 계산
if is_common:
    rarity_score = 0
elif DATA_OK:
    rarity_score = clamp(100 - macro_pct * 10)
else:
    rarity_score = clamp(s_ent / 4 * 100)

length_score    = clamp(len(password) / 16 * 100)
entropy_score   = clamp(s_ent / 4 * 100)
pattern_penalty = bias_score * 15
security_score  = clamp((length_score * 0.4 + entropy_score * 0.6) - pattern_penalty)
if is_common:
    security_score = clamp(security_score, 0, 10)

col1, col2 = st.columns(2)

gauge_common = dict(
    axis={"range": [0, 100], "tickfont": {"color": gauge_font}},
    steps=[
        {"range": [0, 30],  "color": "rgba(255,90,90,0.22)"},
        {"range": [30, 70], "color": "rgba(255,210,90,0.18)"},
        {"range": [70, 100],"color": "rgba(90,255,160,0.18)"},
    ],
    bgcolor="rgba(0,0,0,0)",
    borderwidth=0,
)

with col1:
    fig1 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rarity_score,
        title={"text": "희귀도 점수", "font": {"color": gauge_font, "size": 15}},
        number={"font": {"color": gauge_font, "size": 40}},
        gauge={**gauge_common, "bar": {"color": "#7c8cff", "thickness": 0.6}},
    ))
    fig1.update_layout(
        height=260,
        margin=dict(t=60, b=10, l=20, r=20),
        paper_bgcolor=gauge_paper,
        plot_bgcolor =plot_bg,
    )
    st.markdown('<div class="glass-flat" style="padding:10px 16px;">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(f'<div style="text-align:center;color:{text_hint};font-size:0.80rem;padding-bottom:8px;">높을수록 드문 구조</div></div>', unsafe_allow_html=True)

with col2:
    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=security_score,
        title={"text": "보안 점수", "font": {"color": gauge_font, "size": 15}},
        number={"font": {"color": gauge_font, "size": 40}},
        gauge={**gauge_common, "bar": {"color": "#ff8cc6", "thickness": 0.6}},
    ))
    fig2.update_layout(
        height=260,
        margin=dict(t=60, b=10, l=20, r=20),
        paper_bgcolor=gauge_paper,
        plot_bgcolor =plot_bg,
    )
    st.markdown('<div class="glass-flat" style="padding:10px 16px;">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(f'<div style="text-align:center;color:{text_hint};font-size:0.80rem;padding-bottom:8px;">높을수록 안전</div></div>', unsafe_allow_html=True)


# =====================================================
# SECTION 5 — 개선 제안
# =====================================================

st.markdown(f"""
<div class="glass-divider"></div>
<div class="section-header">
  <div class="section-icon">5️⃣</div>
  <div class="section-title-text">개선 제안</div>
</div>
""", unsafe_allow_html=True)

tips = []
if is_common:
    tips.append(("🚨", "이미 알려진 흔한 비밀번호입니다. 즉시 사용을 중단하세요."))
if len(password) < 12:
    tips.append(("📏", "길이를 12자 이상으로 늘리면 전수조사 시간이 크게 증가합니다."))
if n_symbol == 0:
    tips.append(("✳️", "특수문자를 포함하면 문자 종류가 늘어나 추측 난이도가 높아집니다."))
if n_digit == 0 or n_upper == 0:
    tips.append(("🔠", "대문자, 숫자를 함께 섞어 문자 구성을 다양화하세요."))
if patterns_found:
    tips.append(("🧩", "연속된 숫자/문자, 키보드 패턴, 흔한 단어 등 예측 가능한 요소를 피하세요."))
if DATA_OK and macro_pct >= 0.5:
    tips.append(("🏗️", "문자를 바꾸더라도 구조 자체가 흔하면 위험합니다. 구조 자체를 다양화하세요."))

if not tips:
    st.markdown(f"""
    <div class="success-box">
      🎉 현재 입력한 비밀번호는 길이, 문자 구성, 패턴, 희귀도 측면에서 비교적 균형 잡힌 상태입니다.<br><br>
      다만 어떤 비밀번호든 <strong>다른 사이트와 재사용하지 않는 것</strong>이 가장 중요합니다.
    </div>
    """, unsafe_allow_html=True)
else:
    for icon, tip in tips:
        st.markdown(f"""
        <div class="tip-card">{icon} &nbsp; {tip}</div>
        """, unsafe_allow_html=True)

st.markdown(f'<div style="color:{text_hint};font-size:0.80rem;margin-top:10px;">이 페이지의 점수는 통계적 분석에 기반한 참고용 지표이며, 절대적인 보안 수준을 보장하지 않습니다.</div>', unsafe_allow_html=True)
