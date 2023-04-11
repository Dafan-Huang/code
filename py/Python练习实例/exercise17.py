# 题目：输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。
# 程序分析：利用 while 或 for 语句,条件为输入的字符不为 '\n'。

s = input('请输入一行字符：')
letters = 0
space = 0
digit = 0
others = 0
for c in s:
    if c.isalpha(): # isalpha() 方法检测字符串是否只由字母组成
        letters += 1
    elif c.isspace(): # isspace() 方法检测字符串是否只由空格组成
        space += 1
    elif c.isdigit(): # isdigit() 方法检测字符串是否只由数字组成
        digit += 1
    else:
        others += 1
print('char = %d,space = %d,digit = %d,others = %d' % (letters,space,digit,others))