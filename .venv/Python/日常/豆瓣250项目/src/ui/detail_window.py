#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电影详情窗口模块
包含电影详情界面的实现
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from typing import Dict, Optional

from ..core.config import WINDOW_CONFIG, COLORS
from ..utils.helpers import logger, create_tooltip


class MovieDetailWindow:
    """电影详情窗口类"""
    
    def __init__(self, parent: tk.Tk, movie: Dict, poster_manager):
        self.parent = parent
        self.movie = movie
        self.poster_manager = poster_manager
        self.window: Optional[tk.Toplevel] = None
        self.poster_label: Optional[tk.Label] = None
        
        self._create_window()
        self._create_widgets()
        self._load_poster()
    
    def _create_window(self) -> None:
        """创建窗口"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"电影详情 - {self.movie['title']}")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        self.window.configure(bg=COLORS['bg'])
        
        # 居中显示
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (300)
        y = (self.window.winfo_screenheight() // 2) - (250)
        self.window.geometry(f'600x500+{x}+{y}')
        
        # 设置为模态窗口
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # 绑定关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.destroy)
    
    def _create_widgets(self) -> None:
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建顶部信息区域
        self._create_header(main_frame)
        
        # 创建内容区域
        self._create_content(main_frame)
        
        # 创建按钮区域
        self._create_buttons(main_frame)
    
    def _create_header(self, parent: ttk.Frame) -> None:
        """创建顶部信息区域"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 左侧海报区域
        poster_frame = ttk.Frame(header_frame)
        poster_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        self.poster_label = ttk.Label(
            poster_frame,
            text="加载中...",
            width=20,
            anchor="center",
            relief="sunken",
            background=COLORS['bg']
        )
        self.poster_label.pack()
        
        # 右侧信息区域
        info_frame = ttk.Frame(header_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 电影标题
        title_label = ttk.Label(
            info_frame,
            text=self.movie['title'],
            font=('Arial', 16, 'bold'),
            foreground=COLORS['primary']
        )
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # 基本信息
        info_items = [
            ("排名", f"#{self.movie['rank']}"),
            ("评分", f"{self.movie['rating']} 分"),
            ("年份", self.movie.get('year', '未知')),
            ("类型", self.movie.get('genre', '未知')),
            ("导演", self.movie.get('director', '未知')),
            ("主演", self.movie.get('actors', '未知'))
        ]
        
        for label, value in info_items:
            self._create_info_item(info_frame, label, value)
    
    def _create_info_item(self, parent: ttk.Frame, label: str, value: str) -> None:
        """创建信息项"""
        item_frame = ttk.Frame(parent)
        item_frame.pack(fill=tk.X, pady=2)
        
        label_widget = ttk.Label(
            item_frame,
            text=f"{label}:",
            width=8,
            anchor="w",
            font=('Arial', 10, 'bold')
        )
        label_widget.pack(side=tk.LEFT)
        
        value_widget = ttk.Label(
            item_frame,
            text=value,
            anchor="w",
            font=('Arial', 10)
        )
        value_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 为长文本添加提示框
        if len(value) > 30:
            create_tooltip(value_widget, value)
    
    def _create_content(self, parent: ttk.Frame) -> None:
        """创建内容区域"""
        content_frame = ttk.LabelFrame(parent, text="电影简介", padding=10)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 简介文本
        description = self.movie.get('description', '暂无简介')
        
        # 创建文本框和滚动条
        text_frame = ttk.Frame(content_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.description_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=('Arial', 10),
            bg=COLORS['bg'],
            fg=COLORS['text'],
            relief="flat",
            padx=10,
            pady=10
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.description_text.yview)
        self.description_text.configure(yscrollcommand=scrollbar.set)
        
        self.description_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 插入简介内容
        self.description_text.insert(tk.END, description)
        self.description_text.config(state=tk.DISABLED)
    
    def _create_buttons(self, parent: ttk.Frame) -> None:
        """创建按钮区域"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)
        
        # 打开豆瓣链接按钮
        if self.movie.get('link'):
            open_link_btn = ttk.Button(
                button_frame,
                text="在豆瓣中查看",
                command=self._open_douban_link
            )
            open_link_btn.pack(side=tk.LEFT, padx=(0, 10))
            create_tooltip(open_link_btn, "在浏览器中打开豆瓣电影页面")
        
        # 关闭按钮
        close_btn = ttk.Button(
            button_frame,
            text="关闭",
            command=self.destroy
        )
        close_btn.pack(side=tk.RIGHT)
        
        # 绑定ESC键关闭
        self.window.bind('<Escape>', lambda e: self.destroy())
        
        # 设置焦点到关闭按钮
        close_btn.focus_set()
    
    def _load_poster(self) -> None:
        """加载海报"""
        poster_url = self.movie.get('poster')
        if poster_url:
            def on_poster_loaded(photo):
                if self.poster_label:
                    self.poster_label.config(image=photo, text="")
                    self.poster_label.image = photo  # 保持引用
            
            def on_poster_error(error):
                logger.warning(f"详情页海报加载失败: {error}")
                if self.poster_label:
                    self.poster_label.config(text="海报加载失败")
            
            self.poster_manager.load_detail_poster(poster_url, on_poster_loaded, on_poster_error)
        else:
            self.poster_label.config(text="暂无海报")
    
    def _open_douban_link(self) -> None:
        """打开豆瓣链接"""
        link = self.movie.get('link')
        if link:
            try:
                webbrowser.open(link)
                logger.info(f"打开豆瓣链接: {link}")
            except Exception as e:
                logger.error(f"打开链接失败: {e}")
                messagebox.showerror("错误", f"无法打开链接: {str(e)}")
    
    def show(self) -> None:
        """显示窗口"""
        if self.window:
            self.window.deiconify()
            self.window.lift()
            self.window.focus_set()
    
    def destroy(self) -> None:
        """销毁窗口"""
        if self.window:
            self.window.destroy()
            self.window = None
    
    def is_alive(self) -> bool:
        """检查窗口是否存在"""
        return self.window is not None and self.window.winfo_exists()
