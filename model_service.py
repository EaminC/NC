import json
import requests
from typing import Dict, List, Optional

class ModelService:
    def __init__(self, config_path: str = "config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.base_url = self.config['api']['base_url']
        self.api_key = self.config['api']['api_key']
        self.models = self.config['models']
        
    def get_headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, model_name: str, message: str) -> Dict:
        """Chat with specified model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} does not exist")
            
        data = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": message}
            ]
        }
        
        response = requests.post(
            self.base_url,
            headers=self.get_headers(),
            json=data
        )
        return response.json()
    
    def get_available_models(self) -> List[str]:
        """Get all available model names"""
        return list(self.models.keys())
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """Get model information"""
        return self.models.get(model_name) 