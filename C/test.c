//统计一行字符中字母，数字，空格和其他字符的个数
#include <stdio.h>

int main()
{
	//char line[150];
	int line[150];
	int i, alphabets, digits, spaces, others;

	alphabets = digits = spaces = others = 0;

	printf("Enter a line of string: ");

	line[0]=getchar();
	if (line[0]>=48 && line[0]<=57)
	{
		digits++;
	}
	printf("Digits: %d\n", digits);
	
	// for ( i = 0; i < 150; i++)
	// {
	// 	if ((line[i] >= 'a' && line[i] <= 'z') || (line[i] >= 'A' && line[i] <= 'Z'))
	// 	{
	// 		alphabets++;
	// 	}
	// 	else if (line[i] >= '0' && line[i] <= '9')
	// 	{
	// 		digits++;
	// 	}
	// 	else if (line[i] == ' ')
	// 	{
	// 		spaces++;
	// 	}
	// 	else
	// 	{
	// 		others++;
	// 	}
	// }
	

	// gets(line);

	// for(i=0; line[i]!='\0'; ++i)
	// {
	// 	if((line[i]>='a' && line[i]<='z') || (line[i]>='A' && line[i]<='Z'))
	// 	{
	// 		++alphabets;
	// 	}
	// 	else if(line[i]>='0' && line[i]<='9')
	// 	{
	// 		++digits;
	// 	}
	// 	else if(line[i]==' ')
	// 	{
	// 		++spaces;
	// 	}
	// 	else
	// 	{
	// 		++others;
	// 	}
	// }

	printf("Alphabets: %d\n", alphabets);
	printf("Digits: %d\n", digits);
	printf("White spaces: %d\n", spaces);
	printf("Other characters: %d\n", others);
	return 0;
}