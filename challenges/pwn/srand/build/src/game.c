#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_NUMBER 99999

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void banner() {
    printf(" ___  *  *  **  **  ___  ____  ____ \n");
    printf("/ **)( \\/ )(  )(  )/ **)(_  *)( *__)\n");
    printf("\\__ \\ \\  /  )(__)(( (__   )(   )__) \n");
    printf("(___/  \\/  (______)\\___) (__) (__) \n");
    printf("\n");
    printf("Welcome to the SVUCTF HELLOWORLD 2024!\n");
    printf("\n");
}

void game() {
    int secret_number = rand() % MAX_NUMBER + 1;
    int guess;

    printf("I've thought of a number between 1 and %d.\n", MAX_NUMBER);
    printf("You have only one chance to guess this number. Good luck!\n\n");
    printf("Please enter your guess: ");

    if (scanf("%d", &guess) != 1) {
        printf("Invalid input, game over.\n");
        return;
    }

    if (guess == secret_number) {
        printf("\nCongratulations! You've guessed the number %d!\n",
               secret_number);
        system("/bin/sh");
    } else {
        printf(
            "\nSorry, you didn't guess correctly. The right number was %d.\n",
            secret_number);
    }
}

int main() {
    srand(time(NULL));
    init();
    banner();
    game();
    return 0;
}
