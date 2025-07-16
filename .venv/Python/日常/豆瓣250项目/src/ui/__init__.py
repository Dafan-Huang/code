#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI模块初始化文件
"""

from .main_window import MainWindow, create_main_window
from .detail_window import MovieDetailWindow

__all__ = ['MainWindow', 'MovieDetailWindow', 'create_main_window']
