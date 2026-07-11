"""
This module contains unit tests for the `preprocessing.py` module, specifically testing the `load_and_clean_data` function. 
The tests ensure that the function correctly loads and cleans financial data from a CSV file, verifying that the resulting DataFrame has the expected structure and content.
"""
from model.preprocessing import load_and_clean_data
import pandas as pd
import pytest

def test_load_and_clean_data(raw_revolut_csv: str) -> None:
    """
    Test the `load_and_clean_data` function to ensure it correctly loads and cleans the financial data.
    Parameters:
        raw_revolut_csv (str): The path to the temporary CSV file containing sample financial data.
    """

    df = load_and_clean_data(raw_revolut_csv)

    expected_columns = {'Date', 'Balance'}
    assert set(df.columns) == expected_columns
    assert 81,0 not in df['Balance'].values
    assert df['Date'].is_unique
