"""
Command-line interface for the evaluation tool.
"""

import argparse
import logging
import sys
from pathlib import Path

from benchmark_cli.models import EvaluationResult
from benchmark_cli.metrics.registry import MetricRegistry
from benchmark_cli.engine import EvaluationEngine
from benchmark_cli.loaders import DataLoader
from benchmark_cli.reporters import ResultsReporter
from benchmark_cli.reviewers import HumanReviewer


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


class EvaluationCLI:
    """Command-line interface for the evaluation tool."""
    
    def __init__(self):
        """Initialize CLI components."""
        self.registry = MetricRegistry()
        self.engine = EvaluationEngine(self.registry)
        self.reviewer = HumanReviewer()
        self.reporter = ResultsReporter()
    
    def run(self):
        """Main CLI entry point."""
        parser = argparse.ArgumentParser(
            description="Chatbot Evaluation CLI Tool",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Run automated evaluation
  python main.py data.json --mode auto --output results.json
  
  # Run with specific metrics
  python main.py data.json --metrics exact_match token_overlap
  
  # Hybrid mode with threshold
  python main.py data.json --mode hybrid --threshold 0.7 --output results.json
  
  # List available metrics
  python main.py --list-metrics
            """
        )
        
        parser.add_argument(
            'input_file',
            nargs='?',
            help='Input file (JSON or CSV) with evaluation pairs'
        )
        
        parser.add_argument(
            '--mode',
            choices=['auto', 'human', 'hybrid'],
            default='auto',
            help='Evaluation mode (default: auto)'
        )
        
        parser.add_argument(
            '--metrics',
            nargs='+',
            help='Specific metrics to use (default: all)'
        )
        
        parser.add_argument(
            '--threshold',
            type=float,
            help='Score threshold for human review in hybrid mode'
        )
        
        parser.add_argument(
            '--output',
            '-o',
            help='Output file path (JSON or CSV)'
        )
        
        parser.add_argument(
            '--list-metrics',
            action='store_true',
            help='List available metrics and exit'
        )
        
        parser.add_argument(
            '--verbose',
            '-v',
            action='store_true',
            help='Enable verbose logging'
        )
        
        parser.add_argument(
            '--no-expected',
            action='store_true',
            help='Hide expected answers during human review'
        )
        
        args = parser.parse_args()
        
        # Setup logging
        setup_logging(args.verbose)
        
        # List metrics
        if args.list_metrics:
            print("\nAvailable metrics:")
            for name in self.registry.list_metrics():
                metric = self.registry.get(name)
                print(f"  - {name}")
            return
        
        # Validate input file
        if not args.input_file:
            parser.error("input_file is required (unless using --list-metrics)")
        
        # Load data
        try:
            print(f"\nLoading data from: {args.input_file}")
            pairs = DataLoader.load(args.input_file)
            print(f"Loaded {len(pairs)} evaluation pairs.")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading data: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Validate metrics if specified
        if args.metrics:
            invalid = [m for m in args.metrics if self.registry.get(m) is None]
            if invalid:
                print(f"Warning: Invalid metrics: {invalid}", file=sys.stderr)
                print(f"Available metrics: {', '.join(self.registry.list_metrics())}")
        
        # Run evaluation
        results: list[EvaluationResult] = []
        
        if args.mode in ['auto', 'hybrid']:
            print(f"\nRunning automated evaluation...")
            results = self.engine.evaluate_batch(pairs, args.metrics)
            self.reporter.print_summary(results)
        
        if args.mode in ['human', 'hybrid']:
            print(f"\nStarting human review mode...")
            try:
                human_scores = self.reviewer.review_batch(
                    pairs,
                    show_expected=not args.no_expected,
                    threshold=args.threshold if args.mode == 'hybrid' else None,
                    results=results if args.mode == 'hybrid' else None
                )
                
                # Merge human scores with results
                if not results:
                    results = [EvaluationResult(pair.id, []) for pair in pairs]
                
                # Match human scores to results
                if args.mode == 'hybrid' and args.threshold:
                    # In hybrid mode with threshold, only some pairs were reviewed
                    reviewed_indices = []
                    for i, (pair, result) in enumerate(zip(pairs, results)):
                        if result.metrics:
                            avg_score = sum(m.score for m in result.metrics) / len(result.metrics)
                            if avg_score < args.threshold:
                                reviewed_indices.append(i)
                    
                    for idx, scores in zip(reviewed_indices, human_scores):
                        if idx < len(results):
                            results[idx].human_scores = scores
                else:
                    # All pairs reviewed
                    for result, scores in zip(results, human_scores):
                        result.human_scores = scores
            except KeyboardInterrupt:
                print("\n\nEvaluation interrupted by user.")
                sys.exit(1)
        
        # Save results
        if args.output:
            try:
                self.reporter.save(results, args.output)
            except ValueError as e:
                print(f"Error saving results: {e}", file=sys.stderr)
                sys.exit(1)
        elif args.mode == 'auto':
            print("\nNote: Use --output to save results to a file")

