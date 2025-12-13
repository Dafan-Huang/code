# 数学建模数据采集和上传工具

这个工具集可以自动从互联网抓取数据，并定时上传到GitHub仓库。

## 功能特性

- **数据采集**: 自动采集天气、股票、新闻、经济等多种类型的数据
- **自动上传**: 将采集的数据自动上传到GitHub仓库
- **定时任务**: 支持设置定时任务，自动执行数据采集和上传
- **跨平台**: 支持Windows、Linux和macOS系统

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 手动执行数据采集

```bash
python main.py collect
```

### 2. 手动上传数据到GitHub

```bash
python main.py upload
```

### 3. 运行完整流程（采集+上传）

```bash
python main.py run
```

### 4. 设置定时任务

```bash
python main.py schedule
```

这将创建以下定时任务：
- 数据采集：每天早上9点执行
- Git上传：每天晚上9点执行

### 5. 查看当前定时任务

```bash
python main.py list
```

### 6. 移除定时任务

```bash
python main.py remove
```

## 文件结构

```
工具脚本/
├── main.py              # 主控制脚本
├── data_collector.py    # 数据采集器
├── git_uploader.py      # Git上传器
├── schedule_manager.py  # 定时任务管理器
└── README.md           # 使用说明
```

## 配置说明

### 数据采集配置

在 `data_collector.py` 中可以配置：
- 数据采集类型
- 数据源API
- 输出目录
- 文件保留天数

### Git上传配置

在 `git_uploader.py` 中可以配置：
- 仓库路径
- 远程仓库名称
- 分支名称
- 提交信息格式

### 定时任务配置

在 `schedule_manager.py` 中可以配置：
- 任务执行时间
- 任务频率
- 日志输出位置

## 日志文件

程序运行时会生成以下日志文件：
- `main.log` - 主程序日志
- `data_collector.log` - 数据采集日志
- `git_uploader.log` - Git上传日志
- `schedule_manager.log` - 定时任务管理日志

## 注意事项

1. 首次使用前请确保：
   - 已安装所有依赖
   - Git仓库已正确配置
   - 有足够的权限创建定时任务

2. 数据采集使用的是模拟数据，实际使用时需要：
   - 申请相应的API密钥
   - 配置正确的API端点
   - 遵守API使用限制

3. 定时任务需要系统权限：
   - Windows: 需要管理员权限
   - Linux/macOS: 需要用户权限

## 故障排除

### 常见问题

1. **定时任务创建失败**
   - 检查是否有足够的权限
   - 确认系统支持定时任务功能

2. **Git上传失败**
   - 检查网络连接
   - 确认Git配置正确
   - 查看日志文件获取详细错误信息

3. **数据采集失败**
   - 检查API配置
   - 确认网络连接正常
   - 查看日志文件获取详细错误信息

### 获取帮助

如果遇到问题，请查看相应的日志文件，或使用 `--verbose` 参数获取详细输出：

```bash
python main.py run --verbose
```

## 扩展功能

### 添加新的数据源

1. 在 `DataCollector` 类中添加新的采集方法
2. 在 `collect_all_data` 方法中调用新方法
3. 配置相应的数据处理和保存逻辑

### 修改定时任务

1. 编辑 `schedule_manager.py` 中的时间配置
2. 重新运行 `python main.py remove` 移除旧任务
3. 运行 `python main.py schedule` 创建新任务

### 自定义Git配置

1. 修改 `git_uploader.py` 中的仓库配置
2. 调整提交信息和推送策略
3. 添加更多的Git操作（如标签、分支等）