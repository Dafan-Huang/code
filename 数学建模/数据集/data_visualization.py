# 数学建模数据可视化工具
# 功能：提供多种数据可视化方法，帮助理解数据分布和关系

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class DataVisualizer:
    def __init__(self, df):
        """
        初始化数据可视化器
        :param df: 输入的DataFrame
        """
        self.df = df.copy()
        
    def basic_distribution_plot(self, columns=None):
        """
        绘制基本分布图
        :param columns: 指定列名列表，若为None则绘制所有数值列
        """
        if columns is None:
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        else:
            numeric_columns = columns
            
        n_cols = len(numeric_columns)
        n_rows = (n_cols + 2) // 3  # 每行3个图
        
        plt.figure(figsize=(15, 5 * n_rows))
        
        for i, col in enumerate(numeric_columns):
            plt.subplot(n_rows, 3, i + 1)
            
            # 直方图
            plt.hist(self.df[col].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            plt.title(f'{col} 分布')
            plt.xlabel(col)
            plt.ylabel('频数')
            plt.grid(True, alpha=0.3)
            
        plt.tight_layout()
        plt.show()
        
    def box_plot(self, columns=None):
        """
        绘制箱线图
        :param columns: 指定列名列表
        """
        if columns is None:
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        else:
            numeric_columns = columns
            
        plt.figure(figsize=(12, 6))
        self.df[numeric_columns].boxplot()
        plt.title('箱线图 - 异常值检测')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
    def scatter_plot_matrix(self, columns=None, sample_size=1000):
        """
        绘制散点图矩阵
        :param columns: 指定列名列表
        :param sample_size: 采样大小，避免数据量过大
        """
        if columns is None:
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns[:4]  # 限制列数
        else:
            numeric_columns = columns
            
        # 如果数据量太大，进行采样
        if len(self.df) > sample_size:
            plot_df = self.df[numeric_columns].sample(n=sample_size, random_state=42)
        else:
            plot_df = self.df[numeric_columns]
            
        pd.plotting.scatter_matrix(plot_df, figsize=(12, 12), alpha=0.6, diagonal='hist')
        plt.suptitle('散点图矩阵')
        plt.tight_layout()
        plt.show()
        
    def correlation_heatmap(self, columns=None):
        """
        绘制相关性热力图
        :param columns: 指定列名列表
        """
        if columns is None:
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        else:
            numeric_columns = columns
            
        correlation_matrix = self.df[numeric_columns].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                    square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
        plt.title('特征相关性热力图')
        plt.tight_layout()
        plt.show()
        
        return correlation_matrix
        
    def time_series_plot(self, time_col, value_cols):
        """
        绘制时间序列图
        :param time_col: 时间列名
        :param value_cols: 数值列名列表
        """
        if time_col not in self.df.columns:
            print(f"错误：找不到时间列 '{time_col}'")
            return
            
        plt.figure(figsize=(15, 8))
        
        for col in value_cols:
            if col in self.df.columns:
                plt.plot(self.df[time_col], self.df[col], label=col, marker='o', markersize=3)
                
        plt.title('时间序列图')
        plt.xlabel('时间')
        plt.ylabel('数值')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
    def categorical_plot(self, cat_col, value_col=None):
        """
        绘制分类变量图
        :param cat_col: 分类列名
        :param value_col: 数值列名（可选）
        """
        if cat_col not in self.df.columns:
            print(f"错误：找不到分类列 '{cat_col}'")
            return
            
        plt.figure(figsize=(12, 6))
        
        if value_col and value_col in self.df.columns:
            # 箱线图
            sns.boxplot(x=cat_col, y=value_col, data=self.df)
            plt.title(f'{cat_col} vs {value_col}')
        else:
            # 计数图
            self.df[cat_col].value_counts().plot(kind='bar')
            plt.title(f'{cat_col} 分布')
            
        plt.xlabel(cat_col)
        plt.ylabel(value_col if value_col else '频数')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
    def pair_plot(self, columns=None, hue=None):
        """
        绘制配对图
        :param columns: 指定列名列表
        :param hue: 分类变量列名
        """
        if columns is None:
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns[:4]  # 限制列数
        else:
            numeric_columns = columns
            
        plot_df = self.df[list(numeric_columns) + ([hue] if hue else [])]
        
        # 如果数据量太大，进行采样
        if len(plot_df) > 500:
            plot_df = plot_df.sample(n=500, random_state=42)
            
        sns.pairplot(plot_df, hue=hue, diag_kind='hist')
        plt.suptitle('配对图', y=1.02)
        plt.tight_layout()
        plt.show()
        
    def violin_plot(self, cat_col, value_col):
        """
        绘制小提琴图
        :param cat_col: 分类列名
        :param value_col: 数值列名
        """
        if cat_col not in self.df.columns or value_col not in self.df.columns:
            print(f"错误：找不到指定的列")
            return
            
        plt.figure(figsize=(10, 6))
        sns.violinplot(x=cat_col, y=value_col, data=self.df)
        plt.title(f'{cat_col} vs {value_col} 小提琴图')
        plt.xlabel(cat_col)
        plt.ylabel(value_col)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
    def missing_values_plot(self):
        """绘制缺失值可视化图"""
        missing_data = self.df.isnull().sum()
        missing_percentage = (missing_data / len(self.df)) * 100
        
        plt.figure(figsize=(12, 6))
        
        # 条形图
        plt.subplot(1, 2, 1)
        missing_data[missing_data > 0].plot(kind='bar')
        plt.title('缺失值数量')
        plt.xlabel('列名')
        plt.ylabel('缺失值数量')
        plt.xticks(rotation=45)
        
        # 热力图
        plt.subplot(1, 2, 2)
        sns.heatmap(self.df.isnull(), yticklabels=False, cbar=True, cmap='viridis')
        plt.title('缺失值热力图')
        
        plt.tight_layout()
        plt.show()
        
    def save_plots(self, filename_prefix):
        """
        保存当前图形
        :param filename_prefix: 文件名前缀
        """
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        plt.savefig(f"{filename_prefix}_{timestamp}.png", dpi=300, bbox_inches='tight')
        print(f"图形已保存为: {filename_prefix}_{timestamp}.png")

# 示例使用
if __name__ == "__main__":
    # 读取示例数据
    try:
        df = pd.read_excel("test.xlsx")
        print("成功读取test.xlsx文件")
    except:
        print("未找到test.xlsx，生成示例数据...")
        exec(open('sample.py').read())
        df = pd.read_excel("test.xlsx")
    
    # 创建可视化器实例
    visualizer = DataVisualizer(df)
    
    # 基本分布图
    print("绘制基本分布图...")
    visualizer.basic_distribution_plot()
    
    # 箱线图
    print("绘制箱线图...")
    visualizer.box_plot()
    
    # 相关性热力图
    print("绘制相关性热力图...")
    visualizer.correlation_heatmap()
    
    # 分类变量图
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        print("绘制分类变量图...")
        visualizer.categorical_plot(categorical_cols[0])
    
    # 时间序列图（如果有日期列）
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0:
        numeric_cols = df.select_dtypes(include=[np.number]).columns[:2]  # 取前两个数值列
        print("绘制时间序列图...")
        visualizer.time_series_plot(date_cols[0], numeric_cols)
    
    # 缺失值可视化
    print("绘制缺失值可视化图...")
    visualizer.missing_values_plot()
    
    # 散点图矩阵（限制列数避免图形过大）
    numeric_cols = df.select_dtypes(include=[np.number]).columns[:4]
    print("绘制散点图矩阵...")
    visualizer.scatter_plot_matrix(numeric_cols)
    
    print("\n数据可视化完成！")