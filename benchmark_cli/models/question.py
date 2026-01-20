"""
Question input models.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class QuestionInput:
    """Represents a question input (without response)."""
    id: str
    question: str
    expected: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
