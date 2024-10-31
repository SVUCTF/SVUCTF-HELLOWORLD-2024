#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SWAP(a, b)              \
    {                           \
        unsigned char temp = a; \
        a = b;                  \
        b = temp;               \
    }

static const unsigned char KEY[] = "svuctf";
static const int KEY_LEN = 6;
static const char base64_chars[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

void base64_encode(const unsigned char* input, char* output, int input_len) {
    int i, j;
    unsigned char current;

    for (i = 0, j = 0; i < input_len; i += 3) {
        // 第一个6位
        current = (input[i] >> 2);
        output[j++] = base64_chars[current & 0x3F];

        // 第二个6位
        current = (input[i] << 4) & 0x30;
        if (i + 1 >= input_len) {
            output[j++] = base64_chars[current & 0x3F];
            output[j++] = '=';
            output[j++] = '=';
            break;
        }
        current |= (input[i + 1] >> 4) & 0x0F;
        output[j++] = base64_chars[current & 0x3F];

        // 第三个6位
        current = (input[i + 1] << 2) & 0x3C;
        if (i + 2 >= input_len) {
            output[j++] = base64_chars[current & 0x3F];
            output[j++] = '=';
            break;
        }
        current |= (input[i + 2] >> 6) & 0x03;
        output[j++] = base64_chars[current & 0x3F];

        // 第四个6位
        current = input[i + 2] & 0x3F;
        output[j++] = base64_chars[current];
    }
    output[j] = '\0';
}

void init(const unsigned char* key, unsigned char* S, int key_len) {
    // 初始化S盒
    for (int i = 0; i < 256; i++) {
        S[i] = i;
    }

    // 按密钥打乱S盒
    int j = 0;
    for (int i = 0; i < 256; i++) {
        j = (j + S[i] + key[i % key_len]) & 0xFF;
        SWAP(S[i], S[j]);
    }
}

void encrypt(unsigned char* data, unsigned char* S, int data_len) {
    int i = 0, j = 0;

    for (int n = 0; n < data_len; n++) {
        i = (i + 1) & 0xFF;
        j = (j + S[i]) & 0xFF;
        SWAP(S[i], S[j]);
        unsigned char K = S[(S[i] + S[j]) & 0xFF];
        data[n] ^= K;
    }
}

int main() {
    unsigned char data[256];
    unsigned char S[256];
    const char* expected_encoded =
        "cShiGz8rdlXyFRggqjmEyOm4S5dblDTev+C5AM3FlRc=";

    printf("Input flag: ");
    fgets((char*)data, sizeof(data), stdin);
    data[strcspn((char*)data, "\n")] = '\0';

    int data_len = strlen((char*)data);

    init(KEY, S, KEY_LEN);
    encrypt(data, S, data_len);

    size_t encoded_size = 4 * ((data_len + 2) / 3) + 1;
    char* encoded_data = malloc(encoded_size);
    base64_encode(data, encoded_data, data_len);

    if (strcmp(encoded_data, expected_encoded) == 0) {
        printf("Congratulations!\n");
    } else {
        printf("Try again!\n");
    }

    free(encoded_data);
    return 0;
}
