"""
This module contains unit tests for the `train.py` module, specifically testing the `create_target` and `train_test_split_by_time` functions. 
The tests ensure that the target column is correctly created and that the data is split into training and testing sets based on chronological order.
"""
import pandas as pd
from model.train import create_target, train_test_split_by_time

def test_create_target(balance_df: pd.DataFrame) -> None:
    """
    Test the `create_target` function to ensure it correctly adds a target column representing the balance `horizon_days` in the future.
    Parameters:
        balance_df (pd.DataFrame): A DataFrame containing a 'Balance' column for testing
        horizon_days (int): The number of days ahead for which to predict the balance.
    """
    horizon_days = 3
    target_df = create_target(balance_df, horizon_days)

    assert target_df['Target'].iloc[0] == 1030.0
    assert len(target_df) == len(balance_df) - horizon_days

def test_train_test_split_by_time(balance_df: pd.DataFrame) -> None:
    """
    Test the `train_test_split_by_time` function to ensure it correctly splits the DataFrame into training and testing sets based on chronological order.
    Parameters:
        balance_df (pd.DataFrame): A DataFrame containing a 'Date' column for testing
    """
    train_df, test_df = train_test_split_by_time(balance_df, test_ratio=0.2)

    assert len(train_df) == 8
    assert len(test_df) == 2
    assert train_df['Date'].max() < test_df['Date'].min()
