import math

# =========================
# CONFIG
# PAGE STATE
# =========================import os
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
    layout="wide"
)

# =====================================================
# 데이터 불러오기 (없어도 페이지 동작은 가능하도록)
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
        if ch.isupper():
            macro += "U"
        elif ch.islower():
            macro += "L"
        elif ch.isdigit():
            macro += "d"
        else:
            macro += "s"
    return macro


def charset_size(password):
    size = 0
    if any(c.islower() for c in password):
        size += 26
    if any(c.isupper() for c in password):
        size += 26
    if any(c.isdigit() for c in password):
        size += 10
    if any(not c.isalnum() for c in password):
        size += 32
    return max(size, 1)


def theoretical_entropy(password):
    """문자 구성(charset)만 고려한 이론적 엔트로피 (bits)"""
    if not password:
        return 0.0
    return len(password) * math.log2(charset_size(password))


RUNS = "0123456789abcdefghijklmnopqrstuvwxyz"
RUNS_REV = RUNS[::-1]
KEYBOARD_PATTERNS = ["qwerty", "qwer", "asdf", "asdfgh", "zxcv", "1qaz", "zaq1"]


def detect_pattern_count(password):
    """예측 가능한 패턴의 개수를 센다 (엔트로피 감점용)"""
    lower = password.lower()
    count = 0

    # 연속 상승/하강 시퀀스 (3자 이상)
    for seq in (RUNS, RUNS_REV):
        for i in range(len(seq) - 2):
            chunk = seq[i:i + 3]
            if chunk in lower:
                count += 1
                break

    # 키보드 인접 패턴
    if any(p in lower for p in KEYBOARD_PATTERNS):
        count += 1

    # 동일 문자 3회 이상 반복
    if re.search(r"(.)\1{2,}", password):
        count += 1

    return count


def effective_entropy(password):
    """패턴 감점을 반영한 실질 엔트로피 (bits)"""
    penalty = detect_pattern_count(password) * 10
    return max(theoretical_entropy(password) - penalty, 0)


def entropy_grade(bits):
    if bits < 20:
        return "낮음", "🔴"
    elif bits < 40:
        return "보통", "🟡"
    else:
        return "높음", "🟢"


def estimate_crack_seconds(password, guesses_per_second=1_000_000):
    """비밀번호 전수조사 예상 시간 (초). 기본: 초당 100만 회 시도 가정"""
    combos = charset_size(password) ** max(len(password), 1)
    return combos / guesses_per_second / 2


def format_seconds(seconds):
    if seconds < 1:
        return "1초 미만"
    units = [
        ("년", 60 * 60 * 24 * 365),
        ("일", 60 * 60 * 24),
        ("시간", 60 * 60),
        ("분", 60),
        ("초", 1),
    ]
    for name, unit in units:
        if seconds >= unit:
            value = seconds / unit
            if value > 1e12:
                return f"{value:.2e} {name} 이상"
            return f"약 {value:,.1f}{name}"
    return "1초 미만"


def risk_label(pct):
    if pct is None:
        return "데이터 없음", "⚪"
    if pct <= 1:
        return "매우 위험", "🔴"
    elif pct <= 10:
        return "위험", "🟠"
    elif pct <= 50:
        return "보통", "🟡"
    else:
        return "비교적 안전", "🟢"


# =====================================================
# 사이드바 - 정보보안 용어 사전
# =====================================================

