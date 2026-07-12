"""
Preprocesses financial data by loading it from a CSV file, cleaning it, and preparing it for further analysis or modeling.
"""
from pathlib import Path
import pandas as pd

def load_and_clean_data(file_path: str, keep_description: bool = False, fill_gaps: bool = True, keep_amount: bool = False) -> pd.DataFrame:
    """
    Load the financial data from a CSV file, clean it by removing unnecessary columns, filtering out reverted transactions, and handling duplicate dates. 
    Parameters: 
        file_path (str): The path to the CSV file containing the financial data.
        keep_description (bool): Whether to keep the description column in the cleaned DataFrame.
        fill_gaps (bool): Whether to fill gaps in the date index by forward-filling the last known balance.
        keep_amount (bool): Whether to keep the amount column in the cleaned DataFrame.
    Returns:
        df (pd.DataFrame): A cleaned DataFrame with the relevant financial data.
    """
    df = pd.read_csv(file_path)

    required_columns = {'Type', 'Product', 'Started Date', 'Completed Date', 'Description', 'Amount', 'Fee', 'Currency', 'State', 'Balance'}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df.drop(['Type', 'Product', 'Completed Date'], axis=1)
    df['Date'] = pd.to_datetime(df['Started Date']).dt.normalize()
    df = df.drop('Started Date', axis=1)
    df = df[df['State'] != 'REVERTED']
    if not keep_description:
        df = df.drop(['Description'], axis=1)
    if not keep_amount:
        df = df.drop(['Amount'], axis=1)

    df = df.drop(['State', 'Currency', 'Fee'], axis=1)

    if df['Date'].duplicated().sum() > 0:
        df = df.groupby('Date').last().reset_index()
    
    if fill_gaps:
        df = df.set_index('Date').asfreq('D').ffill().reset_index()
    return df

def write_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Write the cleaned DataFrame to a CSV file.
    Parameters:
        df (pd.DataFrame): The cleaned DataFrame to be written to a CSV file.
        output_path (str): The path where the cleaned CSV file will be saved.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)