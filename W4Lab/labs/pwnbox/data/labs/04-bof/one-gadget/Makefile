CC     := gcc
CFLAGS := -fno-stack-protector -no-pie
TARGET := one-gadget

all: $(TARGET)

$(TARGET): one-gadget.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
