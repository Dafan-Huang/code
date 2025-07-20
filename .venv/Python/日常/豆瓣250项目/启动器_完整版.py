#!/usr/bin/env python3
"""
豆瓣250项目完整启动器
提供友好的命令行界面来选择运行不同版本的应用
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🎬 豆瓣250电影项目完整启动器")
    print("=" * 50)
    print()
    print("请选择要运行的版本:")
    print("1. 完整单文件版本 (douban_movie_app.py) [推荐]")
    print("2. 模块化版本 (main.py)")
    print("3. 原始简单版本")
    print("4. 改进版本")
    print("5. 网络诊断工具")
    print("6. 运行测试")
    print("7. 查看项目信息")
    print("8. 退出")
    print()
    
    while True:
        try:
            choice = input("请输入选择 (1-8): ").strip()
            
            if choice == "1":
                print("🚀 启动完整单文件版本...")
                print("💡 这是功能最完整的版本，包含GUI界面、图片显示等所有功能")
                run_app("douban_movie_app.py")
                break
            elif choice == "2":
                print("🚀 启动模块化版本...")
                print("💡 这是模块化架构版本，代码结构清晰")
                run_app("main.py")
                break
            elif choice == "3":
                print("🚀 启动原始简单版本...")
                if check_versions_dir():
                    run_app("versions/豆瓣250.py") 
                break
            elif choice == "4":
                print("🚀 启动改进版本...")
                if check_versions_dir():
                    run_app("versions/豆瓣250_新版.py")
                break
            elif choice == "5":
                print("🔧 启动网络诊断工具...")
                if os.path.exists("network_tester.py"):
                    run_app("network_tester.py")
                elif check_tools_dir():
                    run_app("tools/豆瓣250_诊断工具.py")
                else:
                    print("❌ 网络诊断工具未找到")
                break
            elif choice == "6":
                print("🧪 运行测试...")
                run_tests()
                break
            elif choice == "7":
                show_project_info()
            elif choice == "8":
                print("👋 再见!")
                sys.exit(0)
            else:
                print("❌ 无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n👋 再见!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ 发生错误: {e}")

def check_versions_dir():
    """检查versions目录"""
    if not os.path.exists("versions"):
        print("❌ versions目录不存在")
        print("💡 提示: 请运行模块化版本或完整单文件版本")
        return False
    return True

def check_tools_dir():
    """检查tools目录"""
    if not os.path.exists("tools"):
        print("❌ tools目录不存在")
        return False
    return True

def run_app(script_path, *args):
    """运行应用"""
    if not os.path.exists(script_path):
        print(f"❌ 文件不存在: {script_path}")
        return
    
    try:
        print(f"📂 运行文件: {script_path}")
        if script_path.endswith("douban_movie_app.py"):
            print("⏳ 正在启动GUI界面，请稍候...")
        cmd = [sys.executable, script_path] + list(args)
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 应用运行失败: {e}")
        print("💡 提示: 请确保已安装所有依赖包 (pip install -r requirements.txt)")
    except FileNotFoundError:
        print("❌ Python解释器未找到")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

def run_tests():
    """运行测试"""
    test_files = []
    
    # 查找测试文件
    if os.path.exists("tests"):
        for file in os.listdir("tests"):
            if file.endswith(".py"):
                test_files.append(f"tests/{file}")
    
    if os.path.exists("tools"):
        for file in os.listdir("tools"):
            if file.startswith("test_") and file.endswith(".py"):
                test_files.append(f"tools/{file}")
    
    if not test_files:
        print("❌ 未找到测试文件")
        return
    
    print(f"🧪 找到 {len(test_files)} 个测试文件:")
    for i, test_file in enumerate(test_files, 1):
        print(f"  {i}. {test_file}")
    
    try:
        choice = input("\n选择要运行的测试 (输入数字，回车运行全部): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(test_files):
                run_app(test_files[idx])
        else:
            for test_file in test_files:
                print(f"\n🧪 运行测试: {test_file}")
                run_app(test_file)
    except Exception as e:
        print(f"❌ 运行测试失败: {e}")

def show_project_info():
    """显示项目信息"""
    print()
    print("📋 豆瓣250电影项目信息")
    print("-" * 40)
    print("项目名称: 豆瓣电影Top250浏览器")
    print("主要特色: 完整单文件版本 + 模块化架构")
    print("技术栈: Python, Tkinter, Requests, BeautifulSoup, PIL")
    print("核心功能: 电影数据获取, 海报显示, GUI界面, 搜索导出")
    print()
    print("🌟 推荐版本:")
    print("  • 完整单文件版本 (douban_movie_app.py) - 功能最全，913行代码")
    print("  • 模块化版本 (main.py) - 代码结构清晰，便于维护")
    print()
    print("📁 项目结构:")
    show_file_structure()
    print()

def show_file_structure():
    """显示文件结构"""
    structure = [
        "├── douban_movie_app.py (⭐ 完整单文件版本，913行)",
        "├── main.py (模块化版本入口)",
        "├── src/ (模块化源代码)",
        "│   ├── core/ (核心模块)",
        "│   ├── ui/ (用户界面)",
        "│   └── utils/ (工具模块)",
        "├── data/ (数据存储)",
        "├── docs/ (文档)",
        "├── tests/ (测试文件)",
        "├── requirements.txt (依赖)",
        "└── 启动程序.bat (批处理启动器)"
    ]
    
    for line in structure:
        print(line)

def check_dependencies():
    """检查依赖包"""
    print("🔍 检查依赖包...")
    required_packages = ['requests', 'beautifulsoup4', 'pillow']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').replace('4', ''))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("💡 请运行: pip install -r requirements.txt")
        return False
    else:
        print("✅ 所有依赖包已安装")
        return True

if __name__ == "__main__":
    # 确保在项目根目录运行
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 检查关键文件
    print("🔧 初始化检查...")
    key_files = ["douban_movie_app.py", "main.py", "requirements.txt"]
    missing_files = [f for f in key_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"⚠️  警告: 缺少关键文件: {', '.join(missing_files)}")
    else:
        print("✅ 关键文件检查通过")
    
    print()
    main()
