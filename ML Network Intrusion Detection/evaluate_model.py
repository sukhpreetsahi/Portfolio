from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, f1_score

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "CSVs"

MODEL_PATH = MODEL_DIR / "final_model.joblib"
SELECTOR_PATH = MODEL_DIR / "variance_selector.joblib"
CORRELATED_PATH = MODEL_DIR / "correlated_features.npy"
COLUMNS_PATH = MODEL_DIR / "columns_after_corr.npy"

def load_dataset():
    csv_files = list(DATA_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CIC-IDS2017 CSV files found. Download the public dataset separately.")
    return pd.concat([pd.read_csv(path) for path in csv_files], ignore_index=True)

def preprocess(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df["Label"] = df["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    return df

def main():
    final_model = joblib.load(MODEL_PATH)
    selector = joblib.load(SELECTOR_PATH)
    correlated = np.load(CORRELATED_PATH, allow_pickle=True).tolist()
    columns_after_corr = np.load(COLUMNS_PATH, allow_pickle=True).tolist()

    df = preprocess(load_dataset())
    features = df.drop("Label", axis=1)
    labels = df["Label"]

    from sklearn.model_selection import train_test_split
    _, X_temp, _, y_temp = train_test_split(features, labels, test_size=0.4, stratify=labels, random_state=42)
    _, X_test, _, y_test = train_test_split(X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)

    X_test = X_test.drop(columns=correlated, errors="ignore")
    X_test = X_test[columns_after_corr]
    X_test = selector.transform(X_test)
    predictions = final_model.predict(X_test)

    print(classification_report(y_test, predictions, target_names=["Normal", "Malicious"], digits=4))
    cm = confusion_matrix(y_test, predictions)
    print("Confusion matrix:")
    print(cm)
    print(f"F1 score: {f1_score(y_test, predictions):.4f}")
    print(f"False negatives: {cm[1, 0]}")
    print(f"False positives: {cm[0, 1]}")

if __name__ == "__main__":
    main()
