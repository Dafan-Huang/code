#include<stdio.h>
void swap1(int a,int b)
{
    int temp=a;
    a=b;
    b=temp;
    printf("a=%d,b=%d\n",a,b);
}

void swap2(int *a,int b)
{
    int temp=*a;
    *a=b;
    b=temp;
    printf("*a=%d,b=%d\n",*a,b);
}

void swap3(int *a,int *b)
{
    int temp=*a;
    *a=*b;
    *b=temp;
    printf("*a=%d,*b=%d\n",a,b);
}

void swap4(int *a,int *b)
{
    int *temp=a;
    a=b;
    b=temp;
    printf("a=%d,b=%d\n",a,b);
}

int main()
{
    int x=3,y=4;
    swap1(x,y);
    printf("x=%d,y=%d\n",x,y);
    return 0;
}