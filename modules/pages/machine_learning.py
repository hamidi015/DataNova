import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from modules.data_loader import load_data
from modules.ml_engine import MLEngine

def show(uploaded_file):
    """Machine Learning Page - Only ML Content"""
    
    st.title("🤖 Machine Learning")
    st.caption("Compare ML Models & Evaluate Accuracy")
    
    # Load data
    df = load_data(uploaded_file)
    
    st.info("📊 Training machine learning models on your data...")
    
    # ===== PREPARE DATA =====
    # Get numeric columns for training
    numeric_df = df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) < 2:
        st.error(
    "❌ Machine Learning requires at least 2 numeric columns."
    )

    st.info(
        f"Detected numeric columns: {list(numeric_df.columns)}"
    )

    st.info(
        "Examples: Revenue & Profit, Age & Salary, Clicks & Conversions."
    )
    st.stop()
    
    # Use last column as target, others as features
    X = numeric_df.iloc[:, :-1]
    y = numeric_df.iloc[:, -1]
    
    # ===== TRAIN MODELS =====
    engine = MLEngine()
    engine.train(X, y)
    
    accuracy_scores = engine.evaluate()
    
    st.success("✅ Models trained successfully!")
    
    st.markdown("---")
    
    # ===== MODEL PREDICTIONS =====
    st.subheader("🎯 Next Month Predictions")
    
    # Create prediction data
    next_data = X.iloc[-1:] * 1.05  # Assume 5% increase
    predictions = engine.predict(next_data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "📈 Linear Regression",
            f"${predictions['linear_regression']:,.0f}",
            delta=f"{((predictions['linear_regression'] / y.iloc[-1] - 1) * 100):.1f}%"
        )
    
    with col2:
        st.metric(
            "🌲 Random Forest",
            f"${predictions['random_forest']:,.0f}",
            delta=f"{((predictions['random_forest'] / y.iloc[-1] - 1) * 100):.1f}%"
        )
    
    with col3:
        st.metric(
            "🌳 Decision Tree",
            f"${predictions['decision_tree']:,.0f}",
            delta=f"{((predictions['decision_tree'] / y.iloc[-1] - 1) * 100):.1f}%"
        )
    
    st.markdown("---")
    
    # ===== MODEL ACCURACY =====
    st.subheader("📊 Model Accuracy Scores (R² Score)")
    
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
    
    st.markdown("---")
    
    # ===== BEST MODEL =====
    best_model = engine.get_best_model(accuracy_scores)
    best_accuracy = accuracy_scores[best_model]
    
    st.subheader("🏆 Best Performing Model")
    st.success(f"**{best_model.replace('_', ' ').title()}** with accuracy **{best_accuracy:.4f}**")
    
    st.markdown("---")
    
    # ===== MODEL LEADERBOARD =====
    st.subheader("🏅 Model Leaderboard")
    
    leaderboard_df = pd.DataFrame({
        "Rank": [1, 2, 3],
        "Model": ["Linear Regression", "Random Forest", "Decision Tree"],
        "Accuracy (R²)": [
            accuracy_scores['linear_regression'],
            accuracy_scores['random_forest'],
            accuracy_scores['decision_tree']
        ]
    })
    
    leaderboard_df = leaderboard_df.sort_values("Accuracy (R²)", ascending=False).reset_index(drop=True)
    leaderboard_df["Rank"] = range(1, len(leaderboard_df) + 1)
    
    st.dataframe(leaderboard_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ===== ACCURACY COMPARISON CHART =====
    st.subheader("📈 Accuracy Comparison")
    
    chart_df = pd.DataFrame({
        "Model": ["Linear Regression", "Random Forest", "Decision Tree"],
        "Accuracy": [
            accuracy_scores['linear_regression'],
            accuracy_scores['random_forest'],
            accuracy_scores['decision_tree']
        ]
    })
    
    fig = px.bar(
        chart_df,
        x="Model",
        y="Accuracy",
        color="Accuracy",
        title="ML Model Accuracy Comparison",
        labels={"Accuracy": "R² Score"}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ===== PREDICTION COMPARISON =====
    st.subheader("🎯 Prediction Comparison")
    
    prediction_df = pd.DataFrame({
        "Model": ["Linear Regression", "Random Forest", "Decision Tree"],
        "Prediction": [
            predictions['linear_regression'],
            predictions['random_forest'],
            predictions['decision_tree']
        ],
        "Accuracy": [
            accuracy_scores['linear_regression'],
            accuracy_scores['random_forest'],
            accuracy_scores['decision_tree']
        ]
    })
    
    prediction_df = prediction_df.sort_values("Prediction", ascending=False).reset_index(drop=True)
    
    st.dataframe(prediction_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ===== MODEL INSIGHTS =====
    st.subheader("💡 Model Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Highest Prediction:** ${prediction_df.iloc[0]['Prediction']:,.0f}
        **Model:** {prediction_df.iloc[0]['Model']}
        """)
    
    with col2:
        if best_accuracy > 0.9:
            st.success("✅ **Very High Confidence** - Models are reliable")
        elif best_accuracy > 0.75:
            st.info("ℹ️ **Good Confidence** - Models show strong performance")
        else:
            st.warning("⚠️ **Moderate Confidence** - Consider adding more data")
    
    st.markdown("---")
    
    # ===== DOWNLOAD OPTIONS =====
    st.subheader("📥 Download Results")
    
    # Download predictions
    csv_predictions = prediction_df.to_csv(index=False)
    st.download_button(
        label="📊 Download Predictions CSV",
        data=csv_predictions,
        file_name="ml_predictions.csv",
        mime="text/csv"
    )
    
    # Download leaderboard
    csv_leaderboard = leaderboard_df.to_csv(index=False)
    st.download_button(
        label="🏅 Download Leaderboard CSV",
        data=csv_leaderboard,
        file_name="ml_leaderboard.csv",
        mime="text/csv"
    )