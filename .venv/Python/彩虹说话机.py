"""
彩虹说话机
一个使用Tkinter和pyttsx3实现的彩色界面语音播报应用。
"""

import tkinter as tk
import pyttsx3
import itertools
import random

class RainbowSpeakerApp:
    COLORS = ["#FF6F61", "#FFB347", "#FFF275", "#8DE969", "#4FC3F7", "#9575CD", "#F06292"]
    TEXTS = [
        "你写的代码真是一团糟！", "又出bug了吧,气死我了！", "你这家伙能不能认真点？",
        "写代码别瞎搞行不行！", "这都能写错，服了你了！", "别再摸鱼了，赶紧干活！",
        "你是不是又忘了保存？", "代码乱七八糟，重写！", "你写的什么鬼东西！",
        "别再犯傻了，动动脑子！", "写代码能不能走点心？", "又报错了，气不气？",
        "你这水平还敢写代码？", "别再拖延了，快点写！", "写成这样不如不写！",
        "你是不是在逗我？", "代码写得跟屎一样！", "别再出错了，求你了！",
        "你能不能靠谱点？", "写代码别睡着了！", "你写的代码像没睡醒一样！",
        "这点小事都能写错，服气！", "你写的代码让我怀疑人生！", "你是不是把键盘当鼓敲？",
        "写成这样老板都要哭了！"
    ]
    NAMES = ["席睿康", "程天睿", "王天一", "高祺享"]

    def __init__(self, root):
        self.root = root
        self.engine = pyttsx3.init()
        self.color_cycle = itertools.cycle(self.COLORS)
        self.speaking_names = False
        self.name_job = None

        self.setup_ui()
        self.center_window()
        self.change_bg()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def change_bg(self):
        color = next(self.color_cycle)
        self.root.configure(bg=color)
        self.main_frame.configure(bg=color)
        self.root.after(200, self.change_bg)

    def random_label_text(self):
        new_text = random.choice(self.TEXTS)
        self.label.config(text=new_text)
        self.speak(new_text)

    def speak_random_name(self):
        if self.speaking_names:
            name = random.choice(self.NAMES)
            self.speak(f"{name}，回头")
            self.name_job = self.root.after(1500, self.speak_random_name)

    def toggle_speak_names(self):
        self.speaking_names = not self.speaking_names
        self.toggle_button.config(
            text="停止名字播报" if self.speaking_names else "开始名字播报"
        )
        if self.speaking_names:
            self.speak_random_name()
        elif self.name_job:
            self.root.after_cancel(self.name_job)
            self.name_job = None

    def on_enter(self, e):
        e.widget._original_bg = e.widget.cget("bg")
        e.widget.config(bg="#f5f5f5")

    def on_leave(self, e):
        e.widget.config(bg=getattr(e.widget, "_original_bg", "#fff"))

    def setup_ui(self):
        self.root.title("彩虹说话机")
        self.root.geometry("420x280")
        self.root.resizable(False, False)

        self.main_frame = tk.Frame(self.root, bg=self.COLORS[0])
        self.main_frame.pack(expand=True, fill="both")

        self.label = tk.Label(
            self.main_frame, text="你好，世界！",
            font=("微软雅黑", 20, "bold"),
            bg=self.COLORS[0], fg="#222", pady=20, padx=10,
            relief="groove", bd=2
        )
        self.label.pack(pady=(30, 20), ipadx=10, ipady=10, fill="x", padx=30)

        button_style = {
            "font": ("微软雅黑", 14),
            "bg": "#fff",
            "fg": "#333",
            "activebackground": "#e0e0e0",
            "activeforeground": "#FF6F61",
            "relief": "ridge",
            "bd": 2,
            "cursor": "hand2",
            "width": 16,
            "height": 1
        }

        btn_random = tk.Button(self.main_frame, text="随机文本", command=self.random_label_text, **button_style)
        btn_random.pack(pady=8)

        self.toggle_button = tk.Button(self.main_frame, text="开始名字播报", command=self.toggle_speak_names, **button_style)
        self.toggle_button.pack(pady=8)

        for btn in [btn_random, self.toggle_button]:
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

    def center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RainbowSpeakerApp(root)
    root.mainloop()
