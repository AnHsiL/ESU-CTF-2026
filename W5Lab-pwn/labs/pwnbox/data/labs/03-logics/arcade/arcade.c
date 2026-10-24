#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    int guess;
    int i;

    setvbuf(stdout, NULL, _IONBF, 0);
    srand(time(NULL));

    puts("== arcade ==");
    puts("win 3 rounds in a row");

    for (i = 0; i < 3; i++) {
        int target = rand() % 100;

        printf("round %d, guess: ", i + 1);
        if (scanf("%d", &guess) != 1)
            return 0;

        if (guess != target) {
            printf("wrong, it was %d\n", target);
            return 0;
        }
        puts("correct");
    }

    puts("jackpot");
    system("/bin/sh");
    return 0;
}
