import re
from math import factorial
from sympy import *
from sympy.geometry import *

# Define common symbols
x, y, z, t = symbols('x y z t')
a, b, c = symbols('a b c')

while True:
    expr = input(">>> ")

    # Replace 5! with factorial(5)
    expr = re.sub(r"(\d+)!","factorial(\\1)", expr)
    expr = expr.replace("i", "I")

    try:
        # Try eval first (for expressions like 2 + 2, sin(x), etc.)
        result = eval(expr, {"__builtins__": None, "factorial": factorial, **globals()})
        print(result)
    except SyntaxError:
        # If eval fails due to assignment like A = Point(...), use exec instead
        try:
            exec(expr, {"__builtins__": None, "factorial": factorial, **globals()})
        except Exception as e:
            print("Exec Error:", e)
    except Exception as e:
        print("Eval Error:", e)
