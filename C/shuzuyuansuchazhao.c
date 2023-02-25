
#include<stdio.h>
#define size 10
int find(int a[],int n,int x);
int main()
{
int array[size],i=0,n,x;
int pos;
do
{   printf("n(1<=n<=%d):",size);
    scanf("%d",&n);
} while (n<1||n>size);
printf("ngeyuansu%d:",n);
for ( i = 0; i < n; i++)
    scanf("%d",&array[i]);
printf("x");
scanf("%d",&x);
pos=find(array,n,x);
if (pos<n)
    printf("value=%d,index=%d\n",x,pos);
else
    printf("not present!\n");
return 0;
}

int find(int a[],int n, int x)
{
    int i=0;
    while (i<n)
    {
        if (x==a[i])
            break;
        i++;
    }
    return i;
}