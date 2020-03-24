from ..mathexpression import MathExpression


def test_number():
    expr = MathExpression(100)
    assert expr.eval() == 100

def test_string_number():
    expr = MathExpression("100")
    assert expr.eval() == 100

def test_addition():
    expr = MathExpression("90+20")
    assert expr.eval() == 110

def test_subtraction():
    expr = MathExpression("90-20")
    assert expr.eval() == 70

def test_mult():
    expr = MathExpression("88*10")
    assert expr.eval() == 880

def test_division():
    expr = MathExpression("88//11")
    assert expr.eval() == 8

def test_variables():
    expr = MathExpression("NAtoms")
    assert expr.eval({'NAtoms': 70}) == 70

def test_variable_mult():
    expr = MathExpression("3*NAtoms")
    assert expr.eval({'NAtoms': 70}) == 210

def test_variables_mult():
    expr = MathExpression("Three*NAtoms")
    assert expr.eval({'NAtoms': 70, 'Three': 3}) == 210

def test_single_value():
    expr = MathExpression(1)
    assert expr.eval() == 1

def test_single_function():
    expr = """
def eval():
    return 100

eval() 
"""
    expr = MathExpression(expr)
    assert expr.eval() == 100

def test_complex_expr():
    expr = """

def mult(a, b):
    return a*b

def eval(c, d):
    return int(mult(c, d) + 1.0)

eval(c, d) 
"""
    expr = MathExpression(expr)
    assert expr.eval({'c': 21, 'd': 10}) == 211
