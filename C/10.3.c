#include <stdio.h>
#include <string.h>
struct Date
{
    int year;
    int month;
    int day;
};
typedef struct Date Date;
typedef struct Student 
{
    int ID;
    char name[20];
    Date birthday;
    char sex;
    double score;
}Student;
int main()
{
    Student st[3]={{1001,"zhang",{1992,5,21},'F',83},
    {1002,"wang",{1993,6,18},'M',66}};
    Student *p;
    p=st;
    (p+2) ->ID=1003;
    strcpy((p+2) ->name,"li");
    (p+2) ->birthday.year=1993;
    (p+2) ->birthday.month=7;
    (p+2) ->birthday.day=22;
    (p+2) ->sex='M';
    (p+2) ->score=100;
    for ( ;p<st+3; p++)
    {
        printf("%d %s %d. %d. %d %c %f\n",(p)->ID,(p)->name,
        (p)->birthday.year,(p)->birthday.month,(p)->birthday.day,
        (p)->sex,(p)->score);
    }
    return 0;
}
