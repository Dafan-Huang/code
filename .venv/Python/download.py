import requests

# # 生成以 0001, 0002, 0003 为规律的数列
# num_list = [f'{i:04d}' for i in range(1, 151)]

# # 定义要下载的文件 URL 列表
# for num in num_list:
#     url_list=['http://motions.cat/gif/tmb/'num'.gif']

# # 遍历 URL 列表，逐个下载文件
# for url in url_list:
#     # 发送 GET 请求，获取文件内容
#     response = requests.get(url)

#     # 获取文件名
#     filename = url.split('/')[-1]

#     # 保存文件到本地
#     with open(filename, 'wb') as f:
#         f.write(response.content)

# 生成以 0001, 0002, 0003 为规律的数列
num_list = [f'{i:04d}' for i in range(1, 151)]

# 定义要下载的文件 URL 列表
# http://motions.cat/gif/nhn/0001.gif
url_list = [f'http://motions.cat/gif/nhn/{num}.gif' for num in num_list]

# 遍历 URL 列表，逐个下载文件
for url in url_list:
    # 发送 GET 请求，获取文件内容
    response = requests.get(url)

    # 获取文件名
    filename = url.split('/')[-1]

    # 保存文件到本地
    with open(filename, 'wb') as f:
        f.write(response.content)