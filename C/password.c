#include <stdio.h>
#include <conio.h>

int main() {
    char password[100];
    int i = 0;
    char ch;

    printf("Enter password: ");

    while ((ch = _getch()) != '\r') { // '\r' is the Enter key
        if (ch == '\b') { // Handle backspace
            if (i > 0) {
                i--;
                printf("\b \b");
            }
        } else {
            password[i++] = ch;
            printf("*");
        }
    }
    password[i] = '\0'; // Null-terminate the string

    printf("\nYour password is: %s\n", password);

    return 0;
}