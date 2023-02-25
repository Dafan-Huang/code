#include<stdio.h>
#define size 12
int main()
{
    int YYYY,MM,DD;
    int sum,i;
    int m[12]={31,28,31,30,31,30,31,31,30,31,30,31};
    scanf("%d-%d-%d",&YYYY,&MM,&DD);
    if ((YYYY%4==0)&&(YYYY%100!=0||(YYYY%400==0)))
    m[1]=29;
    for ( i = 0; i<MM-1; i++)
    {
        sum+=m[i];
    }
    sum+=DD;
    printf("%d\n",sum);
    return 0;
}