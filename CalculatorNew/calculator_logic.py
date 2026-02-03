#Importing Python's built-in math library
import math

#The return value of math.asin(x) is in radians
#math.degrees() converts radians to degrees
def arcsin(x):
    return math.degrees(math.asin(x))

def arccos(x):
    return math.degrees(math.acos(x))

def arctan(x):
    return math.degrees(math.atan(x))

#`math.radians(x)` converts degrees to radians
#`math.sin()` only accepts radians
def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

#Responsible for all logical calculations
class CalculatorLogic:
    #Receives a mathematical expression in string form
    def evaluate(self, expression: str):

        # Replace the symbols in the interface with operators that Python can recognize.
        expression = expression.replace("x", "*").replace("÷", "/")
        expression = expression.replace("^", "**")
        expression = expression.replace("²", "**2")
        expression = expression.replace("√", "math.sqrt")

        #Use eval to evaluate an expression
        return eval(expression, { #eval: Treat a string as Python code and execute it immediately.
            "math": math, #Allow the use of math.sqrt, math.pi, etc.
            "arcsin": arcsin,
            "arccos": arccos,
            "arctan": arctan,
            "sin": sin,
            "cos": cos,
            "tan": tan
        })
