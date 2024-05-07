%{
#include "edu_parser.h"
#include "edulang.h"

extern int yylex();
void yyerror(const char *s);
%}

%union {
    struct {
        char name[50];
        // other members...
    } node;
    // other members...
}

%token T_PRINTF T_SCANF T_INT T_FLOAT T_CHAR T_VOID T_RETURN T_FOR T_IF T_ELSE T_INCLUDE
%token T_TRUE T_FALSE T_NUMBER T_FLOAT_NUMBER T_IDENTIFIER T_UNARY
%token T_LESS_EQUAL T_GREATER_EQUAL T_EQUAL T_NOT_EQUAL T_GREATER T_LESS T_AND T_OR
%token T_ADD T_SUBTRACT T_DIVIDE T_MULTIPLY T_STRING T_CHARACTER 

%start program

%%
datatype: T_INT 
| T_FLOAT 
| T_CHAR
| T_VOID
;

value: T_NUMBER
| T_FLOAT_NUMBER
| T_CHARACTER
| T_IDENTIFIER
;

arithmetic_operator: T_ADD 
| T_SUBTRACT 
| T_MULTIPLY
| T_DIVIDE
;

expression: expression arithmetic_operator expression
| value
;

relational_operator : T_LESS
| T_GREATER
| T_LESS_EQUAL
| T_GREATER_EQUAL
| T_EQUAL
| T_NOT_EQUAL
;

condition: value relational_operator value 
| T_TRUE 
| T_FALSE
;

init: '=' value 
|
;

statement: datatype T_IDENTIFIER init 
| T_IDENTIFIER '=' expression 
| T_IDENTIFIER relational_operator expression
| T_IDENTIFIER T_UNARY 
| T_UNARY T_IDENTIFIER
;


body: T_FOR '(' statement ';' condition ';' statement ')' '{' body '}'
| T_IF '(' condition ')' '{' body '}' else
| statement ';' 
| body body
| T_PRINTF '(' T_STRING ')' ';'
| T_SCANF '(' T_STRING ',' '&' T_IDENTIFIER ')' ';'
;

else: T_ELSE '{' body '}'
|
;

headers: headers headers
| T_INCLUDE
;

main: datatype T_IDENTIFIER
;

return: T_RETURN value ';' 
|
;

program: headers main '(' ')' '{' body return '}'
;

%%

void yyerror(const char* msg) {
    fprintf(stderr, "%s\n", msg);
}