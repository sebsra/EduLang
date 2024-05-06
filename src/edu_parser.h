/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_SRC_EDU_PARSER_H_INCLUDED
# define YY_YY_SRC_EDU_PARSER_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    T_PRINTF = 258,                /* T_PRINTF  */
    T_SCANF = 259,                 /* T_SCANF  */
    T_INT = 260,                   /* T_INT  */
    T_FLOAT = 261,                 /* T_FLOAT  */
    T_CHAR = 262,                  /* T_CHAR  */
    T_VOID = 263,                  /* T_VOID  */
    T_RETURN = 264,                /* T_RETURN  */
    T_FOR = 265,                   /* T_FOR  */
    T_IF = 266,                    /* T_IF  */
    T_ELSE = 267,                  /* T_ELSE  */
    T_INCLUDE = 268,               /* T_INCLUDE  */
    T_TRUE = 269,                  /* T_TRUE  */
    T_FALSE = 270,                 /* T_FALSE  */
    T_NUMBER = 271,                /* T_NUMBER  */
    T_FLOAT_NUMBER = 272,          /* T_FLOAT_NUMBER  */
    T_IDENTIFIER = 273,            /* T_IDENTIFIER  */
    T_INCREMENT = 274,             /* T_INCREMENT  */
    T_LESS_EQUAL = 275,            /* T_LESS_EQUAL  */
    T_GREATER_EQUAL = 276,         /* T_GREATER_EQUAL  */
    T_EQUAL = 277,                 /* T_EQUAL  */
    T_NOT_EQUAL = 278,             /* T_NOT_EQUAL  */
    T_GREATER = 279,               /* T_GREATER  */
    T_LESS = 280,                  /* T_LESS  */
    T_AND = 281,                   /* T_AND  */
    T_OR = 282,                    /* T_OR  */
    T_ADD = 283,                   /* T_ADD  */
    T_SUBTRACT = 284,              /* T_SUBTRACT  */
    T_DIVIDE = 285,                /* T_DIVIDE  */
    T_MULTIPLY = 286,              /* T_MULTIPLY  */
    T_STRING = 287,                /* T_STRING  */
    T_CHARACTER = 288              /* T_CHARACTER  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 9 "src/edu_parser.y"

    struct {
        char name[50];
        // other members...
    } node;
    // other members...

#line 105 "src/edu_parser.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_SRC_EDU_PARSER_H_INCLUDED  */
