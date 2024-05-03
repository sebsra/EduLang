%{
#include "compiler.h"
void yyerror(char *s) {
    fprintf(stderr, "Error: %s\n", s);
}
%}



%token INTEGER IDENTIFIER

%%

program:
    /* empty */
    | program line
    ;

line:
    INTEGER
    | IDENTIFIER
    ;

%%
