#include<stdio.h>
#define size 10


void print(int a[],int n)
{
    int i;
    printf("The array is:\n");
    for ( i = 0; i < n; i++)
    {
        printf("%5d",a[i]);
    }
    printf("\n");
}

void Bubblesort(int a[],int n)
{
    int i,j,temp;
    for ( i = 0; i < n; i++)
    {
        for ( j = n-1; j >i ; j--)
        {
            if (a[j]<a[j-1])
            {
                temp=a[j-1];
                a[j-1]=a[j];
                a[j]=temp;
            }
        }
    }   
}
int main()
{
    int array[size],i=0,n;
    do
    {
        printf("Please input n(1<=n<=%d):",size);
        scanf("%d",&n);
    } while (n<1||n>size);
    printf("Please input %d elements:",n);
    for ( i = 0; i < n; i++)
    {
        scanf("%d",&array[i]);
    }
    Bubblesort(array,n);
    print(array,n);
    return 0;
}