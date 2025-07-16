#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主模块初始化文件
"""

from .core import *
from .ui import *
from .utils import *

__version__ = "2.0.0"
__author__ = "GitHub Copilot"
__description__ = "豆瓣电影Top250浏览器 - 模块化重构版"

__all__ = [
    # 核心模块
    'DoubanDataFetcher', 'NetworkTester',
    # UI模块
    'MainWindow', 'MovieDetailWindow', 'create_main_window',
    # 工具模块
    'ImageCache', 'ImageLoader', 'PosterManager',
    'Logger', 'ConfigManager', 'PerformanceMonitor', 'ResourceManager',
    'logger', 'config_manager', 'performance_monitor', 'resource_manager',
    'create_tooltip', 'format_duration', 'truncate_text',
    # 配置
    'HEADERS', 'TIMEOUT', 'RETRY_DELAY', 'MAX_RETRIES',
    'WINDOW_CONFIG', 'POSTER_CONFIG', 'COLORS', 'STYLES',
    'BACKUP_MOVIES'
]
