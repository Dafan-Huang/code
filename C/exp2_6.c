#include<stdio.h>
#include<math.h>
int main()
{
    double a,b,c,t;
    scanf("%lf%lf%lf",&a,&b,&c);
    if(a>b)
    {
        t=a;a=b;b=t;
    }
    if (a>c)
    {
        t=a;a=c;c=t;
    }
    if (b>c)
    {
        t=b;b=c;c=t;
    }
if (a<=0||b<=0||c<=0)
{
    printf("Error input!\n");
    return 0;
}
if (a+b>c&&a+c>b&&b+c>a)
{
if (a*a+b*b-c*c<1e-1)
{
    if (a==b)
    {
        printf("%f,%f,%f is a Isosceles triangle.\n",a,b,c);
        return 0;
    }
    else
    {
        printf("%f,%f,%f is a right triangle.\n",a,b,c);
    }
    
}
else
{
    if (a==b||b==c)
    {
        if (b==c)
        {
            printf("%f,%f,%f is a equilateral triangle.\n",a,b,c);
        }
        else
        {
            printf("%f,%f,%f is a isosceles triangle.\n",a,b,c);
        }
        
    }
    else
    {
        printf("%f,%f,%f is a triangle.\n",a,b,c);
    }
    
}
}
else 
{
    printf("%f,%f,%f is not a triangle.\n",a,b,c);
}
    return 0;
}