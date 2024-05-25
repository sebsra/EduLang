#include "functions.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

extern char* yytext;
extern int lineCount;

struct dataType symbol_table[40];
int count = 0;
int q;
char type[10];
void insert_type() {
    strcpy(type, yytext);
}

char* int_to_str(int num) {
    char* str = malloc(12); // Enough to hold all numbers up to 32 bits
    sprintf(str, "%d", num);
    return str;
}

char* float_to_str(float num) {
    char* str = malloc(50); // Arbitrary size
    sprintf(str, "%f", num);
    return str;
}


void add(char c, char *yytext) {
    q = search(yytext);
    if (!q) {
        if (c == 'H') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup(type);
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Header");
            count++;
        } else if (c == 'K') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup("N/A");
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Keyword");
            count++;
        } else if (c == 'V') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup(type);
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Variable");
            count++;
        } else if (c == 'C') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup("CONST");
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Constant");
            count++;
        } else if (c == 'F') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup(type);
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Function");
            count++;
        }
        } else if (c == 'A') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup(type);
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Variable");
            count++;
        }
    }


int search(char *type) {
    for (int i = count - 1; i >= 0; i--) {
        if (strcmp(symbol_table[i].id_name, type) == 0) {
            return -1;
        }
    }
    return 0;
}


void add_array_dimension(int size) {
    if(count < 40) {
        count--;
        symbol_table[count].dimension = 't';
        count++;
    } else {
        fprintf(stderr, "Symbol table is full\n");
    }
}