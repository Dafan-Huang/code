import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import platform

def my_task():
    print("任务正在执行...")

def shutdown_task():
    print("正在关机...")
    current_os = platform.system().lower()
    if current_os == 'windows':
        os.system("shutdown /s /t 1")
    elif current_os == 'linux':
        os.system("shutdown -h now")
    elif current_os == 'darwin':
        os.system("sudo shutdown -h now")
    else:
        print("不支持的操作系统，无法执行关机命令。")

def restart_task():
    """占位任务：无实际重启操作，仅用于演示。"""
    print("正在重启...（占位任务，无实际操作）")

def dummy_placeholder_task():
    """占位任务：无实际开关软件操作，仅用于演示。"""
    print("模拟开关软件...（占位任务，无实际操作）")

TASKS = {
    "打印任务": my_task,
    "定时关机": shutdown_task,
    "定时重启": restart_task,
    "定时开关软件": dummy_placeholder_task
}

def schedule_task(interval, task, repeat=True):
    """
    启动一个线程定时执行指定任务。

    参数:
        interval (int): 任务执行的时间间隔（秒）。
        task (callable): 要执行的任务函数。
        repeat (bool): 是否循环执行任务，默认为 True。为 False 时只执行一次。
    """
    def wrapper():
        if repeat:
            while True:
                task()
                time.sleep(interval)
        else:
            task()
    t = threading.Thread(target=wrapper, daemon=True)
    t.start()

def start_schedule():
    try:
        interval_str = interval_var.get()
        if not interval_str.isdigit():
            messagebox.showwarning("警告", "请输入有效的数字作为间隔")
            return
        interval = int(interval_str)
        task_name = task_var.get()
        if not task_name:
            messagebox.showwarning("警告", "请选择一个任务")
            return
        repeat = repeat_var.get()
        schedule_task(interval, TASKS[task_name], repeat)
        if repeat:
            messagebox.showinfo("提示", f"已启动任务: {task_name}，每{interval}秒执行一次")
        else:
            messagebox.showinfo("提示", f"已启动任务: {task_name}，仅执行一次")
    except ValueError as e:
        # 捕获输入转换为整数时的异常，提示用户输入格式错误
        messagebox.showerror("错误", f"输入格式错误: {e}")
    except Exception as e:
        # 捕获其他异常，建议在实际开发中根据需要细化异常类型
        messagebox.showerror("错误", str(e))

root = tk.Tk()
root.title("定时任务工具")

tk.Label(root, text="选择任务:").grid(row=0, column=0, padx=10, pady=10)
task_var = tk.StringVar()
task_combo = ttk.Combobox(root, textvariable=task_var, values=list(TASKS.keys()), state="readonly")
task_combo.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="间隔(秒):").grid(row=1, column=0, padx=10, pady=10)
interval_var = tk.StringVar(value="10")
tk.Entry(root, textvariable=interval_var).grid(row=1, column=1, padx=10, pady=10)

repeat_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="循环执行", variable=repeat_var).grid(row=2, column=0, columnspan=2, pady=5)

tk.Button(root, text="启动任务", command=start_schedule).grid(row=3, column=0, columnspan=2, pady=20)

root.mainloop()