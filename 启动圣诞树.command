#!/bin/bash
# 🎄 圣诞树启动器 (Mac)

cd "$(dirname "$0")"

echo ""
echo "========================================"
echo "     🎄 圣诞树启动器"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到 Python3！"
    echo ""
    echo "请安装 Python:"
    echo "方法1: 打开终端运行: xcode-select --install"
    echo "方法2: 访问 https://www.python.org/downloads/ 下载安装"
    echo ""
    echo "正在打开 Python 下载页面..."
    open "https://www.python.org/downloads/"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

echo "✅ Python3 已安装"
echo ""
echo "🌐 正在启动服务器..."
echo "   请在浏览器中打开: http://localhost:8000"
echo ""
echo "   按 Ctrl+C 关闭服务器"
echo ""

# Wait 1 second then open browser
sleep 1 && open "http://localhost:8000" &

# Start Python server
python3 -m http.server 8000
