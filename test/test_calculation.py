"""
Unit test for the calculation functions (calculation.py).
"""
from engine.calculation import calculate_savings_rate, get_current_balance
from engine.extraction import SavingGoal
import pytest

def test_calculate_savings_rate(saving_goal: SavingGoal, current_balance: float) -> None:
    """
    Test the `calculate_savings_rate` function to ensure it correctly calculates the required monthly savings rate to reach a specified saving goal by a target date.
    Parameters:
        saving_goal (SavingGoal): An instance of the SavingGoal model containing the target date and amount.
        current_balance (float): The current balance of the user.
    """
    savings_rate = calculate_savings_rate(current_balance, saving_goal)
    expected_months = 50 / 30.0
    expected_rate = (1000.0 - 500.0) / expected_months
    
    assert savings_rate == pytest.approx(expected_rate)