from engine.extraction import SavingGoal
from engine.categorization import categorize_data, aggregate_by_category
from pydantic import BaseModel, Field
from openai import OpenAI
from datetime import date
import os

class SavingsAdvice(BaseModel):
    """
    A Pydantic model representing savings advice based on the user's financial data.
    Attributes:
        is_achievable (bool): Indicates whether the savings goal is achievable based on the user's financial data.
        explanation (str): A detailed explanation of the savings advice provided to the user.
        main_expense_category (str): The main expense category identified from the user's financial data.
    """
    is_achievable: bool = Field(..., description="Indicates whether the savings goal is achievable based on the user's financial data.")
    explanation: str = Field(..., description="A detailed explanation of the savings advice provided to the user.")
    main_expense_category: str = Field(..., description="The main expense category identified from the user's financial data.")

def generate_response(goal: SavingGoal, savings_rate: float, category: str) -> SavingsAdvice:
    """
    Generate a response containing savings advice based on the user's financial data and savings goal.
    Parameters:
        goal (SavingGoal): An instance of the SavingGoal model containing the target date and amount.
        savings_rate (float): The required monthly savings rate to reach the specified saving goal.
        category (str): The main expense category identified from the user's financial data.
    Returns:
        SavingsAdvice: An instance of the SavingsAdvice model containing the generated savings advice.
    """
    time_remaining = (goal.target_date - date.today()).days / 30.0
    is_achievable = savings_rate * time_remaining >= (goal.target_amount)

    context = f"""
    Target amount: {goal.target_amount}
    Target date: {goal.target_date}
    Required monthly savings rate: {savings_rate:.2f}
    Is the goal achievable: {is_achievable}
    Main expense category: {category}
    """

    client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=os.getenv("GITHUB_TOKEN")
        )
        
    client_call = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful financial assistant. "
                    "You are given precomputed facts about a user's savings goal. "
                    "Explain these facts to the user in plain language. "
                    "Do NOT invent or recalculate any numbers — only use the values given to you."
                )

            },
            {
                "role": "user",
                "content": context
            }
        ],   
        response_format=SavingsAdvice
        )
    return client_call.choices[0].message.parsed

goal = SavingGoal(target_date=date(2026, 12, 31), target_amount=1000.0)

generated_response = generate_response(goal, savings_rate=50.0, category="groceries")
print(generated_response)