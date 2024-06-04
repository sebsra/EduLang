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



// Define the Node structure
typedef struct Node {
    struct Node *left;
    struct Node *right;
    char *token;
} Node;

// Function to create a new node
Node* create_node(char *token, Node *left, Node *right) {
    Node *node = (Node *)malloc(sizeof(Node));
    node->token = strdup(token);
    node->left = left;
    node->right = right;
    return node;
}

// Function to print the syntax tree
void print_tree(Node *root) {
    if (root == NULL) return;
    print_tree(root->left);
    printf("%s\n", root->token);
    print_tree(root->right);
}

// Function to free the syntax tree
void free_tree(Node *root) {
    if (root == NULL) return;
    free(root->token);
    free_tree(root->left);
    free_tree(root->right);
    free(root);
}
%}


%union {
    struct nd_obj {
        char name[100];
        struct Node* node;
        int dimensions[10];
    } nd_obj;

    struct nd_obj2 {
        char name[100];
        struct Node* node;
        char type[5];
    } nd_obj2;

    struct nd_obj3 {
        char name[100];
        struct Node* node;
        char if_body[5];
        char else_body[5];
    } nd_obj3;
}


%type <nd_obj> program headers main datatype body else declaration statement value list elements arithmetic_operator expression relational_operator condition init return array_dimension lists
%token <nd_obj> T_PRINTF T_SCANF T_INT T_BOOL T_FLOAT T_CHAR T_VOID T_RETURN T_FOR T_IF T_ELSE T_INCLUDE 
%token <nd_obj> T_TRUE T_FALSE T_IDENTIFIER T_FLOAT_NUMBER T_UNARY T_NUMBER 
%token <nd_obj> T_LESS_EQUAL T_GREATER_EQUAL T_EQUAL T_NOT_EQUAL T_GREATER T_LESS T_AND T_OR
%token <nd_obj> T_ADD T_SUBTRACT T_DIVIDE T_MULTIPLY T_STRING T_CHARACTER


%start program

%%

program:
    headers main '(' ')' '{' body return '}' {
        $$.node = create_node("program", $1.node, create_node("main", create_node("()", NULL, NULL), create_node("{}", $6.node, $7.node)));
    }
;

headers:
    headers headers {
        $$.node = create_node("headers", $1.node, $2.node);
    }
| T_INCLUDE {
        $$.node = create_node("include", NULL, NULL);
        add('H', $1.name);
    }

;

main:
    datatype T_IDENTIFIER {
        $$.node = create_node("main", $1.node, NULL);
        add('F', $2.name);
    }
;

datatype:
    T_INT {
        $$.node = create_node("int", NULL, NULL);
        insert_type();
    }
| T_FLOAT {
        $$.node = create_node("float", NULL, NULL);
        insert_type();
    }
| T_CHAR {
        $$.node = create_node("char", NULL, NULL);
        insert_type();
    }
| T_VOID {
        $$.node = create_node("void", NULL, NULL);
        insert_type();
    }
| T_BOOL {
        $$.node = create_node("bool", NULL, NULL);
        insert_type();
    }
;

body:
    T_FOR '(' statement ';' condition ';' statement ')' '{' body '}' {
        $$.node = create_node("for", create_node("condition", $3.node, $5.node), create_node("body", $7.node, $10.node));
        add('K', $1.name);
    }
| T_IF '(' condition ')' '{' body '}' else {
        $$.node = create_node("if", $3.node, create_node("body", $6.node, $8.node));
        add('K', $1.name);
    }
| statement ';' {
        $$ = $1;
    }
| body body {
        $$.node = create_node("body", $1.node, $2.node);
    }
| T_PRINTF '(' T_STRING ')' ';' {
        $$.node = create_node("printf", NULL, NULL);
        add('K', $1.name);
    }
| T_SCANF  '(' T_STRING ',' '&' T_IDENTIFIER ')' ';' {
        $$.node = create_node("scanf", create_node("identifier", NULL, NULL), NULL);
        add('K', $1.name);
    }
;

else:
    T_ELSE '{' body '}' {
        $$.node = create_node("else", $3.node, NULL);
        add('K', $1.name);
    }

; 

