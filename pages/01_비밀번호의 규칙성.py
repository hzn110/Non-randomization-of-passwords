import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="인간의 비밀번호에는 규칙성이 존재하는가?",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# 홈 버튼
# =====================================================

if st.button("🏠 메인 화면으로 이동"):
    st.switch_page("Home.py")

# =====================================================
# 데이터 로드
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("rockyou_rigorous_behavioral_physics_v2 (1).csv")

df = load_data()

# =====================================================
# 제목
# =====================================================

st.title("📊 인간의 비밀번호에는 규칙성이 존재하는가?")

st.markdown("""
### 페이지 1에서 발견한 인간 행동 편향은 실제 비밀번호에서도 나타날까?
""")

st.info("""
페이지 1에서는

• 인간 행동 편향

• 입력 편의성

• 구조 선호

가 존재함을 확인하였다.

이 페이지에서는 실제 데이터를 이용하여

인간의 비밀번호가 정말 특정 패턴으로 집중되는지 검증한다.
""")

# =====================================================
# SECTION 1
# =====================================================

st.divider()

st.header("1️⃣ 가장 많이 사용되는 비밀번호 구조")

top_macro = (
    df["macrostate"]
    .value_counts()
    .head(20)
    .reset_index()
)

top_macro.columns = ["Macrostate", "Count"]

fig = px.bar(
    top_macro,
    x="Macrostate",
    y="Count",
    title="가장 많이 사용되는 Macrostate"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
수많은 비밀번호가 존재하지만

실제로는 몇 개의 구조에 사용자가 집중되는 현상이 나타난다.

이는 페이지 1에서 설명한 행동 편향이
실제 데이터에서도 관찰된다는 의미이다.
""")

with st.expander("💡 Macrostate란?"):
    st.info("""
    Macrostate는 비밀번호의 구조만 남긴 형태이다.

    예)

    Password123!

    ↓

    Llllllllddds

    서로 다른 비밀번호도
    같은 구조를 공유할 수 있다.
    """)

# =====================================================
# SECTION 2
# =====================================================

st.divider()

st.header("2️⃣ 문자 전이(Bigram) 분석")

def extract_bigrams(series):

    counter = Counter()

    for item in series.dropna():

        pairs = str(item).split("|")

        counter.update(pairs)

    return counter

bigram_counter = extract_bigrams(df["bigram_sequence"])

top_bigram = pd.DataFrame(
    bigram_counter.most_common(20),
    columns=["Bigram", "Count"]
)

fig = px.bar(
    top_bigram,
    x="Bigram",
    y="Count",
    title="가장 많이 등장하는 문자 전이(Bigram)"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
완전히 랜덤한 비밀번호라면

모든 문자 조합이 비슷한 비율로 등장해야 한다.

그러나 실제 데이터에서는

특정 문자 전이가 반복적으로 등장한다.

이는 인간이 특정 문자 패턴을
선호한다는 증거가 된다.
""")

with st.expander("💡 Bigram이란?"):
    st.info("""
    Bigram은 서로 인접한 두 글자의 조합이다.

    예)

    password

    →

    pa
    as
    ss
    sw
    wo
    or
    rd

    와 같이 분석할 수 있다.
    """)

# =====================================================
# SECTION 3
# =====================================================

st.divider()

st.header("3️⃣ Zipf 법칙 검증")

zipf_df = df[
    [
        "guessability_rank",
        "password_popularity"
    ]
].dropna()

