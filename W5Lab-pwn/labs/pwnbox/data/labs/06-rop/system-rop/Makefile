CC     := gcc
CFLAGS := -fno-stack-protector -no-pie
TARGET := system-rop

all: $(TARGET)

$(TARGET): system-rop.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
