#include<stdio.h>
void paixu(int a[])
{
    int i,j,temp;
    for ( i = 0; i<9; i++)
        for ( j =9; j>i;j--)
        {
            if (a[j]<a[j-1])
            {
                temp=a[j-1];
                a[j-1]=a[j];
                a[j]=temp;
            }
        }        
}
int main()
{
    int i,a[10],n;
    double sum=0,ave;
    for ( i = 0; i <10; i++)
    {
        scanf("%d",&a[i]);
    }
    paixu(a); 
    int count1=1,count2=1;
    int j,k;
    for ( j = 1; j <10 ; j++)
    {
        if (a[j]==a[0])
        {
            a[j]=0;
            count1++;
        }
        else
        {
            break;
        }
    }
    for ( k = 8; k>0; k--)
    {
        if (a[k]==a[9])
        {
            a[k]=0;
            count2++;
        }
        else
        {
            break;
        }
    }
    a[0]=0;a[9]=0;
   /* for ( i = 0; i < 10; i++)
    {
        printf("%d ",a[i]);
    }*///调试用
    
   for ( i = 0; i <10; i++)
    {
        sum+=a[i];
    }
    ave=sum/(10-count1-count2);
    printf("%lf\n",ave);
    return 0;
}