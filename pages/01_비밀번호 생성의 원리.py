```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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

    return round(min(score,1),3)


def estimate_entropy(password):

    if len(password) == 0:
        return 0

    return round(
        len(set(password))/len(password)
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

st.header("1️⃣ 내 비밀번호는 얼마나 특별할까?")

pw = st.text_input(
    "랜덤하다고 생각하는 비밀번호를 입력해보세요",
    placeholder="예: Football123!"
)

if pw:

    macro = password_to_macrostate(pw)

    bias = estimate_bias(pw)

    entropy = estimate_entropy(pw)

    macro_count = (
        df["macrostate"] == macro
    ).sum()

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric(
            "예상 편향 점수",
            bias
        )

    with col2:
        st.metric(
            "예상 엔트로피",
            entropy
        )

    with col3:
        st.metric(
            "같은 구조 사용 수",
            f"{macro_count:,}"
        )

    st.markdown("### 비밀번호 구조(Macrostate)")

    st.code(macro)

    if macro_count > 0:

        st.warning(
            f"""
            당신은 새로운 비밀번호를 만들었다고
            생각했을 수 있습니다.

            하지만 이 데이터에서는

            **{macro_count}개**

            의 비밀번호가 같은 구조를 사용합니다.
            """
        )

    else:

        st.success(
            """
            데이터 내에서는
            거의 등장하지 않는 구조입니다.
            """
        )

# ==================================================
# SECTION 2
# ==================================================

st.divider()

st.header("2️⃣ 나는 평균적인 사람과 얼마나 비슷할까?")

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
        line_width=3
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
실제 데이터의 평균 편향 점수는

**{AVG_BIAS:.3f}**

이다.

흥미로운 점은

대부분의 사용자가 매우 높은 편향을 보이지 않는데도

집단 전체에서는 강한 질서가 나타난다는 점이다.
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

fig = px.pie(
    macro_freq,
    values="count",
    names="macrostate",
    hole=0.55,
    title="가장 많이 등장한 비밀번호 구조"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("""
비밀번호 내용은 모두 다르다.

하지만 구조만 남기고 보면

놀라울 정도로 일부 형태에 집중된다.

즉,

사람들은 다른 단어를 사용하면서도

비슷한 방식으로 비밀번호를 만든다.
""")

# ==================================================
# SECTION 4
# ==================================================

st.divider()

st.header("4️⃣ 작은 편향은 어떻게 큰 질서를 만드는가?")

col1,col2 = st.columns(2)

with col1:

    st.metric(
        "평균 편향",
        round(AVG_BIAS,3)
    )

with col2:

    st.metric(
        "평균 질서변수",
        round(AVG_ORDER,3)
    )

comparison = pd.DataFrame({

    "항목":[
        "평균 편향",
        "평균 질서"
    ],

    "값":[
        AVG_BIAS,
        AVG_ORDER
    ]
})

fig = px.bar(
    comparison,
    x="항목",
    y="값",
    title="작은 편향 vs 큰 질서"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("""
흥미롭게도

개인의 편향은 평균 0.159 수준으로 크지 않다.

하지만 집단 수준에서 측정한 질서변수는

0.716으로 매우 높다.

즉,

작은 행동 차이가 모이면

거대한 구조적 패턴이 형성된다.
""")

# ==================================================
# SECTION 5
# ==================================================

st.divider()

st.header("5️⃣ 랜덤한 세계와 비교해보자")

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

real_entropy = df[
    "shannon_entropy"
]

compare_df = pd.DataFrame({

    "Entropy": np.concatenate([
        real_entropy,
        random_entropy
    ]),

    "Group":
    ["실제 사용자"]*len(real_entropy)
    +
    ["랜덤 생성"]*len(random_entropy)
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

실제 데이터는 랜덤 생성 데이터와 비슷해야 한다.

하지만 실제 비밀번호는

특정 구조에 반복적으로 집중되는 경향을 보인다.
""")

# ==================================================
# CONCLUSION
# ==================================================

st.divider()

st.header("📌 우리는 무엇을 발견했을까?")

st.success("""
① 사람들은 서로 다른 비밀번호를 만든다고 생각한다.

② 하지만 구조(Macrostate)는 매우 비슷하다.

③ 개인의 편향은 작지만

④ 집단 전체에서는 강한 질서가 형성된다.

즉,

비밀번호는 무작위 문자열이 아니라

인간 행동이 남긴 흔적이라고 볼 수 있다.

다음 페이지에서는

실제 데이터에서 나타나는 규칙성을 더욱 자세히 분석한다.
""")
```
