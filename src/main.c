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
        } else {
            yyin = fopen(argv[i], "r");
            if (!yyin) {
                perror("Error opening file");
                return 1;
            }
        }
    }

    yyparse();

    

    printf("\n\n");
    printf("\t\t\t\t\t\t\t\t PHASE 1: LEXICAL ANALYSIS \n\n");
    printf("\nSYMBOL   DATATYPE   TYPE   LINE NUMBER   DIMENSION\n");
    printf("____________________________________________________\n\n");
    int inp = 0;
    for (inp = 0; inp < count; inp++) {
        if (symbol_table[inp].is_array) { // Check if the symbol is an array
            printf("%s\t%s\t%s\t%d\t%d\n", symbol_table[inp].id_name, symbol_table[inp].data_type, symbol_table[inp].type, symbol_table[inp].line_no, symbol_table[inp].dimension); // Print symbol information with array size
        } else {
            printf("%s\t%s\t%s\t%d\t-\n", symbol_table[inp].id_name, symbol_table[inp].data_type, symbol_table[inp].type, symbol_table[inp].line_no); // Print symbol information with dash for non-array symbols
        }
    }
    for (inp = 0; inp < count; inp++) {
        free(symbol_table[inp].id_name); // Free memory allocated for id_name
        free(symbol_table[inp].type); // Free memory allocated for type
    }
    printf("\n\n");

    if (yyin) {
        fclose(yyin); // Close input file
    }

    return 0;
}