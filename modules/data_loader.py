import pandas as pd


def load_csv(file_path):
    """
    Load a CSV file.
    """
    return pd.read_csv(file_path)


def load_excel(file_path):
    """
    Load an Excel file.
    """
    return pd.read_excel(file_path)
