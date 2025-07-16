#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
包含日志、性能监控等工具函数
"""

import os
import sys
import time
import threading
from datetime import datetime
from typing import Any, Callable, Dict, Optional

class Logger:
    """简单的日志记录器"""
    
    def __init__(self, log_file: str = None):
        self.log_file = log_file
        self.lock = threading.Lock()
    
    def _write_log(self, level: str, message: str):
        """写入日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] [{level}] {message}"
        
        with self.lock:
            # 打印到控制台
            print(log_msg)
            
            # 写入文件
            if self.log_file:
                try:
                    with open(self.log_file, 'a', encoding='utf-8') as f:
                        f.write(log_msg + '\n')
                except Exception as e:
                    print(f"写入日志文件失败: {e}")
    
    def info(self, message: str):
        """信息日志"""
        self._write_log('INFO', message)
    
    def warning(self, message: str):
        """警告日志"""
        self._write_log('WARNING', message)
    
    def error(self, message: str):
        """错误日志"""
        self._write_log('ERROR', message)
    
    def debug(self, message: str):
        """调试日志"""
        self._write_log('DEBUG', message)


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, logger: Logger = None):
        self.logger = logger or Logger()
        self.timers: Dict[str, float] = {}
    
    def start_timer(self, name: str):
        """开始计时"""
        self.timers[name] = time.time()
    
    def end_timer(self, name: str):
        """结束计时并记录"""
        if name in self.timers:
            elapsed = time.time() - self.timers[name]
            self.logger.info(f"性能监控 - {name}: {elapsed:.4f}秒")
            del self.timers[name]
            return elapsed
        return None
    
    def measure_time(self, func: Callable, *args, **kwargs) -> Any:
        """测量函数执行时间"""
        func_name = func.__name__
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            self.logger.info(f"函数 {func_name} 执行时间: {elapsed:.4f}秒")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.error(f"函数 {func_name} 执行失败 (耗时: {elapsed:.4f}秒): {e}")
            raise


def safe_execute(func: Callable, *args, default=None, **kwargs) -> Any:
    """安全执行函数"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"执行函数 {func.__name__} 时发生错误: {e}")
        return default


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"


def ensure_dir(dir_path: str) -> bool:
    """确保目录存在"""
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"创建目录失败 {dir_path}: {e}")
        return False


def truncate_text(text: str, max_length: int = 50) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def create_tooltip(widget, text: str):
    """创建工具提示"""
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        
        label = tk.Label(tooltip, text=text, 
                        background="lightyellow",
                        relief="solid", borderwidth=1,
                        font=("Microsoft YaHei", 9))
        label.pack()
        
        widget.tooltip = tooltip
    
    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            del widget.tooltip
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def center_window(window, width: int, height: int):
    """窗口居中"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")


def validate_url(url: str) -> bool:
    """验证URL格式"""
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def get_image_size(image_path: str) -> tuple:
    """获取图片尺寸"""
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        logger.error(f"获取图片尺寸失败 {image_path}: {e}")
        return (0, 0)


# 全局实例
logger = Logger('douban_movie.log')
performance_monitor = PerformanceMonitor(logger)

# 导入tkinter用于工具提示
try:
    import tkinter as tk
except ImportError:
    # 如果tkinter不可用，创建一个空的工具提示函数
    def create_tooltip(widget, text: str):
        pass
