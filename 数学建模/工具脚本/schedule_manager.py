#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务管理器 - 设置和管理定时任务
"""

import os
import sys
import platform
import subprocess
import logging
from datetime import datetime, time
from typing import Optional, List

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('schedule_manager.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScheduleManager:
    def __init__(self, project_path: str = None):
        """
        初始化定时任务管理器
        :param project_path: 项目路径
        """
        if project_path is None:
            self.project_path = os.path.dirname(os.path.dirname(__file__))
        else:
            self.project_path = project_path
            
        self.scripts_dir = os.path.join(self.project_path, "工具脚本")
        self.data_collector_path = os.path.join(self.scripts_dir, "data_collector.py")
        self.git_uploader_path = os.path.join(self.scripts_dir, "git_uploader.py")
        
        # 获取Python可执行文件路径
        self.python_path = sys.executable
        
        # 检测操作系统
        self.system = platform.system().lower()
        
    def run_command(self, command: List[str], shell: bool = False) -> Optional[str]:
        """
        运行命令行命令
        :param command: 命令列表
        :param shell: 是否使用shell
        :return: 命令输出
        """
        try:
            if shell:
                command_str = ' '.join(command)
                result = subprocess.run(
                    command_str,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
            else:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
            
            if result.returncode == 0:
                logger.info(f"命令执行成功: {' '.join(command)}")
                return result.stdout
            else:
                logger.error(f"命令执行失败: {' '.join(command)}")
                logger.error(f"错误信息: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"执行命令时发生异常: {e}")
            return None
    
    def create_windows_task(self) -> bool:
        """
        创建Windows定时任务
        :return: 是否成功
        """
        try:
            logger.info("创建Windows定时任务...")
            
            # 数据采集任务（每天早上9点）
            data_command = f'schtasks /create /tn "DataCollector" /tr "{self.python_path} {self.data_collector_path}" /sc daily /st 09:00 /f'
            result = self.run_command([data_command], shell=True)
            
            if result is None:
                logger.error("创建数据采集任务失败")
                return False
            
            # Git上传任务（每天晚上9点）
            git_command = f'schtasks /create /tn "GitUploader" /tr "{self.python_path} {self.git_uploader_path}" /sc daily /st 21:00 /f'
            result = self.run_command([git_command], shell=True)
            
            if result is None:
                logger.error("创建Git上传任务失败")
                return False
            
            logger.info("Windows定时任务创建成功")
            return True
            
        except Exception as e:
            logger.error(f"创建Windows定时任务时发生错误: {e}")
            return False
    
    def create_linux_cron(self) -> bool:
        """
        创建Linux cron定时任务
        :return: 是否成功
        """
        try:
            logger.info("创建Linux cron定时任务...")
            
            # 数据采集任务（每天早上9点）
            data_cron = f"0 9 * * * cd {self.project_path} && {self.python_path} {self.data_collector_path}"
            
            # Git上传任务（每天晚上9点）
            git_cron = f"0 21 * * * cd {self.project_path} && {self.python_path} {self.git_uploader_path}"
            
            # 获取当前用户的crontab
            current_cron = self.run_command(['crontab', '-l'])
            
            if current_cron is None:
                current_cron = ""
            
            # 检查任务是否已存在
            if "DataCollector" not in current_cron:
                # 添加新任务
                new_cron = current_cron.strip() + "\n" + data_cron + "\n" + git_cron + "\n"
                
                # 写入临时文件
                temp_file = os.path.join(self.project_path, "temp_cron.txt")
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(new_cron)
                
                # 安装新的crontab
                result = self.run_command(['crontab', temp_file])
                
                # 删除临时文件
                os.remove(temp_file)
                
                if result is None:
                    logger.error("创建cron任务失败")
                    return False
            
            logger.info("Linux cron定时任务创建成功")
            return True
            
        except Exception as e:
            logger.error(f"创建Linux cron定时任务时发生错误: {e}")
            return False
    
    def create_macos_launchd(self) -> bool:
        """
        创建macOS launchd定时任务
        :return: 是否成功
        """
        try:
            logger.info("创建macOS launchd定时任务...")
            
            # 创建LaunchAgents目录
            launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
            os.makedirs(launch_agents_dir, exist_ok=True)
            
            # 数据采集任务plist文件
            data_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.datacollector</string>
    <key>ProgramArguments</key>
    <array>
        <string>{self.python_path}</string>
        <string>{self.data_collector_path}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>{self.project_path}</string>
    <key>StandardOutPath</key>
    <string>{self.project_path}/data_collector.log</string>
    <key>StandardErrorPath</key>
    <string>{self.project_path}/data_collector_error.log</string>
</dict>
</plist>"""
            
            # Git上传任务plist文件
            git_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.gituploader</string>
    <key>ProgramArguments</key>
    <array>
        <string>{self.python_path}</string>
        <string>{self.git_uploader_path}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>21</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>{self.project_path}</string>
    <key>StandardOutPath</key>
    <string>{self.project_path}/git_uploader.log</string>
    <key>StandardErrorPath</key>
    <string>{self.project_path}/git_uploader_error.log</string>
