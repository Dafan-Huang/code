#include<stdio.h>
#include<stdlib.h>
void writefile(int ch,FILE *fp);
void readfile(int ch,FILE *fp);
int main()
{
    FILE *fp;
    char ch=0;
    fp=fopen("D:\\f1.txt","w+");
    if (fp==NULL)
    {
        printf("file error!\n");
        exit(1);
    }
    writefile(ch,fp);
    rewind(fp);
    readfile(ch,fp);
    fclose(fp);
    return 0;
}
void writefile(int ch,FILE *fp)
{
    printf("Please enter a string of charters ending with '#'\n");
    ch=getchar();
    while (ch!='#')
    {
        fputc(ch,fp);
        ch=getchar();
    }
}
void readfile(int ch,FILE *fp)
{
    while ((ch=fgetc(fp))!=EOF)
    {
        putchar(ch);
    }
    printf("\n");
}