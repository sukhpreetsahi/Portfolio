import joblib
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, f1_score, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os

# Get the directory this script is in
BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "models"

# Load artefacts
print("Loading final model and preprocessing artefacts...")
final_model_loaded = joblib.load(MODEL_DIR / "final_model.joblib")
selector_loaded = joblib.load(MODEL_DIR / "variance_selector.joblib")

correlated_features_loaded = np.load(MODEL_DIR / "correlated_features.npy", allow_pickle=True).tolist()
columns_after_corr_loaded = np.load(MODEL_DIR / "columns_after_corr.npy", allow_pickle=True).tolist()
print("Loaded final model and preprocessing artefacts.")


# Help build a df from CIC-IDS2017 CSVs (using exact CSVs as in the notebook)
DATA_DIR = BASE_DIR / "CSVs"
csv_files = list(DATA_DIR.glob("*.csv"))
if not csv_files:
    raise FileNotFoundError("No CSV files found.")
df_list = []
print("\nLoading CSV files and merging into 1 singular Dataframe...")
for file in csv_files:
    df = pd.read_csv(file)
    df_list.append(df)
# Merge into one DataFrame
df = pd.concat(df_list, ignore_index=True)
for d in df_list: # Free memory
    del d  
df.columns = df.columns.str.strip() # Remove leading/trailing spaces from column names which causes parsing issues
print("Created Dataframe from CSVs")

# 2) Preprocessing - Apply same steps as in notebook
print("\nPreprocessing data... (may take some time)")
df['Label'] = df['Label'].apply(lambda x: 0 if x == 'BENIGN' else 1) # Convert labels to binary (0 for Normal, 1 for Malicious)
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df = df.dropna() # Drop rows with missing values
duplicates = df[df.duplicated()]
df = df.drop_duplicates() # Remove duplicate rows
print(f"Shape after removing duplicates: {df.shape}")


# Splitting exactly as in notebook
print("\nSplitting data into train/val/test...")
features = df.drop("Label", axis=1)
labels = df["Label"]
X_train, X_temp, y_train, y_temp = train_test_split(features, labels, test_size=0.4, stratify=labels, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)
print(f"Train shape: {X_train.shape}, Val shape: {X_val.shape}, Test shape: {X_test.shape}")

# Drop correlated features, enforce column order, apply VarianceThreshold
# Drop the same features from test split
X_test  = X_test.drop(columns=correlated_features_loaded, errors="ignore")
X_test = X_test[columns_after_corr_loaded]
X_test = selector_loaded.transform(X_test)
print ("\nDropping very highly correlated features: " + str(correlated_features_loaded))
print("Dropped low variance features using loaded VarianceThreshold selector.")

# Predict and evaluate
print("\nPredicting and evaluating on test set...")
y_test_pred_loaded = final_model_loaded.predict(X_test)
print("Predictions on test set complete.")

print("\nClassification report (loaded final model):")
print(classification_report(y_test, y_test_pred_loaded, digits=4))

final_f1 = f1_score(y_test, y_test_pred_loaded)
print(f"\nFinal Test F1 score (loaded): {final_f1 * 100:.2f}%")

cm = confusion_matrix(y_test, y_test_pred_loaded)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Normal", "Malicious"])
disp.plot()
plt.title("\nFinal Model Confusion Matrix (Loaded Model, Test Set)")
plt.show()

fn = cm[1, 0]
fp = cm[0, 1]
print(f"False Negatives: {fn}")
print(f"False Positives: {fp}")
print("Finished evaluating loaded model on test set.")