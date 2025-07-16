#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣电影Top250浏览器
主程序入口文件
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)

try:
    from ui.main_window import create_main_window
    from utils.helpers import logger
    from core.config import WINDOW_CONFIG
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖模块都已正确安装")
    sys.exit(1)


def check_dependencies():
    """检查依赖项"""
    required_modules = [
        'tkinter', 'requests', 'bs4', 'PIL', 'threading', 'json'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"缺少以下依赖模块: {', '.join(missing_modules)}"
        print(error_msg)
        if 'tkinter' not in missing_modules:
            messagebox.showerror("依赖错误", error_msg)
        return False
    
    return True


def main():
    """主函数"""
    # 检查依赖项
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # 设置应用程序信息
        logger.info("启动豆瓣电影Top250浏览器")
        logger.info("版本: 2.0.0 - 模块化重构版")
        
        # 创建主窗口
        main_window = create_main_window()
        
        # 运行应用程序
        main_window.run()
        
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        sys.exit(0)
    except Exception as e:
        error_msg = f"程序运行错误: {str(e)}"
        logger.error(error_msg)
        
        # 显示错误对话框
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("程序错误", error_msg)
        except:
            pass
        
        sys.exit(1)
    finally:
        logger.info("程序结束")


if __name__ == "__main__":
    main()
