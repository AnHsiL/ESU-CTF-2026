#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>

int main(void) {
    void *buf = mmap(NULL, 0x1000,
                     PROT_READ | PROT_WRITE | PROT_EXEC,
                     MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    printf("> ");
    fflush(stdout);
    read(0, buf, 0x1000);

    ((void (*)(void))buf)();
    return 0;
}
