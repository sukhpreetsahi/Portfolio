# Methodology

## Objective

The project investigates whether automated natural-language processing can support assessment of security-policy coverage against selected ISO/IEC 27001:2022 Annex A controls.

The system was designed as decision support rather than as an automated certification or audit tool.

## Processing pipeline

1. Policy documents are converted into text.
2. Text is cleaned and divided into manageable chunks.
3. Policy and control text is represented using Sentence Transformer embeddings.
4. Relevant policy passages are identified using semantic similarity and/or lexical retrieval.
5. Retrieved evidence is compared with the relevant control requirement.
6. The system produces a compliance classification and supporting evidence/gaps.

## Hybrid similarity approach

The hybrid approach combines semantic similarity with BM25 keyword retrieval. Semantic similarity helps identify passages that express similar meaning even when terminology differs, while BM25 provides lexical matching for important security terms.

A weighted score is used to combine the signals and configurable thresholds are used to distinguish stronger and weaker evidence.

## Local RAG approach

The RAG pipeline retrieves relevant policy passages before passing the context to a locally hosted Llama 3.2 model. The model is prompted to assess the evidence available in the retrieved context and identify gaps.

Running the language model locally was important to the research because policy documents may contain sensitive organisational information.

## Design principle

The central design principle is **security and privacy by design**: the analysis should be capable of being performed locally without requiring policy documents to be sent to an external AI service.

## Important boundary

Policy text describes intended controls and does not necessarily prove that those controls are implemented in practice. Automated results therefore require human validation before being treated as an assurance conclusion.
