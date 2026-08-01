"""
train_model.py
--------------
This script loads data/processed_dataset.csv, splits it into training and test sets,
trains a Random Forest classifier, prints evaluation metrics (accuracy, precision, recall,
confusion matrix), and saves the trained model to src/model.pkl.
"""

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report,
)


def train_model():
    dataset_path = os.path.join("data", "processed_dataset.csv")
    model_output_path = os.path.join("src", "model.pkl")

    # Check if processed dataset exists
    if not os.path.exists(dataset_path):
        print(" Error: Processed dataset not found!")
        print(f"  - Expected path: {dataset_path}")
        print("\nPlease run 'python src/prepare_dataset.py' first to generate the dataset.")
        return

    print(" Loading dataset...")
    df = pd.read_csv(dataset_path)

    # Separate feature matrix (X) and target label vector (y)
    X = df.drop(columns=["label"])
    y = df["label"]

    print(f" Dataset loaded: {X.shape[0]} samples with {X.shape[1]} features each.")

    # 80/20 Train-Test Split with stratification for balanced class representation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  - Training samples: {X_train.shape[0]}")
    print(f"  - Testing samples:  {X_test.shape[0]}")

    # Initialize and train Random Forest Classifier
    print("\n Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    # Calculate Evaluation Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    print("\n" + "=" * 50)
    print("                MODEL EVALUATION RESULTS              ")
    print("=" * 50)
    print(f" Accuracy:  {accuracy * 100:.2f}%")
    print(f" Precision: {precision * 100:.2f}%")
    print(f" Recall:    {recall * 100:.2f}%")
    print("-" * 50)
    print(" Confusion Matrix:")
    print(f"   TN (True Legitimate):  {cm[0][0]}  | FP (False Phishing): {cm[0][1]}")
    print(f"   FN (False Legitimate): {cm[1][0]}  | TP (True Phishing):  {cm[1][1]}")
    print("-" * 50)
    print("\n Detailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Legitimate (0)", "Phishing (1)"]))

    # Save trained model using joblib
    joblib.dump(model, model_output_path)
    print(f" Success! Trained model saved to: {model_output_path}")


if __name__ == "__main__":
    train_model()
