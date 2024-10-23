# 题目：求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字。
# 例如2+22+222+2222+22222(此时共有5个数相加)，几个数相加由键盘控制。
# 程序分析：关键是计算出每一项的值。

a = int(input("请输入一个数字："))
n = int(input("请输入数列的长度："))

total_sum = 0
current_number = 0

for i in range(n):
    current_number = current_number * 10 + a
    total_sum += current_number

print(f"计算结果为：{total_sum}")