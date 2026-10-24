CC     := gcc
CFLAGS := -no-pie
TARGET := got-hijack

all: $(TARGET)

$(TARGET): got-hijack.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
