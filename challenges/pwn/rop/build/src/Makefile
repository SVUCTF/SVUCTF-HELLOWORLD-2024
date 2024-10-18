CC = gcc
CFLAGS = -Wall -Wextra -Wpedantic -no-pie -fno-stack-protector -m64

TARGET = rop

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
