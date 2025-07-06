#include<stdio.h>
#include<string.h>
struct student
{
    int ID;
    char name[10];
    int score[3];
};
typedef struct student stu;
void average (stu[],int n);
int main()
{
    int n,i,j;
    stu a[10];
    do
    {
        scanf("%d",&n);
    } while (n<=0||n>10);
    for ( i = 0; i < n; i++)
    {
        scanf("%d %s",&a[i].ID,a[i].name);
        for ( j = 0; j < 3; j++)
        {
            scanf("%d",&a[i].score[j]);
        }
    }
    average(a,n);
    return 0;
}

void average(stu a[],int n)
{
    int i,j;
    for ( i = 0; i < n; i++)
    {
        int sum=0;
        int ave=0;
        for ( j = 0; j < 3; j++)
        {
            sum+=a[i].score[j];
        }
        ave=sum/3.0; 
        printf("The average score of the %dth student is %d.\n",i+1,ave);     
    }
}