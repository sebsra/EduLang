#include <missing_dummy.h>

int main()
{
        int test_10 = 0;
        for (int i = 0; i < 10; i++)
        {
            test_10++;
        }
        printf("test_10: %d\n", test_10);

        int test_10_klon = test_10;
        printf("test_10_klon: %d\n", test_10_klon);


        int test_5 = 5 + 5 * 2 - ((2+3)*10) / 5 - (5* 0);

        printf("test_5: %d\n", test_5);

        int test_20 = 0;
        if (true) {
            test_20 = 5;
            test_20 = 10;
            test_20 = 20;
        }
        printf("test_20: %d\n", test_20);

        if((test_5 > test_20) || (test_5 > test_10 )) {
            test_5 = 200;
        }else if(test_5 == test_20) { 
            test_5 = 100;
        }else if(test_10 == test_20) { 
            test_10 = 1000;
        }else {
            test_5 = 0;
        }

        int and_0 = 1 && 0; 
        printf("and_0: %d\n", and_0);

        bool and_wahr = true && true;
        printf("and_wahr: %d\n", and_wahr);

        float comma_number = 5.5;
        printf("comma_number: %f\n", comma_number);

        int number_5 = (int) comma_number;
        printf("number_5: %d\n", number_5);

        int or_0 = 0 || 0;  
        printf("or_0: %d\n", or_0);

        bool or_wahr = true || false;
        printf("or_wahr: %d\n", or_wahr);

        int add_12 = 5 + 7;
        printf("add_12: %d\n", add_12);

        int subtract_3 = 10 - 7;
        printf("subtract_3: %d\n", subtract_3);

        int divide_5 = 10 / 2;
        printf("divide_5: %d\n", divide_5);

        int multiply_10 = 5 * 2;
        printf("multiply_10: %d\n", multiply_10);

        // Array declarations
        int int_array[10][2];    // Integer array
        float float_array[5][3]; // Float array
        char char_array[20];     // Character array

        printf("Hello World\n");

        printf("enter a number:");
        int scan;
        scanf("%d", &scan);
        printf("scan: %d\n", scan);

        int arr[2][3][4] = {
            {{1, 2, 3, 4},
            {5, 6, 7, 8},
            {9, 10, 11, 12}},
            {{13, 14, 15, 16},
            {17, 18, 19, 20},
            {21, 22, 23, 24}}};

        arr[1][2][3] = 0;
        int int_24 = arr[1][2][3];
        printf("int_24: %d\n", int_24);

        // Note: This while loop will cause an infinite loop, so it's commented out.
        // while(true) {
        //     int while_var = 0;
        // }

        return 0;
}