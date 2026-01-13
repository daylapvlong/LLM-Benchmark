"""
Benchmark CLI - A modular CLI tool for evaluating chatbot responses.
"""

__version__ = "0.1.0"

from benchmark_cli.models import (
    EvaluationPair,
    MetricResult,
    EvaluationResult
)
from benchmark_cli.metrics.registry import MetricRegistry
from benchmark_cli.metrics.builtin import (
    ExactMatchMetric,
    TokenOverlapMetric,
    LengthRatioMetric,
    ContainmentMetric
)
from benchmark_cli.engine import EvaluationEngine
from benchmark_cli.loaders import DataLoader
from benchmark_cli.reporters import ResultsReporter
from benchmark_cli.reviewers import HumanReviewer

__all__ = [
    "EvaluationPair",
    "MetricResult",
    "EvaluationResult",
    "MetricRegistry",
    "ExactMatchMetric",
    "TokenOverlapMetric",
    "LengthRatioMetric",
    "ContainmentMetric",
    "EvaluationEngine",
    "DataLoader",
    "ResultsReporter",
    "HumanReviewer",
]

