#include "edulang.h"
#include <stdio.h>
#include <string.h>

int debug = 0; // Debug flag is off by default

int main(int argc, char **argv) {

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-d") == 0 || strcmp(argv[i], "--debug") == 0) {
            debug = 1; // Turn on debug flag
        } else {
            yyin = fopen(argv[i], "r");
            if (!yyin) {
                perror("Error opening file");
                return 1;
            }
        }
    }

    yyparse();

    if (yyin) {
        fclose(yyin);
    }

    return 0;
}