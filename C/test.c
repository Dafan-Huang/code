#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    int dice1, dice2, sum;
    
    // 用当前时间初始化随机数生成器
    srand(time(NULL));
    
    // 生成两个随机数，模拟扔两个骰子
    dice1 = rand() % 6 + 1;
    dice2 = rand() % 6 + 1;
    
    // 计算两个骰子的点数之和
    sum = dice1 + dice2;
    
    // 显示结果
    printf("first:%d\n", dice1);
    printf("second:%d\n", dice2);
    printf("sum is :%d\n", sum);
    
    return 0;
}