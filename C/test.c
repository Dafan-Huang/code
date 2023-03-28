#include<stdio.h>
void menu()
{
    printf("This is a menu\n");
    choice();
}
void choice()
{
    int i;
    scanf("%d",&i);
    switch(i)
    {
        case 1:
            printf("you choose 1\n");
            system("pause");
            break;
        case 2:
            printf("you choose 2\n");
            system("pause");
            break;
        case 0://回到主菜单
            menu();
            break;
        default:
            menu();
            break;
    }
    menu();
}
int main()
{
    menu();
    choice();
    return 0;
}