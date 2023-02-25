#include<stdio.h>
#include<string.h>

int main()
{
    char str[20];
    gets(str);
    int i=0,j=0;
    while (str[i]!='\0')
    {
        if (str[i]<'0'||str[i]>'9')
        {
            for ( j = i; j < strlen(str); j++)
            {
                str[j]=str[j+1];
            }
        }
        else
        {
            i++;
        }
    }
    puts(str);
    return 0;
}