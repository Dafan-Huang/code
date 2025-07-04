import tkinter as tk
import pyttsx3
import itertools
import random

# 初始化语音引擎
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# 彩色背景相关
colors = ["#FF6F61", "#FFB347", "#FFF275", "#8DE969", "#4FC3F7", "#9575CD", "#F06292"]
color_cycle = itertools.cycle(colors)
bg_job = None
changing_bg = False

def change_bg():
    global bg_job
    if changing_bg:
        root.configure(bg=next(color_cycle))
        bg_job = root.after(200, change_bg)

def start_bg_change():
    global changing_bg
    changing_bg = True
    change_bg()

def stop_bg_change():
    global changing_bg, bg_job
    changing_bg = False
    if bg_job:
        root.after_cancel(bg_job)
        bg_job = None

# 随机文本与名字
texts = [
    "你好，世界！",
    "Python最棒!",
    "祝你开心！",
    "编程使人快乐！"
]
names = ["席睿康", "程天睿", "王天一", "高祺享"]

def random_label_text():
    new_text = random.choice(texts)
    label.config(text=new_text)
    speak(new_text)

speaking_names = False

def speak_random_name():
    if speaking_names:
        name = random.choice(names)
        speak(f"{name}，回头")
        root.after(1500, speak_random_name)

def toggle_speak_names():
    global speaking_names
    speaking_names = not speaking_names
    if speaking_names:
        speak_random_name()
        toggle_button.config(text="停止名字播报")
    else:
        toggle_button.config(text="开始名字播报")

# 主窗口设置
root = tk.Tk()
root.title("彩虹说话机")
root.geometry("400x260")
root.resizable(False, False)

# 居中窗口
def center_window(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

# 标签与按钮
label = tk.Label(root, text="你好，世界！", font=("Arial", 16), bg="white")
label.pack(pady=20)

button = tk.Button(root, text="随机文本", command=random_label_text)
button.pack(pady=10)

toggle_button = tk.Button(root, text="开始名字播报", command=toggle_speak_names)
toggle_button.pack(pady=5)

center_window(root)
start_bg_change()

root.mainloop()