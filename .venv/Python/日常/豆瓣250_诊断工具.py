#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣250程序诊断工具
用于检测和解决网络连接问题
"""

import requests
import sys
import time
from bs4 import BeautifulSoup

def test_basic_connection():
    """测试基本网络连接"""
    print("🔍 测试基本网络连接...")
    try:
        response = requests.get('https://httpbin.org/ip', timeout=5)
        if response.status_code == 200:
            print("✅ 基本网络连接正常")
            print(f"   IP信息: {response.json()}")
            return True
        else:
            print(f"❌ 基本网络连接异常，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 基本网络连接失败: {e}")
        return False

def test_douban_access():
    """测试豆瓣访问"""
    print("\n🔍 测试豆瓣网站访问...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    
    try:
        response = requests.get('https://movie.douban.com/top250', headers=headers, timeout=10)
        print(f"   状态码: {response.status_code}")
        print(f"   响应大小: {len(response.text)} 字符")
        
        if response.status_code == 200:
            print("✅ 豆瓣网站访问正常")
            
            # 测试页面解析
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('div', class_='item')
            print(f"   找到电影条目: {len(items)} 个")
            
            if len(items) > 0:
                print("✅ 页面解析正常")
                return True
            else:
                print("❌ 页面解析失败，可能遇到反爬虫")
                return False
        else:
            print(f"❌ 豆瓣网站访问异常")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时，网络连接缓慢")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误，无法访问豆瓣网站")
        return False
    except Exception as e:
        print(f"❌ 豆瓣访问失败: {e}")
        return False

def test_detailed_fetch():
    """测试详细的数据获取"""
    print("\n🔍 测试详细数据获取...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    success_count = 0
    
    for start in [0, 25, 50]:  # 测试前3页
        url = f'https://movie.douban.com/top250?start={start}'
        try:
            print(f"   测试第{start//25 + 1}页...")
            time.sleep(2)  # 增加延迟
            
            response = session.get(url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('div', class_='item')
                
                if items:
                    print(f"   ✅ 第{start//25 + 1}页成功，找到 {len(items)} 个电影")
                    success_count += 1
                else:
                    print(f"   ❌ 第{start//25 + 1}页解析失败")
            else:
                print(f"   ❌ 第{start//25 + 1}页请求失败，状态码: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 第{start//25 + 1}页异常: {e}")
    
    print(f"\n📊 测试结果: {success_count}/3 页成功")
    return success_count > 0

def suggest_solutions():
    """提供解决方案建议"""
    print("\n💡 解决方案建议:")
    print("1. 网络连接问题:")
    print("   - 检查网络连接是否正常")
    print("   - 尝试使用VPN或代理")
    print("   - 检查防火墙设置")
    
    print("\n2. 豆瓣反爬虫限制:")
    print("   - 增加请求延迟（已在代码中实现）")
    print("   - 使用不同的User-Agent")
    print("   - 分批获取数据")
    
    print("\n3. 程序使用建议:")
    print("   - 点击'测试网络'按钮检查连接")
    print("   - 如果网络正常但数据获取失败，程序会自动使用示例数据")
    print("   - 可以稍后重试获取真实数据")

def main():
    """主诊断函数"""
    print("🎬 豆瓣250程序诊断工具")
    print("=" * 50)
    
    # 测试基本连接
    basic_ok = test_basic_connection()
    
    # 测试豆瓣访问
    douban_ok = test_douban_access()
    
    # 测试详细获取
    fetch_ok = test_detailed_fetch()
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 诊断总结:")
    print(f"   基本网络连接: {'✅ 正常' if basic_ok else '❌ 异常'}")
    print(f"   豆瓣网站访问: {'✅ 正常' if douban_ok else '❌ 异常'}")
    print(f"   数据获取测试: {'✅ 正常' if fetch_ok else '❌ 异常'}")
    
    if basic_ok and douban_ok and fetch_ok:
        print("\n🎉 所有测试通过！程序应该能正常工作。")
    else:
        suggest_solutions()
    
    print("\n" + "=" * 50)
    print("现在可以运行豆瓣250程序了！")

if __name__ == '__main__':
    main()
    input("\n按回车键退出...")
