"""
Unit tests for the load_and_clean_data function (preprocessing.py).
"""
from model.preprocessing import load_and_clean_data
from pathlib import Path
import pandas as pd

def test_load_and_clean_data(raw_revolut_csv: Path) -> None:
    """
    Test the `load_and_clean_data` function to ensure it correctly loads and cleans the financial data.
    Parameters:
        raw_revolut_csv (Path): The path to the temporary CSV file containing sample financial data.
    """

    df = load_and_clean_data(raw_revolut_csv)

    expected_columns = {'Date', 'Balance'}
    assert set(df.columns) == expected_columns
    assert 81.0 not in df['Balance'].values
    assert df['Date'].is_unique

def test_load_and_clean_data_fills_columns(raw_revolut_csv_gap: Path) -> None:
    """
    Test the `load_and_clean_data` function to ensure it raises a ValueError when required columns are missing from the input CSV file.
    Parameters:
        raw_revolut_csv_gap (Path): The path to the temporary CSV file containing sample financial data with a date gap.
    """
    df = load_and_clean_data(raw_revolut_csv_gap)

    assert len(df) == 4
    filled_rows = df[df['Date'] == pd.Timestamp('2024-01-02')]
    assert filled_rows['Balance'].values[0] == 1100.0
