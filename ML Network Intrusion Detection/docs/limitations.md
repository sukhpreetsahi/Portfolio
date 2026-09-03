# Limitations

- CIC-IDS2017 is a controlled benchmark and may not reflect modern enterprise traffic.
- Some attack classes are highly separable, which can inflate benchmark performance.
- The dataset is imbalanced, so accuracy alone is not sufficient.
- A low false-negative count on this dataset does not guarantee low missed-detection rates in production.
- Hyperparameter search was constrained by computational resources.
- Network behaviour and attack techniques change over time, creating distribution-shift risk.
- The model is a research/portfolio prototype rather than a production IDS.

A stronger follow-up evaluation would test generalisation to another dataset and to attack types not represented during training.
