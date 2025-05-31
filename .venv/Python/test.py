import tkinter as tk
import pyttsx3

root = tk.Tk()
root.title("Hello Window")
root.geometry("300x200")

label = tk.Label(root, text="你是大傻逼", font=("Arial", 24))

# 播放语音
engine = pyttsx3.init()
engine.say("你是大傻逼")
engine.runAndWait()
label.pack(expand=True)

root.mainloop()