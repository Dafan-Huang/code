#!/usr/bin/env python3
"""
彩虹说话机启动器
提供友好的命令行界面来选择运行不同版本的应用
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🌈 彩虹说话机启动器")
    print("=" * 40)
    print()
    print("请选择要运行的版本:")
    print("1. 原始版本 (基础功能)")
    print("2. 重构版本 (改进架构)")
    print("3. 增强版本 (完整功能) [推荐]")
    print("4. 查看项目信息")
    print("5. 退出")
    print()
    
    while True:
        try:
            choice = input("请输入选择 (1-5): ").strip()
            
            if choice == "1":
                print("🚀 启动原始版本...")
                run_app("src/彩虹说话机.py")
                break
            elif choice == "2":
                print("🚀 启动重构版本...")
                run_app("src/彩虹说话机_重构版.py")
                break
            elif choice == "3":
                print("🚀 启动增强版本...")
                config_path = "config/config.toml"
                if os.path.exists(config_path):
                    run_app("src/彩虹说话机_增强版.py", config_path)
                else:
                    run_app("src/彩虹说话机_增强版.py")
                break
            elif choice == "4":
                show_project_info()
            elif choice == "5":
                print("👋 再见!")
                sys.exit(0)
            else:
                print("❌ 无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n👋 再见!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ 发生错误: {e}")

def run_app(script_path, *args):
    """运行应用"""
    if not os.path.exists(script_path):
        print(f"❌ 文件不存在: {script_path}")
        return
    
    try:
        cmd = [sys.executable, script_path] + list(args)
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 应用运行失败: {e}")
    except FileNotFoundError:
        print("❌ Python解释器未找到")

def show_project_info():
    """显示项目信息"""
    print()
    print("📋 项目信息")
    print("-" * 30)
    print("项目名称: 彩虹说话机")
    print("版本数量: 3个")
    print("技术栈: Python, Tkinter, pyttsx3")
    print("功能: 语音播报, 彩虹背景, 配置管理")
    print()
    print("📁 文件结构:")
    show_file_structure()
    print()

def show_file_structure():
    """显示文件结构"""
    structure = [
        "├── src/",
        "│   ├── 彩虹说话机.py (原始版本)",
        "│   ├── 彩虹说话机_重构版.py (重构版本)",
        "│   └── 彩虹说话机_增强版.py (增强版本)",
        "├── config/",
        "│   └── config.toml (配置文件)",
        "├── docs/",
        "│   └── 彩虹说话机_重构说明.md",
        "├── README.md",
        "├── requirements.txt",
        "└── 启动器.py (当前文件)"
    ]
    
    for line in structure:
        print(line)

if __name__ == "__main__":
    # 确保在项目根目录运行
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    main()
