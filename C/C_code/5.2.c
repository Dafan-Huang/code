#include<stdio.h>
#include<math.h>
double volume(double r,double h,double v);
double area(double r,double h,double s);

int main()
{
    const double pi=3.14;
    double r,h,s,v;
    scanf("%lf%lf",&r,&h);
    s=area(r,h,s);
    v=volume(r,h,v);
    printf("radius=%lf, height=%lf, Area of surface=%lf, Volume=%lf\n",r,h,s,v);
    return 0;
}

double volume(double r,double h,double v)
{
    const double pi=3.14;
    v=pi*r*r*h*1.0/3;
    return v;
}

double area(double r,double h,double s)
{
    const double pi=3.14;
    s=pi*r*r+pi*sqrt(h*h+r*r)*r;
    return s;
}