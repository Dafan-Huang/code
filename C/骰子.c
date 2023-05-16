//扔两颗骰子猜点数，扔5次，统计最终结果
#include<stdio.h>
#include<stdlib.h>
#include<time.h>

int main()
{
    int i, j, k, n, m, a[11] = { 0 };
    srand(time(NULL));
    for (i = 0; i < 5; i++)
    {
        n = rand() % 6 + 1;
        m = rand() % 6 + 1;
        k = n + m;
        a[k - 2]++;
    }
    for (i = 0; i < 11; i++)
    {
        printf("%d点出现的次数为%d\n", i + 2, a[i]);
    }
    return 0;
}