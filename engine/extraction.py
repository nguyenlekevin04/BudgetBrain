"""
Extraction module for extracting saving goal information from user input using the OpenAI API.
"""
from pydantic import BaseModel, Field
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

class SavingGoal(BaseModel):
    """
    A Pydantic model representing a saving goal with a date and amount.
    Attributes:
        target_date (date): The date of the saving goal in YYYY-MM-DD format.
        target_amount (float): The amount of the saving goal.
    """
    target_date: date = Field(..., description="The date of the saving goal in YYYY-MM-DD format.")
    target_amount: float = Field(..., description="The amount of the saving goal.")

def extract_saving_goal(user_input: str) -> SavingGoal:
    """
    Extracts the saving goal information from the user input using the OpenAI API and returns a SavingGoal object.
    Parameters:
        user_input (str): The user input containing the saving goal information.
    Returns:
        SavingGoal: An instance of the SavingGoal model containing the extracted target date and amount.
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
                "content": "You are a helpful assistant that extracts saving goal information from user input."
             },
            {
                "role": "user",
                "content": user_input
            }
        ],   
        response_format=SavingGoal
        )
    return client_call.choices[0].message.parsed