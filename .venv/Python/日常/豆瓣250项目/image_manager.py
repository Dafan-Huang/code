#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片处理模块
负责图片下载、缓存和处理
"""

import os
import requests
import threading
from io import BytesIO
from typing import Optional, Callable, Dict
from PIL import Image, ImageTk
import hashlib

from config import TIMEOUT, POSTER_CONFIG, CACHE_CONFIG
from utils import logger, ensure_dir, safe_execute


class ImageCache:
    """图片缓存管理器"""
    
    def __init__(self):
        self._cache: Dict[str, ImageTk.PhotoImage] = {}
        self._lock = threading.Lock()
        self.cache_dir = CACHE_CONFIG.get('dir', 'cache')
        ensure_dir(self.cache_dir)
    
    def get(self, key: str) -> Optional[ImageTk.PhotoImage]:
        """获取缓存图片"""
        with self._lock:
            return self._cache.get(key)
    
    def set(self, key: str, image: ImageTk.PhotoImage):
        """设置缓存图片"""
        with self._lock:
            # 如果缓存已满，删除最旧的条目
            if len(self._cache) >= POSTER_CONFIG.get('cache_size', 100):
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            
            self._cache[key] = image
    
    def clear(self):
        """清空缓存"""
        with self._lock:
            self._cache.clear()
    
    def get_cache_file_path(self, url: str) -> str:
        """获取缓存文件路径"""
        # 使用URL的MD5作为文件名
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{url_hash}.jpg")
    
    def save_to_disk(self, url: str, image_data: bytes):
        """保存图片到磁盘"""
        try:
            cache_file = self.get_cache_file_path(url)
            with open(cache_file, 'wb') as f:
                f.write(image_data)
            logger.debug(f"图片已保存到缓存: {cache_file}")
        except Exception as e:
            logger.error(f"保存图片缓存失败: {e}")
    
    def load_from_disk(self, url: str) -> Optional[bytes]:
        """从磁盘加载图片"""
        try:
            cache_file = self.get_cache_file_path(url)
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"从磁盘加载图片失败: {e}")
        return None


class PosterManager:
    """海报管理器"""
    
    def __init__(self):
        self.cache = ImageCache()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self._downloading = set()  # 正在下载的URL
        self._lock = threading.Lock()
    
    def get_poster(self, url: str, callback: Optional[Callable] = None) -> Optional[ImageTk.PhotoImage]:
        """获取海报图片"""
        if not url:
            return self._get_placeholder()
        
        # 先从内存缓存获取
        cached_image = self.cache.get(url)
        if cached_image:
            return cached_image
        
        # 异步下载
        if callback:
            self._download_async(url, callback)
        
        # 返回占位图片
        return self._get_placeholder()
    
    def _download_async(self, url: str, callback: Callable):
        """异步下载图片"""
        with self._lock:
            if url in self._downloading:
                return
            self._downloading.add(url)
        
        def download_worker():
            try:
                image = self._download_image(url)
                if image:
                    self.cache.set(url, image)
                    # 调用回调函数更新UI
                    if callback:
                        callback(url, image)
            except Exception as e:
                logger.error(f"异步下载图片失败 {url}: {e}")
            finally:
                with self._lock:
                    self._downloading.discard(url)
        
        thread = threading.Thread(target=download_worker, daemon=True)
        thread.start()
    
    def _download_image(self, url: str) -> Optional[ImageTk.PhotoImage]:
        """下载图片"""
        try:
            # 先尝试从磁盘缓存加载
            cached_data = self.cache.load_from_disk(url)
            if cached_data:
                return self._process_image_data(cached_data)
            
            # 从网络下载
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            
            image_data = response.content
            
            # 保存到磁盘缓存
            self.cache.save_to_disk(url, image_data)
            
            # 处理图片
            return self._process_image_data(image_data)
            
        except Exception as e:
            logger.error(f"下载图片失败 {url}: {e}")
            return None
    
    def _process_image_data(self, image_data: bytes) -> Optional[ImageTk.PhotoImage]:
        """处理图片数据"""
        try:
            # 打开图片
            image = Image.open(BytesIO(image_data))
            
            # 转换为RGB模式
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 调整大小
            target_size = (POSTER_CONFIG['width'], POSTER_CONFIG['height'])
            image = self._resize_image(image, target_size)
            
            # 转换为PhotoImage
            return ImageTk.PhotoImage(image)
            
        except Exception as e:
            logger.error(f"处理图片数据失败: {e}")
            return None
    
    def _resize_image(self, image: Image.Image, target_size: tuple) -> Image.Image:
        """调整图片大小"""
        try:
            # 计算缩放比例
            original_width, original_height = image.size
            target_width, target_height = target_size
            
            # 按比例缩放
            width_ratio = target_width / original_width
            height_ratio = target_height / original_height
            ratio = min(width_ratio, height_ratio)
            
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # 缩放图片
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 如果需要，在中心创建目标尺寸的图片
            if new_width != target_width or new_height != target_height:
                final_image = Image.new('RGB', target_size, POSTER_CONFIG.get('placeholder_color', '#e6e6e6'))
                
                # 计算粘贴位置
                paste_x = (target_width - new_width) // 2
                paste_y = (target_height - new_height) // 2
                
                final_image.paste(resized_image, (paste_x, paste_y))
                return final_image
            
            return resized_image
            
        except Exception as e:
            logger.error(f"调整图片大小失败: {e}")
            return image
    
    def _get_placeholder(self) -> ImageTk.PhotoImage:
        """获取占位图片"""
        try:
            # 创建占位图片
            placeholder = Image.new('RGB', 
                                  (POSTER_CONFIG['width'], POSTER_CONFIG['height']),
                                  POSTER_CONFIG.get('placeholder_color', '#e6e6e6'))
            
            return ImageTk.PhotoImage(placeholder)
            
        except Exception as e:
            logger.error(f"创建占位图片失败: {e}")
            # 返回一个最小的占位图片
            return ImageTk.PhotoImage(Image.new('RGB', (100, 100), '#e6e6e6'))
    
    def preload_images(self, urls: list, callback: Optional[Callable] = None):
        """预加载图片"""
        def preload_worker():
            for url in urls:
                if url and url not in self._downloading:
                    self._download_async(url, callback)
        
        thread = threading.Thread(target=preload_worker, daemon=True)
        thread.start()
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
        logger.info("图片缓存已清空")
    
    def get_cache_info(self) -> Dict:
        """获取缓存信息"""
        return {
            'memory_cache_size': len(self.cache._cache),
            'downloading_count': len(self._downloading),
            'cache_dir': self.cache.cache_dir
        }
