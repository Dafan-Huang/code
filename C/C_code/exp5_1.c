#include<stdio.h>
#define N 10

void input(int array[],int n)
{
    int i;
    printf("please intput %d numbers:",n);
    for ( i = 0; i < n; i++)
    {
        scanf("%5d",&array[i]);
    }
    printf("\n");
}

void output(int array[],int n)
{
    int i;
    printf("The elements are:");
    for ( i = 0; i < n; i++)
    {
        printf("%5d",array[i]);
    }
    printf("\n");
}

int maxnum(int array[],int n)
{
    int i,max;
    max=array[0];
    for ( i = 1; i < n; i++)
    {
        if (array[i]>max)
        {
            max=array[i];
        }
    }
    return max;
}

int minnum(int a[],int n)
{
    int i,min;
    min=a[0];
    for ( i = 1; i < n; i++)
    {
        if (a[i]<min)
        {
            min=a[i];
        }
    }
    return min;
}

int find(int a[],int n,int x)
{
    int i=0;
    while (i<n)
    {
        if (x==a[i])
        {
            break;
        }
        i++;
    }
    return i;
}

double average(int array[],int n)
{
    int i,sum=0;
    for ( i = 0; i < n; i++)
    {
        sum+=array[i];
    }
    return sum*1.0/n;
}

void sort(int array[],int n)
{
    int i,j,temp;
    for ( i = 0; i < n-1; i++)
    {
        for ( j = n-1; j >i; j--)
        {
            if (array[j]<array[j-1])
            {
                temp=array[j-1];
                array[j-1]=array[j];
                array[j]=temp;
            }            
        }        
    }   
}
int main()
{
    int array[N],x,n,pos,max,min;
    double ave=0;
    do
    {
        printf("please enter the number of elements(1<=number<=10)\n");
        scanf("%d",&n);
    } while (n<1||n>N);
    input(array,n);
    output(array,n);
    ave=average(array,n);
    printf("The average is %f",ave);
    max=maxnum(array,n);
    printf("The Maxnum is %d\n",max);
    min=minnum(array,n);
    printf("The Minnum is %d\n",min);
    printf("please input x be searched:");
    scanf("%d",&x);
    pos=find(array,n,x);
    if (pos<n)
    {
        printf("value=%d,index=%d\n",x,pos);
    }
    else
    {
        printf("Not present");
    }
    printf("new order");
    sort(array,n);
    output(array,n);
    printf("\n");
    return 0;
}