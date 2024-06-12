#include <stdio.h>
#include <stdbool.h>

int main()
{
    int test_10 =0;
    for (int i = 0; i < 10; i++)
    {
        test_10++;
    };
    int test_20 = 0;
    if (true) {
        test_20 = 20;
    };
    int and_0 = 1 && 0; 
    bool and_wahr = true && true;
    float comma_number = 5.5;
    int number_5 = (int) comma_number;
    int or_0 = 0 || 0;  
    bool or_wahr = true || false;
    int add_12 = 5 + 7;
    int subtract_3 = 10 - 7;
    int divide_5 = 10 / 2;
    int multiply_10 = 5 * 2;

    // Array declarations
    int int_array[10][2];    // Integer array
    float float_array[5][3]; // Float array
    char char_array[20];     // Character array

    printf("Hello World\n");

    int scan;
    scanf("%d", &scan);

    int arr[2][3][4] = {
        {{1, 2, 3, 4},
         {5, 6, 7, 8},
         {9, 10, 11, 12}},
        {{13, 14, 15, 16},
         {17, 18, 19, 20},
         {21, 22, 23, 24}}};

    arr[0][0][0] = 0;
    int int_24 = arr[1][2][3];

    return 0;
}