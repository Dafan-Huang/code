import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import os

class LibraryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("图书馆管理系统")
        self.books = []  # 存储图书信息的列表

        self.create_widgets()
        self.refresh_books()

    def create_widgets(self):
        # 图书列表
        self.tree = ttk.Treeview(self.root, columns=('书名', '作者', 'ISBN'), show='headings', height=15)
        for col in ('书名', '作者', 'ISBN'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(pady=5, fill=tk.X)

        btns = [
            ("添加图书", self.add_book),
            ("修改图书", self.edit_book),
            ("删除图书", self.delete_book),
            ("查询图书", self.search_book),
            ("显示全部", self.refresh_books)
        ]
        for text, cmd in btns:
            tk.Button(btn_frame, text=text, command=cmd, width=10).pack(side=tk.LEFT, padx=5)

    def add_book(self):
        book = self.get_book_info()
        if book:
            self.books.append(book)
            self.refresh_books()

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
        for book in books if books is not None else self.books:
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

def set_background(root, image_path):
    if not os.path.exists(image_path):
        return None, None
    bg_image = Image.open(image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo  # 保持引用
    bg_label.lower()
    return bg_label, bg_image

def main():
    root = tk.Tk()
    root.update_idletasks()  # 确保窗口尺寸已初始化

    # 设置背景图片
    bg_path = os.path.join(os.path.dirname(__file__), "background.jpg")
    bg_label, bg_image = set_background(root, bg_path)

    app = LibraryManager(root)

    if bg_label and bg_image:
        app.tree.lift()
        # Store the original image as an attribute of the label for resizing
        bg_label.original_image = bg_image
        def resize_bg(event):
            new_width, new_height = event.width, event.height
            # Always use the original image for resizing
            resized = bg_label.original_image.resize((max(1, new_width), max(1, new_height)), Image.LANCZOS)
            bg_photo2 = ImageTk.PhotoImage(resized)
            bg_label.config(image=bg_photo2)
            bg_label.image = bg_photo2  # 保持引用
        root.bind("<Configure>", resize_bg)

    root.mainloop()

if __name__ == "__main__":
    main()