#!/bin/bash
# Urdu Readability Checker - Start script for presentation
cd "$(dirname "$0")"

if [ ! -f "urdu_readability_model.joblib" ]; then
    echo "Model not found. Running training..."
    .venv/bin/python run_linear_regression.py
fi

echo "Starting Urdu Readability Checker..."
echo "Open: http://127.0.0.1:5000"
echo ""
.venv/bin/python run_app.py
