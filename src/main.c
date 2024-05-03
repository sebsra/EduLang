#include "compiler.h"
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror("Error opening file");
            return 1;
        }
    }

    yyparse();

    if (yyin) {
        fclose(yyin);
    }

    return 0;
}
