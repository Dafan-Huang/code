import tkinter as tk
import pyttsx3
import itertools
import random

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def change_bg():
    root.configure(bg=next(color_cycle))
    root.after(200, change_bg)

def random_label_text():
    texts = [
        "你是大傻逼",
        "你好，世界！",
        "Python最棒!",
        "祝你开心！",
        "编程使人快乐！"
    ]
    new_text = random.choice(texts)
    label.config(text=new_text)
    speak(new_text)

root = tk.Tk()
root.title("Hello Window")
root.geometry("300x200")

label = tk.Label(root, text="你是大傻逼", font=("Arial", 24))
label.pack(expand=True)

button = tk.Button(root, text="换一句", command=random_label_text)
button.pack(pady=10)

colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]
color_cycle = itertools.cycle(colors)

root.after(100, lambda: speak("席睿康回头"))
change_bg()
root.mainloop()