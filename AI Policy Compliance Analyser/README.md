# Offline ISO 27001 Policy Compliance Analyser

A research prototype for assessing security-policy coverage against selected ISO/IEC 27001:2022 Annex A controls using NLP, semantic similarity, BM25 retrieval and a locally hosted LLM.

## Overview

This project explores whether parts of security-policy compliance assessment can be supported by automated document analysis. It implements and evaluates two approaches:

1. **Hybrid similarity analysis** — combines Sentence Transformer embeddings, cosine similarity and BM25 keyword retrieval to identify policy evidence relevant to security controls.
2. **Local RAG + LLM analysis** — retrieves relevant policy passages and uses a locally hosted Llama 3.2 model to produce a compliance assessment, evidence and identified gaps.

The original work was developed as university research. This portfolio version extracts the reusable engineering concepts and documents the research findings without distributing the underlying dataset.

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

The first approach combines semantic similarity from a Sentence Transformer model with BM25 keyword retrieval. The combined score identifies relevant evidence and configurable thresholds are used to classify control coverage.

### Retrieval-Augmented Generation

The second approach retrieves relevant policy passages before passing the retrieved context to a locally hosted Llama 3.2 model. The model is prompted to assess the supplied evidence and identify gaps.

## Research Findings

Evaluation on the original research dataset produced the following results:

| Approach | Accuracy | Macro F1 |
|---|---:|---:|
| Hybrid similarity | **70.37%** | **0.6281** |
| RAG + local LLM | 59.26% | 0.5794 |

The hybrid approach performed better on the evaluated dataset. This is a useful engineering finding: adding an LLM did not automatically improve classification quality, and retrieval quality and threshold calibration remained important factors.

These figures are **reported research results, not a claim that the public repository reproduces the original experiment**. The original evaluation data is intentionally not published.

## Security & Privacy Considerations

- Policy documents are treated as potentially sensitive input.
- The public repository does not contain the original policy dataset.
- Generated policy chunks and organisation-specific evaluation data are excluded.
- Secrets and local credentials should never be committed.
- Automated classifications are decision support and are not evidence of ISO certification or a replacement for human assessment.

## Project Structure

```text
AI Policy Compliance Analyser/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── methodology.md
│   ├── evaluation.md
│   └── limitations.md
└── src/
    ├── controls.py
    ├── model_loader.py
    ├── preprocessor.py
    ├── rag.py
    ├── similarity.py
    └── README.md
```

The implementation accepts policy/control content supplied by the user rather than bundling the original research corpus.

## Technologies

`Python` `Sentence Transformers` `MPNet` `BM25` `RAG` `Llama 3.2` `Ollama` `NLP` `ISO/IEC 27001` `Information Security`

## Academic Context

Developed as part of university research investigating automated security-policy compliance assessment using NLP and locally hosted language models.

## Limitations

This is a research prototype. A policy statement is not proof that a control is implemented effectively, and text similarity can miss context, scope and exceptions. LLM output can also be inconsistent. Results therefore require human validation.

## Future Improvements

- Add a public synthetic demonstration dataset.
- Add automated tests and a reproducible public benchmark.
- Improve explainability and evidence traceability.
- Add a CLI application when the project needs one.
- Explore more robust calibration and retrieval strategies.
