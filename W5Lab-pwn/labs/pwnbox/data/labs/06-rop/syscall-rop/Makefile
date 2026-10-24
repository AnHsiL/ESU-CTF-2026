CC     := gcc
CFLAGS := -fno-stack-protector -no-pie
TARGET := syscall-rop

all: $(TARGET)

$(TARGET): syscall-rop.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
