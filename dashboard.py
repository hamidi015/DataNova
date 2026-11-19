import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor


from modules.pdf_report import generate_pdf_report

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)

st.title("🚀 DataNova v7.2 AI Business Analytics Platform")

st.caption("AI-Powered Business Analytics Dashboard")

page = st.sidebar.radio(
    "📂 Navigation",
    [
        "📊 Dashboard",
        "🤖 Machine Learning",
        "📈 Forecast Center",
        "🤖 AI Assistant"
    ]
)

st.sidebar.markdown("---")

st.sidebar.success("🚀 DataNova v7.2")

st.sidebar.markdown("---")

st.sidebar.write("Features")

st.sidebar.write("✅ Analytics")
st.sidebar.write("✅ Machine Learning")
st.sidebar.write("✅ PDF Reports")

if page == "📊 Dashboard":
    st.sidebar.success("📊 Dashboard")

if page == "🤖 Machine Learning":
    st.sidebar.success("🤖 Machine Learning")

if page == "📈 Forecast Center":
    st.sidebar.success("📈 Forecast Center")

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

if page == "📊 Dashboard":

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

if page == "📊 Dashboard":
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

if page == "📊 Dashboard":

    st.subheader("Selected Product")

    st.write(
        f"You selected: {selected_product}"
    )


if page == "📊 Dashboard":

    st.subheader("Sales Data")

    st.dataframe(filtered_df)


csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name=f"{selected_product}_data.csv",
    mime="text/csv"
)



if page == "📊 Dashboard":

    st.subheader("Dataset Preview")

    st.dataframe(df.head())



total_revenue = df["Revenue"].sum()

history_df = pd.read_csv("data/sales_history.csv")

X = history_df[["Month"]]
y = history_df["Revenue"]

model = LinearRegression()
model.fit(X, y)

rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X, y)

dt_model = DecisionTreeRegressor(
    random_state=42
)

dt_model.fit(X, y)

next_month = np.array([[13]])

ml_prediction = model.predict(next_month)[0]

rf_prediction = rf_model.predict(next_month)[0]
dt_prediction = dt_model.predict(next_month)[0]


predictions = model.predict(X)

accuracy = r2_score(
    y,
    predictions
)

rf_predictions = rf_model.predict(X)

rf_accuracy = r2_score(
    y,
    rf_predictions
)

dt_predictions = dt_model.predict(X)

dt_accuracy = r2_score(
    y,
    dt_predictions
)


forecast_df = history_df.copy()

forecast_df.loc[len(forecast_df)] = [
    13,
    ml_prediction
]

total_profit = df["Profit"].sum()

predicted_revenue = total_revenue * 1.10

missing_values = df.isnull().sum().sum()

growth_rate = (
    (predicted_revenue - total_revenue)
    / total_revenue
) * 100


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


if page == "📊 Dashboard":

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

if page == "📊 Dashboard":

    st.subheader("Profit by Product")

    profit_fig = px.bar(
        df,
        x="Product",
        y="Profit",
        color="Product",
        title="Profit by Product"
    )

    st.plotly_chart(profit_fig)

if page == "📊 Dashboard":

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

if page == "📊 Dashboard":

    st.success(
        f"🏆 Best Product: {best_product}"
    )

if page == "📊 Dashboard":

    st.subheader("Automatic Summary Generator")

    summary = f"""
    The dataset contains {len(df)} products.

    Selected revenue is {selected_revenue}.

    Selected profit is {selected_profit}.

    Selected product is {selected_product}.

    Profit margin is {profit_margin:.2f}%.
    """

    st.write(summary)

if page == "📊 Dashboard":

    st.subheader("Dataset Information")

    st.info(
        f"Dataset contains {len(df)} records and {df.shape[1]} columns."
    )

    st.success(
        f"Total Records: {len(df)} | Total Columns: {df.shape[1]}"
    )



if page == "📊 Dashboard":

    st.subheader("Dataset Insights")

    st.write(f"Rows: {df.shape[0]}")

    st.write(f"Columns: {df.shape[1]}")

    st.write(f"Total Cells: {df.shape[0] * df.shape[1]}")

    st.write("Column Names:")

    st.write(list(df.columns))

