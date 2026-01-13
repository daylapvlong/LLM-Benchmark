"""
Evaluation engine for running metrics on evaluation pairs.
"""

from typing import List, Optional
import logging

from benchmark_cli.models import EvaluationPair, EvaluationResult
from benchmark_cli.metrics.registry import MetricRegistry

logger = logging.getLogger(__name__)


class EvaluationEngine:
    """Core evaluation engine."""
    
    def __init__(self, registry: MetricRegistry):
        """Initialize evaluation engine.
        
        Args:
            registry: Metric registry containing available metrics
        """
        self.registry = registry
    
    def evaluate_pair(
        self,
        pair: EvaluationPair,
        metric_names: Optional[List[str]] = None
    ) -> EvaluationResult:
        """Evaluate a single response pair.
        
        Args:
            pair: Evaluation pair to evaluate
            metric_names: Optional list of specific metric names to use
            
        Returns:
            EvaluationResult with all metric scores
        """
        # Determine which metrics to use
        if metric_names:
            metrics = self.registry.get_multiple(metric_names)
            if not metrics:
                logger.warning(f"No valid metrics found from {metric_names}")
                return EvaluationResult(pair_id=pair.id, metrics=[])
        else:
            metrics = self.registry.get_all()
            if not metrics:
                logger.warning("No metrics registered in registry")
                return EvaluationResult(pair_id=pair.id, metrics=[])
        
        # Compute all metrics
        results = []
        for metric in metrics:
            try:
                result = metric.compute(pair.response, pair.expected)
                results.append(result)
            except Exception as e:
                logger.error(f"Error computing metric '{metric.name}' for pair '{pair.id}': {e}")
                # Continue with other metrics even if one fails
        
        return EvaluationResult(
            pair_id=pair.id,
            metrics=results
        )
    
    def evaluate_batch(
        self,
        pairs: List[EvaluationPair],
        metric_names: Optional[List[str]] = None
    ) -> List[EvaluationResult]:
        """Evaluate multiple pairs.
        
        Args:
            pairs: List of evaluation pairs
            metric_names: Optional list of specific metric names to use
            
        Returns:
            List of evaluation results
        """
        logger.info(f"Evaluating {len(pairs)} pairs")
        return [self.evaluate_pair(pair, metric_names) for pair in pairs]

