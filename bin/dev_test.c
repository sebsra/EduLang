#include <stdio.h>
#include <stdbool.h>

int main()
{
    
    for (int i = 0; i < 10; i++)
    {
        printf("Hello, World!\n");
    }
    int and = 1 && 0;
    float comma_number = (float) and;
    int or = 1 || 0;
    int add = 5 + 5;
    int subtract = 10 - 5;
    int divide = 10 / 2;
    int multiply = 5 * 2;

    // Array declarations
    int int_array[10][2];    // Integer array
    float float_array[5][3]; // Float array
    char char_array[20];     // Character array

    if (number > 5)
    {
        int test = 1;
    }

    if (number < 5)
    {
        printf("Number is less than 5\n");
    }
    else
    {
        printf("Number is not less than 5\n");
    }

    int lissst[3] = {1, 2, 3};

    int arr[2][3][4] = {
        {{1, 2, 3, 4},
         {5, 6, 7, 8},
         {9, 10, 11, 12}},
        {{13, 14, 15, 16},
         {17, 18, 19, 20},
         {21, 22, 23, 24}}};

    arr[1][1][1] = 25;
    int declaration;
    return 0;
}