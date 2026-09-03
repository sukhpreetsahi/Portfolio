# Implementation

This directory is for the sanitised implementation extracted from the original research code.

## What is here

- Document preprocessing and text extraction
- Text chunking
- Sentence Transformer embedding generation
- BM25 retrieval
- Hybrid similarity scoring
- RAG retrieval and local LLM integration
- Compliance classification
- CLI entry point

## Public Source code limitations

Removed hard-coded references to the original research organisations, private file paths and dataset locations. Kept the policy documents, generated chunks, ground-truth annotations and organisation-specific results outside the repository.

A future CLI can expose the pipeline through an interface such as:

```text
python main.py --policy <policy-file> --method hybrid
python main.py --policy <policy-file> --method rag
```
