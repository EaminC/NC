# AI Model Testing Framework

A simple framework for testing different AI models through the Infini-AI API.

## Features

- Support for multiple AI models:
  - DeepSeek R1
  - Qwen 32B
  - GLM-4 9B Chat
  - Llama 3.3 70B Instruct
- Easy configuration through JSON
- Simple and clean API interface
- Error handling and logging
- Modular and extensible architecture

## Project Structure

```
ai-model-test/
├── src/                    # Source code
│   ├── services/          # Service layer
│   │   └── model_service.py
│   └── utils/             # Utilities
│       └── config.py
├── tests/                 # Test scripts
│   └── test_models.py
├── config/               # Configuration
│   └── config.json
├── README.md
├── requirements.txt
└── .gitignore
```

## Setup

1. Clone the repository:

```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your API key in `config/config.json`

## Usage

Run the test script:

```bash
python tests/test_models.py
```

## Configuration

Edit `config/config.json` to:

- Update API key
- Add/remove models
- Modify model descriptions

## Development

The project follows a modular structure:

- `src/services/`: Contains the core service classes
- `src/utils/`: Contains utility functions and helpers
- `tests/`: Contains test scripts
- `config/`: Contains configuration files

## License

MIT License
