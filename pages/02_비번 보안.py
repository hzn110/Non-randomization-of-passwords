import streamlit as st
import math

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Entropy → Security",
    layout="wide"
)

# =========================
# MODERN GLASS UI
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0b1220, #020617);
    color: white;
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

<div class="flow">
<span class="badge">Memory Bias</span>
<span class="badge">Keyboard Patterns</span>
<span class="badge">Shortcuts</span>
</div>

<br>

인간은 랜덤을 생성하지 않는다.<br>
대신 “기억하기 쉬운 상태”를 선택한다.<br><br>

→ 결과: 상태 공간이 급격히 축소됨 (Entropy 감소)
</div>
""", unsafe_allow_html=True)

# =========================
# 3. SECURITY LAYER
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
</div>
""", unsafe_allow_html=True)

# =========================
# 4. INTERACTIVE MINI SIM
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

    st.progress(risk / 100)

    if risk < 30:
        st.success("Low Risk (상대적으로 안전)")
    elif risk < 70:
        st.warning("Medium Risk (패턴 가능성 존재)")
    else:
        st.error("High Risk (공격 대상 가능성 높음)")

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

<br>

물리 시스템에서의 엔트로피 감소는 단순한 열역학 개념이 아니라,<br>
정보 시스템에서는 “예측 가능성 증가”로 변환된다.<br><br>

즉, 인간의 선택은 물리적으로는 구조화된 상태이며<br>
정보보안에서는 취약성으로 해석된다.
</div>
""", unsafe_allow_html=True)
