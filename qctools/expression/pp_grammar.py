import pyparsing as pp


__all__ = ['expression']

# normal definitions
plus = pp.Literal('+')
minus = pp.Literal('-')
mult = pp.Literal('*')
divide = pp.Literal('/')
lparent = pp.Suppress('(')
rparent = pp.Suppress(')')
# variables
number = pp.pyparsing_common.number
var = pp.Word(pp.alphas)
#
variable = pp.Or(number | var)
# Operators
operator = pp.Or(plus | minus | mult | divide)

# Simple Expressions
simple_expr_1 = pp.Group(variable + operator + variable)
simple_expr_2 = pp.Group(lparent + variable + operator + variable + rparent)
expr = pp.Or(simple_expr_2 | simple_expr_1 | variable | number)
# Combined Expression
express = pp.Or(pp.Group(expr + operator + expr) |
                pp.Group(lparent + expr + operator + expr + rparent) |
                expr)
# Full Expression
expression = pp.Or(express + operator + express |
                   expr + operator + express |
                   express + operator + expr |
                   expr + operator + expr |
                   expr)
