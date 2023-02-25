#include <stdio.h>

void move (int a[10],int m)
{
    int i,j;
    for ( i = 0; i < m; i++)
    {
        int last=a[9];
        for ( j = 9; j >0; j--)
        {
            a[j]=a[j-1];
        }
       a[0]=last;
    }
}

int main()
{
    int m,i;
    int a[10]={1,2,3,4,5,6,7,8,9,10};
    scanf("%d",&m);
    /*for ( i = 0; i < m; i++)
    {
        int last=a[9];
        for ( j = 9; j >0; j--)
        {
            a[j]=a[j-1];
        }
       a[0]=last;
    }*/
    move(a,m);
    for ( i = 0; i < 10; i++)
    {
        printf("%3d",a[i]);
    }
    return 0;
}