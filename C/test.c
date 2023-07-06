//office
#include <stdio.h>
#include <stdlib.h>

int main(){
    //输出菱形
    int i,j,k;
    for(i=1;i<=4;i++){
        for(j=1;j<=4-i;j++){
            printf(" ");
        }
        for(k=1;k<=2*i-1;k++){
            printf("*");
        }
        printf("\n");
    }
    for(i=1;i<=3;i++){
        for(j=1;j<=i;j++){
            printf(" ");
        }
        for(k=1;k<=7-2*i;k++){
            printf("*");
        }
        printf("\n");
    }
}