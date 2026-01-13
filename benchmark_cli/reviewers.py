"""
Human-in-the-loop review interfaces.
"""

from typing import List, Dict, Any, Optional
import logging

from benchmark_cli.models import EvaluationPair, EvaluationResult

logger = logging.getLogger(__name__)


class HumanReviewer:
    """Interactive human review interface."""
    
    CRITERIA = {
        "correctness": "Is the response factually correct? (1-5)",
        "relevance": "Is the response relevant to the question? (1-5)",
        "completeness": "Does the response cover all key points? (1-5)",
        "tone": "Is the tone appropriate? (1-5)"
    }
    
    def review_pair(self, pair: EvaluationPair, show_expected: bool = True) -> Dict[str, Any]:
        """Conduct interactive review of a single pair.
        
        Args:
            pair: Evaluation pair to review
            show_expected: Whether to show expected answer
            
        Returns:
            Dictionary with scores and optional comments
        """
        print("\n" + "="*70)
        print(f"REVIEW ID: {pair.id}")
        print("="*70)
        print(f"\nQuestion:\n  {pair.question}\n")
        print(f"Response:\n  {pair.response}\n")
        
        if show_expected:
            print(f"Expected:\n  {pair.expected}\n")
        
        print("-"*70)
        print("Please rate the following criteria:\n")
        
        scores: Dict[str, Any] = {}
        for criterion, prompt in self.CRITERIA.items():
            while True:
                try:
                    value = input(f"{prompt}: ").strip()
                    if value.lower() == 'skip':
                        scores[criterion] = None
                        break
                    score = int(value)
                    if 1 <= score <= 5:
                        scores[criterion] = score
                        break
                    print("  Please enter a number between 1 and 5 (or 'skip')")
                except (ValueError, KeyboardInterrupt):
                    if KeyboardInterrupt:
                        raise
                    print("  Invalid input. Please try again.")
        
        # Optional comments
        try:
            comments = input("\nAdditional comments (or press Enter to skip): ").strip()
            if comments:
                scores['comments'] = comments
        except KeyboardInterrupt:
            pass
        
        return scores
    
    def review_batch(
        self,
        pairs: List[EvaluationPair],
        show_expected: bool = True,
        threshold: Optional[float] = None,
        results: Optional[List[EvaluationResult]] = None
    ) -> List[Dict[str, Any]]:
        """Review multiple pairs, optionally filtered by threshold.
        
        Args:
            pairs: List of evaluation pairs
            show_expected: Whether to show expected answers
            threshold: Optional score threshold (only review pairs below threshold)
            results: Optional evaluation results for threshold filtering
            
        Returns:
            List of human review scores (one per pair)
        """
        # Filter pairs if threshold provided
        if threshold is not None and results is not None:
            filtered_pairs = []
            filtered_results = []
            for pair, result in zip(pairs, results):
                if result.metrics:
                    avg_score = sum(m.score for m in result.metrics) / len(result.metrics)
                    if avg_score < threshold:
                        filtered_pairs.append(pair)
                        filtered_results.append(result)
            pairs = filtered_pairs
            results = filtered_results
            print(f"\n{len(pairs)} pairs below threshold {threshold} will be reviewed.")
        
        human_scores = []
        for i, pair in enumerate(pairs, 1):
            print(f"\n[{i}/{len(pairs)}]")
            try:
                scores = self.review_pair(pair, show_expected)
                human_scores.append(scores)
            except KeyboardInterrupt:
                logger.info("Review interrupted by user")
                print("\n\nReview interrupted. Partial results will be saved.")
                break
        
        return human_scores

