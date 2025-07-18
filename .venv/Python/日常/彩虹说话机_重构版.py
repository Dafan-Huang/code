"""
彩虹说话机 - 重构版
一个使用Tkinter和pyttsx3实现的彩色界面语音播报应用。

重构改进:
1. 分离数据配置
2. 改进类结构和方法组织
3. 添加错误处理
4. 增强UI响应性
5. 优化代码可读性和可维护性
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3
import itertools
import random
import threading
import logging
from typing import List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class AppState(Enum):
    """应用状态枚举"""
    IDLE = "idle"
    SPEAKING = "speaking"
    NAME_BROADCASTING = "name_broadcasting"


@dataclass
class AppConfig:
    """应用配置类"""
    # 界面配置
    window_title: str = "彩虹说话机"
    window_size: tuple = (450, 320)
    window_resizable: bool = False
    
    # 颜色配置
    colors: List[str] = None
    color_change_interval: int = 200
    
    # 字体配置
    main_font: tuple = ("微软雅黑", 20, "bold")
    button_font: tuple = ("微软雅黑", 14)
    
    # 语音配置
    speech_rate: int = 200
    speech_volume: float = 0.8
    name_broadcast_interval: int = 1500
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = [
                "#FF6F61", "#FFB347", "#FFF275", "#8DE969", 
                "#4FC3F7", "#9575CD", "#F06292"
            ]


class SpeechEngine:
    """语音引擎封装类"""
    
    def __init__(self, rate: int = 200, volume: float = 0.8):
        self.engine = None
        self.rate = rate
        self.volume = volume
        self._init_engine()
    
    def _init_engine(self):
        """初始化语音引擎"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
        except Exception as e:
            logging.error(f"语音引擎初始化失败: {e}")
            messagebox.showerror("错误", "语音引擎初始化失败，语音功能将不可用")
    
    def speak(self, text: str, callback: Optional[Callable] = None):
        """异步播放语音"""
        if not self.engine:
            return
        
        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
                if callback:
                    callback()
            except Exception as e:
                logging.error(f"语音播放失败: {e}")
        
        threading.Thread(target=_speak, daemon=True).start()


