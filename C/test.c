//统计字符串中a的数量
#include <stdio.h>
#include <string.h>
int main()
{
	char str[100];
	int i, count = 0;
	printf("Please input a string:");
	gets(str);//gets()函数用于从标准输入(stdin)读取一行，并把它存储在str所指向的字符串内，直到一个终止符或EOF(End Of File)。
	for (i = 0; i < strlen(str); i++)
	{
		if (str[i] == 'a')//strlen()函数用于计算字符串的长度，不包括字符串的结束符。
		{
			count++;
		}
	}
	printf("a num is :%d", count);//printf()函数用于格式化输出
	return 0;
}