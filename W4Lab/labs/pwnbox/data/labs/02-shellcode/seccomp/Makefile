CC     := gcc
LDLIBS := -lseccomp
TARGET := seccomp

all: $(TARGET)

$(TARGET): seccomp.c
	$(CC) -o $@ $< $(LDLIBS)

clean:
	rm -f $(TARGET)

.PHONY: all clean
