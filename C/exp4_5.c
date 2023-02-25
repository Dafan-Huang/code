#include<stdio.h>
#include<math.h>
int judgePrime( int n)
{
    int i,k;
    int judge=1;
    if (n==1)
    {
        judge=0;
    }
    k=(int)sqrt(n);
    for ( i = 2;judge&&i<=k; i++)
        if (n%i==0)
            judge=0;
    return judge;
}

int main()
{
    int x,n;
    int q=0;
    for ( x = 4; x <=2000; x+=2)
    {
        for ( n = 2; n < x; n++)
        {
            if (judgePrime(n)&&judgePrime(x-n))
            {
                printf("%4d=%4d+%4d",x,n,x-n);
                q++;
                if (q%4==0)
                {
                    printf("\n");
                }
                else
                {
                    printf(" ");
                }
                
                    break;
            }
            
        }
        
    }
    return 0;
}