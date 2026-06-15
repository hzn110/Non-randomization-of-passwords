import streamlit as st
import math

# =========================
# PAGE STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "page2"  # 현재 페이지 (02)

def go(page_name):
    st.session_state.page = page_name
    st.rerun()

# =========================
# GLOBAL UI STYLE (GLASS DESIGN)
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0b1220, #020617);
    color: white;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* NAVBAR */
.navbar {
    position: sticky;
    top: 0;
    z-index: 999;

    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 12px 18px;

    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(18px);
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

/* TITLE */
.nav-title {
    font-size: 15px;
    font-weight: 600;
}

/* BUTTON STYLE */
.stButton > button {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: white;
    padding: 8px 14px;
    border-radius: 12px;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    background: rgba(99,102,241,0.25);
}

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
# NAVBAR
# =========================
st.markdown("""
<div class="navbar">
    <div class="nav-title">🔐 Password Security Lab</div>
</div>
""", unsafe_allow_html=True)

# =========================
# NAV BUTTONS
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 Main"):
        go("main")

with col2:
    if st.button("📊 Page 01"):
        go("page1")

with col3:
    if st.button("⚙ Page 02"):
        go("page2")

with col4:
    if st.button("🔐 Page 03"):
        go("page3")

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
