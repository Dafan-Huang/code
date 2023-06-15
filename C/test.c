#include <stdio.h>

int main() {
    char c;
    FILE* fp;

    fp = fopen("test.c.txt", "w");

    printf("Please enter characters, end with # :\n");

    while ((c = getchar()) != '#') {
        fputc(c, fp);
        putchar(c);
    }

    fclose(fp);

    return 0;
}