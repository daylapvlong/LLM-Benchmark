"""
Metric registry for managing available metrics.
"""

from typing import Dict, List, Optional
from benchmark_cli.metrics.base import Metric
from benchmark_cli.metrics.builtin import (
    ExactMatchMetric,
    TokenOverlapMetric,
    LengthRatioMetric,
    ContainmentMetric
)


class MetricRegistry:
    """Registry for available metrics."""
    
    def __init__(self, auto_register_defaults: bool = True):
        """Initialize registry.
        
        Args:
            auto_register_defaults: If True, automatically register built-in metrics
        """
        self._metrics: Dict[str, Metric] = {}
        if auto_register_defaults:
            self._register_defaults()
    
    def _register_defaults(self):
        """Register default metrics."""
        defaults = [
            ExactMatchMetric(),
            TokenOverlapMetric(),
            LengthRatioMetric(),
            ContainmentMetric()
        ]
        for metric in defaults:
            self.register(metric)
    
    def register(self, metric: Metric):
        """Register a new metric.
        
        Args:
            metric: Metric instance to register
            
        Raises:
            ValueError: If metric name already exists
        """
        if metric.name in self._metrics:
            raise ValueError(f"Metric '{metric.name}' is already registered")
        self._metrics[metric.name] = metric
    
    def unregister(self, name: str) -> bool:
        """Unregister a metric by name.
        
        Args:
            name: Name of metric to unregister
            
        Returns:
            True if metric was removed, False if not found
        """
        if name in self._metrics:
            del self._metrics[name]
            return True
        return False
    
    def get(self, name: str) -> Optional[Metric]:
        """Get metric by name.
        
        Args:
            name: Metric name
            
        Returns:
            Metric instance or None if not found
        """
        return self._metrics.get(name)
    
    def list_metrics(self) -> List[str]:
        """List all available metric names.
        
        Returns:
            List of metric names
        """
        return list(self._metrics.keys())
    
    def get_all(self) -> List[Metric]:
        """Get all registered metrics.
        
        Returns:
            List of all registered metric instances
        """
        return list(self._metrics.values())
    
    def get_multiple(self, names: List[str]) -> List[Metric]:
        """Get multiple metrics by name.
        
        Args:
            names: List of metric names
            
        Returns:
            List of metric instances (None values filtered out)
        """
        metrics = [self.get(name) for name in names]
        return [m for m in metrics if m is not None]

