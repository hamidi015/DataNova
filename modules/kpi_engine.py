def calculate_kpis(df):

    print("\n===== KPI REPORT =====")

    total_revenue = df["Revenue"].sum()
    total_profit = df["Profit"].sum()
    average_revenue = df["Revenue"].mean()

    best_revenue_product = df.loc[
        df["Revenue"].idxmax(),
        "Product"
    ]

    best_profit_product = df.loc[
        df["Profit"].idxmax(),
        "Product"
    ]

    print(f"Total Revenue: {total_revenue}")

    print(f"Total Profit: {total_profit}")

    print(f"Average Revenue: {average_revenue}")

    print(
        f"Highest Revenue Product: {best_revenue_product}"
    )

    print(
        f"Highest Profit Product: {best_profit_product}"
    )