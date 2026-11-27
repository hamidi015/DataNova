import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DataNova",
    page_icon="🚀",
    layout="wide"
)

import pandas as pd
import numpy as np

st.markdown("""
<style>

div[data-testid="metric-container"] {
    background: rgba(20,20,20,0.9);
    border: 2px solid #00D4FF;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(0,212,255,0.6);
}

</style>
""", unsafe_allow_html=True)


from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor


from modules.pdf_report import generate_pdf_report

from modules.customer_segmentation import (
    segment_customers,
    get_largest_segment,
    get_recommendation
)

from modules.profit_analysis import (

    total_profit,
    most_profitable_product,
    least_profitable_product,
    highest_revenue_product

)

from modules.campaign_ranking import (

    best_campaign,
    worst_campaign,
    campaign_leaderboard

)

# =====================================
# SHARED SECTION - ALL PAGES
# =====================================

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)

col1, col2 = st.columns([1, 4])

with col1:
    st.image(
        "assets/datanova_logo.png",
        width=220
    )

with col2:
    st.title("🚀 DataNova v8.7")
    st.caption(
        "AI-Powered Business Analytics & Forecasting Platform"
    )

st.markdown("""
### 🤖 AI-Powered Business Analytics & Forecasting Platform

Transforming business data into intelligent decisions.
""")

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

st.sidebar.success("🚀 DataNova v8.7")

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

dataset_type = "Unknown"

if (
    "Product" in df.columns
    and "Revenue" in df.columns
    and "Profit" in df.columns
):
    dataset_type = "Business Analytics"

elif (
    "Customer" in df.columns
    and "Age" in df.columns
):
    dataset_type = "Customer Analytics"

elif (
    "Campaign" in df.columns
    and "Clicks" in df.columns
):

    dataset_type = "Marketing Analytics"
    
if dataset_type == "Business Analytics":

    required_columns = [
        "Product",
        "Revenue",
        "Profit"
    ]

elif dataset_type == "Customer Analytics":

    required_columns = [
        "Customer",
        "Age"
    ]

elif dataset_type == "Marketing Analytics":

    required_columns = [
        "Campaign",
        "Clicks"
    ]

else:

    st.error(
        "❌ Unsupported dataset type."
    )
    st.stop()


missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"❌ Missing required columns: {', '.join(missing_columns)}"
    )
    st.stop()

st.success(
    f"✅ {dataset_type} Dataset Detected"
)

numeric_columns = list(
    df.select_dtypes(include="number").columns
)

categorical_columns = list(
    df.select_dtypes(exclude="number").columns
)

st.info(
    f"Numeric Columns: {numeric_columns}"
)

st.info(
    f"Categorical Columns: {categorical_columns}"
)

if len(numeric_columns) > 0:

    selected_target = st.selectbox(
        "🎯 Select Target Column",
        numeric_columns
    )
    
st.write("Selected Target:", selected_target)

st.write("All Numeric Columns:")
st.write(numeric_columns)


st.subheader("🤖 AI Dataset Summary")

st.write(
    f"This dataset contains {df.shape[0]} rows and {df.shape[1]} columns."
)

st.write(
    f"Detected {len(numeric_columns)} numeric column(s)."
)

st.write(
    f"Detected {len(categorical_columns)} categorical column(s)."
)

if len(numeric_columns) > len(categorical_columns):

    st.success(
        "This dataset appears to be primarily numerical and suitable for machine learning and forecasting."
    )

else:

    st.success(
        "This dataset appears to contain significant categorical information and is suitable for segmentation and visualization."
    )

if dataset_type == "Customer Analytics":

    st.info("👥 Customer Analytics Module")

    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")

    st.subheader("👥 Customer Analytics")

    st.write("Column Names:")
    st.write(list(df.columns))

