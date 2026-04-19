# Urdu Readability Checker

A complete project for analyzing Urdu text readability and determining suitable grade level (1–12) for children's books and educational materials.

## Features

- **Urdu text analysis** – Enter Urdu text and get instant readability grade
- **Fry-based grading** – Calibrated to Urdu dataset (Grade 1 = easiest, Grade 12 = hardest)
- **Linear regression model** – Trained on 243K+ Urdu sentences
- **Web interface** – Clean, modern UI with Import, Paste, Sample text

## Quick Start

```bash
cd /home/taskeen/Desktop/check
.venv/bin/python run_app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Project Structure

| File | Purpose |
|------|---------|
| `run_app.py` | Start the web app |
| `app.py` | Flask backend + API |
| `index.html` | Web UI |
| `urdu_features.py` | Feature extraction + Fry grading |
| `urdu_readability_model.joblib` | Trained linear regression model |
| `run_linear_regression.py` | Train model + generate Fry diagram |
| `fry_graph.py` | Generate Fry readability diagram |
| `FRY_FORMULAE.md` | Formulae for X-axis and Y-axis |

## How Grading Works

- **Grade 1** = Easiest (young readers)
- **Grade 12** = Hardest (college level)

Uses Fry formula: syllables per 100 words + sentences per 100 words, calibrated to Urdu dataset.

## First-Time Setup

```bash
python3 -m venv .venv
.venv/bin/pip install flask scikit-learn joblib numpy pandas openpyxl matplotlib
.venv/bin/python run_linear_regression.py   # Creates model
.venv/bin/python run_app.py
```
