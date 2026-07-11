"""
This module defines a Pydantic model for representing a saving goal, which includes a target date and a target amount. 
The model ensures that the data adheres to the specified types and formats, providing validation and serialization capabilities.
"""
from pydantic import BaseModel, Field
from datetime import date

class SavingGoal(BaseModel):
    """
    A Pydantic model representing a saving goal with a date and amount.
    Attributes:
        target_date (date): The date of the saving goal in YYYY-MM-DD format.
        target_amount (float): The amount of the saving goal.
    """
    target_date: date = Field(..., description="The date of the saving goal in YYYY-MM-DD format.")
    target_amount: float = Field(..., description="The amount of the saving goal.")