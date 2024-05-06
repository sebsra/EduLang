import subprocess
import sys
import os
import platform

def run_command(command):
    """ Run shell commands with error handling. """
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {' '.join(command)}: {e}", file=sys.stderr)
        sys.exit(1)

def build():
    # Determine the operating system
    os_type = platform.system()
    print(f"Detected OS: {os_type}")

    # Define the commands based on the OS
    if os_type == "Windows":
        lexer_command = ["win_flex", "-o", "src/edu_lexer.c", "src/edu_lexer.l"]
        parser_command = ["win_bison", "-d", "-o", "src/edu_parser.c", "src/edu_parser.y"]
    else:
        lexer_command = ["flex", "-o", "src/edu_lexer.c", "src/edu_lexer.l"]
        parser_command = ["bison", "-d", "-o", "src/edu_parser.c", "src/edu_parser.y"]

    # Run commands to generate lexer and parser
    print("Generating lexer...")
    run_command(lexer_command)
    print("Generating parser...")
    run_command(parser_command)

    # Compile the C files into a binary executable
    print("Compiling C files...")
    gcc_command = ["gcc", "-o", "bin/edulang", "src/edu_lexer.c", "src/edu_parser.c", "src/main.c", "-Iinclude"]
    run_command(gcc_command)
    print("Compilation successful! Executable created at bin/edulang")

if __name__ == "__main__":
    build()
