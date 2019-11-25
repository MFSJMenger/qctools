import pyparsing as pp


__all__ = ['EXPRESSION']

# normal definitions
PLUS = pp.Literal('+')
MINUS = pp.Literal('-')
MULT = pp.Literal('*')
DIVIDE = pp.Literal('/')
LPARENT = pp.Suppress('(')
RPARENT = pp.Suppress(')')
# variables
NUMBER = pp.pyparsing_common.number
VAR = pp.Word(pp.alphas)
#
VARIABLE = pp.Or(NUMBER | VAR)
# Operators
OPERATOR = pp.Or(PLUS | MINUS | MULT | DIVIDE)

# Simple Expressions
BASE_EXPRESSION = pp.Group(VARIABLE + OPERATOR + VARIABLE)
BASE_EXPRESSION_PARENT = pp.Group(LPARENT + VARIABLE + OPERATOR + VARIABLE + RPARENT)
EXPR = pp.Or(BASE_EXPRESSION | BASE_EXPRESSION_PARENT | VARIABLE | NUMBER)
# Combined Expression
EXPRESS = pp.Or(pp.Group(EXPR + OPERATOR + EXPR)
                | pp.Group(LPARENT + EXPR + OPERATOR + EXPR + RPARENT)
                | EXPR)
# Full Expression
EXPRESSION = pp.Or(EXPRESS + OPERATOR + EXPRESS
                   | EXPR + OPERATOR + EXPRESS
                   | EXPRESS + OPERATOR + EXPR
                   | EXPR + OPERATOR + EXPR
                   | EXPR)
