"""
app.py
------
Flask Web Application for AI-Based Real-Time Phishing Website Detection.

Usage:
    py app/app.py
    Open browser at: http://127.0.0.1:5000
"""

import os
import sys
import joblib
import pandas as pd
from flask import Flask, render_template, request

# Ensure src/ module directory is in Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from feature_extraction import extract_features

app = Flask(__name__, template_folder="templates")

# Path to trained model
MODEL_PATH = os.path.join(SRC_DIR, "model.pkl")


def load_trained_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        input_url = request.form.get("url", "").strip()

        if input_url:
            model = load_trained_model()

            if model is None:
                result = {
                    "error": "Trained model not found (src/model.pkl). Please train the model first by running 'py src/train_model.py'."
                }
            else:
                # Extract features
                features_dict = extract_features(input_url)
                feature_df = pd.DataFrame([features_dict])

                # Model Prediction
                prediction = model.predict(feature_df)[0]
                probabilities = model.predict_proba(feature_df)[0]

                # Format results
                is_phishing = bool(prediction == 1)
                confidence = probabilities[1] * 100 if is_phishing else probabilities[0] * 100

                # Formatted feature breakdown for UI rendering
                feature_breakdown = [
                    {
                        "name": "URL Length",
                        "value": f"{features_dict['url_length']} chars",
                        "status": "warning" if features_dict['url_length'] > 75 else "normal",
                        "desc": "Long URLs often hide malicious parameters"
                    },
                    {
                        "name": "Dots Count",
                        "value": str(features_dict['num_dots']),
                        "status": "warning" if features_dict['num_dots'] > 3 else "normal",
                        "desc": "Multiple dots indicate nested subdomains"
                    },
                    {
                        "name": "'@' Symbol",
                        "value": "Found" if features_dict['having_at_symbol'] else "None",
                        "status": "danger" if features_dict['having_at_symbol'] else "normal",
                        "desc": "Ignores preceding text to trick users"
                    },
                    {
                        "name": "Domain Hyphen ('-')",
                        "value": "Found" if features_dict['prefix_suffix_in_domain'] else "None",
                        "status": "warning" if features_dict['prefix_suffix_in_domain'] else "normal",
                        "desc": "Hyphens in domain imitate brand names"
                    },
                    {
                        "name": "HTTPS Encrypted",
                        "value": "Yes (Secure)" if features_dict['uses_https'] else "No (Unencrypted)",
                        "status": "normal" if features_dict['uses_https'] else "danger",
                        "desc": "Unencrypted HTTP connections are risky"
                    },
                    {
                        "name": "IP Address Domain",
                        "value": "Yes" if features_dict['is_ip'] else "No",
                        "status": "danger" if features_dict['is_ip'] else "normal",
                        "desc": "Using IP address directly indicates phishing"
                    },
                    {
                        "name": "Subdomain Count",
                        "value": str(features_dict['num_subdomains']),
                        "status": "warning" if features_dict['num_subdomains'] >= 2 else "normal",
                        "desc": "Deeply nested subdomains obscure origin"
                    },
                    {
                        "name": "Suspicious Keywords",
                        "value": "Found" if features_dict['has_suspicious_keyword'] else "None",
                        "status": "danger" if features_dict['has_suspicious_keyword'] else "normal",
                        "desc": "Keywords like login, verify, secure, account"
                    },
                ]

                result = {
                    "url": input_url,
                    "is_phishing": is_phishing,
                    "label": "Phishing Alert" if is_phishing else "Safe Website",
                    "confidence": f"{confidence:.1f}",
                    "confidence_float": round(confidence, 1),
                    "features": feature_breakdown
                }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n Launching AI Phishing Website Detector Web App on port {port}...")
    print(f" Open in browser: http://127.0.0.1:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
