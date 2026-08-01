"""
prepare_dataset.py
------------------
This script reads phishing and legitimate URL CSV files, extracts feature
vectors from each URL using feature_extraction.py, and combines them into
a processed dataset (data/processed_dataset.csv) ready for model training.
"""

import os
import pandas as pd
from feature_extraction import extract_features


def prepare_dataset():
    # Define file paths
    phishing_path = os.path.join("data", "phishing_urls.csv")
    legit_path = os.path.join("data", "legit_urls.csv")
    output_path = os.path.join("data", "processed_dataset.csv")

    # Check if raw dataset files exist
    if not os.path.exists(phishing_path) or not os.path.exists(legit_path):
        print(" Error: Missing raw dataset files in the data/ directory!")
        print(f"  - Expected phishing URLs: {phishing_path}")
        print(f"  - Expected legitimate URLs: {legit_path}")
        print("\nPlease place 'phishing_urls.csv' and 'legit_urls.csv' in the data/ folder.")
        print("Each CSV file must contain a 'url' column header.")
        return

    print(" Reading raw dataset files...")
    phishing_df = pd.read_csv(phishing_path)
    legit_df = pd.read_csv(legit_path)

    # Ensure 'url' column exists (case-insensitive check)
    phishing_df.columns = [col.strip().lower() for col in phishing_df.columns]
    legit_df.columns = [col.strip().lower() for col in legit_df.columns]

    if "url" not in phishing_df.columns or "url" not in legit_df.columns:
        print(" Error: Both CSV files must contain a column named 'url'.")
        return

    # Assign labels: 1 = Phishing, 0 = Legitimate
    phishing_df["label"] = 1
    legit_df["label"] = 0

    # Combine both datasets
    combined_df = pd.concat([phishing_df[["url", "label"]], legit_df[["url", "label"]]], ignore_index=True)
    print(f" Combined dataset contains {len(combined_df)} URLs ({len(phishing_df)} Phishing, {len(legit_df)} Legitimate).")

    print("\n Extracting features from URLs (this may take a few seconds)...")
    feature_list = []

    for index, row in combined_df.iterrows():
        url_str = str(row["url"]).strip()
        features = extract_features(url_str)
        features["label"] = row["label"]
        feature_list.append(features)

    # Create processed dataframe
    processed_df = pd.DataFrame(feature_list)

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Save to CSV
    processed_df.to_csv(output_path, index=False)
    print(f"\n Success! Processed feature dataset saved to: {output_path}")
    print(f"  - Total rows: {len(processed_df)}")
    print(f"  - Columns: {list(processed_df.columns)}")


if __name__ == "__main__":
    prepare_dataset()
