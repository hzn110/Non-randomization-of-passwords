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

AVG_BIAS = 0.159
AVG_ENTROPY = 2.678
AVG_ORDER = 0.716

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("📚 용어 사전")

    with st.expander("엔트로피(Entropy)"):

        st.write("""
        무작위성의 정도를 의미한다.

        높을수록 예측하기 어렵다.
        """)

    with st.expander("질서변수(Order Parameter)"):

        st.write("""
        집단이 특정 상태에 얼마나 집중되는지를 나타낸다.

        0에 가까우면 무질서

        1에 가까우면 질서 상태
        """)

    with st.expander("자기조직화(Self-Organization)"):

        st.write("""
        누가 규칙을 만든 것이 아닌데도

        집단 전체에서 질서가 나타나는 현상
        """)

# ==================================================
# TITLE
# ==================================================

st.title("🔐 인간은 정말 랜덤한 비밀번호를 만들 수 있을까?")

st.markdown("""
### 통계역학적 관점에서 바라본 비밀번호 생성 과정
""")

st.info("""
이 페이지의 목표는

'인간은 랜덤한 비밀번호를 만든다'

라는 가설을 검증하는 것이다.
""")

# ==================================================
# SECTION 1
# ==================================================

st.divider()

st.header("1️⃣ 내 비밀번호는 얼마나 랜덤할까?")

pw = st.text_input(
    "랜덤하다고 생각하는 비밀번호를 입력해보세요"
)

if pw:

    length = len(pw)

    unique_ratio = len(set(pw)) / max(length,1)

    entropy_est = unique_ratio * np.log2(
        max(length,1)
    )

    bias = 0

    if re.search(r"123|234|345|456|789", pw):
        bias += 0.3

    if re.search(r"abc|qwe|asd", pw.lower()):
        bias += 0.3

    if len(set(pw)) < len(pw):
        bias += 0.2

    if re.search(r"19\d\d|20\d\d", pw):
        bias += 0.2

    bias = min(bias,1)

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "예상 편향 점수",
        round(bias,3)
    )

    col2.metric(
        "예상 엔트로피",
        round(entropy_est,3)
    )

    col3.metric(
        "데이터 평균 엔트로피",
        AVG_ENTROPY
    )

    gauge = pd.DataFrame({
        "Category":["당신","평균"],
        "Bias":[bias,AVG_BIAS]
    })

    fig = px.bar(
        gauge,
        x="Category",
        y="Bias",
        title="편향 비교"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if bias > AVG_BIAS:

        st.warning("""
당신의 비밀번호는

평균적인 사용자보다

더 예측 가능할 수 있습니다.
""")

    else:

        st.success("""
평균 사용자보다

상대적으로 랜덤합니다.
""")

# ==================================================
# SECTION 2
# ==================================================

st.divider()

st.header("2️⃣ 작은 편향은 어떤 결과를 만들까?")

bias_strength = st.slider(
    "인간의 편향 강도",
    0,
    100,
    20
)

states = np.arange(20)

weights = np.exp(
    bias_strength/25 *
    np.linspace(0,1,20)
)

weights /= weights.sum()

sim_df = pd.DataFrame({
    "State":states,
    "Probability":weights
})

fig = px.bar(
    sim_df,
    x="State",
    y="Probability",
    title="상태 분포"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown(f"""
편향 강도 : **{bias_strength}%**

편향이 커질수록

특정 상태가 선택될 확률이 높아진다.
""")

# ==================================================
# SECTION 3
# ==================================================

st.divider()

st.header("3️⃣ 사람이 많아지면 무슨 일이 일어날까?")

population = st.slider(
    "비밀번호를 만드는 사람 수",
    1,
    100000,
    1000,
    step=1000
)

samples = np.random.choice(
    states,
    size=population,
    p=weights
)

freq = pd.Series(samples).value_counts()

concentration = freq.max()/population

fig = px.histogram(
    x=samples,
    nbins=20,
    title="집단 선택 결과"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.metric(
    "집중도",
    round(concentration,3)
)

st.info("""
한 사람은 랜덤하게 선택할 수 있다.

하지만 사람이 많아질수록

특정 상태에 선택이 집중된다.
""")

# ==================================================
# SECTION 4
# ==================================================

st.divider()

st.header("4️⃣ 질서변수(Order Parameter)를 관찰해보자")

order = concentration

fig = px.bar(
    x=["현재 시뮬레이션","실제 데이터"],
    y=[order,AVG_ORDER],
    labels={"x":"비교","y":"Order Parameter"}
)

st.plotly_chart(
    fig,
    use_container_width=True
)

if order > 0.5:

    st.success("""
질서 상태가 형성되었다.

집단은 더 이상 랜덤하지 않다.
""")

else:

    st.warning("""
아직 무질서 상태에 가깝다.
""")

# ==================================================
# SECTION 5
# ==================================================

st.divider()

st.header("5️⃣ 우리는 무엇을 발견했을까?")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "발견①",
    "편향 존재"
)

c2.metric(
    "발견②",
    "상태 집중"
)

c3.metric(
    "발견③",
    "질서 형성"
)

c4.metric(
    "발견④",
    "자기조직화"
)

# ==================================================
# CONCLUSION
# ==================================================

st.divider()

st.header("📌 결론")

st.success(f"""
실제 데이터의 평균 질서변수는

{AVG_ORDER}

이다.

이는 사람들의 비밀번호가

완전히 랜덤하게 생성되지 않는다는 의미이다.

개인의 작은 편향은

집단 수준에서 증폭되고,

결국 특정 구조가 반복적으로 선택된다.

즉,

비밀번호 생성은

통계역학에서 말하는

자기조직화(Self-Organization)의 한 예로 볼 수 있다.

➡ 다음 페이지에서는

실제 데이터에서 어떤 규칙성이 발견되는지 검증한다.
""")
