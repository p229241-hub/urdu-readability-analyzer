"""
Urdu Readability Checker - Flask Backend
Serves the web UI and provides /api/analyze for readability prediction.
Run: python app.py  |  Then open http://127.0.0.1:5000
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from urdu_features import extract_features, compute_fry_metrics, fry_grade_from_metrics

app = Flask(__name__)

# Load model for ratio display (optional)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "urdu_readability_model.joblib")
model_data = None

def load_model():
    global model_data
    if model_data is None and os.path.exists(MODEL_PATH):
        model_data = joblib.load(MODEL_PATH)
    return model_data

def predict_grade(text: str) -> dict:
    """
    Use Fry-based grading (calibrated to Urdu dataset) for accurate grade levels.
    Grade 1 = easiest, Grade 12 = hardest.
    """
    syll_per_100, sent_per_100 = compute_fry_metrics(text)
    if syll_per_100 is None:
        return {"error": "No valid text to analyze", "grade": None}

    grade = fry_grade_from_metrics(syll_per_100, sent_per_100)

    # Also get model prediction for display (optional)
    pred_ratio = None
    model_data = load_model()
    if model_data:
        features = extract_features(text)
        if features:
            model = model_data["model"]
            feature_cols = model_data["feature_cols"]
            X = pd.DataFrame([[features.get(c, 0) for c in feature_cols]], columns=feature_cols)
            pred_ratio = float(model.predict(X)[0])

    return {
        "grade": grade,
        "readability_ratio": round(pred_ratio, 3) if pred_ratio else None,
        "syllables_per_100": round(syll_per_100, 1),
        "sentences_per_100": round(sent_per_100, 1),
        "message": f"یہ متن گریڈ {grade} کے قارئین کے لیے موزوں ہے",
        "message_en": f"This text is suitable for Grade {grade} readers",
    }

@app.route("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided", "grade": None}), 400
    result = predict_grade(text)
    if result.get("error"):
        return jsonify(result), 400
    return jsonify(result)

if __name__ == "__main__":
    load_model()
    app.run(debug=True, port=5000)
