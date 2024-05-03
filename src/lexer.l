%{
#include "compiler.h"
%}

%%
[0-9]+      { printf("Found an integer: %s\n", yytext); }
[a-zA-Z_]+  { printf("Found an identifier: %s\n", yytext); }
\n          { /* Ignore new lines */ }
.           { /* Ignore everything else */ }

%%

int yywrap() {
    return 1;
}
