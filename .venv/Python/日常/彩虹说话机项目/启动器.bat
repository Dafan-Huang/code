@echo off
echo 彩虹说话机启动器
echo ==================
echo.
echo 请选择要运行的版本:
echo 1. 原始版本 (基础功能)
echo 2. 重构版本 (改进架构)
echo 3. 增强版本 (完整功能) [推荐]
echo 4. 退出
echo.
set /p choice=请输入选择 (1-4): 

if "%choice%"=="1" (
    echo 启动原始版本...
    python src/彩虹说话机.py
) else if "%choice%"=="2" (
    echo 启动重构版本...
    python src/彩虹说话机_重构版.py
) else if "%choice%"=="3" (
    echo 启动增强版本...
    python src/彩虹说话机_增强版.py config/config.toml
) else if "%choice%"=="4" (
    echo 再见!
    exit /b
) else (
    echo 无效选择，请重新运行脚本
)

pause
