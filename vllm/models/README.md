# Model Weights

This directory is for storing model weights used with vLLM deployment.

## Supported Models

The following models are known to work well with vLLM:

- Llama 2 (7B, 13B, 70B)
- Mistral (7B)
- Yi (6B, 34B)
- Qwen (7B, 14B, 72B)
- DeepSeek (7B, 67B)

## Download Instructions

1. Download model weights from their official sources:

   - Llama 2: [Meta AI](https://ai.meta.com/llama/)
   - Mistral: [Mistral AI](https://mistral.ai/)
   - Yi: [01.AI](https://01.ai/)
   - Qwen: [Qwen](https://github.com/QwenLM/Qwen)
   - DeepSeek: [DeepSeek](https://github.com/deepseek-ai/DeepSeek-LLM)

2. Place the downloaded weights in this directory with the following structure:

```
models/
├── llama2-7b/
├── llama2-13b/
├── llama2-70b/
├── mistral-7b/
├── yi-6b/
├── yi-34b/
├── qwen-7b/
├── qwen-14b/
├── qwen-72b/
├── deepseek-7b/
└── deepseek-67b/
```

3. Each model directory should contain the model weights in the format expected by vLLM.

## Usage

When using the vLLM service, specify the path to the model weights:

```bash
python vllm/src/services/vllm_service.py --model models/llama2-7b
```

## Notes

- Make sure you have sufficient disk space for the model weights
- Some models may require specific CUDA versions or GPU memory
- Check the model's license before using
