#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人财务管理系统 - 简化版
适合初学者的Python练手项目

主要功能：
1. 记录收支
2. 查看统计
3. 简单图表
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

# 配置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

class SimpleFinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("个人财务管理系统 - 简化版")
        self.root.geometry("800x600")
        
        # 数据文件
        self.data_file = "finance_data.json"
        self.data = self.load_data()
        
        # 创建界面
        self.create_widgets()
        
        # 刷新显示
        self.refresh_display()
        
    def load_data(self):
        """加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"transactions": []}
    
    def save_data(self):
        """保存数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存数据失败: {str(e)}")
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧输入区
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 输入表单
        ttk.Label(left_frame, text="记账", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # 日期
        ttk.Label(left_frame, text="日期:").pack(anchor=tk.W)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(left_frame, textvariable=self.date_var, width=15).pack(pady=(0, 10))
        
        # 类型
        ttk.Label(left_frame, text="类型:").pack(anchor=tk.W)
        self.type_var = tk.StringVar(value="支出")
        ttk.Combobox(left_frame, textvariable=self.type_var, 
                    values=["收入", "支出"], width=12, state="readonly").pack(pady=(0, 10))
        
        # 金额
        ttk.Label(left_frame, text="金额:").pack(anchor=tk.W)
        self.amount_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.amount_var, width=15).pack(pady=(0, 10))
        
        # 分类
        ttk.Label(left_frame, text="分类:").pack(anchor=tk.W)
        self.category_var = tk.StringVar()
        ttk.Combobox(left_frame, textvariable=self.category_var, 
                    values=["餐饮", "交通", "购物", "娱乐", "工资", "其他"], 
                    width=12).pack(pady=(0, 10))
        
        # 描述
        ttk.Label(left_frame, text="描述:").pack(anchor=tk.W)
        self.description_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.description_var, width=15).pack(pady=(0, 10))
        
        # 按钮
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="添加", command=self.add_transaction).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="清空", command=self.clear_form).pack(side=tk.LEFT)
        
        # 统计信息
        stats_frame = ttk.LabelFrame(left_frame, text="统计信息", padding=10)
        stats_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.stats_label = ttk.Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.pack()
        
        # 右侧显示区
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 创建笔记本控件
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 记录列表页
        self.create_records_tab(notebook)
        
        # 图表页
        self.create_chart_tab(notebook)
        
    def create_records_tab(self, notebook):
        """创建记录列表页"""
        records_frame = ttk.Frame(notebook)
        notebook.add(records_frame, text="记录列表")
        
        # 记录列表
        columns = ("日期", "类型", "金额", "分类", "描述")
        self.tree = ttk.Treeview(records_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor=tk.CENTER)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 打包
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 操作按钮
        button_frame = ttk.Frame(records_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="删除选中", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="导出数据", command=self.export_data).pack(side=tk.LEFT, padx=5)
        
    def create_chart_tab(self, notebook):
        """创建图表页"""
        chart_frame = ttk.Frame(notebook)
        notebook.add(chart_frame, text="图表分析")
        
        # 创建图表
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 更新按钮
        ttk.Button(chart_frame, text="刷新图表", command=self.update_charts).pack(pady=10)
        
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
            
            # 添加到数据
            transaction = {
                "date": date,
                "type": type_val,
                "amount": amount,
                "category": category,
                "description": description,
                "created_at": datetime.now().isoformat()
            }
            
            self.data["transactions"].append(transaction)
            self.save_data()
            
            messagebox.showinfo("成功", "记录添加成功")
            self.clear_form()
            self.refresh_display()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的金额")
        except Exception as e:
            messagebox.showerror("错误", f"添加失败: {str(e)}")
    
    def delete_selected(self):
        """删除选中的记录"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的记录")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的记录吗？"):
            # 获取选中项的索引
            selected_item = selection[0]
            index = self.tree.index(selected_item)
            
            # 从数据中删除
            if 0 <= index < len(self.data["transactions"]):
                del self.data["transactions"][index]
                self.save_data()
                self.refresh_display()
                messagebox.showinfo("成功", "记录已删除")
    
    def clear_form(self):
        """清空表单"""
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.type_var.set("支出")
        self.amount_var.set("")
        self.category_var.set("")
        self.description_var.set("")
    
    def refresh_display(self):
        """刷新显示"""
        # 清空树形视图
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加数据
        for transaction in reversed(self.data["transactions"]):  # 最新的在前
            amount_str = f"￥{transaction['amount']:.2f}"
            self.tree.insert("", "end", values=(
                transaction["date"],
                transaction["type"],
                amount_str,
                transaction["category"],
                transaction["description"]
            ))
        
        # 更新统计信息
        self.update_stats()
        
        # 更新图表
        self.update_charts()
    
    def update_stats(self):
        """更新统计信息"""
        transactions = self.data["transactions"]
        
        total_income = sum(t["amount"] for t in transactions if t["type"] == "收入")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "支出")
        balance = total_income - total_expense
        
        # 当月统计
        current_month = datetime.now().strftime("%Y-%m")
        month_transactions = [t for t in transactions if t["date"].startswith(current_month)]
        month_income = sum(t["amount"] for t in month_transactions if t["type"] == "收入")
        month_expense = sum(t["amount"] for t in month_transactions if t["type"] == "支出")
        
        stats_text = f"""总收入: ￥{total_income:.2f}
总支出: ￥{total_expense:.2f}
余额: ￥{balance:.2f}

本月收入: ￥{month_income:.2f}
本月支出: ￥{month_expense:.2f}"""
        
        self.stats_label.config(text=stats_text)
    
    def update_charts(self):
        """更新图表"""
        # 清空图表
        self.ax1.clear()
        self.ax2.clear()
        
        transactions = self.data["transactions"]
        
        if not transactions:
            self.canvas.draw()
            return
        
        # 图表1: 收支对比
        income_total = sum(t["amount"] for t in transactions if t["type"] == "收入")
        expense_total = sum(t["amount"] for t in transactions if t["type"] == "支出")
        
        categories = ['收入', '支出']
        amounts = [income_total, expense_total]
        colors = ['green', 'red']
        
        self.ax1.bar(categories, amounts, color=colors, alpha=0.7)
        self.ax1.set_title('收支对比')
        self.ax1.set_ylabel('金额 (元)')
        
        # 图表2: 支出分类
        expense_by_category = defaultdict(float)
        for t in transactions:
            if t["type"] == "支出":
                expense_by_category[t["category"]] += t["amount"]
        
        if expense_by_category:
            labels = list(expense_by_category.keys())
            sizes = list(expense_by_category.values())
            self.ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            self.ax2.set_title('支出分类分布')
        
        plt.tight_layout()
        self.canvas.draw()
    
    def export_data(self):
        """导出数据"""
        try:
            filename = f"finance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("成功", f"数据已导出到: {filename}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

def main():
    """主函数"""
    root = tk.Tk()
    app = SimpleFinanceManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
