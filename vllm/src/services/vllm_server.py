#!/usr/bin/env python3
"""
vLLM Server - 在指定GPU上部署单个模型的服务器
"""

import argparse
import asyncio
import json
import os
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from vllm import AsyncLLMEngine, AsyncEngineArgs, SamplingParams
from ..utils.config import Config

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerateRequest(BaseModel):
    """生成请求模型"""
    prompt: str
    max_tokens: Optional[int] = 2048
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.95
    top_k: Optional[int] = -1
    stop: Optional[list] = None

class GenerateResponse(BaseModel):
    """生成响应模型"""
    text: str
    prompt: str
    model: str
    gpu_id: str

class VLLMServer:
    """vLLM服务器类"""
    
    def __init__(self, gpu_id: str, config_path: str = "vllm/config/config.json"):
        self.gpu_id = gpu_id
        self.config = Config(config_path)
        self.gpu_config = self.config.get_gpu_config(gpu_id)
        
        if not self.gpu_config:
            raise ValueError(f"未找到GPU {gpu_id}的配置")
            
        self.model_path = self.gpu_config["model"]
        self.port = self.gpu_config["port"]
        self.host = self.config.server_config.get("host", "0.0.0.0")
        
        # 设置CUDA设备
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
        
        self.engine = None
        self.app = FastAPI(
            title=f"vLLM Server - GPU {gpu_id}",
            description=f"运行在GPU {gpu_id}上的{self.gpu_config['description']}",
            version="1.0.0"
        )
        
        # 添加CORS中间件
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self._setup_routes()
    
    def _setup_routes(self):
        """设置路由"""
        
        @self.app.get("/health")
        async def health_check():
            """健康检查"""
            return {
                "status": "healthy",
                "gpu_id": self.gpu_id,
                "model": self.model_path,
                "port": self.port
            }
        
        @self.app.get("/info")
        async def get_info():
            """获取模型信息"""
            return {
                "gpu_id": self.gpu_id,
                "model": self.model_path,
                "description": self.gpu_config["description"],
                "port": self.port,
                "config": {
                    "tensor_parallel_size": self.gpu_config["tensor_parallel_size"],
                    "gpu_memory_utilization": self.gpu_config["gpu_memory_utilization"],
                    "max_model_len": self.gpu_config["max_model_len"]
                }
            }
        
        @self.app.post("/generate", response_model=GenerateResponse)
        async def generate(request: GenerateRequest):
            """生成文本"""
            if not self.engine:
                raise HTTPException(status_code=503, detail="模型尚未加载")
            
            try:
                sampling_params = SamplingParams(
                    temperature=request.temperature,
                    top_p=request.top_p,
                    top_k=request.top_k,
                    max_tokens=request.max_tokens,
                    stop=request.stop
                )
                
                results = self.engine.generate(
                    request.prompt,
                    sampling_params=sampling_params
                )
                
                # 等待生成完成
                async for request_output in results:
                    pass
                
                generated_text = request_output.outputs[0].text
                
                return GenerateResponse(
                    text=generated_text,
                    prompt=request.prompt,
                    model=self.model_path,
                    gpu_id=self.gpu_id
                )
                
            except Exception as e:
                logger.error(f"生成文本时出错: {e}")
                raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")
    
    async def load_model(self):
        """异步加载模型"""
        try:
            logger.info(f"开始在GPU {self.gpu_id}上加载模型: {self.model_path}")
            
            engine_args = AsyncEngineArgs(
                model=self.model_path,
                tensor_parallel_size=self.gpu_config["tensor_parallel_size"],
                gpu_memory_utilization=self.gpu_config["gpu_memory_utilization"],
                max_model_len=self.gpu_config["max_model_len"],
                device="cuda",
                worker_use_ray=False
            )
            
            self.engine = AsyncLLMEngine.from_engine_args(engine_args)
            logger.info(f"模型加载完成: GPU {self.gpu_id}")
            
        except Exception as e:
            logger.error(f"加载模型失败: {e}")
            raise e
    
    async def start_server(self):
        """启动服务器"""
        await self.load_model()
        
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="info"
        )
        
        server = uvicorn.Server(config)
        logger.info(f"启动服务器: {self.host}:{self.port}")
        await server.serve()

async def main():
    parser = argparse.ArgumentParser(description='启动vLLM服务器')
    parser.add_argument('--gpu', required=True, help='GPU ID')
    parser.add_argument('--config', default="vllm/config/config.json", help='配置文件路径')
    args = parser.parse_args()
    
    try:
        server = VLLMServer(args.gpu, args.config)
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        raise e

if __name__ == "__main__":
    asyncio.run(main()) 