#include <stdio.h>
#include <stdbool.h>

int main()
{
    int number = 10;
    float float_number = 10.5;
    char character = 'a';
    int unary = ++number;
    bool less_equal = 5 <= 10;
    int greater_equal = 10 >= 5;
    int equal = 10 == 10;
    int not_equal = 10 != 5;
    int greater = 10 > 5;
    int less = 5 < 10;
    int and = 1 && 0;
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
        printf("Number is greater than 5\n");
    }
    else
    {
        printf("Number is not greater than 5\n");
    }

    if (number < 5)
    {
        printf("Number is less than 5\n");
    }
    else
    {
        printf("Number is not less than 5\n");
    }

    int list[3] = {1, 2, 3};

    int arr[2][3][4] = {
        {{1, 2, 3, 4},
         {5, 6, 7, 8},
         {9, 10, 11, 12}},
        {{13, 14, 15, 16},
         {17, 18, 19, 20},
         {21, 22, 23, 24}}};

    return 0;
}