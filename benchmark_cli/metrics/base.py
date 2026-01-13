"""
Base metric interface.
"""

from abc import ABC, abstractmethod
from benchmark_cli.models import MetricResult


class Metric(ABC):
    """Base class for evaluation metrics."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Metric name."""
        pass
    
    @abstractmethod
    def compute(self, response: str, expected: str) -> MetricResult:
        """Compute metric score.
        
        Args:
            response: The chatbot response to evaluate
            expected: The expected/ground truth response
            
        Returns:
            MetricResult with score and optional details
        """
        pass

