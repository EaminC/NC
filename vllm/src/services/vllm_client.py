#!/usr/bin/env python3
"""
vLLM Client - 用于连接和管理多个vLLM服务器的客户端
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from ..utils.config import Config

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VLLMClient:
    """vLLM客户端类"""
    
    def __init__(self, config_path: str = "vllm/config/config.json"):
        self.config = Config(config_path)
        self.client_config = self.config.config.get("client", {})
        self.timeout = self.client_config.get("default_timeout", 300)
        self.retry_attempts = self.client_config.get("retry_attempts", 3)
        self.retry_delay = self.client_config.get("retry_delay", 1)
        self.session = None
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    def get_server_url(self, gpu_id: str) -> str:
        """获取指定GPU服务器的URL"""
        gpu_config = self.config.get_gpu_config(gpu_id)
        if not gpu_config:
            raise ValueError(f"未找到GPU {gpu_id}的配置")
        
        host = self.config.server_config.get("host", "localhost")
        port = gpu_config["port"]
        return f"http://{host}:{port}"
    
    def list_available_servers(self) -> Dict[str, Dict]:
        """列出所有可用的服务器配置"""
        servers = {}
        for gpu_id in self.config.get_available_gpus():
            gpu_config = self.config.get_gpu_config(gpu_id)
            servers[gpu_id] = {
                "gpu_id": gpu_id,
                "model": gpu_config["model"],
                "description": gpu_config["description"],
                "port": gpu_config["port"],
                "url": self.get_server_url(gpu_id)
            }
        return servers
    
    async def check_server_health(self, gpu_id: str) -> Dict[str, Any]:
        """检查指定服务器的健康状态"""
        if not self.session:
            raise RuntimeError("客户端会话未初始化，请使用async with语句")
        
        url = f"{self.get_server_url(gpu_id)}/health"
        
        for attempt in range(self.retry_attempts):
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "gpu_id": gpu_id,
                            "status": "healthy",
                            "url": self.get_server_url(gpu_id),
                            "response": data
                        }
                    else:
                        logger.warning(f"服务器健康检查失败 GPU {gpu_id}: HTTP {response.status}")
                        
            except Exception as e:
                logger.warning(f"健康检查尝试 {attempt + 1}/{self.retry_attempts} 失败 GPU {gpu_id}: {e}")
                if attempt < self.retry_attempts - 1:
                    await asyncio.sleep(self.retry_delay)
        
        return {
            "gpu_id": gpu_id,
            "status": "unhealthy",
            "url": self.get_server_url(gpu_id),
            "error": "健康检查失败"
        }
    
    async def get_server_info(self, gpu_id: str) -> Dict[str, Any]:
        """获取指定服务器的详细信息"""
        if not self.session:
            raise RuntimeError("客户端会话未初始化，请使用async with语句")
        
        url = f"{self.get_server_url(gpu_id)}/info"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"HTTP {response.status}: {await response.text()}")
                    
        except Exception as e:
            logger.error(f"获取服务器信息失败 GPU {gpu_id}: {e}")
            raise e
    
    async def generate_text(
        self,
        gpu_id: str,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: int = -1,
        stop: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """在指定GPU上生成文本"""
        if not self.session:
            raise RuntimeError("客户端会话未初始化，请使用async with语句")
        
        url = f"{self.get_server_url(gpu_id)}/generate"
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "stop": stop
        }
        
        try:
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"文本生成成功 GPU {gpu_id}: {len(result.get('text', ''))} 字符")
                    return result
                else:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
                    
        except Exception as e:
            logger.error(f"文本生成失败 GPU {gpu_id}: {e}")
            raise e
    
    async def check_all_servers(self) -> Dict[str, Dict]:
        """检查所有服务器的健康状态"""
        tasks = []
        for gpu_id in self.config.get_available_gpus():
            tasks.append(self.check_server_health(gpu_id))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        health_status = {}
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"健康检查出错: {result}")
            else:
                health_status[result["gpu_id"]] = result
        
        return health_status
    
    async def generate_on_best_server(
        self,
        prompt: str,
        model_preference: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """在最佳可用服务器上生成文本"""
        # 检查所有服务器健康状态
        health_status = await self.check_all_servers()
        healthy_servers = [
            gpu_id for gpu_id, status in health_status.items()
            if status.get("status") == "healthy"
        ]
        
        if not healthy_servers:
            raise Exception("没有健康的服务器可用")
        
        # 根据模型偏好选择服务器
        target_server = None
        if model_preference:
            for preferred_model in model_preference:
                for gpu_id in healthy_servers:
                    gpu_config = self.config.get_gpu_config(gpu_id)
                    if preferred_model.lower() in gpu_config["model"].lower():
                        target_server = gpu_id
                        break
                if target_server:
                    break
        
        # 如果没有找到偏好模型，选择第一个健康的服务器
        if not target_server:
            target_server = healthy_servers[0]
        
        logger.info(f"选择服务器 GPU {target_server} 进行文本生成")
        return await self.generate_text(target_server, prompt, **kwargs)

class VLLMClientManager:
    """vLLM客户端管理器 - 简化常用操作"""
    
    def __init__(self, config_path: str = "vllm/config/config.json"):
        self.config_path = config_path
    
    async def list_servers(self) -> Dict[str, Dict]:
        """列出所有服务器"""
        async with VLLMClient(self.config_path) as client:
            return client.list_available_servers()
    
    async def check_health(self, gpu_id: Optional[str] = None) -> Dict[str, Dict]:
        """检查服务器健康状态"""
        async with VLLMClient(self.config_path) as client:
            if gpu_id:
                result = await client.check_server_health(gpu_id)
                return {gpu_id: result}
            else:
                return await client.check_all_servers()
    
    async def generate(
        self,
        prompt: str,
        gpu_id: Optional[str] = None,
        model_preference: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """生成文本"""
        async with VLLMClient(self.config_path) as client:
            if gpu_id:
                return await client.generate_text(gpu_id, prompt, **kwargs)
            else:
                return await client.generate_on_best_server(
                    prompt, model_preference, **kwargs
                ) 