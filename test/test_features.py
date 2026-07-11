"""
Unit tests for the build_features function (features.py).
"""
from model.features import build_features
import pandas as pd

def test_build_features(cleaned_df: pd.DataFrame) -> None:
    """
    Test the `build_features` function to ensure it correctly builds features from the cleaned DataFrame.
    Parameters:
        cleaned_df (pd.DataFrame): A cleaned DataFrame containing financial data.
    """
    df_features = build_features(cleaned_df)

    assert len(df_features) == 10
    assert df_features['Date'].iloc[0] == pd.Timestamp('2024-01-31')
    assert df_features['Balance_lag_30'].iloc[0] == 1000.0
    assert df_features['Balance_lag_7'].iloc[0] == 1023.0
    assert df_features['Rolling_mean_30'].iloc[0] == 1015.5
    assert df_features['Day'].iloc[0] == 31
    assert df_features['Weekday'].iloc[0] == 2
    assert df_features['Month'].iloc[0] == 1
    assert df_features['Days_since_start'].iloc[0] == 30