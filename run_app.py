#!/usr/bin/env python3
"""
Run the Urdu Readability Checker web app.
Starts Flask server - open http://127.0.0.1:5000 in your browser.
"""
import os
import sys

# Ensure we're in the project directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Check model exists
if not os.path.exists("urdu_readability_model.joblib"):
    print("ERROR: Model file not found. Run: python run_linear_regression.py")
    sys.exit(1)

from app import app, load_model

if __name__ == "__main__":
    print("Loading model...")
    load_model()
    print("=" * 50)
    print("Urdu Readability Checker")
    print("Open: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=False)
