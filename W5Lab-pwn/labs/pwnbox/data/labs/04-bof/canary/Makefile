CC     := gcc
CFLAGS := -fstack-protector -no-pie
TARGET := canary

all: $(TARGET)

$(TARGET): canary.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
