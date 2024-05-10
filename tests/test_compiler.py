import subprocess
import yaml
import textwrap 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from build_compiler import build


def run_compiler_test(test_input, debug=False):
    try:
        temp_test_input = os.path.join("tests", "temp_test_input.txt")
        with open(temp_test_input, 'w') as f:
            f.write(test_input)
        
        # Get the absolute path to the 'compiler' executable
        compiler_path = os.path.join(os.getcwd(), 'bin', 'edulang')
        
        # Add debug flag if debug is True
        command = [compiler_path, temp_test_input]
        if debug:
            command.append('-d')

        result = subprocess.run(command, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.output
    

def main():
    test_cases_yaml = os.path.join("tests", "test_cases.yaml")
    with open(test_cases_yaml, 'r') as file:
        test_cases = yaml.safe_load(file)

    # Build the compiler
    build()

     # Run the test cases (in debug mode)
    failed_tests = []

    def wrap_in_main(c_code):
        return f"""
        int main() {{
            {c_code}
            return 0;
        }}"""
    
    def wrap_output_in_main(expected_output):
        return f"""FOUND : T_INT (int)
FOUND : T_IDENTIFIER (main)
FOUND TOKEN: (
FOUND TOKEN: )
FOUND TOKEN: {{
{expected_output}
FOUND : T_RETURN (return)
FOUND : T_NUMBER (0)
FOUND TOKEN: ;
FOUND TOKEN: }}"""

    # Usage in your test loop
    for i, test_case in enumerate(test_cases, start=1):
        print(f"Test Case {i}: {test_case['input']}")
        input = wrap_in_main(test_case['input'])
        expected_output = wrap_output_in_main(test_case['expected_output'].strip())

        unfiltered_output = run_compiler_test(input, debug=True)
        # filter output to allow comparison with expected output
        output_lines = unfiltered_output.split('\n')
        filtered_lines = [line for line in output_lines if not line.startswith('Processed line')]
        filtered_output = '\n'.join(filtered_lines)
        
        # Compare the compiler output to the expected output
        if filtered_output.strip() != expected_output.strip():
            print(f"❌ Test Case {i} Failed!\n\nExpected:\n{expected_output}\n\nGot:\n{filtered_output}")
            failed_tests.append(i)
        else:
            print(f"✅ Test Case {i} Passed!")

        print()

    if failed_tests:
        raise AssertionError(f"Test Cases {failed_tests} failed!")

if __name__ == "__main__":
    main()