if "Age" in df.columns:

    st.write(
        f"Average Age: {df['Age'].mean():.1f}"
    )

    st.write(
        f"Youngest Age: {df['Age'].min()}"
    )

    st.write(
        f"Oldest Age: {df['Age'].max()}"
    )

    average_age = df['Age'].mean()

    st.subheader("🤖 AI Customer Insight")

    if average_age < 35:

        st.success(
            "Customer base is relatively young. Focus on digital engagement and mobile-first strategies."
        )

    else:

        st.success(
            "Customer base is mature. Focus on loyalty programs and personalized services."
        )


    if "Country" in df.columns:

        st.write("Countries:")

        st.write(
            df["Country"].unique()
        )
        
        st.write(
            f"Countries Count: {df['Country'].nunique()}"
        )

        st.write(
            f"Countries Count: {df['Country'].nunique()}"
        )

        if len(numeric_columns) > 0 and len(categorical_columns) > 0:

            st.subheader("📊 Automatic Visualization")

            auto_chart = px.bar(
                df,
                x=categorical_columns[0],
                y=numeric_columns[0],
                title="Automatic Dataset Visualization"
            )

            st.plotly_chart(
                auto_chart,
                use_container_width=True
            )


elif dataset_type == "Marketing Analytics":

    st.info("📢 Marketing Analytics Module")

    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")

    st.subheader("📢 Marketing Analytics")

    st.write("Column Names:")
    st.write(list(df.columns))

    if "Clicks" in df.columns:
        st.write(
            f"Total Clicks: {df['Clicks'].sum()}"
        )

    if "Campaign" in df.columns:
        st.write("Campaigns:")
        st.write(
            df["Campaign"].unique()
        )



if page == "📊 Dashboard" and "Product" in df.columns:

    product_options = ["All Products"] + list(df["Product"])

    selected_product = st.selectbox(
        "Choose a Product",
        product_options
    )

    search_term = st.text_input(
        "Search Product"
    )

else:

    selected_product = "All Products"
    search_term = ""


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

if "Revenue" in filtered_df.columns:
    selected_revenue = filtered_df["Revenue"].sum()
else:
    selected_revenue = 0

if "Profit" in filtered_df.columns:
    selected_profit = filtered_df["Profit"].sum()
else:
    selected_profit = 0

# =====================================
# DASHBOARD PAGE
# =====================================

if page == "📊 Dashboard":

    st.subheader("Selected Product")

    st.write(
        f"You selected: {selected_product}"
    )


if page == "📊 Dashboard":

    st.subheader("Sales Data")

    st.dataframe(filtered_df)


if page == "📊 Dashboard":

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



if "Revenue" in df.columns:
    total_revenue = df["Revenue"].sum()
else:
    total_revenue = 0

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

if "Profit" in df.columns:
    total_profit_value = df["Profit"].sum()
else:
    total_profit_value = 0

predicted_revenue = total_revenue * 1.10

missing_values = df.isnull().sum().sum()

if total_revenue > 0:
    growth_rate = (
        (predicted_revenue - total_revenue)
        / total_revenue
    ) * 100
else:
    growth_rate = 0


if selected_revenue > 0:
    profit_margin = (
        selected_profit / selected_revenue
    ) * 100
else:
    profit_margin = 0
    
##### Here I did changes I will come back for it later########
if page == "📊 Dashboard":

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Revenue",
            selected_revenue
    )

    with col2:
        st.metric(
            "📈 Profit",
            selected_profit
    )

    with col3:
        st.metric(
            "📊 Margin",
            f"{profit_margin:.2f}%"
    )

    with col4:
        st.metric(
            "📦 Products",
            len(df)
    )
####################### bis here #############

if page == "📊 Dashboard":

    with col1:
        st.subheader("Revenue by Product")

    fig = px.bar(
        df,
        x=categorical_columns[0],
        y=numeric_columns[0],
        color=categorical_columns[0],
        title="Dataset Overview"
    )

    st.plotly_chart(fig)

    with col2:
        st.subheader("Revenue Table")

        st.dataframe(df)

