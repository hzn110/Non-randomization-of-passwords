import streamlit as st
import pandas as pd

df = pd.read_csv("rockyou_rigorous_behavioral_physics_v2 (1).csv")

st.write(df[[
    "human_bias_score",
    "order_parameter",
    "shannon_entropy",
    "macrostate",
    "macrostate_frequency"
]].describe())

st.write(
    df["macrostate"]
    .value_counts()
    .head(10)
)
