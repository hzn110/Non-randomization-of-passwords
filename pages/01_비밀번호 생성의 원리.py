# ==================================================
# SECTION 1
# ==================================================

st.divider()

st.header("1️⃣ 내 비밀번호는 얼마나 랜덤할까?")

st.markdown("""
<div style="
background:rgba(255,255,255,0.08);
padding:25px;
border-radius:20px;
margin-bottom:20px;
">

<h4 style="margin-top:0;">
🔍 비밀번호 실험실
</h4>

비밀번호를 입력하면

<ul>
<li>실제 사용자 데이터와 비교</li>
<li>구조(Macrostate) 분석</li>
<li>인간적 편향 탐지</li>
<li>예측 가능성 평가</li>
</ul>

</div>
""", unsafe_allow_html=True)

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

    st.subheader("예측 가능성")

    score = min(
        entropy / 4.5,
        1.0
    )

    st.progress(score)

    if score < 0.4:

        st.error("예측하기 쉬운 비밀번호")

    elif score < 0.7:

        st.warning("평균 수준의 비밀번호")

    else:

        st.success("상대적으로 예측하기 어려운 비밀번호")

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
            "길이",
            len(pw)
        )

    st.markdown(
        f"""
        <div style="
        background:rgba(255,255,255,0.08);
        padding:20px;
        border-radius:15px;
        margin-top:20px;
        ">

        <h4>구조 분석 결과</h4>

        <b>{pw}</b>

        <br><br>

        ↓

        <br><br>

        <b style="font-size:20px;">
        {macro}
        </b>

        </div>
        """,
        unsafe_allow_html=True
    )

    if macro_count > 0:

        st.warning(
            f"""
            이 데이터셋에는

            **{macro_count:,}개**

            의 비밀번호가

            당신과 동일한 구조를 사용한다.
            """
        )

    similar = df[
        df["macrostate"] == macro
    ].head(5)

    if len(similar) > 0:

        st.subheader(
            "같은 구조를 가진 실제 비밀번호 예시"
        )

        for example in similar["microstate"]:

            st.markdown(
                f"""
                <div style="
                background:rgba(255,255,255,0.05);
                padding:12px;
                margin-bottom:8px;
                border-radius:10px;
                ">
                {example}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    st.markdown(
        f"""
### 분석 결과

당신의 비밀번호 구조는 **{macro}** 이다.

실제 데이터에서는 동일한 구조가
**{macro_count:,}번** 등장한다.

즉 비밀번호 내용은 달라도

사람들은 비슷한 방식으로 비밀번호를 만드는 경향이 있다.
"""
    )
