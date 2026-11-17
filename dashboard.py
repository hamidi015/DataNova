import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)

st.title("🚀 DataNova Dashboard")

st.markdown(
    """
    Welcome to DataNova.

    Upload, analyze, and visualize business data in real time.
    """
)

if uploaded_file is None:
    st.info("Please upload a CSV file.")
    st.stop()

if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_excel(uploaded_file)

st.success(
    f"Loaded file: {uploaded_file.name}"
)

product_options = ["All Products"] + list(df["Product"])

selected_product = st.selectbox(
    "Choose a Product",
    product_options
)

st.info(
    f"Currently analyzing: {selected_product}"
)

if selected_product == "All Products":
    filtered_df = df
else:
    filtered_df = df[
        df["Product"] == selected_product
    ]

selected_revenue = filtered_df["Revenue"].sum()

selected_profit = filtered_df["Profit"].sum()

st.subheader("Selected Product")

st.write(
    f"You selected: {selected_product}"
)

st.subheader("Sales Data")

st.dataframe(filtered_df)


st.subheader("Dataset Preview")

st.dataframe(df.head())



total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()

profit_margin = (
    selected_profit / selected_revenue
) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Selected Revenue",
        selected_revenue
    )

with col2:
    st.metric(
        "Selected Profit",
        selected_profit
    )

with col3:
    st.metric(
        "Profit Margin %",
        f"{profit_margin:.2f}%"
    )



col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product")
    st.bar_chart(
        df.set_index("Product")["Revenue"]
    )

with col2:
    st.subheader("Revenue Table")
    st.dataframe(
        df[["Product", "Revenue"]]
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

st.subheader("Automatic Summary Generator")

summary = f"""
The dataset contains {len(df)} products.

Selected revenue is {selected_revenue}.

Selected profit is {selected_profit}.

Selected product is {selected_product}.

Profit margin is {profit_margin:.2f}%.
"""

st.write(summary)

st.subheader("Dataset Information")

st.info(
    f"Dataset contains {len(df)} records and {df.shape[1]} columns."
)

st.success(
    f"Total Records: {len(df)} | Total Columns: {df.shape[1]}"
)

st.subheader("Dataset Insights")


st.write(f"Rows: {df.shape[0]}")

st.write(f"Columns: {df.shape[1]}")
st.write(f"Total Cells: {df.shape[0] * df.shape[1]}")

st.write("Column Names:")

st.write(list(df.columns))

st.subheader("Data Quality Check")

missing_values = df.isnull().sum().sum()

st.write(f"Missing Values: {missing_values}")

if missing_values == 0:
    st.success("Data Quality Score: 100%")
else:
    st.warning("Data Quality Score: Needs Review")

st.subheader("Revenue Statistics")

st.write(f"Maximum Revenue: {df['Revenue'].max()}")

st.write(f"Minimum Revenue: {df['Revenue'].min()}")

st.write(f"Average Revenue: {df['Revenue'].mean():.2f}")

st.subheader("Business Recommendation")

st.info(
    f"Recommendation: Focus on {best_product} because it generates the highest revenue."
)

st.subheader("Profit Statistics")

st.subheader("Business Health Score")

score = 100

if missing_values > 0:
    score -= 20

st.success(f"Business Health Score: {score}/100")

st.write(f"Maximum Profit: {df['Profit'].max()}")

st.write(f"Minimum Profit: {df['Profit'].min()}")

st.write(f"Average Profit: {df['Profit'].mean():.2f}")

st.subheader("Project Status")

st.success("✅ DataNova v1.0 Successfully Running")

st.subheader("Smart Business Insight")

if total_profit > 500:
    st.success("Business is performing well. Profit is above 500.")
else:
    st.warning("Business profit needs improvement.")
    
st.subheader("Revenue Rating")

if total_revenue >= 2000:
    st.success("Excellent Revenue Performance")
else:
    st.warning("Revenue Performance Needs Improvement")

st.subheader("Product Ranking")

ranking = df.sort_values(
    by="Revenue",
    ascending=False
)

st.dataframe(
    ranking[["Product", "Revenue"]]
)

st.subheader("Top 3 Business Insights")

st.write(
    f"1. {best_product} is the best performing product."
)

st.write(
    f"2. The selected product generated {selected_revenue} revenue."
)


st.write(
    f"3. Dataset contains {missing_values} missing values."
)



st.subheader("Top Product Share")

top_share = (
    df["Revenue"].max()
    / total_revenue
) * 100

st.write(
    f"{best_product} contributes {top_share:.2f}% of total revenue."
)

st.subheader("Product Summary")

st.write(
    f"Total Products Analyzed: {len(df)}"
)

st.markdown("---")

st.caption(
    "DataNova v2.5 | Built with Python, Pandas and Streamlit"
)