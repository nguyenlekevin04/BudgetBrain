"""
This module contains functions to evaluate the accuracy of a categorization model using cosine similarity.
"""
import mlflow
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
    
def evaluate_categorization(test_cases: list[tuple[str, str]], categories: list[str]) -> float:
    """
    Evaluate the accuracy of the categorization model using cosine similarity.
    Parameters:
        test_cases (list[tuple[str, str]]): A list of tuples containing input text and expected category.
        categories (list[str]): A list of predefined categories for categorization.
    Returns:
        float: The accuracy of the categorization model as a percentage.
    """
    counter = 0
    embeddings_categories = model.encode(categories, convert_to_tensor=True)

    for input_text, expected_category in test_cases:
        embedding_input = model.encode(input_text, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embedding_input, embeddings_categories)
        predicted_category = categories[cosine_scores.argmax()]

        if predicted_category == expected_category:
            counter += 1
    
    return counter / len(test_cases)

def choose_category(option: int):
    """
    Choose a predefined list of categories based on the provided option.
    Parameters:
        option (int): An integer representing the choice of category set.
    Returns:
        list[str]: A list of predefined categories corresponding to the chosen option.
    """
    match option:
        case 1:
            return ["fuel", "insurance", "maintenance","groceries", "government fees", "parking", "transfer"]
        case 2:
            return ["sprit", "versicherung", "instandhaltung","lebensmittel", "Gebühren", "Parken", "Überweisung"]

def choose_test_cases(option: int):
    """
    Choose a predefined list of test cases based on the provided option.
    Parameters:
        option (int): An integer representing the choice of test case set.
    Returns:
        list[tuple[str, str]]: A list of tuples containing input text and expected category corresponding to the chosen option.
    """
    match option:
        case 1:
            return [
                ("JET", "fuel"),
                ("Ordnungsamt Dresden", "government fees"),
                ("NORMA", "groceries"),
                ("Allianz insurance", "insurance"),
                ("Payment from KEVIN LE NGUYEN", "transfer"),
                ("STAR", "fuel"),
                ("HEM", "fuel"),
                ("To Bundeskasse DO Halle", "government fees"),
                ("Aral", "fuel"),
                ("TÜV", "maintenance"),
                ("autodoc.de", "maintenance"),
                ("reifen.com", "maintenance"),
            ]
        case 2:
            return [
                ("JET", "sprit"),
                ("Ordnungsamt Dresden fee", "Gebühren"),
                ("NORMA grocery store", "lebensmittel"),
                ("Allianz insurance", "versicherung"),
                ("Payment from KEVIN LE NGUYEN", "Überweisung"),
                ("STAR Tankstelle", "sprit"),
                ("HEM Tankstelle", "sprit"),
                ("To Bundeskasse DO Halle", "Gebühren"),
                ("Aral Tankstelle", "sprit"),
                ("TÜV inspection", "instandhaltung"),
                ("autodoc.de", "instandhaltung"),
                ("reifen.com", "instandhaltung"),
            ]
        case 3:
            return [
                ("JET gas station", "fuel"),
                ("Ordnungsamt Dresden fee", "government fees"),
                ("NORMA grocery store", "groceries"),
                ("Allianz insurance", "insurance"),
                ("Payment from KEVIN LE NGUYEN", "transfer"),
                ("STAR gas station", "fuel"),
                ("HEM gas station", "fuel"),
                ("To Bundeskasse DO Halle", "government fees"),
                ("Aral gas station", "fuel"),
                ("TÜV car inspection", "maintenance"),
                ("autodoc.de", "maintenance"),
                ("reifen.com", "maintenance"),
            ]
        
def log_accuracy_to_mlflow() -> None:
    """
    Log the accuracy of different categorization configurations to MLflow for tracking and comparison.
    This function evaluates the accuracy of various categorization configurations and logs the results to MLflow.
    """
    cat_v1 = choose_category(1)
    cat_v2 = choose_category(2)
    test_cases_v1 = choose_test_cases(1)
    test_cases_v2 = choose_test_cases(2)
    test_cases_v3 = choose_test_cases(3)

    config = [
        {"option": 1, "categories": cat_v1, "test_cases": test_cases_v1},
        {"option": 2, "categories": cat_v2, "test_cases": test_cases_v1},
        {"option": 3, "categories": cat_v1, "test_cases": test_cases_v2},
        {"option": 4, "categories": cat_v2, "test_cases": test_cases_v2},
        {"option": 5, "categories": cat_v1, "test_cases": test_cases_v3},
        {"option": 6, "categories": cat_v2, "test_cases": test_cases_v3},
    ]

    for cfg in config:
        with mlflow.start_run():
            mlflow.log_param("option", cfg["option"])
            mlflow.log_param("categories", cfg["categories"])
            mlflow.log_param("test_cases", cfg["test_cases"])

            accuracy = evaluate_categorization(cfg["test_cases"], cfg["categories"])
            mlflow.log_metric("accuracy", accuracy)
