#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用工具模块
包含工具函数和辅助功能
"""

import os
import sys
import json
import threading
import time
from typing import Dict, Any, Optional
from datetime import datetime


class Logger:
    """简单的日志记录器"""
    
    def __init__(self, log_file: str = None):
        self.log_file = log_file
        self._lock = threading.Lock()
    
    def log(self, level: str, message: str) -> None:
        """
        记录日志
        
        Args:
            level: 日志级别
            message: 日志消息
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        
        with self._lock:
            print(log_entry)
            
            if self.log_file:
                try:
                    with open(self.log_file, 'a', encoding='utf-8') as f:
                        f.write(log_entry + '\n')
                except Exception as e:
                    print(f"日志写入失败: {e}")
    
    def info(self, message: str) -> None:
        """记录信息日志"""
        self.log("INFO", message)
    
    def warning(self, message: str) -> None:
        """记录警告日志"""
        self.log("WARNING", message)
    
    def error(self, message: str) -> None:
        """记录错误日志"""
        self.log("ERROR", message)
    
    def debug(self, message: str) -> None:
        """记录调试日志"""
        self.log("DEBUG", message)


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file
        self.config = {}
        self._lock = threading.Lock()
        
        if config_file and os.path.exists(config_file):
            self.load()
    
    def load(self) -> None:
        """加载配置"""
        if not self.config_file:
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"配置加载失败: {e}")
            self.config = {}
    
    def save(self) -> None:
        """保存配置"""
        if not self.config_file:
            return
        
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"配置保存失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        with self._lock:
            return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        with self._lock:
            self.config[key] = value
    
    def update(self, new_config: Dict) -> None:
        """更新配置"""
        with self._lock:
            self.config.update(new_config)


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, logger: Logger = None):
        self.logger = logger or Logger()
        self._timers = {}
        self._lock = threading.Lock()
    
    def start_timer(self, name: str) -> None:
        """开始计时"""
        with self._lock:
            self._timers[name] = time.time()
    
    def end_timer(self, name: str) -> float:
        """结束计时并返回耗时"""
        with self._lock:
            if name not in self._timers:
                return 0.0
            
            elapsed = time.time() - self._timers[name]
            del self._timers[name]
            
            self.logger.debug(f"性能监控 - {name}: {elapsed:.4f}秒")
            return elapsed
    
    def measure_time(self, func):
        """装饰器：测量函数执行时间"""
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            self.start_timer(func_name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                self.end_timer(func_name)
        return wrapper


class ResourceManager:
    """资源管理器"""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        self.ensure_data_dir()
    
    def ensure_data_dir(self) -> None:
        """确保数据目录存在"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_data_path(self, filename: str) -> str:
        """获取数据文件路径"""
        return os.path.join(self.data_dir, filename)
    
    def save_data(self, filename: str, data: Any) -> bool:
        """保存数据到文件"""
        try:
            filepath = self.get_data_path(filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"数据保存失败: {e}")
            return False
    
    def load_data(self, filename: str) -> Optional[Any]:
        """从文件加载数据"""
        try:
            filepath = self.get_data_path(filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"数据加载失败: {e}")
        return None
    
    def get_resource_path(self, *paths) -> str:
        """获取资源文件路径"""
        if getattr(sys, 'frozen', False):
            # 打包后的路径
            base_path = sys._MEIPASS
        else:
            # 开发环境路径
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(base_path, *paths)


def create_tooltip(widget, text: str):
    """
    为控件创建提示框
    
    Args:
        widget: tkinter控件
        text: 提示文本
    """
    import tkinter as tk
    
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        label = tk.Label(tooltip, text=text, background='#FFFFE0', 
                        relief='solid', borderwidth=1, font=('Arial', 8))
        label.pack()
        
        widget.tooltip = tooltip
    
    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            delattr(widget, 'tooltip')
    
    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)


def format_duration(seconds: float) -> str:
    """
    格式化时长显示
    
    Args:
        seconds: 秒数
        
    Returns:
        str: 格式化的时长字符串
    """
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        sec = seconds % 60
        return f"{int(minutes)}分{sec:.1f}秒"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)}小时{int(minutes)}分钟"


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    截断文本
    
    Args:
        text: 原文本
        max_length: 最大长度
        
    Returns:
        str: 截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


# 全局实例
logger = Logger()
config_manager = ConfigManager()
performance_monitor = PerformanceMonitor(logger)
resource_manager = ResourceManager()
