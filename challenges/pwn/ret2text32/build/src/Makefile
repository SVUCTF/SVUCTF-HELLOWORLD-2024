CC = gcc-4.8
CFLAGS = -Wall -Wextra -Wpedantic -fno-stack-protector

TARGET = ret2text32

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
