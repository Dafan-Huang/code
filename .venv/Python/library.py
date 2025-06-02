import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class LoginDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="用户名:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(master, text="密码:").grid(row=1, column=0, sticky=tk.W)
        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show="*")
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        return self.username_entry

    def apply(self):
        self.result = {
            "username": self.username_entry.get(),
            "password": self.password_entry.get()
        }

def login(users):
    while True:
        dlg = LoginDialog(None, title="登录")
        if dlg.result is None:
            return None, None
        username = dlg.result["username"]
        password = dlg.result["password"]
        user = users.get(username)
        if user and user["password"] == password:
            return username, user["role"]
        else:
            messagebox.showerror("登录失败", "用户名或密码错误，请重试。")

class ReaderManager:
    def __init__(self):
        self.readers = {'reader': {'password': 'reader123', 'role': '读者'}}

    def add_reader(self, username, password="reader123"):
        if username in self.readers:
            return False
        self.readers[username] = {'password': password, 'role': '读者'}
        return True

    def delete_reader(self, username):
        if username == 'reader':
            return False
        return self.readers.pop(username, None) is not None

    def get_readers(self):
        return list(self.readers.keys())

class LibraryManager:
    def __init__(self, root, role="管理员", username="admin", reader_manager=None):
        self.root = root
        self.role = role
        self.username = username
        self.reader_manager = reader_manager
        self.root.title("图书馆管理系统")
        self.books = []
        self.borrowed_books = set()
        self.create_widgets()
        self.refresh_books()
        self.set_role_permissions()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=('书名', '作者', 'ISBN'), show='headings', height=15)
        for col in ('书名', '作者', 'ISBN'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.btn_frame.pack(pady=5, fill=tk.X)

        self.button_widgets = []
        self.btns = [
            ("添加图书", self.add_book),
            ("修改图书", self.edit_book),
            ("删除图书", self.delete_book),
            ("查询图书", self.search_book),
            ("显示全部", self.refresh_books)
        ]
        for text, cmd in self.btns:
            btn = tk.Button(self.btn_frame, text=text, command=cmd, width=10)
            btn.pack(side=tk.LEFT, padx=5)
            self.button_widgets.append(btn)

        if self.role == "读者":
            borrow_btn = tk.Button(self.btn_frame, text="借书", command=self.borrow_book, width=10)
            borrow_btn.pack(side=tk.LEFT, padx=5)
            return_btn = tk.Button(self.btn_frame, text="还书", command=self.return_book, width=10)
            return_btn.pack(side=tk.LEFT, padx=5)
        elif self.role == "管理员":
            manage_btn = tk.Button(self.btn_frame, text="读者管理", command=self.manage_readers, width=10)
            manage_btn.pack(side=tk.LEFT, padx=5)

    def set_role_permissions(self):
        if self.role == "读者":
            for btn, (text, _) in zip(self.button_widgets, self.btns):
                if text not in ("查询图书", "显示全部"):
                    btn["state"] = tk.DISABLED

    def add_book(self):
        book = self.get_book_info()
        if book:
            if not any(b['isbn'] == book['isbn'] for b in self.books):
                self.books.append(book)
                self.refresh_books()
            else:
                messagebox.showwarning("提示", "该图书已存在")

    def edit_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要修改的图书")
            return
        idx = self.tree.index(selected[0])
        book = self.books[idx]
        new_book = self.get_book_info(book)
        if new_book:
            self.books[idx] = new_book
            self.refresh_books()

    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要删除的图书")
            return
        idx = self.tree.index(selected[0])
        del self.books[idx]
        self.refresh_books()

    def search_book(self):
        keyword = simpledialog.askstring("查询图书", "请输入书名/作者/ISBN关键词：")
        if keyword:
            keyword = keyword.strip()
            results = [
                b for b in self.books
                if keyword.lower() in b['title'].lower()
                or keyword.lower() in b['author'].lower()
                or keyword.lower() in b['isbn'].lower()
            ]
            self.refresh_books(results)

    def refresh_books(self, books=None):
        self.tree.delete(*self.tree.get_children())
        valid_books = [
            book for book in (books if books is not None else self.books)
            if isinstance(book, dict) and 'title' in book and 'author' in book and 'isbn' in book
        ]
        for book in valid_books:
            self.tree.insert('', tk.END, values=(book['title'], book['author'], book['isbn']))

    def get_book_info(self, book=None):
        info = {}
        info['title'] = simpledialog.askstring("书名", "请输入书名：", initialvalue=book['title'] if book else "")
        if not info['title']:
            return None
        info['author'] = simpledialog.askstring("作者", "请输入作者：", initialvalue=book['author'] if book else "")
        if not info['author']:
            return None
        info['isbn'] = simpledialog.askstring("ISBN", "请输入ISBN：", initialvalue=book['isbn'] if book else "")
        if not info['isbn']:
            return None
        return info

    # 读者功能
    def borrow_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要借阅的图书")
            return
        idx = self.tree.index(selected[0])
        book = self.books[idx]
        if book['isbn'] in self.borrowed_books:
            messagebox.showinfo("提示", "您已借阅该图书")
            return
        self.borrowed_books.add(book['isbn'])
        messagebox.showinfo("借书成功", f"您已借阅《{book['title']}》")

    def return_book(self):
        if not self.borrowed_books:
            messagebox.showinfo("提示", "您没有借阅任何图书")
            return
        borrowed = [b for b in self.books if b['isbn'] in self.borrowed_books]
        if not borrowed:
            messagebox.showinfo("提示", "您没有借阅任何图书")
            return
        titles = [f"{b['title']} (ISBN:{b['isbn']})" for b in borrowed]
        choice = simpledialog.askstring("还书", "请输入要归还的图书ISBN：\n" + "\n".join(titles))
        if not choice:
            return
        choice = choice.strip()
        if choice in self.borrowed_books:
            self.borrowed_books.remove(choice)
            messagebox.showinfo("还书成功", f"ISBN为{choice}的图书已归还")
        else:
            messagebox.showwarning("提示", "您未借阅该ISBN的图书")

    # 管理员功能
    def manage_readers(self):
        reader_win = tk.Toplevel(self.root)
        reader_win.title("读者管理")
        reader_win.geometry("400x300")
        reader_win.transient(self.root)

        columns = ('用户名',)
        tree = ttk.Treeview(reader_win, columns=columns, show='headings', height=10)
        tree.heading('用户名', text='用户名')
        tree.column('用户名', width=200, anchor='center')
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def refresh_readers():
            tree.delete(*tree.get_children())
            for r in self.reader_manager.get_readers():
                tree.insert('', tk.END, values=(r,))

        def add_reader():
            username = simpledialog.askstring("添加读者", "请输入新读者用户名：", parent=reader_win)
            if not username:
                return
            username = username.strip()
            if not self.reader_manager.add_reader(username):
                messagebox.showwarning("提示", "该读者已存在", parent=reader_win)
                return
            refresh_readers()
            messagebox.showinfo("成功", f"已添加读者：{username}", parent=reader_win)

        def delete_reader():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("提示", "请选择要删除的读者", parent=reader_win)
                return
            idx = tree.index(selected[0])
            username = self.reader_manager.get_readers()[idx]
            if username == 'reader':
                messagebox.showwarning("提示", "默认读者不能删除", parent=reader_win)
                return
            if messagebox.askyesno("确认", f"确定要删除读者 {username} 吗？", parent=reader_win):
                self.reader_manager.delete_reader(username)
                refresh_readers()

        btn_frame = tk.Frame(reader_win)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="添加读者", command=add_reader, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="删除读者", command=delete_reader, width=10).pack(side=tk.LEFT, padx=5)

        refresh_readers()

def main():
    root = tk.Tk()
    root.withdraw()
    reader_manager = ReaderManager()
    # 管理员账号
    users = {
        "admin": {"password": "admin123", "role": "管理员"},
    }
    # 加入所有读者账号
    users.update(reader_manager.readers)
    username, role = login(users)
    if username is None:
        root.destroy()
        return
    root.deiconify()
    app = LibraryManager(root, role, username, reader_manager)
    root.title(f"图书馆管理系统 - {role}({username})")
    root.mainloop()

if __name__ == "__main__":
    main()
