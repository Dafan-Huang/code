#include<stdio.h>
int main()
{
    int i,j;
    for ( i = 0; i <=3; i++)
    {
        for ( j = 3-i; j >0; j--)
        {
            printf(" ");
        }
        for ( j = 2*i+1;j>0 ; j--)
        {
            printf("*");
        }
        printf("\n");
    }
    for ( i = 3; i >=1; i--)
    {
        for ( j = 3-i; j>=0 ; j--)
        {
            printf(" ");
        }
        for ( j = 2*i-1; j >0; j--)
        {
            printf("*");
        }
        printf("\n");
    }
    
    return 0;

}