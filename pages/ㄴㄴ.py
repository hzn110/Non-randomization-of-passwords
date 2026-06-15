import streamlit as st
import pandas as pd

df = pd.read_csv("rockyou_rigorous_behavioral_physics_v2 (1).csv")

st.write(df.shape)

st.write("Human Bias 평균")
st.write(df["human_bias_score"].mean())

st.write("Entropy 평균")
st.write(df["shannon_entropy"].mean())

st.write("Order Parameter 평균")
st.write(df["order_parameter"].mean())
