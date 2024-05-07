%{
#include "edu_parser.h"
#include "edulang.h"

extern int yylex();
void yyerror(char *s);
%}

%union {
    struct {
        char name[50];
        // other members...
    } node;
    // other members...
}

%token T_PRINTF T_SCANF T_INT T_FLOAT T_CHAR T_VOID T_RETURN T_FOR T_IF T_ELSE T_INCLUDE
%token T_TRUE T_FALSE T_NUMBER T_FLOAT_NUMBER T_IDENTIFIER T_INCREMENT
%token T_LESS_EQUAL T_GREATER_EQUAL T_EQUAL T_NOT_EQUAL T_GREATER T_LESS T_AND T_OR
%token T_ADD T_SUBTRACT T_DIVIDE T_MULTIPLY T_STRING T_CHARACTER

%start program

%%
program:
    program statement
    | /* empty */
    ;

statement:
    type_declaration statement
    | assignment_statement
    | initialization_statement
    | function_declaration
    | control_structure
    | io_statement
    | expression_statement
    ;

type_declaration:
    T_INT T_IDENTIFIER
    | T_FLOAT T_IDENTIFIER
    | T_CHAR T_IDENTIFIER
    | T_VOID T_IDENTIFIER
    ;

initialization_statement:
    type_declaration '=' expression ';'
    ;

assignment_statement:
    T_IDENTIFIER '=' expression ';'
    ;

function_declaration:
    T_VOID T_IDENTIFIER '(' ')' compound_statement
    ;

control_structure:
    T_IF '(' expression ')' compound_statement
    | T_IF '(' expression ')' compound_statement T_ELSE compound_statement
    | T_FOR '(' assignment_statement expression ';' expression ')' compound_statement
    ;

io_statement:
    T_PRINTF '(' T_STRING ')' ';'
    | T_SCANF '(' T_STRING ',' '&' T_IDENTIFIER ')' ';'
    ;

expression_statement:
    expression ';'
    ;

expression:
    T_IDENTIFIER
    | T_NUMBER
    | T_FLOAT_NUMBER
    | unary_expression
    | expression T_ADD expression
    | expression T_SUBTRACT expression
    | expression T_MULTIPLY expression
    | expression T_DIVIDE expression
    | expression T_LESS expression
    | expression T_GREATER expression
    | expression T_LESS_EQUAL expression
    | expression T_GREATER_EQUAL expression
    | expression T_EQUAL expression
    | expression T_NOT_EQUAL expression
    | expression T_AND expression
    | expression T_OR expression

    ;

unary_expression:
    T_INCREMENT T_IDENTIFIER
    ;

compound_statement:
    '{' statement '}'
    ;

%%

void yyerror(char *s) {
    fprintf(stderr, "%s\n", s);
}

