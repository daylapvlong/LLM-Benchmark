"""
Service for appending bot responses to output files.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ResponseAppender:
    """Append bot responses to output files."""
    
    @staticmethod
    def append_to_json(
        filepath: str,
        question_id: str,
        question: str,
        response: str,
        expected: str = None,
        metadata: Dict[str, Any] = None
    ):
        """Append a response to JSON file.
        
        Creates file if it doesn't exist, appends if it does.
        """
        path = Path(filepath)
        
        # Load existing data or create new list
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except (json.JSONDecodeError, FileNotFoundError):
                data = []
        else:
            data = []
        
        # Create new entry
        entry = {
            'id': question_id,
            'question': question,
            'response': response,
        }
        
        if expected:
            entry['expected'] = expected
        if metadata:
            entry['metadata'] = metadata
        
        # Append and save
        data.append(entry)
        
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.debug(f"Appended response to {filepath}")
    
    @staticmethod
    def append_to_csv(
        filepath: str,
        question_id: str,
        question: str,
        response: str,
        expected: str = None
    ):
        """Append a response to CSV file.
        
        Creates file with headers if it doesn't exist.
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        file_exists = path.exists()
        
        with open(path, 'a', encoding='utf-8', newline='') as f:
            fieldnames = ['id', 'question', 'response']
            if expected:
                fieldnames.append('expected')
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header if new file
            if not file_exists:
                writer.writeheader()
            
            row = {
                'id': question_id,
                'question': question,
                'response': response
            }
            if expected:
                row['expected'] = expected
            
            writer.writerow(row)
        
        logger.debug(f"Appended response to {filepath}")
    
    @staticmethod
    def append_batch_to_json(
        filepath: str,
        results: List[Dict[str, Any]]
    ):
        """Append multiple responses to JSON file at once."""
        path = Path(filepath)
        
        # Load existing data
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except (json.JSONDecodeError, FileNotFoundError):
                data = []
        else:
            data = []
        
        # Append all entries
        data.extend(results)
        
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Appended {len(results)} responses to {filepath}")
    
    @staticmethod
    def append_batch_to_csv(
        filepath: str,
        results: List[Dict[str, Any]]
    ):
        """Append multiple responses to CSV file at once."""
        if not results:
            return
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        file_exists = path.exists()
        
        # Determine fieldnames from first result
        fieldnames = ['id', 'question', 'response']
        if any('expected' in r for r in results):
            fieldnames.append('expected')
        
        with open(path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            for result in results:
                row = {
                    'id': result.get('id', ''),
                    'question': result.get('question', ''),
                    'response': result.get('response', '')
                }
                if 'expected' in result and 'expected' in fieldnames:
                    row['expected'] = result.get('expected', '')
                
                writer.writerow(row)
        
        logger.info(f"Appended {len(results)} responses to {filepath}")
