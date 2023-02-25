#include<stdio.h>
#include<math.h>
int i,j,x;
int main()
{
for ( i = 1; i <10; i++)
{
    for ( j = 0; j <10; j++)
    {
        x=i*1100+j*11;
        if (i!=j&&(int)sqrt(x)*(int)sqrt(x)==x)
        {
            printf("%d",x);
        }
    }
}
return 0;
}

