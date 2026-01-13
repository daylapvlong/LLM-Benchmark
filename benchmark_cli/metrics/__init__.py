"""
Metrics package for evaluation metrics.
"""

from benchmark_cli.metrics.base import Metric
from benchmark_cli.metrics.registry import MetricRegistry
from benchmark_cli.metrics.builtin import (
    ExactMatchMetric,
    TokenOverlapMetric,
    LengthRatioMetric,
    ContainmentMetric
)

__all__ = [
    "Metric",
    "MetricRegistry",
    "ExactMatchMetric",
    "TokenOverlapMetric",
    "LengthRatioMetric",
    "ContainmentMetric",
]

