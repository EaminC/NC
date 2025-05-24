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

## Setup

1. Clone the repository:

```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Install dependencies:

```bash
pip install requests
```

3. Configure your API key in `config.json`

## Usage

Run the test script:

```bash
python test.py
```

## Project Structure

```
.
├── README.md
├── config.json          # Configuration file
├── model_service.py     # Core service class
├── test.py             # Main test script
└── .gitignore          # Git ignore rules
```

## Configuration

Edit `config.json` to:

- Update API key
- Add/remove models
- Modify model descriptions

## License

MIT License
