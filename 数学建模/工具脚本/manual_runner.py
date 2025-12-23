#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动任务执行器 - 手动执行数据采集和Git上传任务
"""

import os
import sys
import logging
from datetime import datetime
from typing import List, Optional

# 添加工具脚本目录到路径
scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(scripts_dir)

# 导入现有的模块
from data_collector import DataCollector
from git_uploader import GitUploader

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('manual_tasks.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ManualTaskRunner:
    def __init__(self):
        """
        初始化手动任务执行器
        """
        self.project_path = os.path.dirname(scripts_dir)
        self.collector = DataCollector()
        self.uploader = GitUploader()
        
    def show_menu(self):
        """
        显示菜单
        """
        print("\n" + "="*50)
        print("           数学建模 - 手动任务执行器")
        print("="*50)
        print("1. 执行数据采集")
        print("2. 执行Git上传")
        print("3. 执行数据采集 + Git上传")
        print("4. 查看Git状态")
        print("5. 查看最近提交历史")
        print("6. 清理旧数据文件")
        print("0. 退出")
        print("="*50)
        
    def run_data_collection(self) -> bool:
        """
        运行数据采集
        :return: 是否成功
        """
        try:
            logger.info("开始执行数据采集任务...")
            print("\n正在采集数据，请稍候...")
            
            # 采集数据
            saved_files = self.collector.collect_all_data()
            
            if saved_files:
                print(f"\n[成功] 数据采集完成！共保存 {len(saved_files)} 个文件:")
                for file in saved_files:
                    print(f"   - {os.path.basename(file)}")
                return True
            else:
                print("\n[失败] 数据采集失败，没有保存任何文件")
                return False
                
        except Exception as e:
            logger.error(f"执行数据采集时发生错误: {e}")
            print(f"\n❌ 数据采集失败: {e}")
            return False
    
    def run_git_upload(self) -> bool:
        """
        运行Git上传
        :return: 是否成功
        """
        try:
            logger.info("开始执行Git上传任务...")
            print("\n正在上传到GitHub，请稍候...")
            
            # 上传数据
            success = self.uploader.upload_data()
            
            if success:
                print("\n[成功] Git上传成功！")
                return True
            else:
                print("\n[失败] Git上传失败")
                return False
                
        except Exception as e:
            logger.error(f"执行Git上传时发生错误: {e}")
            print(f"\n❌ Git上传失败: {e}")
            return False
    
    def run_both_tasks(self) -> bool:
        """
        运行数据采集和Git上传
        :return: 是否成功
        """
        try:
            logger.info("开始执行数据采集和Git上传任务...")
            
            # 先执行数据采集
            collect_success = self.run_data_collection()
            
            if collect_success:
                # 如果数据采集成功，再执行Git上传
                upload_success = self.run_git_upload()
                
                if upload_success:
                    print("\n[成功] 所有任务执行成功！")
                    return True
                else:
                    print("\n[警告] 数据采集成功，但Git上传失败")
                    return False
            else:
                print("\n[失败] 数据采集失败，跳过Git上传")
                return False
                
        except Exception as e:
            logger.error(f"执行任务时发生错误: {e}")
            print(f"\n❌ 任务执行失败: {e}")
            return False
    
    def show_git_status(self):
        """
        显示Git状态
        """
        try:
            print("\n正在检查Git状态...")
            
            # 检查是否有更改
            has_changes = self.uploader.check_git_status()
            
            if has_changes:
                print("\n[信息] 检测到文件更改:")
                output = self.uploader.run_command(['git', 'status'])
                if output:
                    print(output)
            else:
                print("\n[成功] 工作区干净，没有未提交的更改")
                
        except Exception as e:
            logger.error(f"检查Git状态时发生错误: {e}")
            print(f"\n❌ 检查Git状态失败: {e}")
    
    def show_commit_history(self):
        """
        显示提交历史
        """
        try:
            print("\n正在获取提交历史...")
            
            history = self.uploader.get_commit_history(limit=10)
            
            if history:
                print("\n[信息] 最近的提交历史:")
                print(history)
            else:
                print("\n[失败] 无法获取提交历史")
                
        except Exception as e:
            logger.error(f"获取提交历史时发生错误: {e}")
            print(f"\n❌ 获取提交历史失败: {e}")
    
    def cleanup_old_files(self):
        """
        清理旧数据文件
        """
        try:
            print("\n正在清理旧数据文件...")
            
            # 询问保留天数
            while True:
                try:
                    days = input("请输入要保留的天数 (默认7天): ").strip()
                    if not days:
                        days = 7
                    else:
                        days = int(days)
                    break
                except ValueError:
                    print("请输入有效的数字")
            
            self.collector.cleanup_old_files(days_to_keep=days)
            print(f"\n✅ 清理完成，保留了最近 {days} 天的数据文件")
            
        except Exception as e:
            logger.error(f"清理旧文件时发生错误: {e}")
            print(f"\n❌ 清理失败: {e}")
    
    def run(self):
        """
        运行主程序
        """
        logger.info("启动手动任务执行器")
        
        while True:
            try:
                self.show_menu()
                
                choice = input("\n请选择操作 (0-6): ").strip()
                
                if choice == '0':
                    print("\n👋 再见！")
                    break
                    
                elif choice == '1':
                    self.run_data_collection()
                    
                elif choice == '2':
                    self.run_git_upload()
                    
                elif choice == '3':
                    self.run_both_tasks()
                    
                elif choice == '4':
                    self.show_git_status()
                    
                elif choice == '5':
                    self.show_commit_history()
                    
                elif choice == '6':
                    self.cleanup_old_files()
                    
                else:
                    print("\n❌ 无效选择，请输入0-6之间的数字")
                
                # 询问是否继续
                if choice != '0':
                    input("\n按回车键继续...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 用户中断，程序退出")
                break
            except Exception as e:
                logger.error(f"程序运行时发生错误: {e}")
                print(f"\n❌ 发生错误: {e}")
                input("按回车键继续...")

def main():
    """主函数"""
    runner = ManualTaskRunner()
    runner.run()

if __name__ == "__main__":
    main()