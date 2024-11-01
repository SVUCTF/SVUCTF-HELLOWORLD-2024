#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void banner() {
    printf(" ___  _  _  __  __  ___  ____  ____ \n");
    printf("/ __)( \\/ )(  )(  )/ __)(_  _)( ___)\n");
    printf("\\__ \\ \\  /  )(__)(( (__   )(   )__) \n");
    printf("(___/  \\/  (______)\\___) (__) (__) \n");
    printf("\n");
    printf("Welcome to the SVUCTF HELLOWORLD 2024!\n");
    printf("\n");
}

void b4ckd00r() {
    int fd = open("/dev/urandom", O_RDONLY);
    int secret_code;
    read(fd, &secret_code, sizeof(secret_code));
    close(fd);

    int user_input;
    scanf("%d", &user_input);

    if (user_input == secret_code) {
        system("/bin/sh");
    } else {
        puts("Hacker!");
    }
}

void vuln() {
    int data_size;
    char buf[32];

    puts("Welcome to the secret data vault!");
    puts("How much data do you want to store (in bytes)?");
    scanf("%d", &data_size);

    puts("Enter your secret data now:");
    read(0, &buf, data_size);
    puts("Data stored successfully!");
}

int main() {
    init();
    banner();
    vuln();
    return 0;
}
