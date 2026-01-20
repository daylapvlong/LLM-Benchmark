"""
Result reporters for generating evaluation reports.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any
import logging

from benchmark_cli.models.evaluation import EvaluationResult

logger = logging.getLogger(__name__)


class ResultsReporter:
    """Generate evaluation reports."""
    
    @staticmethod
    def print_summary(results: List[EvaluationResult]):
        """Print summary statistics to console.
        
        Args:
            results: List of evaluation results
        """
        if not results:
            print("No results to report.")
            return
        
        print("\n" + "="*70)
        print("EVALUATION SUMMARY")
        print("="*70)
        
        # Aggregate metrics
        if not results[0].metrics:
            print("\nNo metrics computed.")
            return
        
        metric_names = [m.metric_name for m in results[0].metrics]
        aggregates: Dict[str, List[float]] = {name: [] for name in metric_names}
        
        for result in results:
            for metric in result.metrics:
                aggregates[metric.metric_name].append(metric.score)
        
        print(f"\nTotal responses evaluated: {len(results)}\n")
        print(f"{'Metric':<30} {'Mean':<10} {'Min':<10} {'Max':<10} {'Std':<10}")
        print("-"*70)
        
        for name, scores in aggregates.items():
            if not scores:
                continue
            mean_score = sum(scores) / len(scores)
            min_score = min(scores)
            max_score = max(scores)
            # Calculate standard deviation
            variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
            std_score = variance ** 0.5
            print(f"{name:<30} {mean_score:<10.3f} {min_score:<10.3f} {max_score:<10.3f} {std_score:<10.3f}")
    
    @staticmethod
    def save_to_json(results: List[EvaluationResult], filepath: str):
        """Save detailed results to JSON.
        
        Args:
            results: List of evaluation results
            filepath: Output file path
        """
        output = []
        for result in results:
            item: Dict[str, Any] = {
                'id': result.pair_id,
                'metrics': {m.metric_name: m.score for m in result.metrics},
                'details': {m.metric_name: m.details for m in result.metrics if m.details}
            }
            if result.human_scores:
                item['human_scores'] = result.human_scores
            output.append(item)
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Detailed results saved to: {filepath}")
        print(f"\nDetailed results saved to: {filepath}")
    
    @staticmethod
    def save_to_csv(results: List[EvaluationResult], filepath: str):
        """Save results summary to CSV.
        
        Args:
            results: List of evaluation results
            filepath: Output file path
        """
        if not results:
            logger.warning("No results to save")
            return
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8', newline='') as f:
            # Get all metric names
            metric_names = [m.metric_name for m in results[0].metrics] if results[0].metrics else []
            
            # Collect all human score keys
            human_score_keys = set()
            for result in results:
                if result.human_scores:
                    human_score_keys.update(result.human_scores.keys())
            
            fieldnames = ['id'] + metric_names + sorted(human_score_keys)
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                row: Dict[str, Any] = {'id': result.pair_id}
                row.update(result.get_summary())
                writer.writerow(row)
        
        logger.info(f"Summary CSV saved to: {filepath}")
        print(f"Summary CSV saved to: {filepath}")
    
    @staticmethod
    def save(results: List[EvaluationResult], filepath: str):
        """Save results to file (auto-detect format).
        
        Args:
            results: List of evaluation results
            filepath: Output file path (JSON or CSV)
            
        Raises:
            ValueError: If file format is not supported
        """
        path = Path(filepath)
        suffix = path.suffix.lower()
        
        if suffix == '.json':
            ResultsReporter.save_to_json(results, filepath)
        elif suffix == '.csv':
            ResultsReporter.save_to_csv(results, filepath)
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Use .json or .csv")
