import subprocess
import os

def run_compiler_test(test_input):
    try:
        with open('temp_test_input.txt', 'w') as f:
            f.write(test_input)
        
        # Get the absolute path to the 'compiler' executable
        compiler_path = os.path.join(os.getcwd(), 'bin', 'compiler')
        
        result = subprocess.run([compiler_path, 'temp_test_input.txt'], text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.output

def main():
    test_cases = [
        {
            'input': 'test input 1',
            'expected_output': 'Found an identifier: test\nFound an identifier: input\nFound an integer: 1\n'
        },
        {
            'input': 'test input 2',
            'expected_output': 'Found an identifier: test\nFound an identifier: input\nFound an integer: 2\n'
        },
        {
            'input': 'test input 3',
            'expected_output': 'Found an identifier: test\nFound an identifier: input\nFound an integer: 3\n'
        },
        # Add more test cases as needed
    ]

    for i, test_case in enumerate(test_cases, start=1):
        print(f"Test Case {i}: Running...")
        result = run_compiler_test(test_case['input'])
        expected_output = test_case['expected_output']

        # Compare the compiler output to the expected output
        if result.strip() == expected_output.strip():
            print(f"✅ Test Case {i} Passed!")
        else:
            print(f"❌ Test Case {i} Failed!\n  Expected: {expected_output}\n  Got: {result}")
        print()

if __name__ == "__main__":
    main()