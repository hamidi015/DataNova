def generate_recommendation(df):

    if "Revenue" not in df.columns:
        return "No revenue data available."

    if "Profit" not in df.columns:
        return "No profit data available."

    revenue = df["Revenue"].sum()
    profit = df["Profit"].sum()

    margin = (profit / revenue) * 100

    if margin >= 30:
        return "Excellent profitability. Consider expanding operations."

    elif margin >= 15:
        return "Business performance is healthy. Continue current strategy."

    else:
        return "Profit margin is low. Review costs and pricing."