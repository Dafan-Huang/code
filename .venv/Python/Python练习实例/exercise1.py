# 题目：有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？
# 程序分析：可填在百位、十位、个位的数字都是1、2、3、4。组成所有的排列后再去 掉不满足条件的排列。

count=0
for i in range(1,4+1):
    for j in range(1,4+1):
        for k in range(1,4+1):
            if i!=j and i!=k and j!=k:
                count+=1
                print(i,j,k)
print(count)


