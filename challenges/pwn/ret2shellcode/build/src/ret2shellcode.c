#include <stdio.h>
#include <sys/mman.h>
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

void vuln() {
    char* buf = mmap(NULL, 0x100, PROT_READ | PROT_WRITE | PROT_EXEC,
                     MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    puts("Send me shellcode:");
    read(0, buf, 0x100);
    ((void (*)(void))buf)();
}

int main() {
    init();
    banner();
    vuln();
    return 0;
}
