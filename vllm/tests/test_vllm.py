import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from vllm.src.services.vllm_service import VLLMService

def show_gpu_info(service: VLLMService):
    """显示所有配置的GPU信息"""
    print("\n配置的GPU信息:")
    print("-" * 50)
    for gpu_id in service.config.get_available_gpus():
        gpu_config = service.config.get_gpu_config(gpu_id)
        print(f"GPU {gpu_id}:")
        print(f"  模型: {gpu_config['model']}")
        print(f"  描述: {gpu_config['description']}")
        print(f"  张量并行度: {gpu_config['tensor_parallel_size']}")
        print(f"  GPU内存使用率: {gpu_config['gpu_memory_utilization']}")
        print(f"  最大模型长度: {gpu_config['max_model_len']}")
        print("-" * 50)

def test_vllm(gpu_id: str, message: str = "Hello, please introduce yourself"):
    """Test vLLM model on specific GPU"""
    service = VLLMService()
    
    # 显示GPU信息
    show_gpu_info(service)
    
    print(f"\n正在加载 GPU {gpu_id} 上的模型...")
    service.load_model(gpu_id)
    
    print("\n生成回答...")
    try:
        response = service.generate(message, gpu_id)
        print("\n回答:")
        print(response)
    except Exception as e:
        print(f"错误: {str(e)}")
    print("-" * 50)

def test_all_gpus(message: str = "Hello, please introduce yourself"):
    """Test vLLM models on all configured GPUs"""
    service = VLLMService()
    
    # 显示GPU信息
    show_gpu_info(service)
    
    print("\n正在加载所有配置的GPU上的模型...")
    service.load_all_models()
    
    for gpu_id in service.config.get_available_gpus():
        print(f"\n测试 GPU {gpu_id}...")
        try:
            response = service.generate(message, gpu_id)
            print("\n回答:")
            print(response)
        except Exception as e:
            print(f"错误: {str(e)}")
        print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description='测试 vLLM 模型')
    parser.add_argument('--gpu', help='要测试的GPU ID (如果不指定，将测试所有配置的GPU)')
    parser.add_argument('--message', default="Hello, please introduce yourself", help='发送给模型的消息')
    args = parser.parse_args()
    
    if args.gpu:
        test_vllm(args.gpu, args.message)
    else:
        test_all_gpus(args.message)

if __name__ == "__main__":
    main() 