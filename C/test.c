#include <stdio.h>
#include <math.h>
int main()
{
    int a[5],i;
    int *p=a;
    for ( i = 0; i < 5; i++)
    {
        scanf("%d",&a[i]);
    }
    for ( i = 0; i < 5; i++)
    {
        printf("%d",a[i]);
    }
    printf("\n");
    printf("%d\n",*++p);
    printf("%d\n",*p);
    return 0;
}