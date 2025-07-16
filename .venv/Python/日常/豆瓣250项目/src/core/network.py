#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络测试模块
包含网络连接测试功能
"""

import requests
import time
from typing import Dict, List, Optional
from src.core.config import HEADERS, TIMEOUT, RETRY_DELAY, MAX_RETRIES


class NetworkTester:
    """网络测试器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def test_connection(self, url: str, timeout: int = TIMEOUT) -> Dict:
        """
        测试单个URL的连接
        
        Args:
            url: 测试的URL
            timeout: 超时时间
            
        Returns:
            Dict: 测试结果
        """
        result = {
            'url': url,
            'success': False,
            'status_code': None,
            'response_time': None,
            'error': None
        }
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=timeout)
            end_time = time.time()
            
            result['success'] = True
            result['status_code'] = response.status_code
            result['response_time'] = end_time - start_time
            
        except requests.exceptions.RequestException as e:
            result['error'] = str(e)
        
        return result
    
    def test_douban_connection(self) -> bool:
        """
        测试豆瓣连接
        
        Returns:
            bool: 连接是否成功
        """
        test_urls = [
            'https://movie.douban.com',
            'https://movie.douban.com/top250',
            'https://www.douban.com'
        ]
        
        for url in test_urls:
            result = self.test_connection(url)
            if result['success'] and result['status_code'] == 200:
                return True
        
        return False
    
    def test_multiple_urls(self, urls: List[str]) -> Dict:
        """
        测试多个URL的连接
        
        Args:
            urls: URL列表
            
        Returns:
            Dict: 测试结果统计
        """
        results = []
        success_count = 0
        total_time = 0
        
        for url in urls:
            result = self.test_connection(url)
            results.append(result)
            
            if result['success']:
                success_count += 1
                total_time += result['response_time']
        
        return {
            'results': results,
            'success_count': success_count,
            'total_count': len(urls),
            'success_rate': success_count / len(urls) if urls else 0,
            'average_time': total_time / success_count if success_count > 0 else 0
        }
    
    def ping_test(self, url: str, count: int = 3) -> Dict:
        """
        对URL进行ping测试
        
        Args:
            url: 测试的URL
            count: 测试次数
            
        Returns:
            Dict: ping测试结果
        """
        results = []
        success_count = 0
        total_time = 0
        
        for i in range(count):
            result = self.test_connection(url)
            results.append(result)
            
            if result['success']:
                success_count += 1
                total_time += result['response_time']
            
            if i < count - 1:  # 不是最后一次，等待一下
                time.sleep(0.5)
        
        return {
            'url': url,
            'results': results,
            'success_count': success_count,
            'total_count': count,
            'success_rate': success_count / count,
            'average_time': total_time / success_count if success_count > 0 else 0,
            'min_time': min(r['response_time'] for r in results if r['success']) if success_count > 0 else 0,
            'max_time': max(r['response_time'] for r in results if r['success']) if success_count > 0 else 0
        }
    
    def diagnose_network(self) -> Dict:
        """
        网络诊断
        
        Returns:
            Dict: 诊断结果
        """
        diagnosis = {
            'basic_connectivity': False,
            'douban_access': False,
            'dns_resolution': False,
            'recommendations': []
        }
        
        # 基本连接测试
        basic_test = self.test_connection('https://www.baidu.com')
        diagnosis['basic_connectivity'] = basic_test['success']
        
        if not diagnosis['basic_connectivity']:
            diagnosis['recommendations'].append('检查网络连接')
        
        # 豆瓣访问测试
        diagnosis['douban_access'] = self.test_douban_connection()
        
        if not diagnosis['douban_access']:
            diagnosis['recommendations'].append('豆瓣网站可能无法访问，检查防火墙设置')
        
        # DNS解析测试
        dns_test = self.test_connection('https://8.8.8.8')
        diagnosis['dns_resolution'] = dns_test['success']
        
        if not diagnosis['dns_resolution']:
            diagnosis['recommendations'].append('DNS解析可能有问题，尝试更换DNS服务器')
        
        return diagnosis
    
    def get_connection_info(self) -> Dict:
        """
        获取连接信息
        
        Returns:
            Dict: 连接信息
        """
        info = {
            'headers': dict(self.session.headers),
            'timeout': TIMEOUT,
            'retry_delay': RETRY_DELAY,
            'max_retries': MAX_RETRIES
        }
        
        return info
