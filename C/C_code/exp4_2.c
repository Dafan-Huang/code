#include<stdio.h>
void Drawtriangle(int n,char c)
{
    int i,j;
    for ( i = 1; i <=n; i++)
    {
        for ( j = 1; j<=n-i; j++)
        {
            printf(" ");
        }
        for ( j = 1; j<=2*i-1; j++)
        {
            printf("%c",c);
        }
        printf("\n");
    }
    return;
} 
int main()
{   int n;
    char c;
    scanf("%d%c",&n,&c);
    Drawtriangle(n,c);
    return 0;
}