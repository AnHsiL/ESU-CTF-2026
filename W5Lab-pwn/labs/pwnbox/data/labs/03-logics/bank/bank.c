#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int balance = 100;
    unsigned int amount;

    setvbuf(stdout, NULL, _IONBF, 0);
    puts("== bank ==");
    printf("balance: %d\n", balance);

    printf("withdraw: ");
    if (scanf("%u", &amount) != 1)
        return 0;

    if ((int)amount > balance) {
        puts("insufficient funds");
        return 0;
    }

    balance -= amount;
    printf("balance: %d\n", balance);

    if (balance >= 1000000) {
        puts("premium member");
        system("/bin/sh");
    }

    return 0;
}
