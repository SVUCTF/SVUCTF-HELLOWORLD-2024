#include <stddef.h>
#include <stdio.h>

#define FLAG_LENGTH 23
#define KEY(i) ((i * 7) % 256)

int main(void) {
    const unsigned char enc_data[FLAG_LENGTH] = {
        0x66, 0x6b, 0x6f, 0x72, 0x67, 0x7a, 0x1a, 0x44, 0x67, 0x7c, 0x72, 0x23,
        0x0b, 0x18, 0x3d, 0x58, 0x04, 0x28, 0x30, 0xb5, 0xfb, 0xb2, 0xe7};
    char flag[FLAG_LENGTH + 1];

    for (size_t i = 0; i < FLAG_LENGTH; i++) {
        flag[i] = enc_data[i] ^ KEY(i);
    }
    flag[FLAG_LENGTH] = '\0';

    printf("%s\n", flag);
    return 0;
}
