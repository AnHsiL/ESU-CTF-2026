#include <stdio.h>
#include <stdlib.h>

struct inventory {
    int is_admin;
    int qty[8];
};

int main(void) {
    struct inventory inv = {0};
    int idx;
    int val;

    setvbuf(stdout, NULL, _IONBF, 0);
    puts("== warehouse ==");

    while (1) {
        printf("slot: ");
        if (scanf("%d", &idx) != 1)
            break;
        if (idx > 7) {
            puts("slot out of range");
            continue;
        }
        printf("qty: ");
        if (scanf("%d", &val) != 1)
            break;

        inv.qty[idx] = val;
        printf("slot %d = %d\n", idx, inv.qty[idx]);

        if (inv.is_admin) {
            puts("welcome, admin");
            system("/bin/sh");
            return 0;
        }
    }

    puts("bye");
    return 0;
}
