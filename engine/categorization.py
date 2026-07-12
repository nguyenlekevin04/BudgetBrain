from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

CATEGORIES = ["fuel", "insurance", "maintenance","groceries", "government fees", "parking", "transfer"]

test_cases = [
    ("JET", "fuel"),
    ("Ordnungsamt Dresden fee", "government fees"),
    ("NORMA grocery store", "groceries"),
    ("Allianz insurance", "insurance"),
    ("Payment from KEVIN LE NGUYEN", "transfer"),
    ("STAR Tankstelle", "fuel"),
    ("HEM Tankstelle", "fuel"),
    ("To Bundeskasse DO Halle", "government fees"),
    ("Aral Tankstelle", "fuel"),
    ("TÜV inspection", "maintenance"),
    ("autodoc.de", "maintenance"),
    ("reifen.com", "maintenance"),
]

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

        print(f"Input: {input_text} | Predicted: {predicted_category} | Expected: {expected_category}")

        if predicted_category == expected_category:
            counter += 1
    
    return counter / len(test_cases)

accuracy = evaluate_categorization(test_cases, CATEGORIES)
print(f"Accuracy: {accuracy:.2%}")