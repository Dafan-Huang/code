@echo off
chcp 65001 >nul
title 数学建模手动任务执行器

echo.
echo ========================================
echo        数学建模手动任务执行器
echo ========================================
echo.

cd /d "%~dp0"

python manual_runner.py

pause