import plotly.express as px
import streamlit as st
import pandas as pd
from modules.pdf_report import generate_pdf_report

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)

st.title("🚀 DataNova Dashboard")

st.markdown(
    """
    ### Interactive Business Analytics Dashboard

    Built with Python, Pandas, Plotly and Streamlit.
    """
)

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
    excel_file = pd.ExcelFile(uploaded_file)

    selected_sheet = st.selectbox(
        "Select Excel Sheet",
        excel_file.sheet_names
    )

    df = pd.read_excel(
        uploaded_file,
        sheet_name=selected_sheet
    )

st.success(
    f"Loaded file: {uploaded_file.name}"
)


product_options = ["All Products"] + list(df["Product"])

selected_product = st.selectbox(
    "Choose a Product",
    product_options
)

search_term = st.text_input(
    "Search Product"
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

if search_term:
    filtered_df = filtered_df[
        filtered_df["Product"]
        .str.contains(
            search_term,
            case=False
        )
    ]

selected_revenue = filtered_df["Revenue"].sum()

selected_profit = filtered_df["Profit"].sum()

st.subheader("Selected Product")

st.write(
    f"You selected: {selected_product}"
)

st.subheader("Sales Data")

st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name=f"{selected_product}_data.csv",
    mime="text/csv"
)



st.subheader("Dataset Preview")

st.dataframe(df.head())



total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()

profit_margin = (
    selected_profit / selected_revenue
) * 100

col1, col2, col3, col4 = st.columns(4)

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

with col4:
    st.metric(
        "Products",
        len(df)
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product")

    fig = px.bar(
        df,
        x="Product",
        y="Revenue",
        color="Product",
        title="Revenue by Product"
    )

    st.plotly_chart(fig)

with col2:
    st.subheader("Revenue Table")
    st.dataframe(
        df[["Product", "Revenue"]]
    )

st.subheader("Profit by Product")

profit_fig = px.bar(
    df,
    x="Product",
    y="Profit",
    color="Product",
    title="Profit by Product"
)

st.plotly_chart(profit_fig)

st.subheader("Revenue vs Profit Comparison")

comparison_df = df[
    ["Product", "Revenue", "Profit"]
]

comparison_fig = px.bar(
    comparison_df,
    x="Product",
    y=["Revenue", "Profit"],
    barmode="group",
    title="Revenue vs Profit"
)

st.plotly_chart(
    comparison_fig,
    key="comparison_chart"
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

st.header("🤖 AI & Business Insights")

st.subheader("Business Health Score")

score = 100

if missing_values > 0:
    score -= 20

if total_profit < 500:
    score -= 20

if total_revenue < 2000:
    score -= 20

if profit_margin < 20:
    score -= 20

st.success(f"Business Health Score: {score}/100")

st.subheader("📋 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Revenue",
        total_revenue
    )

with col2:
    st.metric(
        "Profit",
        total_profit
    )

with col3:
    st.metric(
        "Best Product",
        best_product
    )

with col4:
    st.metric(
        "Health Score",
        score
    )

if score >= 80:
    st.success("Business health is excellent.")
elif score >= 60:
    st.warning("Business health is good.")
else:
    st.error("Business health needs improvement.")

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

st.subheader("Revenue Share by Product")

pie_fig = px.pie(
    df,
    values="Revenue",
    names="Product",
    title="Revenue Share by Product"
)

st.plotly_chart(pie_fig)

st.subheader("Top Product Share")

top_share = (
    df["Revenue"].max()
    / total_revenue
) * 100

st.write(
    f"{best_product} contributes {top_share:.2f}% of total revenue."
)

# Revenue Trend Analysis
st.subheader("Revenue Trend Analysis")

trend_fig = px.line(
    df,
    x="Product",
    y="Revenue",
    markers=True,
    title="Revenue Trend"
)

st.plotly_chart(
    trend_fig,
    key="revenue_trend_chart"
)

st.subheader("Revenue Trend Insight")

if df["Revenue"].iloc[0] > df["Revenue"].iloc[-1]:
    st.warning(
        "Revenue trend is decreasing."
    )
else:
    st.success(
        "Revenue trend is increasing."
    )

# Product Summary
st.subheader("Product Summary")

st.write(
    f"Total Products Analyzed: {len(df)}"
)

st.subheader("PDF Report Export")

st.subheader("AI Business Advisor")

if score >= 80:
    st.success(
        f"""
        • {best_product} is the strongest product.
        • Business health is excellent.
        • Continue investing in top-performing products.
        """
    )
elif score >= 60:
    st.warning(
        """
        • Business performance is stable.
        • Review weaker products.
        • Improve revenue growth.
        """
    )
else:
    st.error(
        """
        • Business needs attention.
        • Revenue and profit should be improved.
        • Review strategy and operations.
        """
    )


if st.button("Generate PDF Report"):

    pdf_file = generate_pdf_report(
        total_revenue,
        total_profit,
        profit_margin,
        best_product,
        score
    )

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="Download PDF Report",
            data=file,
            file_name="DataNova_Report.pdf",
            mime="application/pdf"
        )


st.markdown("---")

st.caption(
    "DataNova v4.4 | Built with Python, Pandas, Plotly and Streamlit"
)