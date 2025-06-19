import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import csv
import datetime
from PIL import Image, ImageTk  # 需安装 pillow 库

BOOKS_FILE = "books.txt"
READERS_FILE = "readers.txt"
HISTORY_FILE = "borrow_history.json"

# ========== 工具函数 ==========
def load_json(filename, default):
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========== 登录对话框 ==========
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

# ========== 读者管理 ==========
class ReaderManager:
    def __init__(self):
        self.readers = load_json(READERS_FILE, {'reader': {'password': 'reader123', 'role': '读者'}})

    def add_reader(self, username, password="reader123"):
        if username in self.readers:
            return False
        self.readers[username] = {'password': password, 'role': '读者'}
        self.save()
        return True

    def delete_reader(self, username):
        if username == 'reader':
            return False
        result = self.readers.pop(username, None) is not None
        if result:
            self.save()
        return result

    def get_readers(self):
        return list(self.readers.keys())

    def save(self):
        save_json(READERS_FILE, self.readers)

# ========== 借阅历史 ==========
def load_history():
    return load_json(HISTORY_FILE, {})

def save_history(data):
    save_json(HISTORY_FILE, data)

class BorrowHistory:
    def __init__(self):
        self.history = load_history()

    def add_record(self, username, isbn, action):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.setdefault(username, []).append({
            "isbn": isbn,
            "action": action,
            "time": now
        })
        save_history(self.history)

    def get_user_history(self, username):
        return self.history.get(username, [])

    def get_all_history(self):
        return self.history

# ========== 密码修改 ==========
def change_password(reader_manager, username, parent=None):
    old = simpledialog.askstring("修改密码", "请输入原密码：", show="*", parent=parent)
    if not old or reader_manager.readers[username]["password"] != old:
        messagebox.showwarning("提示", "原密码错误", parent=parent)
        return
    new = simpledialog.askstring("修改密码", "请输入新密码：", show="*", parent=parent)
    if not new:
        return
    reader_manager.readers[username]["password"] = new
    reader_manager.save()
    messagebox.showinfo("成功", "密码修改成功", parent=parent)

