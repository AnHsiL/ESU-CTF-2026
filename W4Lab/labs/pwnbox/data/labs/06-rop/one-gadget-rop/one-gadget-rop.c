#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void) {
    char buf[0x20];

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("gift: %p\n", printf);
    printf("name: ");
    read(0, buf, 0x200);

    return 0;
}
