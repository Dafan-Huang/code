#include<stdio.h>

void printDiamond(int k);

int main()
{
    int n;
    scanf("%d",&n);
    printDiamond(n);
    return  0;
}

void printDiamond(k)
{
    int i,j,n;
    n=k/2+1;
    for ( i = 0; i < n; i++)
    {
        for ( j = 0; j < n-i; j++)
        {
            printf(" ");
        }
        for ( j = 0; j < 2*i+1; j++)
        {
            printf("*");
        }
        printf("\n");
    }
    for ( i = n-2; i >=0; i--)
    {
         for ( j = 0; j < n-i; j++)
        {
            printf(" ");
        }
        for ( j = 0; j < 2*i+1; j++)
        {
            printf("*");
        }
        printf("\n");
    }
    
}

