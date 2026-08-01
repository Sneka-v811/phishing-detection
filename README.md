# AI-Based Real-Time Phishing Website Detection System

## Overview
This project is an AI-powered system designed to detect whether a given URL or website is **Phishing** or **Legitimate** using Machine Learning.

The system works by extracting key syntactic and domain features from URLs (such as URL length, presence of `@` symbols, IP address usage, subdomains, and suspicious keywords), and using a classification algorithm trained on historical data to predict safety in real time.

---

## Folder Structure

```text
phishing-detection/
│
├── data/                  # Storage directory for the training dataset (CSV)
│
├── src/                   # Source code modules
│   ├── feature_extraction.py  # Extracts lexical & domain features from URLs
│   ├── train_model.py         # Model training pipeline (Random Forest / Decision Tree)
│   └── predict.py             # Inference module to classify single URLs
│
├── app/                   # Web application interface
│   ├── app.py             # Flask backend app
│   └── templates/
│       └── index.html     # HTML frontend user interface
│
├── requirements.txt       # Project Python library dependencies
└── README.md              # Project overview and setup instructions
```

---

## Setup & Installation

### 1. Environment Setup (Recommended)
It is recommended to use a Python virtual environment.

```bash
# Navigate to project directory
cd phishing-detection

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Quick Test: Feature Extraction
To verify that feature extraction is working:
```bash
python src/feature_extraction.py
```
