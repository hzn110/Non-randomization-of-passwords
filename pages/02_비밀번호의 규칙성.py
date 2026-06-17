import streamlit as stimport pandas as pdimport numpy as npimport plotly.express as pximport plotly.graph_objects as goimport reimport os

st.set_page_config(page_title="인간은 어떻게 비밀번호를 만드는가?",page_icon="📊",layout="wide",initial_sidebar_state="expanded")

======================

다크/라이트 모드 상태 (메인과 공유)

======================

if "dark_mode" not in st.session_state:st.session_state.dark_mode = True

dark = st.session_state.dark_mode

======================

다크/라이트 CSS 변수 (메인과 동일)

======================

if dark:bg_main   = "radial-gradient(circle at 20% 25%, rgba(160,130,255,0.22) 0%, transparent 50%), radial-gradient(circle at 80% 12%, rgba(220,130,255,0.18) 0%, transparent 50%), radial-gradient(circle at 50% 88%, rgba(100,170,255,0.16) 0%, transparent 55%), linear-gradient(160deg, rgba(18,14,48,0.92) 0%, rgba(22,14,52,0.88) 50%, rgba(16,12,42,0.92) 100%)"glass_bg  = "linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(200,180,255,0.03) 100%)"glass_hov = "linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(200,180,255,0.07) 100%)"border    = "rgba(200,180,255,0.15)"border_hov= "rgba(220,200,255,0.32)"text_main = "rgba(255,255,255,0.95)"text_sub  = "rgba(220,210,255,0.60)"text_hint = "rgba(180,170,255,0.35)"badge_bg  = "rgba(200,180,255,0.07)"shadow    = "rgba(60,30,120,0.18)"shadow_hov= "rgba(80,40,160,0.28)"sidebar_bg= "rgba(18,12,45,0.50)"sidebar_br= "rgba(200,180,255,0.10)"title_grad= "linear-gradient(135deg,#e8e0ff 0%,#c4b5ff 50%,#f9c6ff 100%)"num_grad  = "linear-gradient(135deg,#ffffff 0%,#c4b5ff 100%)"chart_bg  = "rgba(0,0,0,0)"chart_paper = "rgba(0,0,0,0)"chart_font  = "rgba(220,210,255,0.80)"bar_color   = "#a78bfa"bar_color2  = "#f9a8d4"else:bg_main   = "radial-gradient(circle at 15% 20%, rgba(100,140,255,0.12) 0%, transparent 45%), radial-gradient(circle at 85% 15%, rgba(255,100,180,0.10) 0%, transparent 45%), radial-gradient(circle at 50% 90%, rgba(80,220,180,0.10) 0%, transparent 50%), linear-gradient(160deg,#f0f2ff 0%,#faf5ff 50%,#f0f8ff 100%)"glass_bg  = "linear-gradient(135deg, rgba(255,255,255,0.72) 0%, rgba(255,255,255,0.45) 100%)"glass_hov = "linear-gradient(135deg, rgba(255,255,255,0.90) 0%, rgba(255,255,255,0.65) 100%)"border    = "rgba(120,120,180,0.18)"border_hov= "rgba(100,100,220,0.38)"text_main = "rgba(30,30,60,0.95)"text_sub  = "rgba(60,60,100,0.65)"text_hint = "rgba(100,100,160,0.55)"badge_bg  = "rgba(100,100,220,0.09)"shadow    = "rgba(100,100,200,0.10)"shadow_hov= "rgba(100,100,200,0.22)"sidebar_bg= "rgba(255,255,255,0.55)"sidebar_br= "rgba(180,180,220,0.20)"title_grad= "linear-gradient(135deg,#3b3bb0 0%,#7c3aed 50%,#db2777 100%)"num_grad  = "linear-gradient(135deg,#3b3bb0 0%,#6366f1 100%)"chart_bg  = "rgba(0,0,0,0)"chart_paper = "rgba(0,0,0,0)"chart_font  = "rgba(60,60,100,0.80)"bar_color   = "#7c3aed"bar_color2  = "#db2777"

st.markdown(f"""

""", unsafe_allow_html=True)

======================

사이드바 — 모드 토글 + 용어 사전

======================

