#include <stdio.h>
int main()
{
    int a,b,sum,difference,product;
    double quotient,ave;
    scanf("%d%d",&a,&b);
    sum=a+b;
    difference=a-b;
    product=a*b;
    quotient=a*1.0/b;
    ave=(a+b)*1.0/2;
    printf("sum=%d\n",sum);
    printf("difference=%d\n",difference);
    printf("product=%d\n",product);
    printf("quotiennt=%f\n",quotient);
    printf("ave=%f\n",ave);
    return 0;
}