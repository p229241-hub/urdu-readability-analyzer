"""
Urdu Readability - Linear Regression
Runs full pipeline: load data, train model, save model, generate Fry diagram.
Run: python run_linear_regression.py
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Loading data...")
try:
    data = pd.read_csv("input_to_linear_regression2_cleaned.csv")
    print("Loaded cleaned CSV")
except FileNotFoundError:
    data = pd.read_excel("input_to_linear_regression2.xlsx")
    if "Unnamed: 8" in data.columns:
        data = data.drop(columns=["Unnamed: 8"])
    data = data.dropna()
    print("Loaded and cleaned from Excel")

feature_cols = [
    "1-syllable_words", "2-syllable_words", "3-syllable_words", "4-syllable_words",
    "5-syllable_words", "6-syllable_words", "7-syllable_words", "8-syllable_words",
    "word_length-1", "word_length-2", "word_length-3", "word_length-4",
    "word_length-5", "word_length-6", "word_length-7", "word_length-8",
    "sentence_length"
]

X = data[feature_cols]
y = data["avg_syllable/avg_word_length"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training model...")
model = LinearRegression()
model.fit(X_train, y_train)

alpha = model.intercept_
beta = dict(zip(feature_cols, model.coef_))
gamma = model.score(X_test, y_test)

print("\n" + "="*60)
print("LINEAR REGRESSION PARAMETERS")
print("="*60)
print(f"\nALPHA (Intercept): {alpha:.6f}")
print(f"\nBETA (Coefficients):")
for feat, coef in beta.items():
    print(f"  {feat}: {coef:.6f}")
print(f"\nGAMMA (R² Score): {gamma:.6f}")

y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"\nRMSE: {rmse:.4f}")

# Save model
model_data = {"model": model, "alpha": alpha, "beta": beta, "gamma": gamma, "feature_cols": feature_cols}
joblib.dump(model_data, "urdu_readability_model.joblib")
print("\nModel saved to: urdu_readability_model.joblib")

# Fry diagram - proper Fry graph with curved boundaries
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
exec(open("fry_graph.py", encoding="utf-8").read())
print("\nDone.")
