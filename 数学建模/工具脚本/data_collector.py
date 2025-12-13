#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据采集器 - 定时从互联网抓取数据并保存到数学建模？文件夹
"""

import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import logging
from typing import List, Dict, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collector.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self, output_dir: str = None):
        """
        初始化数据采集器
        :param output_dir: 输出目录，默认为"数学建模？"文件夹
        """
        if output_dir is None:
            self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "数学建模？")
        else:
            self.output_dir = output_dir
            
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 请求头，模拟浏览器
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
    def collect_weather_data(self) -> Optional[pd.DataFrame]:
        """
        采集天气数据（示例：使用免费的天气API）
        """
        try:
            # 使用免费的天气API（示例）
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': 'Beijing',  # 可以修改为其他城市
                'appid': 'your_api_key_here',  # 需要替换为实际的API密钥
                'units': 'metric'
            }
            
            # 注意：这里使用模拟数据，实际使用时需要申请API密钥
            logger.info("采集天气数据...")
            
            # 模拟天气数据
            weather_data = {
                'timestamp': [datetime.now()],
                'city': ['北京'],
                'temperature': [random.uniform(15, 35)],
                'humidity': [random.uniform(30, 90)],
                'pressure': [random.uniform(1000, 1020)],
                'wind_speed': [random.uniform(0, 10)],
                'description': [random.choice(['晴', '多云', '阴', '小雨', '中雨'])]
            }
            
            df = pd.DataFrame(weather_data)
            logger.info(f"成功采集天气数据，形状: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"采集天气数据失败: {e}")
            return None
    
    def collect_stock_data(self) -> Optional[pd.DataFrame]:
        """
        采集股票数据（示例：使用模拟数据）
        """
        try:
            logger.info("采集股票数据...")
            
            # 模拟股票数据
            stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
            stock_data = []
            
            for stock in stocks:
                stock_data.append({
                    'timestamp': datetime.now(),
                    'symbol': stock,
                    'price': random.uniform(100, 500),
                    'volume': random.randint(1000000, 10000000),
                    'change': random.uniform(-5, 5),
                    'change_percent': random.uniform(-5, 5)
                })
            
            df = pd.DataFrame(stock_data)
            logger.info(f"成功采集股票数据，形状: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"采集股票数据失败: {e}")
            return None
    
    def collect_news_data(self) -> Optional[pd.DataFrame]:
        """
        采集新闻数据（示例：使用模拟数据）
        """
        try:
            logger.info("采集新闻数据...")
            
            # 模拟新闻数据
            news_sources = ['新华网', '人民网', '央视新闻', '澎湃新闻', '界面新闻']
            categories = ['科技', '财经', '体育', '娱乐', '国际']
            
            news_data = []
            for i in range(10):
                news_data.append({
                    'timestamp': datetime.now() - timedelta(minutes=random.randint(0, 1440)),
                    'source': random.choice(news_sources),
                    'category': random.choice(categories),
                    'title': f'新闻标题{i+1}',
                    'content': f'这是第{i+1}条新闻的内容摘要...',
                    'views': random.randint(100, 10000),
                    'likes': random.randint(10, 1000)
                })
            
            df = pd.DataFrame(news_data)
            logger.info(f"成功采集新闻数据，形状: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"采集新闻数据失败: {e}")
            return None
    
    def collect_economic_data(self) -> Optional[pd.DataFrame]:
        """
        采集经济数据（示例：使用模拟数据）
        """
        try:
            logger.info("采集经济数据...")
            
            # 模拟经济指标数据
            indicators = ['GDP增长率', 'CPI', 'PMI', '失业率', '汇率']
            countries = ['中国', '美国', '日本', '德国', '英国']
            
            economic_data = []
            for country in countries:
                for indicator in indicators:
                    economic_data.append({
                        'timestamp': datetime.now(),
                        'country': country,
                        'indicator': indicator,
                        'value': random.uniform(0, 100),
                        'unit': random.choice(['%', '指数', '百分点']),
                        'period': f"{datetime.now().year}-{datetime.now().month}"
                    })
            
            df = pd.DataFrame(economic_data)
            logger.info(f"成功采集经济数据，形状: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"采集经济数据失败: {e}")
            return None
    
    def save_data(self, df: pd.DataFrame, data_type: str) -> str:
        """
        保存数据到文件
        :param df: 数据DataFrame
        :param data_type: 数据类型
        :return: 保存的文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data_type}_{timestamp}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        logger.info(f"数据已保存到: {filepath}")
        return filepath
    
    def collect_all_data(self) -> List[str]:
        """
        采集所有类型的数据
        :return: 保存的文件路径列表
        """
        saved_files = []
        
        # 采集各种数据
        data_collectors = [
            (self.collect_weather_data, 'weather'),
            (self.collect_stock_data, 'stock'),
            (self.collect_news_data, 'news'),
            (self.collect_economic_data, 'economic')
        ]
        
        for collector, data_type in data_collectors:
            try:
                df = collector()
                if df is not None and not df.empty:
                    filepath = self.save_data(df, data_type)
                    saved_files.append(filepath)
                
                # 添加随机延迟，避免请求过于频繁
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.error(f"采集{data_type}数据时发生错误: {e}")
        
        return saved_files
    
    def cleanup_old_files(self, days_to_keep: int = 7):
        """
        清理旧的数据文件
        :param days_to_keep: 保留天数
        """
        try:
            cutoff_time = datetime.now() - timedelta(days=days_to_keep)
            deleted_count = 0
            
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.csv'):
                    filepath = os.path.join(self.output_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        deleted_count += 1
                        logger.info(f"删除旧文件: {filename}")
            
            logger.info(f"清理完成，删除了 {deleted_count} 个旧文件")
            
        except Exception as e:
            logger.error(f"清理旧文件时发生错误: {e}")

def main():
    """主函数"""
    logger.info("开始数据采集任务...")
    
    # 创建数据采集器
    collector = DataCollector()
    
    # 采集数据
    saved_files = collector.collect_all_data()
    
    # 清理旧文件
    collector.cleanup_old_files(days_to_keep=7)
    
    logger.info(f"数据采集完成，共保存 {len(saved_files)} 个文件")
    
    # 返回保存的文件列表，供其他脚本使用
    return saved_files

if __name__ == "__main__":
    main()