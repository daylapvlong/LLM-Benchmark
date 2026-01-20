"""
Configuration management for API settings.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for API settings."""
    
    DEFAULT_CONFIG_FILE = "config.json"
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize config from file.
        
        Args:
            config_file: Path to config file (default: config.json in current directory)
        """
        self.config_file = config_file or self.DEFAULT_CONFIG_FILE
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        config_path = Path(self.config_file)
        
        # Try current directory first
        if not config_path.is_absolute():
            config_path = Path.cwd() / config_path
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"Loaded config from {config_path}")
                return config
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Error loading config file: {e}")
        
        # Try environment variables as fallback
        return self._load_from_env()
    
    def _load_from_env(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}
        
        if os.getenv('API_URL'):
            config['api_url'] = os.getenv('API_URL')
        if os.getenv('API_KEY'):
            config['api_key'] = os.getenv('API_KEY')
        if os.getenv('API_DELAY'):
            try:
                config['delay'] = float(os.getenv('API_DELAY'))
            except ValueError:
                pass
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value."""
        return self.config.get(key, default)
    
    def has_api_config(self) -> bool:
        """Check if API configuration is available."""
        return bool(self.config.get('api_url'))
    
    @property
    def api_url(self) -> Optional[str]:
        return self.config.get('api_url')
    
    @property
    def api_key(self) -> Optional[str]:
        return self.config.get('api_key')
    
    @property
    def delay(self) -> float:
        return self.config.get('delay', 0.5)
    
    @property
    def auto_fetch(self) -> bool:
        """Check if auto-fetch is enabled."""
        return self.config.get('auto_fetch', True)  # Default to True
