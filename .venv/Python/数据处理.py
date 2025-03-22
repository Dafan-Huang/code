import pandas as pd
import numpy as np
from scipy.ndimage import convolve1d

# 读取原始数据
df = pd.read_excel(r"C:\Users\24096\Desktop\code\.venv\Python\衍射光强.xlsx")

# 定义高斯加权窗口（五点）
weights = np.array([0.1, 0.2, 0.4, 0.2, 0.1])
df["五点平滑光强"] = convolve1d(df["光强"], weights, mode="nearest")

# 导出文件
df.to_excel(r"衍射光强_深度平滑数据.xlsx", index=False)