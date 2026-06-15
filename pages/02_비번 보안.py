import streamlit as st

# =========================
# STATE INIT
# =========================
if "page" not in st.session_state:
    st.session_state.page = "main"

def go(page):
    st.session_state.page = page
    st.rerun()

# =========================
# GLOBAL UI STYLE (GLASS NAV)
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

.nav-title {
    font-size: 15px;
    font-weight: 600;
}

/* BUTTONS */
.nav-btn {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: white;
    padding: 8px 14px;
    border-radius: 12px;
    margin-left: 8px;
    cursor: pointer;
}

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
# NAVIGATION BAR
# =========================
st.markdown("""
<div class="navbar">
    <div class="nav-title">🔐 Entropy Security Lab</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 Home"):
        go("main")

with col2:
    if st.button("📊 Analysis"):
        go("page1")

with col3:
    if st.button("⚙ Model"):
        go("page2")

with col4:
    if st.button("🔐 Security"):
        go("page3")

st.divider()

# =========================
# PAGES
# =========================

# -------------------------
# MAIN PAGE
# -------------------------
if st.session_state.page == "main":
    st.title("🔬 인간 비밀번호 선택과 정보보안")

    st.markdown("""
    <div class="card">
    이 프로젝트는 인간의 비밀번호 선택이
    통계물리학적 엔트로피 관점에서 어떻게 해석되는지 분석한다.
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# PAGE 1
# -------------------------
elif st.session_state.page == "page1":
    st.title("📊 비밀번호 패턴 분석")

    data = {
        "123456": "매우 위험 (상위 사용 패턴)",
        "abc123": "위험",
        "qwerty123": "중간",
        "X7!kP2#z": "안전"
    }

    for k, v in data.items():
        st.markdown(f"""
        <div class="card">
        <b>{k}</b><br>{v}
        </div>
        """, unsafe_allow_html=True)

# -------------------------
# PAGE 2 (PHYSICS → MODEL)
# -------------------------
elif st.session_state.page == "page2":
    st.title("⚙ 통계물리 모델")

    st.markdown("""
    <div class="card">
    엔트로피는 가능한 상태 수와 로그적으로 비례한다.<br><br>
    인간의 선택은 균등 분포가 아닌 편향된 분포를 가진다.<br><br>
    → 상태 공간이 축소된다.
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# PAGE 3 (SECURITY)
# -------------------------
elif st.session_state.page == "page3":
    st.title("🔐 정보보안 해석")

    st.markdown("""
    <div class="card">
    공격자는 무작위 탐색이 아니라<br>
    인간의 패턴을 이용한 확률 기반 탐색을 수행한다.<br><br>

    → Dictionary Attack<br>
    → Pattern Exploitation<br>
    → Reduced Search Space
    </div>
    """, unsafe_allow_html=True)
