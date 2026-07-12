"""
Categorization functions for processing input text and assigning it to predefined categories.
"""
from sentence_transformers import SentenceTransformer, util
from model.preprocessing import load_and_clean_data
import pandas as pd
import mlflow

model = SentenceTransformer('all-MiniLM-L6-v2')
CATEGORIES = ["fuel", "insurance", "maintenance","groceries", "government fees", "parking", "transfer"]

def transform_input(input_text: str) -> str:
    """
    Transform the input text into a predefined category based on specific keywords.
    Parameters:
        input_text (str): The input text to be transformed.
    Returns:
        str: The corresponding category if a keyword match is found; otherwise, None.
    """
    keyword_map = {
        "jet": "fuel",
        "star": "fuel",
        "hem": "fuel",
        "aral": "fuel",
        "totalenergies": "fuel",
        "allianz": "insurance",
        "tüv": "maintenance",
        "autodoc": "maintenance",
        "reifen": "maintenance",
        "norma": "groceries",
        "ordnungsamt": "government fees",
        "bundeskasse": "government fees",
        "payment from": "transfer",
        "kaufland": "groceries",
    }
    for keyword in keyword_map:
        if keyword in input_text.lower():
            return keyword_map[keyword]
    return None

def categorize_input(input_text: str) -> str:
    """
    Categorize the input text into one of the predefined categories using cosine similarity and keyword mapping.
    Parameters:
        input_text (str): The input text to be categorized.
    Returns:
        str: The predicted category based on cosine similarity or keyword mapping.
    """
    transformed_text = transform_input(input_text)
    if transformed_text:
        return transformed_text
    else:
        embeddings_categories = model.encode(CATEGORIES, convert_to_tensor=True)
        embedding_input = model.encode(input_text, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embedding_input, embeddings_categories)
        predicted_category = CATEGORIES[cosine_scores.argmax()]
        return predicted_category
    
def categorize_data(df: pd.DataFrame, column_name: str = "Description") -> pd.DataFrame:
    """
    Categorize the input text in a DataFrame column into predefined categories using the `categorize_input` function.
    Parameters:
        df (pd.DataFrame): The DataFrame containing the input text to be categorized.
        column_name (str): The name of the column in the DataFrame that contains the input text.
    Returns:
        pd.DataFrame: A new DataFrame with an additional 'Category' column containing the predicted categories.
    """
    return df.assign(Category=df[column_name].apply(categorize_input))

def aggregate_by_category(df: pd.DataFrame) -> pd.Series:
    """
    Aggregate the input DataFrame by the 'Category' column and calculate the sum of the 'Amount' column for each category.
    Parameters:
        df (pd.DataFrame): The DataFrame containing the 'Category' and 'Amount' columns.
    Returns:
        pd.Series: A new Series with the sum of 'Amount' for each category.
    """
    return df.groupby('Category')['Amount'].sum().abs()