"""
predict.py
----------
Command-line inference utility for the AI Phishing Detection System.

Usage:
  python src/predict.py "https://example.com"
  python src/predict.py (interactive prompt)
"""

import sys
import os
import joblib
import pandas as pd
from feature_extraction import extract_features


def predict_url(url: str):
    """
    Extracts features from the given URL and predicts whether it is Phishing or Legitimate.
    Returns a dictionary containing prediction results and confidence metrics.
    """
    # Locate model file
    model_path = os.path.join("src", "model.pkl")
    if not os.path.exists(model_path):
        # Fallback check for root directory if run from src/
        model_path = "model.pkl" if os.path.exists("model.pkl") else os.path.join("src", "model.pkl")

    if not os.path.exists(model_path):
        print(" Error: Trained model file 'src/model.pkl' not found!")
        print("Please train the model first by running: python src/train_model.py")
        sys.exit(1)

    # Load model
    model = joblib.load(model_path)

    # Extract features
    features_dict = extract_features(url)

    # Convert to DataFrame matching model input format
    feature_df = pd.DataFrame([features_dict])

    # Predict class (0 = Legitimate, 1 = Phishing)
    prediction = model.predict(feature_df)[0]
    probabilities = model.predict_proba(feature_df)[0]

    # Calculate confidence score
    # probabilities[0] is probability of Legitimate, probabilities[1] is Phishing
    if prediction == 1:
        result_label = "Phishing"
        confidence = probabilities[1] * 100
    else:
        result_label = "Legitimate"
        confidence = probabilities[0] * 100

    return {
        "url": url,
        "prediction": result_label,
        "is_phishing": bool(prediction == 1),
        "confidence": confidence,
        "features": features_dict,
    }


def main():
    print("=" * 60)
    print("       AI-BASED REAL-TIME PHISHING WEBSITE DETECTOR        ")
    print("=" * 60)

    # Get URL from command line argument or prompt user
    if len(sys.argv) > 1:
        url_input = sys.argv[1]
    else:
        url_input = input("\nEnter website URL to analyze: ").strip()

    if not url_input:
        print("Error: No URL provided.")
        return

    print(f"\n Analyzing URL: {url_input} ...\n")
    result = predict_url(url_input)

    # Output formatted prediction result
    print("-" * 60)
    if result["is_phishing"]:
        print(f" RESULT    : [!] PHISHING ALERT ({result['confidence']:.1f}% confidence)")
    else:
        print(f" RESULT    : [OK] LEGITIMATE WEBSITE ({result['confidence']:.1f}% confidence)")
    print("-" * 60)

    print("\n Feature Breakdown:")
    features = result["features"]
    print(f"  * URL Length            : {features['url_length']} characters")
    print(f"  * Dots Count            : {features['num_dots']}")
    print(f"  * '@' Symbol Present    : {'Yes (Suspicious)' if features['having_at_symbol'] else 'No'}")
    print(f"  * Domain Hyphen ('-')   : {'Yes (Suspicious)' if features['prefix_suffix_in_domain'] else 'No'}")
    print(f"  * HTTPS Encryption      : {'Yes (Secure)' if features['uses_https'] else 'No (Unencrypted)'}")
    print(f"  * IP Address Domain     : {'Yes (Suspicious)' if features['is_ip'] else 'No'}")
    print(f"  * Subdomain Count       : {features['num_subdomains']}")
    print(f"  * Suspicious Keywords   : {'Yes (Suspicious)' if features['has_suspicious_keyword'] else 'No'}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
