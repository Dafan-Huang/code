import tkinter as tk
import pyttsx3
import itertools
import random

# 初始化语音引擎（只初始化一次，提高效率）
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def change_bg():
    root.configure(bg=next(color_cycle))
    root.after(200, change_bg)

def random_label_text():
    new_text = random.choice(texts)
    label.config(text=new_text)
    speak(new_text)

def speak_random_name():
    name = random.choice(names)
    speak(f"{name}，回头")
    root.after(1000, speak_random_name)

# 预定义文本和名字
texts = [
    "你好，世界！",
    "Python最棒!",
    "祝你开心！",
    "编程使人快乐！"
]
names = ["席睿康", "程天睿", "王天一", "高祺享"]

# 颜色循环
colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]
color_cycle = itertools.cycle(colors)

# 创建主窗口
root = tk.Tk()
root.title("彩虹说话机")
root.geometry("350x220")

label = tk.Label(root, text="你好，世界！", font=("Arial", 24))
label.pack(expand=True)

button = tk.Button(root, text="换一句", command=random_label_text)
button.pack(pady=10)

# 启动背景变换和名字播报
change_bg()
root.after(100, speak_random_name)
root.mainloop()