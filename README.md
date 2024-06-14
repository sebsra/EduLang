# EduLang
A compiler project for educational purpose, demonstrating how to use lex and yacc to build a new programming language.

run edulang.exe [filename] to compile a file and generate tree.dot file.

install graphviz and run command "dot -Tpng tree.dot -o tree.png" to convert dot to png
...Or use https://www.devtoolsdaily.com/graphviz and insert text from the tree.dot file

run edulang.exe with flag "-d" for extra debugging information

run edulang.exe with flag "-s" to print symbol table 