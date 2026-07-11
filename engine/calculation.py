"""
This module contains the `calculate_savings_rate` function, which calculates the required monthly savings rate to reach a specified saving goal by a target date. 
It takes into account the current balance and the target amount, and raises exceptions for invalid inputs.
"""
from engine.extraction import SavingGoal
from datetime import date

def calculate_savings_rate(current_balance: float, goal: SavingGoal) -> float:
    """
    Calculate the required monthly savings rate to reach a specified saving goal by a target date.
    Parameters:
        current_balance (float): The current balance of the user.
        goal (SavingGoal): An instance of the SavingGoal model containing the target date and amount.
    Exceptions:
        ValueError: If the target date is in the past.
    Returns:
        float: The required monthly savings rate to reach the goal. If the goal is already met, returns 0.0.
    """
    target_amount = goal.target_amount
    missing_amount = target_amount - current_balance
    remaining_months = (goal.target_date - date.today()).days / 30.0

    if remaining_months <= 0:
        raise ValueError("The target date must be in the future.")
    
    if missing_amount <= 0:
        return 0.0
    else:
        return missing_amount / remaining_months