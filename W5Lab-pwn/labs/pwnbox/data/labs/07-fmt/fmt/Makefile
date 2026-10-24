CC     := gcc
CFLAGS := -fno-stack-protector -no-pie
TARGET := fmt

all: $(TARGET)

$(TARGET): fmt.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
