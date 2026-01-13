"""
Built-in evaluation metrics.
"""

from benchmark_cli.metrics.base import Metric
from benchmark_cli.models import MetricResult


class ExactMatchMetric(Metric):
    """Exact string match metric."""
    
    @property
    def name(self) -> str:
        return "exact_match"
    
    def compute(self, response: str, expected: str) -> MetricResult:
        """Compute exact match score (case-insensitive)."""
        score = 1.0 if response.strip().lower() == expected.strip().lower() else 0.0
        return MetricResult(
            metric_name=self.name,
            score=score,
            details={"match": score == 1.0}
        )


class TokenOverlapMetric(Metric):
    """Simple token overlap metric (ROUGE-like F1 score)."""
    
    @property
    def name(self) -> str:
        return "token_overlap"
    
    def compute(self, response: str, expected: str) -> MetricResult:
        """Compute token overlap F1 score."""
        resp_tokens = set(response.lower().split())
        exp_tokens = set(expected.lower().split())
        
        if not exp_tokens:
            return MetricResult(self.name, 0.0, details={"error": "empty expected"})
        
        overlap = resp_tokens & exp_tokens
        
        if not resp_tokens:
            return MetricResult(self.name, 0.0, details={"error": "empty response"})
        
        recall = len(overlap) / len(exp_tokens)
        precision = len(overlap) / len(resp_tokens)
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return MetricResult(
            metric_name=self.name,
            score=f1,
            details={
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "overlap_tokens": len(overlap),
                "response_tokens": len(resp_tokens),
                "expected_tokens": len(exp_tokens)
            }
        )


class LengthRatioMetric(Metric):
    """Evaluates response length relative to expected."""
    
    @property
    def name(self) -> str:
        return "length_ratio"
    
    def compute(self, response: str, expected: str) -> MetricResult:
        """Compute length similarity score."""
        resp_len = len(response.split())
        exp_len = len(expected.split())
        
        if exp_len == 0:
            return MetricResult(
                self.name, 
                0.0, 
                details={"error": "empty expected", "response_words": resp_len}
            )
        
        ratio = resp_len / exp_len
        # Score closer to 1.0 for similar lengths (penalize deviation from 1.0)
        score = 1.0 - min(abs(ratio - 1.0), 1.0)
        
        return MetricResult(
            metric_name=self.name,
            score=score,
            details={
                "response_words": resp_len,
                "expected_words": exp_len,
                "ratio": ratio
            }
        )


class ContainmentMetric(Metric):
    """Checks if response contains key phrases from expected."""
    
    @property
    def name(self) -> str:
        return "key_phrase_containment"
    
    def compute(self, response: str, expected: str) -> MetricResult:
        """Compute key phrase containment score."""
        # Extract phrases (3+ char words) from expected
        exp_words = [w for w in expected.lower().split() if len(w) >= 3]
        resp_lower = response.lower()
        
        if not exp_words:
            return MetricResult(
                self.name, 
                0.0, 
                details={"error": "no key phrases in expected"}
            )
        
        contained = sum(1 for word in exp_words if word in resp_lower)
        score = contained / len(exp_words)
        
        return MetricResult(
            metric_name=self.name,
            score=score,
            details={
                "key_phrases_found": contained,
                "total_key_phrases": len(exp_words)
            }
        )

