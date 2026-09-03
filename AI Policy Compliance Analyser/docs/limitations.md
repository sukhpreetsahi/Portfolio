# Limitations

This project is a research prototype and should not be treated as an automated ISO/IEC 27001 audit or certification system.

## Evidence is not implementation

A policy can describe an intended security control without proving that the control is actually implemented. Automated analysis can identify relevant wording, but implementation assurance requires additional evidence and human review.

## Semantic similarity is not compliance

A high similarity score indicates that text appears relevant to a control; it does not establish that the requirement is fully satisfied.

## Retrieval affects RAG quality

The local LLM can only reason over the evidence supplied to it. Missing or poorly retrieved passages can therefore produce incomplete assessments.

## Local LLM limitations

Small locally hosted language models may produce inconsistent classifications or explanations. Results should be reviewed rather than accepted blindly.

## Dataset limitations

The reported evaluation results come from the original research dataset, which is not publicly distributed. A future public version should use a synthetic or otherwise appropriately licensed dataset so that the complete pipeline can be reproduced independently.

## Scope

The project assesses selected policy evidence against selected controls and is not intended to cover every requirement of an ISO/IEC 27001 certification assessment.
