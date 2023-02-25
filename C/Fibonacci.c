#include<stdio.h>
#define N 30
int main()
{
    int i,fib[N]={0,1,1};
    int n=17;
    
    for ( i = 3; i <= n ; i++)
    fib[i]=fib[i-1]+fib[i-2];
    for ( i = 1; i <=n; i++)
    {
        printf("%10d",fib[i]);
        if((i)%5==0)
        printf("\n");
    }
    return 0;
}