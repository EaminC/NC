# AI Model Testing Framework

A modular and extensible framework for testing different AI models through the Infini-AI API. This framework provides a clean interface for interacting with various AI models and comparing their responses.

[![GitHub](https://img.shields.io/github/license/EaminC/NC)](https://github.com/EaminC/NC/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

## Features

- Support for multiple AI models:
  - DeepSeek R1
  - Qwen 32B
  - GLM-4 9B Chat
  - Llama 3.3 70B Instruct
  - And more...
- Easy configuration through JSON
- Simple and clean API interface
- Error handling and logging
- Modular and extensible architecture
- Type hints for better code maintainability

## Project Structure

```
ai-model-test/
├── src/                    # Source code
│   ├── services/          # Service layer
│   │   ├── __init__.py
│   │   └── model_service.py    # Core service implementation
│   └── utils/             # Utilities
│       ├── __init__.py
│       └── config.py           # Configuration management
├── tests/                 # Test scripts
│   ├── __init__.py
│   ├── test_one_model.py      # Single model test script
│   └── test_all_models.py     # All models test script
├── config/               # Configuration
│   └── config.json            # Model and API configuration
├── README.md
├── requirements.txt
└── .gitignore
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/EaminC/NC.git
cd NC
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your API key:
   - Copy `config/config.json` to `config/config.local.json`
   - Update the API key in `config/config.local.json`

## Usage

### Test Single Model

Use `test_one_model.py` to test a specific model:

```bash
# Basic usage
python tests/test_one_model.py --model deepseek-r1

# Custom message
python tests/test_one_model.py --model deepseek-r1 --message "Hello, please introduce yourself"
```

### Test All Models

Use `test_all_models.py` to test all configured models:

```bash
# Basic usage
python tests/test_all_models.py

# Custom message
python tests/test_all_models.py --message "Hello, please introduce yourself"
```

### Custom Testing

You can create your own test script using the ModelService:

```python
from src.services.model_service import ModelService

# Initialize service
service = ModelService()

# Chat with a specific model
response = service.chat("deepseek-r1", "Hello, how are you?")
print(response)
```

## Configuration

The `config/config.json` file contains all configuration settings:

```json
{
  "api": {
    "base_url": "https://cloud.infini-ai.com/maas/v1/chat/completions",
    "api_key": "your-api-key"
  },
  "models": {
    "model-name": {
      "name": "model-name",
      "description": "Model description"
    }
  }
}
```

### Adding New Models

To add a new model:

1. Add the model configuration to `config/config.json`
2. The framework will automatically detect and support the new model

## Development

### Project Structure

- `src/services/`: Contains the core service classes
  - `model_service.py`: Main service implementation
- `src/utils/`: Contains utility functions and helpers
  - `config.py`: Configuration management
- `tests/`: Contains test scripts
  - `test_one_model.py`: Single model test implementation
  - `test_all_models.py`: All models test implementation
- `config/`: Contains configuration files
  - `config.json`: Main configuration file

### Adding New Features

1. Create new service classes in `src/services/`
2. Add utility functions in `src/utils/`
3. Write tests in `tests/`
4. Update configuration in `config/`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/EaminC/NC/blob/main/LICENSE) file for details

## Acknowledgments

- Infini-AI for providing the API
- All contributors to this project

## Contact

EaminC - [@EaminC](https://github.com/EaminC)

Project Link: [https://github.com/EaminC/NC](https://github.com/EaminC/NC)
