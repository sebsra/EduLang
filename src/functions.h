// functions.h

#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <stdio.h>

struct dataType {
   char * id_name;
   char * data_type;
   char *  dimension;
   char * type;
   int line_no;
   int is_array;     
};
extern struct dataType symbol_table[40];
extern int count;  

char* int_to_str(int num);
char* float_to_str(float num);

void insert_type();
void add(char c, char *yytext);
int search(char *type);
void add_array(char *name, int size);
void assign_array(char *name, int index, int value);

#endif // FUNCTIONS_H