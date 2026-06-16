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
    page_title="내 비밀번호는 얼마나 흔할까?",
    page_icon="🔑",
    layout="wide"
)

# =====================================================
# 데이터 불러오기 (실패해도 분석은 동작하도록 처리)
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
    # 첫 번째 컬럼을 비밀번호 컬럼으로 사용
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
    common_set = set(common_list)
    COMMON_OK = True
except Exception:
    common_list = []
    common_set = set()
    COMMON_OK = False


# =====================================================
# 분석 함수 (1~2페이지와 동일한 통계물리 지표 재사용)
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
    total = 0.0
    prev = None
    for ch in password:
        pos = _key_position(ch)
        if pos is not None and prev is not None:
            total += math.sqrt((pos[0] - prev[0]) ** 2 + (pos[1] - prev[1]) ** 2)
        if pos is not None:
            prev = pos
    return total


def shannon_entropy(password):
    if not password:
        return 0.0
    counts = Counter(password)
    n = len(password)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


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


def order_parameter(password):
    if not password:
        return 0.0
    counts = {"U": 0, "L": 0, "d": 0, "s": 0}
    for ch in password:
        if ch.isupper():
            counts["U"] += 1
        elif ch.islower():
            counts["L"] += 1
        elif ch.isdigit():
            counts["d"] += 1
        else:
            counts["s"] += 1
    total = len(password)
    fractions = [c / total for c in counts.values()]
    ideal = 0.25
    return sum(abs(f - ideal) for f in fractions) / 2  # 0(균형) ~ 1(편중)


SEQUENCES = [
    "0123456789", "9876543210",
    "abcdefghijklmnopqrstuvwxyz",
]

KEYBOARD_PATTERNS = ["qwer", "asdf", "zxcv", "qwerty", "asdfgh", "1qaz", "zaq1"]
COMMON_WORDS = ["password", "love", "admin", "welcome", "iloveyou",
                "monkey", "dragon", "letmein", "qwerty", "123456"]


def detect_patterns(password):
    lower = password.lower()
    found = []

    # 연속 숫자/알파벳 (4자 이상)
    for seq in SEQUENCES:
        for i in range(len(seq) - 3):
            chunk = seq[i:i + 4]
            if chunk in lower:
                found.append("연속된 문자/숫자 (예: 1234, abcd)")
                break

    # 반복 문자 (3회 이상)
    if re.search(r'(.)\1{2,}', password):
        found.append("같은 문자 반복 (예: aaa, 111)")

    # 연도 패턴
    if re.search(r'(19|20)\d{2}', password):
        found.append("연도 형태 포함 (예: 1999, 2024)")

    # 키보드 패턴
    if any(p in lower for p in KEYBOARD_PATTERNS):
        found.append("키보드 인접 자판 패턴 (예: qwer, asdf)")

    # 흔한 단어
    if any(w in lower for w in COMMON_WORDS):
        found.append("흔히 쓰이는 단어 포함 (예: password, love)")

    return found


def human_bias_score(password):
    return len(detect_patterns(password))


def percentile_rank(series, value):
    series = series.dropna()
    if len(series) == 0:
        return None
    return float((series < value).mean() * 100)


def estimate_crack_time_seconds(password):
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    charset = 0
    charset += 26 if has_lower else 0
    charset += 26 if has_upper else 0
    charset += 10 if has_digit else 0
    charset += 32 if has_symbol else 0
    charset = max(charset, 1)

    combinations = charset ** max(len(password), 1)

    # 오프라인 공격 가정: 초당 100억(1e10) 회 시도
    guesses_per_second = 1e10
    return combinations / guesses_per_second / 2  # 평균적으로 절반만 탐색


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


# =====================================================
# 화면 구성
# =====================================================

st.title("🔑 내 비밀번호는 얼마나 흔할까?")
st.markdown("### 입력한 비밀번호의 희귀도(Rarity)와 보안성(Security)을 분석해보자")

st.info("""
🔒 입력하신 비밀번호는 서버에 저장되거나 전송되지 않고,
이 브라우저 화면 안에서만 분석에 사용됩니다.

다만 실제로 사용 중인 비밀번호 대신,
테스트용으로 변형한 비밀번호를 입력하는 것을 추천합니다.
""")

password = st.text_input("분석할 비밀번호를 입력해보세요", type="password")

if not password:
    st.stop()

# -----------------------------------------------------
# ① 기본 구조 분석
# -----------------------------------------------------

st.divider()
st.header("1️⃣ 기본 구조 분석")