with st.sidebar:
    st.title("📚 정보보안 용어 사전")

    with st.expander("엔트로피 (Entropy)"):
        st.write("""
        비밀번호가 얼마나 예측하기 어려운지를 비트(bit) 단위로 나타낸 값이다.

        엔트로피가 높을수록
        무차별 대입 공격에 더 많은 시도가 필요하다.
        """)

    with st.expander("사전 공격 (Dictionary Attack)"):
        st.write("""
        무작위로 모든 조합을 시도하는 대신,

        실제 사람들이 자주 쓰는 비밀번호/패턴 목록(사전)을
        우선적으로 시도하는 공격 방식이다.

        인간의 선택이 특정 패턴에 몰려 있을수록
        이 공격은 매우 효율적으로 작동한다.
        """)

    with st.expander("브루트포스 (Brute Force)"):
        st.write("""
        가능한 모든 조합을 처음부터 끝까지
        전부 시도해보는 공격 방식이다.

        이론적으로는 가장 확실하지만,
        엔트로피가 높을수록 시간이 기하급수적으로 늘어난다.
        """)

    with st.expander("Zipf의 법칙"):
        st.write("""
        소수의 항목이 전체 빈도의 대부분을 차지하고,

        나머지 수많은 항목은 매우 낮은 빈도로 분포하는
        '멱법칙(power-law)' 형태의 분포이다.

        비밀번호의 구조(거시상태) 분포 역시
        이와 유사한 형태를 보인다.
        """)

# =====================================================
# 제목
# =====================================================

st.title("🛡️ 인간의 비밀번호 선택은 정보보안에 어떤 영향을 주는가?")

st.markdown("""
### 앞선 통계물리학적 분석 결과를 실제 정보보안 관점으로 연결한다
""")

st.info("""
🎯 목표

1, 2페이지에서 우리는 인간의 비밀번호 선택이
완전히 무작위가 아니라 특정 구조(거시상태)에 몰려 있음을 확인했다.

이 페이지에서는 그 비무작위성이

실제 공격(사전 공격, 브루트포스)에 어떤 영향을 주는지를
직접 체험해본다.
""")

# =====================================================
# SECTION 0 — 상태 분포와 Zipf의 법칙
# =====================================================

st.divider()
st.header("0️⃣ 패턴은 왜 위험한가? — 상태 분포와 Zipf의 법칙")

if DATA_OK:
    macro_counts = df["macrostate"].value_counts().reset_index()
    macro_counts.columns = ["macrostate", "count"]
    macro_counts["rank"] = range(1, len(macro_counts) + 1)

    top_n = 200
    plot_df = macro_counts.head(top_n)

    fig = px.line(
        plot_df,
        x="rank",
        y="count",
        log_x=True,
        log_y=True,
        title="거시상태(구조) 빈도 분포 — Rank vs Frequency (log-log)"
    )
    st.plotly_chart(fig, use_container_width=True)

    total = macro_counts["count"].sum()
    top10_ratio = macro_counts.head(10)["count"].sum() / total * 100

    st.markdown(f"""
    상위 **10개** 구조(거시상태)가 전체 비밀번호의
    약 **{top10_ratio:.1f}%** 를 차지한다.

    로그-로그 그래프에서 거의 직선에 가까운 형태가 나타나는 것은,

    Zipf의 법칙처럼 **소수의 패턴이 압도적인 빈도**를 차지하고
    나머지는 길게 늘어진 분포를 보인다는 뜻이다.
    """)

    with st.expander("💡 이게 왜 사전 공격으로 이어질까?"):
        st.info("""
        만약 인간의 선택이 진짜 무작위였다면

        모든 구조(거시상태)는 거의 비슷한 빈도로 나타나야 한다.

        하지만 실제로는 일부 구조에 빈도가 집중되어 있다.

        공격자는 이 사실을 알고 있기 때문에,

        가능한 모든 조합을 시도하기 전에

        '자주 등장하는 구조 / 자주 등장하는 비밀번호'부터
        먼저 시도한다.

        이것이 바로 **사전 공격(Dictionary Attack)** 이다.
        """)
else:
    st.warning("⚠️ 비교용 데이터셋(rockyou_rigorous_behavioral_physics_v2.csv)을 불러오지 못해 이 섹션은 표시할 수 없습니다.")

# =====================================================
# SECTION 1 — 비밀번호 강도 측정기
# =====================================================

st.divider()
st.header("1️⃣ 비밀번호 강도 측정기")

st.markdown("비밀번호를 입력하면 길이, 엔트로피, 예상 크래킹 시간을 계산한다.")

