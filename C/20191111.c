#include<stdio.h>
#define N 5
typedef struct mobile
{
    char type[20];
    int price;
    int sale;
    int income;
}mobile;

void input(mobile *a,int n)
{
    int i;
    for ( i = 0; i < n; i++)
    {
        scanf("%s",&a[i].type);
        scanf("%d",&a[i].price);
        scanf("%d",&a[i].sale);
       a[i].income=a[i].price*a[i].sale;
    }
}

void sort(mobile*a,int n)
{
    int index,i,k,temp;
    for ( k = 0; k < n-1; k++)
    {
        index=k;
        for ( i = k+1; i < n; i++)
        {
            if (a[i].income>a[index].income)
            {
                index=i;
            }
            if (index!=k)
            {
                temp=a[index].income;
                a[index].income=a[k].income;
                a[k].income=temp;
            }
        }
    }
}

void output(mobile*a,int n)
{
    int i;
    for ( i = 0; i < n; i++)
    {
        puts(a[i].type);
        printf("%10d\n",a[i].income);
    }
    
}

int main()
{
    mobile m[N];
    input(m,N);
    sort(m,N);
    output(m,N);
    return 0;
}