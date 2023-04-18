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