</dict>
</plist>"""
            
            # 写入plist文件
            data_plist_path = os.path.join(launch_agents_dir, "com.user.datacollector.plist")
            git_plist_path = os.path.join(launch_agents_dir, "com.user.gituploader.plist")
            
            with open(data_plist_path, 'w', encoding='utf-8') as f:
                f.write(data_plist)
            
            with open(git_plist_path, 'w', encoding='utf-8') as f:
                f.write(git_plist)
            
            # 加载任务
            self.run_command(['launchctl', 'load', data_plist_path])
            self.run_command(['launchctl', 'load', git_plist_path])
            
            logger.info("macOS launchd定时任务创建成功")
            return True
            
        except Exception as e:
            logger.error(f"创建macOS launchd定时任务时发生错误: {e}")
            return False
    
    def create_scheduled_tasks(self) -> bool:
        """
        根据操作系统创建定时任务
        :return: 是否成功
        """
        try:
            logger.info(f"检测到操作系统: {self.system}")
            
            if self.system == "windows":
                return self.create_windows_task()
            elif self.system in ["linux", "darwin"]:
                if self.system == "darwin":
                    return self.create_macos_launchd()
                else:
                    return self.create_linux_cron()
            else:
                logger.error(f"不支持的操作系统: {self.system}")
                return False
                
        except Exception as e:
            logger.error(f"创建定时任务时发生错误: {e}")
            return False
    
    def list_tasks(self) -> Optional[str]:
        """
        列出当前定时任务
        :return: 任务列表
        """
        try:
            if self.system == "windows":
                result = self.run_command(['schtasks', '/query', '/fo', 'list'])
            elif self.system == "linux":
                result = self.run_command(['crontab', '-l'])
            elif self.system == "darwin":
                result = self.run_command(['launchctl', 'list'])
            else:
                logger.error(f"不支持的操作系统: {self.system}")
                return None
            
            return result
            
        except Exception as e:
            logger.error(f"列出定时任务时发生错误: {e}")
            return None
    
    def remove_tasks(self) -> bool:
        """
        移除定时任务
        :return: 是否成功
        """
        try:
            logger.info("移除定时任务...")
            
            if self.system == "windows":
                # 删除Windows任务
                self.run_command(['schtasks', '/delete', '/tn', 'DataCollector', '/f'], shell=True)
                self.run_command(['schtasks', '/delete', '/tn', 'GitUploader', '/f'], shell=True)
                
            elif self.system == "linux":
                # 删除Linux cron任务
                current_cron = self.run_command(['crontab', '-l'])
                if current_cron:
                    lines = current_cron.strip().split('\n')
                    new_lines = [line for line in lines if "DataCollector" not in line and "GitUploader" not in line]
                    new_cron = '\n'.join(new_lines) + '\n'
                    
                    # 写入临时文件
                    temp_file = os.path.join(self.project_path, "temp_cron.txt")
                    with open(temp_file, 'w', encoding='utf-8') as f:
                        f.write(new_cron)
                    
                    # 安装新的crontab
                    self.run_command(['crontab', temp_file])
                    os.remove(temp_file)
                    
            elif self.system == "darwin":
                # 卸载macOS launchd任务
                launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
                data_plist_path = os.path.join(launch_agents_dir, "com.user.datacollector.plist")
                git_plist_path = os.path.join(launch_agents_dir, "com.user.gituploader.plist")
                
                self.run_command(['launchctl', 'unload', data_plist_path])
                self.run_command(['launchctl', 'unload', git_plist_path])
                
                if os.path.exists(data_plist_path):
                    os.remove(data_plist_path)
                if os.path.exists(git_plist_path):
                    os.remove(git_plist_path)
            
            logger.info("定时任务移除成功")
            return True
            
        except Exception as e:
            logger.error(f"移除定时任务时发生错误: {e}")
            return False
    
    def test_scripts(self) -> bool:
        """
        测试脚本是否正常运行
        :return: 是否成功
        """
        try:
            logger.info("测试脚本...")
            
            # 测试数据采集脚本
            logger.info("测试数据采集脚本...")
            result = self.run_command([self.python_path, self.data_collector_path])
            
            if result is None:
                logger.error("数据采集脚本测试失败")
                return False
            
            # 测试Git上传脚本
            logger.info("测试Git上传脚本...")
            result = self.run_command([self.python_path, self.git_uploader_path])
            
            if result is None:
                logger.error("Git上传脚本测试失败")
                return False
            
            logger.info("脚本测试成功")
            return True
            
        except Exception as e:
            logger.error(f"测试脚本时发生错误: {e}")
            return False

def main():
    """主函数"""
    logger.info("开始定时任务管理...")
    
    # 创建定时任务管理器
    manager = ScheduleManager()
    
    # 测试脚本
    if not manager.test_scripts():
        logger.error("脚本测试失败，请检查脚本是否正常")
        return False
    
    # 创建定时任务
    success = manager.create_scheduled_tasks()
    
    if success:
        logger.info("定时任务创建成功")
        
        # 列出当前任务
        tasks = manager.list_tasks()
        if tasks:
            logger.info("当前定时任务:")
            logger.info(tasks)
    else:
        logger.error("定时任务创建失败")
    
    return success

if __name__ == "__main__":
    main()