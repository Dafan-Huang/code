#include<stdio.h>
#define DAYS_FEB(year)(year%4==0&&year%100!=0)||year%400==0
int main()
{
    int year,days;
    scanf("%d",&year);
    if (DAYS_FEB(year))
    {
        days=29;
    }
    else
    days=28;
    printf("days of the FEB.:%d\n",days);
    return 0;
}