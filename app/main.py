"""
main.py

Streamlit interface for BudgetBrain. Ties together the full pipeline:
user question -> LLM extraction -> categorization -> deterministic calculation
-> LLM explanation.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st

from model.preprocessing import load_and_clean_data
from engine.extraction import extract_saving_goal
from engine.categorization import categorize_data, aggregate_by_category
from engine.calculation import calculate_savings_rate
from engine.response import generate_response

RAW_DATA_PATH = "data/raw/financial_data_raw.csv"


def get_current_balance(df) -> float:
    """
    Return the most recent balance value from a cleaned transactions DataFrame.
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame containing a 'Balance' column,
            sorted chronologically by 'Date'.
    Returns:
        float: The last known balance.
    """
    return float(df["Balance"].iloc[-1])


def get_main_expense_category(df) -> str:
    """
    Categorize transactions and return the category with the highest total spend.
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame with a 'Description' column.
    Returns:
        str: The name of the category with the highest aggregated amount.
    """
    categorized_df = categorize_data(df, "Description")
    category_sums = aggregate_by_category(categorized_df)
    category_sums = category_sums.drop("transfer", errors="ignore")
    return category_sums.idxmax()


st.set_page_config(page_title="BudgetBrain", page_icon="💰")
st.title("💰 BudgetBrain")
st.caption("Ask if you can afford something, and get a grounded, data-backed answer.")

user_input = st.text_input(
    "Ask your question",
    placeholder="Can I afford a 800€ bike by December 2026?",
)

if st.button("Ask BudgetBrain", type="primary") and user_input:
    with st.spinner("Reading your transaction history..."):
        df_for_balance = load_and_clean_data(RAW_DATA_PATH)
        df_for_categories = load_and_clean_data(
            RAW_DATA_PATH, keep_description=True, fill_gaps=False, keep_amount=True
        )
        current_balance = get_current_balance(df_for_balance)
        main_category = get_main_expense_category(df_for_categories)

    with st.spinner("Understanding your question..."):
        goal = extract_saving_goal(user_input)

    try:
        savings_rate = calculate_savings_rate(current_balance, goal)
    except ValueError as e:
        st.error(str(e))
        st.stop()

    with st.spinner("Preparing your answer..."):
        advice = generate_response(goal, savings_rate, main_category)

    st.divider()

    if advice.is_achievable:
        st.success("This goal looks achievable!")
    else:
        st.warning("This goal may be tough to reach as things stand. ⚠️")

    col1, col2 = st.columns(2)
    col1.metric("Required monthly savings", f"{savings_rate:.2f} €")
    col2.metric("Top expense category", main_category)

    st.write(advice.explanation.replace("$", "\\$"))

    with st.expander("See the numbers behind this answer"):
        st.write(f"**Current balance:** {current_balance:.2f} €")
        st.write(f"**Target amount:** {goal.target_amount:.2f} €")
        st.write(f"**Target date:** {goal.target_date}")