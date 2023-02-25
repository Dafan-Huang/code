#include<stdio.h>

int main()
{
    long int x;
    char s[]="0123456789ABCDEF";
    int a[100],i=0;
    scanf("%ld",&x);
    while (x!=0)
    {
        a[i]=x%16;
        x=x/16;
        i++;
    }
    int m=0;
    for ( i = i-1; i >=0; i--)
    {
        m=a[i];
        printf("%c",s[m]);
    }
    return 0;
}