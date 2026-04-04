import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    # ===== 1) 读取数据 =====
    # 把 data.csv 换成你的文件名；如果是 Excel 用 read_excel
    # df = pd.read_excel("data.xlsx", sheet_name=0)
    df = pd.read_csv("data.csv", encoding="utf-8")

    print("\n=== 前 5 行 ===")
    print(df.head())

    print("\n=== 基本信息 ===")
    print(df.info())

    print("\n=== 各列缺失值数量 ===")
    print(df.isna().sum())

    # ===== 2) 数据清洗 =====
    # 2.1 去重
    df = df.drop_duplicates()

    # 2.2 缺失值处理（示例：数值列用中位数填充）
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # 2.3 字符串列去首尾空格（防止“看起来一样但实际不同”）
    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # ===== 3) 统计分析 =====
    print("\n=== 数值列描述统计 ===")
    print(df.describe())

    # 假设有一列分组列 group 和测量值 value，请按你的数据改列名
    if "group" in df.columns and "value" in df.columns:
        grouped = df.groupby("group")["value"].agg(["count", "mean", "std", "min", "max"])
        print("\n=== 分组统计(group vs value) ===")
        print(grouped)
        grouped.to_csv("group_summary.csv", encoding="utf-8-sig")
        print("\n已导出分组统计: group_summary.csv")

    # ===== 4) 可视化 =====
    # 下面示例依赖列名 value，如果没有该列请改成你的列名
    if "value" in df.columns:
        sns.set(style="whitegrid")

        plt.figure(figsize=(8, 5))
        sns.histplot(df["value"], kde=True)
        plt.title("Distribution of value")
        plt.xlabel("value")
        plt.ylabel("count")
        plt.tight_layout()
        plt.savefig("value_distribution.png", dpi=150)
        plt.close()

        plt.figure(figsize=(8, 5))
        sns.boxplot(x=df["value"])
        plt.title("Boxplot of value")
        plt.tight_layout()
        plt.savefig("value_boxplot.png", dpi=150)
        plt.close()

        print("已导出图片: value_distribution.png, value_boxplot.png")

    # ===== 5) 导出清洗后的数据 =====
    df.to_csv("cleaned_data.csv", index=False, encoding="utf-8-sig")
    print("\n已导出清洗后数据: cleaned_data.csv")


if __name__ == "__main__":
    main()
