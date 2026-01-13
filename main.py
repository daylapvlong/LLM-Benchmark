"""
Main entry point for the Benchmark CLI tool.
"""

from benchmark_cli.cli import EvaluationCLI


def main():
    """Main entry point."""
    cli = EvaluationCLI()
    cli.run()


if __name__ == '__main__':
    main()
