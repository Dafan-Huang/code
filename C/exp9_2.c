#include<stdio.h>
#include<stdlib.h>
struct Student
{
	char ID[20];
	char name[30];
	int age;
	double score;
};
typedef struct Student Stu;
#define N 50
void CreateFile(Stu [],int n,FILE *fp);
void ReadOut(Stu [],int n,FILE *fp);
void Sort(Stu [],int len);
int main()
{
	int n,i,x;
	Stu stu[N];
	FILE *fp=NULL;                       
	do
	{
		printf("Please input the number of students:\n");
	    scanf("%d",&n);
	}while(n<1||n>40);
	for(i=0;i<n;i++)
	{
		x=i+1;
		printf("%d(ID name age score):\n",x);
		scanf("%s%s%d%lf",stu[i].ID,stu[i].name,&stu[i].age,&stu[i].score);
	}
	CreateFile(stu,n,fp);
	printf("before being sorted:\n");
	ReadOut(stu,n,fp);
	printf("after being sorted:\n");
    Sort(stu,n);
	return 0;
}
void CreateFile(Stu stu[],int n,FILE *fp)
{
	fp=fopen("D:\\Info.dat","wb+");
	if(fp==0)                       
	{
		printf("file error\n");
		exit(1);
	}
	fwrite(stu,sizeof(Stu),n,fp);
	fclose(fp);
}
void ReadOut(Stu stu[],int n,FILE *fp)
{
	int i=0;
	fp=fopen("D:\\Info.dat","rb");
	if(fp==0)                      
	{
		printf("file error\n");
		exit(1);
	}
	fread(&stu[i],sizeof(Stu),n,fp);
	for(i=0;i<n;i++)
		printf("%s %s %d %.2f\n",stu[i].ID,stu[i].name,stu[i].age,stu[i].score);
	fclose(fp);
}
void Sort(Stu stu[],int len)
{
	int i,k,index;
	Stu temp;
	for(k=0;k<len-1;k++)
	{
		index=k;
		for(i=k+1;i<len;i++)
			if(stu[i].score>stu[index].score)
				index=i;
		if(index!=k)
		{
			temp=stu[index];
			stu[index]=stu[k];
			stu[k]=temp;
		}
	}
	for(i=0;i<len;i++)
		printf("%s %s %d %.2f\n",stu[i].ID,stu[i].name,stu[i].age,stu[i].score);
}
