import time
import threading
import tkinter as tk
from tkinter import ttk
import os
import platform
import queue

def my_task():
    log("任务正在执行...")

shutdown_scheduled = False

def shutdown_task(start_btn=None):
    global shutdown_scheduled
    if shutdown_scheduled:
        log("关机任务已在队列中，请勿重复操作。")
        return
    shutdown_scheduled = True
    log("正在关机...")
    current_os = platform.system().lower()
    if current_os == 'windows':
        os.system("shutdown /s /t 60")  # 60秒后关机，可根据需要调整秒数
    elif current_os == 'linux':
        os.system("shutdown -h now")
    elif current_os == 'darwin':
        log("macOS关机需要管理员权限，请确保以管理员身份运行。")
        os.system("sudo shutdown -h now")
    else:
        log("不支持的操作系统，无法执行关机命令。")
    # 关机任务只执行一次，启动按钮恢复可用
    if start_btn is not None:
        start_btn.config(state='normal')
    shutdown_scheduled = False

def restart_task():
    log("正在重启...（占位任务，无实际操作）")

def dummy_placeholder_task():
    log("模拟开关软件...（占位任务，无实际操作）")

TASKS = {
    "打印任务": my_task,
    "定时关机": None,  # 稍后特殊处理
    "定时重启": restart_task,
    "定时开关软件": dummy_placeholder_task
}

log_queue = queue.Queue()

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

start_btn = tk.Button(root, text="启动任务", command=lambda: start_schedule())
start_btn.grid(row=3, column=0, columnspan=2, pady=10)

tk.Label(root, text="任务日志:").grid(row=4, column=0, columnspan=2)
log_text = tk.Text(root, height=10, width=40, state='disabled')
log_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

def log(msg):
    log_queue.put(msg)

def process_log():
    MAX_LOG_LINES = 200  # 最大日志行数，可根据需要调整
    while not log_queue.empty():
        msg = log_queue.get()
        log_text.config(state='normal')
        log_text.insert('end', msg + '\n')
        # 限制最大日志行数
        lines = log_text.get('1.0', 'end-1c').split('\n')
        if len(lines) > MAX_LOG_LINES:
            # 删除多余的旧日志
            log_text.delete('1.0', f'{len(lines) - MAX_LOG_LINES + 1}.0')
        log_text.see('end')
        log_text.config(state='disabled')
    root.after(100, process_log)
def schedule_task(interval, task, repeat=True):
    def wrapper(repeat=repeat):
        if repeat:
            while True:
                task()
                time.sleep(interval)
        else:
            task()
    t = threading.Thread(target=wrapper, daemon=True)
    t.start()
def validate_params():
    task_name = task_var.get()
    if not task_name:
        log("请选择一个任务。")
        return None, None, None
    try:
        interval = int(interval_var.get())
        if interval <= 0:
            log("请输入大于0的间隔秒数。")
            return None, None, None
    except ValueError:
        log("请输入有效的数字作为间隔。")
        return None, None, None
    repeat = repeat_var.get()
    return task_name, interval, repeat

def schedule_selected_task(task_name, interval, repeat):
    global shutdown_scheduled
    if task_name == "定时关机":
        if shutdown_scheduled:
            log("关机任务已在队列中，请勿重复操作。")
            return
        start_btn.config(state='disabled')
        shutdown_scheduled = True
        task = lambda: shutdown_task(start_btn)
    else:
        task = TASKS[task_name]
    schedule_task(interval, task, repeat)

def start_schedule():
    params = validate_params()
    if params[0] is None:
        return
    task_name, interval, repeat = params
    schedule_selected_task(task_name, interval, repeat)

process_log()
root.mainloop()