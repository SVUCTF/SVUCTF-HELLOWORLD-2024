CC = gcc
CFLAGS = -Wall -Wextra -Wpedantic -no-pie -m64

TARGET = rop

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
