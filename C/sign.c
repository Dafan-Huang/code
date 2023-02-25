#include<stdio.h>
int main()
{
    int sign=1,i;
    double sum=0;
    for ( i = 1; i <= 1000; i++)
    {
        sum+=sign*1.0/i;
        sign=-sign;
    }
    printf("%f\n",sum);
    return 0;
}