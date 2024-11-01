#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char secret[] = "/bin/sh";

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

void vuln() {
    char buf[64];
    system("echo \"Hello CTFer, what's your name?\"");
    read(0, &buf, 256);
}

int main() {
    init();
    banner();
    vuln();
    return 0;
}