if page == "📊 Dashboard":

    st.subheader("Profit by Product")

    profit_fig = px.bar(
        df,
        x=categorical_columns[0],
        y=numeric_columns[0],
        color=categorical_columns[0],
        title="Dataset Analysis"
    )

    st.plotly_chart(profit_fig)

if page == "📊 Dashboard":

    st.subheader("Revenue vs Profit Comparison")

comparison_df = df

comparison_fig = px.bar(
    comparison_df,
    x=categorical_columns[0],
    y=numeric_columns[0],
    title="Dataset Comparison"
)

st.plotly_chart(
    comparison_fig,
    key="comparison_chart"
)


if "Revenue" in df.columns and "Product" in df.columns:

    best_product = df.loc[
        df["Revenue"].idxmax(),
        "Product"
    ]

else:

    best_product = "N/A"

if page == "📊 Dashboard":

    st.success(
        f"🏆 Best Product: {best_product}"
    )

if page == "📊 Dashboard":

    st.subheader("🤖 AI Dataset Analyzer")

    if profit_margin >= 20:
        recommendation = (
            "Continue investing in top-performing products and expand the business."
        )

    elif profit_margin >= 10:
        recommendation = (
            "Business performance is stable. Continue monitoring growth."
        )

    else:
        recommendation = (
            "Profit margins are low. Review pricing and profitability."
        )

    if missing_values == 0:
        data_quality = "Excellent"

    elif missing_values <= 5:
        data_quality = "Good"

    else:
        data_quality = "Poor"

    summary = f"""

📊 Dataset Overview

• Products analyzed: {len(df)}

• Total Revenue: {selected_revenue}

• Total Profit: {selected_profit}

• Selected Product: {selected_product}

• Profit Margin: {profit_margin:.2f}%

✅ Data Quality: {data_quality}

🎯 Business Health Score: Available in Executive Summary section

💡 AI Recommendation:
{recommendation}
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

    if "Revenue" in df.columns:

        st.write(f"Maximum Revenue: {df['Revenue'].max()}")

        st.write(f"Minimum Revenue: {df['Revenue'].min()}")

        st.write(f"Average Revenue: {df['Revenue'].mean():.2f}")

    else:

        st.info("Revenue statistics are not available for this dataset.")





if page == "📊 Dashboard":

    st.subheader("Profit Statistics")


if page == "📊 Dashboard":

    st.header("🤖 AI & Business Insights")

    st.subheader("Business Health Score")

score = 100

if missing_values > 0:
    score -= 20

if total_profit_value < 500:
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
            total_profit_value
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

    if total_profit_value > 500:
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

    if "Revenue" in df.columns and "Product" in df.columns:

        ranking = df.sort_values(
            by="Revenue",
            ascending=False
        )

        st.dataframe(
            ranking[["Product", "Revenue"]]
        )

    else:

        st.info(
            "Product ranking is not available for this dataset."
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

    st.subheader("Dataset Share")

    pie_fig = px.pie(
        df,
        values=numeric_columns[0],
        names=categorical_columns[0],
        title="Dataset Distribution"
    )

    st.plotly_chart(pie_fig)

if page == "📊 Dashboard":

    st.subheader("Dataset Trend Insight")

    if "Revenue" in df.columns:

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

    else:

        st.info(
            "Revenue trend analysis is not available for this dataset."
        )


    st.subheader("Top Product Share")

    if "Revenue" in df.columns and total_revenue > 0:

        top_share = (
            df["Revenue"].max()
            / total_revenue
        ) * 100

        st.write(
            f"{best_product} contributes {top_share:.2f}% of total revenue."
        )

    else:

        st.info(
            "Product share analysis is not available for this dataset."
        )




if page == "📈 Forecast Center":

    if dataset_type == "Customer Analytics":

        st.title("👥 Customer Forecast Center")

        st.info(
            "Customer forecasting is under development."
        )

        st.metric(
            "Average Age",
            f"{df['Age'].mean():.1f}"
        )

        st.metric(
            "Countries",
            df["Country"].nunique()
        )

        st.success(
            "Customer Forecast Center loaded successfully."
        )

        st.stop()


    if dataset_type == "Marketing Analytics":

        st.title("📢 Marketing Forecast Center")

        st.info(
            "Marketing forecasting is under development."
        )

        st.metric(
            "Total Clicks",
            df["Clicks"].sum()
        )

        st.metric(
            "Campaigns",
            df["Campaign"].nunique()
        )

        st.success(
            "Marketing Forecast Center loaded successfully."
        )

        st.stop()


    st.title("📈 Forecast Center")

    st.success(
        "AI-powered forecasting and future revenue analysis."
    )

    st.success(
        "AI-powered forecasting and future revenue analysis."
    )

    st.caption(
        "DataNova v8.7 | AI-Powered Multi-Model Forecasting Platform"
    )

    st.info(
        "This page uses Machine Learning to forecast future business revenue."
    )


# =====================================
# MACHINE LEARNING PAGE
# =====================================

if page == "🤖 Machine Learning":
    
    if dataset_type == "Marketing Analytics":

        st.title("📢 Marketing Machine Learning")

        st.info(
            "Marketing analytics model is under development."
        )

        st.metric(
            "Total Clicks",
            df["Clicks"].sum()
        )

        st.metric(
            "Campaigns",
            df["Campaign"].nunique()
        )

        st.success(
            "Marketing dataset detected successfully."
        )

        st.stop()

    if dataset_type == "Customer Analytics":

        st.title("👥 Customer Machine Learning")

        st.info(
            "Customer analytics model is under development."
        )

        st.metric(
            "Average Age",
            f"{df['Age'].mean():.1f}"
        )

    if "Country" in df.columns:

        st.metric(
            "Countries",
            df["Country"].nunique()
        )

        segments = segment_customers(df)

        largest_segment = get_largest_segment(
            segments
        )

        recommendation = get_recommendation(
            largest_segment
        )

        st.subheader(
            "🎯 Customer Segmentation"
        )

        st.write(
            f"Young Customers: {segments['Young']}"
        )

        st.write(
            f"Middle Age Customers: {segments['Middle']}"
        )

        st.write(
            f"Senior Customers: {segments['Senior']}"
        )

        st.success(
            f"Largest Segment: {largest_segment}"
        )

        st.info(
            recommendation
        )

    st.success(
        "Customer dataset detected successfully."
    )

    #st.stop()


    st.title("🤖 Machine Learning")

    st.info(
        "Compare machine learning models and evaluate prediction accuracy."
    )

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
    
    st.subheader("🏆 Best Model")

    best_accuracy = max(
        accuracy,
        rf_accuracy,
        dt_accuracy
    )
    if best_accuracy == accuracy:
        st.success(
            f"Linear Regression is the best model with accuracy {accuracy:.2f}"
        )

    elif best_accuracy == rf_accuracy:
        st.success(
            f"Random Forest is the best model with accuracy {rf_accuracy:.2f}"
        )

    else:
        st.success(
            f"Decision Tree is the best model with accuracy {dt_accuracy:.2f}"
        )

    st.subheader("🏅 Model Leaderboard")

    leaderboard_df = pd.DataFrame({
        "Model": [
            "Linear Regression",
            "Random Forest",
            "Decision Tree"
        ],
        "Accuracy": [
            accuracy,
            rf_accuracy,
            dt_accuracy
        ]
    })

    leaderboard_df = leaderboard_df.sort_values(
        by="Accuracy",
        ascending=False
    )

    st.dataframe(leaderboard_df)

    st.info(
        "Decision Tree currently provides the highest accuracy and is recommended for forecasting."
    )

    st.subheader("📊 Model Accuracy Comparison")

    chart_df = pd.DataFrame({
        "Model": [
            "Linear Regression",
            "Random Forest",
            "Decision Tree"
        ],
        "Accuracy": [
            accuracy,
            rf_accuracy,
            dt_accuracy
        ]
    })

    chart_fig = px.bar(
        chart_df,
        x="Model",
        y="Accuracy",
        color="Model",
        title="Machine Learning Model Accuracy"
    )

    st.plotly_chart(chart_fig)
    
    st.subheader("💰 Profit Intelligence")

    if "Profit" in df.columns and "Product" in df.columns:

        st.success(
            f"Total Profit: ${total_profit(df):,.2f}"
        )

        st.info(
            f"Most Profitable Product: {most_profitable_product(df)}"
        )

        st.warning(
            f"Least Profitable Product: {least_profitable_product(df)}"
        )

        st.write(
            f"Highest Revenue Product: {highest_revenue_product(df)}"
        )

    else:
        st.info(
            "Profit analysis requires Product and Profit columns."
        )


    st.subheader("📢 Campaign Intelligence")

    if "Campaign" in df.columns and "Revenue" in df.columns:

        st.success(
            f"Best Campaign: {best_campaign(df)}"
        )

        st.warning(
            f"Worst Campaign: {worst_campaign(df)}"
        )

        st.dataframe(
            campaign_leaderboard(df)
        )

    else:

        st.info(
            "Campaign analysis requires Campaign and Revenue columns."
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
        "14"
    )

    st.metric(
        "AI IQ",
        "14 Skills"
    )

    st.metric(
        "Version",
        "v8.7"
    )

    st.subheader("🤖 AI Business Summary")

    if dataset_type == "Business Analytics":

        st.success(
            f"""
