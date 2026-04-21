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
CLASSIFIER_PATH = os.path.join(
    os.path.dirname(__file__), "models", "readability_band_classifier.joblib"
)
model_data = None
classifier_data = None


def enrich_features(basic_features: dict) -> dict:
    """Add engineered features used by advanced models."""
    feats = dict(basic_features)
    sent_len = float(feats.get("sentence_length", 0) or 0)
    total_syllables = sum(i * float(feats.get(f"{i}-syllable_words", 0) or 0) for i in range(1, 9))
    total_word_length = sum(i * float(feats.get(f"word_length-{i}", 0) or 0) for i in range(1, 9))
    feats["total_syllables"] = total_syllables
    feats["total_word_length"] = total_word_length
    if sent_len > 0:
        feats["syllables_per_word"] = total_syllables / sent_len
        feats["avg_word_length"] = total_word_length / sent_len
        feats["fry_x_syllables_per_100"] = (total_syllables / sent_len) * 100
        feats["fry_y_sentences_per_100"] = 100 / sent_len
    else:
        feats["syllables_per_word"] = 0.0
        feats["avg_word_length"] = 0.0
        feats["fry_x_syllables_per_100"] = 0.0
        feats["fry_y_sentences_per_100"] = 0.0
    return feats

def load_model():
    global model_data
    if model_data is None and os.path.exists(MODEL_PATH):
        model_data = joblib.load(MODEL_PATH)
    return model_data


def load_classifier():
    global classifier_data
    if classifier_data is None and os.path.exists(CLASSIFIER_PATH):
        classifier_data = joblib.load(CLASSIFIER_PATH)
    return classifier_data

def predict_grade(text: str) -> dict:
    """
    Use Fry-based grading (calibrated to Urdu dataset) for accurate grade levels.
    Grade 1 = easiest, Grade 12 = hardest.
    """
    syll_per_100, sent_per_100 = compute_fry_metrics(text)
    if syll_per_100 is None:
        return {"error": "No valid text to analyze", "grade": None}

    # Primary grade via calibrated Fry formula (1..12)
    grade = fry_grade_from_metrics(syll_per_100, sent_per_100)
    grade_source = "fry_formula"

    # If trained classifier exists, use it for improved grade accuracy
    features = extract_features(text)
    enriched_features = enrich_features(features) if features else None

    cls_bundle = load_classifier()
    band_label = None
    band_confidence = None
    if cls_bundle and enriched_features:
        X_cls = pd.DataFrame(
            [[enriched_features.get(c, 0) for c in cls_bundle["feature_cols"]]],
            columns=cls_bundle["feature_cols"],
        )
        pred_band = int(cls_bundle["model"].predict(X_cls)[0])
        labels = cls_bundle.get("class_labels", ["easy", "moderate", "challenging"])
        if 0 <= pred_band < len(labels):
            band_label = labels[pred_band]
        if hasattr(cls_bundle["model"], "predict_proba"):
            proba = cls_bundle["model"].predict_proba(X_cls)[0]
            band_confidence = float(np.max(proba))

    # Optional: combine band with Fry grade for better UX consistency.
    # Keep grade in expected range while honoring band category.
    if band_label == "easy":
        grade = min(grade, 4)
    elif band_label == "moderate":
        grade = min(max(grade, 5), 8)
    elif band_label == "challenging":
        grade = max(grade, 9)
    if band_label:
        grade_source = "fry_formula + random_forest_band"

    # Also get model prediction for display (optional)
    pred_ratio = None
    model_data = load_model()
    if model_data and enriched_features:
            model = model_data["model"]
            feature_cols = model_data["feature_cols"]
            X = pd.DataFrame([[enriched_features.get(c, 0) for c in feature_cols]], columns=feature_cols)
            pred_ratio = float(model.predict(X)[0])

    return {
        "grade": grade,
        "grade_source": grade_source,
        "readability_band": band_label,
        "band_confidence": round(band_confidence, 4) if band_confidence is not None else None,
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
