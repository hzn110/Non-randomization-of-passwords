import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="인간은 어떻게 비밀번호를 만드는가?",
    page_icon="🔐",
    layout="wide"
)

# =====================================================
# 홈 버튼
# =====================================================

if st.button("🏠 메인 화면으로 이동"):
    st.switch_page("Home.py")

# =====================================================
# 데이터 불러오기
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("rockyou_rigorous_behavioral_physics_v2 (1).csv")

df = load_data()

# =====================================================
# 사이드바
# =====================================================

with st.sidebar:

    st.title("📚 통계역학 용어 사전")

    with st.expander("미시상태 (Microstate)"):
        st.write("""
        통계역학에서 시스템을 구성하는 개별 상태를 의미한다.

        본 연구에서는 비밀번호 하나를
        하나의 미시상태라고 본다.
        """)

    with st.expander("거시상태 (Macrostate)"):
        st.write("""
        여러 미시상태를 묶는 큰 구조이다.

        서로 다른 비밀번호라도
        같은 구조를 가질 수 있다.
        """)

    with st.expander("질서변수 (Order Parameter)"):
        st.write("""
        특정 문자 종류에 얼마나 치우쳐 있는지를 나타낸다.

        값이 커질수록
        특정 문자 유형에 집중된다.
        """)

    with st.expander("자기조직화 (Self-Organization)"):
        st.write("""
        누구도 규칙을 만들지 않았는데

        전체 집단에서 일정한 패턴이 나타나는 현상이다.
        """)

# =====================================================
# 제목
# =====================================================

st.title("🔐 인간은 어떻게 비밀번호를 만드는가?")

st.markdown("""
### 통계역학적 관점에서 분석한 인간의 비밀번호 생성 과정
""")

st.info("""
🎯 탐구 질문

인간은 스스로 랜덤한 비밀번호를 만든다고 생각한다.

하지만 정말 그럴까?

통계역학에서는 수많은 입자의 작은 움직임이 모여
거대한 질서를 만든다고 설명한다.

이 페이지에서는 사람들의 비밀번호 선택 역시
비슷한 방식으로 설명할 수 있는지 탐구한다.
""")

# =====================================================
# SECTION 1
# =====================================================

st.divider()

st.header("1️⃣ 비밀번호 하나는 하나의 미시상태(Microstate)")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "전체 비밀번호 수",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "고유 비밀번호 수",
        f"{df['microstate'].nunique():,}"
    )

with st.expander("💡 미시상태란?"):

    st.info("""
    통계역학에서는 기체를 이루는 개별 분자의 상태를
    미시상태라고 부른다.

    이 연구에서는

    abc123
    password
    qwerty

    와 같은 비밀번호 하나하나를
    하나의 미시상태로 생각한다.
    """)

# =====================================================
# SECTION 2
# =====================================================

st.divider()

st.header("2️⃣ 인간은 어떤 특징을 가진 비밀번호를 선호할까?")

st.subheader("인간 행동 편향 점수")

fig = px.histogram(
    df,
    x="human_bias_score",
    nbins=40,
    title="Human Bias Score 분포"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
Human Bias Score는

• 연속 숫자

• 반복 문자

• 날짜

• 연도

• 키보드 패턴

등 인간이 자주 사용하는 특징을 종합한 점수이다.

점수가 높을수록 인간적인 선택의 흔적이 강하다.
""")

st.subheader("타이핑 이동 거리")

fig = px.histogram(
    df,
    x="keyboard_path_length",
    nbins=40,
    title="Keyboard Path Length 분포"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
비밀번호를 입력할 때 손가락이
키보드 위를 얼마나 이동했는지를 나타낸다.

사람들은 무의식적으로

입력하기 쉬운 패턴을 선호할 가능성이 있다.
""")

# =====================================================
# SECTION 3
# =====================================================

st.divider()

st.header("3️⃣ 개별 선택은 어떤 구조를 만드는가?")

top_macro = (
    df["macrostate"]
    .value_counts()
    .head(15)
    .reset_index()
)

top_macro.columns = ["Macrostate", "Count"]

fig = px.bar(
    top_macro,
    x="Macrostate",
    y="Count",
    title="가장 많이 등장하는 거시상태"
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("💡 거시상태란?"):

    st.info("""
    비밀번호 자체가 아니라

    문자 구조만 남긴 형태이다.

    예)

    Password123!

    ↓

    Llllllllddds

    서로 다른 비밀번호라도
    같은 구조를 가지면 같은 거시상태가 된다.
    """)

st.markdown("""
사람들은 수많은 비밀번호를 만들지만

놀랍게도 일부 구조에 집중되는 경향이 나타난다.

즉,

각자의 선택이 모여
거시적인 규칙성을 만들어낸다.
""")

# =====================================================
# SECTION 4
# =====================================================

st.divider()

st.header("4️⃣ 비밀번호에는 질서가 존재하는가?")

fig = px.histogram(
    df,
    x="order_parameter",
    nbins=50,
    title="Order Parameter 분포"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
Order Parameter는

문자 종류가 얼마나 균형 있게 사용되었는지를 나타낸다.

만약 인간이 완전히 랜덤하게 비밀번호를 만들었다면

문자 사용도 비교적 균형적이어야 한다.

그러나 실제로는 특정 문자 종류에
집중되는 경향이 나타난다.
""")

with st.expander("💡 질서변수란?"):

    st.info("""
    질서변수(Order Parameter)는

    시스템이 얼마나 특정 상태에
    집중되어 있는지를 나타내는 값이다.

    값이 높을수록
    특정 문자 유형 사용이 강하게 나타난다.

    이는 인간이 무작위보다는
    특정 방식을 선호한다는 신호가 될 수 있다.
    """)

# =====================================================
# 결론
# =====================================================

st.divider()

st.header("📌 결론")

st.success("""
인간은 비밀번호를 만들 때

완전히 무작위적으로 선택하지 않는다.

기억하기 쉬움,

입력하기 쉬움,

익숙한 패턴,

반복되는 습관과 같은 작은 요인들이 모여

특정 구조를 가진 비밀번호를 만들어낸다.

즉,

비밀번호 생성은 단순한 개인의 선택이 아니라

수많은 미시적 행동이 모여
거시적 질서를 형성하는

통계역학적 현상으로 해석할 수 있다.

➡️ 다음 페이지에서는

이러한 행동 편향이 실제 데이터에서
어떤 규칙성으로 나타나는지 검증한다.
""")
