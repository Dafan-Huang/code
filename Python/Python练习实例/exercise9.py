# 题目：暂停一秒输出。
# 程序分析：使用 time 模块的 sleep() 函数。

import time
# l=["我是1","我是2","我是3","我是4","我是5","我是6","我是7","我是8","我是9","我是10"]
# for i in l:
#     print(i)
#     time.sleep(1)

for i in range(100):
    print(".")
    time.sleep(0.3)