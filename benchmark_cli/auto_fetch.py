"""
Automatic fetch service that runs by default.
"""

import logging
from pathlib import Path
from typing import Optional
from benchmark_cli.helpers.config import Config
from benchmark_cli.services.fetch_service import FetchService
from benchmark_cli.helpers.loaders import DataLoader

logger = logging.getLogger(__name__)


def run_auto_fetch(config: Optional[Config] = None) -> bool:
    """Run automatic fetch if conditions are met.
    
    Returns:
        True if auto-fetch was executed, False otherwise
    """
    if config is None:
        config = Config()
    
    if not config.has_api_config():
        return False
    
    # Default directories
    inputs_dir = Path("inputs")
    outputs_dir = Path("outputs")
    
    if not inputs_dir.exists():
        logger.debug("inputs/ directory not found")
        return False
    
    outputs_dir.mkdir(exist_ok=True)
    
    # Find all input files
    input_files = sorted(list(inputs_dir.glob("*.json")) + list(inputs_dir.glob("*.csv")))
    
    if not input_files:
        logger.debug("No input files found")
        return False
    
    print("\n" + "="*70)
    print("🤖 AUTO-FETCH MODE - Fetching Bot Responses")
    print("="*70)
    print(f"API: {config.api_url}")
    print(f"Input files: {len(input_files)}")
    print("-"*70)
    
    service = FetchService(
        api_url=config.api_url,
        api_key=config.api_key,
        delay_between_requests=config.delay
    )
    
    processed = 0
    for input_file in input_files:
        try:
            # Try to load as questions
            questions = DataLoader.load_questions(str(input_file))
            
            if not questions:
                logger.debug(f"No questions found in {input_file.name}")
                continue
            
            output_file = outputs_dir / f"{input_file.stem}_responses{input_file.suffix}"
            
            print(f"\n📄 Processing: {input_file.name}")
            print(f"   Questions: {len(questions)}")
            
            service.fetch_and_append(
                str(input_file),
                str(output_file),
                append_mode=True
            )
            
            print(f"   ✓ Saved to: {output_file.name}")
            processed += 1
            
        except Exception as e:
            logger.error(f"Error processing {input_file}: {e}")
            print(f"   ✗ Error: {e}")
            continue
    
    if processed > 0:
        print("\n" + "="*70)
        print(f"✓ Successfully processed {processed} file(s)")
        print("="*70)
        return True
    
    return False
