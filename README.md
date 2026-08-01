# 🛡️ AI Phishing Website Detector

A real-time phishing website detection web app powered by machine learning. Enter any URL and the app analyzes it instantly to determine whether it's likely safe or a phishing attempt.

## 🚀 Live Demo
[https://phishing-detection-h79s.onrender.com](https://phishing-detection-h79s.onrender.com)

> ⚠️ Note: The app is hosted on a free tier, so it may take up to 50 seconds to load if it's been inactive.

## 📋 How It Works

The app extracts key features from a given URL and feeds them into a trained machine learning model to classify it as **Safe** or **Phishing**, along with a confidence score.

**Features analyzed:**
- URL length
- Number of dots / subdomains
- Presence of `@` symbol
- Hyphens in domain (brand imitation check)
- HTTPS usage
- Whether the domain is a raw IP address
- Suspicious keywords (e.g. login, verify, secure, account)

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Machine Learning:** scikit-learn
- **Data Handling:** pandas, numpy
- **Deployment:** Render (Gunicorn WSGI server)
- **Frontend:** HTML/CSS (Flask templates)

## 💻 Running Locally

1. Clone the repo:
   git clone https://github.com/Sneka-v811/phishing-detection.git
   cd phishing-detection

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   python app/app.py

4. Open your browser at http://127.0.0.1:5000

## 📁 Project Structure

phishing-detection/
├── app/
│   ├── app.py              # Flask application
│   └── templates/
│       └── index.html      # Frontend UI
├── src/
│   ├── feature_extraction.py
│   ├── train_model.py
│   ├── predict.py
│   └── model.pkl           # Trained ML model
├── data/
│   ├── legit_urls.csv
│   └── phishing_urls.csv
├── requirements.txt
└── Procfile

## 📌 Disclaimer

This tool is built for educational purposes to demonstrate ML-based phishing detection. It should not be used as the sole method for verifying website safety in production environments.