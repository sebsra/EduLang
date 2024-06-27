// functions.h

#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <stdio.h>

#define MAX_DIMENSIONS 10

extern int lineCount;



struct dataType {
   char * id_name;
   char * data_type;
   int dimensions[MAX_DIMENSIONS];
   char * type;
   int line_no;
   int is_array;     
};

typedef struct Node {
    struct Node *left;
    struct Node *right;
    char *token;
} Node;

Node* create_node(char *token, Node *left, Node *right);
void attachToLeftmost(struct Node* parent, struct Node* newChild);
void attachToRightmost(struct Node* parent, struct Node* newChild);
void print_dot(Node *tree);
void print_in_order(Node *tree);
void print_tree(Node *root);
void free_tree(Node *root);
char* array_to_string(int* array, int size);

extern struct dataType symbol_table[40];
extern int count;  

char* int_to_str(int num);
char* float_to_str(float num);

void insert_type();
void add(char c, char *yytext);
int search(char *type);
void print_dimensions(int dimensions[], int size);
void print_symbol_table();
void add_array_dimension(int dimensions[], int size);
void add_array(char *name, int size);
void assign_array(char *name, int index, int value);


#endif // FUNCTIONS_H