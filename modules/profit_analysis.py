import pandas as pd

def total_profit(df):
    return df["Profit"].sum()

def most_profitable_product(df):
    return df.loc[df["Profit"].idxmax(), "Product"]

def least_profitable_product(df):
    return df.loc[df["Profit"].idxmin(), "Product"]

def highest_revenue_product(df):
    return df.loc[df["Revenue"].idxmax(), "Product"]