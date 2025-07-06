#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    int dice, guess;
    srand(time(NULL)); // 初始化随机种子

    printf("猜测骰子点数（1-6），输入0结束游戏：\n");
    do {
        scanf("%d", &guess); // 输入猜测的点数
        if (guess == 0) // 如果输入0，结束游戏
            break;

        dice = rand() % 6 + 1; // 随机生成骰子点数
        printf("骰子点数为：%d\n", dice);

        if (dice == guess)
            printf("恭喜你猜对了！\n");
        else
            printf("很遗憾猜错了，再试一次吧。\n");
    } while (1);

    printf("游戏结束。\n");
    return 0;
}
