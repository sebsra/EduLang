#ifndef COMPILER_H
#define COMPILER_H

#include <stdio.h>

extern FILE *yyin;
extern int yylex(void);
extern int yyparse(void);

#endif // COMPILER_H
