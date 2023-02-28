#include <stdio.h>
#define P 3.14
int main()
{
    int r,v;
    printf("Please input r\n");
    scanf("%d",&r);
    v=4.0/3.0*r*r*r*P;
    printf("V=%d",v);
    return 0;
}