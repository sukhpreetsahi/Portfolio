# Methodology

## Data preparation

The project uses selected CIC-IDS2017 network-flow CSV files. Traffic labels are converted into a binary target: `0` for BENIGN/Normal and `1` for malicious traffic. Missing/infinite values and duplicate rows are removed.

## Split and feature selection

The cleaned data uses a stratified 60/20/20 train/validation/test split. Features with correlation greater than 0.95 are removed, followed by `VarianceThreshold(0.01)` to remove near-constant features.

PCA is used during exploratory analysis to visualise class separability.

## Models

Two supervised tree-based classifiers are compared:

- Random Forest with balanced class weighting.
- LightGBM with imbalance handling enabled.

Precision, recall, F1-score and confusion matrices are used for evaluation, with particular attention to recall and false negatives because missed malicious traffic is costly in an IDS context.

## Optimisation

`RandomizedSearchCV` explores selected Random Forest and LightGBM hyperparameters. Random Forest tuning uses a training subset to control computational cost.

## Final evaluation

LightGBM was selected based on validation performance and the balance between F1-score and false negatives. The final model was retrained using the combined training and validation data and evaluated once on the held-out test set.
