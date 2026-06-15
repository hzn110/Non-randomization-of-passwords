import streamlit as st

# =========================
# STATE INIT
# =========================
if "page" not in st.session_state:
    st.session_state.page = "page3"

def go(page_name):
    st.session_state.page = page_name
    st.rerun()

# =========================
# GLOBAL STYLE (GLASS UI)
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

/* BUTTON */
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
# NAV BUTTONS (핵심)
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
# PAGE 3 CONTENT (유지)
# =========================
if st.session_state.page == "page3":

    st.title("🔐 정보보안 해석")

    st.markdown("""
    <div class="card">
    <h3>3. Security Layer (정보보안)</h3>

    <b>공격 모델</b><br>
    → Dictionary Attack<br>
    → Pattern Exploitation<br>
    → Brute Force

    <br><br>

    인간의 비밀번호 선택은 무작위가 아니라<br>
    <b>확률적으로 편향된 탐색 공간</b>을 만든다.

    <br><br>

    → 결과적으로 공격자는 전체 공간이 아니라<br>
    “고확률 영역만 탐색”하게 된다.
    </div>
    """, unsafe_allow_html=True)

# =========================
# ROUTING (다른 페이지 연결)
# =========================
elif st.session_state.page == "main":
    st.title("🏠 Main Page")

    st.markdown("""
    <div class="card">
    메인 페이지로 이동됨
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "page1":
    st.title("📊 Page 01")

    st.markdown("""
    <div class="card">
    비밀번호 패턴 분석 페이지
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "page2":
    st.title("⚙ Page 02")

    st.markdown("""
    <div class="card">
    통계물리 (Entropy Model) 페이지
    </div>
    """, unsafe_allow_html=True)
