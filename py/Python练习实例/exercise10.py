# 题目：暂停一秒输出，并格式化当前时间。
# 程序分析：使用 time 模块的 sleep() 函数。
import time 
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
time.sleep(1)
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

# time模块
# time.time()  # 返回当前时间的时间戳（1970纪元后经过的浮点秒数）
# time.localtime([secs])  # 将一个时间戳转化为当前时区的struct_time
# time.gmtime([secs])  # 将一个时间戳转化为UTC时区（0时区）的struct_time
# time.mktime(t)  # 将一个struct_time转化为时间戳
# time.asctime([t])  # 将一个struct_time转化为字符串
# time.ctime([secs])  # 将一个时间戳（按秒计算的浮点数）转化为time.asctime()的形式
# time.strftime(format[, t])  # 将一个struct_time转化为格式化的字符串
# time.strptime(str, format)  # 将格式化时间字符串转化为struct_time
# time.sleep(secs)  # 线程推迟调用线程的运行，secs指秒数

