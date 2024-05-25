%{
#include "edu_parser.h"
#include "edulang.h"
#include "functions.h"
#include <string.h>
%}

%union {
    char* str;
    struct {
        char name[50];
    } node;
    int num;
    char char_val;
    float float_num;
    int token; // Add this line
}

%type <node> datatype value list expression
%token <node> T_PRINTF T_SCANF T_INT T_BOOL T_FLOAT T_CHAR T_VOID T_RETURN T_FOR T_IF T_ELSE T_INCLUDE
%token <node> T_TRUE T_FALSE T_NUMBER T_FLOAT_NUMBER T_IDENTIFIER T_UNARY
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

array_dimension: '[' T_NUMBER ']' {add_array_dimension($2.name);} 
| array_dimension '[' T_NUMBER ']' { } 
;

declaration: datatype T_IDENTIFIER  {add('V', $2.name);}
| datatype T_IDENTIFIER init  {add('V', $2.name);}
| datatype T_IDENTIFIER array_dimension {add('V', $2.name);}
| datatype T_IDENTIFIER array_dimension init  {add('V', $2.name);}


statement: declaration
| T_IDENTIFIER array_dimension '=' value {/* Array Indexing */} 
| T_IDENTIFIER init 
| T_IDENTIFIER relational_operator expression
| T_IDENTIFIER T_UNARY 
| T_UNARY T_IDENTIFIER
;

value: T_NUMBER  { add('C', $1.name); }
| T_FLOAT_NUMBER { add('C', $1.name); }
| T_CHARACTER    { add('C', $1.name); }
| T_IDENTIFIER
| list           { add('L', $1.name); }
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
