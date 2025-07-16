@echo off
echo 豆瓣电影Top250浏览器
echo ==================
echo.
echo 正在启动程序...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 启动程序
python douban_movie_app.py

REM 如果程序异常退出，显示错误信息
if %errorlevel% neq 0 (
    echo.
    echo 程序异常退出，错误代码: %errorlevel%
    echo 请检查依赖是否正确安装：
    echo   pip install requests beautifulsoup4
    echo.
    pause
)
