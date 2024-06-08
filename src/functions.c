#include "functions.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

extern char* yytext;
extern int lineCount;

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

// Function to interpret the list dimensions
int check_list_dimensions(Node* node, int expected_dim) {
    int actual_dim = 0;
    Node* current = node;
    while (current != NULL) {
        actual_dim++;
        current = current->left;
    }
    if (actual_dim != expected_dim) {
        fprintf(stderr, "Error: Expected dimension %d, received %d\n", expected_dim, actual_dim);
        return 0;
    }
    return 1;
}

// Function to interpret the list dimensions
Node* index_into_list(Node* root, int* indices, int num_indices, int current_dim) {
    if (root == NULL) {
        fprintf(stderr, "Error: Null node encountered in dimension %d\n", current_dim);
        return NULL;
    }

    if (current_dim == num_indices) {
        return root;
    }

    int index = indices[current_dim];
    Node* current = root;
    for (int i = 0; i < index; ++i) {
        if (current->right == NULL) {
            fprintf(stderr, "Error: Index %d out of bounds in dimension %d\n", index, current_dim);
            return NULL;
        }
        current = current->right;
    }

    return index_into_list(current->left, indices, num_indices, current_dim + 1);
}

// Function to print indices
void print_indices(int* indices, int num_indices) {
    printf("Element at indices [");
    for (int i = 0; i < num_indices; ++i) {
        printf("%d", indices[i]);
        if (i < num_indices - 1) {
            printf(", ");
        }
    }
    printf("]");
}

// Main interpreter function
void interpret_tree(Node* root, int* indices, int num_indices) {
    if (strcmp(root->token, "list") == 0) {
        if (!check_list_dimensions(root, num_indices)) {
            return;
        }
        Node* element = index_into_list(root, indices, num_indices, 0);
        if (element) {
            print_indices(indices, num_indices);
            printf(": %s\n", element->token);
        } else {
            printf("Element not found.\n");
        }
    } else {
        fprintf(stderr, "Error: Unsupported node type: %s\n", root->token);
    }
}