pw1 = st.text_input("분석할 비밀번호를 입력하세요", type="password", key="pw1")

if pw1:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("길이", f"{len(pw1)}자")

    with col2:
        ent = effective_entropy(pw1)
        st.metric("실질 엔트로피", f"{ent:.1f} bits")

    with col3:
        crack_sec = estimate_crack_seconds(pw1)
        st.metric("예상 크래킹 시간", format_seconds(crack_sec))

    grade, emoji = entropy_grade(effective_entropy(pw1))
    st.markdown(f"**엔트로피 등급: {emoji} {grade}**")

    with st.expander("💡 '실질 엔트로피'란?"):
        st.info("""
        이론적 엔트로피는 '어떤 문자 종류를 썼는가'만 본다.

        하지만 1234, qwerty, 같은 문자 반복처럼
        사람이 자주 쓰는 패턴이 포함되면

        실제 추측 난이도는 이론값보다 훨씬 낮아진다.

        이 페이지에서는 그런 패턴이 발견될 때마다
        엔트로피에서 일정 비트를 감점하여
        '실질 엔트로피'를 계산한다.
        """)
else:
    st.info("👆 비밀번호를 입력하면 분석 결과가 표시됩니다.")

# =====================================================
# SECTION 2 — 실제 데이터와 비교
# =====================================================

st.divider()
st.header("2️⃣ 실제 데이터와 비교")

st.markdown("""
입력한 비밀번호의 **구조(거시상태)** 가
실제 유출 데이터에서 얼마나 자주 등장하는 구조인지 비교한다.

예) `abc123` → `lllddd` 구조 → 상위 1% 패턴 → **매우 위험**
""")

pw2 = st.text_input("비교할 비밀번호를 입력하세요 (기본값: abc123)", value="abc123", key="pw2")

if pw2 and DATA_OK:
    macro2 = get_macrostate(pw2)
    macro_counts2 = df["macrostate"].value_counts().reset_index()
    macro_counts2.columns = ["macrostate", "count"]
    macro_counts2["rank"] = range(1, len(macro_counts2) + 1)
    total_unique = len(macro_counts2)

    match = macro_counts2[macro_counts2["macrostate"] == macro2]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("구조 (Macrostate)", macro2)

    if not match.empty:
        rank = int(match["rank"].iloc[0])
        pct = rank / total_unique * 100
        ratio = match["count"].iloc[0] / df.shape[0] * 100

        with col2:
            st.metric("패턴 순위", f"상위 {pct:.1f}%")

        with col3:
            st.metric("데이터 내 비율", f"{ratio:.4f}%")

        label, emoji = risk_label(pct)
        st.markdown(f"**위험도: {emoji} {label}**")

        if pct <= 1:
            st.error("이 구조는 데이터셋에서 **가장 흔한 패턴 상위 1%** 안에 속한다. 사전 공격의 1순위 후보다.")
        elif pct <= 10:
            st.warning("이 구조는 비교적 흔한 패턴이다. 사전 공격 목록에 포함될 가능성이 높다.")
        else:
            st.success("이 구조는 비교적 드문 패턴이다.")
    else:
        with col2:
            st.metric("패턴 순위", "데이터에 없음")
        with col3:
            st.metric("데이터 내 비율", "0%")
        st.success("이 구조는 분석 데이터셋에서 발견되지 않은, 비교적 드문 구조다.")

elif pw2 and not DATA_OK:
    st.warning("⚠️ 비교용 데이터셋을 불러오지 못해 이 섹션은 표시할 수 없습니다.")

# =====================================================
# SECTION 3 — 엔트로피 비교
# =====================================================

st.divider()
st.header("3️⃣ 엔트로피 비교")

st.markdown("같은 길이라도 어떤 패턴을 쓰느냐에 따라 실질 엔트로피가 크게 달라진다.")

sample_pw = ["123456", "abc123", "qwerty123", "X7!kP2#z"]

