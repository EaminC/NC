#!/usr/bin/env python3
"""
vLLM Server Manager - 用于批量管理多个vLLM服务器
"""

import asyncio
import argparse
import logging
import subprocess
import signal
import sys
import time
from typing import Dict, List, Optional
from ..utils.config import Config

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerManager:
    """vLLM服务器管理器"""
    
    def __init__(self, config_path: str = "vllm/config/config.json"):
        self.config = Config(config_path)
        self.processes: Dict[str, subprocess.Popen] = {}
        self.running = False
        
    def start_server(self, gpu_id: str) -> bool:
        """启动指定GPU上的服务器"""
        if gpu_id in self.processes:
            logger.warning(f"GPU {gpu_id}上的服务器已经在运行")
            return False
        
        gpu_config = self.config.get_gpu_config(gpu_id)
        if not gpu_config:
            logger.error(f"未找到GPU {gpu_id}的配置")
            return False
        
        try:
            # 构建启动命令
            cmd = [
                sys.executable, "-m", "vllm.src.services.vllm_server",
                "--gpu", gpu_id,
                "--config", self.config.config_path
            ]
            
            logger.info(f"启动GPU {gpu_id}上的服务器: {gpu_config['description']}")
            logger.info(f"端口: {gpu_config['port']}, 模型: {gpu_config['model']}")
            
            # 启动进程
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[gpu_id] = process
            logger.info(f"服务器启动成功 GPU {gpu_id}, PID: {process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"启动服务器失败 GPU {gpu_id}: {e}")
            return False
    
    def stop_server(self, gpu_id: str) -> bool:
        """停止指定GPU上的服务器"""
        if gpu_id not in self.processes:
            logger.warning(f"GPU {gpu_id}上没有运行的服务器")
            return False
        
        try:
            process = self.processes[gpu_id]
            logger.info(f"停止GPU {gpu_id}上的服务器, PID: {process.pid}")
            
            # 发送终止信号
            process.terminate()
            
            # 等待进程结束
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning(f"服务器未在10秒内停止，强制终止 GPU {gpu_id}")
                process.kill()
                process.wait()
            
            del self.processes[gpu_id]
            logger.info(f"服务器已停止 GPU {gpu_id}")
            return True
            
        except Exception as e:
            logger.error(f"停止服务器失败 GPU {gpu_id}: {e}")
            return False
    
    def start_all_servers(self, gpu_list: Optional[List[str]] = None) -> int:
        """启动所有或指定的服务器"""
        if gpu_list is None:
            gpu_list = self.config.get_available_gpus()
        
        success_count = 0
        for gpu_id in gpu_list:
            if self.start_server(gpu_id):
                success_count += 1
                # 添加启动间隔，避免资源冲突
                time.sleep(2)
        
        logger.info(f"启动完成: {success_count}/{len(gpu_list)} 个服务器启动成功")
        return success_count
    
    def stop_all_servers(self) -> int:
        """停止所有服务器"""
        gpu_list = list(self.processes.keys())
        success_count = 0
        
        for gpu_id in gpu_list:
            if self.stop_server(gpu_id):
                success_count += 1
        
        logger.info(f"停止完成: {success_count}/{len(gpu_list)} 个服务器停止成功")
        return success_count
    
    def get_server_status(self) -> Dict[str, Dict]:
        """获取所有服务器状态"""
        status = {}
        
        for gpu_id in self.config.get_available_gpus():
            gpu_config = self.config.get_gpu_config(gpu_id)
            
            if gpu_id in self.processes:
                process = self.processes[gpu_id]
                poll_result = process.poll()
                
                if poll_result is None:
                    # 进程仍在运行
                    status[gpu_id] = {
                        "status": "running",
                        "pid": process.pid,
                        "port": gpu_config["port"],
                        "model": gpu_config["model"],
                        "description": gpu_config["description"]
                    }
                else:
                    # 进程已退出
                    status[gpu_id] = {
                        "status": "stopped",
                        "exit_code": poll_result,
                        "port": gpu_config["port"],
                        "model": gpu_config["model"],
                        "description": gpu_config["description"]
                    }
                    # 清理已退出的进程
                    del self.processes[gpu_id]
            else:
                status[gpu_id] = {
                    "status": "not_started",
                    "port": gpu_config["port"],
                    "model": gpu_config["model"],
                    "description": gpu_config["description"]
                }
        
        return status
    
    def monitor_servers(self, interval: int = 30):
        """监控服务器状态"""
        logger.info(f"开始监控服务器，检查间隔: {interval}秒")
        self.running = True
        
        try:
            while self.running:
                status = self.get_server_status()
                
                # 检查是否有异常退出的服务器
                for gpu_id, info in status.items():
                    if info["status"] == "stopped":
                        logger.warning(f"检测到服务器异常退出 GPU {gpu_id}, 退出代码: {info['exit_code']}")
                        # 可以在这里添加自动重启逻辑
                
                # 显示状态摘要
                running_count = sum(1 for info in status.values() if info["status"] == "running")
                total_count = len(status)
                logger.info(f"服务器状态: {running_count}/{total_count} 运行中")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("监控被中断")
        finally:
            self.running = False
    
    def cleanup(self):
        """清理资源"""
        logger.info("清理资源...")
        self.running = False
        self.stop_all_servers()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

def signal_handler(signum, frame, manager: ServerManager):
    """信号处理器"""
    logger.info(f"接收到信号 {signum}，正在清理...")
    manager.cleanup()
    sys.exit(0)

async def main():
    parser = argparse.ArgumentParser(description='vLLM服务器管理器')
    parser.add_argument('--action', 
                       choices=['start', 'stop', 'restart', 'status', 'monitor'],
                       default='start',
                       help='执行的操作')
    parser.add_argument('--gpu', 
                       help='指定GPU ID（如果不指定则操作所有GPU）')
    parser.add_argument('--config', 
                       default="vllm/config/config.json", 
                       help='配置文件路径')
    parser.add_argument('--monitor-interval',
                       type=int,
                       default=30,
                       help='监控间隔（秒）')
    
    args = parser.parse_args()
    
    manager = ServerManager(args.config)
    
    # 设置信号处理器
    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, manager))
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f, manager))
    
    try:
        if args.action == 'start':
            if args.gpu:
                manager.start_server(args.gpu)
            else:
                manager.start_all_servers()
                
        elif args.action == 'stop':
            if args.gpu:
                manager.stop_server(args.gpu)
            else:
                manager.stop_all_servers()
                
        elif args.action == 'restart':
            if args.gpu:
                manager.stop_server(args.gpu)
                time.sleep(2)
                manager.start_server(args.gpu)
            else:
                manager.stop_all_servers()
                time.sleep(2)
                manager.start_all_servers()
                
        elif args.action == 'status':
            status = manager.get_server_status()
            print("\n=== 服务器状态 ===")
            for gpu_id, info in status.items():
                print(f"GPU {gpu_id}: {info['status']}")
                print(f"  模型: {info['model']}")
                print(f"  端口: {info['port']}")
                print(f"  描述: {info['description']}")
                if info["status"] == "running":
                    print(f"  PID: {info['pid']}")
                elif info["status"] == "stopped":
                    print(f"  退出代码: {info['exit_code']}")
                print()
                
        elif args.action == 'monitor':
            manager.monitor_servers(args.monitor_interval)
            
    except Exception as e:
        logger.error(f"操作失败: {e}")
        manager.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 