class DataProvider:
    """数据提供者类"""
    
    FUNNY_TEXTS = [
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
    
    @classmethod
    def get_random_text(cls) -> str:
        """获取随机文本"""
        return random.choice(cls.FUNNY_TEXTS)
    
    @classmethod
    def get_random_name(cls) -> str:
        """获取随机名字"""
        return random.choice(cls.NAMES)


class UIComponents:
    """UI组件管理器"""
    
    def __init__(self, root: tk.Tk, config: AppConfig):
        self.root = root
        self.config = config
        self.main_frame = None
        self.label = None
        self.random_button = None
        self.toggle_button = None
        self.status_label = None
        
    def setup_window(self):
        """设置窗口属性"""
        self.root.title(self.config.window_title)
        self.root.geometry(f"{self.config.window_size[0]}x{self.config.window_size[1]}")
        self.root.resizable(self.config.window_resizable, self.config.window_resizable)
        
    def create_widgets(self):
        """创建UI组件"""
        # 主框架
        self.main_frame = tk.Frame(self.root, bg=self.config.colors[0])
        self.main_frame.pack(expand=True, fill="both")
        
        # 标题标签
        self.label = tk.Label(
            self.main_frame, 
            text="你好，世界！",
            font=self.config.main_font,
            bg=self.config.colors[0], 
            fg="#222", 
            pady=20, 
            padx=10,
            relief="groove", 
            bd=2,
            wraplength=400
        )
        self.label.pack(pady=(30, 20), ipadx=10, ipady=10, fill="x", padx=30)
        
        # 按钮样式
        button_style = {
            "font": self.config.button_font,
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
        
        # 按钮框架
        button_frame = tk.Frame(self.main_frame, bg=self.config.colors[0])
        button_frame.pack(pady=10)
        
        # 随机文本按钮
        self.random_button = tk.Button(
            button_frame, 
            text="随机文本", 
            **button_style
        )
        self.random_button.pack(pady=5)
        
        # 名字播报切换按钮
        self.toggle_button = tk.Button(
            button_frame, 
            text="开始名字播报", 
            **button_style
        )
        self.toggle_button.pack(pady=5)
        
        # 状态标签
        self.status_label = tk.Label(
            self.main_frame,
            text="就绪",
            font=("微软雅黑", 10),
            bg=self.config.colors[0],
            fg="#666"
        )
        self.status_label.pack(pady=(10, 0))
        
        # 绑定鼠标事件
        for btn in [self.random_button, self.toggle_button]:
            btn.bind("<Enter>", self._on_button_enter)
            btn.bind("<Leave>", self._on_button_leave)
    
    def _on_button_enter(self, event):
        """按钮鼠标进入事件"""
        event.widget.config(bg="#f5f5f5")
    
    def _on_button_leave(self, event):
        """按钮鼠标离开事件"""
        event.widget.config(bg="#fff")
    
    def update_background_color(self, color: str):
        """更新背景颜色"""
        self.root.configure(bg=color)
        if self.main_frame:
            self.main_frame.configure(bg=color)
        if self.label:
            self.label.configure(bg=color)
        if self.status_label:
            self.status_label.configure(bg=color)
    
    def update_text(self, text: str):
        """更新显示文本"""
        if self.label:
            self.label.config(text=text)
    
    def update_status(self, status: str):
        """更新状态文本"""
        if self.status_label:
            self.status_label.config(text=status)
    
    def update_toggle_button(self, text: str):
        """更新切换按钮文本"""
        if self.toggle_button:
            self.toggle_button.config(text=text)
    
    def center_window(self):
        """居中窗口"""
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")


class RainbowSpeakerApp:
    """彩虹说话机主应用类"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.config = AppConfig()
        self.speech_engine = SpeechEngine(
            rate=self.config.speech_rate,
            volume=self.config.speech_volume
        )
        self.ui = UIComponents(root, self.config)
        self.data_provider = DataProvider()
        
        # 状态管理
        self.state = AppState.IDLE
        self.color_cycle = itertools.cycle(self.config.colors)
        self.name_broadcast_job = None
        
        # 初始化
        self._setup_logging()
        self._initialize_ui()
        self._start_background_tasks()
    
    def _setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def _initialize_ui(self):
        """初始化UI"""
        self.ui.setup_window()
        self.ui.create_widgets()
        self.ui.center_window()
        
        # 绑定事件
        self.ui.random_button.config(command=self.handle_random_text)
        self.ui.toggle_button.config(command=self.handle_toggle_name_broadcast)
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _start_background_tasks(self):
        """启动后台任务"""
        self._change_background_color()
    
    def _change_background_color(self):
        """循环改变背景颜色"""
        if self.state != AppState.IDLE:
            return
        
        color = next(self.color_cycle)
        self.ui.update_background_color(color)
        self.root.after(self.config.color_change_interval, self._change_background_color)
    
    def handle_random_text(self):
        """处理随机文本按钮点击"""
        if self.state == AppState.SPEAKING:
            return
        
        self.state = AppState.SPEAKING
        self.ui.update_status("正在播放...")
        
        random_text = self.data_provider.get_random_text()
        self.ui.update_text(random_text)
        
        def on_speech_complete():
            self.state = AppState.IDLE
            self.ui.update_status("就绪")
            self._change_background_color()
        
        self.speech_engine.speak(random_text, on_speech_complete)
    
    def handle_toggle_name_broadcast(self):
        """处理名字播报切换按钮点击"""
        if self.state == AppState.NAME_BROADCASTING:
            self._stop_name_broadcast()
        else:
            self._start_name_broadcast()
    
    def _start_name_broadcast(self):
        """开始名字播报"""
        self.state = AppState.NAME_BROADCASTING
        self.ui.update_toggle_button("停止名字播报")
        self.ui.update_status("名字播报中...")
        self._broadcast_name()
    
    def _stop_name_broadcast(self):
        """停止名字播报"""
        self.state = AppState.IDLE
        self.ui.update_toggle_button("开始名字播报")
        self.ui.update_status("就绪")
        
        if self.name_broadcast_job:
            self.root.after_cancel(self.name_broadcast_job)
            self.name_broadcast_job = None
        
        self._change_background_color()
    
    def _broadcast_name(self):
        """播报名字"""
        if self.state != AppState.NAME_BROADCASTING:
            return
        
        random_name = self.data_provider.get_random_name()
        message = f"{random_name}，回头"
        self.speech_engine.speak(message)
        
        # 调度下一次播报
        self.name_broadcast_job = self.root.after(
            self.config.name_broadcast_interval,
            self._broadcast_name
        )
    
    def on_closing(self):
        """窗口关闭事件处理"""
        self._stop_name_broadcast()
        self.root.destroy()
    
    def run(self):
        """运行应用"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            logging.error(f"应用运行错误: {e}")
            messagebox.showerror("错误", f"应用运行出错: {e}")


def main():
    """主函数"""
    root = tk.Tk()
    app = RainbowSpeakerApp(root)
    app.run()


if __name__ == "__main__":
    main()
