#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口界面
包含主界面的实现
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from typing import List, Dict, Optional
import webbrowser

from config import WINDOW_CONFIG, COLORS, STYLES
from utils import logger, center_window, create_tooltip, truncate_text
from data_fetcher import DoubanDataFetcher
from image_manager import PosterManager
from network_tester import NetworkTester


class MainWindow:
    """主窗口类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.movies: List[Dict] = []
        self.filtered_movies: List[Dict] = []
        self.current_page = 0
        self.movies_per_page = 10
        
        # 组件管理器
        self.data_fetcher = DoubanDataFetcher()
        self.poster_manager = PosterManager()
        self.network_tester = NetworkTester()
        
        # UI组件
        self.movie_listbox = None
        self.search_var = None
        self.status_var = None
        self.progress_var = None
        self.info_text = None
        self.page_label = None
        
        # 初始化
        self._init_window()
        self._init_ui()
        self._bind_events()
        
        # 启动时检查网络和加载数据
        self._startup_check()
    
    def _init_window(self):
        """初始化窗口"""
        self.root.title(WINDOW_CONFIG['title'])
        self.root.configure(bg=COLORS['bg'])
        
        # 设置窗口大小和位置
        center_window(self.root, WINDOW_CONFIG['width'], WINDOW_CONFIG['height'])
        self.root.minsize(WINDOW_CONFIG['min_width'], WINDOW_CONFIG['min_height'])
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def _init_ui(self):
        """初始化用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建顶部工具栏
        self._create_toolbar(main_frame)
        
        # 创建主要内容区域
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # 创建左侧电影列表
        self._create_movie_list(content_frame)
        
        # 创建右侧信息面板
        self._create_info_panel(content_frame)
        
        # 创建底部状态栏
        self._create_status_bar(main_frame)
    
    def _create_toolbar(self, parent):
        """创建工具栏"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # 搜索框
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_frame, text="搜索:", font=STYLES['text']['font']).pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                               font=STYLES['entry']['font'])
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        # 搜索按钮
        search_btn = ttk.Button(search_frame, text="搜索", 
                               command=self._search_movies)
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 操作按钮
        btn_frame = ttk.Frame(toolbar)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="刷新", 
                  command=self._refresh_data).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(btn_frame, text="网络测试", 
                  command=self._test_network).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(btn_frame, text="关于", 
                  command=self._show_about).pack(side=tk.LEFT)
    
    def _create_movie_list(self, parent):
        """创建电影列表"""
        # 左侧框架
        left_frame = ttk.Frame(parent)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 列表标题
        ttk.Label(left_frame, text="豆瓣电影Top250", 
                 font=STYLES['title']['font']).pack(anchor=tk.W, pady=(0, 10))
        
        # 列表框架
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 电影列表
        self.movie_listbox = tk.Listbox(list_frame, 
                                      font=STYLES['text']['font'],
                                      selectmode=tk.SINGLE,
                                      height=20)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                 command=self.movie_listbox.yview)
        self.movie_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.movie_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 分页控件
        page_frame = ttk.Frame(left_frame)
        page_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(page_frame, text="上一页", 
                  command=self._prev_page).pack(side=tk.LEFT)
        
        self.page_label = ttk.Label(page_frame, text="第 1 页")
        self.page_label.pack(side=tk.LEFT, padx=(10, 10))
        
        ttk.Button(page_frame, text="下一页", 
                  command=self._next_page).pack(side=tk.LEFT)
        
        ttk.Button(page_frame, text="跳转", 
                  command=self._jump_to_page).pack(side=tk.RIGHT)
    
    def _create_info_panel(self, parent):
        """创建信息面板"""
        # 右侧框架
        right_frame = ttk.Frame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # 信息标题
        ttk.Label(right_frame, text="电影信息", 
                 font=STYLES['title']['font']).pack(anchor=tk.W, pady=(0, 10))
        
        # 信息显示区域
        info_frame = ttk.Frame(right_frame)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, 
                                                  font=STYLES['text']['font'],
                                                  wrap=tk.WORD,
                                                  width=40,
                                                  height=25,
                                                  state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # 操作按钮
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="打开豆瓣页面", 
                  command=self._open_douban_page).pack(side=tk.LEFT)
        
        ttk.Button(btn_frame, text="查看详情", 
                  command=self._show_detail).pack(side=tk.RIGHT)
    
    def _create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 状态文本
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(status_frame, 
                                     variable=self.progress_var,
                                     length=200)
        progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
    
    def _bind_events(self):
        """绑定事件"""
        # 列表选择事件
        self.movie_listbox.bind('<<ListboxSelect>>', self._on_movie_select)
        
        # 搜索框回车事件
        self.search_var.trace('w', self._on_search_change)
        
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _startup_check(self):
        """启动检查"""
        def check_worker():
            try:
                self._update_status("正在检查网络连接...")
                network_result = self.network_tester.test_connection()
                
                if network_result['success']:
                    self._update_status("网络连接正常，正在加载数据...")
                    self._load_movies()
                else:
                    self._update_status("网络连接失败，使用离线数据...")
                    self._load_movies()
                    
            except Exception as e:
                logger.error(f"启动检查失败: {e}")
                self._update_status("启动检查失败")
        
        thread = threading.Thread(target=check_worker, daemon=True)
        thread.start()
    
    def _load_movies(self):
        """加载电影数据"""
        try:
            self._update_status("正在加载电影数据...")
            self._update_progress(0)
            
            # 获取电影数据
            self.movies = self.data_fetcher.get_movies()
            self.filtered_movies = self.movies.copy()
            
            # 更新UI
            self.root.after(0, self._update_movie_list)
            
            self._update_status(f"成功加载 {len(self.movies)} 部电影")
            self._update_progress(100)
            
        except Exception as e:
            logger.error(f"加载电影数据失败: {e}")
            self._update_status("加载数据失败")
    
    def _update_movie_list(self):
        """更新电影列表"""
        try:
            self.movie_listbox.delete(0, tk.END)
            
            # 计算当前页的电影
            start_idx = self.current_page * self.movies_per_page
            end_idx = start_idx + self.movies_per_page
            page_movies = self.filtered_movies[start_idx:end_idx]
            
            # 添加到列表
            for movie in page_movies:
                title = movie.get('title', '未知')
                year = movie.get('year', '')
                score = movie.get('score', '0.0')
                display_text = f"{movie.get('rank', 0):3d}. {title} ({year}) - {score}"
                self.movie_listbox.insert(tk.END, display_text)
            
            # 更新分页标签
            total_pages = (len(self.filtered_movies) - 1) // self.movies_per_page + 1
            self.page_label.config(text=f"第 {self.current_page + 1} 页 / 共 {total_pages} 页")
            
        except Exception as e:
            logger.error(f"更新电影列表失败: {e}")
    
    def _on_movie_select(self, event):
        """电影选择事件"""
        try:
            selection = self.movie_listbox.curselection()
            if not selection:
                return
            
            # 获取选中的电影
            movie_idx = selection[0] + self.current_page * self.movies_per_page
            if movie_idx < len(self.filtered_movies):
                movie = self.filtered_movies[movie_idx]
                self._display_movie_info(movie)
                
        except Exception as e:
            logger.error(f"处理电影选择事件失败: {e}")
    
    def _display_movie_info(self, movie: Dict):
        """显示电影信息"""
        try:
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            
            # 格式化电影信息
            info_text = f"""电影信息
{'='*30}

