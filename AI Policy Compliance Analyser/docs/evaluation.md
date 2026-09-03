# Evaluation

The original research compared two approaches for classifying policy coverage.

| Approach | Accuracy | Macro F1 |
|---|---:|---:|
| Hybrid similarity | **70.37%** | **0.6281** |
| RAG + local LLM | 59.26% | 0.5794 |

## Interpretation

The hybrid similarity approach performed better on the original evaluation dataset. The result is useful because it shows that adding a language model does not automatically improve classification quality.

The project highlighted the importance of retrieval quality, threshold calibration and the distinction between textual evidence and actual control implementation.

## Data availability

The original policy documents, manual annotations, organisation-specific results and other research data are intentionally not included in this public repository. The metrics above are reported from the original research experiments.

A reproducible public evaluation dataset is a future improvement rather than a requirement of this portfolio version.
