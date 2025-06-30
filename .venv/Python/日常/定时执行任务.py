import time
import threading
import tkinter as tk
from tkinter import ttk
import os
import platform
import queue

class TaskSchedulerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("定时任务工具")
        self.log_queue = queue.Queue()
        self.shutdown_scheduled = False

        self.TASKS = {
            "打印任务": self.my_task,
            "定时重启": self.restart_task,
            "定时开关软件": self.dummy_placeholder_task,
            "定时关机": self.shutdown_task
        }

        self.create_widgets()
        self.process_log()

    def create_widgets(self):
        tk.Label(self.master, text="选择任务:").grid(row=0, column=0, padx=10, pady=10)
        self.task_var = tk.StringVar()
        self.task_combo = ttk.Combobox(self.master, textvariable=self.task_var, values=list(self.TASKS.keys()), state="readonly")
        self.task_combo.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.master, text="间隔(秒):").grid(row=1, column=0, padx=10, pady=10)
        self.interval_var = tk.StringVar(value="10")
        tk.Entry(self.master, textvariable=self.interval_var).grid(row=1, column=1, padx=10, pady=10)

        self.repeat_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.master, text="循环执行", variable=self.repeat_var).grid(row=2, column=0, columnspan=2, pady=5)

        self.start_btn = tk.Button(self.master, text="启动任务", command=self.start_schedule)
        self.start_btn.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Label(self.master, text="任务日志:").grid(row=4, column=0, columnspan=2)
        self.log_text = tk.Text(self.master, height=10, width=40, state='disabled')
        self.log_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def log(self, msg):
        self.log_queue.put(msg)

    def process_log(self):
        MAX_LOG_LINES = 200
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            self.log_text.config(state='normal')
            self.log_text.insert('end', msg + '\n')
            lines = self.log_text.get('1.0', 'end-1c').split('\n')
            if len(lines) > MAX_LOG_LINES:
                self.log_text.delete('1.0', f'{len(lines) - MAX_LOG_LINES + 1}.0')
            self.log_text.see('end')
            self.log_text.config(state='disabled')
        self.master.after(100, self.process_log)

    def start_schedule(self):
        task_name, interval, repeat = self.validate_params()
        if task_name is None:
            return
        self.schedule_selected_task(task_name, interval, repeat)

    def validate_params(self):
        task_name = self.task_var.get()
        if not task_name:
            self.log("请选择一个任务。")
            return None, None, None
        try:
            interval = int(self.interval_var.get())
            if interval <= 0:
                self.log("请输入大于0的间隔秒数。")
                return None, None, None
        except ValueError:
            self.log("请输入有效的数字作为间隔。")
            return None, None, None
        repeat = self.repeat_var.get()
        # 定时关机任务只执行一次
        if task_name == "定时关机":
            repeat = False
        return task_name, interval, repeat

    def schedule_task(self, interval, task, repeat=True):
        def wrapper():
            if repeat:
                while True:
                    try:
                        task()
                    except Exception as e:
                        self.log(f"任务执行异常: {e}")
                    time.sleep(interval)
            else:
                try:
                    task()
                except Exception as e:
                    self.log(f"任务执行异常: {e}")
        t = threading.Thread(target=wrapper, daemon=True)
        t.start()

    def schedule_selected_task(self, task_name, interval, repeat):
        task = self.TASKS[task_name]
        self.schedule_task(interval, task, repeat)

    # 任务实现
    def my_task(self):
        self.log("任务正在执行...")

    def shutdown_task(self):
        if self.shutdown_scheduled:
            self.log("关机任务已在队列中，请勿重复操作。")
            return
        self.shutdown_scheduled = True
        self.log("正在关机...")
        current_os = platform.system().lower()
        if current_os == 'windows':
            os.system("shutdown /s /t 60")
        elif current_os == 'linux':
            os.system("shutdown -h now")
        elif current_os == 'darwin':
            self.log("macOS关机需要管理员权限，请确保以管理员身份运行。")
            os.system("sudo shutdown -h now")
        else:
            self.log("不支持的操作系统，无法执行关机命令。")

    def restart_task(self):
        self.log("正在重启...（占位任务，无实际操作）")

    def dummy_placeholder_task(self):
        self.log("模拟开关软件...（占位任务，无实际操作）")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskSchedulerApp(root)
    root.mainloop()