with st.sidebar:label = "☀️ 라이트 모드" if dark else "🌙 다크 모드"if st.button(label, key="mode_toggle", use_container_width=True):st.session_state.dark_mode = not st.session_state.dark_modest.rerun()st.divider()st.markdown(f"📚 용어 사전")with st.expander("미시상태 (Microstate)"):st.write("비밀번호 하나하나를 개별 미시상태로 본다.\n\n예) abc123, qwerty, password")with st.expander("거시상태 (Macrostate)"):st.write("문자 구조만 남긴 형태.\n\nPassword123! → Ulllllllddds\n\n같은 구조를 가진 비밀번호는 같은 거시상태.")with st.expander("엔트로피 (Entropy)"):st.write("얼마나 다양하고 예측하기 어려운지를 나타낸다.\n\n높을수록 무작위, 낮을수록 특정 패턴에 집중.")with st.expander("질서변수 (Order Parameter)"):st.write("특정 상태에 얼마나 집중되어 있는지.\n\n0 = 완전 무질서, 1 = 완전 질서")with st.expander("자기조직화 (Self-Organization)"):st.write("누가 규칙을 만든 것이 아닌데도\n\n집단 전체에서 자연스럽게 질서가 나타나는 현상.")

======================

데이터 로드

======================

@st.cache_datadef load_data():base_dir = os.path.dirname(os.path.dirname(os.path.abspath(file)))path = os.path.join(base_dir, "rockyou_rigorous_behavioral_physics_v2.csv")return pd.read_csv(path)

try:df = load_data()DATA_OK = Trueexcept Exception:df = NoneDATA_OK = False

AVG_BIAS    = 0.159AVG_ENTROPY = 2.678AVG_ORDER   = 0.716

def apply_chart_theme(fig):fig.update_layout(paper_bgcolor=chart_paper,plot_bgcolor=chart_bg,font_color=chart_font,font_family="-apple-system, BlinkMacSystemFont, sans-serif",margin=dict(t=40, b=20, l=10, r=10),)fig.update_xaxes(gridcolor=border, zerolinecolor=border)fig.update_yaxes(gridcolor=border, zerolinecolor=border)return fig

======================

Hero

======================

