#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣Top250数据抓取模块
负责从豆瓣网站获取电影数据
"""

import requests
import time
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from .config import HEADERS, REQUEST_DELAY, TIMEOUT


class DoubanDataFetcher:
    """豆瓣数据抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._cache = {}  # 添加缓存
    
    def get_movies(self) -> List[Dict]:
        """
        获取电影列表 (对外接口)
        
        Returns:
            List[Dict]: 电影信息列表
        """
        try:
            # 先尝试从缓存获取
            if 'movies' in self._cache:
                return self._cache['movies']
            
            # 从网络获取
            movies = self.fetch_top250()
            
            # 如果网络获取失败，返回备用数据
            if not movies:
                from .config import BACKUP_MOVIES
                movies = self._convert_backup_data(BACKUP_MOVIES)
            
            # 缓存数据
            self._cache['movies'] = movies
            return movies
            
        except Exception as e:
            print(f"获取电影数据失败: {e}")
            # 返回备用数据
            from .config import BACKUP_MOVIES
            return self._convert_backup_data(BACKUP_MOVIES)
    
    def clear_cache(self):
        """清除缓存"""
        self._cache.clear()
    
    def _convert_backup_data(self, backup_data: List[Dict]) -> List[Dict]:
        """
        转换备用数据格式
        
        Args:
            backup_data: 备用数据
            
        Returns:
            List[Dict]: 转换后的电影数据
        """
        converted_movies = []
        for i, movie in enumerate(backup_data):
            converted_movie = {
                'rank': i + 1,
                'title': movie['title'],
                'rating': movie['rating'],
                'poster': movie['img_url'],
                'link': movie['detail_url'],
                'description': movie.get('quote', ''),
                'year': '经典',
                'genre': '剧情',
                'director': movie.get('info', '').split('主演')[0].replace('导演:', '').strip(),
                'actors': movie.get('info', '').split('主演:')[1].strip() if '主演:' in movie.get('info', '') else '未知'
            }
            converted_movies.append(converted_movie)
        return converted_movies
        
    def fetch_top250(self) -> List[Dict]:
        """
        获取豆瓣电影Top250列表
        
        Returns:
            List[Dict]: 电影信息列表
        """
        movies = []
        
        for start in range(0, 250, 25):
            page_movies = self._fetch_page(start)
            if page_movies:
                movies.extend(page_movies)
                
        print(f"总共获取到 {len(movies)} 部电影")
        return movies
    
    def _fetch_page(self, start: int) -> Optional[List[Dict]]:
        """
        获取单页数据
        
        Args:
            start: 起始位置
            
        Returns:
            Optional[List[Dict]]: 电影信息列表或None
        """
        url = f'https://movie.douban.com/top250?start={start}'
        page_num = start // 25 + 1
        
        try:
            print(f"正在获取第{page_num}页数据...")
            
            # 添加延迟避免请求过快
            time.sleep(REQUEST_DELAY)
            
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            
            # 检查响应内容
            if not response.text or len(response.text) < 1000:
                print(f"第{page_num}页响应内容异常，跳过")
                return None
                
            return self._parse_page(response.text, page_num)
            
        except requests.exceptions.RequestException as e:
            print(f"获取第{page_num}页网络请求失败: {e}")
            return None
        except Exception as e:
            print(f"获取第{page_num}页数据失败: {e}")
            return None
    
    def _parse_page(self, html: str, page_num: int) -> List[Dict]:
        """
        解析页面HTML
        
        Args:
            html: 页面HTML内容
            page_num: 页码
            
        Returns:
            List[Dict]: 解析出的电影信息
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        if not soup:
            print(f"第{page_num}页BeautifulSoup解析失败")
            return []
            
        # 查找电影列表容器
        ol = soup.find('ol', class_='grid_view')
        if not ol:
            print(f"第{page_num}页未找到电影列表容器")
            return []
            
        # 查找电影项目
        items = ol.find_all('li')
        
        if not items:
            print(f"第{page_num}页未找到电影项目")
            return []
            
        print(f"第{page_num}页找到 {len(items)} 个电影项目")
        
        movies = []
        for item in items:
            movie_data = self._parse_movie_item(item)
            if movie_data:
                movies.append(movie_data)
                
        return movies
    
    def _parse_movie_item(self, item) -> Optional[Dict]:
        """
        解析单个电影项目
        
        Args:
            item: BeautifulSoup元素 (li元素)
            
        Returns:
            Optional[Dict]: 电影信息或None
        """
        try:
            # 找到item div
            item_div = item.find('div', class_='item')
            if not item_div:
                return None
            
            # 排名
            rank_em = item_div.find('em')
            rank = rank_em.text.strip() if rank_em else '0'
            
            # 标题
            title_tag = item_div.find('span', class_='title')
            if not title_tag:
                return None
            title = title_tag.text.strip()
            
            # 评分
            rating_tag = item_div.find('span', class_='rating_num')
            if not rating_tag:
                return None
            rating = rating_tag.text.strip()
            
            # 海报图片
            img_tag = item_div.find('img')
            poster = img_tag.get('src', '') if img_tag else ''
            
            # 详情页链接
            detail_link = item_div.find('a')
            link = detail_link['href'] if detail_link else ''
            
            # 基本信息 (导演、主演、年份等)
            info_tag = item_div.find('p', class_='')
            info = info_tag.text.strip() if info_tag else ''
            
            # 解析年份
            year = '未知'
            if info:
                import re
                year_match = re.search(r'(\d{4})', info)
                if year_match:
                    year = year_match.group(1)
            
            # 解析导演
            director = '未知'
            if info and '导演:' in info:
                director_match = re.search(r'导演:\s*([^主]*)', info)
                if director_match:
                    director = director_match.group(1).strip()
            
            # 解析主演
            actors = '未知'
            if info and '主演:' in info:
                actors_match = re.search(r'主演:\s*(.+)', info)
                if actors_match:
                    actors = actors_match.group(1).strip()
            
            # 电影简介/评语
            quote_tag = item_div.find('span', class_='inq')
            description = quote_tag.text.strip() if quote_tag else ''
            
            # 评分人数
            rating_people = self._extract_rating_people(item_div)
            
            return {
                'rank': int(rank),
                'title': title,
                'rating': rating,
                'poster': poster,
                'link': link,
                'year': year,
                'director': director,
                'actors': actors,
                'description': description,
                'genre': '剧情',  # 默认类型
                'rating_people': rating_people
            }
            
        except Exception as e:
            print(f"解析电影项目失败: {e}")
            return None
    
    def _extract_rating_people(self, item) -> str:
        """
        提取评分人数
        
        Args:
            item: BeautifulSoup元素
            
        Returns:
            str: 评分人数
        """
        try:
            star_div = item.find('div', class_='star')
            if star_div:
                rating_people_tags = star_div.find_all('span')
                if len(rating_people_tags) > 3:
                    return rating_people_tags[3].text.strip()
        except Exception:
            pass
        return ''
    
    def fetch_movie_details(self, detail_url: str) -> Dict:
        """
        获取电影详细信息
        
        Args:
            detail_url: 详情页URL
            
        Returns:
            Dict: 详细信息
        """
        try:
            if not detail_url:
                return {'error': '暂无详细信息链接'}
                
            response = self.session.get(detail_url, timeout=TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            details = {}
            
            # 导演信息
            director = self._extract_info_by_label(soup, '导演')
            if director:
                details['director'] = director
                
            # 主演信息
            actors = self._extract_info_by_label(soup, '主演')
            if actors:
                details['actors'] = actors
                
            # 类型
            genre = self._extract_info_by_label(soup, '类型:')
            if genre:
                details['genre'] = genre
                
            # 制片国家/地区
            country = self._extract_info_by_text(soup, '制片国家/地区:')
            if country:
                details['country'] = country
                
            # 上映日期
            release_date = self._extract_info_by_label(soup, '上映日期:')
            if release_date:
                details['release_date'] = release_date
                
            # 片长
            duration = self._extract_info_by_text(soup, '片长:')
            if duration:
                details['duration'] = duration
                
            # 剧情简介
            summary = self._extract_summary(soup)
            if summary:
                details['summary'] = summary
                
            return details
            
        except Exception as e:
            return {'error': f'获取详细信息失败: {str(e)}'}
    
    def _extract_info_by_label(self, soup, label: str) -> Optional[str]:
        """通过标签提取信息"""
        try:
            info_span = soup.find('span', text=label)
            if info_span:
                attrs = info_span.find_next_sibling('span', class_='attrs')
                if attrs:
                    return attrs.get_text().strip()
        except Exception:
            pass
        return None
    
    def _extract_info_by_text(self, soup, text: str) -> Optional[str]:
        """通过文本提取信息"""
        try:
            info_span = soup.find('span', text=text)
            if info_span:
                sibling = info_span.next_sibling
                if sibling:
                    return sibling.strip()
        except Exception:
            pass
        return None
    
    def _extract_summary(self, soup) -> Optional[str]:
        """提取剧情简介"""
        try:
            summary_div = soup.find('div', id='link-report')
            if summary_div:
                summary_span = summary_div.find('span', class_='all')
                if not summary_span:
                    summary_span = summary_div.find('span', property='v:summary')
                if summary_span:
                    return summary_span.get_text().strip()
        except Exception:
            pass
        return None