# ========== 图书导入导出 ==========
def export_books(books):
    with open("books_export.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "author", "isbn", "count", "category", "publisher"])
        writer.writeheader()
        for b in books:
            writer.writerow(b)

def import_books():
    filename = simpledialog.askstring("导入图书", "请输入CSV文件名：")
    if not filename or not os.path.exists(filename):
        messagebox.showwarning("提示", "文件不存在")
        return []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

# ========== 管理员查看所有借阅 ==========
def show_all_borrowed(history, parent=None):
    win = tk.Toplevel(parent)
    win.title("所有读者借阅情况")
    win.geometry("500x400")
    tree = ttk.Treeview(win, columns=("用户名", "ISBN", "操作", "时间"), show="headings")
    for col in ("用户名", "ISBN", "操作", "时间"):
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack(fill=tk.BOTH, expand=True)
    for user, records in history.get_all_history().items():
        for rec in records:
            tree.insert("", tk.END, values=(user, rec["isbn"], rec["action"], rec["time"]))

# ========== 主界面 ==========
class LibraryManager:
    def __init__(self, root, role="管理员", username="admin", reader_manager=None):
        self.root = root
        self.role = role
        self.username = username
        self.reader_manager = reader_manager
        self.books = load_json(BOOKS_FILE, [])
        self.borrowed_books = set()
        self.history = BorrowHistory()

        # 管理员界面添加背景图
        if self.role == "管理员":
            try:
                self.bg_image = Image.open("admin_bg.png")
                self.bg_photo = ImageTk.PhotoImage(self.bg_image)
                self.bg_label = tk.Label(self.root, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print("背景图加载失败：", e)

        self.root.title("图书馆管理系统")
        self.create_widgets()
        self.refresh_books()
        self.set_role_permissions()

    def save_books(self):
        save_json(BOOKS_FILE, self.books)

    def create_widgets(self):
        # 图书列表
        columns = ('书名', '作者', 'ISBN', '库存数量', '类别', '出版社')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 操作按钮（第一行）
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
            btn = tk.Button(self.btn_frame, text=text, command=cmd, width=12)
            btn.pack(side=tk.LEFT, padx=15, pady=5, expand=True)
            self.button_widgets.append(btn)

        # 角色相关按钮（第一行右侧）
        if self.role == "读者":
            borrow_btn = tk.Button(self.btn_frame, text="借书", command=self.borrow_book, width=12)
            borrow_btn.pack(side=tk.LEFT, padx=15, pady=5, expand=True)
            return_btn = tk.Button(self.btn_frame, text="还书", command=self.return_book, width=12)
            return_btn.pack(side=tk.LEFT, padx=15, pady=5, expand=True)
        elif self.role == "管理员":
            manage_btn = tk.Button(self.btn_frame, text="读者管理", command=self.manage_readers, width=12)
            manage_btn.pack(side=tk.LEFT, padx=15, pady=5, expand=True)

        # 功能按钮（第二行）
        extra_btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        extra_btn_frame.pack(pady=2, fill=tk.X)
        if self.role == "读者":
            tk.Button(extra_btn_frame, text="修改密码", command=lambda: change_password(self.reader_manager, self.username, self.root), width=12).pack(side=tk.LEFT, padx=15, pady=5, expand=True)
            tk.Button(extra_btn_frame, text="借阅历史", command=self.show_my_history, width=12).pack(side=tk.LEFT, padx=15, pady=5, expand=True)
        if self.role == "管理员":
            tk.Button(extra_btn_frame, text="导出图书", command=lambda: export_books(self.books), width=12).pack(side=tk.LEFT, padx=15, pady=5, expand=True)
            tk.Button(extra_btn_frame, text="导入图书", command=self.import_books_dialog, width=12).pack(side=tk.LEFT, padx=15, pady=5, expand=True)
            tk.Button(extra_btn_frame, text="查看借阅情况", command=lambda: show_all_borrowed(self.history, self.root), width=14).pack(side=tk.LEFT, padx=15, pady=5, expand=True)

    def set_role_permissions(self):
        if self.role == "读者":
            for btn, (text, _) in zip(self.button_widgets, self.btns):
                if text not in ("查询图书", "显示全部"):
                    btn["state"] = tk.DISABLED

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
        info['count'] = int(simpledialog.askstring("库存数量", "请输入库存数量：", initialvalue=str(book.get('count', 1) if book else "1")) or "1")
        info['category'] = simpledialog.askstring("类别", "请输入类别：", initialvalue=book.get('category', "") if book else "")
        info['publisher'] = simpledialog.askstring("出版社", "请输入出版社：", initialvalue=book.get('publisher', "") if book else "")
        return info

    def refresh_books(self, books=None):
        self.tree.delete(*self.tree.get_children())
        valid_books = [
            book for book in (books if books is not None else self.books)
            if isinstance(book, dict) and 'title' in book and 'author' in book and 'isbn' in book
        ]
        for book in valid_books:
            self.tree.insert(
                '', tk.END,
                values=(
                    book.get('title', ''),
                    book.get('author', ''),
                    book.get('isbn', ''),
                    book.get('count', ''),
                    book.get('category', ''),
                    book.get('publisher', '')
                )
            )

    def add_book(self):
        book = self.get_book_info()
        if book:
            if not any(b['isbn'] == book['isbn'] for b in self.books):
                self.books.append(book)
                self.save_books()
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
            self.save_books()
            self.refresh_books()

    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要删除的图书")
            return
        idx = self.tree.index(selected[0])
        del self.books[idx]
        self.save_books()
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

    # 读者功能
    def borrow_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择要借阅的图书")
            return
        idx = self.tree.index(selected[0])
        book = self.books[idx]
        if book.get('count', 1) <= 0:
            messagebox.showinfo("提示", "该图书已无库存")
            return
        if book['isbn'] in self.borrowed_books:
            messagebox.showinfo("提示", "您已借阅该图书")
            return
        self.borrowed_books.add(book['isbn'])
        self.books[idx]['count'] = book.get('count', 1) - 1
        self.save_books()
        self.history.add_record(self.username, book['isbn'], "借阅")
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
            for b in self.books:
                if b['isbn'] == choice:
                    b['count'] = b.get('count', 0) + 1
                    break
            self.save_books()
            self.history.add_record(self.username, choice, "归还")
            messagebox.showinfo("还书成功", f"ISBN为{choice}的图书已归还")
        else:
            messagebox.showwarning("提示", "您未借阅该ISBN的图书")

    def show_my_history(self):
        win = tk.Toplevel(self.root)
        win.title("我的借阅历史")
        win.geometry("500x400")
        tree = ttk.Treeview(win, columns=("ISBN", "操作", "时间"), show="headings")
        for col in ("ISBN", "操作", "时间"):
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        tree.pack(fill=tk.BOTH, expand=True)
        for rec in self.history.get_user_history(self.username):
            tree.insert("", tk.END, values=(rec["isbn"], rec["action"], rec["time"]))

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

    def import_books_dialog(self):
        imported = import_books()
        if imported:
            for b in imported:
                if not any(book['isbn'] == b['isbn'] for book in self.books):
                    book = {
                        "title": b.get("title", ""),
                        "author": b.get("author", ""),
                        "isbn": b.get("isbn", ""),
                        "count": int(b.get("count", 1)),
                        "category": b.get("category", ""),
                        "publisher": b.get("publisher", ""),
                    }
                    self.books.append(book)
            self.save_books()
            self.refresh_books()
            messagebox.showinfo("导入成功", f"成功导入{len(imported)}本图书")

# ========== 程序入口 ==========
def main():
    root = tk.Tk()
    root.withdraw()
    reader_manager = ReaderManager()
    users = {
        "admin": {"password": "admin123", "role": "管理员"},
    }
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
