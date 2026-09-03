"""Input schema for control requirements.

Do not bundle copyrighted standards text unless you have redistribution rights.
Load the control catalogue from a source you are authorised to use.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Control:
    id: str
    name: str
    text: str


def validate_control(control: Control) -> None:
    """Validate the minimum fields required by the analysis pipeline."""
    if not control.id.strip() or not control.name.strip() or not control.text.strip():
        raise ValueError("A control requires a non-empty id, name and requirement text")
