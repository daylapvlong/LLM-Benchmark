"""
Benchmark CLI - A modular CLI tool for evaluating chatbot responses.
"""

__version__ = "0.1.0"

# Models
from benchmark_cli.models import (
    EvaluationPair,
    MetricResult,
    EvaluationResult,
    QuestionInput
)

# Metrics
from benchmark_cli.metrics.registry import MetricRegistry
from benchmark_cli.metrics.builtin import (
    ExactMatchMetric,
    TokenOverlapMetric,
    LengthRatioMetric,
    ContainmentMetric
)

# Services
from benchmark_cli.services.evaluation_service import EvaluationService
from benchmark_cli.services.api_service import APIService
from benchmark_cli.services.review_service import ReviewService
from benchmark_cli.services.fetch_service import FetchService

# Helpers
from benchmark_cli.helpers.loaders import DataLoader
from benchmark_cli.helpers.reporters import ResultsReporter
from benchmark_cli.helpers.response_appender import ResponseAppender
from benchmark_cli.helpers.config import Config

# Interfaces
from benchmark_cli.interfaces.cli import EvaluationCLI

__all__ = [
    # Models
    "EvaluationPair",
    "MetricResult",
    "EvaluationResult",
    "QuestionInput",
    # Metrics
    "MetricRegistry",
    "ExactMatchMetric",
    "TokenOverlapMetric",
    "LengthRatioMetric",
    "ContainmentMetric",
    # Services
    "EvaluationService",
    "APIService",
    "ReviewService",
    "FetchService",
    # Helpers
    "DataLoader",
    "ResultsReporter",
    "ResponseAppender",
    "Config",
    # Interfaces
    "EvaluationCLI",
]
