import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter

# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="인간의 비밀번호에는 규칙성이 존재하는가?",
    page_icon="🔍",
    layout="wide"
)

# =====================================================
# 홈 버튼
# =====================================================

# =====================================================
# 데이터 로드
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "rockyou_rigorous_behavioral_physics_v2 (1).csv"
    )

df = load_data()

# =====================================================
# 제목
# =====================================================

st.title("🔍 인간의 비밀번호에는 정말 규칙성이 존재하는가?")

st.markdown("""
### 당신이 공격자라면 비밀번호를 예측할 수 있을까?
""")

st.info("""
페이지1에서는

인간이 특정 방향으로 비밀번호를 선택한다는 사실을 발견했다.

이번에는

실제 데이터가

정말 예측 가능한 패턴을 가지는지 검증해보자.
""")

# =====================================================
# SECTION 1
# =====================================================

st.divider()

st.header("1️⃣ 당신은 해커가 될 수 있을까?")

answer = st.radio(
    "가장 보안이 취약할것 같은 비밀번호를 선택하세요.",
    [
        "password123",
        "T7@zK91!",
        "xM#4L!qp"
    ]
)

if st.button("정답 확인"):

    if answer == "password123":

        st.success("""
정답!

실제 데이터에속에서

사람들은 기억하기 쉬운 패턴을
압도적으로 많이 사용합니다!
""")

    else:

        st.error("""
실제 사용자는 생각보다 훨씬 단순한
비밀번호를 사용합니다.
""")

# =====================================================
# SECTION 2
# =====================================================

st.divider()

st.header("2️⃣ 사람들은 정말 비슷한 구조를 사용할까?")

sample = df[
    [
        "microstate",
        "macrostate"
    ]
].sample(15)

st.dataframe(sample)

if st.button("공통점 찾기"):

    st.info("""
서로 다른 비밀번호인데도

비슷한 구조가 반복된다.
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
        title="가장 많이 사용되는 구조"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success("""
결론

인간은 매우 다양한 비밀번호를 만드는 것 같지만

실제로는 일부 구조를 반복적으로 사용한다.
""")

# =====================================================
# SECTION 3
# =====================================================

st.divider()

st.header("3️⃣ 비밀번호에도 인기 순위가 존재할까?")

top_pw = (
    df["microstate"]
    .value_counts()
    .head(10)
)

cols = st.columns(5)

for i, (pw, count) in enumerate(top_pw.items()):

    cols[i % 5].metric(
        f"{i+1}위",
        pw
    )

st.markdown("### 순위와 빈도의 관계")

zipf_df = (
    df["microstate"]
    .value_counts()
    .reset_index()
)

zipf_df.columns = [
    "password",
    "count"
]

zipf_df["rank"] = np.arange(
    1,
    len(zipf_df)+1
)

fig = px.scatter(
    zipf_df,
    x="rank",
    y="count",
    log_x=True,
    log_y=True,
    title="Zipf Law"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.success("""
소수의 비밀번호가

엄청난 비율을 차지한다.

이를 Zipf 법칙이라고 한다.
""")

# =====================================================
# SECTION 4
# =====================================================

st.divider()

st.header("4️⃣ 사람들은 어떤 문자 조합을 좋아할까?")

guess = st.radio(
    "가장 많이 등장할 것 같은 문자 조합은?",
    [
        "pa",
        "zx",
        "kr",
        "jq"
    ]
)

if st.button("Bigram 결과 보기"):

    st.success("""
정답은 pa 이다.

password

pass123

password1

등의 영향 때문이다.
""")

    counter = Counter()

    for item in df["bigram_sequence"].dropna():

        pairs = str(item).split("|")

        counter.update(pairs)

    top_bigram = pd.DataFrame(
        counter.most_common(15),
        columns=[
            "Bigram",
            "Count"
        ]
    )

    fig = px.bar(
        top_bigram,
        x="Bigram",
        y="Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# SECTION 5
# =====================================================

st.divider()

st.header("5️⃣ 완전히 랜덤한 세계와 비교해보자")

randomness = st.slider(
    "랜덤성",
    0,
    100,
    50
)

sim = np.random.normal(
    50,
    max(3, randomness/5),
    1000
)

fig = px.histogram(
    x=sim,
    nbins=30,
    title="가상의 랜덤 세계"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("### 실제 데이터")

fig2 = px.histogram(
    df,
    x="shannon_entropy",
    nbins=40
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.success("""
실제 비밀번호는

완전한 랜덤 분포와 상당히 다르다.
""")

# =====================================================
# SECTION 6
# =====================================================

st.divider()

st.header("6️⃣ 상태공간의 함정")

possible = st.slider(
    "가능한 비밀번호 수",
    100,
    1000000,
    100000,
    step=100
)

used = int(
    np.log10(possible) * 15
)

col1,col2 = st.columns(2)

col1.metric(
    "가능한 상태",
    f"{possible:,}"
)

col2.metric(
    "실제 집중 상태",
    f"{used:,}"
)

st.warning("""
가능한 조합은 엄청나게 많다.

하지만 사람들은 극히 일부 영역만 반복적으로 사용한다.
""")

# =====================================================
# SECTION 7
# =====================================================

st.divider()

st.header("7️⃣ 실제 공격 시뮬레이션")

if st.button("공격 시작"):

    progress = st.progress(0)

    candidates = [
        "123456",
        "password",
        "qwerty",
        "welcome",
        "admin",
        "password123"
    ]

    for i, pw in enumerate(candidates):

        progress.progress(
            (i+1)/len(candidates)
        )

        st.write(
            f"시도 중 : {pw}"
        )

    st.success("""
공격 성공

해커는 가능한 모든 비밀번호를 시도하지 않는다.

인간이 자주 사용할 비밀번호부터 시도한다.
""")

# =====================================================
# 결론
# =====================================================

st.divider()

st.header("📌 최종 결론")

st.success("""
사람은 랜덤하다고 생각하며 비밀번호를 만든다.

그러나 실제 데이터는

• 반복되는 구조

• 반복되는 문자 조합

• 반복되는 길이

• 반복되는 인기 비밀번호

를 보여준다.

즉,

해커는 모든 비밀번호를 시도하지 않는다.

인간이 가장 먼저 선택할 것 같은 비밀번호부터 시도한다.

그리고 그것이 실제로 매우 잘 통한다.

➡️ 다음 페이지에서는

이러한 규칙성이 왜 보안상 위험한지 알아본다.
""")
