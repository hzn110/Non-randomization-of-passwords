import streamlit as st

st.set_page_config(
    page_title="인간이 만든 비밀번호는 정말 랜덤할까?",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================
# CSS
# ======================
st.markdown("""
<style>

.block-container{
    padding-top:1rem;
    max-width:1200px;
}

.hero{
    text-align:center;
    padding:5rem 1rem;
}

.hero-title{
    font-size:4rem;
    font-weight:700;
    line-height:1.1;
}

.hero-subtitle{
    margin-top:15px;
    color:rgba(255,255,255,0.6);
    font-size:1.2rem;
}

.glass{
    background:rgba(255,255,255,0.04);
    backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:28px;
    padding:30px;
    margin-bottom:20px;
}

.glass:hover{
    background:rgba(255,255,255,0.06);
}

.card-title{
    font-size:1.4rem;
    font-weight:600;
}

.card-desc{
    color:rgba(255,255,255,0.65);
    margin-top:10px;
}

.question{
    text-align:center;
    padding:70px 20px;
    margin-top:30px;
}

.big-number{
    text-align:center;
    font-size:3rem;
    font-weight:700;
}

.big-label{
    text-align:center;
    color:gray;
}

</style>
""", unsafe_allow_html=True)

# ======================
# 메뉴
# ======================
page = st.sidebar.radio(
    "메뉴",
    [
        "홈",
        "① 생성 과정 분석",
        "② 규칙성 검증",
        "③ 정보보안 분석",
        "④ 비밀번호 안전도 측정"
    ]
)

# ======================
# 홈
# ======================
if page == "홈":

    st.markdown("""
    <div class="hero">

    <div class="hero-title">
    🔐 인간이 만든 비밀번호는<br>
    정말 랜덤할까?
    </div>

    <div class="hero-subtitle">
    Statistical Physics × Information Security
    </div>

    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="glass">
        <div class="big-number">1400만+</div>
        <div class="big-label">분석 대상 비밀번호</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass">
        <div class="big-number">100+</div>
        <div class="big-label">발견된 패턴</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="glass">
        <div class="big-number">2</div>
        <div class="big-label">융합 학문 분야</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 프로젝트 소개")

    st.markdown("""
    우리는 비밀번호를 만들 때 스스로는 무작위라고 생각한다.

    하지만 실제 비밀번호 데이터는 인간이 반복적으로 특정 규칙을 사용한다는 사실을 보여준다.

    본 프로젝트는 실제 유출 비밀번호 데이터를 활용하여 인간의 선택 행동을 통계물리학적으로 분석하고,
    그 결과를 정보보안 관점에서 해석하는 것을 목표로 한다.
    """)

    st.markdown("## 연구 진행 과정")

    col1,col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="glass">
        <div class="card-title">
        ① 생성 과정 분석
        </div>

        <div class="card-desc">
        비밀번호 길이, 문자 구성,
        엔트로피를 분석하여
        인간이 비밀번호를 만드는 과정을 탐구한다.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass">
        <div class="card-title">
        ② 규칙성 검증
        </div>

        <div class="card-desc">
        연속 숫자,
        키보드 배열,
        날짜 패턴 등을 통해
        인간 선택의 보편성을 검증한다.
        </div>
        </div>
        """, unsafe_allow_html=True)

    col3,col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="glass">
        <div class="card-title">
        ③ 정보보안 분석
        </div>

        <div class="card-desc">
        발견된 규칙성이
        실제 공격 환경에서 어떤 위험을 만드는지 분석한다.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="glass">
        <div class="card-title">
        ④ 비밀번호 안전도 측정
        </div>

        <div class="card-desc">
        사용자가 입력한 비밀번호의
        희귀도와 안전도를 평가한다.
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass question">

    <h2>🧠 핵심 연구 질문</h2>

    인간이 만든 비밀번호는 정말 랜덤할까?<br><br>

    그리고 그 비무작위성은<br>
    정보보안에 어떤 영향을 미칠까?

    </div>
    """, unsafe_allow_html=True)

# ======================
# 페이지1
# ======================
elif page == "① 생성 과정 분석":
    st.title("① 생성 과정 분석")
    st.info("팀원 담당 페이지")

# ======================
# 페이지2
# ======================
elif page == "② 규칙성 검증":
    st.title("② 규칙성 검증")
    st.info("팀원 담당 페이지")

# ======================
# 페이지3
# ======================
elif page == "③ 정보보안 분석":
    st.title("③ 정보보안 분석")
    st.info("추후 구현 예정")

# ======================
# 페이지4
# ======================
elif page == "④ 비밀번호 안전도 측정":
    st.title("④ 비밀번호 안전도 측정")
    st.info("추후 구현 예정")
