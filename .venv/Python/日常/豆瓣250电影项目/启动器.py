#!/usr/bin/env python3
"""
豆瓣250电影项目启动器
提供友好的命令行界面来选择运行不同版本的应用
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🎬 豆瓣250电影项目启动器")
    print("=" * 50)
    print()
    print("请选择要运行的版本:")
    print("1. 高级版本 (完整GUI界面) [推荐]")
    print("2. 改进版本 (命令行增强)")
    print("3. 原始版本 (简单脚本)")
    print("4. 网络诊断工具")
    print("5. 测试脚本")
    print("6. 查看项目信息")
    print("7. 退出")
    print()
    
    while True:
        try:
            choice = input("请输入选择 (1-7): ").strip()
            
            if choice == "1":
                print("🚀 启动高级版本（GUI界面）...")
                run_app("main.py")
                break
            elif choice == "2":
                print("🚀 启动改进版本...")
                run_app("versions/豆瓣250_新版.py")
                break
            elif choice == "3":
                print("🚀 启动原始版本...")
                run_app("versions/豆瓣250.py")
                break
            elif choice == "4":
                print("🔧 启动网络诊断工具...")
                run_app("tools/豆瓣250_诊断工具.py")
                break
            elif choice == "5":
                print("🧪 运行测试脚本...")
                run_app("tools/test_douban.py")
                break
            elif choice == "6":
                show_project_info()
            elif choice == "7":
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
        print(f"📂 运行文件: {script_path}")
        cmd = [sys.executable, script_path] + list(args)
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 应用运行失败: {e}")
        print("💡 提示: 请确保已安装所有依赖包 (pip install -r requirements.txt)")
    except FileNotFoundError:
        print("❌ Python解释器未找到")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

def show_project_info():
    """显示项目信息"""
    print()
    print("📋 豆瓣250电影项目信息")
    print("-" * 40)
    print("项目名称: 豆瓣250电影数据获取工具")
    print("版本数量: 3个主要版本")
    print("技术栈: Python, Tkinter, Requests, BeautifulSoup")
    print("功能: 电影数据获取, 海报下载, GUI界面, 数据导出")
    print()
    print("📁 项目结构:")
    show_file_structure()
    print()
    print("💡 推荐使用高级版本获得最佳体验！")
    print()

def show_file_structure():
    """显示文件结构"""
    structure = [
        "├── main.py (高级版本主程序)",
        "├── src/ (源代码)",
        "│   ├── core/ (核心模块)",
        "│   ├── ui/ (用户界面)",
        "│   └── utils/ (工具模块)",
        "├── versions/ (不同版本)",
        "│   ├── 豆瓣250.py (原始版本)",
        "│   ├── 豆瓣250_新版.py (改进版本)",
        "│   └── 启动豆瓣250.py (启动脚本)",
        "├── tools/ (工具和测试)",
        "│   ├── 豆瓣250_诊断工具.py",
        "│   └── test_douban.py",
        "├── docs/ (文档)",
        "├── data/ (数据存储)",
        "└── requirements.txt (依赖)"
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
            __import__(package.replace('-', '_'))
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
    
    # 检查依赖
    print("🔧 初始化检查...")
    if not os.path.exists("requirements.txt"):
        print("⚠️  未找到 requirements.txt 文件")
    
    main()
