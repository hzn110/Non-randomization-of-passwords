import streamlit as st
import math
import random
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="정보보안 결론",
    page_icon="🔐",
    layout="wide"
)

# =========================
# APPLE LIQUID GLASS UI
# =========================
st.markdown("""
<style>
/* 배경 */
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: white;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 글래스 카드 */
.glass {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* 버튼 */
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border-radius: 12px;
    padding: 0.6rem 1rem;
    border: none;
    transition: 0.2s;
}
.stButton > button:hover {
    transform: scale(1.03);
}

/* 텍스트 */
h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("🔐 인간의 비밀번호 선택과 정보보안")

st.markdown("""
<div class="glass">
<h3>탐구 목표</h3>
인간의 비밀번호 선택 패턴이 정보보안에 미치는 영향을
<strong>통계물리학적 엔트로피 관점</strong>에서 분석한다.
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================
# 분석 1: 엔트로피 계산
# =========================
def entropy(password):
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(not c.isalnum() for c in password): pool += 10
    
    if pool == 0:
        return 0
    
    return len(password) * math.log2(pool)

def crack_time(entropy_value):
    # 매우 단순한 모델 (초 단위)
    guesses = 2 ** entropy_value
    speed = 1e9  # 10억/초 가정
    seconds = guesses / speed
    
    if seconds < 1:
        return "즉시"
    elif seconds < 3600:
        return "몇 초 ~ 몇 시간"
    elif seconds < 86400:
        return "수일"
    elif seconds < 31536000:
        return "수년"
    else:
        return "수십 년 이상"

st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("📊 비밀번호 강도 측정기")

pw = st.text_input("비밀번호 입력")

if pw:
    e = entropy(pw)
    t = crack_time(e)

    st.metric("엔트로피", f"{e:.2f} bits")
    st.metric("예상 크래킹 시간", t)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# =========================
# 분석 2: 실제 패턴 비교
# =========================
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("📉 인간 비밀번호 패턴 분석")

data = {
    "123456": "상위 0.1% 사용 패턴 / 매우 위험",
    "abc123": "상위 1% 패턴 / 위험",
    "qwerty123": "상위 5% 패턴 / 보통 위험",
    "X7!kP2#z": "하위 1% 패턴 / 안전"
}

for k, v in data.items():
    st.write(f"**{k}** → {v}")

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# =========================
# 분석 3: 브루트포스 시뮬
# =========================
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("💥 브루트포스 시뮬레이터")

if st.button("시뮬레이션 실행"):
    examples = {
        "123456": 0.01,
        "abc123": 0.05,
        "qwerty123": 2,
        "X7!kP2#z": 25
    }

    for k, v in examples.items():
        st.write(f"🔑 {k}")
        bar = st.progress(0)

        for i in range(100):
            time.sleep(0.005)
            bar.progress(i + 1)

        st.write(f"→ {v}초 / 수년~수십년 차이 발생")

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# =========================
# 결론
# =========================
st.markdown("""
<div class="glass">
<h2>🧠 정보보안 결론</h2>

<ul>
<li>인간은 랜덤하지 않다</li>
<li>기억하기 쉬운 패턴에 집중한다</li>
<li>이로 인해 엔트로피가 낮아진다</li>
<li>공격자는 이를 이용해 사전 공격을 수행한다</li>
</ul>

<hr>

<h3>📌 최종 결론</h3>
통계물리학적으로 인간의 비밀번호 선택은 높은 엔트로피 상태가 아니라<br>
특정 패턴에 집중된 낮은 엔트로피 상태이다.<br><br>

이는 정보보안 측면에서 예측 가능성을 증가시키며,<br>
결과적으로 비밀번호 크래킹 성공률을 높인다.<br><br>

따라서 안전한 비밀번호 설계를 위해서는<br>
<strong>인간의 직관을 거스르는 비직관적 구조</strong>가 필요하다.
</div>
""", unsafe_allow_html=True)
