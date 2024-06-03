%{
#include "edu_parser.h"
#include "edulang.h"
#include "functions.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
extern char* yytext;
extern int lineCount;
int array_dimension_index = 0;
%}

%union {
    char* str;
    struct {
        char name[50];
        int dimensions[10];
    } node;
    char char_val;
    float float_num;
    int token; // Add this line
}



%type <node> datatype value list expression array_dimension 
%token <node> T_PRINTF T_SCANF T_INT T_BOOL T_FLOAT T_CHAR T_VOID T_RETURN T_FOR T_IF T_ELSE T_INCLUDE 
%token <node> T_TRUE T_FALSE T_IDENTIFIER T_FLOAT_NUMBER T_UNARY T_NUMBER 
%token <node> T_LESS_EQUAL T_GREATER_EQUAL T_EQUAL T_NOT_EQUAL T_GREATER T_LESS T_AND T_OR
%token <node> T_ADD T_SUBTRACT T_DIVIDE T_MULTIPLY T_STRING T_CHARACTER

%start program

%%

program: headers main '(' ')' '{' body return '}'
;

headers: headers headers
| T_INCLUDE { add('H', $1.name); }
|
;

main: datatype T_IDENTIFIER { add('F', $1.name); }
;

datatype: T_INT { insert_type(); }
| T_FLOAT       { insert_type(); }
| T_CHAR        { insert_type(); }
| T_VOID        { insert_type(); }
| T_BOOL        { insert_type(); }    
;

body: T_FOR { add('K', $1.name); } '(' statement ';' condition ';' statement ')' '{' body '}'
| T_IF { add('K', $1.name); } '(' condition ')' '{' body '}' else
| statement ';' 
| body body
| T_PRINTF { add('K', $1.name); } '(' T_STRING ')' ';'
| T_SCANF  { add('K', $1.name); } '(' T_STRING ',' '&' T_IDENTIFIER ')' ';'
;

else: T_ELSE '{' body '}' { add('K', $1.name); }
|
; 

array_dimension: '[' T_NUMBER ']' { 
    if (array_dimension_index <= 10) {
    $$.dimensions[array_dimension_index++] = atoi($2.name);
     }
    }
| array_dimension '[' T_NUMBER ']' { 
    if (array_dimension_index <= 10) {
    $$.dimensions[array_dimension_index++] = atoi($3.name); }
    }
;


declaration: datatype T_IDENTIFIER { add('V', $2.name); }
| datatype T_IDENTIFIER init { add('V', $2.name); }
| datatype T_IDENTIFIER array_dimension { add('A', $2.name); add_array_dimension($3.dimensions); array_dimension_index = 0;}
| datatype T_IDENTIFIER array_dimension init { add('A', $2.name); add_array_dimension($3.dimensions);  array_dimension_index = 0;}
;



statement: declaration
| T_IDENTIFIER array_dimension '=' value { /* Handle array indexing */ }
| T_IDENTIFIER init 
| T_IDENTIFIER relational_operator expression
| T_IDENTIFIER T_UNARY 
| T_UNARY T_IDENTIFIER
;



value: T_NUMBER 
| T_FLOAT_NUMBER 
| T_CHARACTER
| T_IDENTIFIER 
| list
;

list: '{' elements '}' 
;

elements: value
| elements ',' value
;

arithmetic_operator: T_ADD 
| T_SUBTRACT 
| T_MULTIPLY
| T_DIVIDE
;

expression: expression arithmetic_operator expression {} // Simplified for illustration
| value {}
| T_UNARY value {} // Handle unary operators correctly
| value T_UNARY {}
;

relational_operator : T_LESS
| T_GREATER
| T_LESS_EQUAL
| T_GREATER_EQUAL
| T_EQUAL
| T_NOT_EQUAL
| T_AND
| T_OR
;

condition: value relational_operator value 
| T_TRUE  { add('K', $1.name); }
| T_FALSE { add('K', $1.name); }
;

init: '=' condition
| '=' expression
| '=' value 
| '=' list
;

return: T_RETURN { add('K', $1.name); } value ';' 
|
;

%%

void yyerror(const char* msg) {
    fprintf(stderr, "%s\n", msg);
}
