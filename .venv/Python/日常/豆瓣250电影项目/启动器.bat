@echo off
chcp 65001 >nul
title 豆瓣250电影项目启动器

echo 🎬 豆瓣250电影项目启动器
echo ==========================================
echo.
echo 请选择要运行的版本:
echo 1. 高级版本 (完整GUI界面) [推荐]
echo 2. 改进版本 (命令行增强)
echo 3. 原始版本 (简单脚本)
echo 4. 网络诊断工具
echo 5. 测试脚本
echo 6. 安装依赖包
echo 7. 退出
echo.

:input
set /p choice=请输入选择 (1-7): 

if "%choice%"=="1" (
    echo 🚀 启动高级版本...
    python main.py
    goto end
) else if "%choice%"=="2" (
    echo 🚀 启动改进版本...
    python versions/豆瓣250_新版.py
    goto end
) else if "%choice%"=="3" (
    echo 🚀 启动原始版本...
    python versions/豆瓣250.py
    goto end
) else if "%choice%"=="4" (
    echo 🔧 启动网络诊断工具...
    python tools/豆瓣250_诊断工具.py
    goto end
) else if "%choice%"=="5" (
    echo 🧪 运行测试脚本...
    python tools/test_douban.py
    goto end
) else if "%choice%"=="6" (
    echo 📦 安装依赖包...
    pip install -r requirements.txt
    echo.
    echo ✅ 依赖包安装完成
    echo.
    goto input
) else if "%choice%"=="7" (
    echo 👋 再见!
    goto end
) else (
    echo ❌ 无效选择，请重新输入
    echo.
    goto input
)

:end
echo.
echo 按任意键退出...
pause >nul
