CC = gcc
CFLAGS = -Wall -Wextra -Wpedantic -no-pie -fno-stack-protector -m64

TARGET = ret2text64

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
