# Machine Learning Network Intrusion Detection

A supervised machine-learning project for detecting malicious network traffic using the [**CIC-IDS2017**](https://www.unb.ca/cic/datasets/ids-2017.html) intrusion-detection dataset.

The project compares **Random Forest** and **LightGBM** classifiers, applies feature-selection techniques to reduce redundant and low-variance features, performs hyperparameter tuning, and evaluates a final model on a held-out test set.

The final selected model is a **LightGBM baseline configuration retrained on the combined training and validation data** before final evaluation.

---

## Project Overview

Network intrusion detection involves identifying potentially malicious activity within network traffic. This project explores how supervised machine-learning models can be applied to network-flow data to distinguish between **benign** and **malicious** traffic.

The workflow covers:

- Data preprocessing and cleaning
- Binary attack/benign classification
- Feature correlation analysis
- Variance-based feature selection
- Exploratory PCA visualisation
- Random Forest modelling
- LightGBM modelling
- Hyperparameter optimisation
- Model comparison
- Final model selection
- Held-out test evaluation

The project was originally developed as part of university coursework and has been retained in its original notebook-based implementation.

---

## Dataset

This project uses the **CIC-IDS2017** dataset, a publicly available network intrusion-detection benchmark produced by the Canadian Institute for Cybersecurity.

The dataset contains labelled network traffic representing both benign activity and multiple types of attacks.

The full dataset is **not included in this repository** due to its size.

To reproduce the experiment, obtain CIC-IDS2017 separately and place the required CSV files in a local `CSVs/` directory.

### Dataset

**CIC-IDS2017 — Canadian Institute for Cybersecurity**

The repository references the public dataset but does not redistribute it.

---

## Methodology

### 1. Data Loading

The notebook loads the available CIC-IDS2017 CSV files from the local `CSVs/` directory and combines them into a single dataset.

Column names are cleaned to remove unwanted whitespace.

### 2. Binary Classification

The original attack labels are converted into a binary classification problem:

```text
BENIGN → 0
All other labels → 1
```

This allows the models to focus on the primary intrusion-detection problem of distinguishing normal traffic from potentially malicious traffic.

### 3. Data Cleaning

The preprocessing pipeline removes:

- Infinite values
- Missing values
- Duplicate records

This is performed before model training to prevent invalid or duplicated observations from affecting the models.

### 4. Train/Validation/Test Split

The cleaned dataset is divided using a stratified split:

```text
60% → Training
20% → Validation
20% → Test
```

A fixed random state of `42` is used to make the experiment reproducible.

Stratification is used to maintain the relative class distribution across the three subsets.

### 5. Feature Selection

Two feature-selection stages are applied.

#### Correlation Filtering

Features with a correlation greater than `0.95` are removed based on the training data.

This reduces highly redundant features and helps simplify the resulting feature space.

#### Variance Threshold

`VarianceThreshold` is then applied using a threshold of `0.01`.

Features with very low variance are removed because they provide limited discriminatory information.

### 6. PCA Exploration

Principal Component Analysis (PCA) is used for exploratory visualisation of the processed feature space.

PCA is used for visual analysis rather than as the final modelling transformation.

---

## Machine Learning Models

Two supervised machine-learning algorithms are evaluated.

### Random Forest

The baseline Random Forest classifier uses:

- 100 estimators
- `class_weight="balanced"`
- `n_jobs=-1`
- `random_state=42`

A tuned Random Forest model is also generated using `RandomizedSearchCV`.

Class balancing is used because intrusion-detection datasets can contain substantial differences between benign and malicious traffic volumes.

### LightGBM

The baseline LightGBM classifier uses:

- 500 estimators
- `learning_rate=0.05`
- `is_unbalance=True`
- `n_jobs=-1`
- `random_state=42`

A tuned LightGBM model is also evaluated.

### Final Model

The final selected model is the **baseline LightGBM configuration**, rather than the tuned LightGBM estimator.

It is retrained using the combined training and validation datasets before being evaluated against the held-out test set.

---

## Hyperparameter Optimisation

Hyperparameter optimisation is performed using `RandomizedSearchCV`.

The optimisation process uses cross-validation and **F1-score** as the primary scoring metric.

Random Forest tuning uses a reduced training subset to keep computational requirements manageable, while LightGBM uses a larger tuning search.

The tuned models are retained alongside the baseline models to allow comparison between configurations.

---

## Evaluation

Model performance is assessed using:

- Precision
- Recall
- F1-score
- Confusion matrix
- False positives
- False negatives

F1-score provides a balance between precision and recall, while false-negative analysis is particularly important for an intrusion-detection use case.

A false negative represents malicious traffic incorrectly classified as benign.

---

## Results

The final LightGBM model achieved approximately **99.9% F1-score** on the held-out CIC-IDS2017 test set.

Final evaluation results:

- **F1-score:** ~99.9%
- **False negatives:** 15
- **False positives:** 107

For an intrusion-detection task, false negatives are particularly important because they represent malicious traffic that was classified as benign.

These results should be interpreted as **benchmark results on CIC-IDS2017**, rather than evidence of production-ready intrusion-detection performance.

---

## Final Model

The final model is a **LightGBM classifier** using the baseline configuration.

The final training process combines:

```text
Training set + Validation set
```

The resulting model is then evaluated against the previously held-out test set.

The saved final model is:

```text
models/final_model.joblib
```

---

## Repository Structure

```text
ML Network Intrusion Detection/
│
├── models-notebook.ipynb
├── codefortesting.py
├── requirements.txt
├── README.md
│
├── docs/
│   ├── methodology.md
│   └── limitations.md
│
└── models/
    ├── final_model.joblib
    ├── lgbm_baseline.joblib
    ├── lgbm_tuned.joblib
    ├── rf_baseline.joblib
    ├── rf_tuned.joblib
    ├── variance_selector.joblib
    ├── correlated_features.npy
    ├── columns_after_corr.npy
    └── final_feature_names.npy
```

### Key Files

| File | Description |
|---|---|
| `models-notebook.ipynb` | Original modelling, experimentation and evaluation notebook |
| `codefortesting.py` | Loads the saved model and preprocessing artefacts and reproduces test-set evaluation |
| `models/final_model.joblib` | Saved final LightGBM model |
| `models/lgbm_baseline.joblib` | Baseline LightGBM model |
| `models/lgbm_tuned.joblib` | Tuned LightGBM model |
| `models/rf_baseline.joblib` | Baseline Random Forest model |
| `models/rf_tuned.joblib` | Tuned Random Forest model |
| `models/variance_selector.joblib` | Saved variance-based feature selector |
| `models/correlated_features.npy` | Saved feature information from correlation filtering |
| `models/columns_after_corr.npy` | Feature column ordering after correlation filtering |
| `models/final_feature_names.npy` | Final feature names used by the modelling pipeline |
| `requirements.txt` | Python dependencies required to run the project |

---

## Reproducing the Evaluation

### 1. Obtain the Dataset

Download the CIC-IDS2017 dataset separately from its public source.

The complete dataset is intentionally not included in this repository.

### 2. Prepare the Dataset

Place the required CSV files in a local directory:

```text
CSVs/
├── <CIC-IDS2017 CSV files>
└── ...
```

### 3. Install Dependencies

Create a Python environment and install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Evaluation Script

From the project directory:

```bash
python codefortesting.py
```

The script loads the saved final model and preprocessing artefacts, reconstructs the preprocessing and data split used during the original experiment, and evaluates the model on the held-out test data.

---

## Security Relevance

Machine-learning-based intrusion detection can complement traditional signature- and rule-based detection approaches by identifying statistical patterns associated with malicious network activity.

This project demonstrates several security-relevant concepts:

- Network intrusion detection
- Supervised machine learning
- Security data preprocessing
- Class imbalance handling
- False-negative analysis
- Feature selection
- Model evaluation
- Hyperparameter optimisation
- Benchmark-based security experimentation

In a real security environment, an ML-based detector would typically operate alongside other controls such as SIEM correlation, signatures, network telemetry, threat intelligence and analyst investigation.

---

## Limitations

This project is a research and portfolio implementation rather than a production-ready intrusion-detection system.

### Dataset Limitations

CIC-IDS2017 is a controlled benchmark dataset and may not accurately represent modern enterprise network environments.

### Distribution Shift

Network behaviour, applications and attack techniques change over time. A model trained on historical data may therefore perform differently when exposed to new traffic distributions or previously unseen attacks.

### Class Imbalance

Security datasets can contain significant differences between benign and malicious observations. Accuracy alone can therefore be misleading, which is why precision, recall, F1-score and false-negative counts are also considered.

### Benchmark Performance

Some attack traffic in CIC-IDS2017 can be highly distinguishable from benign traffic. High benchmark performance therefore does not necessarily translate directly into equivalent real-world performance.

### False Negatives

A low false-negative count on the benchmark does not guarantee that the model will identify novel or evasive attacks.

### Computational Constraints

Hyperparameter optimisation was constrained to keep experimentation computationally practical. A larger search space or additional cross-validation could potentially produce different model configurations.

### Production Deployment

Before deployment in a real environment, the model would require additional testing using contemporary network traffic, unseen attack techniques, continuous monitoring, model drift detection and appropriate operational controls.

---

## Technologies

- **Python**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **LightGBM**
- **Joblib**
- **Matplotlib**
- **Seaborn**
- **Jupyter Notebook**
- **CIC-IDS2017**

---

## Skills Demonstrated

- Network intrusion detection
- Machine learning for cybersecurity
- Data preprocessing
- Feature engineering and selection
- Random Forest classification
- Gradient boosting / LightGBM
- Hyperparameter optimisation
- Model evaluation
- Imbalanced classification
- Security-focused false-negative analysis
- Reproducible ML experimentation

---

## Disclaimer

This project was developed for academic and portfolio purposes.

The reported performance is based on the CIC-IDS2017 benchmark dataset and should not be interpreted as a guarantee of effectiveness against real-world or previously unseen network attacks.
