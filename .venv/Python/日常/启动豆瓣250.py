#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣250程序测试启动脚本
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_imports():
    """测试依赖包导入"""
    try:
        import requests
        import bs4
        import PIL
        print("✅ 所有依赖包导入成功")
        return True
    except ImportError as e:
        print(f"❌ 依赖包导入失败: {e}")
        print("请运行: pip install requests beautifulsoup4 pillow")
        return False

def show_instructions():
    """显示使用说明"""
    instructions = """
🎬 豆瓣电影Top250 - 使用说明

📋 主要功能：
• 获取豆瓣Top250电影列表
• 鼠标悬停查看海报
• 双击电影名称查看详情
• 标记看过状态
• 筛选和分页浏览

🖱️ 操作指南：
1. 点击"获取豆瓣Top250"加载数据
2. 鼠标悬停在电影名上查看海报
3. 双击电影名称打开详情窗口
4. 点击"看过"列标记状态
5. 使用筛选和分页功能

💡 新功能：
• 双击电影名称打开详情窗口
• 查看导演、主演、类型等信息
• 异步加载海报和详细信息
• 支持打开豆瓣电影页面

祝您使用愉快！
"""
    
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo("豆瓣250使用说明", instructions)
    root.destroy()

def main():
    """主函数"""
    print("🎬 豆瓣电影Top250程序启动中...")
    print("=" * 50)
    
    # 检查依赖
    if not test_imports():
        return
    
    # 显示使用说明
    show_instructions()
    
    # 启动主程序
    try:
        print("🚀 正在启动程序...")
        exec(open('豆瓣250.py', encoding='utf-8').read())
        
    except FileNotFoundError:
        print("❌ 找不到豆瓣250.py文件")
        print("请确保在正确的目录中运行此脚本")
        
    except Exception as e:
        print(f"❌ 程序启动失败: {e}")
        print("请检查程序文件是否完整")

if __name__ == '__main__':
    main()
