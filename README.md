# BudgetBrain

![CI](https://github.com/nguyenlekevin04/BudgetBrain/actions/workflows/ci.yml/badge.svg)

BudgetBrain answers natural-language questions like *"Can I afford a €800 bike by December?"* by combining an LLM for language understanding with a deterministic engine for the actual math. The LLM never calculates — it only extracts parameters and explains results, so every number shown to the user traces back to one calculation, not a hallucination.

## Quickstart

### Requirements
- Python 3.11
- A GitHub account (for GitHub Models Inference API access)

### Setup
```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GITHUB_TOKEN=your_github_personal_access_token
```

### Run the app
```bash
streamlit run app/main.py
```

### Run the tests
```bash
pytest -v
```

## Architecture

BudgetBrain is built around a four-stage pipeline:

```
User question → Extraction (LLM) → Categorization + Calculation (deterministic) → Response (LLM)
```

1. **Extraction** — an LLM parses the user's question into a structured `SavingGoal` (target amount, target date), using strict schema validation (Pydantic + OpenAI structured outputs) so the model can't return malformed data.
2. **Categorization** — historical transactions are grouped into spending categories (fuel, groceries, insurance, etc.) using a two-stage approach: a keyword dictionary handles known merchants directly, and a zero-shot embedding classifier (sentence-transformers + cosine similarity) handles anything unrecognized.
3. **Calculation** — a plain Python function computes the required monthly savings rate from the user's current balance, the target amount, and the time remaining. No LLM involved.
4. **Response** — an LLM turns the calculated numbers into a plain-language explanation. It is given the final numbers as facts and instructed not to invent or recompute anything.

## Components

- `model/preprocessing.py` — loads and cleans raw Revolut CSV exports (duplicate handling, date-gap filling, reverted-transaction filtering)
- `model/features.py` — builds calendar and lag-based features (7/30-day balance history, rolling averages)
- `model/train.py` — trains and evaluates a baseline balance-forecasting model
- `engine/extraction.py` — LLM-based parameter extraction from natural language
- `engine/categorization.py` — transaction categorization (keyword lookup + zero-shot embeddings)
- `engine/calculation.py` — deterministic savings-rate calculation
- `engine/response.py` — LLM-based explanation generation
- `app/main.py` — Streamlit interface tying the pipeline together

## Limitations / possible future improvements

- **Small transaction history** — the underlying balance-forecasting model is trained on roughly two years of personal data; both accuracy figures above should be read as illustrative, not production-grade
- **Category set is hand-curated** — new merchant types require either a keyword-dictionary update or reliance on the (less reliable) embedding fallback
- **No persistent data pipeline** — the app reads a static CSV export rather than a live-updating source
- **Single-user, single-currency** — built around one personal Revolut export, not designed for multi-user or multi-currency use

## Tests

Tests are written with `pytest` and run automatically via GitHub Actions on every push.

```bash
pytest -v
```

Coverage includes:
- data cleaning and date-gap handling (`preprocessing.py`)
- feature engineering, including lag features (`features.py`)
- target creation and chronological train/test splitting (`train.py`)
- savings-rate calculation, including edge cases (past target dates, already-met goals) (`calculation.py`)
- transaction categorization (`categorization.py`)