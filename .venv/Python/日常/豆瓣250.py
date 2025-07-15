# ...（省略前面代码）

class DoubanApp:
    def __init__(self, root):
        # ...（省略原有初始化代码）

        self.filter_mode = 'all'  # 可为 'all', 'seen', 'unseen'

        # 按钮区
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.btn_fetch = ttk.Button(btn_frame, text="获取豆瓣Top250", command=self.show_movies)
        self.btn_fetch.grid(row=0, column=0, padx=5)

        self.btn_prev = ttk.Button(btn_frame, text="上一页", command=self.prev_page, state='disabled')
        self.btn_prev.grid(row=0, column=1, padx=5)

        self.page_label = ttk.Label(btn_frame, text="第 0 / 0 页", font=('微软雅黑', 12))
        self.page_label.grid(row=0, column=2, padx=5)

        self.btn_next = ttk.Button(btn_frame, text="下一页", command=self.next_page, state='disabled')
        self.btn_next.grid(row=0, column=3, padx=5)

        # 新增筛选按钮
        self.btn_all = ttk.Button(btn_frame, text="显示全部", command=lambda: self.set_filter('all'))
        self.btn_all.grid(row=0, column=4, padx=5)
        self.btn_seen = ttk.Button(btn_frame, text="只看看过", command=lambda: self.set_filter('seen'))
        self.btn_seen.grid(row=0, column=5, padx=5)
        self.btn_unseen = ttk.Button(btn_frame, text="只看没看过", command=lambda: self.set_filter('unseen'))
        self.btn_unseen.grid(row=0, column=6, padx=5)

        # ...（省略其余初始化代码）

    def set_filter(self, mode):
        self.filter_mode = mode
        self.current_page = 0
        self.update_page()

    def get_display_movies(self):
        if self.filter_mode == 'seen':
            return [m for m in self.movies if self.seen_dict.get(m['title'], False)]
        elif self.filter_mode == 'unseen':
            return [m for m in self.movies if not self.seen_dict.get(m['title'], False)]
        return self.movies

    # 优化海报弹窗性能
    def on_tree_motion(self, event):
        region = self.tree.identify('region', event.x, event.y)
        if region != 'cell':
            self.hide_img_popup()
            return
        col = self.tree.identify_column(event.x)
        if col == '#4':
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
        self.show_img_popup(img_url, event)

    def show_img_popup(self, img_url, event):
        def fetch_and_show():
            if img_url in self.img_cache:
                img = self.img_cache[img_url]
            else:
                try:
                    resp = requests.get(img_url, timeout=10)
                    resp.raise_for_status()
                    image = Image.open(io.BytesIO(resp.content))
                    image = image.resize((120, 180))
                    img = ImageTk.PhotoImage(image)
                    self.img_cache[img_url] = img
                except Exception:
                    return
            # 只在主线程更新UI
            self.root.after(0, lambda: self._show_img_popup(img, event))
        threading.Thread(target=fetch_and_show, daemon=True).start()

    def _show_img_popup(self, img, event):
        if self.img_popup:
            self.img_popup.destroy()
        self.img_popup = tk.Toplevel(self.root)
        self.img_popup.overrideredirect(True)
        self.img_popup.attributes('-topmost', True)
        x = self.root.winfo_pointerx() + 20
        y = self.root.winfo_pointery() + 20
        self.img_popup.geometry(f"+{x}+{y}")
        label = tk.Label(self.img_popup, image=img)
        label.image = img
        label.pack()

    def hide_img_popup(self):
        if self.img_popup:
            self.img_popup.destroy()
            self.img_popup = None
        self._last_row_id = None

# ...（其余代码不变）
