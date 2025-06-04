import os

# 一个简单的实用程序：查询当前文件夹下所有文件和文件夹


def list_files_and_dirs(path='.'):
    print(f"列出路径: {os.path.abspath(path)} 下的所有文件和文件夹：")
    for item in os.listdir(path):
        print(item)

if __name__ == "__main__":
    list_files_and_dirs()