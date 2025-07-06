#include<stdio.h>
#include<math.h>
int main()
{
    double item,sum;
    sum=0;
    int i,sign,q;
    sign=1;i=1;
    double m,n;
    m=2,n=1;
    scanf("%d",&q);
    while (i<=q)
    {
        item=sign*m/n;
        sum=sum+item;
        m=m+n;
        n=m-n;
        sign=-sign;
        i++;
    }
    printf("sum=%lf",sum);
    return 0;
}