macro = get_macrostate(password)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("길이", f"{len(password)}자")

with col2:
    n_upper = sum(c.isupper() for c in password)
    n_lower = sum(c.islower() for c in password)
    n_digit = sum(c.isdigit() for c in password)
    n_symbol = sum(not c.isalnum() for c in password)
    st.metric("문자 종류 수", sum(x > 0 for x in [n_upper, n_lower, n_digit, n_symbol]))

with col3:
    st.metric("섀넌 엔트로피", f"{shannon_entropy(password):.2f} bits")

with col4:
    st.metric("질서변수 (Order Parameter)", f"{order_parameter(password):.2f}")

st.markdown(f"""
**거시상태(Macrostate) 구조**: `{macro}`

(U = 대문자, L = 소문자, d = 숫자, s = 특수문자)
""")

with st.expander("💡 구조 읽는 법"):
    st.write("""
    예를 들어 `Password123!` 은 `Ulllllllddds` 형태의 거시상태를 가진다.

    문자 자체는 다르더라도, 같은 구조(거시상태)를 가진 비밀번호는
    실제 유출 데이터에서 매우 많이 발견된다.
    """)

# -----------------------------------------------------
# ② 희귀도 분석
# -----------------------------------------------------

st.divider()
st.header("2️⃣ 희귀도 분석 (Rarity)")

is_common = password.lower() in {p.lower() for p in common_list} if COMMON_OK else False

if COMMON_OK:
    if is_common:
        st.error(f"🚨 이 비밀번호는 실제 유출 데이터에서 자주 등장하는 **'흔한 비밀번호 목록'에 포함**되어 있습니다.")
    else:
        st.success("✅ 입력한 비밀번호는 흔한 비밀번호 목록(common_passwords.csv)에서 발견되지 않았습니다.")
else:
    st.warning("⚠️ common_passwords.csv 데이터를 불러오지 못해 흔한 비밀번호 여부는 확인할 수 없습니다.")

if DATA_OK:
    macro_counts = df["macrostate"].value_counts(normalize=True)
    macro_ratio = macro_counts.get(macro, 0.0)
    macro_pct = macro_ratio * 100

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "같은 구조(macrostate)를 가진 비밀번호 비율",
            f"{macro_pct:.4f}%"
        )

    with col2:
        if macro_pct > 0:
            surprisal = -math.log2(macro_ratio)
            st.metric("구조 희귀도 (Surprisal)", f"{surprisal:.2f} bits")
        else:
            st.metric("구조 희귀도 (Surprisal)", "데이터 내 발견되지 않음")

    if macro_pct >= 0.5:
        st.warning(f"""
        입력한 비밀번호와 **동일한 구조**를 가진 비밀번호가
        분석 데이터셋의 **{macro_pct:.2f}%** 를 차지합니다.

        문자가 달라도 구조가 흔하면, 공격자의 패턴 기반 추측 공격에 노출될 수 있습니다.
        """)
    else:
        st.success(f"""
        입력한 비밀번호와 동일한 구조를 가진 비밀번호는
        데이터셋에서 **{macro_pct:.4f}%** 로 비교적 드문 구조입니다.
        """)

    ent_pct = percentile_rank(df["shannon_entropy"], shannon_entropy(password))
    if ent_pct is not None:
        st.markdown(f"""
        입력한 비밀번호의 섀넌 엔트로피는 분석 데이터셋 내에서
        **상위 {100 - ent_pct:.1f}%** 수준입니다.
        (값이 높을수록 더 무작위적인 비밀번호)
        """)
else:
    st.warning("⚠️ 비교용 데이터셋(rockyou_rigorous_behavioral_physics_v2.csv)을 불러오지 못해 일부 비교 분석을 표시할 수 없습니다.")

# -----------------------------------------------------
# ③ 보안성 분석
# -----------------------------------------------------

st.divider()
st.header("3️⃣ 보안성 분석 (Security)")

patterns_found = detect_patterns(password)
bias_score = human_bias_score(password)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧩 발견된 인간적 패턴")
    if patterns_found:
        for p in patterns_found:
            st.write(f"- ⚠️ {p}")
    else:
        st.write("- ✅ 뚜렷한 인간 행동 패턴이 발견되지 않았습니다.")

    st.metric("Human Bias Score", bias_score)

