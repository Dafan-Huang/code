#include<stdio.h>
int main()
{
    int addresscode;
    int year,month,day;
    int seqno;
    char checkcode;
    printf("请输入身份证号码:");
    scanf("%6d%4d%2d%2d%3d%1c",&addresscode,&year,&month,&day,&seqno,&checkcode);
    printf("地址码:%d\n",addresscode);
    printf("出生日期: %dY %dM %dD\n",year,month,day);
    printf("顺序码:%03d\n",seqno);
    printf("校验码:%c\n",checkcode);
    return 0;
}