#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣电影Top250浏览器
完整单文件版本
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import threading
import requests
import time
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import webbrowser
import random
from datetime import datetime
import hashlib
from io import BytesIO

# 尝试导入PIL，如果失败则不使用图片功能
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL未安装，图片功能将不可用")

# 配置常量
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

REQUEST_DELAY = 1
RETRY_DELAY = 2
MAX_RETRIES = 3
TIMEOUT = 15

WINDOW_CONFIG = {
    'title': '豆瓣电影Top250',
    'width': 1000,
    'height': 700,
    'min_width': 800,
    'min_height': 600
}

COLORS = {
    'bg': '#f5f5f5',
    'primary': '#1890ff',
    'text': '#262626',
    'text_secondary': '#8c8c8c'
}

STYLES = {
    'title': {'font': ('Microsoft YaHei', 16, 'bold')},
    'subtitle': {'font': ('Microsoft YaHei', 12, 'bold')},
    'text': {'font': ('Microsoft YaHei', 10)}
}

# 备用电影数据
BACKUP_MOVIES = [
    {
        'rank': 1, 'title': '肖申克的救赎', 'year': '1994', 'score': '9.7',
        'director': '弗兰克·德拉邦特', 'actors': ['蒂姆·罗宾斯', '摩根·弗里曼'],
        'genre': '剧情/犯罪', 'country': '美国',
        'detail_url': 'https://movie.douban.com/subject/1292052/',
        'quote': '希望让人自由。',
        'description': '20世纪40年代末，小有成就的青年银行家安迪因涉嫌杀害妻子及她的情人而锒铛入狱。'
    },
    {
        'rank': 2, 'title': '霸王别姬', 'year': '1993', 'score': '9.6',
        'director': '陈凯歌', 'actors': ['张国荣', '张丰毅', '巩俐'],
        'genre': '剧情/爱情/同性', 'country': '中国大陆',
        'detail_url': 'https://movie.douban.com/subject/1291546/',
        'quote': '风华绝代。',
        'description': '段小楼与程蝶衣是一对打小一起长大的师兄弟，两人一个演生，一个演旦。'
    },
    {
        'rank': 3, 'title': '阿甘正传', 'year': '1994', 'score': '9.5',
        'director': '罗伯特·泽米吉斯', 'actors': ['汤姆·汉克斯', '罗宾·怀特'],
        'genre': '剧情/爱情', 'country': '美国',
        'detail_url': 'https://movie.douban.com/subject/1292720/',
        'quote': '一部美国近现代史。',
        'description': '阿甘于二战结束后不久出生在美国南方阿拉巴马州一个闭塞的小镇。'
    },
    {
        'rank': 4, 'title': '泰坦尼克号', 'year': '1997', 'score': '9.4',
        'director': '詹姆斯·卡梅隆', 'actors': ['莱昂纳多·迪卡普里奥', '凯特·温丝莱特'],
        'genre': '剧情/爱情/灾难', 'country': '美国',
        'detail_url': 'https://movie.douban.com/subject/1292722/',
        'quote': '失去的才是永恒的。',
        'description': '1912年4月14日，载着1316号乘客和891名船员的豪华巨轮泰坦尼克号与冰山相撞而沉没。'
    },
    {
        'rank': 5, 'title': '千与千寻', 'year': '2001', 'score': '9.4',
        'director': '宫崎骏', 'actors': ['柊瑠美', '入野自由', '夏木真理'],
        'genre': '剧情/动画/家庭', 'country': '日本',
        'detail_url': 'https://movie.douban.com/subject/1291561/',
        'quote': '最好的宫崎骏，最好的久石让。',
        'description': '千寻和爸爸妈妈一同驱车前往新家，在郊外的小路上不慎进入了一个奇特的隧道。'
    }
]

class Logger:
    """简单的日志记录器"""
    
    def __init__(self):
        self.log_file = 'douban_movie.log'
    
    def info(self, message):
        self._log('INFO', message)
    
    def error(self, message):
        self._log('ERROR', message)
    
    def warning(self, message):
        self._log('WARNING', message)
    
    def _log(self, level, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] [{level}] {message}"
        print(log_msg)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg + '\n')
        except:
            pass

logger = Logger()

