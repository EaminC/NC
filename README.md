# AI Model Testing Framework

A modular and extensible framework for testing different AI models through both API and vLLM deployment. This framework provides a clean interface for interacting with various AI models and comparing their responses.

[![GitHub](https://img.shields.io/github/license/EaminC/NC)](https://github.com/EaminC/NC/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

## Features

- Support for multiple AI models:
  - DeepSeek R1
  - Qwen 32B
  - GLM-4 9B Chat
  - Llama 3.3 70B Instruct
  - And more...
- Multiple deployment options:
  - API-based testing
  - vLLM local deployment
- Easy configuration through JSON
- Simple and clean API interface
- Error handling and logging
- Modular and extensible architecture
- Type hints for better code maintainability

## Project Structure

```
ai-model-test/
├── api/                    # API-based testing
│   ├── src/               # Source code
│   │   ├── services/      # Service layer
│   │   │   ├── __init__.py
│   │   │   └── model_service.py    # Core service implementation
│   │   └── utils/         # Utilities
│   │       ├── __init__.py
│   │       └── config.py           # Configuration management
│   ├── tests/             # Test scripts
│   │   ├── __init__.py
│   │   ├── test_one_model.py      # Single model test script
│   │   └── test_all_models.py     # All models test script
│   └── config/            # Configuration
│       └── config.json            # Model and API configuration
├── vllm/                   # vLLM deployment
│   ├── src/               # Source code
│   │   ├── services/      # Service layer
│   │   │   ├── __init__.py
│   │   │   └── vllm_service.py    # vLLM service implementation
│   │   └── utils/         # Utilities
│   │       ├── __init__.py
│   │       └── config.py           # Configuration management
│   ├── tests/             # Test scripts
│   │   ├── __init__.py
│   │   └── test_vllm.py           # vLLM test script
│   ├── models/            # Model weights
│   │   └── README.md              # Model download instructions
│   └── config/            # Configuration
│       └── config.json            # vLLM configuration
├── README.md
├── requirements.txt
└── .gitignore
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- CUDA-compatible GPU (for vLLM deployment)
- Sufficient disk space for model weights

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

3. Configure your API key (for API-based testing):

   - Copy `api/config/config.json` to `api/config/config.local.json`
   - Update the API key in `api/config/config.local.json`

4. Download model weights (for vLLM deployment):
   - Follow instructions in `vllm/models/README.md`
   - Place downloaded weights in `vllm/models/` directory

## Usage

### API-based Testing

#### List Available Models

To see all available models and their descriptions:

```bash
python api/tests/test_one_model.py --list-models
```

#### Test Single Model

Use `test_one_model.py` to test a specific model:

```bash
# Basic usage
python api/tests/test_one_model.py --model deepseek-r1

# Custom message
python api/tests/test_one_model.py --model deepseek-r1 --message "Hello, please introduce yourself"
```

#### Test All Models

Use `test_all_models.py` to test all configured models:

```bash
# Basic usage
python api/tests/test_all_models.py

# Custom message
python api/tests/test_all_models.py --message "Hello, please introduce yourself"
```

### vLLM Deployment

#### Start vLLM Server

```bash
python vllm/src/services/vllm_service.py --model path/to/model --port 8000
```

#### Test vLLM Deployment

```bash
python vllm/tests/test_vllm.py --port 8000 --message "Hello, please introduce yourself"
```

## Configuration

### API Configuration

The `api/config/config.json` file contains all API configuration settings:

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

### vLLM Configuration

The `vllm/config/config.json` file contains vLLM deployment settings:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "max_parallel_seqs": 256
  },
  "model": {
    "tensor_parallel_size": 1,
    "gpu_memory_utilization": 0.9,
    "max_model_len": 2048
  }
}
```

## Development

### Project Structure

- `api/`: API-based testing implementation
  - `src/services/`: Core service classes
  - `src/utils/`: Utility functions
  - `tests/`: Test scripts
  - `config/`: Configuration files
- `vllm/`: vLLM deployment implementation
  - `src/services/`: vLLM service classes
  - `src/utils/`: Utility functions
  - `tests/`: Test scripts
  - `models/`: Model weights
  - `config/`: Configuration files

### Adding New Features

1. Create new service classes in appropriate `src/services/` directory
2. Add utility functions in appropriate `src/utils/` directory
3. Write tests in appropriate `tests/` directory
4. Update configuration in appropriate `config/` directory

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
- vLLM team for the deployment framework
- All contributors to this project

## Contact

EaminC - [@EaminC](https://github.com/EaminC)

Project Link: [https://github.com/EaminC/NC](https://github.com/EaminC/NC)
