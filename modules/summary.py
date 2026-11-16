def generate_summary(df):

    total_products = len(df)

    total_revenue = df["Revenue"].sum()

    total_profit = df["Profit"].sum()

    best_product = df.loc[
        df["Revenue"].idxmax(),
        "Product"
    ]

    print("\n===== EXECUTIVE SUMMARY =====")

    print(
        f"The dataset contains {total_products} products."
    )

    print(
        f"Total revenue is {total_revenue}."
    )

    print(
        f"Total profit is {total_profit}."
    )

    print(
        f"{best_product} generated the highest revenue."
    )