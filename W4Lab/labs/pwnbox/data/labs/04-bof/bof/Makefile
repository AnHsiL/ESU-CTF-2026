CC     := gcc
CFLAGS := -fno-stack-protector -no-pie
TARGET := bof

all: $(TARGET)

$(TARGET): bof.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
