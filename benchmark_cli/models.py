"""
Data models for evaluation pairs and results.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class EvaluationPair:
    """Represents a chatbot response to evaluate."""
    id: str
    question: str
    response: str
    expected: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class MetricResult:
    """Result from a single metric evaluation."""
    metric_name: str
    score: float
    details: Optional[Dict[str, Any]] = None


@dataclass
class EvaluationResult:
    """Complete evaluation result for a response."""
    pair_id: str
    metrics: List[MetricResult]
    human_scores: Optional[Dict[str, Any]] = None
    
    def get_summary(self) -> Dict[str, float]:
        """Get summary of all metric scores."""
        summary = {m.metric_name: m.score for m in self.metrics}
        if self.human_scores:
            summary.update({k: v for k, v in self.human_scores.items() if isinstance(v, (int, float))})
        return summary

