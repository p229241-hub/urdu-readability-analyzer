# Run Urdu Readability Checker

## Quick Start

```bash
cd Desktop/check
.venv/bin/python run_app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## First Time? Create model & venv

```bash
cd Desktop/check
python3 -m venv .venv
.venv/bin/pip install flask scikit-learn joblib numpy
.venv/bin/python run_linear_regression.py   # Creates urdu_readability_model.joblib
.venv/bin/python run_app.py
```

## What it does

- **Front-end:** Enter Urdu text → Click "Analyze Readability"
- **Backend:** Extracts features → Runs linear regression model → Returns grade (1–12)
- **Result:** "This text is suitable for Grade X readers"
