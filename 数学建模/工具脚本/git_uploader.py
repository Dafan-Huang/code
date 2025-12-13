#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git自动上传器 - 将采集的数据自动上传到GitHub
"""

import os
import subprocess
import logging
from datetime import datetime
from typing import List, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('git_uploader.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GitUploader:
    def __init__(self, repo_path: str = None):
        """
        初始化Git上传器
        :param repo_path: 仓库路径，默认为当前目录
        """
        if repo_path is None:
            self.repo_path = os.path.dirname(os.path.dirname(__file__))
        else:
            self.repo_path = repo_path
            
        # 数据目录
        self.data_dir = os.path.join(self.repo_path, "数学建模？")
        
    def run_command(self, command: List[str], cwd: str = None) -> Optional[str]:
        """
        运行命令行命令
        :param command: 命令列表
        :param cwd: 工作目录
        :return: 命令输出
        """
        try:
            if cwd is None:
                cwd = self.repo_path
                
            result = subprocess.run(
                command,
                cwd=cwd,
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
    
    def check_git_status(self) -> bool:
        """
        检查Git状态
        :return: 是否有更改需要提交
        """
        try:
            # 检查Git状态
            output = self.run_command(['git', 'status', '--porcelain'])
            
            if output is None:
                logger.error("无法获取Git状态")
                return False
            
            # 如果有输出，说明有更改
            has_changes = len(output.strip()) > 0
            
            if has_changes:
                logger.info("检测到文件更改")
            else:
                logger.info("没有文件更改")
                
            return has_changes
            
        except Exception as e:
            logger.error(f"检查Git状态时发生错误: {e}")
            return False
    
    def add_files(self, file_patterns: List[str] = None) -> bool:
        """
        添加文件到暂存区
        :param file_patterns: 文件模式列表，默认添加数据文件夹
        :return: 是否成功
        """
        try:
            if file_patterns is None:
                # 默认添加数据文件夹
                file_patterns = ['数学建模？/*.csv', '*.log']
            
            for pattern in file_patterns:
                logger.info(f"添加文件: {pattern}")
                output = self.run_command(['git', 'add', pattern])
                
                if output is None:
                    logger.error(f"添加文件失败: {pattern}")
                    return False
            
            logger.info("文件添加成功")
            return True
            
        except Exception as e:
            logger.error(f"添加文件时发生错误: {e}")
            return False
    
    def commit_changes(self, message: str = None) -> bool:
        """
        提交更改
        :param message: 提交信息
        :return: 是否成功
        """
        try:
            if message is None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"自动上传数据 - {timestamp}"
            
            logger.info(f"提交更改: {message}")
            output = self.run_command(['git', 'commit', '-m', message])
            
            if output is None:
                logger.error("提交失败")
                return False
            
            logger.info("提交成功")
            return True
            
        except Exception as e:
            logger.error(f"提交时发生错误: {e}")
            return False
    
    def push_to_remote(self, remote: str = 'origin', branch: str = 'master') -> bool:
        """
        推送到远程仓库
        :param remote: 远程仓库名称
        :param branch: 分支名称
        :return: 是否成功
        """
        try:
            logger.info(f"推送到远程仓库: {remote}/{branch}")
            output = self.run_command(['git', 'push', remote, branch])
            
            if output is None:
                logger.error("推送失败")
                return False
            
            logger.info("推送成功")
            return True
            
        except Exception as e:
            logger.error(f"推送时发生错误: {e}")
            return False
    
    def pull_latest_changes(self, remote: str = 'origin', branch: str = 'master') -> bool:
        """
        拉取最新更改
        :param remote: 远程仓库名称
        :param branch: 分支名称
        :return: 是否成功
        """
        try:
            logger.info(f"拉取最新更改: {remote}/{branch}")
            output = self.run_command(['git', 'pull', remote, branch])
            
            if output is None:
                logger.error("拉取失败")
                return False
            
            logger.info("拉取成功")
            return True
            
        except Exception as e:
            logger.error(f"拉取时发生错误: {e}")
            return False
    
    def check_remote_connection(self) -> bool:
        """
        检查远程连接
        :return: 是否连接成功
        """
        try:
            logger.info("检查远程连接...")
            output = self.run_command(['git', 'remote', '-v'])
            
            if output is None:
                logger.error("无法获取远程仓库信息")
                return False
            
            logger.info("远程仓库信息:")
            logger.info(output)
            
            # 尝试ping远程仓库
            output = self.run_command(['git', 'ls-remote', 'origin'])
            
            if output is None:
                logger.error("无法连接到远程仓库")
                return False
            
            logger.info("远程连接正常")
            return True
            
        except Exception as e:
            logger.error(f"检查远程连接时发生错误: {e}")
            return False
    
    def upload_data(self, force: bool = False) -> bool:
        """
        上传数据到GitHub
        :param force: 是否强制上传
        :return: 是否成功
        """
        try:
            logger.info("开始上传数据到GitHub...")
            
            # 检查远程连接
            if not self.check_remote_connection():
                logger.error("远程连接检查失败，无法上传")
                return False
            
            # 拉取最新更改
            if not self.pull_latest_changes():
                logger.warning("拉取最新更改失败，继续上传...")
            
            # 检查是否有更改
            if not force and not self.check_git_status():
                logger.info("没有更改需要上传")
                return True
            
            # 添加文件
            if not self.add_files():
                logger.error("添加文件失败")
                return False
            
            # 再次检查是否有更改
            if not self.check_git_status():
                logger.info("没有更改需要提交")
                return True
            
            # 提交更改
            if not self.commit_changes():
                logger.error("提交失败")
                return False
            
            # 推送到远程仓库
            if not self.push_to_remote():
                logger.error("推送失败")
                return False
            
            logger.info("数据上传成功")
            return True
            
        except Exception as e:
            logger.error(f"上传数据时发生错误: {e}")
            return False
    
    def get_commit_history(self, limit: int = 5) -> Optional[str]:
        """
        获取提交历史
        :param limit: 限制条数
        :return: 提交历史
        """
        try:
            output = self.run_command(['git', 'log', '--oneline', f'-{limit}'])
            return output
            
        except Exception as e:
            logger.error(f"获取提交历史时发生错误: {e}")
            return None

def main():
    """主函数"""
    logger.info("开始Git上传任务...")
    
    # 创建Git上传器
    uploader = GitUploader()
    
    # 上传数据
    success = uploader.upload_data()
    
    if success:
        logger.info("Git上传任务完成")
        
        # 显示最近的提交历史
        history = uploader.get_commit_history()
        if history:
            logger.info("最近的提交历史:")
            logger.info(history)
    else:
        logger.error("Git上传任务失败")
    
    return success

if __name__ == "__main__":
    main()