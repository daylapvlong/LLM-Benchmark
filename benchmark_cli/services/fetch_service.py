"""
Service for fetching bot responses and appending to output files.
"""

import json
import logging
from pathlib import Path
from typing import List, Optional

from benchmark_cli.helpers.loaders import DataLoader
from benchmark_cli.models.question import QuestionInput
from benchmark_cli.services.api_service import APIService
from benchmark_cli.helpers.response_appender import ResponseAppender

logger = logging.getLogger(__name__)


class FetchService:
    """Service to fetch bot responses and append to output files."""
    
    def __init__(
        self,
        api_url: str,
        api_key: Optional[str] = None,
        delay_between_requests: float = 0.5
    ):
        """Initialize fetch service.
        
        Args:
            api_url: API endpoint URL
            api_key: Optional API key
            delay_between_requests: Delay between API calls
        """
        self.api_service = APIService(api_url, api_key)
        self.delay_between_requests = delay_between_requests
    
    def fetch_and_append(
        self,
        input_file: str,
        output_file: str,
        append_mode: bool = True
    ):
        """Load questions, fetch responses, and append to output.
        
        Args:
            input_file: Path to input file with questions
            output_file: Path to output file
            append_mode: If True, append to existing file; if False, overwrite
        """
        # Load questions
        logger.info(f"Loading questions from {input_file}")
        questions = DataLoader.load_questions(input_file)
        
        if not questions:
            logger.warning("No questions found in input file")
            return
        
        logger.info(f"Found {len(questions)} questions")
        
        # Fetch responses
        question_texts = [q.question for q in questions]
        responses = self.api_service.get_responses_batch(
            question_texts,
            delay_between_requests=self.delay_between_requests
        )
        
        # Prepare output data
        output_path = Path(output_file)
        suffix = output_path.suffix.lower()
        
        if suffix == '.json':
            results = []
            for question, (q_text, response) in zip(questions, responses):
                entry = {
                    'id': question.id,
                    'question': q_text,
                    'response': response
                }
                if question.expected:
                    entry['expected'] = question.expected
                if question.metadata:
                    entry['metadata'] = question.metadata
                results.append(entry)
            
            if append_mode:
                ResponseAppender.append_batch_to_json(output_file, results)
            else:
                # Overwrite mode
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
        
        elif suffix == '.csv':
            results = []
            for question, (q_text, response) in zip(questions, responses):
                entry = {
                    'id': question.id,
                    'question': q_text,
                    'response': response
                }
                if question.expected:
                    entry['expected'] = question.expected
                results.append(entry)
            
            if append_mode:
                ResponseAppender.append_batch_to_csv(output_file, results)
            else:
                # For overwrite, we need to write header first
                ResponseAppender.append_batch_to_csv(output_file, results)
        
        logger.info(f"Completed fetching {len(responses)} responses")