fig = px.scatter(
    zipf_df,
    x="guessability_rank",
    y="password_popularity",
    log_x=True,
    log_y=True,
    title="Rank vs Popularity (Zipf Law)"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
상위 몇 개의 비밀번호가
매우 높은 빈도를 차지한다.

이 현상은 언어 빈도나
도시 규모 분포에서도 나타나는
Zipf 법칙과 유사하다.

즉,

비밀번호 역시 무작위가 아니라
집중된 분포를 가진다.
""")

with st.expander("💡 Zipf 법칙이란?"):
    st.info("""
    Zipf 법칙은

    가장 많이 사용되는 대상이
    압도적으로 많이 등장하고

    순위가 내려갈수록
    빈도가 급격히 감소하는 현상이다.

    언어, 경제, 인터넷 데이터 등에서
    자주 발견된다.
    """)

# =====================================================
# SECTION 4
# =====================================================

st.divider()

st.header("4️⃣ 인간은 정말 랜덤하게 비밀번호를 만드는가?")

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        df,
        x="shannon_entropy",
        nbins=40,
        title="Shannon Entropy 분포"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.histogram(
        df,
        x="macrostate_surprisal",
        nbins=40,
        title="Macrostate Surprisal 분포"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
엔트로피는

비밀번호가 얼마나 예측하기 어려운지를 나타낸다.

만약 인간이 완전히 랜덤하게 비밀번호를 만들었다면

값이 넓게 퍼져야 한다.

하지만 실제 데이터에서는

특정 영역에 집중되는 경향이 나타난다.

이는 많은 사람들이
유사한 구조를 반복적으로 사용한다는 의미이다.
""")

with st.expander("💡 엔트로피란?"):
    st.info("""
    엔트로피는

    얼마나 다양하고 예측하기 어려운지를 나타내는 지표이다.

    높을수록 예측하기 어렵고

    낮을수록 특정 패턴에 집중되어 있다.
    """)

# =====================================================
# SECTION 5
# =====================================================

st.divider()

st.header("5️⃣ 가능한 비밀번호는 많은데 왜 비슷할까?")

fig = px.histogram(
    df,
    x="empirical_state_density",
    nbins=50,
    title="Empirical State Density"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
길이 8~12자리 비밀번호만 생각해도

이론적으로 가능한 조합은
수조 개 이상 존재한다.

하지만 실제 데이터에서는

극히 일부 구조만 반복적으로 사용된다.

즉,

가능한 상태 공간은 매우 넓지만

실제 사용 공간은 매우 좁다.
""")

with st.expander("💡 상태 밀도(State Density)란?"):
    st.info("""
    상태 밀도는

    가능한 모든 상태 중

    실제로 얼마나 많은 상태가
    사용되고 있는지를 나타낸다.

    통계역학에서는

    입자가 특정 상태에 몰리는 현상을
    설명할 때 사용된다.
    """)

# =====================================================
# SECTION 6
# =====================================================

st.divider()

st.header("6️⃣ 비밀번호 길이 분포")

fig = px.histogram(
    df,
    x="length",
    nbins=30,
    title="비밀번호 길이 분포"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
완전한 랜덤이라면

길이도 매우 다양하게 분포해야 한다.

하지만 실제로는

특정 길이 구간에 집중되는 경향이 나타난다.

이는 기억하기 쉽고
입력하기 쉬운 길이를 선호하기 때문이다.
""")

# =====================================================
# SECTION 7
# =====================================================

st.divider()

st.header("7️⃣ 실제 데이터 관찰")

sample_size = st.slider(
    "확인할 샘플 개수",
    5,
    50,
    10
)

sample_df = df[
    [
        "microstate",
        "length",
        "macrostate",
        "human_bias_score"
    ]
].sample(sample_size)

st.dataframe(
    sample_df,
    use_container_width=True
)

st.markdown("""
직접 데이터를 살펴보면

서로 다른 비밀번호라도

비슷한 길이,

비슷한 구조,

비슷한 행동 편향 점수

를 가지는 경우가 많다는 것을 확인할 수 있다.
""")

# =====================================================
# 결론
# =====================================================

st.divider()

st.header("📌 결론")

st.success("""
페이지 1에서는

인간이 특정 방향으로 비밀번호를 선택한다는 사실을 확인하였다.

페이지 2에서는 실제 데이터를 분석하여

• 특정 구조(Macrostate)

• 특정 문자 전이(Bigram)

• 특정 길이

• 특정 엔트로피 범위

• 특정 인기 비밀번호

가 반복적으로 등장함을 확인하였다.

즉,

인간의 비밀번호는 완전히 랜덤하지 않으며

강한 규칙성과 보편성을 가진다는 사실을
데이터를 통해 검증할 수 있었다.

➡️ 다음 페이지에서는

이러한 규칙성이 왜 정보보안에 위험한지
살펴본다.
""")