class DoubanDataFetcher:
    """豆瓣数据抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._cache = {}
    
    def get_movies(self) -> List[Dict]:
        """获取电影列表"""
        try:
            if 'movies' in self._cache:
                logger.info("从缓存获取电影数据")
                return self._cache['movies']
            
            logger.info("开始从网络获取电影数据")
            movies = self._fetch_from_network()
            
            if not movies:
                logger.warning("网络获取失败，使用备用数据")
                movies = BACKUP_MOVIES.copy()
            
            self._cache['movies'] = movies
            logger.info(f"成功获取 {len(movies)} 部电影数据")
            return movies
            
        except Exception as e:
            logger.error(f"获取电影数据失败: {e}")
            return BACKUP_MOVIES.copy()
    
    def _fetch_from_network(self) -> List[Dict]:
        """从网络获取数据"""
        movies = []
        
        for page in range(0, 250, 25):
            try:
                url = f"https://movie.douban.com/top250?start={page}"
                page_movies = self._fetch_page(url)
                
                if page_movies:
                    movies.extend(page_movies)
                    logger.info(f"成功获取第 {page//25 + 1} 页数据，共 {len(page_movies)} 部电影")
                    time.sleep(REQUEST_DELAY + random.uniform(0.5, 1.5))
                else:
                    logger.warning(f"第 {page//25 + 1} 页数据获取失败")
                    
            except Exception as e:
                logger.error(f"获取第 {page//25 + 1} 页数据时发生错误: {e}")
                continue
        
        return movies
    
    def _fetch_page(self, url: str) -> List[Dict]:
        """获取单页数据"""
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=TIMEOUT)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                movies = self._parse_movies(soup)
                
                if movies:
                    return movies
                else:
                    logger.warning(f"页面解析失败，重试 {attempt + 1}/{MAX_RETRIES}")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"网络请求失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    
            except Exception as e:
                logger.error(f"页面解析错误 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        
        return []
    
    def _parse_movies(self, soup: BeautifulSoup) -> List[Dict]:
        """解析电影数据"""
        movies = []
        
        try:
            movie_items = soup.find_all('div', class_='item')
            
            for item in movie_items:
                try:
                    movie = self._parse_movie_item(item)
                    if movie:
                        movies.append(movie)
                except Exception as e:
                    logger.error(f"解析电影条目失败: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"解析电影列表失败: {e}")
        
        return movies
    
    def _parse_movie_item(self, item) -> Dict:
        """解析单个电影条目"""
        movie = {}
        
        try:
            # 排名
            rank_elem = item.find('div', class_='pic').find('em')
            movie['rank'] = int(rank_elem.text) if rank_elem else 0
            
            # 详情链接
            link_elem = item.find('div', class_='pic').find('a')
            movie['detail_url'] = link_elem.get('href') if link_elem else ''
            
            # 信息区域
            info_elem = item.find('div', class_='info')
            if info_elem:
                # 标题
                title_elem = info_elem.find('div', class_='hd').find('a')
                if title_elem:
                    title_spans = title_elem.find_all('span', class_='title')
                    movie['title'] = title_spans[0].text if title_spans else ''
                
                # 基本信息
                bd_elem = info_elem.find('div', class_='bd')
                if bd_elem:
                    # 导演、演员等信息
                    info_text = bd_elem.find('p', class_='').text if bd_elem.find('p', class_='') else ''
                    movie.update(self._parse_movie_info(info_text))
                    
                    # 评分
                    star_elem = bd_elem.find('div', class_='star')
                    if star_elem:
                        rating_elem = star_elem.find('span', class_='rating_num')
                        movie['score'] = rating_elem.text if rating_elem else '0.0'
                    
                    # 经典台词
                    quote_elem = bd_elem.find('span', class_='inq')
                    movie['quote'] = quote_elem.text if quote_elem else ''
            
            return movie
            
        except Exception as e:
            logger.error(f"解析电影条目详情失败: {e}")
            return {}
    
    def _parse_movie_info(self, info_text: str) -> Dict:
        """解析电影基本信息"""
        info = {}
        
        try:
            lines = info_text.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('导演:'):
                    info['director'] = line.replace('导演:', '').strip()
                elif line.startswith('主演:'):
                    actors_str = line.replace('主演:', '').strip()
                    info['actors'] = [actor.strip() for actor in actors_str.split('/') if actor.strip()]
                elif re.match(r'^\d{4}', line):
                    parts = line.split('/')
                    if len(parts) >= 3:
                        info['year'] = parts[0].strip()
                        info['country'] = parts[1].strip()
                        info['genre'] = parts[2].strip()
                    elif len(parts) == 2:
                        info['year'] = parts[0].strip()
                        info['genre'] = parts[1].strip()
                    else:
                        info['year'] = parts[0].strip()
        
        except Exception as e:
            logger.error(f"解析电影信息失败: {e}")
        
        return info
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
        logger.info("缓存已清空")
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            response = self.session.get('https://movie.douban.com/top250', timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"连接测试失败: {e}")
            return False

class NetworkTester:
    """网络测试器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.test_urls = [
            'https://www.douban.com',
            'https://movie.douban.com',
            'https://www.baidu.com'
        ]
    
    def test_connection(self) -> Dict:
        """测试网络连接"""
        result = {
            'success': False,
            'message': '网络连接失败',
            'latency': 0
        }
        
        try:
            for url in self.test_urls:
                try:
                    start_time = time.time()
                    response = self.session.get(url, timeout=10)
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        result['success'] = True
                        result['message'] = '网络连接正常'
                        result['latency'] = (end_time - start_time) * 1000
                        return result
                        
                except Exception:
                    continue
            
            return result
            
        except Exception as e:
            logger.error(f"网络测试失败: {e}")
            result['message'] = f'网络测试失败: {e}'
            return result

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
        
        # 启动时加载数据
        self._startup_check()
    
    def _init_window(self):
        """初始化窗口"""
        self.root.title(WINDOW_CONFIG['title'])
        self.root.configure(bg=COLORS['bg'])
        
        # 设置窗口大小和位置
        self._center_window(WINDOW_CONFIG['width'], WINDOW_CONFIG['height'])
        self.root.minsize(WINDOW_CONFIG['min_width'], WINDOW_CONFIG['min_height'])
    
    def _center_window(self, width: int, height: int):
        """窗口居中"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
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
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=STYLES['text']['font'])
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        ttk.Button(search_frame, text="搜索", command=self._search_movies).pack(side=tk.LEFT, padx=(0, 10))
        
        # 操作按钮
        btn_frame = ttk.Frame(toolbar)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="刷新", command=self._refresh_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="网络测试", command=self._test_network).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="关于", command=self._show_about).pack(side=tk.LEFT)
    
    def _create_movie_list(self, parent):
        """创建电影列表"""
        left_frame = ttk.Frame(parent)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_frame, text="豆瓣电影Top250", font=STYLES['title']['font']).pack(anchor=tk.W, pady=(0, 10))
        
        # 列表框架
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.movie_listbox = tk.Listbox(list_frame, font=STYLES['text']['font'], selectmode=tk.SINGLE, height=20)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.movie_listbox.yview)
        self.movie_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.movie_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 分页控件
        page_frame = ttk.Frame(left_frame)
        page_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(page_frame, text="上一页", command=self._prev_page).pack(side=tk.LEFT)
        
        self.page_label = ttk.Label(page_frame, text="第 1 页")
        self.page_label.pack(side=tk.LEFT, padx=(10, 10))
        
        ttk.Button(page_frame, text="下一页", command=self._next_page).pack(side=tk.LEFT)
        ttk.Button(page_frame, text="跳转", command=self._jump_to_page).pack(side=tk.RIGHT)
    
    def _create_info_panel(self, parent):
        """创建信息面板"""
        right_frame = ttk.Frame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        ttk.Label(right_frame, text="电影信息", font=STYLES['title']['font']).pack(anchor=tk.W, pady=(0, 10))
        
        info_frame = ttk.Frame(right_frame)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, font=STYLES['text']['font'], wrap=tk.WORD, 
                                                  width=40, height=25, state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # 操作按钮
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="打开豆瓣页面", command=self._open_douban_page).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="导出信息", command=self._export_info).pack(side=tk.RIGHT)
    
    def _create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT)
        
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, length=200)
        progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
    
    def _bind_events(self):
        """绑定事件"""
        self.movie_listbox.bind('<<ListboxSelect>>', self._on_movie_select)
        self.search_var.trace('w', self._on_search_change)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _startup_check(self):
        """启动检查"""
        def check_worker():
            try:
                self._update_status("正在检查网络连接...")
                network_result = self.network_tester.test_connection()
                
                if network_result['success']:
                    self._update_status("网络连接正常，正在加载数据...")
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
            
            self.movies = self.data_fetcher.get_movies()
            self.filtered_movies = self.movies.copy()
            
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
            
            start_idx = self.current_page * self.movies_per_page
            end_idx = start_idx + self.movies_per_page
            page_movies = self.filtered_movies[start_idx:end_idx]
            
            for movie in page_movies:
                title = movie.get('title', '未知')
                year = movie.get('year', '')
                score = movie.get('score', '0.0')
                display_text = f"{movie.get('rank', 0):3d}. {title} ({year}) - {score}"
                self.movie_listbox.insert(tk.END, display_text)
            
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

豆瓣链接：
{movie.get('detail_url', '暂无')}
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
                    if (search_text in movie.get('title', '').lower() or
                        search_text in movie.get('director', '').lower() or
                        any(search_text in actor.lower() for actor in movie.get('actors', []))):
                        self.filtered_movies.append(movie)
            
            self.current_page = 0
            self._update_movie_list()
            
            self._update_status(f"搜索结果: {len(self.filtered_movies)} 部电影")
            
        except Exception as e:
            logger.error(f"搜索电影失败: {e}")
    
    def _on_search_change(self, *args):
        """搜索框变化事件"""
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
            page_str = simpledialog.askstring("跳转", "请输入页码:")
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

版本：2.0.0 - 完整版
作者：开发者

功能特点：
• 浏览豆瓣Top250电影
• 搜索和过滤功能
• 电影详情展示
• 网络状态检测
• 离线数据支持
• 分页浏览
• 信息导出

技术栈：
• Python 3.x
• tkinter (GUI)
• requests (网络请求)
• BeautifulSoup (网页解析)
• threading (多线程)

使用说明：
1. 程序启动时自动检查网络并加载数据
2. 可在搜索框中输入关键词搜索电影
3. 点击电影条目查看详细信息
4. 支持分页浏览和页面跳转
5. 可导出电影信息到文本文件

注意事项：
• 首次运行需要网络连接
• 如果网络不可用，会使用内置的备用数据
• 建议安装pillow库以获得更好的图片支持
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
    
    def _export_info(self):
        """导出电影信息"""
        try:
            selection = self.movie_listbox.curselection()
            if not selection:
                messagebox.showwarning("提示", "请先选择一部电影")
                return
            
            movie_idx = selection[0] + self.current_page * self.movies_per_page
            if movie_idx < len(self.filtered_movies):
                movie = self.filtered_movies[movie_idx]
                
                # 生成文件名
                filename = f"{movie.get('title', '未知电影')}_信息.txt"
                
                # 获取当前显示的信息
                info_content = self.info_text.get(1.0, tk.END)
                
                # 写入文件
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(info_content)
                
                messagebox.showinfo("导出成功", f"电影信息已导出到：{filename}")
                
        except Exception as e:
            logger.error(f"导出信息失败: {e}")
            messagebox.showerror("错误", f"导出失败: {e}")
    
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

def check_dependencies():
    """检查依赖项"""
    required_modules = ['tkinter', 'requests', 'bs4']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"缺少以下依赖模块: {', '.join(missing_modules)}"
        print(error_msg)
        print("请运行以下命令安装依赖:")
        print("pip install requests beautifulsoup4")
        if not PIL_AVAILABLE:
            print("pip install pillow  # 可选，用于图片支持")
        return False
    
    return True

def main():
    """主函数"""
    print("豆瓣电影Top250浏览器 v2.0.0")
    print("="*50)
    
    # 检查依赖项
    if not check_dependencies():
        input("按任意键退出...")
        return
    
    try:
        logger.info("启动豆瓣电影Top250浏览器")
        
        # 创建主窗口
        app = MainWindow()
        
        # 运行应用程序
        app.run()
        
    except KeyboardInterrupt:
        logger.info("用户中断程序")
    except Exception as e:
        error_msg = f"程序运行错误: {str(e)}"
        logger.error(error_msg)
        print(error_msg)
        
        try:
            messagebox.showerror("程序错误", error_msg)
        except:
            pass
    finally:
        logger.info("程序结束")

if __name__ == "__main__":
    main()
