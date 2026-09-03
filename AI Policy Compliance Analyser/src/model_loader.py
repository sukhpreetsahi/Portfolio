"""Optional local LLM integration via Ollama."""
from __future__ import annotations

DEFAULT_MODEL = "llama3.2:3b"


def run_inference(model: str, system_prompt: str, user_prompt: str) -> str:
    """Send an assessment request to a locally running Ollama model."""
    import ollama

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": 0, "repeat_penalty": 1.2, "num_predict": 350},
    )
    return response["message"]["content"]
