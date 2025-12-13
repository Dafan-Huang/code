#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主控制脚本 - 统一管理数据采集和上传任务
"""

import os
import sys
import argparse
import logging
from datetime import datetime

# 添加脚本目录到Python路径
scripts_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(scripts_dir)
sys.path.append(scripts_dir)

from data_collector import DataCollector
from git_uploader import GitUploader
from schedule_manager import ScheduleManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(project_dir, 'main.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def collect_data():
    """采集数据"""
    logger.info("开始数据采集...")
    collector = DataCollector()
    saved_files = collector.collect_all_data()
    logger.info(f"数据采集完成，保存了 {len(saved_files)} 个文件")
    return saved_files

def upload_data():
    """上传数据"""
    logger.info("开始上传数据...")
    uploader = GitUploader()
    success = uploader.upload_data()
    if success:
        logger.info("数据上传成功")
    else:
        logger.error("数据上传失败")
    return success

def setup_schedule():
    """设置定时任务"""
    logger.info("开始设置定时任务...")
    manager = ScheduleManager()
    success = manager.create_scheduled_tasks()
    if success:
        logger.info("定时任务设置成功")
    else:
        logger.error("定时任务设置失败")
    return success

def remove_schedule():
    """移除定时任务"""
    logger.info("开始移除定时任务...")
    manager = ScheduleManager()
    success = manager.remove_tasks()
    if success:
        logger.info("定时任务移除成功")
    else:
        logger.error("定时任务移除失败")
    return success

def list_schedule():
    """列出定时任务"""
    logger.info("当前定时任务:")
    manager = ScheduleManager()
    tasks = manager.list_tasks()
    if tasks:
        print(tasks)
    else:
        print("没有找到定时任务")

def run_full_cycle():
    """运行完整的数据采集和上传流程"""
    logger.info("开始运行完整流程...")
    
    # 采集数据
    saved_files = collect_data()
    
    # 上传数据
    upload_success = upload_data()
    
    if upload_success and saved_files:
        logger.info("完整流程执行成功")
        return True
    else:
        logger.error("完整流程执行失败")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='数学建模数据采集和上传工具')
    parser.add_argument('command', choices=['collect', 'upload', 'schedule', 'remove', 'list', 'run'], 
                       help='要执行的命令')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info(f"执行命令: {args.command}")
    
    try:
        if args.command == 'collect':
            collect_data()
        elif args.command == 'upload':
            upload_data()
        elif args.command == 'schedule':
            setup_schedule()
        elif args.command == 'remove':
            remove_schedule()
        elif args.command == 'list':
            list_schedule()
        elif args.command == 'run':
            run_full_cycle()
        else:
            logger.error(f"未知命令: {args.command}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        sys.exit(0)
    except Exception as e:
        logger.error(f"执行命令时发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()