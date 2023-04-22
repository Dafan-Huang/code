//动态数组
#include<stdio.h>
#include<stdlib.h>
int main()
{
    int *p;//定义指针
    int i;
    int n;
    printf("Please input the length of array:");
    scanf("%d",&n);//输入数组长度
    p=(int *)malloc(n*sizeof(int));//动态分配内存
//  p=(int *)calloc(n,sizeof(int));
    for(i=0;i<n;i++)
    {
        scanf("%d",&p[i]);
    }
    for(i=0;i<n;i++)
    {
        printf("%d ",p[i]);
    }
    free(p);//释放内存
    return 0;
}

// 笑死了，这个程序是我自己写的，但是我不知道为什么，我把它放在了这里
// 但是我不想删掉它，因为我觉得它很有意思
// 但是我又不知道它有什么意思
// 你懂吗？
// 你真的懂了吗？

