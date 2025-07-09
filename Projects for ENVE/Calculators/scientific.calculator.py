import math

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Error! Division by zero."

def power(x, y):
    return x ** y

def square_root(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return "Error! Square root of negative number."

def percentage(x, y):
    return (x * y) / 100

def factorial(x):
    if x >= 0 and int(x) == x:
        return math.factorial(int(x))
    else:
        return "Error! Factorial of non-integer or negative number."

def logarithm(x, base):
    if x > 0 and base > 0 and base != 1:
        return math.log(x, base)
    else:
        return "Error! Logarithm with non-positive number or invalid base."

def natural_log(x):
    if x > 0:
        return math.log(x)
    else:
        return "Error! Natural logarithm of non-positive number."

def sin(x):
    return math.sin(math.radians(x))

def cosine(x):
    return math.cos(math.radians(x))

def tangent(x):
    return math.tan(math.radians(x))

def cot(x):
    if x != 0:
        return 1 / math.tan(math.radians(x))
    else:
        return "Error! Cotangent of zero is undefined."

def sec(x):
    if x % 90 == 0 and x % 180 != 0:
        return "Error! Secant of undefined value."
    else:
        return 1 / math.cos(math.radians(x))

def cosec(x):
    if x != 0:
        return 1 / math.sin(math.radians(x))
    else:
        return "Error! Cosecant of zero is undefined."

def get_number(prompt):
    value = input(prompt)
    if value.lower() == 'pi':
        return math.pi
    elif value.lower() == 'e':
        return math.e
    else:
        return float(value)

def calculator():
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Square Root")
    print("7. Percentage")
    print("8. Factorial")
    print("9. Logarithm")
    print("10. Natural Log (ln)")
    print("11. Sin")
    print("12. Cosine")
    print("13. Tangent")
    print("14. Cotangent")
    print("15. Secant")
    print("16. Cosecant")

    choice = input("Enter choice (1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16): ")

    if choice in ['1', '2', '3', '4', '5', '7']:
        num1 = get_number("Enter first number (or 'pi' or 'e'): ")
        num2 = get_number("Enter second number (or 'pi' or 'e'): ")

        if choice == '1':
            print(f"{num1} + {num2} = {add(num1, num2)}")
        elif choice == '2':
            print(f"{num1} - {num2} = {subtract(num1, num2)}")
        elif choice == '3':
            print(f"{num1} * {num2} = {multiply(num1, num2)}")
        elif choice == '4':
            print(f"{num1} / {num2} = {divide(num1, num2)}")
        elif choice == '5':
            print(f"{num1} ^ {num2} = {power(num1, num2)}")
        elif choice == '7':
            print(f"{num1}% of {num2} = {percentage(num1, num2)}")
    elif choice in ['6', '8', '10']:
        num = get_number("Enter number (or 'pi' or 'e'): ")

        if choice == '6':
            print(f"√{num} = {square_root(num)}")
        elif choice == '8':
            print(f"{num}! = {factorial(num)}")
        elif choice == '10':
            print(f"ln({num}) = {natural_log(num)}")
    elif choice == '9':
        base = get_number("Enter the base for logarithm: ")
        num = get_number("Enter number (or 'pi' or 'e'): ")
        print(f"log base {base} of {num} = {logarithm(num, base)}")
    elif choice in ['11', '12', '13', '14', '15', '16']:
        num = float(input("Enter degree value: "))
        
        if choice == '11':
            print(f"sin({num} degrees) = {sin(num)}")
        elif choice == '12':
            print(f"cos({num} degrees) = {cosine(num)}")
        elif choice == '13':
            print(f"tan({num} degrees) = {tangent(num)}")
        elif choice == '14':
            print(f"cot({num} degrees) = {cot(num)}")
        elif choice == '15':
            print(f"sec({num} degrees) = {sec(num)}")
        elif choice == '16':
            print(f"cosec({num} degrees) = {cosec(num)}")
    else:
        print("Invalid input")

calculator()
