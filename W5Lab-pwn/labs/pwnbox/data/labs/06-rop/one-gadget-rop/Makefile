CC     := gcc
CFLAGS := -fno-stack-protector -no-pie
TARGET := one-gadget-rop

all: $(TARGET)

$(TARGET): one-gadget-rop.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
