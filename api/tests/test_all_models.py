import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.model_service import ModelService

def test_all_models(message: str = "Who are you?"):
    """测试所有可用的模型"""
    service = ModelService()
    
    print(f"开始测试所有可用模型，共 {len(service.get_available_models())} 个模型")
    print("=" * 50)
    
    for model_name in service.get_available_models():
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
    parser = argparse.ArgumentParser(description='测试所有可用的AI模型')
    parser.add_argument('--message', default="Who are you?", help='要发送给模型的消息')
    args = parser.parse_args()
    
    test_all_models(args.message)

if __name__ == "__main__":
    main() 