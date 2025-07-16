#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣数据获取模块
负责从豆瓣网站获取电影数据
"""

import requests
import time
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import random

from config import HEADERS, REQUEST_DELAY, TIMEOUT, DOUBAN_URLS, BACKUP_MOVIES, MAX_RETRIES, RETRY_DELAY
from utils import logger, safe_execute


class DoubanDataFetcher:
    """豆瓣数据抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._cache = {}
    
    def get_movies(self) -> List[Dict]:
        """获取电影列表"""
        try:
            # 先尝试从缓存获取
            if 'movies' in self._cache:
                logger.info("从缓存获取电影数据")
                return self._cache['movies']
            
            # 从网络获取
            logger.info("开始从网络获取电影数据")
            movies = self._fetch_from_network()
            
            # 如果网络获取失败，返回备用数据
            if not movies:
                logger.warning("网络获取失败，使用备用数据")
                movies = self._get_backup_movies()
            
            # 缓存数据
            self._cache['movies'] = movies
            logger.info(f"成功获取 {len(movies)} 部电影数据")
            return movies
            
        except Exception as e:
            logger.error(f"获取电影数据失败: {e}")
            return self._get_backup_movies()
    
    def _fetch_from_network(self) -> List[Dict]:
        """从网络获取数据"""
        movies = []
        
        # 获取多页数据
        for page in range(0, 250, 25):  # 豆瓣Top250分10页
            try:
                url = f"{DOUBAN_URLS['base']}?start={page}"
                page_movies = self._fetch_page(url)
                
                if page_movies:
                    movies.extend(page_movies)
                    logger.info(f"成功获取第 {page//25 + 1} 页数据，共 {len(page_movies)} 部电影")
                    
                    # 添加延迟避免被封
                    time.sleep(REQUEST_DELAY + random.uniform(0.5, 1.5))
                else:
                    logger.warning(f"第 {page//25 + 1} 页数据获取失败")
                    
            except Exception as e:
                logger.error(f"获取第 {page//25 + 1} 页数据时发生错误: {e}")
                continue
        
        return movies
    
    def _fetch_page(self, url: str) -> List[Dict]:
        """获取单页数据"""
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=TIMEOUT)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                movies = self._parse_movies(soup)
                
                if movies:
                    return movies
                else:
                    logger.warning(f"页面解析失败，重试 {attempt + 1}/{MAX_RETRIES}")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"网络请求失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    
            except Exception as e:
                logger.error(f"页面解析错误 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        
        return []
    
    def _parse_movies(self, soup: BeautifulSoup) -> List[Dict]:
        """解析电影数据"""
        movies = []
        
        try:
            # 查找电影条目
            movie_items = soup.find_all('div', class_='item')
            
            for item in movie_items:
                try:
                    movie = self._parse_movie_item(item)
                    if movie:
                        movies.append(movie)
                except Exception as e:
                    logger.error(f"解析电影条目失败: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"解析电影列表失败: {e}")
        
        return movies
    
    def _parse_movie_item(self, item) -> Dict:
        """解析单个电影条目"""
        movie = {}
        
        try:
            # 排名
            rank_elem = item.find('div', class_='pic').find('em')
            movie['rank'] = int(rank_elem.text) if rank_elem else 0
            
            # 海报
            img_elem = item.find('div', class_='pic').find('img')
            movie['poster'] = img_elem.get('src') if img_elem else ''
            
            # 详情链接
            link_elem = item.find('div', class_='pic').find('a')
            movie['detail_url'] = link_elem.get('href') if link_elem else ''
            
            # 信息区域
            info_elem = item.find('div', class_='info')
            if info_elem:
                # 标题
                title_elem = info_elem.find('div', class_='hd').find('a')
                if title_elem:
                    title_spans = title_elem.find_all('span', class_='title')
                    movie['title'] = title_spans[0].text if title_spans else ''
                
                # 基本信息
                bd_elem = info_elem.find('div', class_='bd')
                if bd_elem:
                    # 导演、演员等信息
                    info_text = bd_elem.find('p', class_='').text if bd_elem.find('p', class_='') else ''
                    movie.update(self._parse_movie_info(info_text))
                    
                    # 评分
                    star_elem = bd_elem.find('div', class_='star')
                    if star_elem:
                        rating_elem = star_elem.find('span', class_='rating_num')
                        movie['score'] = rating_elem.text if rating_elem else '0.0'
                    
                    # 评价人数
                    people_elem = bd_elem.find('span', string=re.compile(r'人评价'))
                    if people_elem:
                        movie['rating_count'] = people_elem.text
                    
                    # 经典台词
                    quote_elem = bd_elem.find('span', class_='inq')
                    movie['quote'] = quote_elem.text if quote_elem else ''
            
            return movie
            
        except Exception as e:
            logger.error(f"解析电影条目详情失败: {e}")
            return {}
    
    def _parse_movie_info(self, info_text: str) -> Dict:
        """解析电影基本信息"""
        info = {}
        
        try:
            # 分割信息行
            lines = info_text.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 导演信息
                if line.startswith('导演:'):
                    info['director'] = line.replace('导演:', '').strip()
                
                # 主演信息
                elif line.startswith('主演:'):
                    actors_str = line.replace('主演:', '').strip()
                    info['actors'] = [actor.strip() for actor in actors_str.split('/') if actor.strip()]
                
                # 年份、国家、类型信息
                elif re.match(r'^\d{4}', line):
                    # 使用正则表达式解析
                    parts = line.split('/')
                    if len(parts) >= 3:
                        info['year'] = parts[0].strip()
                        info['country'] = parts[1].strip()
                        info['genre'] = parts[2].strip()
                    elif len(parts) == 2:
                        info['year'] = parts[0].strip()
                        info['genre'] = parts[1].strip()
                    else:
                        info['year'] = parts[0].strip()
        
        except Exception as e:
            logger.error(f"解析电影信息失败: {e}")
        
        return info
    
    def _get_backup_movies(self) -> List[Dict]:
        """获取备用电影数据"""
        logger.info("使用备用电影数据")
        return BACKUP_MOVIES.copy()
    
    def get_movie_detail(self, movie_id: str) -> Dict:
        """获取电影详情"""
        try:
            if movie_id in self._cache:
                return self._cache[movie_id]
            
            url = f"{DOUBAN_URLS['detail_base']}{movie_id}/"
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            detail = self._parse_movie_detail(soup)
            
            # 缓存详情
            self._cache[movie_id] = detail
            return detail
            
        except Exception as e:
            logger.error(f"获取电影详情失败 {movie_id}: {e}")
            return {}
    
    def _parse_movie_detail(self, soup: BeautifulSoup) -> Dict:
        """解析电影详情"""
        detail = {}
        
        try:
            # 简介
            summary_elem = soup.find('span', property='v:summary')
            if summary_elem:
                detail['description'] = summary_elem.text.strip()
            
            # 其他详细信息可以根据需要添加
            
        except Exception as e:
            logger.error(f"解析电影详情失败: {e}")
        
        return detail
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
        logger.info("缓存已清空")
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            response = self.session.get(DOUBAN_URLS['base'], timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"连接测试失败: {e}")
            return False
