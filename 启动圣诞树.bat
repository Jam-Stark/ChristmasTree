@echo off
chcp 65001 >nul
title 圣诞树启动器

echo.
echo 🎄 正在启动圣诞树服务器...
echo.
echo 🌐 请在浏览器中打开: http://localhost:8000
echo.
echo 按 Ctrl+C 关闭服务器
echo.

:: Wait 2 seconds then open browser
start "" "http://localhost:8000"

:: Start Python server
python -m http.server 8000

pause
