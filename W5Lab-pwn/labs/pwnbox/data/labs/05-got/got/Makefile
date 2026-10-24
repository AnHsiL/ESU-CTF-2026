CC     := gcc
CFLAGS := -no-pie
TARGET := got

all: $(TARGET)

$(TARGET): got.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
