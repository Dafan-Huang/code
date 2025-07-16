import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
import threading
import webbrowser

PAGE_SIZE = 25

def fetch_douban_top250():
    """
    获取豆瓣电影Top250列表。

    Returns:
        list[dict]: 每部电影为一个字典，包含详细信息。
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    movies = []
    for start in range(0, 250, 25):
        url = f'https://movie.douban.com/top250?start={start}'
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.find_all('div', class_='item')
            
            for item in items:
                title_tag = item.find('span', class_='title')
                rating_tag = item.find('span', class_='rating_num')
                img_tag = item.find('img')
                
                # 获取电影详情页链接
                detail_link = item.find('a')
                detail_url = detail_link['href'] if detail_link else ''
                
                # 获取电影基本信息
                info_tag = item.find('p', class_='')
                info = info_tag.text.strip() if info_tag else ''
                
                # 获取电影简介/评语
                quote_tag = item.find('span', class_='inq')
                quote = quote_tag.text.strip() if quote_tag else ''
                
                # 获取评分人数
                rating_people_tag = item.find('div', class_='star').find_all('span')
                rating_people = rating_people_tag[3].text if len(rating_people_tag) > 3 else ''
                
                if title_tag and rating_tag and img_tag:
                    title = title_tag.text.strip()
                    rating = rating_tag.text.strip()
                    img_url = img_tag['src']
                    movies.append({
                        'title': title, 
                        'rating': rating, 
                        'img_url': img_url,
                        'detail_url': detail_url,
                        'info': info,
                        'quote': quote,
                        'rating_people': rating_people
                    })
        except Exception as e:
            print(f"获取第{start}页数据失败: {e}")
            continue
    return movies

class MovieDetailWindow:
    def __init__(self, parent, movie_data):
        self.parent = parent
        self.movie_data = movie_data
        self.detail_window = None
        self.create_detail_window()
        
    def create_detail_window(self):
        """创建电影详情窗口"""
        self.detail_window = tk.Toplevel(self.parent.root)
        self.detail_window.title(f"电影详情 - {self.movie_data['title']}")
        self.detail_window.geometry("800x600")
        self.detail_window.resizable(True, True)
        
        # 居中显示
        self.center_window()
        
        # 设置窗口属性
        self.detail_window.configure(bg='#f8f9fa')
        self.detail_window.transient(self.parent.root)
        self.detail_window.grab_set()
        
        # 创建界面
        self.create_interface()
        
    def center_window(self):
        """窗口居中显示"""
        self.detail_window.update_idletasks()
        width = 800
        height = 600
        x = (self.detail_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.detail_window.winfo_screenheight() // 2) - (height // 2)
        self.detail_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """创建详情界面"""
        # 创建主框架
        main_frame = tk.Frame(self.detail_window, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题栏
        title_frame = tk.Frame(main_frame, bg='#f8f9fa')
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame, text=self.movie_data['title'], 
                              font=('微软雅黑', 18, 'bold'), 
                              bg='#f8f9fa', fg='#2c3e50')
        title_label.pack(side='left')
        
        # 评分标签
        rating_label = tk.Label(title_frame, text=f"★ {self.movie_data['rating']}", 
                               font=('微软雅黑', 14, 'bold'), 
                               bg='#f8f9fa', fg='#f39c12')
        rating_label.pack(side='right')
        
        # 内容区域
        content_frame = tk.Frame(main_frame, bg='#f8f9fa')
        content_frame.pack(fill='both', expand=True)
        
        # 左侧海报区域
        left_frame = tk.Frame(content_frame, bg='#f8f9fa')
        left_frame.pack(side='left', fill='y', padx=(0, 20))
        
        # 海报
        self.poster_label = tk.Label(left_frame, text="加载中...", 
                                    font=('微软雅黑', 12), 
                                    bg='#ffffff', 
                                    width=20, height=15,
                                    relief='solid', bd=1)
        self.poster_label.pack(pady=(0, 10))
        
        # 右侧信息区域
        right_frame = tk.Frame(content_frame, bg='#f8f9fa')
        right_frame.pack(side='left', fill='both', expand=True)
        
        # 基本信息
        info_frame = tk.LabelFrame(right_frame, text="基本信息", 
                                  font=('微软雅黑', 12, 'bold'), 
                                  bg='#f8f9fa', fg='#2c3e50')
        info_frame.pack(fill='x', pady=(0, 15))
        
        # 显示基本信息
        basic_info = self.movie_data.get('info', '暂无信息')
        info_text = tk.Text(info_frame, height=4, wrap='word', 
                           font=('微软雅黑', 10), 
                           bg='#ffffff', relief='flat')
        info_text.pack(fill='x', padx=10, pady=10)
        info_text.insert('1.0', basic_info)
        info_text.config(state='disabled')
        
        # 评分信息
        rating_frame = tk.LabelFrame(right_frame, text="评分信息", 
                                   font=('微软雅黑', 12, 'bold'), 
                                   bg='#f8f9fa', fg='#2c3e50')
        rating_frame.pack(fill='x', pady=(0, 15))
        
        rating_info = f"豆瓣评分: {self.movie_data['rating']}\n评分人数: {self.movie_data.get('rating_people', '暂无')}"
        rating_info_label = tk.Label(rating_frame, text=rating_info, 
                                   font=('微软雅黑', 10), 
                                   bg='#f8f9fa', justify='left')
        rating_info_label.pack(anchor='w', padx=10, pady=10)
        
        # 电影简介
        quote_frame = tk.LabelFrame(right_frame, text="电影简介", 
                                   font=('微软雅黑', 12, 'bold'), 
                                   bg='#f8f9fa', fg='#2c3e50')
        quote_frame.pack(fill='x', pady=(0, 15))
        
        quote_text = self.movie_data.get('quote', '暂无简介')
        quote_label = tk.Label(quote_frame, text=quote_text, 
                              font=('微软雅黑', 10), 
                              bg='#f8f9fa', wraplength=400, justify='left')
        quote_label.pack(anchor='w', padx=10, pady=10)
        
        # 详细信息区域
        detail_frame = tk.LabelFrame(right_frame, text="详细信息", 
                                    font=('微软雅黑', 12, 'bold'), 
                                    bg='#f8f9fa', fg='#2c3e50')
        detail_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        self.detail_text = tk.Text(detail_frame, height=8, wrap='word', 
                                  font=('微软雅黑', 10), 
                                  bg='#ffffff', relief='flat')
        detail_scroll = ttk.Scrollbar(detail_frame, orient="vertical", command=self.detail_text.yview)
        self.detail_text.configure(yscrollcommand=detail_scroll.set)
        
        self.detail_text.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        detail_scroll.pack(side='right', fill='y', pady=10)
        
        self.detail_text.insert('1.0', "正在加载详细信息...")
        self.detail_text.config(state='disabled')
        
        # 按钮区域
        button_frame = tk.Frame(main_frame, bg='#f8f9fa')
        button_frame.pack(fill='x', pady=(20, 0))
        
        # 打开豆瓣页面按钮
        open_douban_btn = tk.Button(button_frame, text="打开豆瓣页面", 
                                   font=('微软雅黑', 10), 
                                   bg='#3498db', fg='white',
                                   command=self.open_douban_page)
        open_douban_btn.pack(side='left', padx=(0, 10))
        
        # 关闭按钮
        close_btn = tk.Button(button_frame, text="关闭", 
                             font=('微软雅黑', 10), 
                             bg='#95a5a6', fg='white',
                             command=self.close_window)
        close_btn.pack(side='right')
        
        # 异步加载海报和详细信息
        self.load_poster()
        self.load_detailed_info()
    
    def load_poster(self):
        """异步加载海报"""
        def load_image():
            try:
                if self.movie_data['img_url']:
                    resp = requests.get(self.movie_data['img_url'], timeout=10)
                    resp.raise_for_status()
                    image = Image.open(io.BytesIO(resp.content))
                    image = image.resize((200, 280), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    # 更新UI必须在主线程
                    self.detail_window.after(0, lambda: self.update_poster(photo))
                else:
                    self.detail_window.after(0, lambda: self.poster_label.config(text="无海报"))
            except Exception as e:
                self.detail_window.after(0, lambda: self.poster_label.config(text=f"海报加载失败"))
        
        threading.Thread(target=load_image, daemon=True).start()
    
    def update_poster(self, photo):
        """更新海报显示"""
        self.poster_label.config(image=photo, text="")
        self.poster_label.image = photo  # 保持引用
    
    def load_detailed_info(self):
        """异步加载详细信息"""
        def fetch_details():
            try:
                if not self.movie_data.get('detail_url'):
                    self.detail_window.after(0, lambda: self.update_detail_info("暂无详细信息链接"))
                    return
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                resp = requests.get(self.movie_data['detail_url'], headers=headers, timeout=15)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                # 获取详细信息
                details = []
                
                # 导演信息
                info_span = soup.find('span', text='导演')
                if info_span:
                    directors = info_span.find_next_sibling('span', class_='attrs')
                    if directors:
                        details.append(f"导演: {directors.get_text().strip()}")
                
                # 主演信息
                info_span = soup.find('span', text='主演')
                if info_span:
                    actors = info_span.find_next_sibling('span', class_='attrs')
                    if actors:
                        details.append(f"主演: {actors.get_text().strip()}")
                
                # 类型
                info_span = soup.find('span', text='类型:')
                if info_span:
                    genre = info_span.find_next_sibling('span', class_='attrs')
                    if genre:
                        details.append(f"类型: {genre.get_text().strip()}")
                
                # 制片国家/地区
                info_span = soup.find('span', text='制片国家/地区:')
                if info_span:
                    country = info_span.next_sibling
                    if country:
                        details.append(f"制片国家/地区: {country.strip()}")
                
                # 上映日期
                info_span = soup.find('span', text='上映日期:')
                if info_span:
                    date = info_span.find_next_sibling('span', class_='attrs')
                    if date:
                        details.append(f"上映日期: {date.get_text().strip()}")
                
                # 片长
                info_span = soup.find('span', text='片长:')
                if info_span:
                    duration = info_span.next_sibling
                    if duration:
                        details.append(f"片长: {duration.strip()}")
                
                # 剧情简介
                summary_div = soup.find('div', id='link-report')
                if summary_div:
                    summary_span = summary_div.find('span', class_='all')
                    if not summary_span:
                        summary_span = summary_div.find('span', property='v:summary')
                    if summary_span:
                        details.append(f"\\n剧情简介:\\n{summary_span.get_text().strip()}")
                
                detail_text = '\\n'.join(details) if details else "暂无详细信息"
                self.detail_window.after(0, lambda: self.update_detail_info(detail_text))
                
            except Exception as e:
                error_msg = f"加载详细信息失败: {str(e)}"
                self.detail_window.after(0, lambda: self.update_detail_info(error_msg))
        
        threading.Thread(target=fetch_details, daemon=True).start()
    
    def update_detail_info(self, info_text):
        """更新详细信息显示"""
        self.detail_text.config(state='normal')
        self.detail_text.delete('1.0', 'end')
        self.detail_text.insert('1.0', info_text)
        self.detail_text.config(state='disabled')
    
    def open_douban_page(self):
        """打开豆瓣页面"""
        if self.movie_data.get('detail_url'):
            webbrowser.open(self.movie_data['detail_url'])
        else:
            messagebox.showwarning("警告", "无法获取豆瓣页面链接")
    
    def close_window(self):
        """关闭详情窗口"""
        if self.detail_window:
            self.detail_window.destroy()


class DoubanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("豆瓣电影Top250")
        
        # 获取屏幕尺寸并设置适合的窗口大小
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # 设置窗口大小为屏幕的80%，但不小于最小尺寸
        window_width = min(max(int(screen_width * 0.8), 900), 1400)
        window_height = min(max(int(screen_height * 0.8), 650), 900)
        
        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#f5f5f5')
        self.root.minsize(900, 650)  # 设置最小窗口大小
        self.movies = []
        self.current_page = 0
        self.img_popup = None
        self.img_cache = {}
        self.seen_dict = {}  # 记录看过状态
        self.filter_seen = False

        # 优化样式配置
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', 
                       font=('微软雅黑', 11), 
                       rowheight=35,  # 增加行高
                       background='#ffffff', 
                       fieldbackground='#ffffff',
                       selectbackground='#e3f2fd')
        style.configure('Treeview.Heading', 
                       font=('微软雅黑', 12, 'bold'), 
                       background='#e0e0e0',
                       foreground='#333333')
        style.configure('TButton', font=('微软雅黑', 11), padding=(10, 5))
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('微软雅黑', 11))

        # 创建主框架
        frame = ttk.Frame(self.root, padding=15)
        frame.pack(fill='both', expand=True)
        
        # 创建表格框架
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill='both', expand=True, pady=(0, 10))

        columns = ('序号', '电影名', '评分', '看过')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=18)
        for col in columns:
            self.tree.heading(col, text=col)
            if col == '电影名':
                self.tree.column(col, width=int(window_width * 0.5), anchor='w')  # 左对齐，动态宽度
            elif col == '看过':
                self.tree.column(col, width=80, anchor='center')
            elif col == '序号':
                self.tree.column(col, width=80, anchor='center')
            else:  # 评分
                self.tree.column(col, width=100, anchor='center')
        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # 按钮框架
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        self.btn_fetch = ttk.Button(btn_frame, text="获取豆瓣Top250", command=self.show_movies)
        self.btn_fetch.grid(row=0, column=0, padx=5)

        self.btn_prev = ttk.Button(btn_frame, text="上一页", command=self.prev_page, state='disabled')
        self.btn_prev.grid(row=0, column=1, padx=5)

        self.page_label = ttk.Label(btn_frame, text="第 0 / 0 页", font=('微软雅黑', 12))
        self.page_label.grid(row=0, column=2, padx=5)

        self.btn_next = ttk.Button(btn_frame, text="下一页", command=self.next_page, state='disabled')
        self.btn_next.grid(row=0, column=3, padx=5)

        self.btn_filter = ttk.Button(btn_frame, text="只看已看过", command=self.toggle_filter)
        self.btn_filter.grid(row=0, column=4, padx=5)

        self.tree.bind('<Motion>', self.on_tree_motion)
        self.tree.bind('<Leave>', self.on_tree_leave)
        self.tree.bind('<Button-1>', self.on_tree_click)
        self.tree.bind('<Double-1>', self.on_tree_double_click)  # 双击事件

        # 复选框图片
        self.checked_img = ImageTk.PhotoImage(Image.new('RGB', (20, 20), (0, 200, 0)))
        self.unchecked_img = ImageTk.PhotoImage(Image.new('RGB', (20, 20), (220, 220, 220)))

        # 绑定窗口大小调整事件
        self.root.bind('<Configure>', self.on_window_resize)
        
        # 存储窗口尺寸用于动态调整
        self.window_width = window_width
        self.window_height = window_height

    def show_movies(self):
        def task():
            self.btn_fetch.config(state='disabled')
            self.btn_prev.config(state='disabled')
            self.btn_next.config(state='disabled')
            self.tree.delete(*self.tree.get_children())
            self.page_label.config(text="加载中...")
            try:
                self.movies = fetch_douban_top250()
                self.seen_dict = {m['img_url']: False for m in self.movies}
                self.current_page = 0
                self.update_page()
            except Exception as e:
                messagebox.showerror("错误", f"获取数据失败: {e}")
                self.page_label.config(text="第 0 / 0 页")
            finally:
                self.btn_fetch.config(state='normal')
        threading.Thread(target=task, daemon=True).start()

    def get_display_movies(self):
        if self.filter_seen:
            return [m for m in self.movies if self.seen_dict.get(m['img_url'], False)]
        return self.movies

    def update_page(self):
        self.tree.delete(*self.tree.get_children())
        display_movies = self.get_display_movies()
        total_pages = (len(display_movies) + PAGE_SIZE - 1) // PAGE_SIZE
        if total_pages == 0:
            self.page_label.config(text="第 0 / 0 页")
            self.btn_prev.config(state='disabled')
            self.btn_next.config(state='disabled')
            return
        start = self.current_page * PAGE_SIZE
        end = start + PAGE_SIZE
        page_movies = display_movies[start:end]
        for idx, movie in enumerate(page_movies, start + 1):
            seen = self.seen_dict.get(movie['img_url'], False)
            check = "√" if seen else ""
            self.tree.insert('', 'end', values=(idx, movie['title'], movie['rating'], check))
        self.page_label.config(text=f"第 {self.current_page + 1} / {total_pages} 页")
        self.btn_prev.config(state='normal' if self.current_page > 0 else 'disabled')
        self.btn_next.config(state='normal' if self.current_page < total_pages - 1 else 'disabled')

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def next_page(self):
        display_movies = self.get_display_movies()
        total_pages = (len(display_movies) + PAGE_SIZE - 1) // PAGE_SIZE
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_page()

    def toggle_filter(self):
        self.filter_seen = not self.filter_seen
        self.btn_filter.config(text="显示全部" if self.filter_seen else "只看已看过")
        self.current_page = 0
        self.update_page()

    def on_tree_click(self, event):
        region = self.tree.identify('region', event.x, event.y)
        if region != 'cell':
            return
        col = self.tree.identify_column(event.x)
        if col != '#4':  # "看过"列
            return
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
        title = self.tree.item(row_id, 'values')[1]
        movie = next((m for m in self.movies if m['title'] == title), None)
        if movie:
            img_url = movie['img_url']
            self.seen_dict[img_url] = not self.seen_dict.get(img_url, False)
            self.update_page()

    def on_tree_double_click(self, event):
        """双击事件处理 - 打开电影详情"""
        region = self.tree.identify('region', event.x, event.y)
        if region != 'cell':
            return
        
        col = self.tree.identify_column(event.x)
        if col == '#4':  # "看过"列不打开详情
            return
            
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
            
        title = self.tree.item(row_id, 'values')[1]
        movie = next((m for m in self.movies if m['title'] == title), None)
        if movie:
            MovieDetailWindow(self, movie)

    def on_tree_motion(self, event):
        region = self.tree.identify('region', event.x, event.y)
        if region != 'cell':
            self.hide_img_popup()
            return
        col = self.tree.identify_column(event.x)
        if col == '#4':  # "看过"列不弹窗
            self.hide_img_popup()
            return
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            self.hide_img_popup()
            return
        title = self.tree.item(row_id, 'values')[1]
        movie = next((m for m in self.movies if m['title'] == title), None)
        if not movie:
            self.hide_img_popup()
            return
        img_url = movie.get('img_url')
        if not img_url:
            self.hide_img_popup()
            return
        if getattr(self, '_last_row_id', None) == row_id:
            return
        self._last_row_id = row_id
        
        # 添加延迟显示，避免快速移动时频繁弹窗
        self.cancel_pending_popup()
        self._popup_timer = self.root.after(300, lambda: self.show_img_popup(img_url, event))

    def cancel_pending_popup(self):
        """取消待执行的弹窗"""
        if hasattr(self, '_popup_timer') and self._popup_timer:
            self.root.after_cancel(self._popup_timer)
            self._popup_timer = None

    def on_tree_leave(self, _):
        self.cancel_pending_popup()
        self.hide_img_popup()
        self._last_row_id = None

    def show_img_popup(self, img_url, event):
        # 节流：只有图片url变化时才启动新线程
        if getattr(self, '_last_img_url', None) == img_url:
            return
        self._last_img_url = img_url

        def fetch_and_show():
            if img_url in self.img_cache:
                img = self.img_cache[img_url]
            else:
                try:
                    resp = requests.get(img_url, timeout=10)
                    resp.raise_for_status()
                    image = Image.open(io.BytesIO(resp.content))
                    # 保持比例缩放，增大显示尺寸
                    image = image.resize((150, 220), Image.Resampling.LANCZOS)
                    img = ImageTk.PhotoImage(image)
                    self.img_cache[img_url] = img
                except Exception as e:
                    print(f"图片加载异常: {e}")
                    return
            
            if self.img_popup:
                self.img_popup.destroy()
            
            self.img_popup = tk.Toplevel(self.root)
            self.img_popup.overrideredirect(True)
            self.img_popup.attributes('-topmost', True)
            
            # 优化海报显示位置逻辑
            # 获取当前鼠标相对于主窗口的位置
            mouse_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
            mouse_y = self.root.winfo_pointery() - self.root.winfo_rooty()
            
            # 获取窗口和屏幕尺寸
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # 海报尺寸
            popup_width = 150
            popup_height = 220
            
            # 计算最佳显示位置
            # 默认显示在鼠标右侧
            x = self.root.winfo_rootx() + mouse_x + 20
            y = self.root.winfo_rooty() + mouse_y - popup_height // 2
            
            # 如果右侧空间不足，显示在左侧
            if x + popup_width > screen_width:
                x = self.root.winfo_rootx() + mouse_x - popup_width - 20
            
            # 如果左侧空间也不足，显示在窗口内右侧
            if x < 0:
                x = self.root.winfo_rootx() + window_width - popup_width - 20
            
            # 垂直位置调整
            if y < 0:
                y = 10
            elif y + popup_height > screen_height:
                y = screen_height - popup_height - 10
            
            self.img_popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
            
            # 添加边框和阴影效果
            self.img_popup.configure(bg='#333333')
            label = tk.Label(self.img_popup, image=img, bg='#333333', bd=2, relief='solid')
            label.image = img
            label.pack(padx=2, pady=2)
            
        threading.Thread(target=fetch_and_show, daemon=True).start()

    def hide_img_popup(self):
        if self.img_popup:
            self.img_popup.destroy()
            self.img_popup = None
        self._last_img_url = None

    def on_window_resize(self, event):
        """窗口大小调整时的回调函数"""
        if event.widget == self.root:
            # 获取新的窗口大小
            new_width = self.root.winfo_width()
            new_height = self.root.winfo_height()
            
            # 更新电影名列宽度
            if hasattr(self, 'tree') and self.tree:
                self.tree.column('电影名', width=int(new_width * 0.5))
            
            self.window_width = new_width
            self.window_height = new_height

if __name__ == '__main__':
    root = tk.Tk()
    app = DoubanApp(root)
    root.mainloop()
