#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win(void) {
    system("/bin/sh");
}

int main(void) {
    char buf[0x20];

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("name: ");
    read(0, buf, 0x100);
    printf("hello, %s", buf);

    printf("name again: ");
    read(0, buf, 0x100);

    return 0;
}
