# 数学建模数据预处理工具
# 功能：数据清洗、缺失值处理、异常值检测、特征工程等

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class DataPreprocessor:
    def __init__(self, df):
        """
        初始化数据预处理器
        :param df: 输入的DataFrame
        """
        self.df = df.copy()
        self.original_df = df.copy()
        
    def basic_info(self):
        """显示数据基本信息"""
        print("=" * 50)
        print("数据基本信息")
        print("=" * 50)
        print(f"数据形状: {self.df.shape}")
        print(f"\n数据类型:")
        print(self.df.dtypes)
        print(f"\n缺失值统计:")
        print(self.df.isnull().sum())
        print(f"\n基本统计信息:")
        print(self.df.describe())
        
    def handle_missing_values(self, strategy='mean', columns=None):
        """
        处理缺失值
        :param strategy: 填充策略 ('mean', 'median', 'mode', 'constant', 'knn')
        :param columns: 指定列名列表，若为None则处理所有数值列
        """
        if columns is None:
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        else:
            numeric_columns = columns
            
        print(f"\n使用 {strategy} 策略处理缺失值...")
        
        if strategy == 'knn':
            imputer = KNNImputer(n_neighbors=5)
            self.df[numeric_columns] = imputer.fit_transform(self.df[numeric_columns])
        else:
            imputer = SimpleImputer(strategy=strategy)
            self.df[numeric_columns] = imputer.fit_transform(self.df[numeric_columns])
            
        print("缺失值处理完成")
        
    def detect_outliers(self, method='zscore', threshold=3):
        """
        检测异常值
        :param method: 检测方法 ('zscore', 'iqr')
        :param threshold: 阈值
        :return: 异常值的索引
        """
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        outliers_indices = []
        
        for col in numeric_columns:
            if method == 'zscore':
                z_scores = np.abs(stats.zscore(self.df[col].dropna()))
                outliers = np.where(z_scores > threshold)[0]
            elif method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)].index
            else:
                raise ValueError("方法必须是 'zscore' 或 'iqr'")
                
            outliers_indices.extend(outliers)
            
        return list(set(outliers_indices))
    
    def remove_outliers(self, method='zscore', threshold=3):
        """移除异常值"""
        outliers = self.detect_outliers(method, threshold)
        self.df = self.df.drop(outliers)
        print(f"移除了 {len(outliers)} 个异常值")
        
    def normalize_data(self, method='standard', columns=None):
        """
        数据标准化/归一化
        :param method: 'standard' (标准化) 或 'minmax' (归一化)
        :param columns: 指定列名列表
        """
        if columns is None:
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        else:
            numeric_columns = columns
            
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError("方法必须是 'standard' 或 'minmax'")
            
        self.df[numeric_columns] = scaler.fit_transform(self.df[numeric_columns])
        print(f"使用 {method} 方法完成数据标准化")
        
    def encode_categorical(self, columns=None):
        """
        编码分类变量
        :param columns: 指定分类列名列表
        """
        if columns is None:
            categorical_columns = self.df.select_dtypes(include=['object']).columns
        else:
            categorical_columns = columns
            
        le = LabelEncoder()
        for col in categorical_columns:
            self.df[col] = le.fit_transform(self.df[col].astype(str))
            
        print("分类变量编码完成")
        
    def feature_engineering(self, operations=None):
        """
        特征工程
        :param operations: 操作列表，如 ['polynomial', 'interaction', 'log']
        """
        if operations is None:
            operations = ['polynomial']
            
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        
        if 'polynomial' in operations:
            for col in numeric_columns:
                self.df[f'{col}_squared'] = self.df[col] ** 2
                self.df[f'{col}_sqrt'] = np.sqrt(np.abs(self.df[col]))
                
        if 'interaction' in operations and len(numeric_columns) >= 2:
            col1, col2 = numeric_columns[0], numeric_columns[1]
            self.df[f'{col1}_{col2}_interaction'] = self.df[col1] * self.df[col2]
            
        if 'log' in operations:
            for col in numeric_columns:
                if (self.df[col] > 0).all():
                    self.df[f'{col}_log'] = np.log(self.df[col])
                    
        print(f"完成特征工程: {operations}")
        
    def correlation_analysis(self):
        """相关性分析"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        correlation_matrix = numeric_df.corr()
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('特征相关性热力图')
        plt.tight_layout()
        plt.show()
        
        return correlation_matrix
        
    def save_processed_data(self, filename):
        """保存处理后的数据"""
        self.df.to_csv(filename, index=False)
        print(f"处理后的数据已保存到: {filename}")
        
    def get_processed_data(self):
        """获取处理后的数据"""
        return self.df

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
    
    # 创建预处理器实例
    preprocessor = DataPreprocessor(df)
    
    # 显示基本信息
    preprocessor.basic_info()
    
    # 处理缺失值
    preprocessor.handle_missing_values(strategy='mean')
    
    # 检测并处理异常值
    outliers = preprocessor.detect_outliers(method='iqr')
    print(f"检测到 {len(outliers)} 个异常值")
    
    # 数据标准化
    preprocessor.normalize_data(method='standard')
    
    # 编码分类变量
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        preprocessor.encode_categorical()
    
    # 特征工程
    preprocessor.feature_engineering(['polynomial'])
    
    # 相关性分析
    correlation_matrix = preprocessor.correlation_analysis()
    
    # 保存处理后的数据
    preprocessor.save_processed_data("processed_data.csv")
    
    print("\n数据预处理完成！")