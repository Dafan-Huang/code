import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            show_data(df)
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件:\n{e}")

def show_data(df):
    for widget in frame.winfo_children():
        widget.destroy()
    cols = list(df.columns)
    tree = ttk.Treeview(frame, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for _, row in df.head(5).iterrows():
        tree.insert("", "end", values=list(row))
    tree.pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("Excel 文件预览")
root.geometry("800x300")

btn = tk.Button(root, text="选择Excel文件", command=open_file)
btn.pack(pady=10)

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()