# EduLang
A compiler project for educational purpose, demonstrating how to use lex and yacc to build a new programming language.

run edulang.exe [filename] to compile a file and generate tree.dot file.

install graphviz and run command "dot -Tpng tree.dot -o tree.png" to convert dot to png
...Or use https://www.devtoolsdaily.com/graphviz and insert text from the tree.dot file

run edulang.exe with flag "-d" for extra debugging information

run edulang.exe with flag "-s" to print symbol table 

run interpreter.exe [filename] do interpret a dot
optionally you can set an include directory using the flag --include 
and --generate_video to generate an mp4 version of the interpretation (still in beta)

batch scripts are available in bin/batchScripts
