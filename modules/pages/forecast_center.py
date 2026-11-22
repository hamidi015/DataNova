import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from modules.data_loader import load_data
from modules.ml_engine import MLEngine

def show(uploaded_file):
    """Forecast Center Page - Only Forecasting Content"""
    
    st.title("📈 Forecast Center")
    st.caption("AI-Powered Revenue Forecasting & Predictions")
    
    # Load data
    df = load_data(uploaded_file)
    
    st.info("🔮 Analyzing historical data and generating forecasts...")
    
    # ===== PREPARE DATA =====
    numeric_df = df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) < 2:
        st.error("❌ Need at least 2 numeric columns for forecasting")
        st.stop()
    
    X = numeric_df.iloc[:, :-1]
    y = numeric_df.iloc[:, -1]
    
    # ===== TRAIN MODELS =====
    engine = MLEngine()
    engine.train(X, y)
    
    accuracy_scores = engine.evaluate()
    
    # Create forecast data (simulate next periods)
    next_data = X.iloc[-1:] * 1.05
    predictions = engine.predict(next_data)
    
    st.success("✅ Forecast models ready!")
    
    st.markdown("---")
    
    # ===== EXECUTIVE SUMMARY =====
    st.subheader("📋 Forecast Executive Summary")
    
    best_model = engine.get_best_model(accuracy_scores)
    best_accuracy = accuracy_scores[best_model]
    best_prediction = predictions[best_model]
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.metric(
            "🏆 Best Model",
            best_model.replace("_", " ").title()
        )
    
    with summary_col2:
        st.metric(
            "📊 Confidence Score",
            f"{best_accuracy * 100:.1f}%"
        )
    
    with summary_col3:
        current_revenue = y.iloc[-1]
        growth = ((best_prediction - current_revenue) / current_revenue * 100)
        st.metric(
            "📈 Expected Growth",
            f"{growth:.2f}%"
        )
    
    with summary_col4:
        st.metric(
            "🎯 Forecast Revenue",
            f"${best_prediction:,.0f}"
        )
    
    st.markdown("---")
    
    # ===== CURRENT vs FORECAST =====
    st.subheader("💰 Revenue Forecast Comparison")
    
    current_revenue = y.iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "📊 Current Revenue",
            f"${current_revenue:,.0f}"
        )
    
    with col2:
        st.metric(
            "🔮 Forecast Revenue",
            f"${best_prediction:,.0f}",
            delta=f"${best_prediction - current_revenue:,.0f}"
        )
    
    with col3:
        growth_rate = ((best_prediction - current_revenue) / current_revenue * 100)
        st.metric(
            "📈 Growth Rate",
            f"{growth_rate:.2f}%"
        )
    
    st.markdown("---")
    
    # ===== ALL MODEL FORECASTS =====
    st.subheader("🤖 Machine Learning Forecast Models")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        lr_growth = ((predictions['linear_regression'] - current_revenue) / current_revenue * 100)
        st.metric(
            "📈 Linear Regression",
            f"${predictions['linear_regression']:,.0f}",
            delta=f"{lr_growth:.2f}%"
        )
    
    with col2:
        rf_growth = ((predictions['random_forest'] - current_revenue) / current_revenue * 100)
        st.metric(
            "🌲 Random Forest",
            f"${predictions['random_forest']:,.0f}",
            delta=f"{rf_growth:.2f}%"
        )
    
    with col3:
        dt_growth = ((predictions['decision_tree'] - current_revenue) / current_revenue * 100)
        st.metric(
            "🌳 Decision Tree",
            f"${predictions['decision_tree']:,.0f}",
            delta=f"{dt_growth:.2f}%"
        )
    
    st.markdown("---")
    
    # ===== MODEL ACCURACY FOR FORECAST =====
    st.subheader("🎯 Model Accuracy Scores")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Linear Regression",
            f"{accuracy_scores['linear_regression']:.4f}"
        )
    
    with col2:
        st.metric(
            "Random Forest",
            f"{accuracy_scores['random_forest']:.4f}"
        )
    
    with col3:
        st.metric(
            "Decision Tree",
            f"{accuracy_scores['decision_tree']:.4f}"
        )
    
    # Confidence level indicator
    if best_accuracy >= 0.90:
        st.success("✅ **Very High Confidence** - Forecast is highly reliable")
    elif best_accuracy >= 0.75:
        st.info("ℹ️ **Good Confidence** - Forecast is reliable")
    elif best_accuracy >= 0.60:
        st.warning("⚠️ **Moderate Confidence** - Use with caution")
    else:
        st.error("❌ **Low Confidence** - Recommend more historical data")
    
    st.markdown("---")
    
    # ===== FORECAST CHART =====
    st.subheader("📊 Forecast Visualization")
    
    # Create forecast dataframe with historical + predicted
    forecast_data = pd.DataFrame({
        "Period": list(range(1, len(y) + 2)),
        "Revenue": list(y.values) + [best_prediction],
        "Type": ["Historical"] * len(y) + ["Forecast"]
    })
    
    fig = px.line(
        forecast_data,
        x="Period",
        y="Revenue",
        color="Type",
        markers=True,
        title="Revenue Forecast - Historical & Predicted",
        labels={"Revenue": "Revenue ($)", "Period": "Time Period"}
    )
    
    fig.add_hline(
        y=current_revenue,
        line_dash="dash",
        line_color="gray",
        annotation_text="Current Level"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ===== PREDICTION TABLE =====
    st.subheader("📋 Forecast Details")
    
    forecast_table = pd.DataFrame({
        "Model": ["Linear Regression", "Random Forest", "Decision Tree"],
        "Forecast": [
            predictions['linear_regression'],
            predictions['random_forest'],
            predictions['decision_tree']
        ],
        "Accuracy": [
            accuracy_scores['linear_regression'],
            accuracy_scores['random_forest'],
            accuracy_scores['decision_tree']
        ],
        "Growth %": [
            ((predictions['linear_regression'] - current_revenue) / current_revenue * 100),
            ((predictions['random_forest'] - current_revenue) / current_revenue * 100),
            ((predictions['decision_tree'] - current_revenue) / current_revenue