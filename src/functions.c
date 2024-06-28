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

void attachToRightmost(struct Node* parent, struct Node* newChild) {
    struct Node* rightmost_child = parent;
    while (rightmost_child->right != NULL) {
        rightmost_child = rightmost_child->right;
    }
    rightmost_child->right = newChild;
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



void add_array_dimension(char * dimensions) {
    if (symbol_table[count - 1].is_array) { 
        symbol_table[count - 1].dimensions = strdup(dimensions);
    } else {
        fprintf(stderr, "Last symbol in the table is not marked as an array\n");
    }

}

void print_dimensions(char * dimensions) {
    printf("[");
    for (int i = 0; i < strlen(dimensions); i++) {
        if (dimensions[i] == ',') {
            printf("][");
        } else {
            printf("%c", dimensions[i]);
        }
    }
    printf("]");
}

void check_array_dimensions_for_0(char *name) {
    for (int i = 0; name[i] != '\0'; i++) {
        if (i == 0 || name[i] == ',') {
            // Find the length of the substring till the next comma or end of the string
            int start = i + (name[i] == ',' ? 1 : 0); // Skip the comma if i is not 0
            int length = 0;
            while (name[start + length] != ',' && name[start + length] != '\0') {
                length++;
            }
    
            // Allocate memory for dim_value and copy the substring
            char *dim_value = (char *)malloc(length + 1); // +1 for null terminator
            strncpy(dim_value, name + start, length);
            dim_value[length] = '\0'; // Null-terminate the string
    
            // Convert to integer and validate
            int dim_value_int = atoi(dim_value);
            if (dim_value_int <= 0) {
                // Allocate memory for the error message
                char *message = (char *)malloc(strlen("Invalid Array Dimensions: ") + length + 1); // +1 for null terminator
                sprintf(message, "Invalid Array Dimensions: %s", dim_value);
                yyerror(message);
                free(message); // Free the allocated memory for the message
            }

            // Free the allocated memory for dim_value
            free(dim_value);
    
            // Move i to the end of the current number segment to avoid re-checking
            i = start + length - 1;
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
        if (symbol_table[inp].is_array) {
            print_dimensions(symbol_table[inp].dimensions);
        } else {
            printf("-");
        }
        printf("\n");
    }
        for (inp = 0; inp < count; inp++) {
        free(symbol_table[inp].id_name); // Free memory allocated for id_name
        free(symbol_table[inp].type); // Free memory allocated for type
    }
    printf("\n\n");
}

void yyerror(const char* msg) {
    fprintf(stderr, "Error at line %d: %s\n", lineCount, msg);
    exit(1);
}