CC     := gcc
CFLAGS := -fno-stack-protector
TARGET := pie

all: $(TARGET)

$(TARGET): pie.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