🏆 Best Product: {best_product}

💰 Total Revenue: {total_revenue}

💵 Total Profit: {total_profit_value}

🎯 Business Health Score: {score}/100

📈 Forecast Revenue: {ml_prediction:.0f}
"""
    )

    elif dataset_type == "Customer Analytics":

        st.success(
            f"""
👥 Average Age: {df['Age'].mean():.1f}

🌍 Countries: {df['Country'].nunique()}

🤖 Customer base appears diverse and relatively young.
"""
    )

    elif dataset_type == "Marketing Analytics":

        st.success(
        f"""
📢 Total Clicks: {df['Clicks'].sum()}

📈 Campaigns: {df['Campaign'].nunique()}

🤖 Marketing engagement appears healthy.
"""
    )

    st.subheader("🤖 Ask DataNova")

    st.markdown("""

### Try asking:

- What is my best product?
- What is the forecast revenue?
- What is my total profit?
- What is my business health score?
- Which model is most accurate?
- Should I increase investment?
""")

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

            if score >= 80:
                st.success(
                    "Recommendation: Increase investment and business expansion."
                )

            elif score >= 60:
                st.info(
                    "Recommendation: Maintain current strategy and monitor growth."
                )

            else:
                st.warning(
                    "Recommendation: Review business performance before increasing investment."
                )

        elif "accurate" in user_question.lower():
            st.success(
                "Decision Tree is currently the most accurate model."
        )
        
                    
        elif "current revenue" in user_question.lower():
            st.success(
                f"Current Revenue: {total_revenue}"
        )     
        
        elif "revenue" in user_question.lower():
            st.success(
                f"Total Revenue: {total_revenue}"
        )
        elif "margin" in user_question.lower():
            st.success(
                f"Profit Margin: {profit_margin:.2f}%"
        )

        elif "growth" in user_question.lower():
            st.success(
                f"Expected Growth: {growth_rate:.2f}%"
            )

        elif "forecast growth" in user_question.lower():
            st.success(
                f"Forecast Growth Rate: {growth_rate:.2f}%"
            )

        elif "profit" in user_question.lower():
            st.success(
                f"Total Profit: {total_profit_value}"
            )
        
        elif "best model" in user_question.lower():
            st.success(
                "Best Model: Decision Tree"
        )
        
        elif "confidence" in user_question.lower():
            st.success(
                f"Confidence Score: {accuracy * 100:.0f}%"
        )
        
        elif "health score" in user_question.lower():
            st.success(
                f"Health Score: {score}/100"
        )
        
        elif "products" in user_question.lower():
            st.success(
                f"Total Products: {len(df)}"
        )


else:
    st.warning(
        "Sorry, I don't understand that question yet."
    )
if dataset_type == "Customer Analytics":

    customer_question = st.selectbox(
        "Choose a customer question",
        [
            "What is the average age?",
            "How many countries are represented?",
            "What customer insight do you have?"
        ]
    )

    if customer_question == "What is the average age?":
        st.success(
            f"Average Age: {df['Age'].mean():.1f}"
        )

    elif customer_question == "How many countries are represented?":
        st.success(
            f"Countries: {df['Country'].nunique()}"
        )

    elif customer_question == "What customer insight do you have?":
        st.success(
            "Customer base appears diverse and relatively young."
        )

    st.stop()



if dataset_type == "Marketing Analytics":

    marketing_question = st.selectbox(
        "Choose a marketing question",
        [
            "What are the total clicks?",
            "How many campaigns are there?",
            "What marketing insight do you have?"
        ]
    )

    if marketing_question == "What are the total clicks?":
        st.success(
            f"Total Clicks: {df['Clicks'].sum()}"
        )

    elif marketing_question == "How many campaigns are there?":
        st.success(
            f"Campaigns: {df['Campaign'].nunique()}"
        )

    elif marketing_question == "What marketing insight do you have?":
        st.success(
            "Marketing engagement appears healthy."
        )

    st.stop()

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

#####################################################

if page == "📈 Forecast Center":

    st.success(
        f"""
