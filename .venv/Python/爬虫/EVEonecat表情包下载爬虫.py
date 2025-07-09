import os
import requests
from tqdm import tqdm

# 保存图片的文件夹
save_dir = "images"
os.makedirs(save_dir, exist_ok=True)

# 生成以 0001, 0002, 0003 为规律的数列
num_list = [f'{i:04d}' for i in range(1, 151)]

# 定义要下载的文件 URL 列表
url_list = [f'http://motions.cat/gif/nhn/{num}.gif' for num in num_list]

# 遍历 URL 列表，逐个下载文件
for url in tqdm(url_list, desc="Downloading"):
    filename = os.path.join(save_dir, url.split('/')[-1])
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
