#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络测试模块
负责测试网络连接状态
"""

import requests
import time
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import HEADERS, TIMEOUT, RETRY_DELAY, MAX_RETRIES, NETWORK_TEST_URLS
from utils import logger


class NetworkTester:
    """网络测试器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.test_urls = NETWORK_TEST_URLS
    
    def test_connection(self) -> Dict:
        """测试网络连接"""
        result = {
            'success': False,
            'message': '网络连接失败',
            'details': [],
            'speed': 0,
            'latency': 0
        }
        
        try:
            logger.info("开始网络连接测试")
            
            # 并发测试多个URL
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {executor.submit(self._test_url, url): url for url in self.test_urls}
                
                for future in as_completed(futures):
                    url = futures[future]
                    try:
                        test_result = future.result()
                        result['details'].append(test_result)
                        
                        # 如果有一个成功，就认为网络可用
                        if test_result['success']:
                            result['success'] = True
                            result['message'] = '网络连接正常'
                            result['latency'] = test_result['latency']
                            
                    except Exception as e:
                        logger.error(f"测试URL {url} 时发生错误: {e}")
                        result['details'].append({
                            'url': url,
                            'success': False,
                            'latency': 0,
                            'error': str(e)
                        })
            
            # 计算平均延迟
            successful_tests = [detail for detail in result['details'] if detail['success']]
            if successful_tests:
                result['latency'] = sum(detail['latency'] for detail in successful_tests) / len(successful_tests)
            
            logger.info(f"网络测试完成: {result['message']}")
            return result
            
        except Exception as e:
            logger.error(f"网络测试失败: {e}")
            result['message'] = f'网络测试失败: {e}'
            return result
    
    def _test_url(self, url: str) -> Dict:
        """测试单个URL"""
        result = {
            'url': url,
            'success': False,
            'latency': 0,
            'error': None
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                start_time = time.time()
                response = self.session.get(url, timeout=TIMEOUT)
                end_time = time.time()
                
                if response.status_code == 200:
                    result['success'] = True
                    result['latency'] = (end_time - start_time) * 1000  # 转换为毫秒
                    return result
                else:
                    result['error'] = f'HTTP {response.status_code}'
                    
            except requests.exceptions.Timeout:
                result['error'] = '请求超时'
            except requests.exceptions.ConnectionError:
                result['error'] = '连接错误'
            except Exception as e:
                result['error'] = str(e)
            
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
        
        return result
    
    def test_douban_access(self) -> bool:
        """测试豆瓣网站访问"""
        try:
            response = self.session.get('https://movie.douban.com/top250', timeout=TIMEOUT)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"豆瓣访问测试失败: {e}")
            return False
    
    def get_network_info(self) -> Dict:
        """获取网络信息"""
        info = {
            'connection_test': self.test_connection(),
            'douban_access': self.test_douban_access(),
            'dns_resolution': self._test_dns_resolution(),
            'proxy_status': self._check_proxy_status()
        }
        
        return info
    
    def _test_dns_resolution(self) -> bool:
        """测试DNS解析"""
        try:
            import socket
            socket.gethostbyname('www.douban.com')
            return True
        except Exception as e:
            logger.error(f"DNS解析测试失败: {e}")
            return False
    
    def _check_proxy_status(self) -> Dict:
        """检查代理状态"""
        return {
            'http_proxy': self.session.proxies.get('http'),
            'https_proxy': self.session.proxies.get('https'),
            'using_proxy': bool(self.session.proxies)
        }
    
    def diagnose_network_issues(self) -> List[str]:
        """诊断网络问题"""
        issues = []
        
        # 基本连接测试
        connection_result = self.test_connection()
        if not connection_result['success']:
            issues.append("无法连接到互联网")
        
        # DNS解析测试
        if not self._test_dns_resolution():
            issues.append("DNS解析失败")
        
        # 豆瓣访问测试
        if not self.test_douban_access():
            issues.append("无法访问豆瓣网站")
        
        # 延迟测试
        if connection_result['latency'] > 5000:  # 5秒
            issues.append("网络延迟过高")
        
        return issues
    
    def get_network_suggestions(self) -> List[str]:
        """获取网络建议"""
        suggestions = []
        issues = self.diagnose_network_issues()
        
        if "无法连接到互联网" in issues:
            suggestions.extend([
                "检查网络连接",
                "确认网络设置",
                "重启路由器"
            ])
        
        if "DNS解析失败" in issues:
            suggestions.extend([
                "更换DNS服务器",
                "清除DNS缓存",
                "检查防火墙设置"
            ])
        
        if "无法访问豆瓣网站" in issues:
            suggestions.extend([
                "检查是否被防火墙阻止",
                "尝试使用代理",
                "稍后再试"
            ])
        
        if "网络延迟过高" in issues:
            suggestions.extend([
                "检查网络质量",
                "关闭占用带宽的应用",
                "联系网络服务提供商"
            ])
        
        return suggestions
