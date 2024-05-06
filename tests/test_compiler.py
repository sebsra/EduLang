import subprocess
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from build_compiler import build


def run_compiler_test(test_input, debug=False):
    try:
        with open('temp_test_input.txt', 'w') as f:
            f.write(test_input)
        
        # Get the absolute path to the 'compiler' executable
        compiler_path = os.path.join(os.getcwd(), 'bin', 'edulang')
        
        # Add debug flag if debug is True
        command = [compiler_path, 'temp_test_input.txt']
        if debug:
            command.append('-d')

        result = subprocess.run(command, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.output
    

def main():
    test_cases = [
    {'input': 'printf("Hello, world!");', 'expected_output': 'FOUND : T_PRINTF (printf)\nFOUND T_STRING: "Hello, world!"'},
    {'input': 'scanf("%d", &num);', 'expected_output': 'FOUND : T_SCANF (scanf)\nFOUND T_STRING: "%d"\nFOUND : T_IDENTIFIER (num)'},
    {'input': 'int num;', 'expected_output': 'FOUND : T_INT (int)\nFOUND : T_IDENTIFIER (num)'},
    {'input': 'float num;', 'expected_output': 'FOUND : T_FLOAT (float)\nFOUND : T_IDENTIFIER (num)'},
    {'input': 'char c;', 'expected_output': 'FOUND : T_CHAR (char)\nFOUND : T_IDENTIFIER (c)'},
    {'input': 'void func();', 'expected_output': 'FOUND : T_VOID (void)\nFOUND : T_IDENTIFIER (func)'},
    #{'input': 'return 0;', 'expected_output': 'FOUND : T_RETURN (return)\nFOUND : T_NUMBER (0)'},
    #{'input': 'for (int i = 0; i < 10; i++) {}', 'expected_output': 'FOUND : T_FOR (for)\nFOUND : T_INT (int)\nFOUND : T_IDENTIFIER (i)\nFOUND : T_NUMBER (0)\nFOUND : T_LESS (<)\nFOUND : T_NUMBER (10)\nFOUND : T_INCREMENT (++)'},
    {'input': 'if (num > 0) {}', 'expected_output': 'FOUND : T_IF (if)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_GREATER (>)\nFOUND : T_NUMBER (0)'},
    #{'input': 'if (num > 0) {} else {}', 'expected_output': 'FOUND : T_IF (if)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_GREATER (>)\nFOUND : T_NUMBER (0)\nFOUND : T_ELSE (else)'},
    {'input': '#include <stdio.h>', 'expected_output': 'FOUND : T_INCLUDE (#include <stdio.h>)'},
    #{'input': 'bool flag = true;', 'expected_output': 'FOUND : T_BOOL (bool)\nFOUND : T_IDENTIFIER (flag)\nFOUND : T_TRUE (true)'},
    #{'input': 'bool flag = false;', 'expected_output': 'FOUND : T_BOOL (bool)\nFOUND : T_IDENTIFIER (flag)\nFOUND : T_FALSE (false)'},
    #{'input': 'int num = 123;', 'expected_output': 'FOUND : T_INT (int)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_NUMBER (123)'},
    ##{'input': 'float num = 123.456;', 'expected_output': 'FOUND : T_FLOAT (float)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_FLOAT_NUMBER (123.456)'},
    {'input': 'int identifier;', 'expected_output': 'FOUND : T_INT (int)\nFOUND : T_IDENTIFIER (identifier)'},
    {'input': 'num++;', 'expected_output': 'FOUND : T_IDENTIFIER (num)\nFOUND : T_INCREMENT (++)'},
    {'input': 'if (num <= 10) {}', 'expected_output': 'FOUND : T_IF (if)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_LESS_EQUAL (<=)\nFOUND : T_NUMBER (10)'},
    {'input': 'if (num >= 10) {}', 'expected_output': 'FOUND : T_IF (if)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_GREATER_EQUAL (>=)\nFOUND : T_NUMBER (10)'},
    {'input': 'if (num == 10) {}', 'expected_output': 'FOUND : T_IF (if)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_EQUAL (==)\nFOUND : T_NUMBER (10)'},
    {'input': 'if (num != 10) {}', 'expected_output': 'FOUND : T_IF (if)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_NOT_EQUAL (!=)\nFOUND : T_NUMBER (10)'},
    {'input': 'if (num > 10) {}', 'expected_output': 'FOUND : T_IF (if)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_GREATER (>)\nFOUND : T_NUMBER (10)'},
    {'input': 'if (num < 10) {}', 'expected_output': 'FOUND : T_IF (if)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_LESS (<)\nFOUND : T_NUMBER (10)'},
    {'input': 'if (num > 0 && num < 10) {}', 'expected_output': 'FOUND : T_IF (if)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_GREATER (>)\nFOUND : T_NUMBER (0)\nFOUND : T_AND (&&)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_LESS (<)\nFOUND : T_NUMBER (10)'},
    {'input': 'if (num < 0 || num > 10) {}', 'expected_output': 'FOUND : T_IF (if)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_LESS (<)\nFOUND : T_NUMBER (0)\nFOUND : T_OR (||)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_GREATER (>)\nFOUND : T_NUMBER (10)'},
    {'input': 'num = num + 1;', 'expected_output': 'FOUND : T_IDENTIFIER (num)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_ADD (+)\nFOUND : T_NUMBER (1)'},
    {'input': 'num = num - 1;', 'expected_output': 'FOUND : T_IDENTIFIER (num)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_SUBTRACT (-)\nFOUND : T_NUMBER (1)'},
    {'input': 'num = num / 2;', 'expected_output': 'FOUND : T_IDENTIFIER (num)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_DIVIDE (/)\nFOUND : T_NUMBER (2)'},
    {'input': 'num = num * 2;', 'expected_output': 'FOUND : T_IDENTIFIER (num)\nFOUND : T_IDENTIFIER (num)\nFOUND : T_MULTIPLY (*)\nFOUND : T_NUMBER (2)'},
   #{'input': 'char c = \'a\';', 'expected_output': 'FOUND : T_CHAR (char)\nFOUND : T_IDENTIFIER (c)\nFOUND T_CHARACTER: \'a\''},
    {'input': 'printf("Hello, world!");', 'expected_output': 'FOUND : T_PRINTF (printf)\nFOUND T_STRING: "Hello, world!"'}
]

    # Build the compiler
    build()

     # Run the test cases (in debug mode)
    failed_tests = []
    for i, test_case in enumerate(test_cases, start=1):
        print(f"Test Case {i}: {test_case['input']}")
        result = run_compiler_test(test_case['input'], debug=True)
        expected_output = test_case['expected_output']
        
        # Compare the compiler output to the expected output
        if result.strip() != expected_output.strip():
            print(f"❌ Test Case {i} Failed!\nExpected:\n{expected_output}\nGot:\n{result}")
            failed_tests.append(i)
        else:
            print(f"✅ Test Case {i} Passed!")

        print()

    if failed_tests:
        raise AssertionError(f"Test Cases {failed_tests} failed!")

if __name__ == "__main__":
    main()