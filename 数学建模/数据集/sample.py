# 随机生成参考数据并保存到 /d:/code/数学建模/数据集/test.xlsx
# 运行: python gen_sample_excel.py

import numpy as np
import pandas as pd
from pathlib import Path

# 配置
out_path = Path(r"d:/code/数学建模/数据集/test.xlsx")
out_path.parent.mkdir(parents=True, exist_ok=True)
n_rows = 100
random_seed = 42

np.random.seed(random_seed)

# 构造数据
df = pd.DataFrame({
    "样本ID": np.arange(1, n_rows + 1),
    "x1_正态(0,1)": np.random.normal(loc=0.0, scale=1.0, size=n_rows),
    "x2_均匀(0,10)": np.random.uniform(low=0.0, high=10.0, size=n_rows),
    "x3_整数(0-5)": np.random.randint(0, 6, size=n_rows),
    "类别": np.random.choice(["A", "B", "C"], size=n_rows, p=[0.5, 0.3, 0.2]),
    "日期": pd.date_range("2025-01-01", periods=n_rows, freq="D")
})

# 随机引入一些缺失值作为参考
nan_mask = np.random.rand(*df.shape) < 0.03  # 约3%缺失
df = df.mask(nan_mask)

# 保存到 Excel
df.to_excel(out_path, index=False)
print(f"已生成 {n_rows} 行参考数据并保存到: {out_path}")