@echo off
chcp 65001 >nul
title 豆包炫酷启动器

echo ========================================
echo    豆包炫酷启动器 - 正在启动...
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 没有检测到 Python！
    echo.
    echo 请先安装 Python 3.8 或更高版本：
    echo 下载地址: https://www.python.org/downloads/
    echo 安装时记得勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM 检查 pywebview 是否安装
python -c "import webview" >nul 2>&1
if errorlevel 1 (
    echo [提示] 首次运行，正在安装依赖...
    pip install pywebview>=4.0 --quiet
    echo 依赖安装完成！
    echo.
)

REM 启动动画
python doubao_launcher.py

REM 运行结束后自动关闭
exit
