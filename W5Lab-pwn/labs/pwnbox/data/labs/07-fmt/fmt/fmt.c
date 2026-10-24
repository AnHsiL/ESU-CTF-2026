#include <stdio.h>
#include <stdlib.h>

void win(void) {
    system("/bin/sh");
}

int main(void) {
    char buf[0x100];

    setvbuf(stdout, NULL, _IONBF, 0);

    while (1) {
        printf("> ");
        if (fgets(buf, sizeof(buf), stdin) == NULL)
            break;
        printf(buf);
    }

    return 0;
}
