#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人财务管理系统
Personal Finance Manager

主要功能：
1. 收支记录
2. 分类管理
3. 数据统计
4. 图表展示
5. 预算管理
6. 数据导出

作者：GitHub Copilot
版本：1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from collections import defaultdict
import csv

# 配置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

class FinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("个人财务管理系统")
        self.root.geometry("1000x700")
        
        # 数据库文件
        self.db_file = "finance.db"
        self.init_database()
        
        # 创建界面
        self.create_widgets()
        
        # 加载数据
        self.refresh_data()
        
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # 创建交易记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建预算表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                month TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建标签页
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 记账页面
        self.create_record_tab(notebook)
        
        # 统计页面
        self.create_statistics_tab(notebook)
        
        # 预算页面
        self.create_budget_tab(notebook)
        
        # 设置页面
        self.create_settings_tab(notebook)
        
    def create_record_tab(self, notebook):
        """创建记账页面"""
        record_frame = ttk.Frame(notebook)
        notebook.add(record_frame, text="记账")
        
        # 左侧：输入区域
        left_frame = ttk.Frame(record_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 输入表单
        ttk.Label(left_frame, text="添加交易记录", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # 日期选择
        ttk.Label(left_frame, text="日期:").pack(anchor=tk.W)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(left_frame, textvariable=self.date_var, width=20).pack(pady=(0, 10))
        
        # 类型选择
        ttk.Label(left_frame, text="类型:").pack(anchor=tk.W)
        self.type_var = tk.StringVar(value="支出")
        type_combo = ttk.Combobox(left_frame, textvariable=self.type_var, 
                                 values=["收入", "支出"], width=17, state="readonly")
        type_combo.pack(pady=(0, 10))
        type_combo.bind("<<ComboboxSelected>>", self.on_type_changed)
        
        # 金额输入
        ttk.Label(left_frame, text="金额:").pack(anchor=tk.W)
        self.amount_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.amount_var, width=20).pack(pady=(0, 10))
        
        # 分类选择
        ttk.Label(left_frame, text="分类:").pack(anchor=tk.W)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(left_frame, textvariable=self.category_var, 
                                          width=17, state="readonly")
        self.category_combo.pack(pady=(0, 10))
        self.update_categories()
        
        # 描述输入
        ttk.Label(left_frame, text="描述:").pack(anchor=tk.W)
        self.description_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.description_var, width=20).pack(pady=(0, 10))
        
        # 按钮
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="添加记录", command=self.add_transaction).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="清空", command=self.clear_form).pack(side=tk.LEFT)
        
        # 右侧：记录列表
        right_frame = ttk.Frame(record_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_frame, text="交易记录", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # 创建树形视图
        columns = ("日期", "类型", "金额", "分类", "描述")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 打包树形视图和滚动条
        tree_frame = ttk.Frame(right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 操作按钮
        button_frame2 = ttk.Frame(right_frame)
        button_frame2.pack(pady=10)
        
        ttk.Button(button_frame2, text="删除记录", command=self.delete_transaction).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame2, text="刷新", command=self.refresh_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame2, text="导出数据", command=self.export_data).pack(side=tk.LEFT)
        
    def create_statistics_tab(self, notebook):
        """创建统计页面"""
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="统计分析")
        
        # 顶部控制区
        control_frame = ttk.Frame(stats_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="统计周期:").pack(side=tk.LEFT)
        self.period_var = tk.StringVar(value="本月")
        period_combo = ttk.Combobox(control_frame, textvariable=self.period_var,
                                   values=["本月", "上月", "最近3个月", "最近6个月", "本年"], 
                                   width=10, state="readonly")
        period_combo.pack(side=tk.LEFT, padx=(5, 10))
        period_combo.bind("<<ComboboxSelected>>", self.update_charts)
        
        ttk.Button(control_frame, text="更新图表", command=self.update_charts).pack(side=tk.LEFT)
        
        # 图表区域
        chart_frame = ttk.Frame(stats_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建图表
        self.create_charts(chart_frame)
        
    def create_budget_tab(self, notebook):
        """创建预算页面"""
        budget_frame = ttk.Frame(notebook)
        notebook.add(budget_frame, text="预算管理")
        
        # 左侧：预算设置
        left_frame = ttk.Frame(budget_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Label(left_frame, text="设置预算", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # 月份选择
        ttk.Label(left_frame, text="月份:").pack(anchor=tk.W)
        self.budget_month_var = tk.StringVar(value=datetime.now().strftime("%Y-%m"))
        ttk.Entry(left_frame, textvariable=self.budget_month_var, width=20).pack(pady=(0, 10))
        
        # 分类选择
        ttk.Label(left_frame, text="分类:").pack(anchor=tk.W)
        self.budget_category_var = tk.StringVar()
        self.budget_category_combo = ttk.Combobox(left_frame, textvariable=self.budget_category_var, 
                                                 width=17, state="readonly")
        self.budget_category_combo.pack(pady=(0, 10))
        self.update_budget_categories()
        
        # 预算金额
        ttk.Label(left_frame, text="预算金额:").pack(anchor=tk.W)
        self.budget_amount_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.budget_amount_var, width=20).pack(pady=(0, 10))
        
        # 按钮
        budget_button_frame = ttk.Frame(left_frame)
        budget_button_frame.pack(pady=10)
        
        ttk.Button(budget_button_frame, text="设置预算", command=self.set_budget).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(budget_button_frame, text="清空", command=self.clear_budget_form).pack(side=tk.LEFT)
        
        # 右侧：预算列表和对比
        right_frame = ttk.Frame(budget_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_frame, text="预算执行情况", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # 预算列表
        budget_columns = ("月份", "分类", "预算", "实际", "差额", "完成率")
        self.budget_tree = ttk.Treeview(right_frame, columns=budget_columns, show="headings", height=10)
        
        for col in budget_columns:
            self.budget_tree.heading(col, text=col)
            self.budget_tree.column(col, width=80, anchor=tk.CENTER)
        
        self.budget_tree.pack(fill=tk.BOTH, expand=True)
        
        # 刷新按钮
        ttk.Button(right_frame, text="刷新预算", command=self.refresh_budget).pack(pady=10)
        
    def create_settings_tab(self, notebook):
        """创建设置页面"""
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="设置")
        
        ttk.Label(settings_frame, text="系统设置", font=("Arial", 14, "bold")).pack(pady=20)
        
        # 数据管理
        data_frame = ttk.LabelFrame(settings_frame, text="数据管理", padding=10)
        data_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(data_frame, text="导出所有数据", command=self.export_all_data).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(data_frame, text="清空所有数据", command=self.clear_all_data).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(data_frame, text="备份数据库", command=self.backup_database).pack(side=tk.LEFT)
        
        # 分类管理
        category_frame = ttk.LabelFrame(settings_frame, text="分类管理", padding=10)
        category_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(category_frame, text="支出分类: 餐饮, 交通, 购物, 娱乐, 医疗, 教育, 其他").pack(anchor=tk.W)
        ttk.Label(category_frame, text="收入分类: 工资, 奖金, 投资, 其他").pack(anchor=tk.W)
        
    def create_charts(self, parent):
        """创建图表"""
        # 创建图表画布
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle('财务数据分析', fontsize=16)
        
        canvas = FigureCanvasTkAgg(self.fig, parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 初始化图表
        self.update_charts()
        
    def update_categories(self):
        """更新分类选项"""
        if self.type_var.get() == "支出":
            categories = ["餐饮", "交通", "购物", "娱乐", "医疗", "教育", "其他"]
        else:
            categories = ["工资", "奖金", "投资", "其他"]
        
        self.category_combo['values'] = categories
        if categories:
            self.category_var.set(categories[0])
            
    def update_budget_categories(self):
        """更新预算分类选项"""
        categories = ["餐饮", "交通", "购物", "娱乐", "医疗", "教育", "其他"]
        self.budget_category_combo['values'] = categories
        if categories:
            self.budget_category_var.set(categories[0])
            
    def on_type_changed(self, event):
        """类型改变时更新分类"""
        self.update_categories()
        
    def add_transaction(self):
        """添加交易记录"""
        try:
            date = self.date_var.get()
            type_val = self.type_var.get()
            amount = float(self.amount_var.get())
            category = self.category_var.get()
            description = self.description_var.get()
            
            if not all([date, type_val, amount, category]):
                messagebox.showwarning("警告", "请填写完整信息")
                return
                
            # 保存到数据库
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (date, type, amount, category, description)
                VALUES (?, ?, ?, ?, ?)
            """, (date, type_val, amount, category, description))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("成功", "交易记录添加成功")
            self.clear_form()
            self.refresh_data()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的金额")
        except Exception as e:
            messagebox.showerror("错误", f"添加记录失败: {str(e)}")
            
    def delete_transaction(self):
        """删除选中的交易记录"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的记录")
            return
            
        if messagebox.askyesno("确认", "确定要删除选中的记录吗？"):
            # 这里需要实现删除逻辑
            # 由于树形视图没有直接存储记录ID，这里简化处理
            messagebox.showinfo("提示", "删除功能待完善")
            
    def clear_form(self):
        """清空表单"""
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.type_var.set("支出")
        self.amount_var.set("")
        self.category_var.set("")
        self.description_var.set("")
        self.update_categories()
        
    def refresh_data(self):
        """刷新数据显示"""
        # 清空树形视图
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 从数据库加载数据
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT date, type, amount, category, description FROM transactions ORDER BY date DESC")
        
        for row in cursor.fetchall():
            # 格式化金额显示
            amount_str = f"￥{row[2]:.2f}"
            self.tree.insert("", "end", values=(row[0], row[1], amount_str, row[3], row[4]))
            
        conn.close()
        
    def update_charts(self, event=None):
        """更新图表"""
        # 清空所有子图
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
            
        # 获取数据
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # 根据选择的周期获取数据
        period = self.period_var.get()
        if period == "本月":
            start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
        elif period == "上月":
            last_month = datetime.now().replace(day=1) - timedelta(days=1)
            start_date = last_month.replace(day=1).strftime("%Y-%m-%d")
        elif period == "最近3个月":
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        elif period == "最近6个月":
            start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
        else:  # 本年
            start_date = datetime.now().replace(month=1, day=1).strftime("%Y-%m-%d")
            
        cursor.execute("SELECT * FROM transactions WHERE date >= ?", (start_date,))
        transactions = cursor.fetchall()
        conn.close()
        
        if not transactions:
            self.fig.canvas.draw()
            return
            
        # 1. 收支趋势图
        dates = []
        incomes = []
        expenses = []
        
        # 按日期分组
        daily_data = defaultdict(lambda: {'income': 0, 'expense': 0})
        for trans in transactions:
            date = trans[1]
            amount = trans[3]
            trans_type = trans[2]
            
            if trans_type == "收入":
                daily_data[date]['income'] += amount
            else:
                daily_data[date]['expense'] += amount
                
        # 排序并准备数据
        sorted_dates = sorted(daily_data.keys())
        for date in sorted_dates:
            dates.append(datetime.strptime(date, "%Y-%m-%d"))
            incomes.append(daily_data[date]['income'])
            expenses.append(daily_data[date]['expense'])
            
        self.ax1.plot(dates, incomes, 'g-', label='收入', marker='o')
        self.ax1.plot(dates, expenses, 'r-', label='支出', marker='s')
        self.ax1.set_title('收支趋势')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        
        # 2. 支出分类饼图
        expense_categories = defaultdict(float)
        for trans in transactions:
            if trans[2] == "支出":
                expense_categories[trans[4]] += trans[3]
                
        if expense_categories:
            labels = list(expense_categories.keys())
            sizes = list(expense_categories.values())
            self.ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            self.ax2.set_title('支出分类分布')
            
        # 3. 收支对比柱状图
        total_income = sum(incomes)
        total_expense = sum(expenses)
        
        categories = ['收入', '支出']
        amounts = [total_income, total_expense]
        colors = ['green', 'red']
        
        self.ax3.bar(categories, amounts, color=colors, alpha=0.7)
        self.ax3.set_title('收支对比')
        self.ax3.set_ylabel('金额 (元)')
        
        # 4. 月度统计
        monthly_data = defaultdict(lambda: {'income': 0, 'expense': 0})
        for trans in transactions:
            month = trans[1][:7]  # 取年-月部分
            amount = trans[3]
            trans_type = trans[2]
            
            if trans_type == "收入":
                monthly_data[month]['income'] += amount
            else:
                monthly_data[month]['expense'] += amount
                
        months = sorted(monthly_data.keys())
        month_incomes = [monthly_data[m]['income'] for m in months]
        month_expenses = [monthly_data[m]['expense'] for m in months]
        
        x = range(len(months))
        width = 0.35
        
        self.ax4.bar([i - width/2 for i in x], month_incomes, width, label='收入', color='green', alpha=0.7)
        self.ax4.bar([i + width/2 for i in x], month_expenses, width, label='支出', color='red', alpha=0.7)
        self.ax4.set_title('月度收支统计')
        self.ax4.set_ylabel('金额 (元)')
        self.ax4.set_xticks(x)
        self.ax4.set_xticklabels(months, rotation=45)
        self.ax4.legend()
        
        plt.tight_layout()
        self.fig.canvas.draw()
        
    def set_budget(self):
        """设置预算"""
        try:
            month = self.budget_month_var.get()
            category = self.budget_category_var.get()
            amount = float(self.budget_amount_var.get())
            
            if not all([month, category, amount]):
                messagebox.showwarning("警告", "请填写完整信息")
                return
                
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # 检查是否已存在相同的预算
            cursor.execute("SELECT id FROM budgets WHERE month = ? AND category = ?", (month, category))
            existing = cursor.fetchone()
            
            if existing:
                # 更新现有预算
                cursor.execute("UPDATE budgets SET amount = ? WHERE month = ? AND category = ?", 
                             (amount, month, category))
            else:
                # 添加新预算
                cursor.execute("INSERT INTO budgets (month, category, amount) VALUES (?, ?, ?)", 
                             (month, category, amount))
                
            conn.commit()
            conn.close()
            
            messagebox.showinfo("成功", "预算设置成功")
            self.clear_budget_form()
            self.refresh_budget()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的金额")
        except Exception as e:
            messagebox.showerror("错误", f"设置预算失败: {str(e)}")
            
    def clear_budget_form(self):
        """清空预算表单"""
        self.budget_month_var.set(datetime.now().strftime("%Y-%m"))
        self.budget_category_var.set("")
        self.budget_amount_var.set("")
        
    def refresh_budget(self):
        """刷新预算显示"""
        # 清空预算树形视图
        for item in self.budget_tree.get_children():
            self.budget_tree.delete(item)
            
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # 获取所有预算
        cursor.execute("SELECT month, category, amount FROM budgets ORDER BY month DESC")
        budgets = cursor.fetchall()
        
        for budget in budgets:
            month, category, budget_amount = budget
            
            # 计算实际支出
            cursor.execute("""
                SELECT SUM(amount) FROM transactions 
                WHERE date LIKE ? AND type = '支出' AND category = ?
            """, (f"{month}%", category))
            
            actual_result = cursor.fetchone()
            actual_amount = actual_result[0] if actual_result[0] else 0
            
            # 计算差额和完成率
            difference = budget_amount - actual_amount
            completion_rate = (actual_amount / budget_amount * 100) if budget_amount > 0 else 0
            
            # 插入到树形视图
            self.budget_tree.insert("", "end", values=(
                month, category, f"￥{budget_amount:.2f}", f"￥{actual_amount:.2f}", 
                f"￥{difference:.2f}", f"{completion_rate:.1f}%"
            ))
            
        conn.close()
        
    def export_data(self):
        """导出交易数据"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT date, type, amount, category, description FROM transactions ORDER BY date DESC")
                
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["日期", "类型", "金额", "分类", "描述"])
                    writer.writerows(cursor.fetchall())
                    
                conn.close()
                messagebox.showinfo("成功", f"数据已导出到: {filename}")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
            
    def export_all_data(self):
        """导出所有数据"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                
                # 获取所有交易记录
                cursor.execute("SELECT * FROM transactions")
                transactions = cursor.fetchall()
                
                # 获取所有预算
                cursor.execute("SELECT * FROM budgets")
                budgets = cursor.fetchall()
                
                conn.close()
                
                # 构建数据字典
                data = {
                    "transactions": [
                        {
                            "id": t[0], "date": t[1], "type": t[2], "amount": t[3],
                            "category": t[4], "description": t[5], "created_at": t[6]
                        } for t in transactions
                    ],
                    "budgets": [
                        {
                            "id": b[0], "category": b[1], "amount": b[2], 
                            "month": b[3], "created_at": b[4]
                        } for b in budgets
                    ]
                }
                
                with open(filename, 'w', encoding='utf-8') as jsonfile:
                    json.dump(data, jsonfile, ensure_ascii=False, indent=2)
                    
                messagebox.showinfo("成功", f"所有数据已导出到: {filename}")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
            
    def clear_all_data(self):
        """清空所有数据"""
        if messagebox.askyesno("确认", "确定要清空所有数据吗？此操作不可恢复！"):
            try:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transactions")
                cursor.execute("DELETE FROM budgets")
                conn.commit()
                conn.close()
                
                messagebox.showinfo("成功", "所有数据已清空")
                self.refresh_data()
                self.refresh_budget()
                
            except Exception as e:
                messagebox.showerror("错误", f"清空数据失败: {str(e)}")
                
    def backup_database(self):
        """备份数据库"""
        try:
            import shutil
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"finance_backup_{timestamp}.db"
            
            shutil.copy2(self.db_file, backup_filename)
            messagebox.showinfo("成功", f"数据库已备份到: {backup_filename}")
            
        except Exception as e:
            messagebox.showerror("错误", f"备份失败: {str(e)}")

def main():
    """主函数"""
    root = tk.Tk()
    app = FinanceManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
