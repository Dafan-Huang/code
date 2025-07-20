"""
彩虹说话机 - 增强版（支持配置文件）
一个使用Tkinter和pyttsx3实现的彩色界面语音播报应用。

新增功能:
1. 支持TOML配置文件
2. 动态配置加载
3. 配置验证
4. 日志文件输出
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyttsx3
import itertools
import random
import threading
import logging
from typing import List, Optional, Callable, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import os
from pathlib import Path

# 尝试导入toml，如果没有则使用json作为配置格式
try:
    import tomllib
    HAS_TOML = True
except ImportError:
    try:
        import tomli as tomllib
        HAS_TOML = True
    except ImportError:
        HAS_TOML = False


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
    window_width: int = 450
    window_height: int = 320
    window_resizable: bool = False
    
    # 颜色配置
    colors: List[str] = field(default_factory=lambda: [
        "#FF6F61", "#FFB347", "#FFF275", "#8DE969", 
        "#4FC3F7", "#9575CD", "#F06292"
    ])
    color_change_interval: int = 200
    
    # 字体配置
    main_font_family: str = "微软雅黑"
    main_font_size: int = 20
    main_font_style: str = "bold"
    button_font_family: str = "微软雅黑"
    button_font_size: int = 14
    
    # 语音配置
    speech_rate: int = 200
    speech_volume: float = 0.8
    name_broadcast_interval: int = 1500
    
    # 文本内容
    funny_texts: List[str] = field(default_factory=lambda: [
        "你写的代码真是一团糟！", "又出bug了吧,气死我了！", "你这家伙能不能认真点？",
        "写代码别瞎搞行不行！", "这都能写错，服了你了！", "别再摸鱼了，赶紧干活！",
        "你是不是又忘了保存？", "代码乱七八糟，重写！", "你写的什么鬼东西！",
        "别再犯傻了，动动脑子！", "写代码能不能走点心？", "又报错了，气不气？",
        "你这水平还敢写代码？", "别再拖延了，快点写！", "写成这样不如不写！",
        "你是不是在逗我？", "代码写得跟屎一样！", "别再出错了，求你了！",
        "你能不能靠谱点？", "写代码别睡着了！", "你写的代码像没睡醒一样！",
        "这点小事都能写错，服气！", "你写的代码让我怀疑人生！", "你是不是把键盘当鼓敲？",
        "写成这样老板都要哭了！"
    ])
    
    names: List[str] = field(default_factory=lambda: [
        "席睿康", "程天睿", "王天一", "高祺享"
    ])
    
    # 日志配置
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None
    
    @property
    def main_font(self) -> tuple:
        """主字体元组"""
        return (self.main_font_family, self.main_font_size, self.main_font_style)
    
    @property
    def button_font(self) -> tuple:
        """按钮字体元组"""
        return (self.button_font_family, self.button_font_size)
    
    @property
    def window_size(self) -> tuple:
        """窗口尺寸元组"""
        return (self.window_width, self.window_height)


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config_file()
        self.config = AppConfig()
        self.load_config()
    
    def _find_config_file(self) -> Optional[str]:
        """查找配置文件"""
        possible_paths = [
            "config.toml",
            "config.json",
            "rainbow_speaker_config.toml",
            "rainbow_speaker_config.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def load_config(self):
        """加载配置"""
        if not self.config_path or not os.path.exists(self.config_path):
            logging.info("使用默认配置")
            return
        
        try:
            if self.config_path.endswith('.toml') and HAS_TOML:
                self._load_toml_config()
            elif self.config_path.endswith('.json'):
                self._load_json_config()
            else:
                logging.warning(f"不支持的配置文件格式: {self.config_path}")
        except Exception as e:
            logging.error(f"加载配置文件失败: {e}")
            messagebox.showwarning("配置加载失败", f"无法加载配置文件，使用默认配置。\n错误: {e}")
    
    def _load_toml_config(self):
        """加载TOML配置"""
        with open(self.config_path, 'rb') as f:
            data = tomllib.load(f)
        self._update_config_from_dict(data)
    
    def _load_json_config(self):
        """加载JSON配置"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self._update_config_from_dict(data)
    
    def _update_config_from_dict(self, data: Dict[str, Any]):
        """从字典更新配置"""
        # 扁平化嵌套的配置
        flat_config = {}
        for section, values in data.items():
            if isinstance(values, dict):
                for key, value in values.items():
                    flat_config[key] = value
            else:
                flat_config[section] = values
        
        # 更新配置对象
        for key, value in flat_config.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def save_config(self, path: Optional[str] = None):
        """保存配置"""
        save_path = path or self.config_path or "config.json"
        
        try:
            config_dict = {
                "UI": {
                    "window_title": self.config.window_title,
                    "window_width": self.config.window_width,
                    "window_height": self.config.window_height,
                    "window_resizable": self.config.window_resizable
                },
                "Colors": {
                    "colors": self.config.colors,
                    "color_change_interval": self.config.color_change_interval
                },
                "Fonts": {
                    "main_font_family": self.config.main_font_family,
                    "main_font_size": self.config.main_font_size,
                    "main_font_style": self.config.main_font_style,
                    "button_font_family": self.config.button_font_family,
                    "button_font_size": self.config.button_font_size
                },
                "Speech": {
                    "rate": self.config.speech_rate,
                    "volume": self.config.speech_volume,
                    "name_broadcast_interval": self.config.name_broadcast_interval
                },
                "Texts": {
                    "funny_texts": self.config.funny_texts,
                    "names": self.config.names
                },
                "Logging": {
                    "level": self.config.log_level,
                    "format": self.config.log_format,
                    "file_path": self.config.log_file
                }
            }
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, ensure_ascii=False, indent=2)
            
            logging.info(f"配置已保存到: {save_path}")
            
        except Exception as e:
            logging.error(f"保存配置失败: {e}")
            messagebox.showerror("保存失败", f"无法保存配置文件。\n错误: {e}")