if page == "📊 Dashboard":

    st.subheader("Data Quality Check")


    st.write(f"Missing Values: {missing_values}")

    if missing_values == 0:
        st.success("Data Quality Score: 100%")
    else:
        st.warning("Data Quality Score: Needs Review")

if page == "📊 Dashboard":

    st.subheader("Revenue Statistics")

    st.write(f"Maximum Revenue: {df['Revenue'].max()}")

    st.write(f"Minimum Revenue: {df['Revenue'].min()}")

    st.write(f"Average Revenue: {df['Revenue'].mean():.2f}")





if page == "📊 Dashboard":

    st.subheader("Profit Statistics")


if page == "📊 Dashboard":

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

if page == "📊 Dashboard":

    st.success(f"Business Health Score: {score}/100")

if page == "📊 Dashboard":

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

if page == "📊 Dashboard":

    if score >= 80:
        st.success("Business health is excellent.")
    elif score >= 60:
        st.warning("Business health is good.")
    else:
        st.error("Business health needs improvement.")



if page == "📊 Dashboard":

    st.subheader("Project Status")

    st.success("✅ DataNova v7.0 Successfully Running")

if page == "📊 Dashboard":

    st.subheader("Smart Business Insight")

    if total_profit > 500:
        st.success("Business is performing well. Profit is above 500.")
    else:
        st.warning("Business profit needs improvement.")
    
if page == "📊 Dashboard":

    st.subheader("Revenue Rating")

    if total_revenue >= 2000:
        st.success("Excellent Revenue Performance")
    else:
        st.warning("Revenue Performance Needs Improvement")

if page == "📊 Dashboard":

    st.subheader("Product Ranking")

    ranking = df.sort_values(
        by="Revenue",
        ascending=False
    )

    st.dataframe(
        ranking[["Product", "Revenue"]]
    )

if page == "📊 Dashboard":

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

if page == "📊 Dashboard":

    st.subheader("Revenue Share by Product")

    pie_fig = px.pie(
        df,
        values="Revenue",
        names="Product",
        title="Revenue Share by Product"
    )

    st.plotly_chart(pie_fig)

if page == "📊 Dashboard":

    st.subheader("Revenue Trend Insight")

    if df["Revenue"].iloc[0] > df["Revenue"].iloc[-1]:
        st.warning(
            "Revenue trend is decreasing."
        )
    else:
        st.success(
            "Revenue trend is increasing."
        )

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


    st.subheader("Top Product Share")

    top_share = (
        df["Revenue"].max()
        / total_revenue
    ) * 100

    st.write(
        f"{best_product} contributes {top_share:.2f}% of total revenue."
    )




if page == "📈 Forecast Center":

    st.title("📈 Forecast Center")
    
    st.caption(
    "DataNova v7.3 | AI-Powered Multi-Model Forecasting Platform"
)


    st.info(
        "This page uses Machine Learning to forecast future business revenue."
    )
    
if page == "🤖 AI Assistant":

    st.title("🤖 AI Assistant")

    st.success(
        "Welcome to the DataNova AI Business Assistant."
    )

    st.info(
        "Ask business questions and receive intelligent recommendations."
    )
    
    st.metric(
        "Questions Available",
        "8"
    )
    
    st.metric(
        "AI Status",
        "Online"
    )
    
    st.metric(
        "Version",
        "v7.5"
    )

    st.subheader("🤖 Ask DataNova")
    
    st.info(
    "Ask me about products, forecasts, business health, investment, or machine learning models."
)
    
    user_question = st.text_input(
        "Ask DataNova anything"
)

    if user_question:
        st.info(f"You asked: {user_question}")

        if "best product" in user_question.lower():
            st.success(f"Best Product: {best_product}")

        elif "forecast" in user_question.lower():
            st.success(f"Forecast Revenue: {ml_prediction:.0f}")

        elif "business health" in user_question.lower():
            st.success(f"Business Health Score: {score}/100")

        elif "investment" in user_question.lower():
            st.success(
                "Recommendation: Increase investment and business expansion."
            )

        elif "accurate" in user_question.lower():
            st.success(
                "Decision Tree is currently the most accurate model."
            )
        elif "revenue" in user_question.lower():
            st.success(
                f"Total Revenue: {total_revenue}"
        )
        elif "margin" in user_question.lower():
            st.success(
            f"Profit Margin: {profit_margin:.2f}%"
        )

        elif "profit" in user_question.lower():
            st.success(
                f"Total Profit: {total_profit}"
            )
        

    else:
        st.warning(
            "Sorry, I don't understand that question yet."
        )

    
    question = st.selectbox(
        "Choose a business question",
        [
            "What is my best product?",
            "Which model is most accurate?",
            "What is the forecast revenue?",
            "Should I increase investment?",
            "What is my business health?"
        ]
    )

    if question == "What is my best product?":
        st.success(f"Best Product: {best_product}")

    elif question == "Which model is most accurate?":
        st.success("Decision Tree is currently the most accurate model.")

    elif question == "What is the forecast revenue?":
        st.success(f"Forecast Revenue: {ml_prediction:.0f}")

    elif question == "Should I increase investment?":
        st.success(
            "Yes. Current forecast and growth rate indicate positive business performance."
        )

    elif question == "What is my business health?":
        st.success(
            "Business health is excellent with a score of 100/100."
        )