st.markdown(f"""

탐구 질문

st.markdown(f"""

======================

SECTION 1 — 내 비밀번호는 얼마나 랜덤할까?

======================

st.markdown(f'1️⃣ 내 비밀번호는 얼마나 랜덤할까?', unsafe_allow_html=True)

st.markdown(f"""

pw = st.text_input("랜덤하다고 생각하는 비밀번호를 입력해보세요", placeholder="예: Tr0ub4dor&3")

if pw:length = len(pw)unique_ratio = len(set(pw)) / max(length, 1)entropy_est = unique_ratio * np.log2(max(length, 1))

bias = 0
if re.search(r"123|234|345|456|789", pw): bias += 0.3
if re.search(r"abc|qwe|asd", pw.lower()): bias += 0.3
if len(set(pw)) < len(pw): bias += 0.2
if re.search(r"19\d\d|20\d\d", pw): bias += 0.2
bias = min(bias, 1)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="glass stat-row">
        <div class="big-number">{round(bias, 3)}</div>
        <div class="big-label">예상 편향 점수</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="glass stat-row">
        <div class="big-number">{round(entropy_est, 3)}</div>
        <div class="big-label">예상 엔트로피</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="glass stat-row">
        <div class="big-number">{AVG_ENTROPY}</div>
        <div class="big-label">데이터 평균 엔트로피</div>
    </div>""", unsafe_allow_html=True)

gauge_df = pd.DataFrame({"카테고리": ["내 비밀번호", "평균"], "편향 점수": [bias, AVG_BIAS]})
fig = px.bar(gauge_df, x="카테고리", y="편향 점수", color="카테고리",
             color_discrete_sequence=[bar_color, bar_color2], title="편향 점수 비교")
fig = apply_chart_theme(fig)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

if bias > AVG_BIAS:
    st.markdown(f"""<div class="glass" style="border-color:rgba(255,120,120,0.30);">
        <div class="body-text">⚠️ 입력한 비밀번호는 평균적인 사용자보다 <strong>더 예측 가능</strong>할 수 있습니다.<br>
        반복 패턴, 연속 숫자, 연도 등의 요소가 편향을 높입니다.</div></div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""<div class="glass" style="border-color:rgba(120,255,180,0.30);">
        <div class="body-text">✅ 평균 사용자보다 상대적으로 <strong>랜덤</strong>합니다.</div></div>""", unsafe_allow_html=True)

======================

SECTION 2 — 작은 편향은 어떤 결과를 만들까?

======================

st.markdown(f'2️⃣ 작은 편향은 어떤 결과를 만들까?', unsafe_allow_html=True)

st.markdown(f"""

bias_strength = st.slider("인간의 편향 강도", 0, 100, 20, key="bias_slider")states = np.arange(20)weights = np.exp(bias_strength / 25 * np.linspace(0, 1, 20))weights /= weights.sum()

sim_df = pd.DataFrame({"상태 번호": states, "선택 확률": weights})fig = px.bar(sim_df, x="상태 번호", y="선택 확률",color_discrete_sequence=[bar_color], title="상태 분포 — 편향 강도에 따른 변화")fig = apply_chart_theme(fig)st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""

======================

SECTION 3 — 사람이 많아지면?

======================

st.markdown(f'3️⃣ 사람이 많아지면 무슨 일이 일어날까?', unsafe_allow_html=True)

population = st.slider("비밀번호를 만드는 사람 수", 1, 100000, 5000, step=1000, key="pop_slider")

samples = np.random.choice(states, size=population, p=weights)freq = pd.Series(samples).value_counts()concentration = freq.max() / population

fig = px.histogram(x=samples, nbins=20, color_discrete_sequence=[bar_color2],title=f"집단 선택 결과 — {population:,}명의 선택 분포")fig = apply_chart_theme(fig)fig.update_layout(xaxis_title="상태 번호", yaxis_title="선택 횟수")st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)with col1:st.markdown(f"""{concentration:.3f}집중도 (최고 빈도 / 전체)""", unsafe_allow_html=True)with col2:st.markdown(f"""{population:,}시뮬레이션 인원""", unsafe_allow_html=True)

st.markdown(f"""

======================

SECTION 4 — 질서변수 관찰

======================

st.markdown(f'4️⃣ 질서변수(Order Parameter)를 관찰해보자', unsafe_allow_html=True)

order = concentrationfig = go.Figure()fig.add_bar(x=["현재 시뮬레이션", "실제 데이터 (RockYou)"],y=[order, AVG_ORDER],marker_color=[bar_color, bar_color2],text=[f"{order:.3f}", f"{AVG_ORDER}"],textposition="outside")fig = apply_chart_theme(fig)fig.update_layout(title="Order Parameter 비교", yaxis_title="Order Parameter", yaxis_range=[0, 1.1])st.plotly_chart(fig, use_container_width=True)

if order > 0.5:status_text = f"질서 상태가 형성되었다. (Order Parameter = {order:.3f})집단은 더 이상 랜덤하지 않다."status_color = "rgba(120,255,180,0.30)"else:status_text = f"아직 무질서 상태에 가깝다. (Order Parameter = {order:.3f})편향 강도를 높이면 질서 상태로 전환된다."status_color = "rgba(255,200,100,0.25)"

st.markdown(f"""

======================

SECTION 5 — 발견 요약 (실제 데이터)

======================

st.markdown(f'5️⃣ 실제 데이터에서 무엇을 발견했을까?', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)findings = [("편향 존재", f"평균 편향 {AVG_BIAS}"),("상태 집중", "상위 10개 구조가\n대다수 차지"),("질서 형성", f"Order Parameter\n평균 {AVG_ORDER}"),("자기조직화", "규칙 없이\n패턴 반복"),]icons = ["🎯", "📌", "🔮", "🌀"]for col, (title, desc), icon in zip([col1, col2, col3, col4], findings, icons):with col:st.markdown(f"""{icon}{title}{desc}""", unsafe_allow_html=True)

if DATA_OK:st.markdown(f'📈 실제 Shannon Entropy 분포', unsafe_allow_html=True)fig = px.histogram(df, x="shannon_entropy", nbins=50,color_discrete_sequence=[bar_color],title="RockYou 데이터셋 Shannon Entropy 분포")fig = apply_chart_theme(fig)fig.update_layout(xaxis_title="Shannon Entropy (bits)", yaxis_title="비밀번호 수")st.plotly_chart(fig, use_container_width=True)

======================

결론

======================

st.markdown(f"""
