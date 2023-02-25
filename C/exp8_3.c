#include<stdio.h>
struct Date
{
    int year;
    int month;
    int day;
};
typedef struct Date Date;

int checkDate(Date date);
int main()
{
    Date date;
    int flag;
    do
    {
        printf("Please input date!\n");
        scanf("%d%d%d",&date.year,&date.month,&date.day);
        flag = checkDate(date);
        if (flag)
        {
            printf("The date is valid!\n");
        }
        else
        {
            printf("Invalid date!\n");
        }
    } while (!flag);
    return 0;
}
int checkDate(Date date)
{
    if (date.year<1900||date.year>2018)
    {
        return 0;
    }
    if (date.month<1||date.month>12)
    {
        return 0;
    }
    if (date.month==1  ||
        date.month==3  ||
        date.month==5  ||
        date.month==7  ||
        date.month==8  ||
        date.month==10 ||
        date.month==12  )
    {
        if (date.day<1||date.day>31)
        {
            return 0;
        }
    }
    else if (date.month==4 ||
             date.month==6 ||
             date.month==9 ||
             date.month==11 )
    {
        if (date.day<1||date.day>30)
        {
            return 0;
        }
    }
    else
    {
        if (date.year%4==0&&date.year%100!=00||date.year%400==0)
        {
            if (date.day<1||date.day>29)
            {
                return 0;
            }
        }
        else
        {
            if (date.day<1||date.day>28)
            {
                return 0;
            }
        }
    }
    return 1;
}