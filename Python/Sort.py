# 十一种常用的排序算法

a=[12,34,23,56,45,10,9,514,114]

# # 1.选择排序
# def Select_Sort(list):
#     n=len(list) #列表长度
#     for i in range(n-1): #循环列表
#         min = i
#         for j in range(i+1,n): #循环列表中的元素
#             if list[j]<list[min]: #如果列表中的元素小于列表中的第一个元素
#                 min = j #将列表中的元素赋值给列表中的第一个元素
#         list[i],list[min]=list[min],list[i] #交换列表中的元素
        
# Select_Sort(a)
# print(a)

# # 2.冒泡排序
# def Bubble_Sort(list):
#     n=len(list) #列表长度
#     for i in range(n-1,-1,-1): #循环列表
#         for j in range(0,i): #循环列表中的元素
#             if list[j]>list[j+1]: #如果列表中的元素大于列表中的第二个元素
#                 a[j],a[j+1]=a[j+1],a[j] #交换列表中的元素

# Bubble_Sort(a)
# print(a)         

# # 3.插入排序
# def Insert_Sort(list):
#     n=len(list) #列表长度
#     for i in range(1,n): #循环列表
#         x=list[i] #将列表中的元素赋值给x
#         j=i-1 
#         while j>=0:
#             if x<=a[j]:
#                 a[j+1]=a[j]
#                 j-=1
#             else:
#                 break
#         a[j+1]=x

# Insert_Sort(a)
# print(a)

# # 4.归并排序
def Merge(list,start,mid,end):
    tmp=[]
    l= start
    r= mid+1
    while l<=mid and r<=end:
        if list[l]<=list[r]:
            tmp.append(list[l])
            l+=1
        else:
            tmp.append(list[r])
            r+=1
    tmp.extend(list[l:mid+1])
    tmp.extend(list[r:end+1])
    for i in range(start,end+1):
        list[i]=tmp[i-start]

def Merge_Sort(list,start,end):
    if start==end:
        return
    mid=(start+end)//2  
    Merge_Sort(list,start,mid)
    Merge_Sort(list,mid+1,end)
    Merge(list,start,mid,end)

Merge_Sort(a,0,len(a)-1)
print(a)

## 5.快速排序
# def Quick_Sort(list,start,end):
#     if start>=end:
#         return
#     mid=list[start]
#     low=start
#     high=end
#     while low<high:
#         while low<high and list[high]>=mid:
#             high-=1
#         list[low]=list[high]
#         while low<high and list[low]<mid:
#             low+=1
#         list[high]=list[low]
#     list[low]=mid
#     Quick_Sort(list,start,low-1)
#     Quick_Sort(list,low+1,end)

# Quick_Sort(a,0,len(a)-1)
# print(a)

# # 6.堆排序
# def Heap_Sort(list):