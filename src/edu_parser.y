%{
#include "edu_parser.h"
#include "edulang.h"
#include "functions.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>


FILE *fp;
extern char* yytext;
extern int lineCount;

int array_dimension_index = 0;
int list_diemnsion_index = 0;
Node* last_list_node_in_dimension[10];

// Function to create a new node
Node* create_node(char *token, Node *left, Node *right) {
    Node *node = (Node *)malloc(sizeof(Node));
    node->token = strdup(token);
    node->left = left;
    node->right = right;
    return node;
}

void attachToLeftmost(struct Node* parent, struct Node* newChild) {
    struct Node* leftmost_child = parent;
    while (leftmost_child->left != NULL) {
        leftmost_child = leftmost_child->left;
    }
    leftmost_child->left = newChild;
}

void print_dot(Node *tree) {
    if (tree == NULL) {
        printf("Tree is NULL, returning from print_dot function\n");
        return;
    }
    char *start, *end;
    start = strchr(tree->token, '\"');
    end = strrchr(tree->token, '\"');
    
    if (start) *start = '\'';
    if (end) *end = '\'';
    
    fprintf(fp, "\"%p\" [label=\"%s\"];\n", (void *)tree, tree->token);
    fprintf(fp, "\"%p\" [label=\"%s\"];\n", (void *)tree, tree->token);

    if (tree->left) {
        fprintf(fp, "\"%p\" -> \"%p\" [label=\"left\"];\n", (void *)tree, (void *)tree->left);
        print_dot(tree->left);
    }

    if (tree->right) {
        fprintf(fp, "\"%p\" -> \"%p\" [label=\"right\"];\n", (void *)tree, (void *)tree->right);
        print_dot(tree->right);
    }
}
void print_in_order(Node *tree) {
    if (tree == NULL) {
        printf("NULL, ");
        return;
    }
    print_in_order(tree->left);
    printf("%s, ", tree->token);
    print_in_order(tree->right);
}

void print_tree(Node *root) {
    fp = fopen("tree.dot", "w");
    fprintf(fp, "digraph G {\n");
    print_dot(root);
    fprintf(fp, "}\n");
    fclose(fp);
    //printf("in-order array: ");
    //print_in_order(root);
}

// Function to free the syntax tree
void free_tree(Node *root) {
    if (root == NULL) return;
    free(root->token);
    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

char* array_to_string(int* array, int size) {
    char* result = malloc(size * 4 * sizeof(char)); // Allocate enough memory
    result[0] = '\0'; // Start with an empty string
    
    for (int i = 0; i < size; i++) {
        if (array[i] != 0) {
            char buffer[12]; // Buffer to hold string representation of integer
            sprintf(buffer, "%d", array[i]); // Convert integer to string
            strcat(result, buffer); // Append to result string
            if (array[i+1] != 0) {
            strcat(result, ", "); 
            }
        }
    }

    return result;
}
%}


%union {
    struct nd_obj {
        char name[100];
        struct Node* node;
    } nd_obj;

    struct array_obj {
        char name[100];
        struct Node* node;
        int dimensions[10];
    } array_obj;

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


%type <nd_obj> program headers main datatype body if else declaration statement value arithmetic_operator expression relational_operator condition init return  
%type <array_obj> list values list_1  list_1_s  list_2  list_2_s  list_3  list_3_s  list_4  list_4_s  list_5  list_5_s  list_6  list_6_s  list_7  list_7_s  list_8  list_8_s  list_9  list_9_s  list_10
%type <array_obj> array_dimension
%token <nd_obj> T_PRINTF T_SCANF T_INT T_BOOL T_FLOAT T_CHAR T_VOID T_RETURN T_FOR T_IF T_ELSE T_INCLUDE 
%token <nd_obj> T_TRUE T_FALSE T_IDENTIFIER T_FLOAT_NUMBER T_UNARY T_NUMBER 
%token <nd_obj> T_LESS_EQUAL T_GREATER_EQUAL T_EQUAL T_NOT_EQUAL T_GREATER T_LESS T_AND T_OR
%token <nd_obj> T_ADD T_SUBTRACT T_DIVIDE T_MULTIPLY T_STRING T_CHARACTER


%start program

%%

program:
    headers main '(' ')' '{' body return '}' {
        $2.node->left = $6.node; 
        $2.node->right = $7.node; 
        $$.node = create_node("program", $1.node, $2.node);
        print_tree($$.node);
    }
    | main '(' ')' '{' body return '}' {
        $1.node->left = $5.node; 
        $1.node->right = $6.node; 
        $$.node = create_node("program", NULL, $1.node);
        print_tree($$.node);
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
        $$.node = create_node("main", NULL, NULL);
        add('F', $2.name);
    }
;

datatype:
    T_INT {
        struct Node *temp = create_node("int", NULL, NULL);	
        $$.node = create_node("type", temp, NULL);
        insert_type();
    }
| T_FLOAT {
        struct Node *temp = create_node("float", NULL, NULL);
        $$.node = create_node("type", temp, NULL);
        insert_type();
    }
| T_CHAR {
        struct Node *temp = create_node("char", NULL, NULL);
        $$.node = create_node("type", temp, NULL);
        insert_type();
    }
| T_VOID {
        struct Node *temp = create_node("void", NULL, NULL);
        $$.node = create_node("type", temp, NULL);
        insert_type();
    }
| T_BOOL {
        struct Node *temp = create_node("bool", NULL, NULL);
        $$.node = create_node("type", temp, NULL);
        insert_type();
    }
;

body:
    T_FOR '(' statement ';' condition ';' statement ')' '{' body '}' {
        struct Node *temp = create_node("Condition", $5.node, $7.node); 
        struct Node *temp2 = create_node("Condition", $3.node, temp);
        $$.node = create_node("for", temp2, $10.node);
        add('K', $1.name);
    }
| if {
        $$.node = $1.node;
}
| if else {
        $$.node = create_node("if_else", $1.node, $2.node);
}
| statement ';' {
        $$ = $1;
    }
| body body {
        $$.node = create_node("body", $1.node, $2.node);
    }
| T_PRINTF '(' T_STRING ')' ';' {
        struct Node *temp = create_node($3.name, NULL, NULL); 
        $$.node = create_node("printf", NULL, temp);
        add('K', $1.name);
    }
| T_SCANF  '(' T_STRING ',' '&' T_IDENTIFIER ')' ';' {
        $$.node = create_node("scanf", NULL, NULL);
        add('K', $1.name);
    }
;

else: T_ELSE '{' body '}' {
        $$.node = create_node("else", NULL, $3.node);
        add('K', $1.name);
    }
; 

if: T_IF '(' condition ')' '{' body '}' {
        $$.node = create_node("if", $3.node, $6.node);
        add('K', $1.name);
    }


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
        $2.node = create_node($2.name, $1.node, NULL);
        $$.node = create_node("declaration", $2.node, NULL);
        add('V', $2.name);
    }
| datatype T_IDENTIFIER init {
        $2.node = create_node($2.name, $1.node, NULL);
        $$.node = create_node("declaration_init", $2.node, $3.node);
        add('V', $2.name);
    }
| datatype T_IDENTIFIER array_dimension {
        struct Node *dimension = create_node(array_to_string($3.dimensions, 10), NULL, NULL);
        $3.node = create_node("array_dim", dimension, NULL);
        $2.node = create_node($2.name, $1.node, $3.node);
        $$.node = create_node("declaraion", $2.node, NULL);
        add('A', $2.name);
        add_array_dimension($3.dimensions, sizeof($3.dimensions)/sizeof($3.dimensions[0]));
        array_dimension_index = 0;
    }
| datatype T_IDENTIFIER array_dimension init {
        struct Node *dimension = create_node(array_to_string($3.dimensions, 10), NULL, NULL);
        $3.node = create_node("array_dim", dimension, NULL);
        $2.node = create_node($2.name, $1.node, $3.node);
        $$.node = create_node("array_declaration_init", $2.node, $4.node);

        add('A', $2.name);
        add_array_dimension($3.dimensions, sizeof($3.dimensions)/sizeof($3.dimensions[0]));
        array_dimension_index = 0;
    }
;

statement: declaration {
        $$ = $1;
    }
| T_IDENTIFIER array_dimension init {
        struct Node *dimension = create_node(array_to_string($2.dimensions, 10), NULL, NULL);
        $3.node = create_node("array_index", dimension, $3.node);
        $1.node = create_node($1.name, NULL, NULL);
        $$.node = create_node("array_assignment", $1.node, $3.node);
    }
| T_IDENTIFIER init {
        $$.node = create_node("assignment", $1.node, $2.node);
    }
| expression {
        $$.node = $1.node;
    }
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
list: list_1 { $$.node = $1.node;}
| list_2 { $$.node = $1.node;}
| list_3 { $$.node = $1.node;}
| list_4 { $$.node = $1.node;}
| list_5 { $$.node = $1.node;}
| list_6 { $$.node = $1.node;}
| list_7 { $$.node = $1.node;}
| list_8 { $$.node = $1.node;}
| list_9 { $$.node = $1.node;}
| list_10 { $$.node = $1.node;}
;

values: value {
    $$.node = $1.node;
    }
| values ',' value 
{
    attachToLeftmost($1.node, $3.node);
}
;

list_1: '{' values '}' {
    $$.node = create_node("list" , NULL, $2.node);
    }
;

list_1_s : list_1 {
    $$.node = $1.node;
    }
|  list_1_s ',' list_1 {
    attachToLeftmost($1.node, $3.node);
}
;

list_2: '{' list_1_s '}' {
    $$.node = create_node("list" , NULL, $2.node);
    }
;

list_2_s : list_2 {
    $$.node = $1.node;
    }
|  list_2_s ',' list_2{
    attachToLeftmost($1.node, $3.node);
}
;

list_3: '{' list_2_s '}' {
    $$.node = create_node("list" , NULL, $2.node);
}
;

list_3_s : list_3 {
    $$.node = $1.node;
    }
|  list_3_s ',' list_3 {
    attachToLeftmost($1.node, $3.node);
}
;

list_4: '{' list_3_s '}' {
    $$.node = create_node("list" , NULL, $2.node);
}
;

list_4_s : list_4 {
    $$.node = $1.node;
    }
|  list_4_s ',' list_4 {
    attachToLeftmost($1.node, $3.node);
}
;

list_5: '{' list_4_s '}' {
    $$.node = create_node("list" , NULL, $2.node);
}
;

list_5_s : list_5 {
    $$.node = $1.node;
    }
|  list_5_s ',' list_5 {
    attachToLeftmost($1.node, $3.node);
}
;

list_6: '{' list_5_s '}' {
    $$.node = create_node("list" , NULL, $2.node);
}
;

list_6_s : list_6 {
    $$.node = $1.node;
    }
|  list_6_s ',' list_6 {
    attachToLeftmost($1.node, $3.node);
}
;

list_7: '{' list_6_s '}' {
    $$.node = create_node("list" , NULL, $2.node);
}
;

list_7_s : list_7 {
    $$.node = $1.node;
    }
|  list_7_s ',' list_7 {
    attachToLeftmost($1.node, $3.node);
}
;

list_8: '{' list_7_s '}' {
    $$.node = create_node("list" , NULL, $2.node);
}
;

list_8_s : list_8 {
    $$.node = $1.node;
    }
|  list_8_s ',' list_8 {
    attachToLeftmost($1.node, $3.node);
}
;

list_9: '{' list_8_s '}' {
    $$.node = create_node("list" , NULL, $2.node);
}
;

list_9_s : list_9 
|  list_9_s ',' list_9 {
    attachToLeftmost($1.node, $3.node);
}
;

list_10: '{' list_9_s '}' {
    $$.node = create_node("list" , NULL, $2.node);
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
        struct Node *var = create_node($1.name, NULL, NULL);
        struct Node *unary = create_node($2.name, NULL, NULL);
        $$.node = create_node("unary", var, unary); 
    }
| T_UNARY T_IDENTIFIER {
        struct Node *var = create_node($2.name, NULL, NULL);
        struct Node *unary = create_node($1.name, NULL, NULL);
        $$.node = create_node("unary", unary, var); 
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
    expression relational_operator expression {
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
    }
;

return:
    T_RETURN value ';' {
        $$.node = create_node("return", NULL, $2.node);
        add('K', $1.name);
    }
;

%%

void yyerror(const char* msg) {
    fprintf(stderr, "Error at line %d: %s\n", lineCount, msg);
}
