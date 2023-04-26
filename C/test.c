//最大公约数
#include <stdio.h>
int main()
{
	int a,b;
	int i;
	int max;
	printf("Please input two numbers:");
	scanf("%d %d",&a,&b);
	if(a>b)
	{
		max=b;
	}
	else
	{
		max=a;
	}
	for(i=max;i>0;i--)
	{
		if(a%i==0&&b%i==0)
		{
			printf("The greatest common divisor is %d",i);
			break;
		}
	}
	return 0;
}