with col2:
    st.subheader("⏱️ 이론적 전수조사 시간")

    crack_seconds = estimate_crack_time_seconds(password)

    if is_common:
        st.metric("예상 크랙 시간", "1초 미만")
        st.caption("이미 알려진 비밀번호 목록에 있어, 이론적 전수조사 시간과 무관하게 즉시 노출될 수 있습니다.")
    else:
        st.metric("예상 크랙 시간", format_seconds(crack_seconds))
        st.caption("초당 100억 회 시도가 가능한 오프라인 공격을 가정한 추정치입니다.")

with st.expander("💡 왜 '희귀도'와 '보안성'을 따로 볼까?"):
    st.info("""
    이론적인 전수조사 시간(엔트로피 기반)만 보면 안전해 보이는 비밀번호라도,

    실제 유출 데이터에서 같은 구조나 동일한 문자열이 자주 등장한다면

    공격자는 전수조사가 아니라 **패턴 기반 추측**으로 훨씬 빠르게 접근할 수 있다.

    즉, 진짜 보안성은

    이론적 엔트로피 × 실제 데이터에서의 희귀도

    둘을 함께 봐야 한다.
    """)

# -----------------------------------------------------
# ④ 종합 점수
# -----------------------------------------------------

st.divider()
st.header("4️⃣ 종합 점수")


def clamp(v, lo=0, hi=100):
    return max(lo, min(hi, v))


# 희귀도 점수: 100 = 매우 희귀, 0 = 매우 흔함
if is_common:
    rarity_score = 0
elif DATA_OK:
    rarity_score = clamp(100 - macro_pct * 10)
else:
    rarity_score = clamp(shannon_entropy(password) / 4 * 100)

# 보안 점수: 길이, 엔트로피, 패턴 감점 종합
length_score = clamp(len(password) / 16 * 100)
entropy_score = clamp(shannon_entropy(password) / 4 * 100)
pattern_penalty = bias_score * 15

security_score = clamp((length_score * 0.4 + entropy_score * 0.6) - pattern_penalty)

if is_common:
    security_score = clamp(security_score, 0, 10)

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rarity_score,
        title={"text": "희귀도 점수 (높을수록 드묾)"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#7c8cff"},
            "steps": [
                {"range": [0, 30], "color": "rgba(255,90,90,0.3)"},
                {"range": [30, 70], "color": "rgba(255,210,90,0.3)"},
                {"range": [70, 100], "color": "rgba(90,255,160,0.3)"},
            ],
        },
    ))
    fig.update_layout(height=280, margin=dict(t=60, b=10, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=security_score,
        title={"text": "보안 점수 (높을수록 안전)"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#ff8cc6"},
            "steps": [
                {"range": [0, 30], "color": "rgba(255,90,90,0.3)"},
                {"range": [30, 70], "color": "rgba(255,210,90,0.3)"},
                {"range": [70, 100], "color": "rgba(90,255,160,0.3)"},
            ],
        },
    ))
    fig.update_layout(height=280, margin=dict(t=60, b=10, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------
# ⑤ 개선 제안
# -----------------------------------------------------

st.divider()
st.header("5️⃣ 개선 제안")

tips = []

if is_common:
    tips.append("이미 알려진 흔한 비밀번호입니다. 즉시 사용을 중단하세요.")

if len(password) < 12:
    tips.append("길이를 12자 이상으로 늘리면 전수조사 시간이 크게 증가합니다.")

if n_symbol == 0:
    tips.append("특수문자를 포함하면 문자 종류가 늘어나 추측 난이도가 높아집니다.")

if n_digit == 0 or n_upper == 0:
    tips.append("대문자, 숫자를 함께 섞어 문자 구성을 다양화하세요.")

if patterns_found:
    tips.append("연속된 숫자/문자, 키보드 패턴, 흔한 단어 등 예측 가능한 요소를 피하세요.")

if DATA_OK and macro_pct >= 0.5:
    tips.append("문자를 바꾸더라도 구조(예: 소문자+숫자 8자리) 자체가 흔하면 위험합니다. 구조 자체를 다양화하세요.")

if not tips:
    st.success("""
    현재 입력한 비밀번호는 길이, 문자 구성, 패턴, 희귀도 측면에서
    비교적 균형 잡힌 상태로 보입니다.

    다만 어떤 비밀번호든 다른 사이트와 재사용하지 않는 것이 가장 중요합니다.
    """)
else:
    for t in tips:
        st.warning(f"- {t}")

st.caption("""
이 페이지의 점수는 통계적 분석에 기반한 참고용 지표이며,
절대적인 보안 수준을 보장하지 않습니다.
""")
