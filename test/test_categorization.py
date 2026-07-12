"""
Unit tests for the transform_input and categorize_input functions (categorization.py).
"""
from engine.categorization import transform_input, categorize_input

def test_transform_input() -> None:
    """
    Test the `transform_input` function to ensure it correctly transforms input text into predefined categories based on specific keywords.
    """
    assert transform_input("JET") == "fuel"
    assert transform_input("jet") == "fuel"
    assert transform_input("Unknown Shop") == None

def test_categorize_input() -> None:
    """
    Test the `categorize_input` function to ensure it correctly categorizes input text into predefined categories.
    """
    assert categorize_input("JET") == "fuel"
    assert categorize_input("Unknown Shop") != None