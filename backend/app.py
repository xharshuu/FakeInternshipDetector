from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import numpy as np

app = Flask(__name__)
CORS(app)

# ── Load trained model ──────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE, 'model')

vectorizer = joblib.load(os.path.join(MODEL_DIR, 'tfidf_vectorizer.joblib'))
classifier = joblib.load(os.path.join(MODEL_DIR, 'scam_classifier.joblib'))

print("ML model loaded successfully.")


@app.route("/")
def home():
    return "<h2>✅ Scam Detector API is running (ML-powered)!</h2><p>Use the browser extension to analyze offers.</p>"


@app.route("/check", methods=["POST"])
def check_offer():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "Empty text"}), 400

    # Vectorise and predict
    X = vectorizer.transform([text])
    prediction = classifier.predict(X)[0]          # 0 = legit, 1 = scam
    probabilities = classifier.predict_proba(X)[0]  # [prob_legit, prob_scam]

    scam_confidence = float(probabilities[1])        # 0.0 → 1.0
    risk_score = int(round(scam_confidence * 100))   # 0 → 100

    if risk_score >= 60:
        result = "Scam"
    elif risk_score >= 30:
        result = "Suspicious"
    else:
        result = "Safe"

    return jsonify({
        "result": result,
        "risk_score": risk_score,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
