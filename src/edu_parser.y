%{
#include "edu_parser.h"
#include "edulang.h"
#include "functions.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

// Define the Node structure
typedef struct Node {
    struct Node *left;
    struct Node *right;
    char *token;
} Node;


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

#include <stdio.h>

void attachToLeftmost(struct Node* parent, struct Node* newChild) {
    struct Node* leftmost_child = parent;
    while (leftmost_child->left != NULL) {
        leftmost_child = leftmost_child->left;
    }
    leftmost_child->left = newChild;
}

FILE *fp;

void print_dot(Node *tree) {
    if (tree == NULL) {
        return;
    }

    // Print the node with its memory address as the identifier and its token as the label
    fprintf(fp, "\"%p\" [label=\"%s\"];\n", (void *)tree, tree->token);

    if (tree->left) {
        // Print the edge with label
        fprintf(fp, "\"%p\" -> \"%p\" [label=\"left\"];\n", (void *)tree, (void *)tree->left);
        print_dot(tree->left);
    }

    if (tree->right) {
        // Print the edge with label
        fprintf(fp, "\"%p\" -> \"%p\" [label=\"right\"];\n", (void *)tree, (void *)tree->right);
        print_dot(tree->right);
    }
}
void print_pre_order(Node *tree) {
    if (tree == NULL) {
        printf("NULL, ");
        return;
    }

    printf("%s, ", tree->token);

    print_pre_order(tree->left);

    print_pre_order(tree->right);
}

void print_tree(Node *root) {
    fp = fopen("tree.dot", "w");
    fprintf(fp, "digraph G {\n");
    print_dot(root);
    fprintf(fp, "}\n");
    fclose(fp);

    printf("pre-order array: ");
    print_pre_order(root);
    printf("\n");
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


%type <nd_obj> program headers main datatype body else declaration statement value arithmetic_operator expression relational_operator condition init return  
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
        array_dimension_index = 0;
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
