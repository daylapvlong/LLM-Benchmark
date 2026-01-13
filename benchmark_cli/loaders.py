"""
Data loaders for reading evaluation pairs from various formats.
"""

import json
import csv
from pathlib import Path
from typing import List
import logging

from benchmark_cli.models import EvaluationPair

logger = logging.getLogger(__name__)


class DataLoader:
    """Load evaluation data from files."""
    
    @staticmethod
    def load_from_json(filepath: str) -> List[EvaluationPair]:
        """Load pairs from JSON file.
        
        Expected JSON format:
        [
            {
                "id": "pair1",
                "question": "...",
                "response": "...",
                "expected": "...",
                "metadata": {...}  # optional
            },
            ...
        ]
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            List of EvaluationPair objects
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {filepath}: {e}")
        
        if not isinstance(data, list):
            raise ValueError(f"JSON file must contain a list, got {type(data)}")
        
        pairs = []
        for i, item in enumerate(data):
            try:
                pair = EvaluationPair(
                    id=item.get('id', str(i)),
                    question=item['question'],
                    response=item['response'],
                    expected=item['expected'],
                    metadata=item.get('metadata')
                )
                pairs.append(pair)
            except KeyError as e:
                logger.warning(f"Skipping item {i}: missing required field {e}")
                continue
        
        logger.info(f"Loaded {len(pairs)} pairs from {filepath}")
        return pairs
    
    @staticmethod
    def load_from_csv(filepath: str) -> List[EvaluationPair]:
        """Load pairs from CSV file.
        
        Expected CSV format:
        id,question,response,expected
        pair1,"...","...","..."
        ...
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            List of EvaluationPair objects
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required columns are missing
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        pairs = []
        try:
            with open(path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                
                # Check required columns
                required_cols = {'question', 'response', 'expected'}
                if not required_cols.issubset(reader.fieldnames or []):
                    missing = required_cols - set(reader.fieldnames or [])
                    raise ValueError(f"CSV missing required columns: {missing}")
                
                for i, row in enumerate(reader):
                    try:
                        pair = EvaluationPair(
                            id=row.get('id', str(i)),
                            question=row['question'],
                            response=row['response'],
                            expected=row['expected']
                        )
                        pairs.append(pair)
                    except KeyError as e:
                        logger.warning(f"Skipping row {i}: missing required field {e}")
                        continue
        except Exception as e:
            raise ValueError(f"Error reading CSV file {filepath}: {e}")
        
        logger.info(f"Loaded {len(pairs)} pairs from {filepath}")
        return pairs
    
    @staticmethod
    def load(filepath: str) -> List[EvaluationPair]:
        """Load pairs from file (auto-detect format).
        
        Args:
            filepath: Path to file (JSON or CSV)
            
        Returns:
            List of EvaluationPair objects
            
        Raises:
            ValueError: If file format is not supported
        """
        path = Path(filepath)
        suffix = path.suffix.lower()
        
        if suffix == '.json':
            return DataLoader.load_from_json(filepath)
        elif suffix == '.csv':
            return DataLoader.load_from_csv(filepath)
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Use .json or .csv")

