#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口模块
包含主界面的实现
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import List, Dict, Optional, Any

from ..core.data_fetcher import DoubanDataFetcher
from ..core.network import NetworkTester
from ..core.config import WINDOW_CONFIG, STYLES, COLORS
from ..utils.image import PosterManager
from ..utils.helpers import logger, performance_monitor, create_tooltip
from .detail_window import MovieDetailWindow


class MainWindow:
    """主窗口类"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.movies: List[Dict] = []
        self.current_movie_data: Dict = {}
        self.poster_manager = PosterManager()
        self.data_fetcher = DoubanDataFetcher()
        self.network_tester = NetworkTester()
        self.hover_poster_label: Optional[tk.Label] = None
        self.detail_window: Optional[MovieDetailWindow] = None
        
        # 初始化界面
        self._init_window()
        self._init_widgets()
        self._bind_events()
        
        # 启动时加载数据
        self.load_data()
    
    def _init_window(self) -> None:
        """初始化窗口"""
        self.root.title("豆瓣电影Top250")
        self.root.geometry(f"{WINDOW_CONFIG['width']}x{WINDOW_CONFIG['height']}")
        self.root.minsize(WINDOW_CONFIG['min_width'], WINDOW_CONFIG['min_height'])
        self.root.configure(bg=COLORS['bg'])
        
        # 居中显示
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _init_widgets(self) -> None:
        """初始化界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建顶部工具栏
        self._create_toolbar(main_frame)
        
        # 创建内容区域
        self._create_content_area(main_frame)
        
        # 创建状态栏
        self._create_status_bar(main_frame)
        
        # 应用样式
        self._apply_styles()
    
    def _create_toolbar(self, parent: ttk.Frame) -> None:
        """创建工具栏"""
        toolbar_frame = ttk.Frame(parent, style="Toolbar.TFrame")
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 刷新按钮
        self.refresh_btn = ttk.Button(
            toolbar_frame, 
            text="刷新数据", 
            command=self.refresh_data,
            style="Toolbar.TButton"
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        create_tooltip(self.refresh_btn, "重新获取豆瓣Top250数据")
        
        # 网络测试按钮
        self.network_btn = ttk.Button(
            toolbar_frame,
            text="网络测试",
            command=self.test_network,
            style="Toolbar.TButton"
        )
        self.network_btn.pack(side=tk.LEFT, padx=(0, 10))
        create_tooltip(self.network_btn, "测试网络连接状态")
        
        # 清除缓存按钮
        self.clear_cache_btn = ttk.Button(
            toolbar_frame,
            text="清除缓存",
            command=self.clear_cache,
            style="Toolbar.TButton"
        )
        self.clear_cache_btn.pack(side=tk.LEFT, padx=(0, 10))
        create_tooltip(self.clear_cache_btn, "清除图片缓存")
        
        # 加载状态标签
        self.loading_label = ttk.Label(
            toolbar_frame,
            text="",
            style="Loading.TLabel"
        )
        self.loading_label.pack(side=tk.RIGHT)
    
    def _create_content_area(self, parent: ttk.Frame) -> None:
        """创建内容区域"""
        content_frame = ttk.Frame(parent, style="Content.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建电影列表
        self._create_movie_list(content_frame)
        
        # 创建海报显示区域
        self._create_poster_area(content_frame)
    
    def _create_movie_list(self, parent: ttk.Frame) -> None:
        """创建电影列表"""
        # 列表框架
        list_frame = ttk.Frame(parent, style="List.TFrame")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 搜索框
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="搜索:", style="Search.TLabel").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            style="Search.TEntry"
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.search_var.trace('w', self._on_search)
        
        # 电影列表
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建Treeview
        self.movie_tree = ttk.Treeview(
            list_container,
            columns=('rank', 'title', 'rating', 'year'),
            show='headings',
            style="Movie.Treeview"
        )
        
        # 设置列标题
        self.movie_tree.heading('rank', text='排名')
        self.movie_tree.heading('title', text='电影名称')
        self.movie_tree.heading('rating', text='评分')
        self.movie_tree.heading('year', text='年份')
        
        # 设置列宽
        self.movie_tree.column('rank', width=60, anchor='center')
        self.movie_tree.column('title', width=200, anchor='w')
        self.movie_tree.column('rating', width=60, anchor='center')
        self.movie_tree.column('year', width=80, anchor='center')
        
        # 滚动条
        scrollbar_y = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.movie_tree.yview)
        scrollbar_x = ttk.Scrollbar(list_container, orient=tk.HORIZONTAL, command=self.movie_tree.xview)
        
        self.movie_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 布局
        self.movie_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _create_poster_area(self, parent: ttk.Frame) -> None:
        """创建海报显示区域"""
        poster_frame = ttk.Frame(parent, style="Poster.TFrame")
        poster_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # 海报标签
        self.poster_label = ttk.Label(
            poster_frame,
            text="将鼠标悬停在电影名称上\n查看海报",
            style="Poster.TLabel",
            anchor="center"
        )
        self.poster_label.pack(pady=20)
    
    def _create_status_bar(self, parent: ttk.Frame) -> None:
        """创建状态栏"""
        status_frame = ttk.Frame(parent, style="Status.TFrame")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(
            status_frame,
            text="准备就绪",
            style="Status.TLabel"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # 电影计数标签
        self.count_label = ttk.Label(
            status_frame,
            text="",
            style="Status.TLabel"
        )
        self.count_label.pack(side=tk.RIGHT)
    
    def _apply_styles(self) -> None:
        """应用样式"""
        style = ttk.Style()
        
        # 配置各种样式
        for style_name, style_config in STYLES.items():
            style.configure(style_name, **style_config)
    
    def _bind_events(self) -> None:
        """绑定事件"""
        # 电影列表事件
        self.movie_tree.bind('<Motion>', self._on_movie_hover)
        self.movie_tree.bind('<Leave>', self._on_movie_leave)
        self.movie_tree.bind('<Double-1>', self._on_movie_double_click)
        self.movie_tree.bind('<Return>', self._on_movie_double_click)
        
        # 窗口事件
        self.root.bind('<Control-r>', lambda e: self.refresh_data())
        self.root.bind('<F5>', lambda e: self.refresh_data())
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus())
        
        # 搜索框事件
        self.search_entry.bind('<Escape>', lambda e: self.search_var.set(''))
    
    @performance_monitor.measure_time
    def load_data(self) -> None:
        """加载数据"""
        self._set_loading_state(True)
        self.update_status("正在加载电影数据...")
        
        def load_task():
            try:
                # 获取电影数据
                movies = self.data_fetcher.get_movies()
                
                # 在主线程中更新界面
                self.root.after(0, self._update_movie_list, movies)
                
            except Exception as e:
                error_msg = f"数据加载失败: {str(e)}"
                logger.error(error_msg)
                self.root.after(0, self._show_error, error_msg)
            finally:
                self.root.after(0, self._set_loading_state, False)
        
        threading.Thread(target=load_task, daemon=True).start()
    
    def refresh_data(self) -> None:
        """刷新数据"""
        self.data_fetcher.clear_cache()
        self.load_data()
    
    def test_network(self) -> None:
        """测试网络连接"""
        self.update_status("正在测试网络连接...")
        
        def test_task():
            try:
                is_connected = self.network_tester.test_douban_connection()
                status = "网络连接正常" if is_connected else "网络连接失败"
                self.root.after(0, self.update_status, status)
                
                if not is_connected:
                    self.root.after(0, messagebox.showwarning, "网络测试", "无法连接到豆瓣网站，可能影响数据获取")
                    
            except Exception as e:
                error_msg = f"网络测试失败: {str(e)}"
                logger.error(error_msg)
                self.root.after(0, self.update_status, error_msg)
        
        threading.Thread(target=test_task, daemon=True).start()
    
    def clear_cache(self) -> None:
        """清除缓存"""
        self.poster_manager.clear_cache()
        cache_info = self.poster_manager.get_cache_info()
        messagebox.showinfo("缓存清除", f"已清除 {cache_info['size']} 个缓存图片")
        self.update_status("缓存已清除")
    
    def _update_movie_list(self, movies: List[Dict]) -> None:
        """更新电影列表"""
        self.movies = movies
        self.current_movie_data = {movie['title']: movie for movie in movies}
        
        # 清空当前列表
        for item in self.movie_tree.get_children():
            self.movie_tree.delete(item)
        
        # 添加电影数据
        for movie in movies:
            self.movie_tree.insert('', 'end', values=(
                movie['rank'],
                movie['title'],
                movie['rating'],
                movie.get('year', '未知')
            ))
        
        # 更新状态
        self.update_status("数据加载完成")
        self.count_label.config(text=f"共 {len(movies)} 部电影")
    
    def _on_search(self, *args) -> None:
        """搜索过滤"""
        search_text = self.search_var.get().lower()
        
        # 清空当前列表
        for item in self.movie_tree.get_children():
            self.movie_tree.delete(item)
        
        # 过滤并添加匹配的电影
        filtered_movies = []
        for movie in self.movies:
            if (search_text in movie['title'].lower() or 
                search_text in movie.get('year', '').lower() or
                search_text in str(movie.get('rating', ''))):
                filtered_movies.append(movie)
                self.movie_tree.insert('', 'end', values=(
                    movie['rank'],
                    movie['title'],
                    movie['rating'],
                    movie.get('year', '未知')
                ))
        
        # 更新计数
        self.count_label.config(text=f"显示 {len(filtered_movies)} / {len(self.movies)} 部电影")
    
    def _on_movie_hover(self, event) -> None:
        """电影悬停事件"""
        item = self.movie_tree.identify_row(event.y)
        if item:
            values = self.movie_tree.item(item)['values']
            if values:
                title = values[1]  # 电影名称
                movie = self.current_movie_data.get(title)
                if movie and movie.get('poster'):
                    self._show_hover_poster(movie['poster'])
    
    def _on_movie_leave(self, event) -> None:
        """电影离开事件"""
        self._hide_hover_poster()
    
    def _on_movie_double_click(self, event) -> None:
        """电影双击事件"""
        selection = self.movie_tree.selection()
        if selection:
            item = selection[0]
            values = self.movie_tree.item(item)['values']
            if values:
                title = values[1]  # 电影名称
                movie = self.current_movie_data.get(title)
                if movie:
                    self._show_movie_detail(movie)
    
    def _show_hover_poster(self, poster_url: str) -> None:
        """显示悬停海报"""
        def on_poster_loaded(photo):
            self.poster_label.config(image=photo, text="")
            self.poster_label.image = photo  # 保持引用
        
        def on_poster_error(error):
            logger.warning(f"海报加载失败: {error}")
        
        self.poster_manager.load_hover_poster(poster_url, on_poster_loaded, on_poster_error)
    
    def _hide_hover_poster(self) -> None:
        """隐藏悬停海报"""
        self.poster_label.config(image="", text="将鼠标悬停在电影名称上\n查看海报")
        self.poster_label.image = None
    
    def _show_movie_detail(self, movie: Dict) -> None:
        """显示电影详情"""
        if self.detail_window:
            self.detail_window.destroy()
        
        self.detail_window = MovieDetailWindow(self.root, movie, self.poster_manager)
        self.detail_window.show()
    
    def _set_loading_state(self, loading: bool) -> None:
        """设置加载状态"""
        if loading:
            self.loading_label.config(text="加载中...")
            self.refresh_btn.config(state='disabled')
        else:
            self.loading_label.config(text="")
            self.refresh_btn.config(state='normal')
    
    def _show_error(self, error_msg: str) -> None:
        """显示错误信息"""
        messagebox.showerror("错误", error_msg)
        self.update_status(error_msg)
    
    def update_status(self, message: str) -> None:
        """更新状态栏"""
        self.status_label.config(text=message)
        logger.info(f"状态: {message}")
    
    def run(self) -> None:
        """运行主循环"""
        self.root.mainloop()


def create_main_window() -> MainWindow:
    """创建主窗口"""
    root = tk.Tk()
    return MainWindow(root)
