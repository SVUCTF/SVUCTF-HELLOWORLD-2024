#include <stdio.h>
#include <stdlib.h>
#include <time.h>

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

void backdoor() {
    system("/bin/sh");
}

void vuln() {
    char buf[100];
    puts("There is something amazing here, do you know anything?");
    gets(buf);
    puts("Maybe I will tell you next time !");
}

int main() {
    init();
    banner();
    vuln();
    return 0;
}
