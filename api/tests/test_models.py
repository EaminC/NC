import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.model_service import ModelService

def main():
    # Initialize service
    service = ModelService()
    
    # Test all models
    message = "Who are you?"
    for model_name in service.get_available_models():
        print(f"\nTesting model: {model_name}")
        print(f"Model description: {service.get_model_info(model_name)['description']}")
        print("Response:")
        try:
            response = service.chat(model_name, message)
            print(response)
        except Exception as e:
            print(f"Error: {str(e)}")
        print("-" * 50)

if __name__ == "__main__":
    main() 