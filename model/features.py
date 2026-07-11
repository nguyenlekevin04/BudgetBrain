"""
This module contains functions for building additional features from the cleaned financial data.
"""
import pandas as pd

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build additional features from the cleaned financial data DataFrame. 
    This function adds new columns for the day of the month, weekday, month, and the number of days since the start of the dataset.
    Parameters:
        df (pd.DataFrame): The cleaned DataFrame containing financial data.
    Returns:
        df (pd.DataFrame): A DataFrame with additional features added.
    """
    df = df.copy()
    df['Day'] = df['Date'].dt.day
    df['Weekday'] = df['Date'].dt.weekday
    df['Month'] = df['Date'].dt.month
    df['Days_since_start'] = (df['Date'] - df['Date'].min()).dt.days

    df['Balance_lag_7'] = df['Balance'].shift(7)
    df['Balance_lag_30'] = df['Balance'].shift(30)
    df['Rolling_mean_30'] = df['Balance'].rolling(window=30).mean()

    df = df.dropna().reset_index(drop=True)
    return df

