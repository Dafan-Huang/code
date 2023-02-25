#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int main()
{
    FILE *fp;//定义文件
    fp=fopen("D:\\file.txt","w");//打开文件
    /*打开方式有3*2*2种
    r 读    txt          rb 读      bat         
    w 写                 ……   
    a 追加
    r+ 读写打开
    w+ 读写新建
    a+ 读写追加
    */
    if(fp==NULL)
    {
        printf("打开文件失败\n");
        exit(1);
    }//判断是否正确打开

    //fgetc(fp)
    /*
    char ch;
    while ((ch=fgetc(fp))!=EOF)
    {
        putchar(ch);
    }
    */

    //fgets(str,读取的个数,fp)
    /*
    char str[200];
    while(fgets(str,200,fp))
    {
        puts(str);
    }
    */

    //fread(buffer,size,n,fp)
    /*
    char str[200];
    fread(str,sizeof(str),1,fp);
    puts(str);
    */

    //fscanf(fp,格式控制字符串，地址)
    /*
    char str[100];
    fscanf(fp,"%s",&str);
    puts(str);
    */

    //fputc(字符,fp)
    //fputc('a',fp);

    //fputs(str,fp)
    /*
    char str[100]="132abc";
    fputs(str,fp);
    */

    //fwrite(buffer,size,n,fp)
    int number =114;
    int n;
    fwrite(&number,sizeof(number),1,fp);
    rewind(fp);
    fread(n,sizeof(number),1,fp);
    printf("%d",n);    
    fclose(fp);//关闭文件
    return 0;
}