import math

# =========================
# CONFIG
# PAGE STATE
# =========================
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
