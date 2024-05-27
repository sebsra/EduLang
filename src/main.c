#include "edulang.h"
#include <stdio.h>
#include <string.h>
#include<stdlib.h>
#include<ctype.h>
#include "functions.h"


extern char* yytext;
extern int lineCount;

int debug = 0; // Debug flag is off by default
int i = 0;


int main(int argc, char **argv) {

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-d") == 0 || strcmp(argv[i], "--debug") == 0) {
            debug = 1; // Turn on debug flag
            yyparse();
        } else if (strcmp(argv[i], "-s") == 0) {
            yyparse();
            print_symbol_table(); // Call the function when '-s' is passed
        } else {
            yyin = fopen(argv[i], "r");
            if (!yyin) {
                perror("Error opening file");
                return 1;
            }
        }
    }

    if (yyin) {
        fclose(yyin); // Close input file
    }
    return 0;
}