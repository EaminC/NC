#!/bin/bash

# vLLM服务器启动脚本

set -e

# 默认配置
CONFIG_PATH="vllm/config/config.json"
LOG_DIR="vllm/logs"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 解析命令行参数
GPU_LIST=""
ACTION="start"

while [[ $# -gt 0 ]]; do
    case $1 in
        --gpu)
            GPU_LIST="$2"
            shift 2
            ;;
        --config)
            CONFIG_PATH="$2"
            shift 2
            ;;
        --action)
            ACTION="$2"
            shift 2
            ;;
        --help)
            echo "用法: $0 [选项]"
            echo "选项:"
            echo "  --gpu <gpu_ids>     指定GPU列表（逗号分隔），如 '0,1,2'"
            echo "  --config <path>     配置文件路径 (默认: $CONFIG_PATH)"
            echo "  --action <action>   操作类型: start|stop|restart|status (默认: start)"
            echo "  --help              显示此帮助信息"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

echo "=== vLLM服务器管理 ==="
echo "配置文件: $CONFIG_PATH"
echo "操作: $ACTION"
echo "GPU列表: ${GPU_LIST:-"全部"}"
echo

# 执行操作
if [ -n "$GPU_LIST" ]; then
    python -m vllm.src.services.server_manager --action "$ACTION" --gpu "$GPU_LIST" --config "$CONFIG_PATH"
else
    python -m vllm.src.services.server_manager --action "$ACTION" --config "$CONFIG_PATH"
fi 