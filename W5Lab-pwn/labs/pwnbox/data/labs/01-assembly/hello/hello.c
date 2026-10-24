#include <unistd.h>

int main(void) {
    char buf[0x20];
    ssize_t n;

    write(1, "Name: ", 6);
    n = read(0, buf, sizeof(buf));
    write(1, "Hello, ", 7);
    write(1, buf, n);
    return 0;
}