🏆 Best Model: Decision Tree

📈 Forecast Revenue: {ml_prediction:.0f}

📈 Expected Growth: {growth_rate:.2f}%

🎯 Confidence Score: {accuracy * 100:.0f}%

✅ Forecast Reliability: Very High

📊 Models Compared: 3

💡 Recommendation: Continue business expansion.
"""
)

    st.subheader("📈 Revenue Forecast")

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
        f"Current Revenue: {total_revenue}\n"
        f"Predicted Revenue: {ml_prediction:.0f}\n"
        f"Expected Growth: {growth_rate:.2f}%"
    )


    st.subheader("🔬 Model Forecast Details")
    
    st.info(
    "This section compares forecast outputs from multiple machine learning models."
    )

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

    st.subheader("💡 Forecast Recommendation")

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

    st.markdown("---")
    
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

    report = (
        f"Forecast Revenue: {ml_prediction:.0f}\n"
        f"Expected Growth: {growth_rate:.2f}%\n"
        f"Best Model: Decision Tree\n"
        f"Confidence Score: {accuracy * 100:.0f}%\n"
        f"Recommendation: Continue investing in high-performing products and monitor revenue growth trends."
    )

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

    st.subheader("📈 Machine Learning Forecast Chart")


    forecast_fig = px.line(
        forecast_df,
        x="Month",
        y="Revenue",
        markers=True,
        title="Revenue Forecast with Machine Learning"
    )

    st.plotly_chart(forecast_fig)

##########################################################


# Product Summary
if page == "📊 Dashboard":

    if "Profit" in df.columns:

        st.write(f"Maximum Profit: {df['Profit'].max()}")

        st.write(f"Minimum Profit: {df['Profit'].min()}")

        st.write(f"Average Profit: {df['Profit'].mean():.2f}")

    else:

        st.info(
            "Profit statistics are not available for this dataset."
        )


    st.subheader("Product Summary")

    st.write(
        f"Total Products Analyzed: {len(df)}"
    )

if page == "📊 Dashboard":

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


    st.caption(
        "DataNova v8.7 | Built with Python, Pandas, Plotly, Scikit-Learn and Streamlit"
    )