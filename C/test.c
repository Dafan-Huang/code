//随机生成一百个数,并且每十个数换行,并且每个数之间用逗号隔开
//输出到文件中
//读文件判断数组中是否存在某个数（50）
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 100

void bubble_sort(int a[], int n)//冒泡排序
{
	int i, j, t;
	for (i = 0; i < n - 1; i++)
	{
		for (j = n - 1; j > i; j--)
		{
			if (a[j - 1] > a[j])
			{
				t = a[j - 1];
				a[j - 1] = a[j];
				a[j] = t;
			}
		}
	}
}

void output(int a[],int n)//输出
{
	int i;
	for(i=0;i<n;i++)
	{
		printf("%5d,",a[i]);
		if((i+1)%10==0)
			printf("\n");
	}
	printf("\n");
}

void output_file(int a[],int n)//输出到文件
{
	int i;
	FILE *fp;
	if((fp=fopen("./test.txt","w"))==NULL)
	{
		printf("error\n");
		exit(0);
	}
	for(i=0;i<n;i++)
	{
		fprintf(fp,"%5d,",a[i]);
		if((i+1)%10==0)
			fprintf(fp,"\n");
	}
	fprintf(fp,"\n");
	fclose(fp);
}

void read_file(int a[],int n)//读文件
{
	int i;
	FILE *fp;
	if((fp=fopen("test.txt","r"))==NULL)
	{
		printf("error\n");
		exit(0);
	}
	for(i=0;i<n;i++)
	{
		fscanf(fp,"%d,",&a[i]);
	}
	fclose(fp);
}

int main()
{
	int i, a[N];
	int j=0;
	srand(time(NULL));
	for (i = 0; i < N; i++)
	{
		a[i] = rand() % 10000;
	}
	output(a,N);
	bubble_sort(a, N);
	output(a,N);
	output_file(a,N);
	return 0;
}

void hello()
{
	printf("hello world\n");
	return 0;
}