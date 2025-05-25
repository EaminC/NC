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
  - vLLM local deployment with server-client architecture
- **New vLLM Features:**
  - Multi-GPU support with independent model deployment per GPU
  - Server-client architecture for distributed inference
  - Health monitoring and automatic failover
  - Load balancing across multiple servers
  - RESTful API for each model server
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
├── vllm/                   # vLLM deployment (Server-Client Architecture)
│   ├── src/               # Source code
│   │   ├── services/      # Service layer
│   │   │   ├── __init__.py
│   │   │   ├── vllm_server.py     # Individual model server
│   │   │   ├── vllm_client.py     # Client for connecting to servers
│   │   │   └── server_manager.py  # Multi-server management
│   │   └── utils/         # Utilities
│   │       ├── __init__.py
│   │       └── config.py           # Configuration management
│   ├── tests/             # Test scripts
│   │   ├── __init__.py
│   │   └── test_client.py         # Client test script
│   ├── scripts/           # Utility scripts
│   │   └── start_servers.sh       # Server startup script
│   ├── models/            # Model weights
│   │   └── README.md              # Model download instructions
│   └── config/            # Configuration
│       └── config.json            # vLLM configuration with per-GPU settings
├── README.md
├── requirements.txt
└── .gitignore
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- CUDA-compatible GPU(s) (for vLLM deployment)
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

### vLLM Server-Client Deployment

The new vLLM implementation uses a server-client architecture where each GPU runs an independent model server on its own port.

#### Server Management

##### Start All Servers

```bash
# Using the management script
python -m vllm.src.services.server_manager --action start

# Using the shell script
./vllm/scripts/start_servers.sh --action start
```

##### Start Specific GPU Server

```bash
# Start server on GPU 0
python -m vllm.src.services.server_manager --action start --gpu 0

# Using shell script
./vllm/scripts/start_servers.sh --action start --gpu 0
```

##### Check Server Status

```bash
python -m vllm.src.services.server_manager --action status
```

##### Stop Servers

```bash
# Stop all servers
python -m vllm.src.services.server_manager --action stop

# Stop specific GPU server
python -m vllm.src.services.server_manager --action stop --gpu 0
```

##### Monitor Servers

```bash
python -m vllm.src.services.server_manager --action monitor --monitor-interval 30
```

#### Client Usage

##### Interactive Client

```bash
# Start interactive client
python -m vllm.tests.test_client --action interactive
```

##### List Available Servers

```bash
python -m vllm.tests.test_client --action list
```

##### Health Check

```bash
# Check all servers
python -m vllm.tests.test_client --action health

# Check specific GPU
python -m vllm.tests.test_client --action health --gpu 0
```

##### Generate Text

```bash
# Generate on specific GPU
python -m vllm.tests.test_client --action generate --gpu 0 --prompt "Hello, world!"

# Auto-select best server
python -m vllm.tests.test_client --action generate --prompt "Hello, world!"

# With model preference
python -m vllm.tests.test_client --action generate --prompt "Hello!" --model-preference llama qwen
```

#### Direct Server Access

Each server provides a RESTful API:

```bash
# Health check
curl http://localhost:8000/health

# Get server info
curl http://localhost:8000/info

# Generate text
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, world!", "max_tokens": 100}'
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

The `vllm/config/config.json` file contains vLLM deployment settings with per-GPU configuration:

```json
{
  "gpus": {
    "0": {
      "model": "models/llama2-7b",
      "tensor_parallel_size": 1,
      "gpu_memory_utilization": 0.9,
      "max_model_len": 2048,
      "description": "Llama 2 7B model on GPU 0",
      "port": 8000
    },
    "1": {
      "model": "models/qwen-14b",
      "tensor_parallel_size": 1,
      "gpu_memory_utilization": 0.9,
      "max_model_len": 2048,
      "description": "Qwen 14B model on GPU 1",
      "port": 8001
    }
  },
  "server": {
    "host": "0.0.0.0",
    "max_parallel_seqs": 256
  },
  "client": {
    "default_timeout": 300,
    "retry_attempts": 3,
    "retry_delay": 1
  }
}
```

### Key Features of New vLLM Architecture

1. **Independent GPU Deployment**: Each GPU runs its own model server on a unique port
2. **RESTful API**: Each server provides a standardized REST API
3. **Health Monitoring**: Built-in health checks and status monitoring
4. **Load Balancing**: Client can automatically select the best available server
5. **Model Preference**: Support for model-based server selection
6. **Graceful Degradation**: Automatic failover when servers are unavailable
7. **Batch Management**: Easy start/stop/restart of multiple servers

## Development

### Adding New Models

1. Update `vllm/config/config.json` with new GPU configuration
2. Download model weights to `vllm/models/` directory
3. Start the server for the new GPU

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
