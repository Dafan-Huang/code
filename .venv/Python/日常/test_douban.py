#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试豆瓣250程序的启动脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from 豆瓣250 import *
    print("程序模块导入成功!")
    
    # 测试启动
    if __name__ == '__main__':
        print("启动豆瓣250程序...")
        root = tk.Tk()
        app = DoubanApp(root)
        print("程序界面初始化完成!")
        print("窗口大小:", root.geometry())
        root.mainloop()
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保安装了所需的依赖包:")
    print("pip install requests beautifulsoup4 pillow")
except Exception as e:
    print(f"程序启动失败: {e}")
