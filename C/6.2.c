#include<stdio.h>

int fun(int a,int b,int r[])
{
    int n=0,i;
    for ( i = a; i<=b; i++)
    {
        if (i%7==0||i%11==0)
            if (i%77!=0)
            {
                r[n]=i;
                n++;
            }
    }
    return n;
}
int main()
{
    int a,b,r[1000]={0},i,n;
    do
    {
      scanf("%d%d",&a,&b);
    } while (a>b);
    n=fun(a,b,r);
    for ( i = 0; i <n; i++)
    {
        printf("%d",r[i]);
        if (i<n-1)
        {
            printf(" ");
        }
        else
        {
            printf("\n");break;
        }
    }

return 0;
}