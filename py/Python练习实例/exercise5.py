# 题目：输入三个整数x,y,z，请把这三个数由小到大输出。
# 程序分析：我们想办法把最小的数放到x上，先将x与y进行比较，如果x>y则将x与y的值进行交换，然后再用x与z进行比较，
# 如果x>z则将x与z的值进行交换，这样能使x最小。

x = int(input("请输入第一个数："))
y = int(input("请输入第二个数："))
z = int(input("请输入第三个数："))
if x > y:
    x,y = y,x
if x>z:
    x,z = z,x
if y>z:
    y,z = z,y
print(x,y,z)


#python3自带的排序函数是sorted()
l = []
for i in range(3):
    x = int(input('integer:\n'))
    l.append(x)
l.sort()
print (l)