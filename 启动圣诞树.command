#!/bin/bash
# 双击此文件启动圣诞树！
# Double-click to start Christmas Tree!

cd "$(dirname "$0")"
echo "🎄 正在启动圣诞树服务器..."
echo "🌐 请在浏览器中打开: http://localhost:8000"
echo ""
echo "按 Ctrl+C 关闭服务器"
echo ""

# Open browser automatically
sleep 1 && open "http://localhost:8000" &

# Start server
python3 -m http.server 8000