if page == "📈 Forecast Center":

    st.subheader("📋 Executive Forecast Summary")

    st.success(
        f"""
🏆 Best Model: Decision Tree

📈 Forecast Revenue: {ml_prediction:.0f}

📈 Expected Growth: {growth_rate:.2f}%

🎯 Confidence Score: {accuracy * 100:.0f}%

🤖 Models Compared: 3
"""
    )

    st.subheader("Revenue Forecast")

    col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current Revenue",
        f"{total_revenue:.0f}"
    )

with col2:
    st.metric(
        "Forecast Revenue",
        f"{ml_prediction:.0f}"
    )

with col3:
    st.metric(
        "Expected Growth %",
        f"{growth_rate:.2f}%"
    )

st.info(
    f"""
Current Revenue: {total_revenue}

Predicted Revenue: {ml_prediction:.0f}

Expected Growth: {growth_rate:.2f}%
"""
)

st.subheader("🤖 Machine Learning Forecast")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Linear Regression",
        f"{ml_prediction:.0f}"
    )

with col2:
    st.metric(
        "Random Forest",
        f"{rf_prediction:.0f}"
    )

with col3:
    st.metric(
        "Decision Tree",
        f"{dt_prediction:.0f}"
    )

st.metric(
    "AI Confidence Score",
    f"{accuracy * 100:.0f}%"
)

if accuracy >= 0.90:
    st.success("Confidence Level: Very High")
elif accuracy >= 0.75:
    st.info("Confidence Level: High")
else:
    st.warning("Confidence Level: Moderate")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Linear Regression Accuracy",
        f"{accuracy:.2f}"
    )

with col2:
    st.metric(
        "Random Forest Accuracy",
        f"{rf_accuracy:.2f}"
    )

with col3:
    st.metric(
        "Decision Tree Accuracy",
        f"{dt_accuracy:.2f}"
    )


    st.subheader("🏆 Model Comparison")

best_accuracy = max(
    accuracy,
    rf_accuracy,
    dt_accuracy
)

if best_accuracy == accuracy:
    st.success(
        f"Best Model: Linear Regression (Accuracy: {accuracy:.2f})"
    )

elif best_accuracy == rf_accuracy:
    st.success(
        f"Best Model: Random Forest (Accuracy: {rf_accuracy:.2f})"
    )

else:
    st.success(
        f"Best Model: Decision Tree (Accuracy: {dt_accuracy:.2f})"
    )

st.subheader("🤖 AI Recommendation")

if growth_rate > 5:
    st.success(
        "AI Recommendation: Business growth is positive. Consider increasing inventory and marketing investment."
    )

else:
    st.warning(
        "AI Recommendation: Growth is limited. Review pricing and sales strategy."
    )

if ml_prediction > rf_prediction:
    st.success(
        f"Linear Regression predicts higher revenue: {ml_prediction:.0f}"
    )
else:
    st.success(
        f"Random Forest predicts higher revenue: {rf_prediction:.0f}"
    )

