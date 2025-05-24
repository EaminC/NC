import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.model_service import ModelService

def list_available_models():
    """List all available models with their descriptions"""
    service = ModelService()
    models = service.get_available_models()
    
    print("\nAvailable Models:")
    print("=" * 50)
    for model_name in models:
        model_info = service.get_model_info(model_name)
        print(f"\nModel: {model_name}")
        print(f"Description: {model_info['description']}")
    print("\n" + "=" * 50)

def test_single_model(model_name: str, message: str = "Who are you?"):
    """Test a single specified model"""
    service = ModelService()
    
    if model_name not in service.get_available_models():
        print(f"Error: Model {model_name} does not exist")
        return
        
    print(f"\nTesting model: {model_name}")
    print(f"Model description: {service.get_model_info(model_name)['description']}")
    print("Response:")
    try:
        response = service.chat(model_name, message)
        print(response)
    except Exception as e:
        print(f"Error: {str(e)}")
    print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description='Test a specific AI model')
    parser.add_argument('--model', help='Model name to test, e.g., --model deepseek-r1')
    parser.add_argument('--message', default="Who are you?", help='Message to send to the model')
    parser.add_argument('--list-models', action='store_true', help='List all available models')
    args = parser.parse_args()
    
    if args.list_models:
        list_available_models()
    elif args.model:
        test_single_model(args.model, args.message)
    else:
        parser.print_help()
        print("\nError: Either --model or --list-models must be specified")

if __name__ == "__main__":
    main() 