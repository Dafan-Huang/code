import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.ndimage import convolve1d

# 1. 加载数据并修正异常值
df = pd.read_excel(r"C:\Users\24096\Desktop\code\.venv\Python\衍射光强1.xlsx")  # Update with the full path to the file
df.loc[df["位置x"].between(31.5, 32.1), "光强Ia"] = 9  # 替换异常值

# 2. 五点高斯平滑
weights = np.array([0.1, 0.2, 0.4, 0.2, 0.1])
df["平滑光强"] = convolve1d(df["光强Ia"], weights, mode="nearest")

# 3. 定义理论模型
def theoretical_model(x, I0, a, x0, L=1.0, wavelength=632e-9):
    beta = np.pi * a * (x - x0) / (wavelength * L)
    with np.errstate(divide="ignore", invalid="ignore"):
        intensity = I0 * (np.sin(beta) / beta) ** 2
    intensity[np.isnan(intensity)] = I0  # 处理beta=0处的NaN
    return intensity

# 4. 数据归一化
df["实验归一化"] = df["平滑光强"] / df["平滑光强"].max()

# 5. 拟合理论模型
p0 = [1.0, 1e-4, 14.55]  # 初始参数：[I0, a (缝宽, m), x0 (中心位置)]
x_data = df["位置x"].values
y_data = df["实验归一化"].values
popt, pcov = curve_fit(theoretical_model, x_data, y_data, p0=p0)

# 6. 生成理论曲线
df["理论归一化"] = theoretical_model(x_data, *popt)

# 7. 保存修正后的数据
df.to_excel("修正后的衍射光强数据.xlsx", index=False)

# 8. 可视化对比
plt.figure(figsize=(10, 6))
plt.scatter(df["位置x"], df["实验归一化"], s=10, label="实验数据（平滑后）", color="blue")
plt.plot(df["位置x"], df["理论归一化"], "r--", linewidth=2, label="理论拟合")
plt.xlabel("位置x (mm)")
plt.ylabel("归一化光强")
plt.title("单缝衍射光强分布 - 实验 vs 理论")
plt.legend()
plt.grid(True)
plt.show()

# 输出拟合参数
print("拟合参数：")
print(f"I0 = {popt[0]:.2f}")
print(f"缝宽 a = {popt[1]*1e3:.2f} mm")
print(f"中心位置 x0 = {popt[2]:.2f} mm")