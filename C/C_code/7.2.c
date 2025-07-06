#include <stdio.h>

void sort(int*a,int n)
{
    int i,j;
    for ( i = 0; i < n-1; i++)
    {
       for ( j = i+1; j < n; j++)
       {
            if (*(a+j)<*(a+i))
            {
                int t=*(a+j);
                *(a+j)=*(a+i);
                *(a+i)=t;
            }
       }
    }
}
int main()
{
    int n,*a;int i;
    scanf("%d",&n);
    for ( i = 0; i < n; i++)
    {
        scanf("%d",(a+i));
    } 
    sort(a,n);
    for ( i = 0; i < n; i++)
    {
        printf("%d  ",a[i]);
    }
    printf("\n");
    return 0;
}