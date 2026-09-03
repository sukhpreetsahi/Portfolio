"""Retrieval-Augmented Generation helpers.

The public repository intentionally does not contain policy documents or the
original evaluation corpus. This module accepts retrieved text supplied by the
caller and can use a local Ollama model when one is installed.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Assessment:
    evidence: str
    gaps: str
    label: str
    reasoning: str


SYSTEM_PROMPT = """You are an evidence-based security policy assessor.
Assess only the supplied control requirement and policy evidence.
Do not invent requirements or evidence. Return exactly one label:
Compliant, Partially Compliant, or Non-Compliant.
"""


def build_prompt(control: dict, policy_sections: list[str]) -> str:
    """Build a structured assessment prompt from caller-supplied content."""
    sections = "\n\n".join(
        f"Section {i}:\n{section.strip()}" for i, section in enumerate(policy_sections, 1)
    )
    return f"""Assess the policy evidence against the supplied control.\n\n"
    f"Control ID: {control['id']}\n"
    f"Control name: {control['name']}\n"
    f"Control requirement: {control['text']}\n\n"
    f"Policy evidence:\n{sections}\n\n"
    "Return:\n"
    "Evidence Found: [specific evidence]\n"
    "Gaps: [missing core requirements]\n"
    "Label: [Compliant / Partially Compliant / Non-Compliant]\n"
    "Reasoning: [one sentence]"""


def run_local_assessment(control: dict, policy_sections: list[str], model: str = "llama3.2:3b") -> str:
    """Run an assessment through a locally hosted Ollama model."""
    import ollama

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(control, policy_sections)},
        ],
        options={"temperature": 0, "repeat_penalty": 1.2, "num_predict": 350},
    )
    return response["message"]["content"]
