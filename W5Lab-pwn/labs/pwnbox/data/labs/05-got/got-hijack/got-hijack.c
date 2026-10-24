#include <stdio.h>
#include <stdlib.h>

void win(void) {
    system("/bin/sh");
}

int main(void) {
    unsigned long addr;
    unsigned long val;

    setvbuf(stdout, NULL, _IONBF, 0);

    printf("win: %p\n", win);

    printf("addr: ");
    if (scanf("%lx", &addr) != 1)
        return 0;

    printf("val: ");
    if (scanf("%lx", &val) != 1)
        return 0;

    *(unsigned long *)addr = val;

    puts("bye");
    return 0;
}
