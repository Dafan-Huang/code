#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define N 2080000
int main()
{
    char a[N];
    static b[2];
    int i,j;
    int count=0;
    srand(time(NULL));
    for ( i = 0; i < N; i++)
    {
        j=rand()%2;
        b[j]++;
    }
    for ( i = 0; i < 2; i++)
    {
        printf("%d--%2d\n",i,b[i]);
    }
    return 0;
}