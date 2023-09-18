# 题目：输入某年某月某日，判断这一天是这一年的第几天？
# 程序分析：以3月5日为例，应该先把前两个月的加起来，然后再加上5天即本年的第几天，
# 特殊情况，闰年且输入月份大于2时需考虑多加一天：

year = int(input('year:'))
month = int(input('month:'))
day = int(input('day:'))

months = (0,31,59,90,120,151,181,212,243,273,304,334)


if 0 < month <= 12:
    sum =months[month-1]+day
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        if month > 2:
            sum += 1
            print('it is the %dth day.' % sum)
    else:
        print('it is the %dth day.' % sum)
else:
    print('data error')