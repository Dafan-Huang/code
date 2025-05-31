import tkinter as tk
import pyttsx3
import itertools

root = tk.Tk()
root.title("Hello Window")
root.geometry("300x200")

label = tk.Label(root, text="你是大傻逼", font=("Arial", 24))

# 播放语音
engine = pyttsx3.init()
engine.say("你是大傻逼")
engine.runAndWait()
label.pack(expand=True)

colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]
color_cycle = itertools.cycle(colors)

def change_bg():
    root.configure(bg=next(color_cycle))
    root.after(200, change_bg)

change_bg()
root.mainloop()