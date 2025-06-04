import os

def list_files_and_dirs(path='.'):
    abs_path = os.path.abspath(path)
    items = os.listdir(path)
    files = [f for f in items if os.path.isfile(os.path.join(path, f))]
    dirs = [d for d in items if os.path.isdir(os.path.join(path, d))]

    print(f"列出路径: {abs_path} 下的所有文件和文件夹：")
    for item in items:
        print(item)

    print(f"\n文件数量: {len(files)}")
    print(f"文件夹数量: {len(dirs)}")

    if files:
        print("\n文件列表:")
        for f in files:
            print(f"  {f}")
    if dirs:
        print("\n文件夹列表:")
        for d in dirs:
            print(f"  {d}")

if __name__ == "__main__":
    list_files_and_dirs()