class SpeechEngine:
    """语音引擎封装类"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """初始化语音引擎"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.config.speech_rate)
            self.engine.setProperty('volume', self.config.speech_volume)
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
    
    def update_settings(self, rate: int = None, volume: float = None):
        """更新语音设置"""
        if not self.engine:
            return
        
        try:
            if rate is not None:
                self.engine.setProperty('rate', rate)
                self.config.speech_rate = rate
            if volume is not None:
                self.engine.setProperty('volume', volume)
                self.config.speech_volume = volume
        except Exception as e:
            logging.error(f"更新语音设置失败: {e}")


class DataProvider:
    """数据提供者类"""
    
    def __init__(self, config: AppConfig):
        self.config = config
    
    def get_random_text(self) -> str:
        """获取随机文本"""
        return random.choice(self.config.funny_texts)
    
    def get_random_name(self) -> str:
        """获取随机名字"""
        return random.choice(self.config.names)
    
    def add_text(self, text: str):
        """添加新文本"""
        if text and text not in self.config.funny_texts:
            self.config.funny_texts.append(text)
    
    def add_name(self, name: str):
        """添加新名字"""
        if name and name not in self.config.names:
            self.config.names.append(name)


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
        self.menu_bar = None
        
    def setup_window(self):
        """设置窗口属性"""
        self.root.title(self.config.window_title)
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.resizable(self.config.window_resizable, self.config.window_resizable)
        
    def create_menu(self, app_instance):
        """创建菜单栏"""
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # 文件菜单
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="加载配置", command=app_instance.load_config_file)
        file_menu.add_command(label="保存配置", command=app_instance.save_config_file)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=app_instance.on_closing)
        
        # 设置菜单
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="设置", menu=settings_menu)
        settings_menu.add_command(label="语音设置", command=app_instance.show_speech_settings)
        settings_menu.add_command(label="文本管理", command=app_instance.show_text_manager)
        
        # 帮助菜单
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=app_instance.show_about)
        
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
    
    def __init__(self, root: tk.Tk, config_path: Optional[str] = None):
        self.root = root
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config
        
        self.speech_engine = SpeechEngine(self.config)
        self.ui = UIComponents(root, self.config)
        self.data_provider = DataProvider(self.config)
        
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
        level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        
        handlers = [logging.StreamHandler()]
        if self.config.log_file:
            handlers.append(logging.FileHandler(self.config.log_file, encoding='utf-8'))
        
        logging.basicConfig(
            level=level,
            format=self.config.log_format,
            handlers=handlers
        )
    
    def _initialize_ui(self):
        """初始化UI"""
        self.ui.setup_window()
        self.ui.create_menu(self)
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
    
    def load_config_file(self):
        """加载配置文件"""
        file_path = filedialog.askopenfilename(
            title="选择配置文件",
            filetypes=[("TOML files", "*.toml"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                old_config = self.config_manager.config_path
                self.config_manager.config_path = file_path
                self.config_manager.load_config()
                self.config = self.config_manager.config
                
                # 更新UI
                self._reinitialize_after_config_change()
                messagebox.showinfo("成功", "配置文件加载成功！")
                
            except Exception as e:
                self.config_manager.config_path = old_config
                messagebox.showerror("错误", f"加载配置文件失败：{e}")
    
    def save_config_file(self):
        """保存配置文件"""
        file_path = filedialog.asksaveasfilename(
            title="保存配置文件",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("TOML files", "*.toml"), ("All files", "*.*")]
        )
        
        if file_path:
            self.config_manager.save_config(file_path)
            messagebox.showinfo("成功", "配置文件保存成功！")
    
    def show_speech_settings(self):
        """显示语音设置对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("语音设置")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        # 语音速度
        tk.Label(dialog, text="语音速度:").pack(pady=5)
        rate_var = tk.IntVar(value=self.config.speech_rate)
        rate_scale = tk.Scale(dialog, from_=50, to=400, orient=tk.HORIZONTAL, variable=rate_var)
        rate_scale.pack(pady=5, padx=20, fill="x")
        
        # 音量
        tk.Label(dialog, text="音量:").pack(pady=5)
        volume_var = tk.DoubleVar(value=self.config.speech_volume)
        volume_scale = tk.Scale(dialog, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, variable=volume_var)
        volume_scale.pack(pady=5, padx=20, fill="x")
        
        # 按钮
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def apply_settings():
            self.speech_engine.update_settings(rate_var.get(), volume_var.get())
            dialog.destroy()
        
        tk.Button(button_frame, text="应用", command=apply_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        dialog.transient(self.root)
        dialog.grab_set()
    
    def show_text_manager(self):
        """显示文本管理对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("文本管理")
        dialog.geometry("400x300")
        
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 搞笑文本标签页
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text="搞笑文本")
        
        text_listbox = tk.Listbox(text_frame)
        text_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        for text in self.config.funny_texts:
            text_listbox.insert(tk.END, text)
        
        # 名字标签页
        name_frame = ttk.Frame(notebook)
        notebook.add(name_frame, text="名字列表")
        
        name_listbox = tk.Listbox(name_frame)
        name_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        for name in self.config.names:
            name_listbox.insert(tk.END, name)
        
        dialog.transient(self.root)
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """彩虹说话机 - 增强版

功能特点:
• 彩虹背景色循环变换
• 随机搞笑文本播报
• 定时名字播报
• 支持配置文件
• 语音设置调节
• 文本内容管理

技术栈:
• Python 3.7+
• Tkinter (GUI)
• pyttsx3 (语音合成)
• TOML/JSON (配置文件)

作者: AI Assistant
版本: 2.0 Enhanced"""
        
        messagebox.showinfo("关于彩虹说话机", about_text)
    
    def _reinitialize_after_config_change(self):
        """配置更改后重新初始化"""
        # 更新语音引擎
        self.speech_engine = SpeechEngine(self.config)
        
        # 更新数据提供者
        self.data_provider = DataProvider(self.config)
        
        # 更新UI
        self.ui.config = self.config
        self.color_cycle = itertools.cycle(self.config.colors)
        
        # 重新设置窗口属性
        self.ui.setup_window()
    
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
    import sys
    
    config_path = None
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    root = tk.Tk()
    app = RainbowSpeakerApp(root, config_path)
    app.run()


if __name__ == "__main__":
    main()
