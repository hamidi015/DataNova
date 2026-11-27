import pandas as pd


def best_campaign(df):
    if "Campaign" in df.columns and "Revenue" in df.columns:
        return df.groupby("Campaign")["Revenue"].sum().idxmax()
    return "N/A"


def worst_campaign(df):
    if "Campaign" in df.columns and "Revenue" in df.columns:
        return df.groupby("Campaign")["Revenue"].sum().idxmin()
    return "N/A"


def campaign_leaderboard(df):
    if "Campaign" in df.columns and "Revenue" in df.columns:

        leaderboard = (
            df.groupby("Campaign")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        return leaderboard

    return pd.DataFrame()