array_dimension:
    '[' T_NUMBER ']' { 
        if (array_dimension_index <= 10) {
            $$.dimensions[array_dimension_index++] = atoi($2.name);
        }
    }
| array_dimension '[' T_NUMBER ']' { 
        if (array_dimension_index <= 10) {
            $$.dimensions[array_dimension_index++] = atoi($3.name);
        }
    }
;

declaration: datatype T_IDENTIFIER {
        $$.node = create_node($2.name, NULL, NULL);
        add('V', $2.name);
    }
| datatype T_IDENTIFIER init {
        $$.node = create_node($2.name, NULL, $3.node);
        add('V', $2.name);
    }
| datatype T_IDENTIFIER array_dimension {
        $$.node = create_node($2.name, NULL, NULL);
        add('A', $2.name);
        add_array_dimension($3.dimensions);
        array_dimension_index = 0;
    }
| datatype T_IDENTIFIER array_dimension init {
         $$.node = create_node($2.name, NULL, NULL);
        add('A', $2.name);
        add_array_dimension($3.dimensions);
        array_dimension_index = 0;
    }
;

statement: declaration {
        $$ = $1;
    }
| T_IDENTIFIER array_dimension '=' value {
        $$.node = create_node("=", $1.node, $4.node);
    }
| T_IDENTIFIER init {
        $$.node = create_node("=", $1.node, $2.node);
    }
| T_IDENTIFIER relational_operator expression {
        $$.node = create_node($2.name, $1.node, $3.node);
    }
| expression
;

value: T_NUMBER {
        $$.node = create_node($1.name, NULL, NULL);
    }
| T_FLOAT_NUMBER {
        $$.node = create_node($1.name, NULL, NULL);
    }
| T_CHARACTER {
        $$.node = create_node($1.name, NULL, NULL);
    }
| T_IDENTIFIER {
        $$.node = create_node($1.name, NULL, NULL);
    }
;


list: '{' elements '}' { 
        $$.node = $2.node;
    }
| '{' lists '}'{ 
        $$.node = $2.node;
    }
;

lists: 
    list {
        $$.node = $1.node;
    }
| lists ',' list {
        struct Node* rightmost_child = $1.node;
        while (rightmost_child->right != NULL) {
            rightmost_child = rightmost_child->right;
        }
        rightmost_child->right = $3.node;
    }

elements:
    value {
    $$.node = $1.node;
    }
| elements ',' value {
        struct Node* rightmost_child = $1.node;
        while (rightmost_child->right != NULL) {
            rightmost_child = rightmost_child->right;
        }
        rightmost_child->right = $3.node;
    }
;

arithmetic_operator: T_ADD
| T_SUBTRACT
| T_MULTIPLY
| T_DIVIDE
;

expression:
    expression arithmetic_operator expression {
        $$.node = create_node($2.name, $1.node, $3.node);
    }
| value {
        $$.node = $1.node;
    }
| T_IDENTIFIER T_UNARY {
        $$.node = create_node($2.name, $1.name, NULL); // unary operator before var (var is right child!)
    }
| T_UNARY T_IDENTIFIER {
        $$.node = create_node($1.name, $2.name, NULL);  // unary operator after var (var is left child!)
    }
;

relational_operator:
T_LESS 
| T_GREATER 
| T_LESS_EQUAL 
| T_GREATER_EQUAL
| T_EQUAL 
| T_NOT_EQUAL 
| T_AND 
| T_OR 
;

condition:
    value relational_operator value {
        $$.node = create_node($2.name, $1.node, $3.node);
    }
| T_TRUE {
        $$.node = create_node($1.name, NULL, NULL);
        add('K', $1.name);
    }
| T_FALSE {
        $$.node = create_node($1.name, NULL, NULL);
        add('K', $1.name);
    }
;

init:
    '=' condition {
        $$.node = $2.node;
    }
| '=' expression {
        $$.node = $2.node;
    }
| '=' value {
        $$.node = $2.node;
    }
| '=' list {
        $$.node = $2.node;
        print_tree($2.node);
    }
;

return:
    T_RETURN value ';' {
        $$.node = create_node($1.name, NULL, $2.node);
        add('K', $1.name);
    }
|
;

%%

void yyerror(const char* msg) {
    fprintf(stderr, "Error at line %d: %s\n", lineCount, msg);
}
