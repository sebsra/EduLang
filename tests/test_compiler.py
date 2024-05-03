import subprocess
import os

def run_compiler_test(test_input):
    # Assuming the compiler is compiled into an executable named 'compiler'
    # and that it takes input from a file and outputs to stdout.
    try:
        # Saving the test input into a temporary file
        with open('temp_test_input.txt', 'w') as f:
            f.write(test_input)
        
        # Running the compiler executable and capturing output
        result = subprocess.run(['./compiler', 'temp_test_input.txt'], text=True, capture_output=True, check=True)
        return result.stdout  # return the output of the compiler
    except subprocess.CalledProcessError as e:
        return e.output  # return error output if the compiler crashes or fails

def main():
    # Define your test cases here as tuples of (input, expected_output)
    test_cases = [
        ("test input 1", "expected output 1"),
        ("test input 2", "expected output 2"),
        ("test input 3", "expected output 3"),
    ]
    
    for i, (test_input, expected_output) in enumerate(test_cases, start=1):
        print(f"Test Case {i}: Running...")
        result = run_compiler_test(test_input)
        
        # Compare the compiler output to the expected output
        if result.strip() == expected_output.strip():
            print(f"✅ Test Case {i} Passed!")
        else:
            print(f"❌ Test Case {i} Failed!\n  Expected: {expected_output}\n  Got: {result}")
        print()

if __name__ == "__main__":
    main()
