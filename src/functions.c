#include "functions.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

extern char* yytext;
extern int lineCount;



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

FILE *fp;
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

struct dataType symbol_table[40];
int count = 0;
int q;
char type[10];
void insert_type() {
    strcpy(type, yytext);
}


char* int_to_str(int num) {
    char* str = malloc(12); // Enough to hold all numbers up to 32 bits
    sprintf(str, "%d", num);
    return str;
}

char* float_to_str(float num) {
    char* str = malloc(50); // Arbitrary size
    sprintf(str, "%f", num);
    return str;
}


void add(char c, char *yytext) {
    q = search(yytext);
    if (!q) {
        if (c == 'H') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup(type);
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Header");
            count++;
        } else if (c == 'K') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup("N/A");
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Keyword");
            count++;
        } else if (c == 'V') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup(type);
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Variable");
            count++;
        } else if (c == 'C') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup("CONST");
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Constant");
            count++;
        } else if (c == 'F') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup(type);
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Function");
            count++;
        } else if (c == 'A') {
            symbol_table[count].id_name = strdup(yytext);
            symbol_table[count].data_type = strdup(type);
            symbol_table[count].line_no = lineCount;
            symbol_table[count].type = strdup("Variable");
            symbol_table[count].is_array = 1;
            count++;
        }
    }
}

int search(char *type) {
    for (int i = count - 1; i >= 0; i--) {
        if (strcmp(symbol_table[i].id_name, type) == 0) {
            return -1;
        }
    }
    return 0;
}



void add_array_dimension(int dimensions[], int size) {
    if (symbol_table[count - 1].is_array) { 
        // Assuming dimensions is an array of the same size as size
        memcpy(symbol_table[count - 1].dimensions, dimensions, size * sizeof(int));
    } else {
        fprintf(stderr, "Last symbol in the table is not marked as an array\n");
    }
}

void print_dimensions(int dimensions[], int size) {
    for (int i = 0; i < size; i++) {
        if (dimensions[i] == 0) {
            break;
        }
        else if (i != 0) {
            printf("x");
        }
        printf("%d", dimensions[i]);
        if (i < size - 1) {
            
        }
    }
}

    
void print_symbol_table() {
    printf("\n\n");
    printf("PHASE 1: LEXICAL ANALYSIS \n\n");
    printf("%-20s %-20s %-20s %-10s %-10s\n", 
        "SYMBOL", 
        "DATATYPE", 
        "TYPE", 
        "LINE NUMBER", 
        "DIMENSION");

    int inp;
    for (inp = 0; inp < count; inp++) {
        printf("%-20s %-20s %-20s %-10d ", 
            symbol_table[inp].id_name, 
            symbol_table[inp].data_type, 
            symbol_table[inp].type, 
            symbol_table[inp].line_no);
        print_dimensions(symbol_table[inp].dimensions, sizeof(symbol_table[inp].dimensions)/sizeof(symbol_table[inp].dimensions[0]));
        printf("\n");
    }
        for (inp = 0; inp < count; inp++) {
        free(symbol_table[inp].id_name); // Free memory allocated for id_name
        free(symbol_table[inp].type); // Free memory allocated for type
    }
    printf("\n\n");
}