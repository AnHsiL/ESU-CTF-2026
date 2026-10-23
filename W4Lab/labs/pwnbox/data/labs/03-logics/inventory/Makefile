CC     := gcc
TARGET := inventory

all: $(TARGET)

$(TARGET): inventory.c
	$(CC) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
