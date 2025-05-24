import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.model_service import ModelService

def test_single_model(model_name: str, message: str = "Who are you?"):
    """测试单个指定的模型"""
    service = ModelService()
    
    if model_name not in service.get_available_models():
        print(f"错误: 模型 {model_name} 不存在")
        return
        
    print(f"\n测试模型: {model_name}")
    print(f"模型描述: {service.get_model_info(model_name)['description']}")
    print("响应:")
    try:
        response = service.chat(model_name, message)
        print(response)
    except Exception as e:
        print(f"错误: {str(e)}")
    print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description='测试单个指定的AI模型')
    parser.add_argument('--model', required=True, help='要测试的模型名称，例如：--model deepseek-r1')
    parser.add_argument('--message', default="Who are you?", help='要发送给模型的消息')
    args = parser.parse_args()
    
    test_single_model(args.model, args.message)

if __name__ == "__main__":
    main() 