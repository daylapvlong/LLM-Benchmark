"""
API service for fetching bot responses.
"""

import requests
import time
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class APIService:
    """Service for making API calls to get bot responses."""
    
    def __init__(
        self,
        api_url: str,
        api_key: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        retry_attempts: int = 3,
        retry_delay: float = 1.0
    ):
        """Initialize API service.
        
        Args:
            api_url: Base URL for the API endpoint
            api_key: Optional API key for authentication
            headers: Optional custom headers
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts on failure
            retry_delay: Delay between retries in seconds
        """
        self.api_url = api_url
        self.api_key = api_key
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        
        # Setup headers
        self.headers = headers or {}
        if api_key:
            self.headers.setdefault('Authorization', f'Bearer {api_key}')
        self.headers.setdefault('Content-Type', 'application/json')
    
    def get_response(self, question: str, **kwargs) -> str:
        """Get bot response for a question.
        
        Args:
            question: The question to ask
            **kwargs: Additional parameters for the API call
            
        Returns:
            Bot response as string
            
        Raises:
            requests.RequestException: If API call fails after retries
        """
        payload = {
            'question': question,
            **kwargs
        }
        
        for attempt in range(self.retry_attempts):
            try:
                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=self.headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                # Extract response text (adjust based on your API format)
                data = response.json()
                return data.get('response') or data.get('answer') or data.get('text') or str(data)
                
            except requests.exceptions.RequestException as e:
                if attempt < self.retry_attempts - 1:
                    logger.warning(f"API call failed (attempt {attempt + 1}/{self.retry_attempts}): {e}")
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    logger.error(f"API call failed after {self.retry_attempts} attempts: {e}")
                    raise
        
        return ""
    
    def get_responses_batch(
        self,
        questions: list[str],
        delay_between_requests: float = 0.5,
        **kwargs
    ) -> list[tuple[str, str]]:
        """Get responses for multiple questions.
        
        Args:
            questions: List of questions
            delay_between_requests: Delay between API calls in seconds
            **kwargs: Additional parameters for API calls
            
        Returns:
            List of (question, response) tuples
        """
        results = []
        total = len(questions)
        
        for i, question in enumerate(questions, 1):
            logger.info(f"Fetching response {i}/{total}: {question[:50]}...")
            try:
                response = self.get_response(question, **kwargs)
                results.append((question, response))
                
                # Rate limiting
                if i < total:
                    time.sleep(delay_between_requests)
                    
            except Exception as e:
                logger.error(f"Failed to get response for question {i}: {e}")
                results.append((question, ""))  # Empty response on error
        
        return results
