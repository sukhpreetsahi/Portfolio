# Machine Learning Network Intrusion Detection

A supervised machine-learning project for classifying network traffic as **normal** or **malicious** using the CIC-IDS2017 intrusion-detection dataset.

The project compares **Random Forest** and **LightGBM**, with preprocessing, feature selection, class-imbalance handling, hyperparameter tuning and final evaluation.

## Project overview

The workflow:

1. Loads selected CIC-IDS2017 CSV files.
2. Cleans missing/infinite values and duplicates.
3. Converts the original traffic labels into a binary Normal/Malicious target.
4. Creates a stratified 60/20/20 train/validation/test split.
5. Removes highly correlated features (`> 0.95`).
6. Removes very-low-variance features using `VarianceThreshold(0.01)`.
7. Uses PCA for exploratory visualisation of class separability.
8. Trains baseline Random Forest and LightGBM classifiers.
9. Tunes both models using `RandomizedSearchCV`.
10. Selects and retrains the strongest model on the combined training and validation sets.
11. Evaluates the final model on an untouched test set using classification metrics and a confusion matrix.

## Models

### Random Forest

Random Forest was selected because an ensemble of decision trees can model non-linear relationships in high-dimensional network-flow data while reducing the variance associated with an individual decision tree.

### LightGBM

LightGBM was selected as a gradient-boosting approach designed for efficient training on larger tabular datasets. Class imbalance was addressed using `is_unbalance=True`.

## Result

The final model was **LightGBM**, trained on the combined training and validation data.

On the original held-out test set, the final model achieved an **F1-score of approximately 99.9%**, with **15 false negatives** and **107 false positives**.

Because this is an intrusion-detection problem, false negatives are particularly important: a missed malicious flow can represent an undetected attack.

These results should be interpreted in the context of CIC-IDS2017 and should not be assumed to represent equivalent performance on real-world network traffic.

## Dataset

This project uses the **CIC-IDS2017 dataset** from the Canadian Institute for Cybersecurity.

The dataset is publicly available from the University of New Brunswick:

https://www.unb.ca/cic/datasets/ids-2017.html

The dataset itself is **not included in this repository**. Download the appropriate CIC-IDS2017 CSV files separately if you want to reproduce the experiments.

The original project excluded Monday's benign-only traffic and the Friday afternoon PortScan CSV, focusing on the selected Tuesday-Friday traffic files used in the experiments.

## Repository contents

- `models-notebook.ipynb` — preprocessing, exploratory analysis, model training, tuning and evaluation.
- `evaluate_model.py` — loads the final model and preprocessing artefacts and evaluates it against locally downloaded dataset files.
- `models/` — selected final model/preprocessing artefacts where included.
- `requirements.txt` — Python dependencies.

## Security relevance

Machine-learning IDS models can complement traditional signature/rule-based detection by learning patterns associated with malicious network behaviour.

Important operational considerations include:

- class imbalance and the cost of missed detections;
- false-positive volume and analyst workload;
- distribution shift between benchmark and production traffic;
- explainability of model decisions;
- adversarial manipulation of network traffic;
- continuous validation against current threats.

## Limitations

CIC-IDS2017 is a controlled benchmark rather than representative live enterprise traffic. The strong separability of some attack patterns can make benchmark performance considerably higher than what may be achieved in production.

The project therefore demonstrates an ML-based intrusion-detection workflow rather than a production-ready IDS.

## Future work

- Evaluate against additional and more recent IDS datasets.
- Test cross-dataset generalisation.
- Investigate unseen attack types.
- Add explainability using feature-attribution techniques.
- Explore streaming/live traffic inference.
- Compare model performance under realistic class distributions.
