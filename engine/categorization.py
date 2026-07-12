"""
Categorization functions for processing input text and assigning it to predefined categories.
"""
from sentence_transformers import SentenceTransformer, util
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
        "payment from": "transfer"
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