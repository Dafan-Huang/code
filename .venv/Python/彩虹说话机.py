import tkinter as tk
import pyttsx3
import itertools
import random

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

colors = ["#FF6F61", "#FFB347", "#FFF275", "#8DE969", "#4FC3F7", "#9575CD", "#F06292"]
color_cycle = itertools.cycle(colors)
bg_job = None
changing_bg = False

def change_bg():
    global bg_job
    if changing_bg:
        color = next(color_cycle)
        root.configure(bg=color)
        label.configure(bg=color)
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

texts = [
    "你写的代码真是一团糟！",
    "又出bug了吧,气死我了！",
    "你这家伙能不能认真点？",
    "写代码别瞎搞行不行！",
    "这都能写错，服了你了！",
    "别再摸鱼了，赶紧干活！",
    "你是不是又忘了保存？",
    "代码乱七八糟，重写！",
    "你写的什么鬼东西！",
    "别再犯傻了，动动脑子！",
    "写代码能不能走点心？",
    "又报错了，气不气？",
    "你这水平还敢写代码？",
    "别再拖延了，快点写！",
    "写成这样不如不写！",
    "你是不是在逗我？",
    "代码写得跟屎一样！",
    "别再出错了，求你了！",
    "你能不能靠谱点？",
    "写代码别睡着了！",
    "你写的代码像没睡醒一样！",
    "这点小事都能写错，服气！",
    "你写的代码让我怀疑人生！",
    "你是不是把键盘当鼓敲？",
    "写成这样老板都要哭了！"
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

root = tk.Tk()
root.title("彩虹说话机")
root.geometry("420x280")
root.resizable(False, False)

def center_window(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

# 使用Frame进行布局
main_frame = tk.Frame(root, bg=colors[0], bd=0)
main_frame.pack(expand=True, fill="both")

label = tk.Label(
    main_frame, text="你好，世界！",
    font=("微软雅黑", 20, "bold"),
    bg=colors[0], fg="#222", pady=20, padx=10,
    relief="groove", bd=2
)
label.pack(pady=(30, 20), ipadx=10, ipady=10, fill="x", padx=30)

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

button = tk.Button(main_frame, text="随机文本", command=random_label_text, **button_style)
button.pack(pady=8)

toggle_button = tk.Button(main_frame, text="开始名字播报", command=toggle_speak_names, **button_style)
toggle_button.pack(pady=8)

def on_enter(e):
    e.widget.config(bg="#f5f5f5")
def on_leave(e):
    e.widget.config(bg="#fff")

for btn in [button, toggle_button]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

center_window(root)
start_bg_change()

root.mainloop()