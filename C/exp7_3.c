#include<stdio.h>
#include<string.h>
#define N 100

void delSpace(char *str)
{
    int i=0,j;
    while ('\0'!=str[i])
    {
        if (' '==str[i])
        {
            for ( j = i; j < strlen(str); j++)
            {
                str[j]=str[j+1];
            }
            continue;
        }
        i++;
    }
}

int main()
{
    char str[N];
    printf("Please input a string with space:");
    gets(str);
    delSpace(str);
    printf("After deleting space:%s\n",str);
    return 0;
}