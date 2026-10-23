CC     := gcc
TARGET := shellcode

all: $(TARGET)

$(TARGET): shellcode.c
	$(CC) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
