#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片处理工具模块
包含图片缓存、加载和处理功能
"""

import requests
import io
import threading
from typing import Optional, Callable, Dict
from PIL import Image, ImageTk
from src.core.config import TIMEOUT, POSTER_CONFIG


class ImageCache:
    """图片缓存管理器"""
    
    def __init__(self):
        self._cache: Dict[str, ImageTk.PhotoImage] = {}
        self._lock = threading.Lock()
    
    def get(self, url: str) -> Optional[ImageTk.PhotoImage]:
        """
        获取缓存的图片
        
        Args:
            url: 图片URL
            
        Returns:
            Optional[ImageTk.PhotoImage]: 缓存的图片或None
        """
        with self._lock:
            return self._cache.get(url)
    
    def set(self, url: str, image: ImageTk.PhotoImage) -> None:
        """
        设置缓存的图片
        
        Args:
            url: 图片URL
            image: 图片对象
        """
        with self._lock:
            self._cache[url] = image
    
    def clear(self) -> None:
        """清除所有缓存"""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """获取缓存大小"""
        with self._lock:
            return len(self._cache)


class ImageLoader:
    """图片加载器"""
    
    def __init__(self, cache: ImageCache):
        self.cache = cache
    
    def load_async(self, url: str, size: tuple, callback: Callable, error_callback: Callable = None) -> None:
        """
        异步加载图片
        
        Args:
            url: 图片URL
            size: 目标尺寸 (width, height)
            callback: 成功回调函数
            error_callback: 错误回调函数
        """
        def load_task():
            try:
                # 检查缓存
                cached_image = self.cache.get(url)
                if cached_image:
                    callback(cached_image)
                    return
                
                # 下载图片
                response = requests.get(url, timeout=TIMEOUT)
                response.raise_for_status()
                
                # 处理图片
                image = Image.open(io.BytesIO(response.content))
                image = image.resize(size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # 缓存图片
                self.cache.set(url, photo)
                
                # 回调
                callback(photo)
                
            except Exception as e:
                if error_callback:
                    error_callback(e)
                else:
                    print(f"图片加载失败: {e}")
        
        threading.Thread(target=load_task, daemon=True).start()


class PosterManager:
    """海报管理器"""
    
    def __init__(self):
        self.cache = ImageCache()
        self.loader = ImageLoader(self.cache)
    
    def load_hover_poster(self, url: str, callback: Callable, error_callback: Callable = None) -> None:
        """
        加载悬停海报
        
        Args:
            url: 图片URL
            callback: 成功回调函数
            error_callback: 错误回调函数
        """
        self.loader.load_async(url, POSTER_CONFIG['hover_size'], callback, error_callback)
    
    def load_detail_poster(self, url: str, callback: Callable, error_callback: Callable = None) -> None:
        """
        加载详情海报
        
        Args:
            url: 图片URL
            callback: 成功回调函数
            error_callback: 错误回调函数
        """
        self.loader.load_async(url, POSTER_CONFIG['detail_size'], callback, error_callback)
    
    def clear_cache(self) -> None:
        """清除缓存"""
        self.cache.clear()
    
    def get_cache_info(self) -> Dict:
        """获取缓存信息"""
        return {
            'size': self.cache.size(),
            'hover_size': POSTER_CONFIG['hover_size'],
            'detail_size': POSTER_CONFIG['detail_size']
        }
