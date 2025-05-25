# vLLM Server-Client 使用示例

本文档提供 vLLM 多 GPU 服务器-客户端架构的详细使用示例。

## 快速开始

### 1. 启动所有服务器

```bash
# 方法1: 使用服务器管理器
python -m vllm.src.services.server_manager --action start

# 方法2: 使用Shell脚本
./vllm/scripts/start_servers.sh --action start
```

### 2. 检查服务器状态

```bash
python -m vllm.src.services.server_manager --action status
```

### 3. 使用客户端进行交互

```bash
python -m vllm.tests.test_client --action interactive
```

## 详细使用场景

### 场景 1: 单 GPU 部署

如果您只想在特定 GPU 上部署模型：

```bash
# 启动GPU 0上的服务器
python -m vllm.src.services.server_manager --action start --gpu 0

# 检查状态
python -m vllm.src.services.server_manager --action status

# 使用客户端连接特定GPU
python -m vllm.tests.test_client --action generate --gpu 0 --prompt "介绍一下深度学习"
```

### 场景 2: 多 GPU 负载均衡

启动多个 GPU 服务器并让客户端自动选择：

```bash
# 启动GPU 0, 1, 2
python -m vllm.src.services.server_manager --action start

# 客户端自动选择最佳服务器
python -m vllm.tests.test_client --action generate --prompt "什么是人工智能？"

# 指定模型偏好
python -m vllm.tests.test_client --action generate --prompt "写一首诗" --model-preference llama qwen
```

### 场景 3: 健康监控

```bash
# 检查所有服务器健康状态
python -m vllm.tests.test_client --action health

# 检查特定GPU
python -m vllm.tests.test_client --action health --gpu 0

# 持续监控
python -m vllm.src.services.server_manager --action monitor --monitor-interval 30
```

### 场景 4: 服务器重启

```bash
# 重启特定GPU服务器
python -m vllm.src.services.server_manager --action restart --gpu 0

# 重启所有服务器
python -m vllm.src.services.server_manager --action restart
```

## 编程接口使用

### 使用 VLLMClientManager

```python
import asyncio
from vllm.src.services.vllm_client import VLLMClientManager

async def example():
    manager = VLLMClientManager()

    # 列出所有服务器
    servers = await manager.list_servers()
    print("可用服务器:", servers)

    # 检查健康状态
    health = await manager.check_health()
    print("健康状态:", health)

    # 生成文本 - 自动选择
    result = await manager.generate(
        prompt="解释什么是transformer模型",
        max_tokens=1000,
        temperature=0.7
    )
    print("生成结果:", result['text'])

    # 生成文本 - 指定GPU
    result = await manager.generate(
        prompt="写一个Python函数",
        gpu_id="0",
        max_tokens=500
    )
    print("GPU 0生成结果:", result['text'])

# 运行示例
asyncio.run(example())
```

### 使用 VLLMClient (更底层控制)

```python
import asyncio
from vllm.src.services.vllm_client import VLLMClient

async def advanced_example():
    async with VLLMClient() as client:
        # 检查特定服务器健康状态
        health = await client.check_server_health("0")
        if health['status'] == 'healthy':
            # 生成文本
            result = await client.generate_text(
                gpu_id="0",
                prompt="编写一个机器学习的例子",
                max_tokens=2048,
                temperature=0.8,
                top_p=0.95
            )
            print("生成的代码:", result['text'])

        # 获取服务器详细信息
        info = await client.get_server_info("0")
        print("服务器信息:", info)

asyncio.run(advanced_example())
```

## REST API 直接访问

每个服务器都提供 RESTful API，您可以直接访问：

### 健康检查

```bash
curl http://localhost:8000/health
```

响应示例：

```json
{
  "status": "healthy",
  "gpu_id": "0",
  "model": "models/llama2-7b",
  "port": 8000
}
```

### 获取服务器信息

```bash
curl http://localhost:8000/info
```

响应示例：

```json
{
  "gpu_id": "0",
  "model": "models/llama2-7b",
  "description": "Llama 2 7B model on GPU 0",
  "port": 8000,
  "config": {
    "tensor_parallel_size": 1,
    "gpu_memory_utilization": 0.9,
    "max_model_len": 2048
  }
}
```

### 生成文本

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "解释一下深度学习的基本概念",
    "max_tokens": 1000,
    "temperature": 0.7,
    "top_p": 0.95
  }'
```

响应示例：

```json
{
  "text": "深度学习是机器学习的一个子领域...",
  "prompt": "解释一下深度学习的基本概念",
  "model": "models/llama2-7b",
  "gpu_id": "0"
}
```

## 配置示例

### 自定义 GPU 配置

在`vllm/config/config.json`中添加新的 GPU 配置：

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
      "gpu_memory_utilization": 0.8,
      "max_model_len": 4096,
      "description": "Qwen 14B model on GPU 1",
      "port": 8001
    },
    "2": {
      "model": "models/mistral-7b",
      "tensor_parallel_size": 1,
      "gpu_memory_utilization": 0.9,
      "max_model_len": 2048,
      "description": "Mistral 7B model on GPU 2",
      "port": 8002
    }
  }
}
```

### 高内存模型配置

对于需要多 GPU 的大模型：

```json
{
  "gpus": {
    "0": {
      "model": "models/llama2-70b",
      "tensor_parallel_size": 4,
      "gpu_memory_utilization": 0.95,
      "max_model_len": 4096,
      "description": "Llama 2 70B model on GPU 0-3",
      "port": 8000
    }
  }
}
```

## 故障排除

### 常见问题

1. **服务器启动失败**

   ```bash
   # 检查GPU是否可用
   nvidia-smi

   # 检查端口是否被占用
   netstat -tlnp | grep 8000

   # 查看详细日志
   python -m vllm.src.services.vllm_server --gpu 0 --config vllm/config/config.json
   ```

2. **客户端连接失败**

   ```bash
   # 检查服务器状态
   python -m vllm.src.services.server_manager --action status

   # 手动健康检查
   curl http://localhost:8000/health
   ```

3. **内存不足**
   - 降低`gpu_memory_utilization`值
   - 减少`max_model_len`
   - 使用更小的模型

### 性能优化

1. **调整内存使用**

   ```json
   {
     "gpu_memory_utilization": 0.8, // 降低内存使用
     "max_model_len": 2048 // 减少最大序列长度
   }
   ```

2. **并行处理优化**
   ```json
   {
     "tensor_parallel_size": 2, // 使用多GPU并行
     "max_parallel_seqs": 128 // 调整并发序列数
   }
   ```

## 生产环境部署

### 使用 systemd 管理服务

创建服务文件`/etc/systemd/system/vllm-gpu0.service`：

```ini
[Unit]
Description=vLLM Server GPU 0
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/your/project
ExecStart=/usr/bin/python -m vllm.src.services.vllm_server --gpu 0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl enable vllm-gpu0
sudo systemctl start vllm-gpu0
```

### 负载均衡配置

使用 nginx 进行负载均衡：

```nginx
upstream vllm_backend {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

server {
    listen 80;
    location /generate {
        proxy_pass http://vllm_backend;
    }
}
```

这个架构为您提供了灵活、可扩展的多 GPU 模型部署解决方案！
