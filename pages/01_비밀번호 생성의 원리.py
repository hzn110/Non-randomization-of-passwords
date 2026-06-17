import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="인간은 정말 랜덤한 비밀번호를 만들 수 있을까?",
    page_icon="🔐",
    layout="wide"
)

# ==================================================
# DATA
# ==================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "rockyou_rigorous_behavioral_physics_v2 (1).csv"
    )

df = load_data()

AVG_BIAS = 0.1586
AVG_ORDER = 0.7163
AVG_ENTROPY = 2.6778

# ==================================================
# FUNCTIONS
# ==================================================

def password_to_macrostate(password):

    result = ""

    for c in password:

        if c.isupper():
            result += "L"

        elif c.islower():
            result += "l"

        elif c.isdigit():
            result += "d"

        else:
            result += "s"

    return result


def estimate_bias(password):

    score = 0

    if re.search(r"123|234|345|456|567|678|789", password):
        score += 0.4

    if re.search(r"qwe|asd|zxc|abc", password.lower()):
        score += 0.3

    if re.search(r"19\d\d|20\d\d", password):
        score += 0.2

    if len(set(password)) < len(password):
        score += 0.1

    return round(min(score, 1), 3)


def estimate_entropy(password):

    if len(password) == 0:
        return 0

    return round(
        len(set(password)) / len(password)
        * np.log2(len(password)),
        3
    )

# ==================================================
# TITLE
# ==================================================

st.title("🔐 인간은 정말 랜덤한 비밀번호를 만들 수 있을까?")

st.caption(
    "RockYou 데이터 10,000개를 이용한 통계역학 실험"
)

# ==================================================
# SECTION 1
# ==================================================

st.divider()

st.header("1️⃣ 당신의 비밀번호를 실험해보자")

pw = st.text_input(
    "",
    placeholder="예: Football123!"
)

st.caption(
    "입력 즉시 실제 사용자 데이터와 비교됩니다."
)

if pw:

    macro = password_to_macrostate(pw)

    bias = estimate_bias(pw)

    entropy = estimate_entropy(pw)

    macro_count = (
        df["macrostate"] == macro
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "편향 점수",
            bias
        )

    with col2:
        st.metric(
            "엔트로피",
            entropy
        )

    with col3:
        st.metric(
            "동일 구조 수",
            f"{macro_count:,}"
        )

    with col4:
        st.metric(
            "구조",
            macro[:10]
        )

    st.markdown(
        f"""
        ### 구조 해석

        **{pw}**

        ↓

        **{macro}**
        """
    )

    if macro_count > 0:

        st.warning(
            f"""
            당신은 새로운 비밀번호를 만들었다고 생각할 수 있습니다.

            하지만 이 데이터에는

            **{macro_count:,}개**

            의 비밀번호가 같은 구조를 사용합니다.
            """
        )

    similar = df[
        df["macrostate"] == macro
    ].head(10)

    if len(similar) > 0:

        st.subheader(
            "같은 구조를 가진 실제 비밀번호 예시"
        )

        st.dataframe(
            similar[
                [
                    "microstate",
                    "shannon_entropy"
                ]
            ],
            use_container_width=True
        )

# ==================================================
# SECTION 2
# ==================================================

st.divider()

st.header("2️⃣ 나는 평균적인 사용자와 얼마나 비슷할까?")

fig = px.histogram(
    df,
    x="human_bias_score",
    nbins=40,
    title="인간 행동 편향 점수 분포"
)

if pw:

    fig.add_vline(
        x=bias,
        line_color="red",
        line_width=4
    )

fig.add_vline(
    x=AVG_BIAS,
    line_dash="dash"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown(f"""
빨간선은 당신의 위치,

점선은 실제 사용자 평균이다.

실제 데이터의 평균 편향 점수는

**{AVG_BIAS:.3f}**

이다.
""")

# ==================================================
# SECTION 3
# ==================================================

st.divider()

st.header("3️⃣ 사람들은 정말 서로 다른 비밀번호를 만들까?")

macro_freq = (
    df["macrostate"]
    .value_counts()
    .head(10)
    .reset_index()
)

macro_freq.columns = [
    "macrostate",
    "count"
]

fig = px.bar(
    macro_freq,
    x="macrostate",
    y="count",
    title="가장 많이 등장한 비밀번호 구조"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("""
비밀번호 내용은 모두 다르다.

그러나 구조만 남기면

소수의 형태에 강하게 집중된다.

즉,

사람들은 다른 단어를 사용하면서도

비슷한 방식으로 비밀번호를 만든다.
""")

# ==================================================
# SECTION 4
# ==================================================

st.divider()

st.header("4️⃣ 작은 편향은 어떻게 큰 질서를 만드는가?")

comparison = pd.DataFrame({

    "항목": [
        "평균 편향",
        "평균 질서변수"
    ],

    "값": [
        AVG_BIAS,
        AVG_ORDER
    ]
})

fig = px.bar(
    comparison,
    x="항목",
    y="값",
    title="개인 편향과 집단 질서 비교"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown(f"""
개인의 평균 편향은

**{AVG_BIAS:.3f}**

수준이다.

하지만 집단 수준에서 측정한 질서변수는

**{AVG_ORDER:.3f}**

이다.

작은 행동 차이가 모이면

거대한 구조적 패턴이 형성된다.
""")

# ==================================================
# SECTION 5
# ==================================================

st.divider()

st.header("5️⃣ 실제 데이터는 랜덤 생성과 다를까?")

sample_size = st.slider(
    "랜덤 비밀번호 생성 수",
    100,
    10000,
    2000,
    step=100
)

random_entropy = np.random.normal(
    3.4,
    0.25,
    sample_size
)

real_entropy = df["shannon_entropy"]

compare_df = pd.DataFrame({

    "Entropy": np.concatenate([
        real_entropy,
        random_entropy
    ]),

    "Group":
    ["실제 사용자"] * len(real_entropy)
    +
    ["랜덤 생성"] * len(random_entropy)
})

fig = px.box(
    compare_df,
    x="Group",
    y="Entropy",
    title="실제 비밀번호 vs 랜덤 생성"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("""
만약 인간이 정말 랜덤하게 비밀번호를 만든다면

두 분포는 비슷해야 한다.

그러나 실제 데이터는

특정 구조에 반복적으로 집중되는 경향을 보인다.
""")

# ==================================================
# CONCLUSION
# ==================================================

st.divider()

st.header("📌 결론")

st.success("""
① 사람들은 서로 다른 비밀번호를 만든다고 생각한다.

② 하지만 구조(Macrostate)는 매우 비슷하다.

③ 개인의 편향은 작다.

④ 그러나 집단 수준에서는 강한 질서가 형성된다.

즉,

비밀번호는 무작위 문자열이 아니라

인간 행동이 남긴 흔적이다.

다음 페이지에서는

실제 데이터에서 나타나는 규칙성을 검증한다.
""")
