import os
import time
import random
import requests
from tqdm import tqdm

save_dir = "EveoneCat"
os.makedirs(save_dir, exist_ok=True)

num_list = [f'{i:04d}' for i in range(1,168)]
url_list = [f'http://motions.cat/gif/nhn/{num}.gif' for num in num_list]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def download_with_retry(url, filename, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
        except requests.RequestException as e:
            if attempt < retries - 1:
                time.sleep(2 + random.random() * 2)
            else:
                print(f"Failed to download {url}: {e}")
    return False

for url in tqdm(url_list, desc="Downloading"):
    filename = os.path.join(save_dir, url.split('/')[-1])
    download_with_retry(url, filename)
    time.sleep(1 + random.random() * 2)  # 随机延迟1-3秒
