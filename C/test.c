#include <stdio.h>
#include <stdlib.h>
int find(int* list, int len) {
    if (len<3)
    {
        return 0;
    }
    
	int i = 0, j = 0;
	int count[2] = { 0 };
	int* a = (int*)malloc(len * sizeof(int));
	int* b = (int*)malloc(len * sizeof(int));
	int sum = 0;
	int third;
	int twoThird;
	for (i = 0;i < len;i++) {
		sum += list[i];
		list[i] = sum;
	}
	if (sum == 0) {
		for (i = 0;i < len-1;i++) {
			if (list[i] == 0)sum++;
		}
		return sum * (sum - 1) / 2;
	}
	if (sum % 3 != 0)return 0;
	third = sum / 3;
	twoThird = third * 2;
	sum = 0;
	for (int i = 0;i < len;i++) {
		if (list[i] == third) {
			a[count[0]] = i;
			count[0]++;
		}
		if (list[i] == twoThird) {
			b[count[1]] = i;
			count[1]++;
		}
	}
	for (i = 0;i < count[0];i++) {
		for (j = 0;j < count[1];i++) {
			if (a[i] < b[j]) {
				sum +=(count[1] - j);
				break;
			}
		}
	}
	return sum;
}

int main()
{
    int n;//数组长度
    scanf("%d",&n);//输入数组长度
    int a[n];//数组
    int i;//循环变量
    for(i=0;i<n;i++)
    {
        scanf("%d",&a[i]);//输入数组元素
    }
    printf("%d",find(a,n));//调用函数
    return 0;
}