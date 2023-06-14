#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int rolling();

int main()
{
    int a[11]={2,3,4,5,6,7,8,9,10,11,12};
    int count[11]={0};

    srand(time(NULL)); // seed the random number generator

    for (int i = 0; i < 10000; i++)
    {
                int result = rolling();
                if (result == a[result-2])
                {
                    count[result-2]++;
                }   
            }

            for (int i = 0; i < 11; i++)
            {
                printf("%d\t",a[i]);
            }

            printf("\n");

            for (int k = 0; k < 11; k++)
            {
                printf("%d\t",count[k]);
            }
            
            return 0;
        }

        int rolling()
        {
            int dice1, dice2, sum;
            
            // 生成两个随机数，模拟扔两个骰子
            dice1 = rand() % 6 + 1;
            dice2 = rand() % 6 + 1;
            
            // 计算两个骰子的点数之和
            sum = dice1 + dice2;
            return sum;        
        }