rows = []
for p in sample_pw:
    bits = effective_entropy(p)
    grade, emoji = entropy_grade(bits)
    rows.append({
        "비밀번호": p,
        "실질 엔트로피 (bits)": round(bits, 1),
        "등급": f"{emoji} {grade}"
    })

entropy_df = pd.DataFrame(rows)

col1, col2 = st.columns([1, 1.4])

with col1:
    st.dataframe(entropy_df, hide_index=True, use_container_width=True)

with col2:
    fig = px.bar(
        entropy_df,
        x="비밀번호",
        y="실질 엔트로피 (bits)",
        color="등급",
        color_discrete_map={"🔴 낮음": "#ff5a5a", "🟡 보통": "#ffd25a", "🟢 높음": "#5affa0"},
        title="실질 엔트로피 비교"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
`123456` 과 `abc123` 은 문자 종류만 보면 나쁘지 않아 보이지만,

연속된 숫자/알파벳 패턴이 그대로 엔트로피를 깎아먹는다.

반면 `X7!kP2#z` 는 길이는 비슷해도

대문자·소문자·숫자·특수문자가 불규칙하게 섞여 있어
패턴 감점이 거의 없다.
""")

# =====================================================
# SECTION 4 — 가상 브루트포스 시뮬레이터
# =====================================================

st.divider()
st.header("4️⃣ 가상 브루트포스 시뮬레이터")

st.markdown("""
초당 약 100만 번 시도가 가능한 컴퓨터를 가정했을 때,

`123456` 과 `X7!kP2#z` 를 전수조사하는 데 걸리는 시간을 비교해본다.
""")

weak_pw = "123456"
strong_pw = "X7!kP2#z"

weak_time = estimate_crack_seconds(weak_pw)
strong_time = estimate_crack_seconds(strong_pw)

if st.button("🚀 브루트포스 시뮬레이션 실행"):

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### `{weak_pw}`")
        bar1 = st.progress(0)
        for i in range(0, 101, 20):
            bar1.progress(i)
            time.sleep(0.04)
        st.error(f"🔓 크랙 완료! 예상 소요 시간: **{format_seconds(weak_time)}**")

    with col2:
        st.markdown(f"#### `{strong_pw}`")
        bar2 = st.progress(0)
        for i in range(0, 101, 4):
            bar2.progress(i)
            time.sleep(0.04)
        st.success(f"🔒 같은 속도로는 예상 소요 시간: **{format_seconds(strong_time)}**")

    st.markdown(f"""
    같은 길이의 비밀번호라도,

    `{weak_pw}` 는 사람이 자주 쓰는 연속 숫자 패턴이라
    **{format_seconds(weak_time)}** 만에 뚫리지만,

    `{strong_pw}` 는 문자 구성이 불규칙해서
    **{format_seconds(strong_time)}** 가 걸린다.
    """)
else:
    st.caption("버튼을 누르면 두 비밀번호의 전수조사 과정을 시뮬레이션합니다.")

# =====================================================
# 정보보안 결론
# =====================================================

st.divider()
st.header("📌 정보보안 결론")

st.success("""
- 인간은 랜덤하지 않다.

- 인간은 기억하기 쉬운 패턴에 집중한다.

- 이 현상은 엔트로피 감소로 설명 가능하다.

- 공격자는 이를 이용해 사전 공격(Dictionary Attack)을 수행한다.

- 따라서 강한 비밀번호는 인간의 직관을 거스르는 방향으로 만들어야 한다.
""")

# =====================================================
# 최종 탐구 결론
# =====================================================

st.divider()
st.header("🧠 최종 탐구 결론")

st.success("""
통계물리학적으로 인간의 비밀번호 선택은 높은 엔트로피 상태가 아니라
특정 패턴에 집중된 낮은 엔트로피 상태를 보인다.

이러한 비무작위성은 정보보안 측면에서 예측 가능성을 증가시키며,
결과적으로 비밀번호 크래킹 성공률을 높이는 원인이 된다.

따라서 안전한 비밀번호 설계를 위해서는
인간의 자연스러운 선택 경향을 의도적으로 피해야 한다.
""")
st.set_page_config(
    page_title="Entropy → Security",
    layout="wide"
)
if "page" not in st.session_state:
    st.session_state.page = "page2"  # 현재 페이지 (02)

def go(page_name):
    st.session_state.page = page_name
    st.rerun()

# =========================
# MODERN GLASS UI
# GLOBAL UI STYLE (GLASS DESIGN)
# =========================
st.markdown("""
<style>
@@ -20,157 +22,186 @@
   font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* glass card */
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
}
/* NAVBAR */
.navbar {
    position: sticky;
    top: 0;
    z-index: 999;

/* highlight flow */
.flow {
   display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.badge {
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("🔁 Entropy Flow: Physics → Security")
    justify-content: space-between;
    align-items: center;

st.markdown("""
<div class="card">
<strong>핵심 질문</strong><br><br>
왜 ‘물리에서의 엔트로피’ 개념이 ‘정보보안 취약성’과 연결되는가?
</div>
""", unsafe_allow_html=True)

# =========================
# 1. PHYSICS LAYER
# =========================
st.markdown("""
<div class="card">
<h3>1. Physics Layer (통계물리)</h3>
    padding: 12px 18px;

<div class="flow">
<span class="badge">Microstate</span>
<span class="badge">Entropy</span>
<span class="badge">Probability Distribution</span>
</div>

<br>

시스템은 가능한 상태가 많을수록 엔트로피가 증가한다.<br>
하지만 인간 선택은 균등 분포가 아니라 <b>편향된 분포</b>를 가진다.
</div>
""", unsafe_allow_html=True)

# =========================
# 2. HUMAN BEHAVIOR
# =========================
st.markdown("""
<div class="card">
<h3>2. Human Behavior Layer</h3>
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(18px);
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

<div class="flow">
<span class="badge">Memory Bias</span>
<span class="badge">Keyboard Patterns</span>
<span class="badge">Shortcuts</span>
</div>
/* TITLE */
.nav-title {
    font-size: 15px;
    font-weight: 600;
}

<br>
/* BUTTON STYLE */
.stButton > button {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: white;
    padding: 8px 14px;
    border-radius: 12px;
    transition: 0.2s;
}

인간은 랜덤을 생성하지 않는다.<br>
대신 “기억하기 쉬운 상태”를 선택한다.<br><br>
.stButton > button:hover {
    transform: translateY(-2px);
    background: rgba(99,102,241,0.25);
}

→ 결과: 상태 공간이 급격히 축소됨 (Entropy 감소)
</div>
/* CARD */
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 18px;
    margin-top: 15px;
    backdrop-filter: blur(16px);
}
</style>
""", unsafe_allow_html=True)

# =========================
# 3. SECURITY LAYER
# NAVBAR
# =========================
st.markdown("""
<div class="card">
<h3>3. Security Layer (정보보안)</h3>

<div class="flow">
<span class="badge">Dictionary Attack</span>
<span class="badge">Pattern Exploitation</span>
<span class="badge">Brute Force</span>
</div>

<br>

공격자는 인간의 편향을 이용해 탐색 공간을 줄인다.<br>
즉, 실제 공격은 “무작위”가 아니라 “확률 기반 탐색”이다.
<div class="navbar">
    <div class="nav-title">🔐 Password Security Lab</div>
</div>
""", unsafe_allow_html=True)

# =========================
# 4. INTERACTIVE MINI SIM
# NAV BUTTONS
# =========================
st.markdown("### ⚡ 패턴 위험 시각화")

pw = st.text_input("비밀번호 입력")

def score(pw):
    s = 0
    if pw.lower() in ["123456","qwerty","password"]:
        s += 90
    if pw.isdigit():
        s += 60
    if len(pw) < 8:
        s += 30
    return min(s, 100)

if pw:
    risk = score(pw)
col1, col2, col3, col4 = st.columns(4)

    st.progress(risk / 100)
with col1:
    if st.button("🏠 Main"):
        go("main")

    if risk < 30:
        st.success("Low Risk (상대적으로 안전)")
    elif risk < 70:
        st.warning("Medium Risk (패턴 가능성 존재)")
    else:
        st.error("High Risk (공격 대상 가능성 높음)")
with col2:
    if st.button("📊 Page 01"):
        go("page1")

# =========================
# 5. FINAL BRIDGE (핵심 페이지)
# =========================
st.markdown("""
<div class="card">
<h2>🔗 Physics → Security 연결</h2>

<div class="flow">
<span class="badge">Entropy 감소</span>
<span class="badge">State Bias</span>
<span class="badge">Predictability 증가</span>
<span class="badge">Attack Success ↑</span>
</div>
with col3:
    if st.button("⚙ Page 02"):
        go("page2")

<br>
with col4:
    if st.button("🔐 Page 03"):
        go("page3")

물리 시스템에서의 엔트로피 감소는 단순한 열역학 개념이 아니라,<br>
정보 시스템에서는 “예측 가능성 증가”로 변환된다.<br><br>

즉, 인간의 선택은 물리적으로는 구조화된 상태이며<br>
정보보안에서는 취약성으로 해석된다.
</div>
""", unsafe_allow_html=True)
st.divider()

# =========================
# ENTROPY FUNCTION (CORE)
# =========================
def entropy(pw):
    pool = 0
    if any(c.islower() for c in pw): pool += 26
    if any(c.isupper() for c in pw): pool += 26
    if any(c.isdigit() for c in pw): pool += 10
    if any(not c.isalnum() for c in pw): pool += 10
    return len(pw) * math.log2(pool) if pool else 0

def crack_time(H):
    return 2**H / 1e9  # 10억 guesses/sec

# =========================
# ROUTER
# =========================

# -------------------------
# MAIN PAGE
# -------------------------
if st.session_state.page == "main":
    st.title("🔬 인간 비밀번호와 정보보안")

    st.markdown("""
    <div class="card">
    이 프로젝트는 인간의 비밀번호 선택이<br>
    통계물리학적 엔트로피 구조와 어떻게 연결되는지 분석한다.
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# PAGE 1
# -------------------------
elif st.session_state.page == "page1":
    st.title("📊 비밀번호 패턴 분석")

    data = {
        "123456": "매우 위험 (패턴 집중)",
        "abc123": "위험",
        "qwerty123": "중간 위험",
        "X7!kP2#z": "고엔트로피 (안전)"
    }

    for k, v in data.items():
        st.markdown(f"""
        <div class="card">
        <b>{k}</b><br>{v}
        </div>
        """, unsafe_allow_html=True)

# -------------------------
# PAGE 2 (CURRENT)
# -------------------------
elif st.session_state.page == "page2":
    st.title("⚙ 비밀번호 보안 분석 (Entropy Model)")

    st.markdown("""
    <div class="card">
    엔트로피는 가능한 상태 수와 로그적으로 증가한다.<br>
    인간의 선택은 균등 분포가 아니라 편향된 분포를 가진다.
    </div>
    """, unsafe_allow_html=True)

    pw = st.text_input("비밀번호 입력")

    if pw:
        H = entropy(pw)
        T = crack_time(H)

        st.metric("Entropy (bits)", round(H, 2))

        if T < 1:
            label = "즉시"
        elif T < 3600:
            label = "짧은 시간"
        elif T < 86400:
            label = "수일"
        elif T < 31536000:
            label = "수년"
        else:
            label = "수십 년 이상"

        st.metric("Crack Time", label)

# -------------------------
# PAGE 3
# -------------------------
elif st.session_state.page == "page3":
    st.title("🔐 정보보안 해석")

    st.markdown("""
    <div class="card">
    공격자는 무작위 탐색이 아니라<br>
    인간의 패턴 기반 확률 탐색을 수행한다.<br><br>

    → Dictionary Attack<br>
    → Pattern Exploitation<br>
    → Reduced Search Space
    </div>
    """, unsafe_allow_html=True)