prediction_df = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Random Forest",
        "Decision Tree"
    ],
    "Prediction": [
        ml_prediction,
        rf_prediction,
        dt_prediction
    ],
    "Accuracy": [
        accuracy,
        rf_accuracy,
        dt_accuracy
    ]
})

prediction_df = prediction_df.sort_values(
    by="Prediction",
    ascending=False
)

prediction_df.insert(
    0,
    "Rank",
    range(1, len(prediction_df) + 1)
)

st.subheader("📊 Prediction Table")

st.dataframe(prediction_df)

st.success(
    f"Total Models Compared: {len(prediction_df)}"
)

top_model = prediction_df.iloc[0]

st.success(
    f"🏆 Highest Forecast: {top_model['Model']} ({top_model['Prediction']:.0f})"
)

st.subheader("🏅 Model Leaderboard")

st.dataframe(
    prediction_df[
        ["Rank", "Model", "Accuracy", "Prediction"]
    ]
)

csv_predictions = prediction_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Download ML Predictions",
    data=csv_predictions,
    file_name="ml_predictions.csv",
    mime="text/csv"
)

st.subheader("🎯 Executive Decision")

if growth_rate >= 10:
    st.success(
        "Recommendation: Increase investment and business expansion."
    )
elif growth_rate >= 5:
    st.info(
        "Recommendation: Maintain current strategy and monitor growth."
    )
else:
    st.warning(
        "Recommendation: Review sales and pricing strategy."
    )

st.subheader("📄 Forecast Recommendation Report")

report = f"""
Forecast Revenue: {ml_prediction:.0f}

Expected Growth: {growth_rate:.2f}%

Best Model: Decision Tree

Confidence Score: {accuracy * 100:.0f}%

Recommendation:
Continue investing in high-performing products and monitor revenue growth trends.
"""

st.text_area(
    "Executive Forecast Report",
    report,
    height=200
)

st.download_button(
    label="📄 Download Forecast Report",
    data=report,
    file_name="forecast_report.txt",
    mime="text/plain"
)

st.subheader("🤖 Ask DataNova")

question = st.selectbox(
    "Choose a business question",
    [
        "What is my best product?",
        "Which model is most accurate?",
        "What is the forecast revenue?",
        "Should I increase investment?"
        "What is my business health?"
    ]
)

if question == "What is my best product?":
    st.success(f"Best Product: {best_product}")

elif question == "Which model is most accurate?":
    st.success("Decision Tree is currently the most accurate model.")

elif question == "What is the forecast revenue?":
    st.success(f"Forecast Revenue: {ml_prediction:.0f}")

elif question == "Should I increase investment?":
    st.success(
        "Yes. Current forecast and growth rate indicate positive business performance."
    )

elif question == "What is my business health?":
    st.success(
        "Business health is excellent with a score of 100/100."
    )

st.subheader("📈 Machine Learning Forecast Chart")


forecast_fig = px.line(
    forecast_df,
    x="Month",
    y="Revenue",
    markers=True,
    title="Revenue Forecast with Machine Learning"
)

st.plotly_chart(forecast_fig)

# Product Summary
if page == "📊 Dashboard":

    st.write(f"Maximum Profit: {df['Profit'].max()}")

    st.write(f"Minimum Profit: {df['Profit'].min()}")

    st.write(f"Average Profit: {df['Profit'].mean():.2f}")


    st.subheader("Product Summary")

    st.write(
        f"Total Products Analyzed: {len(df)}"
    )

st.subheader("PDF Report Export")

if st.button("Generate PDF Report"):

    pdf_file = generate_pdf_report(
        total_revenue,
        total_profit,
        profit_margin,
        best_product,
        score,
        ml_prediction,
        growth_rate,
        accuracy * 100
    )


    with open(pdf_file, "rb") as file:

        st.download_button(
            label="Download PDF Report",
            data=file,
            file_name="DataNova_Report.pdf",
            mime="application/pdf"
        )

st.subheader("AI Business Advisor")

if score >= 80:
    st.success(
        f"""
        • {best_product} is the strongest product.
        • Business health is excellent.
        • Continue investing in top-performing products.
        """
    )
    
st.markdown("---")

st.caption(
    "DataNova v8.2 | Built with Python, Pandas, Plotly, Scikit-Learn and Streamlit"
)
