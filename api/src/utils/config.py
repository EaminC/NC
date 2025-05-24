import json
import os
from typing import Dict

class Config:
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @property
    def api_config(self) -> Dict:
        """Get API configuration"""
        return self.config.get('api', {})
    
    @property
    def models(self) -> Dict:
        """Get models configuration"""
        return self.config.get('models', {})
    
    def get_model_info(self, model_name: str) -> Dict:
        """Get specific model information"""
        return self.models.get(model_name, {}) 