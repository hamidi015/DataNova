import streamlit as st
import pandas as pd

df = pd.read_csv("data/sales.csv")

st.title("🚀 DataNova Dashboard")

st.subheader("Sales Data")

st.dataframe(df)

total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Revenue", total_revenue)

with col2:
    st.metric("Total Profit", total_profit)

st.subheader("Revenue by Product")

st.bar_chart(
    df.set_index("Product")["Revenue"]
)
st.subheader("Profit by Product")

st.bar_chart(
    df.set_index("Product")["Profit"]
)

best_product = df.loc[
    df["Revenue"].idxmax(),
    "Product"
]

st.success(
    f"🏆 Best Product: {best_product}"
)