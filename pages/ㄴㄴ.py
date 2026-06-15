import pandas as pd

df = pd.read_csv("rockyou_rigorous_behavioral_physics_v2 (1).csv")

print(df.shape)

print(df["human_bias_score"].mean())
print(df["shannon_entropy"].mean())
print(df["order_parameter"].mean())
