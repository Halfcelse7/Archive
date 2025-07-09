import re
import math
import cmath

def factorial(n):
    return math.factorial(n)

def sqrt(x):
    return (cmath if x < 0 else math).sqrt(x)

def derivative(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

def integral(f, a, b, n=1000):
    h = (b - a) / n
    result = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        result += f(a + i * h)
    return result * h

def limit(f, x, a, h=1e-5):
    return (f(a + h) + f(a - h)) / 2

def custom_eval(expression):
    expression = re.sub(r"(\d+)!", "factorial(\\1)", expression)
    return eval(expression, {
        "__builtins__": None,
        "factorial": factorial,
        "sqrt": sqrt,
        "derivative": derivative,
        "integral": integral,
        "limit": limit,
        **vars(math),
        **vars(cmath)
    })

def main():
    print("Welcome to the advanced calculator!")
    print("You can perform operations like factorial (!), sqrt, derivative, integral, and limit.")
    print("Examples:")
    print("  5! -> factorial of 5")
    print("  sqrt(4) -> square root of 4")
    print("  derivative(lambda x: x**2 + 3*x + 2, 1) -> derivative of the function at x=1")
    print("  integral(lambda x: x**2 + 3*x + 2, 0, 1) -> integral of the function from 0 to 1")
    print("  limit(lambda x: x**2 + 3*x + 2, 0) -> limit of the function as x approaches 0")
    
    while True:
        try:
            user_input = input(">>> ")
            result = custom_eval(user_input)
            print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
