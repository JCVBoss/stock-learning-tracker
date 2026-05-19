#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 正在启动股票学习路线跟踪系统..."
echo "📊 访问地址: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

source venv/bin/activate
python app.py
