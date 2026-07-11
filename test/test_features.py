"""
This module contains tests for the feature engineering functions in the `features.py` module. 
The tests ensure that the feature building process works correctly and produces the expected output.
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

    assert df_features['Day'].iloc[0] == 1
    assert df_features['Weekday'].iloc[0] == 0
    assert df_features['Month'].iloc[0] == 1
    assert df_features['Days_since_start'].iloc[0] == 0
    assert df_features['Days_since_start'].iloc[-1] == 45