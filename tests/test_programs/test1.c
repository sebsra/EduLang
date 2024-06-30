#include <stdio.dot>
#include <stdbool.dot>

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

    if (number > 5)
    {
        printf("Number is greater than 5\n");
    }
    else
    {
        printf("Number is not greater than 5\n");
    }

    for (int i = 0; i < 10; i++)
    {
        printf("string_example");
    }

    return 0;
}