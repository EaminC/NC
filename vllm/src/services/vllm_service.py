import argparse
from typing import Dict, Optional
from vllm import LLM, SamplingParams
from ..utils.config import Config

class VLLMService:
    def __init__(self, config_path: str = "vllm/config/config.json"):
        self.config = Config(config_path)
        self.server_config = self.config.server_config
        self.llms = {}  # Dictionary to store LLM instances for each GPU
        
    def load_model(self, gpu_id: str):
        """Load model using vLLM for specific GPU"""
        gpu_config = self.config.get_gpu_config(gpu_id)
        if not gpu_config:
            raise ValueError(f"No configuration found for GPU {gpu_id}")
            
        self.llms[gpu_id] = LLM(
            model=gpu_config["model"],
            tensor_parallel_size=gpu_config["tensor_parallel_size"],
            gpu_memory_utilization=gpu_config["gpu_memory_utilization"],
            max_model_len=gpu_config["max_model_len"]
        )
        
    def load_all_models(self):
        """Load models for all configured GPUs"""
        for gpu_id in self.config.get_available_gpus():
            self.load_model(gpu_id)
        
    def generate(self, prompt: str, gpu_id: str, sampling_params: Optional[Dict] = None) -> str:
        """Generate response using loaded model on specific GPU"""
        if gpu_id not in self.llms:
            raise RuntimeError(f"Model not loaded for GPU {gpu_id}. Call load_model first.")
            
        if sampling_params is None:
            sampling_params = SamplingParams(
                temperature=0.7,
                top_p=0.95,
                max_tokens=2048
            )
            
        outputs = self.llms[gpu_id].generate(prompt, sampling_params)
        return outputs[0].outputs[0].text

def main():
    parser = argparse.ArgumentParser(description='Start vLLM server')
    parser.add_argument('--gpu', help='GPU ID to use (if not specified, will use all configured GPUs)')
    parser.add_argument('--port', type=int, default=8000, help='Server port')
    args = parser.parse_args()
    
    service = VLLMService()
    
    if args.gpu:
        print(f"Loading model for GPU {args.gpu}...")
        service.load_model(args.gpu)
    else:
        print("Loading models for all configured GPUs...")
        service.load_all_models()
    
    # TODO: Implement server logic here
    print(f"Models loaded successfully. Ready to serve on port {args.port}")

if __name__ == "__main__":
    main() 