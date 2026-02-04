import os
import time
import random
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('download.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置参数
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(SCRIPT_DIR, "EveoneCat")
MAX_WORKERS = 5  # 并发下载线程数
CHUNK_SIZE = 8192  # 流式下载的块大小
RETRY_TIMES = 3  # 重试次数
TIMEOUT = 15  # 超时时间（秒）
DELAY_RANGE = (0.5, 1.5)  # 下载延迟范围（秒）

os.makedirs(SAVE_DIR, exist_ok=True)

# 生成URL列表
num_list = [f'{i:04d}' for i in range(1, 166)]
url_list = [f'http://motions.cat/gif/nhn/{num}.gif' for num in num_list]

# 创建会话对象，复用连接
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "image/gif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
})


def is_file_valid(filename, min_size=100):
    """检查文件是否已存在且有效"""
    if not os.path.exists(filename):
        return False
    file_size = os.path.getsize(filename)
    return file_size > min_size


def download_with_retry(url, filename, retries=RETRY_TIMES):
    """
    下载文件并支持重试
    
    Args:
        url: 下载链接
        filename: 保存文件名
        retries: 重试次数
    
    Returns:
        bool: 下载是否成功
    """
    # 跳过已下载的文件
    if is_file_valid(filename):
        logger.info(f"文件已存在，跳过: {os.path.basename(filename)}")
        return True
    
    for attempt in range(retries):
        try:
            # 使用流式下载，支持大文件
            response = session.get(url, timeout=TIMEOUT, stream=True)
            response.raise_for_status()
            
            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            
            # 下载到临时文件
            temp_filename = filename + '.tmp'
            with open(temp_filename, 'wb') as f:
                if total_size == 0:
                    f.write(response.content)
                else:
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
            
            # 验证下载的文件
            if is_file_valid(temp_filename):
                os.replace(temp_filename, filename)
                logger.debug(f"成功下载: {os.path.basename(filename)}")
                return True
            else:
                logger.warning(f"下载的文件无效: {os.path.basename(filename)}")
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                
        except requests.Timeout:
            logger.warning(f"下载超时 (尝试 {attempt + 1}/{retries}): {url}")
        except requests.RequestException as e:
            logger.warning(f"下载失败 (尝试 {attempt + 1}/{retries}): {url} - {str(e)}")
        except Exception as e:
            logger.error(f"未知错误: {url} - {str(e)}")
        
        # 重试前等待
        if attempt < retries - 1:
            wait_time = 2 + random.random() * 2
            time.sleep(wait_time)
        else:
            logger.error(f"下载失败，已达到最大重试次数: {url}")
            # 清理临时文件
            temp_filename = filename + '.tmp'
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    return False


def download_single(url):
    """下载单个文件的包装函数"""
    filename = os.path.join(SAVE_DIR, url.split('/')[-1])
    success = download_with_retry(url, filename)
    # 随机延迟，避免过于频繁的请求
    time.sleep(random.uniform(*DELAY_RANGE))
    return success, url


def download_sequential():
    """顺序下载模式"""
    logger.info(f"开始顺序下载 {len(url_list)} 个文件...")
    success_count = 0
    
    for url in tqdm(url_list, desc="下载进度", unit="文件"):
        filename = os.path.join(SAVE_DIR, url.split('/')[-1])
        if download_with_retry(url, filename):
            success_count += 1
        time.sleep(random.uniform(*DELAY_RANGE))
    
    logger.info(f"下载完成！成功: {success_count}/{len(url_list)}")
    return success_count


def download_concurrent():
    """并发下载模式"""
    logger.info(f"开始并发下载 {len(url_list)} 个文件 (线程数: {MAX_WORKERS})...")
    success_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_single, url): url for url in url_list}
        
        with tqdm(total=len(url_list), desc="下载进度", unit="文件") as pbar:
            for future in as_completed(futures):
                success, url = future.result()
                if success:
                    success_count += 1
                pbar.update(1)
    
    logger.info(f"下载完成！成功: {success_count}/{len(url_list)}")
    return success_count


if __name__ == "__main__":
    try:
        # 可以选择下载模式：顺序或并发
        # 并发模式速度更快，但可能对服务器造成更大压力
        mode = "concurrent"  # 可选: "sequential" 或 "concurrent"
        
        if mode == "concurrent":
            download_concurrent()
        else:
            download_sequential()
            
    except KeyboardInterrupt:
        logger.info("\n下载已被用户中断")
    except Exception as e:
        logger.error(f"程序出错: {str(e)}")
    finally:
        session.close()
        logger.info("程序结束")
