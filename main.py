"""
Main entry point for the Benchmark CLI tool.
"""

import sys
from benchmark_cli.interfaces.cli import EvaluationCLI
from benchmark_cli.helpers.config import Config
from benchmark_cli.auto_fetch import run_auto_fetch


def main():
    """Main entry point - auto-fetch by default if configured."""
    config = Config()
    
    # If API is configured, run fetch mode automatically
    if config.has_api_config() and config.auto_fetch:
        if run_auto_fetch(config):
            return  # Exit after auto-fetch
    
    # Otherwise, run normal CLI
    cli = EvaluationCLI()
    cli.run()


if __name__ == '__main__':
    main()
