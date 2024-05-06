#ifndef COMPILER_H
#define COMPILER_H

#include <stdio.h>

extern FILE *yyin;
extern int debug;

// Flex and Bison prototypes
extern int yylex(void);
extern int yyparse(void);

#endif // COMPILER_H
