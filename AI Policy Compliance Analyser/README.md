# Offline ISO 27001 Policy Compliance Analyser

A research prototype for assessing security-policy coverage against selected ISO/IEC 27001:2022 Annex A controls using NLP, semantic similarity, BM25 retrieval and a locally hosted LLM.

## Overview

This project explores whether parts of security-policy compliance assessment can be supported by automated document analysis. It implements and evaluates two approaches:

1. **Hybrid similarity analysis** — combines Sentence Transformer embeddings, cosine similarity and BM25 keyword retrieval to identify policy evidence relevant to security controls.
2. **Local RAG + LLM analysis** — retrieves relevant policy passages and uses a locally hosted Llama 3.2 model to produce a compliance assessment, evidence and identified gaps.

The original work was developed as university research. The public repository version focuses on the reusable implementation, methodology and findings rather than distributing the underlying research dataset.

## Why Offline Analysis?

Security policies can contain confidential, organisation-specific or otherwise sensitive information. The research therefore explored a locally executed workflow rather than sending policy content to an external AI API.

**No original organisational policy documents, policy chunks, ground-truth annotations or private evaluation data are included in this repository.**

## Architecture

```text
Policy document
      |
      v
Pre-processing and chunking
      |
      v
Sentence Transformer embeddings
      |
      +-----------------------------+
      |                             |
      v                             v
Cosine similarity + BM25      Semantic retrieval
      |                             |
      v                             v
Hybrid classification          Local LLM (RAG)
      |                             |
      +--------------+--------------+
                     v
        Compliance assessment
          + evidence + gaps
```

## Analysis Approaches

### Hybrid similarity

The first approach combines semantic similarity from a Sentence Transformer model with BM25 keyword retrieval. The combined score is used to identify relevant evidence and classify control coverage using configurable thresholds.

### Retrieval-Augmented Generation

The second approach retrieves relevant policy passages before passing the retrieved context to a locally hosted Llama 3.2 model. The model is prompted to assess the available evidence and identify compliance gaps.

## Research Findings

Evaluation on the original research dataset produced the following results:

| Approach | Accuracy | Macro F1 |
|---|---:|---:|
| Hybrid similarity | **70.37%** | **0.6281** |
| RAG + local LLM | 59.26% | 0.5794 |

The hybrid approach performed better on the evaluated dataset. This illustrates an important result of the project: adding an LLM did not automatically produce a better compliance classifier, and retrieval and classification quality remain important factors.

The underlying evaluation dataset is intentionally not published.

## Security and Privacy Considerations

- Policy documents are treated as potentially sensitive input.
- The public repository does not contain the original policy dataset.
- Generated policy chunks and organisation-specific evaluation data are excluded.
- Secrets and local credentials should never be committed to the repository.
- Automated classifications should be treated as decision support rather than evidence of ISO certification or a replacement for human assessment.

## Project Structure

```text
AI Policy Compliance Analyser/
├── README.md
├── docs/
│   ├── methodology.md
│   ├── evaluation.md
│   └── limitations.md
└── src/
    └── README.md
```

The `src/` directory is intended for the sanitised implementation extracted from the original research code. Original research data should remain outside the public repository.

## Technologies

`Python` `Sentence Transformers` `MPNet` `BM25` `RAG` `Llama 3.2` `NLP` `ISO/IEC 27001` `Information Security`

## Academic Context

Developed as part of university research investigating automated security-policy compliance assessment using NLP and locally hosted language models.

## Future Improvements

- Add a public synthetic demonstration dataset.
- Provide automated evaluation against a reproducible test set.
- Improve explainability and evidence traceability.
- Add unit and integration tests.
- Package the analyser as a reusable CLI application.
