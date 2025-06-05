from pathlib import Path

def list_files_and_dirs(path='.', output_file='output.txt'):
    """
    递归列出所有文件和文件夹，并写入输出文件。
    """
    def walk_dir(p: Path, level=0, files=None, dirs=None, lines=None):
        if files is None: files = []
        if dirs is None: dirs = []
        if lines is None: lines = []
        items = sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        for item in items:
            prefix = '    ' * level
            if item.is_dir():
                lines.append(f"{prefix}📁 {item.name}/")
                dirs.append(item)
                walk_dir(item, level+1, files, dirs, lines)
            else:
                lines.append(f"{prefix}📄 {item.name}")
                files.append(item)
        return files, dirs, lines

    try:
        p = Path(path).resolve()
        if not p.exists():
            print(f"路径不存在: {p}")
            return

        files, dirs, lines = walk_dir(p)
        summary = [
            f"列出路径: {p} 下的所有文件和文件夹（递归）：",
            *lines,
            f"\n文件数量: {len(files)}",
            f"文件夹数量: {len(dirs)}"
        ]
        output_path = Path(output_file).resolve()
        output_path.write_text('\n'.join(summary) + '\n', encoding='utf-8')
        print(f"结果已写入到 {output_path}")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.txt'
    list_files_and_dirs(path, output_file)
