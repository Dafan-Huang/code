#include<stdio.h>
#include<math.h>
int main()
{
	int x,a,b,c=0;
	scanf("%d%d",&a,&b);
	if(10<=a&&a<=b&&b<=1000)
	{
	for(x=a;x<=b;x+=1)
	{
	   int i,k;
	   k=(int)sqrt(x);
	   for(i=2;i<=k;i++)
	   {
		   if(x%i==0)
		   {
			   break;
		   }
	   }
		if (i>k)
		{
			printf("%d ",x);
			c++;
			if (c%5==0)
			{
				printf("\n");
			}
		}
	 }
	}
	else
	{
		printf("no\n");
	}
	return 0;
}