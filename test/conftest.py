"""
This module contains pytest fixtures for testing purposes. 
The fixtures provide sample data and setup for tests, allowing for consistent and reusable test environments.
"""
import pandas as pd
import pytest

@pytest.fixture
def raw_revolut_csv(tmp_path: pytest.TempPathFactory) -> str:
    """
    Create a temporary CSV file with sample financial data for testing purposes.
    Parameters:
        tmp_path (pytest.TempPathFactory): A pytest fixture that provides a temporary directory unique to the test invocation.
    Returns:
        path (str): The path to the temporary CSV file containing the sample financial data.
    """
    data = {
        'Type': ['TRANSFER', 'CARD_PAYMENT'],
        'Product': ['Current', 'Current'],
        'Started Date': ['2024-01-01 10:00:00', '2024-01-01 15:00:00'],
        'Completed Date': ['2024-01-01 10:01:00', '2024-01-01 15:01:00'],
        'Description': ['Test 1', 'Test 2'],
        'Amount': [100.0, -20.0],
        'Fee': [0.0, 0.0],
        'Currency': ['EUR', 'EUR'],
        'State': ['COMPLETED', 'COMPLETED'],
        'Balance': [1100.0, 1080.0],
    }
    df = pd.DataFrame(data)
    path = tmp_path / "sample.csv"
    df.to_csv(path, index=False)
    return path