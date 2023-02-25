#include <stdio.h>
int SumDiff(int a,int b,int *dif)
{
    int sum;
    *dif=a-b;
    sum=a+b;
    return sum;
}
int main( )
{ 
    int a,b,sum,dif;
    scanf("%d%d",&a,&b);
    sum=SumDiff(a,b,&dif);
    printf("sum=%d, difference=%d\n",sum,dif);
    return 0;
}
