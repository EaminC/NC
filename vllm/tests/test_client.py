#!/usr/bin/env python3
"""
vLLM客户端测试脚本
"""

import asyncio
import argparse
import json
import logging
from typing import Optional, List
from ..src.services.vllm_client import VLLMClientManager

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_list_servers(manager: VLLMClientManager):
    """测试列出服务器"""
    print("\n=== 可用服务器列表 ===")
    servers = await manager.list_servers()
    
    for gpu_id, info in servers.items():
        print(f"GPU {gpu_id}:")
        print(f"  模型: {info['model']}")
        print(f"  描述: {info['description']}")
        print(f"  端口: {info['port']}")
        print(f"  URL: {info['url']}")
        print()

async def test_health_check(manager: VLLMClientManager, gpu_id: Optional[str] = None):
    """测试健康检查"""
    print(f"\n=== 健康检查 {'(GPU ' + gpu_id + ')' if gpu_id else '(所有服务器)'} ===")
    
    try:
        health_status = await manager.check_health(gpu_id)
        
        for gpu, status in health_status.items():
            print(f"GPU {gpu}: {status['status']}")
            if status['status'] == 'healthy':
                print(f"  URL: {status['url']}")
                print(f"  响应: {status.get('response', {})}")
            else:
                print(f"  错误: {status.get('error', '未知错误')}")
            print()
            
    except Exception as e:
        logger.error(f"健康检查失败: {e}")

async def test_generate_text(
    manager: VLLMClientManager,
    prompt: str,
    gpu_id: Optional[str] = None,
    model_preference: Optional[List[str]] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7
):
    """测试文本生成"""
    target_desc = f"GPU {gpu_id}" if gpu_id else "最佳服务器"
    if model_preference:
        target_desc += f" (偏好模型: {', '.join(model_preference)})"
    
    print(f"\n=== 文本生成测试 ({target_desc}) ===")
    print(f"输入: {prompt}")
    print(f"参数: max_tokens={max_tokens}, temperature={temperature}")
    print("-" * 50)
    
    try:
        result = await manager.generate(
            prompt=prompt,
            gpu_id=gpu_id,
            model_preference=model_preference,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        print(f"模型: {result['model']}")
        print(f"GPU: {result['gpu_id']}")
        print(f"生成文本:")
        print(result['text'])
        print("-" * 50)
        
    except Exception as e:
        logger.error(f"文本生成失败: {e}")

async def interactive_mode(manager: VLLMClientManager):
    """交互模式"""
    print("\n=== 交互模式 ===")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'help' 查看命令")
    print("输入 'servers' 查看服务器列表")
    print("输入 'health' 检查服务器健康状态")
    print()
    
    current_gpu = None
    
    while True:
        try:
            user_input = input(f"[GPU {current_gpu if current_gpu else 'auto'}]> ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
            
            elif user_input.lower() == 'help':
                print("可用命令:")
                print("  servers - 列出所有服务器")
                print("  health - 检查服务器健康状态")
                print("  gpu <id> - 选择特定GPU")
                print("  auto - 自动选择GPU")
                print("  quit/exit - 退出")
                print("  其他输入 - 作为prompt进行文本生成")
                
            elif user_input.lower() == 'servers':
                await test_list_servers(manager)
                
            elif user_input.lower() == 'health':
                await test_health_check(manager)
                
            elif user_input.lower().startswith('gpu '):
                gpu_id = user_input[4:].strip()
                current_gpu = gpu_id
                print(f"已选择GPU {gpu_id}")
                
            elif user_input.lower() == 'auto':
                current_gpu = None
                print("已切换到自动选择模式")
                
            elif user_input:
                await test_generate_text(manager, user_input, current_gpu)
                
        except KeyboardInterrupt:
            print("\n退出交互模式")
            break
        except Exception as e:
            logger.error(f"执行命令时出错: {e}")

async def main():
    parser = argparse.ArgumentParser(description='vLLM客户端测试')
    parser.add_argument('--config', 
                       default="vllm/config/config.json", 
                       help='配置文件路径')
    parser.add_argument('--action',
                       choices=['list', 'health', 'generate', 'interactive'],
                       default='interactive',
                       help='执行的操作')
    parser.add_argument('--gpu',
                       help='指定GPU ID')
    parser.add_argument('--prompt',
                       default="你好，请介绍一下自己。",
                       help='生成文本的prompt')
    parser.add_argument('--model-preference',
                       nargs='+',
                       help='模型偏好列表')
    parser.add_argument('--max-tokens',
                       type=int,
                       default=2048,
                       help='最大生成token数')
    parser.add_argument('--temperature',
                       type=float,
                       default=0.7,
                       help='生成温度')
    
    args = parser.parse_args()
    
    manager = VLLMClientManager(args.config)
    
    try:
        if args.action == 'list':
            await test_list_servers(manager)
            
        elif args.action == 'health':
            await test_health_check(manager, args.gpu)
            
        elif args.action == 'generate':
            await test_generate_text(
                manager,
                args.prompt,
                args.gpu,
                args.model_preference,
                args.max_tokens,
                args.temperature
            )
            
        elif args.action == 'interactive':
            await interactive_mode(manager)
            
    except Exception as e:
        logger.error(f"操作失败: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 