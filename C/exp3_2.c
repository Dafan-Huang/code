#include <stdio.h>
#include <string.h>

int main()
{
    char user[]={"huangdafan"},*user1;
    int password=1,password1;
    int n=0;
    do
    {   scanf("%d",&password1);
        scanf("%s",user1);
        if (!strcmp(user,user1)&&password1==password)
        {
            printf("1");
            break;
        }
        else
        {
            printf("0");
            n++;
        } 
        
    } while (n<3);
    
        
        
}