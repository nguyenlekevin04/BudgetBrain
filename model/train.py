"""
Trains a baseline regression model to predict account balance N days ahead,
using calendar-based features from features.py.
"""
from pathlib import Path
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from preprocessing import load_and_clean_data, write_cleaned_data
from features import build_features

def create_target(df: pd.DataFrame, horizon_days: int) -> pd.DataFrame:
    """
    Add a target column representing the balance `horizon_days` in the future.
    Rows without a future value (end of dataset) are dropped.
    Parameters:
        df (pd.DataFrame): The input DataFrame containing financial data.
        horizon_days (int): The number of days ahead for which to predict the balance.
    Returns:
        pd.DataFrame: A DataFrame with the target column added and rows without a future value
    """
    df = df.copy()
    df['Target'] = df['Balance'].shift(-horizon_days)
    df = df.dropna(subset=['Target'])
    return df

def train_test_split_by_time(df: pd.DataFrame, test_ratio: float = 0.2):
    """
    Split chronologically: first (1 - test_ratio) rows = train, rest = test.
    Parameters:
        df (pd.DataFrame): The input DataFrame containing financial data.
        test_ratio (float): The ratio of the dataset to include in the test split.
    Returns:
        tuple: A tuple containing the training and testing DataFrames.
    """
    split_idx = int(len(df) * (1 - test_ratio))
    return df.iloc[:split_idx], df.iloc[split_idx:]

def train_model(train_df: pd.DataFrame, test_df: pd.DataFrame, features: list[str]) -> tuple[LinearRegression, float]:
    """
    Train a random forest regression model using the specified features and evaluate it on the test set.
    Parameters:
        train_df (pd.DataFrame): The training DataFrame containing financial data.
        test_df (pd.DataFrame): The testing DataFrame containing financial data.
        features (list[str]): A list of feature column names to use for training.
    Returns:
        tuple[RandomForestRegressor, float]: A tuple containing the trained model and the mean absolute error on the test set.
    """
    X_train = train_df[features]
    y_train = train_df['Target']

    X_test = test_df[features]
    y_test = test_df['Target']

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    return (model, mae)

if __name__ == "__main__":
    raw_data_path = Path("data/raw/financial_data_raw.csv")
    cleaned_data_path = Path("data/cleaned/revolut_transactions.csv")
    df = load_and_clean_data(raw_data_path)
    write_cleaned_data(df, cleaned_data_path)

    df_features = build_features(df)

    horizon_days = 7
    df_with_target = create_target(df_features, horizon_days)

    train_df, test_df = train_test_split_by_time(df_with_target)

    feature_cols = ['Day', 'Weekday', 'Month', 'Days_since_start', 'Balance_lag_7', 'Balance_lag_30', 'Rolling_mean_30']

    model, mae = train_model(train_df, test_df, feature_cols)
    print(f"Mean Absolute Error on test set: {mae:.2f}")
    print(len(train_df), "rows in training set,", len(test_df), "rows in test set.")