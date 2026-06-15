import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import re

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
        하나의 미시상태로 본다.
        """)

    with st.expander("거시상태 (Macrostate)"):
        st.write("""
        서로 다른 비밀번호라도

        같은 구조를 가지면

        같은 거시상태(Macrostate)로 분류한다.
        """)

    with st.expander("질서변수 (Order Parameter)"):
        st.write("""
        특정 문자 종류에 얼마나 집중되어 있는지를 나타낸다.
        """)

    with st.expander("자기조직화 (Self-Organization)"):
        st.write("""
        개별 행동은 무작위처럼 보이지만

        전체 집단에서는 일정한 패턴이
        자연스럽게 나타나는 현상이다.
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

비밀번호 선택 역시 비슷한 방식으로
설명할 수 있을까?
""")

# =====================================================
# SECTION 1
# =====================================================

st.divider()

st.header("1️⃣ 당신은 랜덤한 비밀번호를 만들 수 있을까?")

user_pw = st.text_input(
    "무작위라고 생각하는 비밀번호를 입력해보세요"
)

if user_pw:

    length = len(user_pw)

    digit_count = sum(c.isdigit() for c in user_pw)
    upper_count = sum(c.isupper() for c in user_pw)
    lower_count = sum(c.islower() for c in user_pw)

    repeated = len(set(user_pw)) < len(user_pw)

    sequential = bool(
        re.search(
            r"123|234|345|456|567|678|789|abc|qwe",
            user_pw.lower()
        )
    )

    st.subheader("분석 결과")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("길이", length)
    c2.metric("숫자 수", digit_count)
    c3.metric("대문자 수", upper_count)
    c4.metric("소문자 수", lower_count)

    if repeated:
        st.warning("반복 문자가 발견되었습니다.")

    if sequential:
        st.warning("연속 패턴이 발견되었습니다.")

    if not repeated and not sequential:
        st.success("뚜렷한 인간 편향이 발견되지 않았습니다.")

st.markdown("""
대부분의 사람들은

'랜덤하게 만들었다'

고 생각하지만,

실제로는 반복 문자나 연속 숫자를 사용하는 경우가 많다.
""")

# =====================================================
# SECTION 2
# =====================================================

st.divider()

st.header("2️⃣ 인간은 어떤 특징을 가진 비밀번호를 선호할까?")

threshold = st.slider(
    "Human Bias Score 기준",
    0.0,
    1.0,
    0.5
)

filtered = df[
    df["human_bias_score"] >= threshold
]

st.metric(
    "조건을 만족하는 비밀번호 수",
    f"{len(filtered):,}"
)

fig = px.histogram(
    filtered,
    x="human_bias_score",
    nbins=40,
    title="Human Bias Score 분포"
)

st.plotly_chart(fig, use_container_width=True)

st.success("""
분석 결과

높은 Human Bias Score를 가진 비밀번호가
상당수 존재한다.

이는 사람들이 무작위보다

기억하기 쉬운 패턴,

익숙한 패턴을 선호한다는 것을 의미한다.
""")

# =====================================================
# SECTION 3
# =====================================================

st.divider()

st.header("3️⃣ 사람들은 입력하기 쉬운 비밀번호를 선택할까?")

prediction = st.radio(
    "당신의 예상은?",
    [
        "멀리 이동한다",
        "가까운 키를 선호한다"
    ]
)

show = st.button("결과 확인")

if show:

    fig = px.histogram(
        df,
        x="keyboard_path_length",
        nbins=40,
        title="Keyboard Path Length 분포"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success("""
대부분의 비밀번호는

짧은 키보드 이동거리를 가진다.

즉,

사람들은 입력하기 쉬운 패턴을
선호한다.
""")

# =====================================================
# SECTION 4
# =====================================================

st.divider()

st.header("4️⃣ 미시상태가 모이면 거시상태가 될까?")

sample = df[
    [
        "microstate",
        "macrostate"
    ]
].sample(10)

st.dataframe(sample)

if st.button("공통점 찾아보기"):

    st.info("""
서로 다른 비밀번호라도

동일한 구조를 가지는 경우가 많다.

이것이 Macrostate이다.
""")

    top_macro = (
        df["macrostate"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    top_macro.columns = [
        "Macrostate",
        "Count"
    ]

    fig = px.bar(
        top_macro,
        x="Macrostate",
        y="Count",
        title="가장 많이 등장하는 Macrostate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success("""
분석 결과

수많은 비밀번호가 존재하지만

실제로는 일부 구조에 집중된다.

개인의 선택은 다양하지만

전체적으로는 일정한 구조가 형성된다.
""")

# =====================================================
# SECTION 5
# =====================================================

st.divider()

st.header("5️⃣ 자기조직화 시뮬레이션")

bias = st.slider(
    "인간 편향 강도",
    0,
    100,
    50
)

x = np.arange(10)

distribution = np.exp(
    bias / 20 *
    np.linspace(
        0,
        1,
        10
    )
)

distribution /= distribution.sum()

sim_df = pd.DataFrame(
    {
        "State": x,
        "Probability": distribution
    }
)

fig = px.bar(
    sim_df,
    x="State",
    y="Probability",
    title="편향에 따른 상태 집중"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.success("""
편향이 증가할수록

선택은 일부 상태에 집중된다.

이는 통계역학에서 말하는

자기조직화(Self-Organization)

현상과 유사하다.
""")

# =====================================================
# SECTION 6
# =====================================================

st.divider()

st.header("6️⃣ 지금까지 발견한 사실")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "발견 ①",
    "반복 패턴"
)

c2.metric(
    "발견 ②",
    "입력 편의성"
)

c3.metric(
    "발견 ③",
    "문자 편향"
)

c4.metric(
    "발견 ④",
    "거시상태 형성"
)

st.info("""
이 네 가지 현상은 모두

인간이 완전한 무작위 선택을 하지 않는다는 증거이다.
""")

# =====================================================
# 결론
# =====================================================

st.divider()

st.header("📌 최종 결론")

st.success("""
개인의 비밀번호 선택은 무작위처럼 보인다.

그러나

반복 패턴,

입력 편의성,

기억하기 쉬운 구조와 같은

작은 행동 편향들이 모이면

전체 집단에서는 일정한 구조가 형성된다.

즉,

비밀번호 생성은

수많은 미시적 행동이 모여

거시적 질서를 만들어내는

통계역학적 현상으로 해석할 수 있다.

➡️ 다음 페이지에서는

이러한 행동 편향이 실제 데이터에서
어떤 규칙성으로 나타나는지 검증한다.
""")
