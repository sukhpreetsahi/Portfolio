# Implementation

This directory is reserved for the sanitised implementation extracted from the original research code.

## What belongs here

- Document preprocessing and text extraction
- Text chunking
- Sentence Transformer embedding generation
- BM25 retrieval
- Hybrid similarity scoring
- RAG retrieval and local LLM integration
- Compliance classification
- CLI entry point

## Before publishing source code

Remove hard-coded references to the original research organisations, private file paths and dataset locations. Keep the policy documents, generated chunks, ground-truth annotations and organisation-specific results outside the repository.

A future CLI can expose the pipeline through an interface such as:

```text
python main.py --policy <policy-file> --method hybrid
python main.py --policy <policy-file> --method rag
```

These commands document the intended interface; they should only be described as tested usage after the public implementation has been verified.
