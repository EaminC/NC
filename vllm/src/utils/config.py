import json
import os
from typing import Dict, Optional, List

class Config:
    def __init__(self, config_path: str = "vllm/config/config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @property
    def server_config(self) -> Dict:
        """Get server configuration"""
        return self.config.get('server', {})
    
    @property
    def client_config(self) -> Dict:
        """Get client configuration"""
        return self.config.get('client', {})
    
    def get_gpu_config(self, gpu_id: str) -> Optional[Dict]:
        """Get configuration for specific GPU"""
        return self.config.get('gpus', {}).get(gpu_id)
    
    def get_all_gpu_configs(self) -> Dict[str, Dict]:
        """Get configurations for all GPUs"""
        return self.config.get('gpus', {})
    
    def get_available_gpus(self) -> List[str]:
        """Get list of available GPU IDs"""
        return list(self.config.get('gpus', {}).keys())
    
    def get_gpu_by_model(self, model_name: str) -> Optional[str]:
        """根据模型名称查找GPU ID"""
        for gpu_id, gpu_config in self.get_all_gpu_configs().items():
            if model_name.lower() in gpu_config.get('model', '').lower():
                return gpu_id
        return None
    
    def get_gpu_by_port(self, port: int) -> Optional[str]:
        """根据端口号查找GPU ID"""
        for gpu_id, gpu_config in self.get_all_gpu_configs().items():
            if gpu_config.get('port') == port:
                return gpu_id
        return None
    
    @property
    def model_config(self) -> Dict:
        """Get model configuration"""
        return self.config.get('model', {}) 