标题：{movie.get('title', '未知')}
年份：{movie.get('year', '未知')}
评分：{movie.get('score', '0.0')}
排名：{movie.get('rank', 0)}

导演：{movie.get('director', '未知')}
主演：{', '.join(movie.get('actors', []))}
类型：{movie.get('genre', '未知')}
国家：{movie.get('country', '未知')}

经典台词：
{movie.get('quote', '暂无')}

简介：
{movie.get('description', '暂无简介')}
"""
            
            self.info_text.insert(tk.END, info_text)
            self.info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            logger.error(f"显示电影信息失败: {e}")
    
    def _search_movies(self):
        """搜索电影"""
        try:
            search_text = self.search_var.get().strip().lower()
            
            if not search_text:
                self.filtered_movies = self.movies.copy()
            else:
                self.filtered_movies = []
                for movie in self.movies:
                    # 在标题、导演、演员中搜索
                    if (search_text in movie.get('title', '').lower() or
                        search_text in movie.get('director', '').lower() or
                        any(search_text in actor.lower() for actor in movie.get('actors', []))):
                        self.filtered_movies.append(movie)
            
            # 重置页面并更新列表
            self.current_page = 0
            self._update_movie_list()
            
            self._update_status(f"搜索结果: {len(self.filtered_movies)} 部电影")
            
        except Exception as e:
            logger.error(f"搜索电影失败: {e}")
    
    def _on_search_change(self, *args):
        """搜索框变化事件"""
        # 实时搜索
        self._search_movies()
    
    def _prev_page(self):
        """上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            self._update_movie_list()
    
    def _next_page(self):
        """下一页"""
        total_pages = (len(self.filtered_movies) - 1) // self.movies_per_page + 1
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self._update_movie_list()
    
    def _jump_to_page(self):
        """跳转到页面"""
        try:
            page_str = tk.simpledialog.askstring("跳转", "请输入页码:")
            if page_str:
                page = int(page_str) - 1
                total_pages = (len(self.filtered_movies) - 1) // self.movies_per_page + 1
                if 0 <= page < total_pages:
                    self.current_page = page
                    self._update_movie_list()
                else:
                    messagebox.showerror("错误", f"页码超出范围 (1-{total_pages})")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def _refresh_data(self):
        """刷新数据"""
        def refresh_worker():
            try:
                self._update_status("正在刷新数据...")
                self.data_fetcher.clear_cache()
                self._load_movies()
            except Exception as e:
                logger.error(f"刷新数据失败: {e}")
                self._update_status("刷新失败")
        
        thread = threading.Thread(target=refresh_worker, daemon=True)
        thread.start()
    
    def _test_network(self):
        """测试网络"""
        def test_worker():
            try:
                self._update_status("正在测试网络...")
                result = self.network_tester.test_connection()
                
                if result['success']:
                    message = f"网络连接正常\n延迟: {result['latency']:.0f}ms"
                    messagebox.showinfo("网络测试", message)
                else:
                    message = f"网络连接失败\n错误: {result['message']}"
                    messagebox.showerror("网络测试", message)
                
                self._update_status("网络测试完成")
                
            except Exception as e:
                logger.error(f"网络测试失败: {e}")
                messagebox.showerror("网络测试", f"测试失败: {e}")
        
        thread = threading.Thread(target=test_worker, daemon=True)
        thread.start()
    
    def _show_about(self):
        """显示关于信息"""
        about_text = """豆瓣电影Top250浏览器
        
版本：2.0.0
作者：开发者
        
功能特点：
• 浏览豆瓣Top250电影
• 搜索和过滤功能
• 电影详情展示
• 网络状态检测
• 离线数据支持

技术栈：
• Python 3.x
• tkinter (GUI)
• requests (网络请求)
• BeautifulSoup (网页解析)
• PIL (图像处理)
"""
        
        messagebox.showinfo("关于", about_text)
    
    def _open_douban_page(self):
        """打开豆瓣页面"""
        try:
            selection = self.movie_listbox.curselection()
            if not selection:
                messagebox.showwarning("提示", "请先选择一部电影")
                return
            
            movie_idx = selection[0] + self.current_page * self.movies_per_page
            if movie_idx < len(self.filtered_movies):
                movie = self.filtered_movies[movie_idx]
                url = movie.get('detail_url', '')
                if url:
                    webbrowser.open(url)
                else:
                    messagebox.showwarning("提示", "该电影没有详情链接")
                    
        except Exception as e:
            logger.error(f"打开豆瓣页面失败: {e}")
            messagebox.showerror("错误", f"打开页面失败: {e}")
    
    def _show_detail(self):
        """显示详情窗口"""
        try:
            selection = self.movie_listbox.curselection()
            if not selection:
                messagebox.showwarning("提示", "请先选择一部电影")
                return
            
            movie_idx = selection[0] + self.current_page * self.movies_per_page
            if movie_idx < len(self.filtered_movies):
                movie = self.filtered_movies[movie_idx]
                # 这里可以创建详情窗口
                messagebox.showinfo("详情", f"电影详情功能开发中...\n\n选中电影：{movie.get('title', '未知')}")
                
        except Exception as e:
            logger.error(f"显示详情失败: {e}")
            messagebox.showerror("错误", f"显示详情失败: {e}")
    
    def _update_status(self, message: str):
        """更新状态栏"""
        self.root.after(0, lambda: self.status_var.set(message))
    
    def _update_progress(self, value: float):
        """更新进度条"""
        self.root.after(0, lambda: self.progress_var.set(value))
    
    def _on_closing(self):
        """窗口关闭事件"""
        try:
            logger.info("程序正在关闭...")
            self.root.destroy()
        except Exception as e:
            logger.error(f"关闭程序时发生错误: {e}")
    
    def run(self):
        """运行主循环"""
        try:
            logger.info("启动主窗口")
            self.root.mainloop()
        except Exception as e:
            logger.error(f"主循环运行错误: {e}")
            raise


def create_main_window():
    """创建主窗口"""
    return MainWindow()


if __name__ == "__main__":
    # 导入缺失的模块
    import tkinter.simpledialog
    
    app = create_main_window()
    app.run()
